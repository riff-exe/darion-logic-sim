"""
timing_lib.py - shared infrastructure for tests/test_timing.py
=======================================================================
Measurement and oracle tools for verifying the Reactor real-delay (PRIORITY) engine.

  Engine      per-task commit log (time, gate, value) for EVERY gate, taken from the
              engine's own visual queue. No probe buffers, so no observer effect.
  Bench       netlist builder that tracks fan-in slots / fan-out for the delay formula.
  spec_delay  the documented delay model, encoded independently of the Cython tables.
  RefSim      independent pure-Python discrete-event reference of the same semantics
              (inertial rejection via stale-event check, (time, gate_loc) tie order).
              Also reports "tie hazards": pulses whose width equals a gate delay exactly,
              where the outcome legitimately depends on same-tick ordering.
  icarus_*    structural-Verilog export with per-gate #delay and a trace parser, giving a
              third-party reference simulator for tie-free runs.
  sta         topological longest-path arrival times under the same delay model.
"""

import os
import sys
import heapq
import shutil
import subprocess
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# REACTOR_DIR lets the suite run against an alternative (e.g. mutated) engine build
REACTOR_DIR = os.environ.get("REACTOR_DIR") or os.path.join(ROOT, "reactor")
for _p in (os.path.join(ROOT, "tests", "src"), ROOT, REACTOR_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import Circuit  # noqa: E402
import Const    # noqa: E402

# UI_MODE makes new gates visible to the visual queue, which is how we read commits.
Const.set_UI_MODE(True)

AND, NAND, OR, NOR = Const.AND_ID, Const.NAND_ID, Const.OR_ID, Const.NOR_ID
XOR, XNOR, BUF, NOT = Const.XOR_ID, Const.XNOR_ID, Const.BUFFER_ID, Const.NOT_ID
PIN_IN, VAR, PIN_OUT = Const.IC_INPUT_PIN_ID, Const.VARIABLE_ID, Const.IC_OUTPUT_PIN_ID
KIND_NAME = {AND: "AND", NAND: "NAND", OR: "OR", NOR: "NOR", XOR: "XOR", XNOR: "XNOR",
             BUF: "BUF", NOT: "NOT", PIN_IN: "PIN_IN", VAR: "VAR", PIN_OUT: "PIN_OUT"}
NARY = (AND, NAND, OR, NOR, XOR, XNOR)
SINGLE = (BUF, NOT)

# ---- the documented delay model: d = G[type] + FI[type]*fan_in + FO[type]*fan_out ----
G_DELAY = {AND: 3, NAND: 2, OR: 3, NOR: 2, XOR: 4, XNOR: 4, BUF: 2, NOT: 1, PIN_IN: 0, VAR: 0, PIN_OUT: 0}
FI_DELAY = {AND: 1, NAND: 1, OR: 2, NOR: 2, XOR: 2, XNOR: 2}
FO_DELAY = {AND: 1, NAND: 1, OR: 1, NOR: 1, XOR: 2, XNOR: 2, BUF: 1, NOT: 1, PIN_IN: 1, PIN_OUT: 1}


def spec_delay(kind, fanin, fanout):
    return G_DELAY[kind] + FI_DELAY.get(kind, 0) * fanin + FO_DELAY.get(kind, 0) * fanout


def logic_eval(kind, ins):
    if kind == AND:  return int(all(ins))
    if kind == NAND: return int(not all(ins))
    if kind == OR:   return int(any(ins))
    if kind == NOR:  return int(not any(ins))
    if kind == XOR:  return sum(ins) & 1
    if kind == XNOR: return 1 - (sum(ins) & 1)
    if kind in (BUF, PIN_IN, PIN_OUT): return ins[0]
    if kind == NOT:  return 1 - ins[0]
    raise ValueError(kind)


# =============================================================================
# Netlist extraction / reference simulator
# =============================================================================
def extract_netlist(c):
    """[(kind, [src_loc or -1, ...])] indexed by gate location (flat, IC internals included)."""
    nodes = []
    for g in c.gate_verse:
        if g.id == VAR:
            nodes.append((VAR, []))
        else:
            nodes.append((g.id, list(g._sources)))
    return nodes


def fanout_lists(nodes):
    fo = [[] for _ in nodes]
    for i, (_, srcs) in enumerate(nodes):
        for pin, s in enumerate(srcs):
            if s is not None and s >= 0:
                fo[s].append((i, pin))
    return fo


def node_delays(nodes):
    fo = fanout_lists(nodes)
    return [spec_delay(k, len(s), len(fo[i])) for i, (k, s) in enumerate(nodes)]


def zero_delay_settle(nodes, var_values):
    """Fixed-point zero-delay evaluation (DAG or stable cyclic). var_values: {loc: 0/1}."""
    n = len(nodes)
    out = [0] * n
    for loc, v in var_values.items():
        out[loc] = v
    for _ in range(n + 2):
        changed = False
        for i, (k, s) in enumerate(nodes):
            if k == VAR:
                continue
            v = logic_eval(k, [out[x] for x in s])
            if v != out[i]:
                out[i] = v
                changed = True
        if not changed:
            return out
    return out


class RefSim:
    """Independent reference of the engine's discrete-event semantics."""

    def __init__(self, nodes, init_vars=None, state=None, tick_atomic=False):
        """state: optional settled output of every node (needed for feedback circuits, whose
        resting state depends on history and cannot be recomputed from the inputs alone)."""
        self.nodes = nodes
        self.fo = fanout_lists(nodes)
        self.delay = node_delays(nodes)
        self.var_locs = [i for i, (k, _) in enumerate(nodes) if k == VAR]
        iv = {loc: 0 for loc in self.var_locs}
        if init_vars:
            iv.update(init_vars)
        if state is not None:
            if any(s not in (0, 1) for s in state):
                raise ValueError("engine state still contains UNKNOWN values")
            self.out = list(state)
        else:
            self.out = zero_delay_settle(nodes, iv)
        self.commit_t = {}
        self.tick_atomic = tick_atomic
        self.cur_var = dict(iv)
        self.inv = [[self.out[x] if x >= 0 else 0 for x in s] for (_, s) in nodes]
        self.clock = [0] * len(nodes)
        self.last = list(self.out)
        self.pending = {}
        self.ties = []
        self.t = 0

    def run(self, stimulus, until=None, max_events=50_000_000):
        """stimulus: [(t, loc, val)] relative times. Returns commit trace [(t, loc, val)].

        Default semantics replicate the engine: simultaneous commits are applied one at a time
        in (time, gate_loc) order and the target is re-evaluated after each.
        With tick_atomic=True every commit of a tick is applied first and each affected gate is
        evaluated once, so zero-width intermediate states cannot re-stamp a pending event."""
        heap = []
        var_queues = {}
        for (t, loc, val) in dedupe_wave(stimulus):
            if self.cur_var.get(loc) == val:
                continue
            self.cur_var[loc] = val
            var_queues.setdefault(loc, []).append((t, val))
            heapq.heappush(heap, (t, loc))
        trace = []
        n = 0

        def commit(T, loc):
            kind = self.nodes[loc][0]
            if kind == VAR:
                self.out[loc] = var_queues[loc].pop(0)[1]
            else:
                if T < self.clock[loc]:
                    return None
                self.pending.pop(loc, None)
            v = self.out[loc]
            if self.last[loc] != v:
                self.last[loc] = v
                trace.append((T, loc, v))
                self.commit_t[loc] = T
            return v

        def evaluate(T, tg):
            new = logic_eval(self.nodes[tg][0], self.inv[tg])
            if new != self.out[tg]:
                # same-tick collision of an input flip with the gate's own commit
                # (either order): outcome depends on (time, gate_loc) tie-breaking
                if self.pending.get(tg) == T or self.commit_t.get(tg) == T:
                    self.ties.append((T, tg))
                self.out[tg] = new
                ct = T + self.delay[tg]
                self.clock[tg] = ct
                self.pending[tg] = ct
                heapq.heappush(heap, (ct, tg))

        while heap:
            T = heap[0][0]
            if until is not None and T > until:
                break
            n += 1
            if n > max_events:
                raise RuntimeError("RefSim livelock")
            if not self.tick_atomic:
                T, loc = heapq.heappop(heap)
                v = commit(T, loc)
                if v is None:
                    continue
                for (tg, pin) in self.fo[loc]:
                    self.inv[tg][pin] = v
                    evaluate(T, tg)
            else:
                batch = []
                while heap and heap[0][0] == T:
                    batch.append(heapq.heappop(heap)[1])
                touched = []
                for loc in batch:
                    v = commit(T, loc)
                    if v is None:
                        continue
                    for (tg, pin) in self.fo[loc]:
                        self.inv[tg][pin] = v
                        touched.append(tg)
                for tg in sorted(set(touched)):
                    evaluate(T, tg)
        self.t = until if until is not None else self.t
        return trace


# =============================================================================
# Engine wrapper (commit log + exact waveform driver)
# =============================================================================
class Engine:
    def __init__(self, c):
        self.c = c
        self.last = {}

    def settle(self):
        self.c.drain_timed_queue()
        self.c.visual_queue_clear()
        self.last = {g.location: g.output for g in self.c.gate_verse}

    def now(self):
        return self.c.Global_Clock

    def run(self, until=None, max_tasks=20_000_000):
        """Process tasks with time <= until (absolute), or until the queue is empty."""
        c = self.c
        ev = []
        mt = 0 if until is None else until + 1
        n = 0
        while True:
            # structural edits (connect/disconnect/setlimits) enqueue gates directly; drop
            # them so the only entry after one task is that task's own origin
            c.visual_queue_clear()
            if not c.drain_timed_queue(1, mt):
                break
            n += 1
            if n > max_tasks:
                raise RuntimeError("engine livelock: task cap exceeded")
            while not c.visual_queue_empty():
                loc = c.pop_visual_queue()
                v = c.gate_verse[loc].output
                if self.last.get(loc) != v:
                    self.last[loc] = v
                    ev.append((c.Global_Clock, loc, v))
        return ev

    def drive(self, wave, t0=None, until=None):
        """Apply [(rel_time, var_loc, value)] exactly; returns commit trace with ABSOLUTE times."""
        c = self.c
        base = c.Global_Clock if t0 is None else t0
        ev = []
        for (t, loc, val) in dedupe_wave(wave):
            at = base + t
            if at >= 1:
                ev += self.run(until=at - 1)
            assert at >= c.Global_Clock, f"stimulus at {at} is in the past (clock {c.Global_Clock})"
            c.toggle_timed(loc, val, at - c.Global_Clock)
        ev += self.run(until=until)
        return ev


class Bench:
    """Netlist builder. Locations match gate_verse indices."""

    def __init__(self):
        self.c = Circuit.Circuit()
        self.vars = []
        self.gates = []
        self.eng = None

    def var(self):
        v = self.c.getcomponent(VAR)
        self.vars.append(v)
        return v

    def gate(self, kind, *srcs):
        g = self.c.getcomponent(kind)
        n = len(srcs)
        if kind in NARY and n != 2:
            self.c.setlimits(g, n)
        for i, s in enumerate(srcs):
            self.c.connect(g, s if isinstance(s, int) else s.location, i)
        self.gates.append(g)
        return g

    def connect(self, g, idx, src):
        self.c.connect(g, src if isinstance(src, int) else src.location, idx)

    def start(self):
        self.c.simulate(Const.PRIORITY)
        self.eng = Engine(self.c)
        self.eng.settle()
        return self.eng

    def netlist(self):
        return extract_netlist(self.c)

    def refsim(self, init_vars=None):
        return RefSim(self.netlist(), init_vars)


def new_bench():
    Const.set_MODE(Const.DESIGN)   # structural edits and var presets happen in design mode
    return Bench()


def load_ic_flat(path):
    """Parse an IC json into a flat gate list: [(name, kind, [src entry ids])] with entry ids 1-based."""
    import json
    with open(path) as f:
        data = json.load(f)
    return data[4]


def build_flat_ic(bench, path, inputs):
    """Instantiate an IC json as plain gates (pins become wires). inputs: list of locs/gates
    in IC input-pin order. Returns list of output locs in IC output-pin order."""
    entries = load_ic_flat(path)
    n = len(entries)
    inp_idx = [i for i, e in enumerate(entries) if e[1] == PIN_IN]
    out_idx = [i for i, e in enumerate(entries) if e[1] == PIN_OUT]
    ext = {}
    for k, i in enumerate(inp_idx):
        s = inputs[k]
        ext[i + 1] = s if isinstance(s, int) else s.location
    made = {}
    gate_entries = [i for i, e in enumerate(entries) if e[1] not in (PIN_IN, PIN_OUT)]
    for i in gate_entries:
        made[i + 1] = bench.c.getcomponent(entries[i][1])
        if entries[i][1] in NARY and len(entries[i][4]) != 2:
            bench.c.setlimits(made[i + 1], len(entries[i][4]))

    def resolve(eid):
        e = entries[eid - 1]
        if e[1] == PIN_IN:
            return ext[eid]
        if e[1] == PIN_OUT:
            return resolve(e[4][0])
        return made[eid].location

    for i in gate_entries:
        for pin, s in enumerate(entries[i][4]):
            bench.c.connect(made[i + 1], resolve(s), pin)
    bench.flat_map = {eid: g for eid, g in made.items()}
    return [resolve(i + 1) for i in out_idx]


# =============================================================================
# Static timing (topological longest path under the same delay model)
# =============================================================================
def sta_arrival(nodes):
    """Latest commit time of each node if every input toggles at t=0 (DAG only)."""
    delay = node_delays(nodes)
    n = len(nodes)
    arr = [None] * n
    state = [0] * n

    def visit(i):
        stack = [i]
        while stack:
            u = stack[-1]
            if arr[u] is not None:
                stack.pop()
                continue
            k, s = nodes[u]
            if k == VAR:
                arr[u] = 0
                stack.pop()
                continue
            pend = [x for x in s if x >= 0 and arr[x] is None]
            if pend:
                if state[u] == 1:
                    raise ValueError("combinational loop")
                state[u] = 1
                stack.extend(pend)
            else:
                arr[u] = max([arr[x] for x in s if x >= 0] + [0]) + delay[u]
                stack.pop()

    for i in range(n):
        visit(i)
    return arr


def arrival_from(nodes, src):
    """Latest commit time of each node when only `src` toggles at t=0 (None = not reachable)."""
    delay = node_delays(nodes)
    fo = fanout_lists(nodes)
    arr = {src: 0}
    order = []
    seen = set()

    def dfs(u):
        stack = [(u, iter(fo[u]))]
        seen.add(u)
        while stack:
            node, it = stack[-1]
            for (v, _) in it:
                if v not in seen:
                    seen.add(v)
                    stack.append((v, iter(fo[v])))
                    break
            else:
                order.append(node)
                stack.pop()

    dfs(src)
    for u in reversed(order):
        if u == src:
            continue
        reach = [arr[s] for s in nodes[u][1] if s in arr]
        if reach:
            arr[u] = max(reach) + delay[u]
    return arr


# =============================================================================
# Icarus Verilog reference
# =============================================================================
ICARUS = shutil.which("iverilog") and shutil.which("vvp")
_VPRIM = {AND: "and", NAND: "nand", OR: "or", NOR: "nor", XOR: "xor", XNOR: "xnor",
          BUF: "buf", NOT: "not", PIN_IN: "buf", PIN_OUT: "buf"}


def icarus_trace(nodes, init_vars, stimulus, tail=0, base=0, observe=None, strict_from=0):
    """Run the netlist in Icarus with spec delays. stimulus: [(t, loc, val)] relative to `base`.
    Returns trace [(t_rel, loc, val)] for changes at t >= base (relative to base)."""
    delays = node_delays(nodes)
    lines = ["`timescale 1ns/1ns", "module tb;"]
    for i, (k, _) in enumerate(nodes):
        if k == VAR:
            lines.append(f"  reg n{i} = 1'b{init_vars.get(i, 0)};")
        else:
            lines.append(f"  wire n{i};")
    for i, (k, s) in enumerate(nodes):
        if k == VAR:
            continue
        args = ", ".join([f"n{i}"] + [f"n{x}" for x in s])
        lines.append(f"  {_VPRIM[k]} #({delays[i]}) g{i}({args});")
    watch = range(len(nodes)) if observe is None else observe
    for i in watch:
        lines.append(f'  always @(n{i}) $display("E %0d %0d %b", $time, {i}, n{i});')
    lines.append("  initial begin")
    t_prev = 0
    lines.append(f"    #{base};")
    t_prev = base
    last_t = base
    for (t, loc, val) in dedupe_wave(stimulus):
        at = base + t
        if at > t_prev:
            lines.append(f"    #{at - t_prev};")
            t_prev = at
        lines.append(f"    n{loc} = 1'b{val};")
        last_t = max(last_t, at)
    lines.append(f"    #{tail + 1};")
    lines.append("    $finish;")
    lines.append("  end")
    lines.append("endmodule")
    with tempfile.TemporaryDirectory() as d:
        src = os.path.join(d, "tb.v")
        with open(src, "w") as f:
            f.write("\n".join(lines))
        subprocess.run(["iverilog", "-o", os.path.join(d, "t.vvp"), src], check=True,
                       capture_output=True)
        out = subprocess.run(["vvp", os.path.join(d, "t.vvp")], check=True,
                             capture_output=True, text=True).stdout
    trace = []
    for ln in out.splitlines():
        if not ln.startswith("E "):
            continue
        _, t, loc, v = ln.split()
        t = int(t)
        if t < base:
            continue
        if v not in ("0", "1"):
            if t - base >= strict_from:
                raise RuntimeError(f"Icarus produced {v!r} on n{loc} at t={t - base}")
            continue
        trace.append((t - base, int(loc), int(v)))
    return trace


# =============================================================================
# Helpers
# =============================================================================
def dedupe_wave(wave):
    """Time-sorted stimulus keeping only the last assignment per (time, variable)."""
    last = {}
    for (t, loc, val) in wave:
        last[(t, loc)] = val
    return [(t, loc, v) for (t, loc), v in sorted(last.items())]


def canon(trace):
    return sorted(trace)


def first_diff(a, b):
    a, b = canon(a), canon(b)
    for i in range(max(len(a), len(b))):
        x = a[i] if i < len(a) else None
        y = b[i] if i < len(b) else None
        if x != y:
            return i, x, y
    return None


def commits_of(trace, loc):
    return [(t, v) for (t, l, v) in trace if l == loc]
