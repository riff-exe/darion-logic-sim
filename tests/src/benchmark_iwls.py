"""
benchmark_iwls.py  (Multi-Engine Comparison: Python, Cython, Icarus, Verilator on IWLS 2005)
=============================================================================================
Unified benchmark runner comparing simulation engines on IWLS 2005 sequential datasets:
  1. Pure Python Engine        (SIMULATE mode)
  2. Cython Reactor Propagate  (SIMULATE mode / BFS Wavefront)
  3. Cython Reactor Sweep      (COMPILE  mode / Topological Forward-Pass)
  4. Cython Reactor OOP        (SIMULATE mode)
  5. Icarus Verilog            (iverilog + vvp + optional VPI inner-loop timer)
  6. Verilator C++             (verilator -O3 compiled cycle-accurate C++)

Key Capabilities:
-----------------
  - Full Cadence GSCLib 3.0 standard-cell library support (37 cell types, AOI, OAI, MUX, etc.)
  - Multi-bit bus port handling ([msb:lsb] vectors and scalar expansion)
  - Escaped identifier resolution (e.g. \\stato[0] )
  - Clock-aware paired vector execution (setup @ CLK=0, trigger @ CLK=1)
  - 50-cycle warmup to flush DFF states
  - Isolated subprocess worker execution to eliminate Cython state pollution and memory leaks
  - Speedup summary vs. Icarus Verilog VPI baseline
"""

import os
import re
import sys
import time
import datetime
import json
import random
import argparse
import gc
import subprocess
import shutil
import asyncio
import math
from pathlib import Path

_SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
_TESTS_DIR    = os.path.dirname(_SCRIPT_DIR)
_PROJECT_ROOT = os.path.dirname(_TESTS_DIR)

sys.path.insert(0, _SCRIPT_DIR)
sys.path.insert(0, _TESTS_DIR)
sys.path.insert(0, _PROJECT_ROOT)

def send_perf_ctrl(cmd):
    try:
        if os.path.exists("/tmp/rx_perf_ctrl"):
            flags = os.O_WRONLY
            if hasattr(os, 'O_NONBLOCK'):
                flags |= os.O_NONBLOCK
            fd = os.open("/tmp/rx_perf_ctrl", flags)
            os.write(fd, (cmd + "\n").encode())
            os.close(fd)
    except Exception:
        pass

try:
    from iwls_sequential_harness import (
        run_icarus_harness_iwls,
        run_verilator_harness_iwls,
        parse_iwls_ports,
        _VPI_DIR,
        _VPI_TIMER_VPI,
    )
except ImportError:
    try:
        from tests.src.iwls_sequential_harness import (
            run_icarus_harness_iwls,
            run_verilator_harness_iwls,
            parse_iwls_ports,
            _VPI_DIR,
            _VPI_TIMER_VPI,
        )
    except ImportError:
        try:
            from tests.iwls_sequential_harness import (
                run_icarus_harness_iwls,
                run_verilator_harness_iwls,
                parse_iwls_ports,
                _VPI_DIR,
                _VPI_TIMER_VPI,
            )
        except ImportError:
            run_icarus_harness_iwls    = None
            run_verilator_harness_iwls = None
            parse_iwls_ports           = None
            _VPI_DIR                   = ""
            _VPI_TIMER_VPI             = ""


# ===========================================================================
# 1. INTERNAL WORKER — IWLSVerilogRunner (Engine / Reactor)
# ===========================================================================

class IWLSVerilogRunner:
    """
    Parses an IWLS 2005 standard-cell netlist and benchmarks it using
    either the Python Engine or Cython Reactor.
    """

    def __init__(self, v_file_path, circuit_cls, const_mod, is_reactor=True, is_oop=False, mode="engine", use_optimize=True):
        self.filepath = v_file_path
        self.mode = mode
        self.Circuit = circuit_cls
        self.const   = const_mod
        self.circuit = self.Circuit()
        self.circuit.simulate(self.const.DESIGN)
        self.is_reactor = is_reactor
        self.is_oop = is_oop
        self.use_optimize = use_optimize
        self.const_1_node = None
        self.const_0_node = None

        self.nodes = {}
        self.outputs = []
        self.input_vars = []
        self.dff_connections = []
        self.dff_crct = None

        # Load DFF.json from common locations
        for p in [
            os.path.join(_TESTS_DIR, "DFFSR.json"),
            os.path.join(_SCRIPT_DIR, "DFFSR.json"),
            os.path.join(_PROJECT_ROOT, "tests", "DFFSR.json"),
            os.path.join(_PROJECT_ROOT, "DFFSR.json"),
            "tests/DFFSR.json",
            "DFFSR.json",
            os.path.join(_TESTS_DIR, "DFF.json"),
            os.path.join(_SCRIPT_DIR, "DFF.json"),
            os.path.join(_PROJECT_ROOT, "tests", "DFF.json"),
            os.path.join(_PROJECT_ROOT, "DFF.json"),
            "tests/DFF.json",
            "DFF.json",
        ]:
            if os.path.exists(p):
                try:
                    self.dff_crct = self.circuit.get_ic(p)
                    break
                except Exception:
                    pass

        self._parse_verilog(v_file_path)
        self.output_objects = []
        for p in self.outputs:
            node = self.nodes.get(p + "_OUTPIN") or self.nodes.get(p)
            if node is not None:
                self.output_objects.append(node)

        if getattr(self, 'const_1_node', None) is not None:
            self.const_1_node.value = self.const.HIGH
            if hasattr(self.circuit, 'toggle'):
                target = self.const_1_node if (self.is_oop or not self.is_reactor) else self.const_1_node.location
                self.circuit.toggle(target, self.const.HIGH)
        if getattr(self, 'const_0_node', None) is not None:
            self.const_0_node.value = self.const.LOW
            if hasattr(self.circuit, 'toggle'):
                target = self.const_0_node if (self.is_oop or not self.is_reactor) else self.const_0_node.location
                self.circuit.toggle(target, self.const.LOW)

    def _find_clock_var(self):
        """Return the clock variable node, prioritizing the dominant clock driving the most flip-flops."""
        candidates = []
        for var in self.input_vars:
            name = getattr(var, 'custom_name', '') or getattr(var, 'codename', '')
            if isinstance(name, bytes):
                name = name.decode('utf-8', errors='ignore')
            clean = name[3:] if name.startswith("IN_") else name
            base = clean.split('[')[0].strip().lower()
            if base in ('ck', 'clk', 'clock', 'g0') or 'clk' in base or 'clock' in base:
                candidates.append((var, clean))

        if not candidates:
            return None
        if len(candidates) == 1:
            return candidates[0][0]

        ck_counts = {}
        for _, _, ck_wire, _, _ in self.dff_connections:
            ck_counts[ck_wire] = ck_counts.get(ck_wire, 0) + 1

        best_var = candidates[0][0]
        best_count = -1
        for var, clean in candidates:
            cnt = ck_counts.get(clean, 0)
            if cnt > best_count:
                best_count = cnt
                best_var = var
        return best_var

    def _clean_ident(self, s: str) -> str:
        """Strip leading/trailing whitespace from identifier; preserve escaped prefix."""
        s = s.strip()
        return s

    def _parse_verilog(self, filepath):
        json_path = filepath if filepath.endswith('.json') else filepath.replace('.v', '.json')
        if os.path.exists(json_path) and hasattr(self.circuit, 'readfromjson'):
            self.circuit.readfromjson(json_path)
            v_path = filepath if filepath.endswith('.v') else filepath.replace('.json', '.v')
            if os.path.exists(v_path) and parse_iwls_ports:
                _, _, flat_inputs, flat_outputs, _, _ = parse_iwls_ports(v_path)
            else:
                flat_inputs, flat_outputs = [], []

            var_list = self.circuit.get_variables() if hasattr(self.circuit, 'get_variables') else []
            var_dict = {}
            for v in var_list:
                name_str = getattr(v, 'custom_name', None) or getattr(v, 'codename', None) or str(v)
                if isinstance(name_str, bytes):
                    name_str = name_str.decode('utf-8', errors='ignore')
                var_dict[name_str] = v

            if flat_inputs:
                for inp in flat_inputs:
                    expected_name = f"IN_{inp}"
                    if expected_name in var_dict:
                        self.input_vars.append(var_dict[expected_name])
                    else:
                        for k, v in var_dict.items():
                            if inp in k:
                                self.input_vars.append(v)
                                break
            else:
                for name_str, v in sorted(var_dict.items()):
                    if name_str.startswith("IN_"):
                        self.input_vars.append(v)

            if flat_outputs:
                for outp in flat_outputs:
                    self.outputs.append(outp)
            else:
                for comp in (self.circuit.get_components() if hasattr(self.circuit, 'get_components') else []):
                    name_str = getattr(comp, 'custom_name', None) or getattr(comp, 'codename', None) or str(comp)
                    if isinstance(name_str, bytes):
                        name_str = name_str.decode('utf-8', errors='ignore')
                    if name_str.startswith("OUT_"):
                        p_name = name_str[4:].replace("_OUTPIN", "")
                        if p_name not in self.outputs:
                            self.outputs.append(p_name)

            for comp in (self.circuit.get_components() if hasattr(self.circuit, 'get_components') else []):
                name_str = getattr(comp, 'custom_name', None) or getattr(comp, 'codename', None) or str(comp)
                if isinstance(name_str, bytes):
                    name_str = name_str.decode('utf-8', errors='ignore')
                if name_str.startswith("IN_"):
                    self.nodes[name_str[3:]] = comp
                elif name_str.startswith("OUT_"):
                    clean = name_str[4:]
                    if clean.endswith("_OUTPIN"):
                        clean = clean[:-7]
                    self.nodes[clean] = comp
                    self.nodes[clean + "_OUTPIN"] = comp
                elif name_str == "CONST_1":
                    self.const_1_node = comp
                    self.nodes["1'b1"] = comp
                elif name_str == "CONST_0":
                    self.const_0_node = comp
                    self.nodes["1'b0"] = comp
                else:
                    self.nodes[name_str] = comp

            if self.use_optimize and hasattr(self.circuit, 'optimize'):
                self.circuit.optimize()
            return

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Strip comments
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        content = re.sub(r'//.*', '', content)

        # Isolate top-level circuit module
        module_body = content
        for m in re.finditer(r'\bmodule\s+([a-zA-Z0-9_]+)\s*\((.*?)\);', content, flags=re.DOTALL):
            m_name = m.group(1).strip()
            if m_name.lower() not in ('dff', 'dffsrx1', 'dffx1', 'sdffsrx1', 'invx1', 'bufx1'):
                idx_start = m.start()
                end_m = re.search(r'\bendmodule\b', content[idx_start:], flags=re.DOTALL)
                if end_m:
                    module_body = content[idx_start : idx_start + end_m.end()]
                else:
                    module_body = content[idx_start:]
                break

        statements = [s.strip() for s in module_body.split(';') if s.strip()]

        def get_const_node(val_str):
            val_str = val_str.strip()
            if val_str in ("1'b1", "1'h1", "1'd1", "1"):
                if not getattr(self, 'const_1_node', None):
                    self.const_1_node = self.circuit.getcomponent(self.const.VARIABLE_ID)
                    self.const_1_node.rename("CONST_1")
                    self.const_1_node.value = self.const.HIGH
                    for k in ("1'b1", "1'h1", "1'd1", "1"):
                        self.nodes[k] = self.const_1_node
                return self.const_1_node
            elif val_str in ("1'b0", "1'h0", "1'd0", "0", "1'bx", "1'bX", "1'bz", "1'bZ"):
                if not getattr(self, 'const_0_node', None):
                    self.const_0_node = self.circuit.getcomponent(self.const.VARIABLE_ID)
                    self.const_0_node.rename("CONST_0")
                    self.const_0_node.value = self.const.LOW
                    for k in ("1'b0", "1'h0", "1'd0", "0", "1'bx", "1'bX", "1'bz", "1'bZ"):
                        self.nodes[k] = self.const_0_node
                return self.const_0_node
            return None

        # Pre-seed constants
        get_const_node("1'b1")
        get_const_node("1'b0")

        def add_input_var(var_name):
            var_name = self._clean_ident(var_name)
            if not var_name or var_name in self.nodes:
                return
            var_node = self.circuit.getcomponent(self.const.VARIABLE_ID)
            var_node.rename(f"IN_{var_name}")
            self.nodes[var_name] = var_node
            self.input_vars.append(var_node)

        def add_output_pin(out_name):
            out_name = self._clean_ident(out_name)
            if not out_name or out_name + "_OUTPIN" in self.nodes:
                return
            out_node = self.circuit.getcomponent(self.const.IC_OUTPUT_PIN_ID)
            out_node.rename(f"OUT_{out_name}")
            self.nodes[out_name + "_OUTPIN"] = out_node
            self.outputs.append(out_name)
            connections.append((out_node, [out_name]))

        connections = []
        assign_statements = []

        # Pass 1: Declare input / output ports and create gate components
        for stmt in statements:
            # Handle continuous assignments (e.g. assign a = b, c = 1'b0;)
            m_assign = re.match(r'^\s*assign\s+(.*)', stmt, re.IGNORECASE | re.DOTALL)
            if m_assign:
                assign_body = m_assign.group(1).strip()
                for part in assign_body.split(','):
                    if '=' in part:
                        tgt_part, src_part = part.split('=', 1)
                        tgt = self._clean_ident(tgt_part)
                        src = self._clean_ident(src_part)
                        if src.startswith('(') and src.endswith(')'):
                            src = src[1:-1].strip()
                        if tgt and src:
                            assign_statements.append((tgt, src))
                            get_const_node(src)
                continue

            # Handle input port declarations
            m_inp = re.match(r'^input\s+(.*)', stmt, re.DOTALL)
            if m_inp:
                decl = m_inp.group(1).strip()
                m_rng = re.match(r'^\[\s*(\d+)\s*:\s*(\d+)\s*\]\s*(.*)', decl, re.DOTALL)
                if m_rng:
                    msb, lsb = int(m_rng.group(1)), int(m_rng.group(2))
                    names = [n.strip() for n in m_rng.group(3).split(',') if n.strip()]
                    for name in names:
                        step = 1 if msb <= lsb else -1
                        for bit in range(msb, lsb + step, step):
                            add_input_var(f"{name}[{bit}]")
                else:
                    for name in [n.strip() for n in decl.split(',') if n.strip()]:
                        add_input_var(name)
                continue

            # Handle output port declarations
            m_out = re.match(r'^output\s+(.*)', stmt, re.DOTALL)
            if m_out:
                decl = m_out.group(1).strip()
                m_rng = re.match(r'^\[\s*(\d+)\s*:\s*(\d+)\s*\]\s*(.*)', decl, re.DOTALL)
                if m_rng:
                    msb, lsb = int(m_rng.group(1)), int(m_rng.group(2))
                    names = [n.strip() for n in m_rng.group(3).split(',') if n.strip()]
                    for name in names:
                        step = 1 if msb <= lsb else -1
                        for bit in range(msb, lsb + step, step):
                            add_output_pin(f"{name}[{bit}]")
                else:
                    for name in [n.strip() for n in decl.split(',') if n.strip()]:
                        add_output_pin(name)
                continue

            if stmt.startswith(('wire ', 'module ', 'endmodule', 'reg ')):
                continue

            # Gate / Standard-cell instantiation
            paren_idx  = stmt.find('(')
            rparen_idx = stmt.rfind(')')
            if paren_idx == -1 or rparen_idx == -1 or rparen_idx <= paren_idx:
                continue

            header = stmt[:paren_idx].strip()
            tokens = header.split()
            if not tokens:
                continue

            cell_type = tokens[0].upper()
            inst_name = tokens[1] if len(tokens) > 1 else f"inst_{len(self.nodes)}"
            ports_str = stmt[paren_idx + 1 : rparen_idx]

            named_ports = {}
            for pm in re.finditer(r'\.\s*([a-zA-Z0-9_]+)\s*\(\s*([^)]*)\s*\)', ports_str):
                port_pin = pm.group(1).strip().upper()
                wire_ref = self._clean_ident(pm.group(2))
                named_ports[port_pin] = wire_ref

            # Ensure constants referenced in ports are registered
            for w in named_ports.values():
                if w:
                    get_const_node(w)

            # ── 1. Sequential Flip-Flops (DFFX1, DFFSRX1, SDFFSRX1) ─────────
            if cell_type.startswith('DFF') or cell_type.startswith('SDFF'):
                if not self.dff_crct:
                    raise RuntimeError("DFFSR.json or DFF.json is required for sequential logic simulation.")

                dff_inst = self.circuit.load_ic(self.dff_crct)
                if hasattr(dff_inst, 'rename'):
                    dff_inst.rename(f"DFF_{inst_name}")
                else:
                    dff_inst.custom_name = f"DFF_{inst_name}"

                q_wire  = named_ports.get('Q')
                qn_wire = named_ports.get('QN')
                d_wire  = named_ports.get('D')
                ck_wire = named_ports.get('CK', named_ports.get('CLK', named_ports.get('C')))
                rn_wire = named_ports.get('RN', named_ports.get('RESET_N', named_ports.get('RST_N', named_ports.get('CLR_N'))))
                sn_wire = named_ports.get('SN', named_ports.get('SET_N', named_ports.get('PRE_N')))

                # Handle Scan Flip-Flop (SDFFSRX1): multiplex D with SI via SE: D_eff = SE ? SI : D
                se_wire = named_ports.get('SE')
                si_wire = named_ports.get('SI')
                if se_wire and si_wire and d_wire:
                    not_se = self.circuit.getcomponent(self.const.NOT_ID)
                    and_si = self.circuit.getcomponent(self.const.AND_ID)
                    and_d  = self.circuit.getcomponent(self.const.AND_ID)
                    or_d   = self.circuit.getcomponent(self.const.OR_ID)
                    if hasattr(self.circuit, 'setlimits'):
                        self.circuit.setlimits(and_si, 2)
                        self.circuit.setlimits(and_d, 2)
                        self.circuit.setlimits(or_d, 2)
                    connections.append((not_se, [se_wire]))
                    connections.append((and_si, [si_wire, se_wire]))
                    connections.append((and_d,  [d_wire, not_se]))
                    connections.append((or_d,   [and_si, and_d]))
                    d_wire = or_d

                # Map outputs (outputs[0] = Q, outputs[1] = QN)
                if q_wire:
                    self.nodes[q_wire] = dff_inst.outputs[0]
                if qn_wire:
                    self.nodes[qn_wire] = dff_inst.outputs[1]

                self.dff_connections.append((dff_inst, d_wire, ck_wire, rn_wire, sn_wire))
                continue

            # ── 2. Inverters & Buffers ─────────────────────────────────────────
            if cell_type.startswith('INV'):
                g = self.circuit.getcomponent(self.const.NOT_ID)
                y = named_ports.get('Y')
                a = named_ports.get('A')
                if y:
                    self.nodes[y] = g
                    connections.append((g, [a]))
                continue

            if cell_type.startswith('BUF') or cell_type.startswith('CLKBUF') or cell_type.startswith('TBUF'):
                g = self.circuit.getcomponent(self.const.BUFFER_ID)
                y = named_ports.get('Y')
                a = named_ports.get('A')
                if y:
                    self.nodes[y] = g
                    connections.append((g, [a]))
                continue

            if cell_type.startswith('TINV'):
                g = self.circuit.getcomponent(self.const.NOT_ID)
                y = named_ports.get('Y')
                a = named_ports.get('A')
                if y:
                    self.nodes[y] = g
                    connections.append((g, [a]))
                continue

            # ── 3. Basic Gates (AND, OR, NAND, NOR, XOR) ─────────────────────
            if cell_type.startswith('AND2'):
                g = self.circuit.getcomponent(self.const.AND_ID)
                if hasattr(self.circuit, 'setlimits'):
                    self.circuit.setlimits(g, 2)
                y = named_ports.get('Y')
                if y:
                    self.nodes[y] = g
                    connections.append((g, [named_ports.get('A'), named_ports.get('B')]))
                continue

            if cell_type.startswith('OR2'):
                g = self.circuit.getcomponent(self.const.OR_ID)
                if hasattr(self.circuit, 'setlimits'):
                    self.circuit.setlimits(g, 2)
                y = named_ports.get('Y')
                if y:
                    self.nodes[y] = g
                    connections.append((g, [named_ports.get('A'), named_ports.get('B')]))
                continue

            if cell_type.startswith('OR4'):
                g = self.circuit.getcomponent(self.const.OR_ID)
                if hasattr(self.circuit, 'setlimits'):
                    self.circuit.setlimits(g, 4)
                y = named_ports.get('Y')
                if y:
                    self.nodes[y] = g
                    connections.append((g, [named_ports.get('A'), named_ports.get('B'), named_ports.get('C'), named_ports.get('D')]))
                continue

            if cell_type.startswith('NAND2'):
                g = self.circuit.getcomponent(self.const.NAND_ID)
                if hasattr(self.circuit, 'setlimits'):
                    self.circuit.setlimits(g, 2)
                y = named_ports.get('Y')
                if y:
                    self.nodes[y] = g
                    connections.append((g, [named_ports.get('A'), named_ports.get('B')]))
                continue

            if cell_type.startswith('NAND3'):
                g = self.circuit.getcomponent(self.const.NAND_ID)
                if hasattr(self.circuit, 'setlimits'):
                    self.circuit.setlimits(g, 3)
                y = named_ports.get('Y')
                if y:
                    self.nodes[y] = g
                    connections.append((g, [named_ports.get('A'), named_ports.get('B'), named_ports.get('C')]))
                continue

            if cell_type.startswith('NAND4'):
                g = self.circuit.getcomponent(self.const.NAND_ID)
                if hasattr(self.circuit, 'setlimits'):
                    self.circuit.setlimits(g, 4)
                y = named_ports.get('Y')
                if y:
                    self.nodes[y] = g
                    connections.append((g, [named_ports.get('A'), named_ports.get('B'), named_ports.get('C'), named_ports.get('D')]))
                continue

            if cell_type.startswith('NOR2'):
                g = self.circuit.getcomponent(self.const.NOR_ID)
                if hasattr(self.circuit, 'setlimits'):
                    self.circuit.setlimits(g, 2)
                y = named_ports.get('Y')
                if y:
                    self.nodes[y] = g
                    connections.append((g, [named_ports.get('A'), named_ports.get('B')]))
                continue

            if cell_type.startswith('NOR3'):
                g = self.circuit.getcomponent(self.const.NOR_ID)
                if hasattr(self.circuit, 'setlimits'):
                    self.circuit.setlimits(g, 3)
                y = named_ports.get('Y')
                if y:
                    self.nodes[y] = g
                    connections.append((g, [named_ports.get('A'), named_ports.get('B'), named_ports.get('C')]))
                continue

            if cell_type.startswith('NOR4'):
                g = self.circuit.getcomponent(self.const.NOR_ID)
                if hasattr(self.circuit, 'setlimits'):
                    self.circuit.setlimits(g, 4)
                y = named_ports.get('Y')
                if y:
                    self.nodes[y] = g
                    connections.append((g, [named_ports.get('A'), named_ports.get('B'), named_ports.get('C'), named_ports.get('D')]))
                continue

            if cell_type.startswith('XOR2'):
                g = self.circuit.getcomponent(self.const.XOR_ID)
                if hasattr(self.circuit, 'setlimits'):
                    self.circuit.setlimits(g, 2)
                y = named_ports.get('Y')
                if y:
                    self.nodes[y] = g
                    connections.append((g, [named_ports.get('A'), named_ports.get('B')]))
                continue

            # ── 4. Complex AOI Gates ──────────────────────────────────────────
            if cell_type.startswith('AOI21'):
                # Y = ~((A0 & A1) | B0) -> and = AND(A0, A1), Y = NOR(and, B0)
                and_g = self.circuit.getcomponent(self.const.AND_ID)
                nor_g = self.circuit.getcomponent(self.const.NOR_ID)
                if hasattr(self.circuit, 'setlimits'):
                    self.circuit.setlimits(and_g, 2)
                    self.circuit.setlimits(nor_g, 2)
                y = named_ports.get('Y')
                if y:
                    self.nodes[y] = nor_g
                    connections.append((and_g, [named_ports.get('A0'), named_ports.get('A1')]))
                    connections.append((nor_g, [and_g, named_ports.get('B0')]))
                continue

            if cell_type.startswith('AOI22'):
                # Y = ~((A0 & A1) | (B0 & B1))
                and1  = self.circuit.getcomponent(self.const.AND_ID)
                and2  = self.circuit.getcomponent(self.const.AND_ID)
                nor_g = self.circuit.getcomponent(self.const.NOR_ID)
                if hasattr(self.circuit, 'setlimits'):
                    self.circuit.setlimits(and1, 2)
                    self.circuit.setlimits(and2, 2)
                    self.circuit.setlimits(nor_g, 2)
                y = named_ports.get('Y')
                if y:
                    self.nodes[y] = nor_g
                    connections.append((and1, [named_ports.get('A0'), named_ports.get('A1')]))
                    connections.append((and2, [named_ports.get('B0'), named_ports.get('B1')]))
                    connections.append((nor_g, [and1, and2]))
                continue

            # ── 5. Complex OAI Gates ──────────────────────────────────────────
            if cell_type.startswith('OAI21'):
                # Y = ~((A0 | A1) & B0) -> or = OR(A0, A1), Y = NAND(or, B0)
                or_g   = self.circuit.getcomponent(self.const.OR_ID)
                nand_g = self.circuit.getcomponent(self.const.NAND_ID)
                if hasattr(self.circuit, 'setlimits'):
                    self.circuit.setlimits(or_g, 2)
                    self.circuit.setlimits(nand_g, 2)
                y = named_ports.get('Y')
                if y:
                    self.nodes[y] = nand_g
                    connections.append((or_g, [named_ports.get('A0'), named_ports.get('A1')]))
                    connections.append((nand_g, [or_g, named_ports.get('B0')]))
                continue

            if cell_type.startswith('OAI22'):
                # Y = ~((A0 | A1) & (B0 | B1))
                or1    = self.circuit.getcomponent(self.const.OR_ID)
                or2    = self.circuit.getcomponent(self.const.OR_ID)
                nand_g = self.circuit.getcomponent(self.const.NAND_ID)
                if hasattr(self.circuit, 'setlimits'):
                    self.circuit.setlimits(or1, 2)
                    self.circuit.setlimits(or2, 2)
                    self.circuit.setlimits(nand_g, 2)
                y = named_ports.get('Y')
                if y:
                    self.nodes[y] = nand_g
                    connections.append((or1, [named_ports.get('A0'), named_ports.get('A1')]))
                    connections.append((or2, [named_ports.get('B0'), named_ports.get('B1')]))
                    connections.append((nand_g, [or1, or2]))
                continue

            if cell_type.startswith('OAI33'):
                # Y = ~((A0 | A1 | A2) & (B0 | B1 | B2))
                or1    = self.circuit.getcomponent(self.const.OR_ID)
                or2    = self.circuit.getcomponent(self.const.OR_ID)
                nand_g = self.circuit.getcomponent(self.const.NAND_ID)
                if hasattr(self.circuit, 'setlimits'):
                    self.circuit.setlimits(or1, 3)
                    self.circuit.setlimits(or2, 3)
                    self.circuit.setlimits(nand_g, 2)
                y = named_ports.get('Y')
                if y:
                    self.nodes[y] = nand_g
                    connections.append((or1, [named_ports.get('A0'), named_ports.get('A1'), named_ports.get('A2')]))
                    connections.append((or2, [named_ports.get('B0'), named_ports.get('B1'), named_ports.get('B2')]))
                    connections.append((nand_g, [or1, or2]))
                continue

            # ── 6. Multiplexer & Adders ───────────────────────────────────────
            if cell_type.startswith('MX2'):
                # Y = S0 ? B : A  == (A & ~S0) | (B & S0)
                not_s = self.circuit.getcomponent(self.const.NOT_ID)
                and1  = self.circuit.getcomponent(self.const.AND_ID)
                and2  = self.circuit.getcomponent(self.const.AND_ID)
                or_g  = self.circuit.getcomponent(self.const.OR_ID)
                if hasattr(self.circuit, 'setlimits'):
                    self.circuit.setlimits(and1, 2)
                    self.circuit.setlimits(and2, 2)
                    self.circuit.setlimits(or_g, 2)
                y = named_ports.get('Y')
                if y:
                    self.nodes[y] = or_g
                    connections.append((not_s, [named_ports.get('S0')]))
                    connections.append((and1, [named_ports.get('A'), not_s]))
                    connections.append((and2, [named_ports.get('B'), named_ports.get('S0')]))
                    connections.append((or_g, [and1, and2]))
                continue

            if cell_type.startswith('ADDH'):
                # Half Adder: CO = A & B, S = A ^ B
                and_g = self.circuit.getcomponent(self.const.AND_ID)
                xor_g = self.circuit.getcomponent(self.const.XOR_ID)
                if hasattr(self.circuit, 'setlimits'):
                    self.circuit.setlimits(and_g, 2)
                    self.circuit.setlimits(xor_g, 2)
                co = named_ports.get('CO')
                s  = named_ports.get('S')
                a  = named_ports.get('A')
                b  = named_ports.get('B')
                if co:
                    self.nodes[co] = and_g
                    connections.append((and_g, [a, b]))
                if s:
                    self.nodes[s] = xor_g
                    connections.append((xor_g, [a, b]))
                continue

            if cell_type.startswith('ADDF'):
                # Full Adder: S = A ^ B ^ CI, CO = (A & B) | ((A ^ B) & CI)
                xor1  = self.circuit.getcomponent(self.const.XOR_ID)
                xor2  = self.circuit.getcomponent(self.const.XOR_ID)
                and1  = self.circuit.getcomponent(self.const.AND_ID)
                and2  = self.circuit.getcomponent(self.const.AND_ID)
                or_g  = self.circuit.getcomponent(self.const.OR_ID)
                if hasattr(self.circuit, 'setlimits'):
                    self.circuit.setlimits(xor1, 2)
                    self.circuit.setlimits(xor2, 2)
                    self.circuit.setlimits(and1, 2)
                    self.circuit.setlimits(and2, 2)
                    self.circuit.setlimits(or_g, 2)
                s  = named_ports.get('S')
                co = named_ports.get('CO')
                a  = named_ports.get('A')
                b  = named_ports.get('B')
                ci = named_ports.get('CI')
                connections.append((xor1, [a, b]))
                connections.append((xor2, [xor1, ci]))
                connections.append((and1, [a, b]))
                connections.append((and2, [xor1, ci]))
                connections.append((or_g, [and1, and2]))
                if s:
                    self.nodes[s] = xor2
                if co:
                    self.nodes[co] = or_g
                continue

            # Fallback: Primitive Verilog gates
            prim_map = {
                'AND': self.const.AND_ID, 'NAND': self.const.NAND_ID,
                'OR': self.const.OR_ID, 'NOR': self.const.NOR_ID,
                'XOR': self.const.XOR_ID, 'NOT': self.const.NOT_ID,
                'BUF': self.const.BUFFER_ID,
            }
            if cell_type in prim_map:
                pts = [self._clean_ident(p) for p in ports_str.split(',') if self._clean_ident(p)]
                if len(pts) >= 2:
                    out_wire = pts[0]
                    in_wires = pts[1:]
                    gid = prim_map[cell_type]
                    g = self.circuit.getcomponent(gid)
                    if hasattr(self.circuit, 'setlimits'):
                        self.circuit.setlimits(g, len(in_wires))
                    self.nodes[out_wire] = g
                    connections.append((g, in_wires))

        # Pass 1.5: Resolve continuous assignments (assign tgt = src)
        for _ in range(20):
            progress = False
            for tgt, src in assign_statements:
                if tgt in self.nodes and self.nodes[tgt] is not None:
                    continue
                src_node = get_const_node(src)
                if src_node is None:
                    src_node = self.nodes.get(src)
                if src_node is not None:
                    self.nodes[tgt] = src_node
                    progress = True
            if not progress:
                break

        # Pass 2: Connect combinational pin nets
        for tgt_gate, src_items in connections:
            if not tgt_gate:
                continue
            for pin_idx, src in enumerate(src_items):
                if isinstance(src, str):
                    src_gate = self.nodes.get(src)
                else:
                    src_gate = src
                if src_gate:
                    self.circuit.connect(tgt_gate, src_gate, pin_idx)

        # Pass 3: Connect DFF inputs (CLK, D, RN, SN)
        for dff_info in self.dff_connections:
            dff_inst = dff_info[0]
            d_wire   = dff_info[1]
            clk_wire = dff_info[2]
            rn_wire  = dff_info[3] if len(dff_info) > 3 else None
            sn_wire  = dff_info[4] if len(dff_info) > 4 else None

            if clk_wire and len(dff_inst.inputs) > 0:
                c_node = self.nodes.get(clk_wire) if isinstance(clk_wire, str) else clk_wire
                if c_node:
                    self.circuit.connect(dff_inst.inputs[0], c_node, 0)
            if d_wire and len(dff_inst.inputs) > 1:
                d_node = self.nodes.get(d_wire) if isinstance(d_wire, str) else d_wire
                if d_node:
                    self.circuit.connect(dff_inst.inputs[1], d_node, 0)
            if len(dff_inst.inputs) > 2:
                rn_node = (self.nodes.get(rn_wire) if isinstance(rn_wire, str) else rn_wire) if rn_wire else None
                if rn_node is None:
                    rn_node = get_const_node("1'b1")
                self.circuit.connect(dff_inst.inputs[2], rn_node, 0)
            if len(dff_inst.inputs) > 3:
                sn_node = (self.nodes.get(sn_wire) if isinstance(sn_wire, str) else sn_wire) if sn_wire else None
                if sn_node is None:
                    sn_node = get_const_node("1'b1")
                self.circuit.connect(dff_inst.inputs[3], sn_node, 0)

        pass

    def build_batches(self, raw_logical_vectors):
        batches = []
        clock_var = self._find_clock_var()
        is_oop = self.is_oop or (self.mode == "reactor_oop")
        has_c1 = getattr(self, 'const_1_node', None) is not None
        has_c0 = getattr(self, 'const_0_node', None) is not None

        for vec in raw_logical_vectors:
            base = []
            for var_node, bit_val in zip(self.input_vars, vec):
                val = self.const.HIGH if bit_val else self.const.LOW
                base.append((var_node if is_oop else var_node.location, val))

            if clock_var is not None:
                clk_target = clock_var if is_oop else clock_var.location
                setup = [(item, self.const.LOW if item == clk_target else val) for item, val in base]
                if has_c1:
                    setup.append((self.const_1_node if is_oop else self.const_1_node.location, self.const.HIGH))
                if has_c0:
                    setup.append((self.const_0_node if is_oop else self.const_0_node.location, self.const.LOW))
                batches.append(setup)

                trigger = [(item, self.const.HIGH if item == clk_target else val) for item, val in base]
                if has_c1:
                    trigger.append((self.const_1_node if is_oop else self.const_1_node.location, self.const.HIGH))
                if has_c0:
                    trigger.append((self.const_0_node if is_oop else self.const_0_node.location, self.const.LOW))
                batches.append(trigger)
            else:
                batch = list(base)
                if has_c1:
                    batch.append((self.const_1_node if is_oop else self.const_1_node.location, self.const.HIGH))
                if has_c0:
                    batch.append((self.const_0_node if is_oop else self.const_0_node.location, self.const.LOW))
                batches.append(batch)

        return batches

    def build_reset_batches(self, count=50):
        batches = []
        clock_var = self._find_clock_var()
        is_oop = self.is_oop or (self.mode == "reactor_oop")
        has_c1 = getattr(self, 'const_1_node', None) is not None
        has_c0 = getattr(self, 'const_0_node', None) is not None

        for i in range(count):
            batch = []
            for var_node in self.input_vars:
                if var_node is clock_var:
                    val = self.const.HIGH if (i % 2 == 1) else self.const.LOW
                else:
                    val = self.const.LOW
                batch.append((var_node if is_oop else var_node.location, val))
            if has_c1:
                batch.append((self.const_1_node if is_oop else self.const_1_node.location, self.const.HIGH))
            if has_c0:
                batch.append((self.const_0_node if is_oop else self.const_0_node.location, self.const.LOW))
            batches.append(batch)
        return batches

    def flatten_batches(self, batches):
        return [item for sublist in batches for item in sublist]

    async def _run_benchmark_async(self, vectors: int, warmup: int,
                                   use_optimize: bool, rx_prop: bool = True, rx_sweep: bool = True,
                                   use_perf: bool = False, perf_events: str = "", perf_tag: str = ""):
        logical_count = max(vectors - warmup, 1)

        _rng = random.Random(42)
        measured_raw = [
            [_rng.randint(0, 1) for _ in range(len(self.input_vars))]
            for _ in range(logical_count)
        ]

        warmup_raw = []
        if warmup > 0:
            warmup_rng = random.Random(1337)
            warmup_raw = [
                [warmup_rng.randint(0, 1) for _ in range(len(self.input_vars))]
                for _ in range(warmup)
            ]

        batch_size = (
            len(self.input_vars)
            + (1 if getattr(self, 'const_1_node', None) else 0)
            + (1 if getattr(self, 'const_0_node', None) else 0)
        )

        flat_warmup_batches   = self.flatten_batches(self.build_batches(warmup_raw))
        flat_measured_batches = self.flatten_batches(self.build_batches(measured_raw))

        total_physical_measured = logical_count * (2 if self._find_clock_var() is not None else 1)
        result = {
            "engine": self.mode,
            "circuit": os.path.basename(self.filepath),
            "vectors": vectors,
            "warmup": warmup,
            "logical_count": logical_count,
            "logical_vectors": logical_count,
            "physical_vectors": total_physical_measured,
            "measured_vectors": logical_count,
            "eval_count": 0,
            "time_ms": 0.0,
            "propagate_ms": 0.0,
            "sweep_ms": 0.0,
            "meps": 0.0
        }

        # ------------------------------------------------------------------
        # PASS 1: propagate (SIMULATE / BFS wavefront)
        # ------------------------------------------------------------------
        if rx_prop:
            if getattr(self, 'const_1_node', None) is not None:
                self.const_1_node.value = self.const.HIGH
                if hasattr(self.circuit, 'toggle'):
                    target = self.const_1_node if (self.is_oop or not self.is_reactor) else self.const_1_node.location
                    self.circuit.toggle(target, self.const.HIGH)
            if getattr(self, 'const_0_node', None) is not None:
                self.const_0_node.value = self.const.LOW
                if hasattr(self.circuit, 'toggle'):
                    target = self.const_0_node if (self.is_oop or not self.is_reactor) else self.const_0_node.location
                    self.circuit.toggle(target, self.const.LOW)

            self.circuit.simulate(self.const.SIMULATE)
            self.const.set_MODE(self.const.SIMULATE)

            reset_cnt = 2 if self.mode == 'engine' else 50
            reset_batches = self.build_reset_batches(reset_cnt)
            if reset_batches:
                flat_reset_batches = self.flatten_batches(reset_batches)
                if flat_reset_batches:
                    self.circuit.batch_toggle(flat_reset_batches, batch_size)

            if flat_warmup_batches:
                self.circuit.batch_toggle(flat_warmup_batches, batch_size)

            gc.collect()
            self.circuit.eval_count = 0
            gc.disable()

            perf_proc = None
            tag_suffix = f"_{perf_tag}" if perf_tag else ""
            c_base = os.path.basename(self.filepath)
            perf_data = f"perf_{self.mode}_prop{tag_suffix}_{c_base}.data"
            perf_txt  = f"perf_{self.mode}_prop{tag_suffix}_{c_base}.txt"
            if use_perf:
                fifo_path = "/tmp/rx_perf_ctrl"
                if not os.path.exists(fifo_path):
                    try: os.mkfifo(fifo_path)
                    except Exception: pass
                cmd = ["perf", "record", "-D", "-1", "-m", "32", "--control=fifo:/tmp/rx_perf_ctrl", "-p", str(os.getpid()), "-o", perf_data]
                if perf_events:
                    cmd.extend(["-e", perf_events])
                perf_proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                time.sleep(0.1)

            send_perf_ctrl("enable")
            propagate_ms = self.circuit.batch_toggle(flat_measured_batches, batch_size, use_perf) if flat_measured_batches else 0.0
            send_perf_ctrl("disable")

            if use_perf and perf_proc:
                perf_proc.terminate()
                perf_proc.wait()
                with open(perf_txt, "w") as f:
                    subprocess.run(["perf", "report", "-i", perf_data], stdout=f, stderr=subprocess.DEVNULL)
                if perf_tag == "opt":
                    compat_txt = f"perf_{self.mode}_prop_{c_base}.txt"
                    try:
                        import shutil
                        shutil.copyfile(perf_txt, compat_txt)
                    except Exception:
                        pass
                for p in (perf_data, perf_data + ".old"):
                    if os.path.exists(p):
                        try: os.remove(p)
                        except Exception: pass

            gc.enable()

            evals = getattr(self.circuit, 'eval_count', 0)
            meps  = (evals / (propagate_ms / 1000.0)) / 1_000_000.0 if propagate_ms > 0 else 0.0

            result["time_ms"]      = propagate_ms
            result["propagate_ms"] = propagate_ms
            result["total_evals"]  = evals
            result["meps"]         = meps

        # ── PASS 2: Sweep (COMPILE / Topological Sweep) ───────────────────────
        has_sweep = (
            self.mode == 'reactor' and
            not self.is_oop and
            hasattr(self.circuit, 'simulate') and
            hasattr(self.const, 'COMPILE')
        )
        if has_sweep and rx_sweep:
            try:
                self.circuit.simulate(self.const.COMPILE)
                self.const.set_MODE(self.const.COMPILE)

                reset_batches = self.build_reset_batches(50)
                sweep_warmup_batches = self.build_batches(warmup_raw)
                sweep_measured_batches = self.build_batches(measured_raw)

                flat_reset_batches = [item for sublist in reset_batches for item in sublist]
                flat_warmup_batches = [item for sublist in sweep_warmup_batches for item in sublist]
                flat_measured_batches = [item for sublist in sweep_measured_batches for item in sublist]

                if flat_reset_batches:
                    self.circuit.batch_toggle(flat_reset_batches, batch_size)

                if flat_warmup_batches:
                    self.circuit.batch_toggle(flat_warmup_batches, batch_size)

                gc.collect()
                self.circuit.eval_count = 0
                gc.disable()

                perf_proc = None
                if use_perf:
                    fifo_path = "/tmp/rx_perf_ctrl"
                    if not os.path.exists(fifo_path):
                        try: os.mkfifo(fifo_path)
                        except Exception: pass
                    perf_data = f"perf_{self.mode}_sweep_{os.path.basename(self.filepath)}.data"
                    perf_txt  = f"perf_{self.mode}_sweep_{os.path.basename(self.filepath)}.txt"
                    cmd = ["perf", "record", "-D", "-1", "-m", "32", "--control=fifo:/tmp/rx_perf_ctrl", "-p", str(os.getpid()), "-o", perf_data]
                    if perf_events:
                        cmd.extend(["-e", perf_events])
                    perf_proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    time.sleep(0.1)

                send_perf_ctrl("enable")
                sweep_ms = self.circuit.batch_toggle(flat_measured_batches, batch_size) if flat_measured_batches else 0.0
                send_perf_ctrl("disable")

                if use_perf and perf_proc:
                    perf_proc.terminate()
                    perf_proc.wait()
                    with open(perf_txt, "w") as f:
                        subprocess.run(["perf", "report", "-i", perf_data], stdout=f, stderr=subprocess.DEVNULL)
                    for p in (perf_data, perf_data + ".old"):
                        if os.path.exists(p):
                            try: os.remove(p)
                            except Exception: pass

                gc.enable()

                sweep_evals = getattr(self.circuit, 'eval_count',
                                      len(flat_measured_batches) // batch_size * len(self.nodes))
                self.circuit.simulate(self.const.SIMULATE)
                self.const.set_MODE(self.const.SIMULATE)
                sweep_meps  = (sweep_evals / (sweep_ms / 1000.0)) / 1_000_000.0 if sweep_ms > 0 else 0.0
                result["sweep_ms"]    = sweep_ms
                result["sweep_evals"] = sweep_evals
                result["sweep_meps"]  = sweep_meps
            except Exception as exc:
                self.circuit.simulate(self.const.SIMULATE)
                self.const.set_MODE(self.const.SIMULATE)
                result["sweep_error"] = str(exc)

        return result

    def run_benchmark(self, vectors: int = 10000, warmup: int = 5000,
                      use_optimize: bool = True, rx_prop: bool = True, rx_sweep: bool = True,
                      use_perf: bool = False, perf_events: str = "", perf_tag: str = "") -> dict:
        return asyncio.run(
            self._run_benchmark_async(vectors, warmup, use_optimize, rx_prop, rx_sweep, use_perf, perf_events, perf_tag)
        )

    def build_physical_batches(self, raw_physical_vectors):
        batches = []
        is_oop = self.is_oop or (self.mode == "reactor_oop")
        has_c1 = getattr(self, 'const_1_node', None) is not None
        has_c0 = getattr(self, 'const_0_node', None) is not None

        for vec in raw_physical_vectors:
            batch = []
            for var_node, bit_val in zip(self.input_vars, vec):
                val = self.const.HIGH if bit_val else self.const.LOW
                batch.append((var_node if is_oop else var_node.location, val))
            if has_c1:
                batch.append((self.const_1_node if is_oop else self.const_1_node.location, self.const.HIGH))
            if has_c0:
                batch.append((self.const_0_node if is_oop else self.const_0_node.location, self.const.LOW))
            batches.append(batch)
        return batches

    async def _run_vectors_async(self, raw_vectors: list, target_mode: int) -> list:
        if hasattr(self.circuit, 'optimize') and self.use_optimize:
            self.circuit.optimize()

        if getattr(self, 'const_1_node', None) is not None:
            self.const_1_node.value = self.const.HIGH
            if hasattr(self.circuit, 'toggle'):
                target = self.const_1_node if (self.is_oop or not self.is_reactor) else self.const_1_node.location
                self.circuit.toggle(target, self.const.HIGH)
        if getattr(self, 'const_0_node', None) is not None:
            self.const_0_node.value = self.const.LOW
            if hasattr(self.circuit, 'toggle'):
                target = self.const_0_node if (self.is_oop or not self.is_reactor) else self.const_0_node.location
                self.circuit.toggle(target, self.const.LOW)

        self.circuit.simulate(target_mode)
        if getattr(self.circuit, 'runner', None) is not None:
            await self.circuit.runner
        self.const.set_MODE(target_mode)

        batches = self.build_physical_batches(raw_vectors)
        batch_size = (
            len(self.input_vars)
            + (1 if getattr(self, 'const_1_node', None) else 0)
            + (1 if getattr(self, 'const_0_node', None) else 0)
        )

        results = []
        for b in batches:
            self.circuit.batch_toggle(b, batch_size)
            results.append([int(g.output) for g in self.output_objects])

        self.const.set_MODE(self.const.SIMULATE)
        return results

    def run_vectors(self, raw_vectors: list, target_mode: int = None) -> list:
        if target_mode is None:
            target_mode = self.const.SIMULATE
        return asyncio.run(self._run_vectors_async(raw_vectors, target_mode))


# ===========================================================================
# 2. SUBPROCESS WORKER DISPATCH
# ===========================================================================

def run_python_backend_process_iwls(filepath: str, mode: str, vectors: int, warmup: int,
                                    optimize: bool, rx_prop: bool = True, rx_sweep: bool = True,
                                    use_perf: bool = False, perf_events: str = "", perf_tag: str = "") -> dict:
    """Run IWLSVerilogRunner in an isolated subprocess to prevent state pollution."""
    cmd = [
        sys.executable, os.path.abspath(__file__),
        "--internal-worker", filepath,
        "--mode", mode,
        "--vectors", str(vectors),
        "--warmup",  str(warmup),
    ]
    if optimize:
        cmd.append("--optimize")
    else:
        cmd.append("--raw")
    if not rx_prop:
        cmd.append("--no-rx-prop")
    if not rx_sweep:
        cmd.append("--no-rx-sweep")
    if use_perf:
        cmd.append("--perf")
        if perf_events:
            cmd.extend(["--perf-events", perf_events])
    if perf_tag:
        cmd.extend(["--perf-tag", perf_tag])

    try:
        t0 = time.perf_counter_ns()
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        t1 = time.perf_counter_ns()

        if res.returncode == 0:
            for line in reversed(res.stdout.strip().split('\n')):
                if line.startswith('{'):
                    data = json.loads(line)
                    data["load_ms"] = data.get("parse_ms", 0.0)
                    return data
            return {"error": "No JSON found in worker stdout: " + res.stdout.strip()[:100]}
        else:
            return {"error": res.stderr.strip() or "Worker process failed"}
    except Exception as e:
        return {"error": str(e)}


def internal_worker_main(filepath: str, mode: str, vectors: int,
                          warmup: int, optimize: bool, rx_prop: bool = True, rx_sweep: bool = True,
                          use_perf: bool = False, perf_events: str = "", perf_tag: str = ""):
    target_path = os.path.join(_SCRIPT_DIR, mode)
    if not os.path.exists(target_path):
        target_path = os.path.join(_PROJECT_ROOT, mode)

    sys.path.insert(0, _PROJECT_ROOT)
    sys.path.insert(0, target_path)
    import Circuit
    import Const

    is_reactor = (mode in ('reactor', 'reactor_oop'))
    is_oop     = (mode == 'reactor_oop')
    try:
        t0 = time.perf_counter_ns()
        runner = IWLSVerilogRunner(
            filepath, Circuit.Circuit, Const, is_reactor=is_reactor, is_oop=is_oop, mode=mode, use_optimize=optimize
        )
        t1 = time.perf_counter_ns()
        stats = runner.run_benchmark(
            vectors=vectors, warmup=warmup, use_optimize=optimize, rx_prop=rx_prop, rx_sweep=rx_sweep,
            use_perf=use_perf, perf_events=perf_events, perf_tag=perf_tag
        )
        stats['parse_ms'] = (t1 - t0) / 1_000_000.0
        print(json.dumps(stats))
    except Exception as e:
        print(json.dumps({"error": str(e)}))


# ===========================================================================
# 3. FILE DISCOVERY
# ===========================================================================

def get_v_files(targets) -> list:
    if isinstance(targets, str):
        targets = [targets]
    v_files = []
    for target in targets:
        if not os.path.exists(target):
            if os.path.exists(os.path.join(_TESTS_DIR, target)):
                target = os.path.join(_TESTS_DIR, target)
            elif os.path.exists(os.path.join(_PROJECT_ROOT, target)):
                target = os.path.join(_PROJECT_ROOT, target)
        if os.path.isfile(target) and (target.endswith('.v') or target.endswith('.json')):
            v_files.append(target)
        elif os.path.isdir(target):
            for root, _, files in os.walk(target):
                for f in files:
                    if f.endswith('.v') and not f.endswith('_tb.v') and not f.endswith('_helper.v') and not f.endswith('_base_tb.v'):
                        v_files.append(os.path.join(root, f))
    return sorted(list(set(v_files)), key=os.path.getsize)


# ===========================================================================
# 4. REPORTING & SPEEDUP ANALYSIS
# ===========================================================================

def _print_speedup_report(all_results: list, md_lines: list = None):
    W = 180
    print()
    print("=" * W)
    print("  SPEEDUP vs ICARUS VERILOG BASELINE  (Icarus VPI sim time = 1x)")
    print("  Reactor modes: prop = BFS wavefront (SIMULATE)  |  sweep = linear fwd-pass (COMPILE)")
    print("=" * W)
    hdr = (
        f"| {'Circuit':<16} "
        f"| {'Engine':>12} "
        f"| {'Reactor prop':>14} "
        f"| {'Reactor sweep':>14} "
        f"| {'Reactor OOP':>14} "
        f"| {'Verilator':>14} |"
    )
    s_sep = (
        f"|{'-'*18}"
        f"|{'-'*14}"
        f"|{'-'*16}"
        f"|{'-'*16}"
        f"|{'-'*16}"
        f"|{'-'*16}|"
    )
    print(hdr)
    print(s_sep)
    if md_lines is not None:
        md_lines.append("")
        md_lines.append("## Speedup vs. Icarus Verilog Baseline (Sim Time = 1x)")
        md_lines.append("")
        md_lines.append(hdr)
        md_lines.append(s_sep)

    def _fmt_sp(time_ms, base_ms):
        if not base_ms or base_ms <= 0 or not time_ms or time_ms <= 0:
            return "N/A"
        sp = base_ms / time_ms
        return f"{sp:.2f}x"

    for row in all_results:
        f   = row['filename']
        e   = row.get('e_res', {})
        r   = row.get('r_res', {})
        ro  = row.get('ro_res', {})
        i   = row.get('i_res', {})
        v   = row.get('v_res', {})

        i_base = i.get('time_ms') if ('error' not in i and i.get('time_ms', 0) > 0) else None

        e_sp  = _fmt_sp(e.get('time_ms'),  i_base) if 'error' not in e else "N/A"
        rp_sp = _fmt_sp(r.get('time_ms'),  i_base) if 'error' not in r else "N/A"
        rs_sp = _fmt_sp(r.get('sweep_ms'), i_base) if ('error' not in r and 'sweep_error' not in r) else "N/A"
        ro_sp = _fmt_sp(ro.get('time_ms'), i_base) if 'error' not in ro else "N/A"
        v_sp  = _fmt_sp(v.get('time_ms'),  i_base) if 'error' not in v else "N/A"

        line = (
            f"| {f:<16} |"
            f" {e_sp:>12} |"
            f" {rp_sp:>14} |"
            f" {rs_sp:>14} |"
            f" {ro_sp:>14} |"
            f" {v_sp:>14} |"
        )
        print(line)
        if md_lines is not None:
            md_lines.append(line)

    print("=" * W)





# ===========================================================================
# 5. MAIN ENTRY POINT
# ===========================================================================

def main():
    parser = argparse.ArgumentParser(description="IWLS 2005 Multi-Engine Logic Simulator Benchmark Runner")
    parser.add_argument('target', nargs='*', default=["tests/IWLS2005/itc99/"],
                        help="Path to one or more IWLS netlist .v files or directories (default: tests/IWLS2005/itc99/)")
    parser.add_argument('--vector', '--vectors', dest='vectors', type=int, default=50000,
                        help="Number of logical test vectors (default: 50,000)")
    parser.add_argument('--warmup', type=int, default=10,
                        help="Number of warmup vectors (default: 10)")
    parser.add_argument('--optimize', action='store_true', default=True,
                        help="Enable topological circuit optimization (default: True)")
    parser.add_argument('--no-optimize', dest='optimize', action='store_false')
    parser.add_argument('--raw', dest='optimize', action='store_false',
                        help="Disable topological circuit optimization (use raw netlist order)")
    parser.add_argument('--no-engine', dest='engine', action='store_false', default=True,
                        help="Disable pure Python Engine")
    parser.add_argument('--no-reactor', dest='reactor', action='store_false', default=True,
                        help="Disable Cython Reactor")
    parser.add_argument('--no-rx-prop', dest='rx_prop', action='store_false', default=True,
                        help="Disable Reactor propagate mode")
    parser.add_argument('--no-rx-sweep', dest='rx_sweep', action='store_false', default=True,
                        help="Disable Reactor sweep mode")
    parser.add_argument('--no-rx-oop', '--no-reactor-oop', dest='rx_oop', action='store_false', default=True,
                        help="Skip Reactor OOP (graph traversal) benchmark")
    parser.add_argument('--no-icarus', dest='icarus', action='store_false', default=True,
                        help="Disable Icarus Verilog")
    parser.add_argument('--no-verilator', dest='verilator', action='store_false', default=True,
                        help="Disable Verilator")
    parser.add_argument('--dump', action='store_true',
                        help="Dump Markdown results table to tests/test_result/benchmark/")
    parser.add_argument('--json', action='store_true',
                        help="Output raw JSON results")
    parser.add_argument('--perf', action='store_true',
                        help="Enable Linux perf performance profiling")
    parser.add_argument('--perf-events', type=str, default="",
                        help="Custom perf events list")
    parser.add_argument('--perf-tag', type=str, default="", help=argparse.SUPPRESS)

    parser.add_argument('--bench', dest='bench', action='store_true', default=None,
                        help="Force benchmark execution")
    parser.add_argument('--no-bench', dest='bench', action='store_false',
                        help="Skip benchmark execution")
    parser.add_argument('--verify', dest='verify', action='store_true', default=False,
                        help="Run connected state verifier across engines before benchmarking or standalone")
    parser.add_argument('--verify-vectors', type=int, default=None,
                        help="Number of test vectors to verify per circuit (default: min(measured, 1000))")

    # Internal worker flags
    parser.add_argument('--internal-worker', type=str, default="", help=argparse.SUPPRESS)
    parser.add_argument('--mode', type=str, default="reactor", help=argparse.SUPPRESS)

    args = parser.parse_args()

    # Worker dispatch
    if args.internal_worker:
        internal_worker_main(
            args.internal_worker, args.mode, args.vectors, args.warmup,
            args.optimize, args.rx_prop, args.rx_sweep, args.perf, args.perf_events,
            getattr(args, 'perf_tag', '')
        )
        sys.exit(0)

    # Discover netlists
    v_files = get_v_files(args.target)
    if not v_files:
        print(f"[-] Error: No .v netlists found in {args.target}")
        sys.exit(1)

    run_bench = True if args.bench is None else args.bench
    run_verify = args.verify

    # ── Connected Verifier Pass ──────────────────────────────────────────────
    if run_verify:
        try:
            from verifier_iwls import verify_circuit as verify_circuit_iwls
        except ImportError:
            try:
                from tests.src.verifier_iwls import verify_circuit as verify_circuit_iwls
            except ImportError:
                from tests.verifier_iwls import verify_circuit as verify_circuit_iwls

        v_count_default = args.verify_vectors if args.verify_vectors is not None else min(max(args.vectors - args.warmup, 1), 1000)

        if not args.json:
            print("=" * 115)
            print("  UNIFIED IWLS 2005 SEQUENTIAL STATE VERIFICATION SUITE")
            print(f"  Vectors/Circuit : {args.vectors:,} (verified: {v_count_default:,}) | Base Model: Icarus Verilog / Verilator")
            print("=" * 115)
            print(f"| {'Circuit':<18} | {'Inputs':<8} | {'Outputs':<8} | {'Vectors':<10} | {'Passed':<10} | {'Failed':<8} | {'Status':<8} |")
            print(f"|{'-'*20}|{'-'*10}|{'-'*10}|{'-'*12}|{'-'*12}|{'-'*10}|{'-'*10}|")
            sys.stdout.flush()

        failed_circuits = []
        for filepath in v_files:
            v_count = args.verify_vectors if args.verify_vectors is not None else min(max(args.vectors - args.warmup, 1), 1000)
            v_report = verify_circuit_iwls(
                filepath,
                vector_count=v_count,
                warmup_count=50,
                use_engine=args.engine,
                use_rx_prop=args.rx_prop,
                use_rx_sweep=args.rx_sweep,
                use_rx_oop=getattr(args, 'rx_oop', True),
                use_icarus=args.icarus,
                use_verilator=getattr(args, 'verilator', True),
                optimize=args.optimize
            )

            status = v_report.get("status", "ERR")
            status_col = f"\033[92mPASS\033[0m{' ' * 4}" if status == "PASS" else f"\033[91mFAIL\033[0m{' ' * 4}"
            c_name  = v_report.get('circuit', os.path.basename(filepath))
            n_in    = str(v_report.get('inputs_count', 'N/A'))
            n_out   = str(v_report.get('outputs_count', 'N/A'))
            tot_v   = f"{v_report.get('total_vectors', 0):,}" if isinstance(v_report.get('total_vectors'), int) else str(v_report.get('total_vectors', 'N/A'))
            pass_v  = f"{v_report.get('pass_count', 0):,}" if isinstance(v_report.get('pass_count'), int) else str(v_report.get('pass_count', 0))
            fail_v  = str(v_report.get('fail_count', 0))
            row_str = (
                f"| {c_name:<18} | "
                f"{n_in:<8} | "
                f"{n_out:<8} | "
                f"{tot_v:<10} | "
                f"{pass_v:<10} | "
                f"{fail_v:<8} | "
                f"{status_col} |"
            )

            if not args.json:
                print(row_str)
                sys.stdout.flush()

            if v_report.get("status") != "PASS" or v_report.get("fail_count", 0) > 0:
                failed_circuits.append(c_name)
                if not args.json:
                    if v_report.get('mismatches'):
                        mm = v_report['mismatches'][0]
                        print(f"  └─> First mismatch at vector #{mm['vector_id']}:")
                        print(f"      Inputs applied: {mm['inputs']}")
                        print(f"      Expected ({mm.get('ref_source')}): {mm['expected']}")
                        for be_key in ('icarus_actual', 'verilator_actual', 'engine_actual', 'rx_prop_actual', 'rx_sweep_actual', 'rx_oop_actual'):
                            if be_key in mm and mm[be_key] != "SKIPPED":
                                print(f"      {be_key}: {mm[be_key]}")

        if failed_circuits:
            if not args.json:
                print(f"\n[-] Verification failed for {len(failed_circuits)} circuit(s): {', '.join(failed_circuits)}.")
                if run_bench:
                    print("[-] Benchmark execution skipped due to verification failure(s).")
            sys.exit(1)

        if not run_bench:
            if not args.json:
                print(f"\n[+] Verifier mode completed successfully for {len(v_files)} circuit(s). No benchmarks requested.")
            sys.exit(0)
        else:
            if not args.json:
                print()

    measured = max(args.vectors - args.warmup, 1)

    vpi_status = (
        "enabled (inner-loop VPI timer)"
        if os.path.exists(_VPI_TIMER_VPI)
        else "disabled (fallback to vvp wall time)"
    )

    W = 180
    cols1 = (
        f"| {'Circuit':<16} "
        f"| {'Engine':^10} "
        f"| {'Reactor (Prop)':^14} | {'Reactor (Sweep)':^15} "
        f"| {'ReactorOOP':^12} "
        f"| {'Icarus':^14} "
        f"| {'Verilator':^14} |"
    )
    sep = (
        f"|{'-'*18}"
        f"|{'-'*12}"
        f"|{'-'*16}|{'-'*17}"
        f"|{'-'*14}"
        f"|{'-'*16}"
        f"|{'-'*16}|"
    )
    cols2 = (
        f"| {'':<16} "
        f"| {'Time(ms)':>10} "
        f"| {'prop(ms)':>14} | {'sweep(ms)':>15} "
        f"| {'prop(ms)':>12} "
        f"| {'sim(ms)':>14} "
        f"| {'sim(ms)':>14} |"
    )

    if not getattr(args, 'json', False):
        print("=" * W)
        print("  UNIFIED IWLS 2005 SEQUENTIAL LOGIC SIMULATOR BENCHMARK")
        print(f"  Total vectors  : {args.vectors:,}  |  Warmup (untimed): {args.warmup:,}  |  Measured: {measured:,}")
        print(f"  Circuits       : {len(v_files)}")
        print(f"  Icarus VPI     : {vpi_status}")
        print("  Reactor modes  : propagate (BFS wavefront, SIMULATE) | sweep (linear fwd-pass, COMPILE)")
        print("  Cell Library   : Cadence GSCLib 3.0 (180nm) + DFF.json")
        print("=" * W)
        print(cols1)
        print(sep)
        print(cols2)

    all_results = []
    md_lines = []
    md_lines.append("# Unified IWLS 2005 Logic Simulator Benchmark")
    md_lines.append("")
    md_lines.append(f"- **Total vectors**: {args.vectors:,} (Warmup: {args.warmup:,}, Measured: {measured:,})")
    md_lines.append(f"- **Circuits**: {len(v_files)}")
    md_lines.append(f"- **Icarus VPI**: {vpi_status}")
    md_lines.append(f"- **Cell Library**: Cadence GSCLib 3.0 (180nm)")
    md_lines.append("")
    md_lines.append(cols1)
    md_lines.append(sep)
    md_lines.append(cols2)

    for filepath in v_files:
        filename = os.path.basename(filepath)

        # 1. Reactor Propagate / Sweep
        if args.reactor and (args.rx_prop or args.rx_sweep):
            r_res = run_python_backend_process_iwls(
                filepath, 'reactor', args.vectors, args.warmup, args.optimize,
                args.rx_prop, args.rx_sweep, args.perf, args.perf_events
            )
        else:
            r_res = {"engine": "Reactor", "file": filename, "error": "disabled"}

        # 2. Reactor OOP
        if args.reactor and args.rx_oop and args.rx_prop:
            ro_res = run_python_backend_process_iwls(
                filepath, 'reactor_oop', args.vectors, args.warmup, args.optimize, True, False,
                args.perf, args.perf_events
            )
        else:
            ro_res = {"engine": "ReactorOOP", "file": filename, "error": "disabled"}

        # 3. Icarus Verilog
        if args.icarus and run_icarus_harness_iwls:
            i_res = run_icarus_harness_iwls(
                filepath, args.vectors, args.warmup, args.perf, args.perf_events
            )
        else:
            i_res = {"engine": "Icarus", "file": filename, "error": "disabled"}

        # 4. Verilator C++
        if args.verilator and run_verilator_harness_iwls:
            v_res = run_verilator_harness_iwls(
                filepath, args.vectors, args.warmup, args.perf, args.perf_events
            )
        else:
            v_res = {"engine": "Verilator", "file": filename, "error": "disabled"}

        # 5. Engine (Pure Python - with adaptive vectors for large netlists)
        if args.engine:
            size_kb = os.path.getsize(filepath) / 1024.0
            if size_kb > 4000:
                eng_vecs = min(args.vectors, 10)
                eng_warm = min(args.warmup, 2)
            elif size_kb > 1000:
                eng_vecs = min(args.vectors, 50)
                eng_warm = min(args.warmup, 5)
            elif size_kb > 100:
                eng_vecs = min(args.vectors, 100)
                eng_warm = min(args.warmup, 5)
            else:
                eng_vecs = min(args.vectors, 500)
                eng_warm = min(args.warmup, 10)

            e_res = run_python_backend_process_iwls(
                filepath, 'engine', eng_vecs, eng_warm, args.optimize, args.rx_prop, args.rx_sweep,
                args.perf, args.perf_events
            )
            if "error" not in e_res and e_res.get("time_ms", 0) > 0:
                e_meas = max(eng_vecs - eng_warm, 1)
                tgt_meas = max(args.vectors - args.warmup, 1)
                if e_meas != tgt_meas:
                    e_res["raw_time_ms"] = e_res["time_ms"]
                    e_res["raw_vectors"] = e_meas
                    e_res["time_ms"] = (e_res["time_ms"] / e_meas) * tgt_meas
                    e_res["measured_vectors"] = tgt_meas
                    if "total_evals" in e_res:
                        e_res["total_evals"] = int((e_res["total_evals"] / e_meas) * tgt_meas)
        else:
            e_res = {"engine": "Engine", "file": filename, "error": "disabled"}

        e_is_dis  = (not args.engine) or (e_res.get('error') == 'disabled')
        r_is_dis  = (not args.reactor) or (not args.rx_prop) or (r_res.get('error') == 'disabled')
        rs_is_dis = (not args.reactor) or (not args.rx_sweep) or (r_res.get('error') == 'disabled')
        ro_is_dis = (not args.reactor) or (not args.rx_oop) or (ro_res.get('error') == 'disabled')
        i_is_dis  = (not args.icarus) or (i_res.get('error') == 'disabled')
        v_is_dis  = (not args.verilator) or (v_res.get('error') == 'disabled')

        e_str     = f"{e_res['time_ms']:.1f}"   if ('error' not in e_res and e_res.get('time_ms', 0) > 0) else ("N/A" if e_is_dis else "ERR")
        r_str     = f"{r_res['time_ms']:.1f}"   if ('error' not in r_res and r_res.get('time_ms', 0) > 0) else ("N/A" if r_is_dis else "ERR")
        rs_str    = (f"{r_res['sweep_ms']:.1f}" if ('sweep_ms' in r_res and r_res.get('sweep_ms', 0) > 0)
                     else ("N/A" if rs_is_dis else ("ERR" if 'sweep_error' in r_res else "N/A")))
        ro_str    = f"{ro_res['time_ms']:.1f}"  if ('error' not in ro_res and ro_res.get('time_ms', 0) > 0) else ("N/A" if ro_is_dis else "ERR")
        i_sim_str = f"{i_res['time_ms']:.2f}"   if ('error' not in i_res and i_res.get('time_ms', 0) > 0) else ("N/A" if i_is_dis else "ERR")
        v_sim_str = f"{v_res['time_ms']:.2f}"   if ('error' not in v_res and v_res.get('time_ms', 0) > 0) else ("N/A" if v_is_dis else "ERR")

        e_ev  = f"{e_res.get('total_evals', 0):>10,}" if ('error' not in e_res and e_res.get('total_evals', 0) > 0) else (f"{'N/A':>10}" if e_is_dis else f"{'ERR':>10}")
        r_ev  = f"{r_res.get('total_evals', 0):>14,}" if ('error' not in r_res and r_res.get('total_evals', 0) > 0) else (f"{'N/A':>14}" if r_is_dis else f"{'ERR':>14}")
        rs_ev = (f"{r_res['sweep_evals']:>15,}"       if ('sweep_evals' in r_res and r_res.get('sweep_evals', 0) > 0)
                 else (f"{'N/A':>15}" if rs_is_dis else (f"{'ERR':>15}" if 'sweep_error' in r_res else f"{'N/A':>15}")))
        ro_ev = f"{ro_res.get('total_evals', 0):>12,}" if ('error' not in ro_res and ro_res.get('total_evals', 0) > 0) else (f"{'N/A':>12}" if ro_is_dis else f"{'ERR':>12}")

        row_str = (
            f"| {filename:<16} | "
            f"{e_str:>10} | {r_str:>14} | {rs_str:>15} | "
            f"{ro_str:>12} | "
            f"{i_sim_str:>14} | "
            f"{v_sim_str:>14} |"
        )
        evals_str = f"| {'evals':<16} | {e_ev} | {r_ev} | {rs_ev} | {ro_ev} | {'-':>14} | {'-':>14} |"

        if not getattr(args, 'json', False):
            print(row_str)
            print(evals_str)

        md_lines.append(row_str)
        md_lines.append(evals_str)

        all_results.append({
            "filename": filename,
            "filepath": filepath,
            "e_res": e_res,
            "r_res": r_res,
            "ro_res": ro_res,
            "i_res": i_res,
            "v_res": v_res,
        })

    # Speedup report
    if not getattr(args, 'json', False):
        _print_speedup_report(all_results, md_lines)

    # Dump results
    if args.dump:
        out_dir = os.path.join(_TESTS_DIR, "test_result", "benchmark")
        os.makedirs(out_dir, exist_ok=True)
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        md_file = os.path.join(out_dir, f"unified_iwls_benchmark_{ts}.md")
        with open(md_file, "w", encoding="utf-8") as f:
            f.write("\n".join(md_lines) + "\n")
        print(f"\n[+] Benchmark markdown report written to: {md_file}")

    if args.json:
        print("\n" + json.dumps(all_results, indent=2))


if __name__ == "__main__":
    main()
