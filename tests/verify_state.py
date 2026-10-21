#!/usr/bin/env python3
"""
Extended sequential verification for IWLS-2005 netlists: primary outputs AND internal flop state.

What it adds over tests/src/verifier_iwls.py
  * compares the Q of every flip-flop (not only primary outputs): the netlist is rewritten so each DFF's
    Q net is also an extra 1-bit output port for the Icarus and Verilator references, and Darion's
    flop IC output is read directly;
  * long runs (tens of thousands of cycles) and two stimuli:
      bench  uniform random on every input including reset (what the benchmarks use)
      run    reset deasserted after warmup, inputs toggle with probability 0.1 (state actually evolves)
  * Darion is driven in the same configurations as the benchmarks: rx-prop (SIMULATE, BFS layout) and
    rx-sweep (COMPILE, DFS layout);
  * reports how many reference bits were X (Icarus, 4-state) and therefore not compared.

Real workload:  python tests/verify_state.py --workload tv80 [--cycles 20000]
        a Z80 program running on the tv80 netlist, bus trace compared with Icarus (see "workload tv80" below)

Case study:     python tests/verify_state.py --case-study [--cycles 2000 --seed 1]
        tv80 with one injected bug (a 2-input cell swapped) runs the Z80 program; the bug is located from the failing
        run with Darion's API and with an Icarus compile/run/VCD workflow; both are timed (see "case study" below)

Usage:  python tests/verify_state.py b14 [--logical 50000] [--ic-logical 5000] [--stim bench|run]
        (reference runs are written under a scratch directory, never inside tests/)
"""
import os
import re
import sys
import time
import shutil
import random
import asyncio
import argparse
import json
import tempfile
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
for p in (os.path.join(HERE, "src"), HERE, ROOT, os.path.join(ROOT, "reactor")):
    if p not in sys.path:
        sys.path.insert(0, p)

import Const      # noqa: E402
import Circuit    # noqa: E402
import iwls_sequential_harness as H   # noqa: E402
import verifier_iwls as V             # noqa: E402
import benchmark_iwls as B            # noqa: E402

DFF_RE = re.compile(r"\b(S?DFF\w*)\s+(\\\S+|\w+)\s*\((.*?)\)\s*;", re.S)


# --------------------------------------------------------------------------------------
# netlist rewrite: expose every flop's Q as an extra scalar output port
# --------------------------------------------------------------------------------------
def make_state_netlist(src, dst):
    text = open(src, encoding="utf-8").read()
    flops, decls, assigns = [], [], []

    def fix(m):
        kind, inst, body = m.group(1), m.group(2), m.group(3)
        idx = len(flops)
        q = re.search(r"\.Q\s*\(([^)]*)\)", body)
        net = q.group(1).strip() if q else ""
        if not net:
            net = f"dbg_q_{idx}"
            decls.append(f"  wire {net};\n")
            body = re.sub(r"\.Q\s*\(\s*\)", f".Q ({net})", body, count=1) if q else body + f", .Q ({net})"
        flops.append(inst)
        assigns.append(f"  assign dbg_o_{idx} = {net} ;\n")
        return f"{kind} {inst} ({body});"

    new = DFF_RE.sub(fix, text)
    ports = ", ".join(f"dbg_o_{i}" for i in range(len(flops)))
    hdr = re.search(r"\bmodule\s+(?!DFF|INV|BUF)(\w+)\s*\((.*?)\)\s*;", new, re.S)
    # wires must be declared before the instances that use them (Icarus is strict about this), and the new
    # outputs must come after the original output declarations so the reference columns keep the original order
    outs = "".join(f"  output dbg_o_{i};\n" for i in range(len(flops)))
    new = new[:hdr.end(2)] + ", " + ports + new[hdr.end(2):]
    first_inst = re.search(r"^\s*[A-Z][A-Za-z0-9]*X\d+\s", new, re.M).start()
    last_decl = list(re.finditer(r"^\s*(?:input|output|wire|reg)\b[^;]*;", new[:first_inst], re.M))[-1]
    cut = last_decl.end()
    new = new[:cut] + "\n" + outs + "".join(decls) + new[cut:]
    end = new.rindex("endmodule")
    new = new[:end] + "".join(assigns) + new[end:]
    open(dst, "w", encoding="utf-8").write(new)
    return flops


# --------------------------------------------------------------------------------------
# stimulus (same warmup as verifier_iwls.py)
# --------------------------------------------------------------------------------------
def make_vectors(n_in, clk_idx, rst_idx, rst_deassert, logical, stim, seed=42):
    rst_assert = 1 - rst_deassert
    phys = []
    for i in range(50):
        w = [0] * n_in
        if i < 10:
            if rst_idx != -1:
                w[rst_idx] = rst_assert
        else:
            if rst_idx != -1:
                w[rst_idx] = rst_deassert
            if clk_idx != -1:
                w[clk_idx] = (i - 10) % 2
        phys.append(w)
    rng = random.Random(seed)
    cur = [rng.randint(0, 1) for _ in range(n_in)]
    for _ in range(logical):
        if stim == "bench":
            cur = [rng.randint(0, 1) for _ in range(n_in)]
        else:
            for i in range(n_in):
                if i != clk_idx and rng.random() < 0.1:
                    cur[i] ^= 1
            if rst_idx != -1:
                cur[rst_idx] = rst_deassert
        for clk in (0, 1):
            v = list(cur)
            v[clk_idx] = clk
            phys.append(v)
    return phys


# --------------------------------------------------------------------------------------
# references: raw line strings (no giant nested lists)
# --------------------------------------------------------------------------------------
def run_icarus(vfile, phys):
    base = os.path.splitext(vfile)[0]
    tb, vvp, vec, out = base + "_tb.v", base + ".vvp", base + "_in.txt", base + "_out.txt"
    open(vec, "w").write("\n".join("".join(map(str, reversed(v))) for v in phys) + "\n")
    V.generate_icarus_verifier_tb(vfile, tb, vec, out, len(phys))
    # iverilog's scanner overflows on one $fdisplay listing thousands of outputs: write them in chunks
    text = open(tb).read()
    m = re.search(r'\$fdisplay\(outfile, "((?:%b)+)", (.*?)\);\n', text, re.S)
    if m:
        args = [x.strip() for x in m.group(2).split(",")]
        if len(args) > 300:
            parts = ["$fwrite(outfile, \"" + "%b" * len(args[i:i + 200]) + "\", " + ", ".join(args[i:i + 200]) + ");"
                     for i in range(0, len(args), 200)]
            text = text[:m.start()] + "\n".join(parts) + '\n$fwrite(outfile, "\\n");\n' + text[m.end():]
            open(tb, "w").write(text)
    gsc = H.find_gsclib_path(vfile)
    subprocess.run(["iverilog", "-o", vvp, gsc, vfile, tb], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run(["vvp", vvp], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return [l.strip().lower() for l in open(out).read().splitlines() if l.strip()]


def run_verilator(vfile, phys):
    base = os.path.splitext(vfile)[0]
    tb, vec, out, obj = base + "_vl.cpp", base + "_vl_in.txt", base + "_vl_out.txt", base + "_vl_obj"
    module, ports, flat_in, flat_out, _, _ = H.parse_iwls_ports(vfile)
    open(vec, "w").write("\n".join("".join(map(str, v)) for v in phys) + "\n")
    V.generate_verilator_verifier_tb(vfile, tb, module, ports, flat_in, flat_out)
    gsc = H.find_gsclib_path(vfile)
    subprocess.run(["verilator", "-O3", "-Wno-fatal", "--default-language", "1364-2001", "--cc", gsc, vfile, "--exe", tb,
                    "--top-module", module, "--Mdir", obj], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run(["make", "-j", str(os.cpu_count() or 4), "-C", obj, "-f", f"V{module}.mk", f"V{module}"],
                   check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run([f"{obj}/V{module}", vec, out], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return [l.strip() for l in open(out).read().splitlines() if l.strip()]


# --------------------------------------------------------------------------------------
# Darion
# --------------------------------------------------------------------------------------
def run_darion(vfile, phys, flop_names, sim_mode):
    r = B.IWLSVerilogRunner(vfile, Circuit.Circuit, Const, is_reactor=True, is_oop=False, mode="reactor",
                            use_optimize=True, sim_mode=sim_mode)
    c = r.circuit
    outs = list(r.output_objects)
    assert len(outs) == len(r.outputs), "some primary outputs were not found in the Darion circuit"
    by_name = {ic.custom_name: ic for ic in c.get_ics()}
    flop_q = []
    for inst in flop_names:
        ic = by_name.get("DFF_" + inst)
        assert ic is not None, f"no flop IC named DFF_{inst}"
        assert ic.outputs[0].custom_name == "Q", ic.outputs[0].custom_name
        flop_q.append(ic.outputs[0])
    gates = outs + flop_q
    target = Const.COMPILE if sim_mode == "compile" else Const.SIMULATE

    async def go():
        c.optimize()
        for node, val in ((r.const_1_node, Const.HIGH), (r.const_0_node, Const.LOW)):
            if node is not None:
                node.value = val
                c.toggle(node.location, val)
        c.simulate(target)
        Const.set_MODE(target)
        batches = r.build_physical_batches(phys)
        bs = len(r.input_vars) + (r.const_1_node is not None) + (r.const_0_node is not None)
        rows = []
        for b in batches:
            c.batch_toggle(b, bs)
            rows.append("".join("1" if g.output == 1 else "0" if g.output == 0 else "x" for g in gates))
        return rows

    return asyncio.run(go()), len(outs)


# --------------------------------------------------------------------------------------
# --workload tv80: a Z80 program running closed-loop on the tv80 gate-level netlist (IWLS 2005 / Opencores).
# The same environment (reset sequence, combinational ROM/RAM read, write on the rising edge) is implemented
# for an Icarus testbench (golden, 4-state) and a Darion driver; bus traces (control strobes, address, data
# out) are compared every half cycle. There is no Verilator leg: a Verilator testbench running the same
# environment on the Cadence UDP netlist diverges from Icarus within the first instructions while Darion
# matches Icarus, so its trace is not a usable reference (root cause not investigated; see the claims doc).
# Program (loops forever; results land in RAM so the run is checkable without trusting any simulator):
#     0000 31 00 90   LD SP,9000h
#     0003 21 00 80   LD HL,8000h
#     0006 06 00      LD B,0
#     0008 3E 00      LD A,0         ; loop
#     000A 80         ADD A,B
#     000B 77         LD (HL),A
#     000C 23         INC HL
#     000D 04         INC B
#     000E 78         LD A,B
#     000F FE 40      CP 40h
#     0011 C2 08 00   JP NZ,0008h
#     0014 CD 20 00   CALL 0020h
#     0017 C3 06 00   JP 0006h
#     0020 3E 55      LD A,55h
#     0022 32 00 81   LD (8100h),A
#     0025 C9         RET
# After the first pass mem[8000h+i] == i for i < 40h and mem[8100h] == 55h.

TV80_SRC = os.path.join(ROOT, "tests", "IWLS2005", "opencores", "tv80.v")
PROGRAM = {
    0x0000: [0x31, 0x00, 0x90, 0x21, 0x00, 0x80, 0x06, 0x00, 0x3E, 0x00, 0x80, 0x77, 0x23, 0x04, 0x78, 0xFE, 0x40,
             0xC2, 0x08, 0x00, 0xCD, 0x20, 0x00, 0xC3, 0x06, 0x00],
    0x0020: [0x3E, 0x55, 0x32, 0x00, 0x81, 0xC9],
}
RESET_CYCLES = 8
CTRL = ["m1_n", "mreq_n", "iorq_n", "rd_n", "wr_n", "rfsh_n", "halt_n", "busak_n"]


def rom():
    mem = bytearray(65536)
    for base, data in PROGRAM.items():
        mem[base:base + len(data)] = bytes(data)
    return mem


def run_icarus_tv80(work, cycles, src=TV80_SRC, vcd=None):
    """Golden testbench; with vcd, also dumps every net of the tv80 module (one level). Returns trace, RAM check,
    compile seconds, run seconds."""
    dump = f'        $dumpfile("{vcd}"); $dumpvars(1, uut);\n' if vcd else ""
    mem_init = "\n".join(f"        mem[{a}] = 8'h{b:02x};" for a, b in enumerate(rom()) if b)
    tb = f"""`timescale 1ns/1ps
module tb;
    reg clk, reset_n; reg [7:0] di; reg [7:0] mem [0:65535]; integer i, f;
    wire m1_n, mreq_n, iorq_n, rd_n, wr_n, rfsh_n, halt_n, busak_n; wire [15:0] A; wire [7:0] dout;
    tv80 uut (.m1_n(m1_n), .mreq_n(mreq_n), .iorq_n(iorq_n), .rd_n(rd_n), .wr_n(wr_n), .rfsh_n(rfsh_n), .halt_n(halt_n),
              .busak_n(busak_n), .A(A), .do(dout), .reset_n(reset_n), .clk(clk), .wait_n(1'b1), .int_n(1'b1),
              .nmi_n(1'b1), .busrq_n(1'b1), .di(di));
    always @(*) di = (!mreq_n && !rd_n) ? mem[A] : 8'h00;
    always @(posedge clk) if (!mreq_n && !wr_n) mem[A] <= dout;
    initial begin
{dump}        for (i = 0; i < 65536; i = i + 1) mem[i] = 8'h00;
{mem_init}
        f = $fopen("{work}/icarus_trace.txt", "w"); clk = 0; reset_n = 0;
        for (i = 0; i < {2 * cycles}; i = i + 1) begin
            if (i >= {2 * RESET_CYCLES}) reset_n = 1;
            clk = i % 2;
            #1;
            $fdisplay(f, "%b%b%b%b%b%b%b%b%b%b", m1_n, mreq_n, iorq_n, rd_n, wr_n, rfsh_n, halt_n, busak_n, A, dout);
        end
        $fclose(f);
        f = $fopen("{work}/icarus_mem.txt", "w");
        for (i = 0; i < 64; i = i + 1) $fdisplay(f, "%0d", mem[32768 + i]);
        $fdisplay(f, "%0d", mem[33024]);
        $fclose(f); $finish;
    end
endmodule
"""
    open(f"{work}/tb.v", "w").write(tb)
    gsc = H.find_gsclib_path(src)
    t0 = time.perf_counter()
    subprocess.run(["iverilog", "-o", f"{work}/tb.vvp", gsc, src, f"{work}/tb.v"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    t1 = time.perf_counter()
    subprocess.run(["vvp", f"{work}/tb.vvp"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    t2 = time.perf_counter()
    trace = [l.strip().lower() for l in open(f"{work}/icarus_trace.txt")]
    mem = [l.strip() for l in open(f"{work}/icarus_mem.txt")]
    return trace, mem, t1 - t0, t2 - t1


class Tv80Darion:
    """The tv80 environment driven through Darion's API, one half-cycle per step() (same environment as the Icarus
    testbench: reset sequence, combinational ROM/RAM read, write on the rising edge). src may be any copy of tv80.v
    with its .json next to it."""

    def __init__(self, src=TV80_SRC, optimize=True, start=True):
        r = B.IWLSVerilogRunner(src, Circuit.Circuit, Const, is_reactor=True, is_oop=False, mode="reactor",
                                use_optimize=optimize, sim_mode="simulate")
        self.c = c = r.circuit
        _, _, self.flat_in, flat_out, _, _ = H.parse_iwls_ports(src)
        self.inputs = r.input_vars
        outs = list(r.output_objects)
        assert len(self.inputs) == len(self.flat_in) and len(outs) == len(flat_out)
        if optimize:
            c.optimize()
        for node, val in ((r.const_1_node, Const.HIGH), (r.const_0_node, Const.LOW)):
            if node is not None:
                node.value = val
        c.simulate(Const.SIMULATE)
        Const.set_MODE(Const.SIMULATE)
        self.idx_in = {n: i for i, n in enumerate(self.flat_in)}
        idx_out = {n: i for i, n in enumerate(flat_out)}
        self.extra = [(n.location, 1 if n is r.const_1_node else 0) for n in (r.const_1_node, r.const_0_node) if n is not None]
        self.bs = len(self.inputs) + len(self.extra)
        self.cur = {n: 0 for n in self.flat_in}
        self.cur.update({"wait_n": 1, "int_n": 1, "nmi_n": 1, "busrq_n": 1})
        self.mem = rom()
        self.ctrl_g = [outs[idx_out[n]] for n in CTRL]
        self.addr_g = [outs[idx_out[f"A[{b}]"]] for b in range(15, -1, -1)]
        self.dout_g = [outs[idx_out[f"do[{b}]"]] for b in range(7, -1, -1)]
        self.engine_ns = 0
        if start:
            self.start()

    def start(self):
        self.apply({n: self.cur[n] for n in self.flat_in})          # initial application of every input

    def apply(self, changed):
        batch = [(self.inputs[self.idx_in[n]].location, v) for n, v in changed.items()] + self.extra
        t0 = time.perf_counter_ns()
        self.c.batch_toggle(batch, self.bs)
        self.engine_ns += time.perf_counter_ns() - t0

    def step(self, i):
        """Half-cycle i; returns the bus trace row (control strobes, address, data out)."""
        ctrl_g, addr_g, dout_g, cur, mem = self.ctrl_g, self.addr_g, self.dout_g, self.cur, self.mem
        clk = i & 1
        if clk and ctrl_g[1].output == 0 and ctrl_g[4].output == 0:            # mreq_n, wr_n low: write with pre-edge data
            a = int("".join(str(g.output & 1) for g in addr_g), 2)
            mem[a] = int("".join(str(g.output & 1) for g in dout_g), 2)
        changed = {"reset_n": int(i >= 2 * RESET_CYCLES), "clk": clk}
        changed = {k: v for k, v in changed.items() if cur[k] != v}
        for k, v in changed.items():
            cur[k] = v
        if changed:
            self.apply(changed)
        for _ in range(4):                                                     # combinational memory read, settle
            if ctrl_g[1].output == 0 and ctrl_g[3].output == 0:
                nd = mem[int("".join(str(g.output & 1) for g in addr_g), 2)]
            else:
                nd = 0
            diff = {f"di[{b}]": (nd >> b) & 1 for b in range(8) if cur[f"di[{b}]"] != (nd >> b) & 1}
            if not diff:
                break
            cur.update(diff)
            self.apply(diff)
        return "".join(str(g.output) if g.output <= 1 else "x" for g in ctrl_g + addr_g + dout_g)

    def ram_check(self):
        return [str(self.mem[0x8000 + i]) for i in range(64)] + [str(self.mem[0x8100])]


def run_darion_tv80(cycles):
    import gc
    d = Tv80Darion()
    gc.collect()
    gc.disable()
    trace = [d.step(i) for i in range(2 * cycles)]
    gc.enable()
    return trace, d.ram_check(), d.engine_ns / 1e6


def compare_trace(name, got, ref, start):
    mism = compared = 0
    first = None
    for t in range(start, min(len(got), len(ref))):
        for k, (a, b) in enumerate(zip(got[t], ref[t])):
            if b == "x":
                continue
            compared += 1
            if a != b:
                mism += 1
                first = first or (t, k)
    print(f"    {name}: {compared:,} bus bits compared, {mism} mismatches" + (f" (first at half-cycle {first[0]}, bit {first[1]})" if first else ""))
    return mism


def workload_tv80(cycles):
    work = tempfile.mkdtemp(prefix="tv80_")
    try:
        ic_trace, ic_mem, _, _ = run_icarus_tv80(work, cycles)
        expect = [str(i) for i in range(64)] + ["85"]
        print(f"tv80 Z80 program, {cycles:,} cycles ({2 * cycles:,} half-cycles)")
        print(f"  Icarus (golden): RAM check mem[8000h+i]==i for i<64 and mem[8100h]==55h: {'PASS' if ic_mem == expect else 'FAIL ' + str(ic_mem[:6])}")
        trace, mem, ms = run_darion_tv80(cycles)
        print(f"  Darion gate-level flops: RAM check {'PASS' if mem == expect else 'FAIL'}")
        compare_trace("Darion vs Icarus", trace, ic_trace, 2 * RESET_CYCLES + 4)
        x = sum(r.count("x") for r in ic_trace[2 * RESET_CYCLES + 4:]) / max(1, sum(len(r) for r in ic_trace[2 * RESET_CYCLES + 4:]))
        print(f"  Icarus X after reset: {x * 100:.2f}% of traced bus bits; Darion engine time (batch_toggle only): {ms:.1f} ms")
    finally:
        shutil.rmtree(work, ignore_errors=True)


# --------------------------------------------------------------------------------------
# --case-study: a CPU program fails after a design change; find where and why, two ways.
# A copy of tv80 gets one 2-input cell swapped (AND2<->OR2 or NAND2<->NOR2): in the Verilog copy for Icarus, and as a
# one-field type change in a copy of Darion's JSON (so gate locations stay identical to the golden copy). The golden
# design is the reference: both copies run the same Z80 program in the same environment (see workload tv80).
#   Darion: run golden and buggy side by side through the API until the bus traces differ (step N); then reload and
#           replay, comparing after every half-cycle the gates that changed (the visual queue of changed gates) until
#           the first internal difference (step m); report the differing gates whose sources all agree (the root).
#   Icarus: compile both with a VCD dump of every tv80 net, run the whole program, find N from the two bus traces,
#           then m and the root net from the two VCDs plus the netlist's cell connections.
# Choosing the bug (not timed) uses Darion: the first candidate whose effect reaches the bus after reset.
SWAP = {"AND2X1": "OR2X1", "OR2X1": "AND2X1", "NAND2X1": "NOR2X1", "NOR2X1": "NAND2X1"}
TYPE_ID = {"AND2X1": 0, "NAND2X1": 1, "OR2X1": 2, "NOR2X1": 3}
CELL_RE = re.compile(r"^(\s*)(AND2X1|OR2X1|NAND2X1|NOR2X1)(\s+)(\\\S+|\w+)", re.M)
INST_RE = re.compile(r"^\s*([A-Z][A-Z0-9]*X\d+)\s+(\\\S+|\w+)\s*\((.*?)\)\s*;", re.M | re.S)
PIN_RE = re.compile(r"\.(\w+)\s*\(\s*([^)]*?)\s*\)")
OUT_PINS = {"Y", "Q", "QN"}


def net_locations(vfile):
    """Map each net to the JSON location of the gate driving it, using the repo's IWLS parser (in a subprocess, so
    its global MODE does not leak into this process)."""
    code = ("import sys, json; sys.path[:0] = [sys.argv[2], sys.argv[3]]; import iwls_parser as P, Circuit, Const\n"
            "r = P.IWLSVerilogRunner(sys.argv[1], Circuit.Circuit, Const)\n"
            "print(); print(json.dumps({k: v.location for k, v in r.nodes.items() if hasattr(v, 'location')}))")
    out = subprocess.run([sys.executable, "-c", code, vfile, os.path.join(ROOT, "scripts"), os.path.join(ROOT, "reactor")],
                         check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=ROOT).stdout.decode()
    return json.loads(out.strip().splitlines()[-1])


def drain(c):
    seen = set()
    while not c.visual_queue_empty():
        seen.add(c.pop_visual_queue())
    return seen


def darion_first_bus_diff(gold_v, bug_v, steps):
    g, b = Tv80Darion(gold_v), Tv80Darion(bug_v)
    for i in range(steps):
        if g.step(i) != b.step(i):
            return i
    return None


def darion_locate(gold_v, bug_v, n):
    """Replay up to the failing step n, comparing after every half-cycle every gate that changed in either copy. While
    the two states are equal before a step, any difference after it is among the gates that changed, so this finds
    the first internal difference exactly. Loaded without optimize() so locations match the JSON order in both."""
    g, b = Tv80Darion(gold_v, optimize=False, start=False), Tv80Darion(bug_v, optimize=False, start=False)
    gg, gb = g.c.gate_verse, b.c.gate_verse
    for x in (g, b):                     # a gate is queued only if its update flag is clear; loading leaves some set
        x.c.visual_queue_clear()
        for gate in x.c.gate_verse:
            gate.update = False
    for i in range(-2, n + 1):           # -2: state right after loading (constants settled); -1: first application of inputs
        if i == -2:
            diff = [k for k, (x, y) in enumerate(zip(gg, gb)) if x.output != y.output]
        else:
            if i == -1:
                g.start(), b.start()
            else:
                g.step(i), b.step(i)
            diff = sorted(k for k in drain(g.c) | drain(b.c) if gg[k].output != gb[k].output)
        if diff:
            roots = [k for k in diff if all(s is None or gg[s.location].output == gb[s.location].output for s in gg[k].sources)]
            return i, diff, roots, gg, gb
    return None, [], [], gg, gb


def read_vcd(path):
    """Return {net: [(time, value)]} for nets of the DUT scope (vectors split into name[bit]) and the time unit in ps."""
    ids, changes, scope, unit = {}, {}, [], 1
    with open(path) as f:
        for line in f:
            tok = line.split()
            if not tok:
                continue
            if tok[0] == "$timescale":
                spec = " ".join(tok[1:-1]) if len(tok) > 2 else next(f).strip()
                m = re.match(r"(\d+)\s*(\w+)", spec)
                unit = int(m.group(1)) * {"s": 10**12, "ms": 10**9, "us": 10**6, "ns": 1000, "ps": 1}[m.group(2)]
            elif tok[0] == "$scope":
                scope.append(tok[2])
            elif tok[0] == "$upscope":
                scope.pop()
            elif tok[0] == "$var" and len(scope) == 2:
                width, code, name = int(tok[2]), tok[3], tok[4]
                rng = re.match(r"\[(\d+):(\d+)\]", tok[5]) if len(tok) > 6 else None
                if width > 1 and rng:
                    hi, lo = int(rng.group(1)), int(rng.group(2))
                    bits = [f"{name}[{b}]" for b in (range(hi, lo - 1, -1) if hi >= lo else range(hi, lo + 1))]
                else:
                    bits = [name]
                ids.setdefault(code, []).append(bits)
            elif tok[0] == "$enddefinitions":
                break
        t = 0
        for line in f:
            c0 = line[0]
            if c0 == "#":
                t = int(line[1:])
            elif c0 in "01xzXZ":
                for names in ids.get(line[1:].strip(), ()):
                    changes.setdefault(names[0], []).append((t, c0.lower()))
            elif c0 in "bB":
                val, code = line[1:].split()
                for names in ids.get(code, ()):
                    v = val.lower().rjust(len(names), "0" if val[0] == "1" else val[0].lower())
                    for nm, bit in zip(names, v):
                        changes.setdefault(nm, []).append((t, bit))
    return changes, unit


def value_before(ch, t):
    """Value of a change list at the last change strictly before time t (x before any change)."""
    v = "x"
    for tt, vv in ch:
        if tt >= t:
            break
        v = vv
    return v


def first_difference(cha, chb):
    """Earliest time at which the two change lists hold different known (0/1) values, or None. X against a value is
    not counted: in 4-state simulation the swapped gate can resolve X differently (NAND(0,x)=1, NOR(0,x)=x)."""
    times = sorted({t for t, _ in cha} | {t for t, _ in chb})
    va = vb = "x"
    ia = ib = 0
    for t in times:
        while ia < len(cha) and cha[ia][0] <= t:
            va = cha[ia][1]
            ia += 1
        while ib < len(chb) and chb[ib][0] <= t:
            vb = chb[ib][1]
            ib += 1
        if va != vb and va in "01" and vb in "01":
            return t
    return None


def case_study(cycles, seed, max_tries=60):
    work = tempfile.mkdtemp(prefix="case_")
    try:
        gold_v, bug_v = os.path.join(work, "gold", "tv80.v"), os.path.join(work, "bug", "tv80.v")
        for d in ("gold", "bug", "ic_gold", "ic_bug"):
            os.makedirs(os.path.join(work, d))
        shutil.copy(TV80_SRC, gold_v)
        shutil.copy(TV80_SRC[:-2] + ".json", gold_v[:-2] + ".json")
        text = open(TV80_SRC).read()
        gold_json = json.load(open(gold_v[:-2] + ".json"))
        locs = net_locations(gold_v)
        steps = 2 * cycles
        start = 2 * RESET_CYCLES + 4

        # choose the bug (not timed)
        cands = list(CELL_RE.finditer(text))
        random.Random(seed).shuffle(cands)
        for tries, m in enumerate(cands[:max_tries], 1):
            y = dict(PIN_RE.findall(INST_RE.match(text, m.start()).group(3)))["Y"]
            bug_json = [list(e) for e in gold_json]
            entry = next(e for e in bug_json if isinstance(e[2], int) and e[2] == locs[y])   # ICs carry a list in this field
            assert entry[1] == TYPE_ID[m.group(2)], (m.group(4), y, entry[:4])
            entry[1] = TYPE_ID[SWAP[m.group(2)]]
            json.dump(bug_json, open(bug_v[:-2] + ".json", "w"))
            open(bug_v, "w").write(text[:m.start(2)] + SWAP[m.group(2)] + text[m.end(2):])
            n = darion_first_bus_diff(gold_v, bug_v, steps)
            # a latent bug: it reaches the bus, and no gate differs until the program runs (after reset)
            if n is not None and n >= start and darion_locate(gold_v, bug_v, n)[0] >= 2 * RESET_CYCLES:
                break
        else:
            print(f"no mutation in {max_tries} candidates reached the bus within {cycles:,} cycles")
            return
        inst = m.group(4)
        print(f"tv80 running the Z80 program for {cycles:,} cycles ({steps:,} half-cycles); bug: {inst} {m.group(2)} -> "
              f"{SWAP[m.group(2)]} (driving net {y}; candidate {tries} of the shuffled list)")

        # Darion workflow (timed)
        t0 = time.perf_counter()
        n = darion_first_bus_diff(gold_v, bug_v, steps)
        t1 = time.perf_counter()
        mstep, diff, roots, gg, gb = darion_locate(gold_v, bug_v, n)
        t2 = time.perf_counter()
        typed = [k for k, (a, b) in enumerate(zip(gg, gb)) if a.codename.split("-")[0] != b.codename.split("-")[0]]
        loc = lambda s: None if s is None else s.location
        same = all(list(map(loc, a.sources)) == list(map(loc, b.sources)) for a, b in zip(gg, gb))
        print(f"  Darion : bus differs first at half-cycle {n}; first internal difference at half-cycle {mstep} ({len(diff)} gates); "
              f"root {[f'{gg[k].codename} (buggy copy: {gb[k].codename}) @{k}' for k in roots]}")
        print(f"           check: injected gate @{typed}; structure identical {same}; root == injected gate: {roots == typed}")
        print(f"           time: load both + run side by side to half-cycle {n}: {(t1 - t0) * 1e3:.0f} ms; reload + replay comparing "
              f"changed gates + localize: {(t2 - t1) * 1e3:.0f} ms; total {(t2 - t0) * 1e3:.0f} ms")

        # Icarus workflow (timed): compile and run both with a full dump of the tv80 module, then analyse
        t0 = time.perf_counter()
        vcd_g, vcd_b = os.path.join(work, "ic_gold", "d.vcd"), os.path.join(work, "ic_bug", "d.vcd")
        tr_g, _, cg, rg_ = run_icarus_tv80(os.path.join(work, "ic_gold"), cycles, gold_v, vcd_g)
        tr_b, _, cb, rb_ = run_icarus_tv80(os.path.join(work, "ic_bug"), cycles, bug_v, vcd_b)
        t1 = time.perf_counter()
        ni = next((i for i, (a, b) in enumerate(zip(tr_g, tr_b))
                   if i >= start and any(x != y and x in "01" and y in "01" for x, y in zip(a, b))), None)
        chg, unit = read_vcd(vcd_g)
        chb, _ = read_vcd(vcd_b)
        step = 1000 // unit                                             # one half-cycle = #1 at 1 ns, VCD time in units
        first = {net: t for net in chg.keys() & chb.keys() if (t := first_difference(chg[net], chb[net])) is not None}
        mi = min(first.values()) // step if first else None
        cut = (mi + 1) * step                                           # state at the end of half-cycle mi
        known = lambda a, b: a != b and a in "01" and b in "01"
        dnets = {net for net in first if known(value_before(chg[net], cut), value_before(chb[net], cut))}
        drivers = {}
        for _cell, name, body in INST_RE.findall(open(bug_v).read()):
            pins = PIN_RE.findall(body)
            ins = [v for p, v in pins if p not in OUT_PINS and v and not v.startswith("1'b")]
            for p, net in pins:
                if p in OUT_PINS and net:
                    drivers[net] = (name, ins)
        roots_i = [(drivers[net][0], net) for net in sorted(dnets) if net in drivers and
                   not any(known(value_before(chg.get(i, []), cut), value_before(chb.get(i, []), cut)) for i in drivers[net][1])]
        t2 = time.perf_counter()
        mb = (os.path.getsize(vcd_g) + os.path.getsize(vcd_b)) / 2 / 2**20
        print(f"  Icarus : bus differs first at half-cycle {ni}; first internal difference at half-cycle {mi} ({len(dnets)} nets); "
              f"root {roots_i}; root == injected cell: {[r[0] for r in roots_i] == [inst]}")
        print(f"           time: compile {cg + cb:.2f} s, run with full VCD dump {rg_ + rb_:.2f} s (both designs, whole program), "
              f"VCD {mb:.1f} MB per design; analysis (trace diff, VCD parse, localize) {t2 - t1:.2f} s; total {t2 - t0:.2f} s")
        os.makedirs(os.path.join(work, "ic_nodump"))
        _, _, c1, r1 = run_icarus_tv80(os.path.join(work, "ic_nodump"), cycles, gold_v)
        _, _, c2, r2 = run_icarus_tv80(os.path.join(work, "ic_nodump"), max(1, (ni + 2) // 2), gold_v)
        print(f"           reference (not part of the workflow): one design without dump: compile {c1:.2f} s, run whole program {r1:.2f} s, "
              f"run only to half-cycle {ni + 1}: {r2:.2f} s")
    finally:
        shutil.rmtree(work, ignore_errors=True)


def compare(got, ref, start, four_state):
    """Return (mismatches, bits compared, X bits skipped, first mismatch, set of mismatching columns)."""
    mism = x_skipped = compared = 0
    first = None
    cols = set()
    for t in range(start, min(len(got), len(ref))):
        g, rf = got[t], ref[t]
        if g == rf:
            compared += len(g)
            continue
        for i, (a, b) in enumerate(zip(g, rf)):
            if four_state and b == "x":
                x_skipped += 1
                continue
            compared += 1
            if a != b:
                mism += 1
                cols.add(i)
                if first is None:
                    first = (t, i, a, b)
    return mism, compared, x_skipped, first, cols


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("circuit", nargs="?")
    ap.add_argument("--workload", choices=("tv80",), help="run a closed-loop program workload instead of random-stimulus state verification")
    ap.add_argument("--cycles", type=int, default=None, help="--workload: clock cycles (default 20000); --case-study: clock cycles (default 2000)")
    ap.add_argument("--logical", type=int, default=50000, help="logical cycles for the Verilator (2-state) comparison")
    ap.add_argument("--ic-logical", type=int, default=5000, help="logical cycles for the Icarus (4-state) comparison; 0 skips")
    ap.add_argument("--stim", choices=("bench", "run"), default="bench")
    ap.add_argument("--suite", default="itc99")
    ap.add_argument("--case-study", action="store_true", help="tv80: locate one injected bug with Darion's API and with an Icarus VCD workflow")
    ap.add_argument("--seed", type=int, default=1, help="--case-study: seed for choosing the injected bug")
    args = ap.parse_args()
    if args.workload == "tv80":
        return workload_tv80(args.cycles or 20000)
    if args.case_study:
        return case_study(args.cycles or 2000, args.seed)
    if not args.circuit:
        ap.error("circuit is required unless --workload or --case-study is given")

    src = os.path.join(ROOT, "tests", "IWLS2005", args.suite, args.circuit + ".v")
    work = tempfile.mkdtemp(prefix="verify_state_")
    try:
        vfile = os.path.join(work, args.circuit + ".v")
        flops = make_state_netlist(src, vfile)
        shutil.copy(src.replace(".v", ".json"), os.path.join(work, args.circuit + ".json"))
        module, ports, flat_in, flat_out, clk_idx, _ = H.parse_iwls_ports(src)
        rst_idx, _, active_low = H.find_reset_port(flat_in)
        deassert = 1 if active_low else 0
        n_out = len(flat_out)
        names = list(flat_out) + list(flops)
        print(f"{args.circuit}: {len(flops)} flops exposed, {n_out} primary outputs, stim={args.stim}")

        phys = make_vectors(len(flat_in), clk_idx, rst_idx, deassert, args.logical, args.stim)
        start = 50
        ic_phys = phys[: 50 + 2 * args.ic_logical]
        results = {}
        for mode in ("simulate", "compile"):
            t = time.time()
            rows, no = run_darion(os.path.join(ROOT, "tests", "IWLS2005", args.suite, args.circuit + ".v"), phys, flops, mode)
            results[mode] = rows
            print(f"  rx-{'prop' if mode == 'simulate' else 'sweep'}: {len(rows)} vectors in {time.time()-t:.1f}s")

        t = time.time()
        vl = run_verilator(vfile, phys)
        print(f"  verilator reference: {len(vl)} vectors in {time.time()-t:.1f}s")
        for mode, rows in results.items():
            mism, cmpd, xs, first, cols = compare(rows, vl, start, False)
            print(f"    rx-{'prop' if mode == 'simulate' else 'sweep'} vs Verilator: {cmpd:,} bits compared, {mism} mismatches in {len(cols)} column(s) {sorted(names[c] for c in cols)[:5]}")

        if args.ic_logical:
            t = time.time()
            ic = run_icarus(vfile, ic_phys)
            xfrac = sum(r[n_out:].count("x") for r in ic[start:]) / max(1, sum(len(r) - n_out for r in ic[start:]))
            xout = sum(r[:n_out].count("x") for r in ic[start:]) / max(1, n_out * len(ic[start:]))
            print(f"  icarus reference: {len(ic)} vectors in {time.time()-t:.1f}s; X after warmup: {xfrac*100:.2f}% of flop bits, {xout*100:.2f}% of output bits")
            for mode, rows in results.items():
                mism, cmpd, xs, first, cols = compare(rows[: len(ic)], ic, start, True)
                print(f"    rx-{'prop' if mode == 'simulate' else 'sweep'} vs Icarus: {cmpd:,} bits compared, {xs:,} X bits skipped, {mism} mismatches in {len(cols)} column(s) {sorted(names[c] for c in cols)[:5]}")
            mism, cmpd, xs, first, cols = compare(vl[: len(ic)], ic, start, True)
            print(f"    (reference check) Verilator vs Icarus: {mism} mismatches in {len(cols)} column(s) {sorted(names[c] for c in cols)[:5]}")
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
