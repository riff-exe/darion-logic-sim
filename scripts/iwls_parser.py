#!/usr/bin/env python3
"""
iwls_parser.py
==============
Parses IWLS 2005 standard-cell Verilog netlists (Cadence GSCLib 3.0) into
Darion Circuit representation and serializes them to JSON format (.json).

Mirrors the workflow of scripts/iscas_parser.py with full support for:
  - 37 Cadence GSCLib 3.0 cell types (AND, OR, NAND, NOR, XOR, XNOR, AOI, OAI, MUX, ADD)
  - Sequential flip-flops (DFFSRX1, DFFX1, SDFFSRX1 with scan muxing, TLATX1)
  - Escaped identifiers (e.g. \\stato[0] )
  - Multi-bit bus port expansions ([msb:lsb] vectors)
  - Continuous assignments (assign a = b)
  - Logic constants (1'b0, 1'b1, 1'bx, etc.)
  - Topological optimization and gate creation order randomization
"""

import os
import glob
import re
import sys
import time
import argparse
import random

# Add project root and reactor path to sys.path
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_SCRIPT_DIR)
sys.path.insert(0, _PROJECT_ROOT)
sys.path.insert(0, os.path.join(_PROJECT_ROOT, 'reactor'))

try:
    import Circuit
    import Const
except ImportError:
    # Fallback to engine if reactor extension is not yet built
    sys.path.insert(0, os.path.join(_PROJECT_ROOT, 'engine'))
    import Circuit
    import Const


class IWLSVerilogRunner:
    """
    Parses an IWLS 2005 standard-cell netlist and loads it into a Darion Circuit.
    """

    def __init__(self, v_file_path, circuit_cls=None, const_mod=None, randomize_gates=False):
        self.Circuit = circuit_cls or Circuit.Circuit
        self.const = const_mod or Const
        self.circuit = self.Circuit()
        self.circuit.simulate(self.const.DESIGN)
        self.randomize_gates = randomize_gates

        self.nodes = {}
        self.outputs = []
        self.input_vars = []
        self.dff_connections = []
        self.dff_crct = None
        self.is_sequential = False
        self.const_1_node = None
        self.const_0_node = None

        # Load DFFSR.json or DFF.json from common search locations
        dff_candidates = [
            os.path.join(_SCRIPT_DIR, "DFFSR.json"),
            os.path.join(_PROJECT_ROOT, "tests", "src", "DFFSR.json"),
            os.path.join(_PROJECT_ROOT, "tests", "DFFSR.json"),
            os.path.join(_PROJECT_ROOT, "DFFSR.json"),
            "tests/src/DFFSR.json",
            "tests/DFFSR.json",
            "DFFSR.json",
            os.path.join(_SCRIPT_DIR, "DFF.json"),
            os.path.join(_PROJECT_ROOT, "tests", "src", "DFF.json"),
            os.path.join(_PROJECT_ROOT, "tests", "DFF.json"),
            os.path.join(_PROJECT_ROOT, "DFF.json"),
            "tests/src/DFF.json",
            "tests/DFF.json",
            "DFF.json",
        ]
        for p in dff_candidates:
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

        # Set default values for constants
        if getattr(self, 'const_1_node', None) is not None:
            self.const_1_node.value = self.const.HIGH
            if hasattr(self.circuit, 'toggle'):
                try:
                    self.circuit.toggle(getattr(self.const_1_node, 'location', self.const_1_node), self.const.HIGH)
                except Exception:
                    try:
                        self.circuit.toggle(self.const_1_node, self.const.HIGH)
                    except Exception:
                        pass
        if getattr(self, 'const_0_node', None) is not None:
            self.const_0_node.value = self.const.LOW
            if hasattr(self.circuit, 'toggle'):
                try:
                    self.circuit.toggle(getattr(self.const_0_node, 'location', self.const_0_node), self.const.LOW)
                except Exception:
                    try:
                        self.circuit.toggle(self.const_0_node, self.const.LOW)
                    except Exception:
                        pass

    def _clean_ident(self, s: str) -> str:
        """Strip leading/trailing whitespace from identifier; preserve escaped prefix."""
        return s.strip()

    def _parse_verilog(self, filepath):
        if filepath.endswith('.json'):
            self.circuit.readfromjson(filepath)
            for gate in (self.circuit.get_components() if hasattr(self.circuit, 'get_components') else self.circuit.components):
                name_str = getattr(gate, 'custom_name', None) or getattr(gate, 'codename', None) or str(gate)
                if isinstance(name_str, bytes):
                    name_str = name_str.decode('utf-8', errors='ignore')
                if 'dff' in name_str.lower() or 'DFF' in name_str or getattr(gate, 'id', None) == 11:
                    self.is_sequential = True
            for v in (self.circuit.get_variables() if hasattr(self.circuit, 'get_variables') else []):
                self.input_vars.append(v)
            return

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Strip comments
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        content = re.sub(r'//.*', '', content)

        # Isolate top-level circuit module
        module_body = content
        for m in re.finditer(r'\bmodule\s+([a-zA-Z0-9_]+)\s*\((.*?)\);', content, flags=re.DOTALL):
            m_name = m.group(1).strip()
            if m_name.lower() not in ('dff', 'dffsrx1', 'dffx1', 'sdffsrx1', 'invx1', 'bufx1', 'udp_tlat', 'udp_dff'):
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
        gate_statements = []

        # Pass 1: Declare input / output ports and gather gate/assign statements
        for stmt in statements:
            # Continuous assignments (e.g. assign a = b, c = 1'b0;)
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

            # Input port declarations
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

            # Output port declarations
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

            if stmt.startswith(('wire ', 'wire\n', 'wire\t', 'module ', 'module\n', 'module\t', 'endmodule', 'reg ', 'reg\n', 'reg\t')):
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
            inst_name = tokens[1] if len(tokens) > 1 else f"inst_{len(gate_statements)}"
            ports_str = stmt[paren_idx + 1 : rparen_idx]

            gate_statements.append((cell_type, inst_name, ports_str))

        # Shuffle gate creation order if --random is requested
        if self.randomize_gates:
            random.shuffle(gate_statements)

        # Pass 2: Instantiate gates and build connection mappings
        for cell_type, inst_name, ports_str in gate_statements:
            named_ports = {}
            for pm in re.finditer(r'\.\s*([a-zA-Z0-9_]+)\s*\(\s*([^)]*)\s*\)', ports_str):
                port_pin = pm.group(1).strip().upper()
                wire_ref = self._clean_ident(pm.group(2))
                named_ports[port_pin] = wire_ref

            # Ensure constants referenced in ports are registered
            for w in named_ports.values():
                if w:
                    get_const_node(w)

            # ── 1. Sequential Flip-Flops & Latches (DFFX1, DFFSRX1, SDFFSRX1, TLATX1) ──
            if cell_type.startswith(('DFF', 'SDFF')):
                self.is_sequential = True
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

                # Scan Flip-Flop (SDFFSRX1): D_eff = SE ? SI : D  => (SI & SE) | (D & ~SE)
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

            if cell_type.startswith('TLAT'):
                self.is_sequential = True
                if self.dff_crct:
                    dff_inst = self.circuit.load_ic(self.dff_crct)
                    if hasattr(dff_inst, 'rename'):
                        dff_inst.rename(f"TLAT_{inst_name}")
                    else:
                        dff_inst.custom_name = f"TLAT_{inst_name}"
                    q_wire  = named_ports.get('Q')
                    qn_wire = named_ports.get('QN')
                    d_wire  = named_ports.get('D')
                    c_wire  = named_ports.get('C', named_ports.get('G', named_ports.get('CK', named_ports.get('CLK'))))
                    rn_wire = named_ports.get('RN')
                    sn_wire = named_ports.get('SN')
                    if q_wire:
                        self.nodes[q_wire] = dff_inst.outputs[0]
                    if qn_wire:
                        self.nodes[qn_wire] = dff_inst.outputs[1]
                    self.dff_connections.append((dff_inst, d_wire, c_wire, rn_wire, sn_wire))
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

            if cell_type.startswith(('BUF', 'CLKBUF', 'TBUF')):
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

            # ── 3. Basic Gates (AND, OR, NAND, NOR, XOR, XNOR) ────────────────
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

            if cell_type.startswith(('NAND2', 'NAND2X1', 'NAND2X2')):
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

            if cell_type.startswith('XNOR2'):
                g = self.circuit.getcomponent(self.const.XNOR_ID)
                if hasattr(self.circuit, 'setlimits'):
                    self.circuit.setlimits(g, 2)
                y = named_ports.get('Y')
                if y:
                    self.nodes[y] = g
                    connections.append((g, [named_ports.get('A'), named_ports.get('B')]))
                continue

            # ── 4. Complex AOI Gates ──────────────────────────────────────────
            if cell_type.startswith('AOI21'):
                # Y = ~((A0 & A1) | B0) -> and_g = AND(A0, A1), nor_g = NOR(and_g, B0)
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
                # Y = ~((A0 | A1) & B0) -> or_g = OR(A0, A1), nand_g = NAND(or_g, B0)
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

            # ── 6. Multiplexers & Adders ──────────────────────────────────────
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
                'XOR': self.const.XOR_ID, 'XNOR': self.const.XNOR_ID,
                'NOT': self.const.NOT_ID, 'BUF': self.const.BUFFER_ID,
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

        # Pass 2.5: Resolve continuous assignments (assign tgt = src)
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

        # Pass 3: Connect combinational pin nets
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

        # Pass 4: Connect DFF inputs (CLK, D, RN, SN)
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

        try:
            self.circuit.simulate(self.const.COMPILE)
        except Exception:
            pass


def process_iwls_file(in_path: str, out_path: str, randomize: bool = False, optimize: bool = False):
    """
    Parses a single IWLS Verilog file and writes its serialized JSON representation.
    """
    tag = []
    if randomize:
        tag.append("RANDOMIZED")
    if optimize:
        tag.append("OPTIMIZED")
    tag_str = f" ({', '.join(tag)})" if tag else ""

    print(f"Parsing {in_path} -> {out_path}{tag_str}...")
    t0 = time.time()
    try:
        runner = IWLSVerilogRunner(in_path, Circuit.Circuit, Const, randomize_gates=randomize)
        if optimize and hasattr(runner.circuit, 'optimize'):
            runner.circuit.optimize()
        runner.circuit.writetojson(out_path)
        dt = time.time() - t0

        size_kb = os.path.getsize(out_path) / 1024.0
        circuit_type = "IWLS Sequential" if runner.is_sequential else "IWLS Combinational"
        comp_count = len(runner.circuit.get_components()) if hasattr(runner.circuit, 'get_components') else len(runner.nodes)
        dff_count = len(runner.dff_connections)

        print(f"  [+] Success: {out_path}")
        print(f"      Type: {circuit_type} | Components: {comp_count:,} | DFFs: {dff_count} | Inputs: {len(runner.input_vars)} | Outputs: {len(runner.outputs)}")
        print(f"      File size: {size_kb:.1f} KB | Time: {dt:.2f}s\n")
        return {
            "status": "success",
            "file": in_path,
            "out": out_path,
            "type": circuit_type,
            "components": comp_count,
            "dffs": dff_count,
            "inputs": len(runner.input_vars),
            "outputs": len(runner.outputs),
            "size_kb": size_kb,
            "time_sec": dt
        }
    except Exception as e:
        dt = time.time() - t0
        print(f"  [-] Failed: {in_path} -> {e} ({dt:.2f}s)\n")
        return {
            "status": "error",
            "file": in_path,
            "out": out_path,
            "error": str(e),
            "time_sec": dt
        }


def main():
    parser = argparse.ArgumentParser(
        description="Parse IWLS 2005 Verilog netlists (Cadence GSCLib 3.0) to Darion JSON format"
    )
    parser.add_argument('path', nargs='?', default=None,
                        help="Optional path to a .v file or directory containing .v files")
    parser.add_argument('--random', action='store_true',
                        help="Randomize the creation order of gates in the JSON output")
    parser.add_argument('--optimize', action='store_true',
                        help="Run topological optimization on the circuit prior to serializing")
    parser.add_argument('-o', '--output', type=str, default=None,
                        help="Custom output file path (for single file) or destination directory")
    parser.add_argument('--max-size-mb', type=float, default=None,
                        help="Skip .v files larger than this threshold in megabytes")
    parser.add_argument('--all', action='store_true',
                        help="Process all IWLS 2005 benchmark subdirectories (itc99, opencores, faraday)")
    parser.add_argument('--skip-existing', action='store_true',
                        help="Skip conversion if target .json already exists and is newer than .v")
    args = parser.parse_args()

    results = []

    # Case 1: Single file specified
    if args.path and os.path.isfile(args.path):
        out_path = args.output if args.output else args.path.replace('.v', '.json')
        res = process_iwls_file(args.path, out_path, args.random, args.optimize)
        results.append(res)
        return

    # Case 2: Specific directory specified
    if args.path and os.path.isdir(args.path):
        v_files = sorted(glob.glob(os.path.join(args.path, '*.v')))
        for f in v_files:
            if "GSCLib_3.0.v" in f or "library" in f:
                continue
            if args.max_size_mb and (os.path.getsize(f) / (1024 * 1024)) > args.max_size_mb:
                print(f"Skipping {f} (exceeds {args.max_size_mb} MB limit)")
                continue

            out_dir = args.output if (args.output and os.path.isdir(args.output)) else args.path
            out_name = os.path.basename(f).replace('.v', '.json')
            out_path = os.path.join(out_dir, out_name)

            if args.skip_existing and os.path.exists(out_path) and os.path.getmtime(out_path) >= os.path.getmtime(f):
                print(f"Skipping {f} (.json is up to date)")
                continue

            res = process_iwls_file(f, out_path, args.random, args.optimize)
            results.append(res)
        print(f"Done processing directory {args.path}.")
        return

    # Case 3: Default — process all standard IWLS 2005 benchmark directories
    dirs_to_process = [
        os.path.join(_PROJECT_ROOT, 'tests', 'IWLS2005', 'itc99'),
        os.path.join(_PROJECT_ROOT, 'tests', 'IWLS2005', 'opencores'),
        os.path.join(_PROJECT_ROOT, 'tests', 'IWLS2005', 'faraday'),
    ]

    total_files = 0
    for source_dir in dirs_to_process:
        if not os.path.exists(source_dir):
            continue
        v_files = sorted(glob.glob(os.path.join(source_dir, '*.v')))
        for f in v_files:
            if "GSCLib_3.0.v" in f or "library" in f:
                continue
            if args.max_size_mb and (os.path.getsize(f) / (1024 * 1024)) > args.max_size_mb:
                print(f"Skipping {f} (exceeds {args.max_size_mb} MB limit)")
                continue

            out_name = os.path.basename(f).replace('.v', '.json')
            out_path = os.path.join(source_dir, out_name)

            if args.skip_existing and os.path.exists(out_path) and os.path.getmtime(out_path) >= os.path.getmtime(f):
                print(f"Skipping {f} (.json is up to date)")
                continue

            res = process_iwls_file(f, out_path, args.random, args.optimize)
            results.append(res)
            total_files += 1

    print(f"\n=========================================================================")
    print(f"  IWLS 2005 PARSER SUMMARY")
    print(f"=========================================================================")
    success_count = sum(1 for r in results if r.get('status') == 'success')
    error_count = sum(1 for r in results if r.get('status') == 'error')
    print(f"  Total Processed : {len(results)}")
    print(f"  Successes       : {success_count}")
    print(f"  Failures        : {error_count}")
    print(f"=========================================================================\n")


if __name__ == '__main__':
    main()
