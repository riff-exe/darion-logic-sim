"""
SIMA ablation runner: times Darion rx-prop / rx-sweep from a chosen reactor build directory.

Build two copies of reactor/ from identical sources and flags, one with -DDARION_EVAL_SWITCH added to
CXXFLAGS (type-switch evaluator) and one without (SIMA), then:

    python tests/ablation_eval.py <reactor_build_dir> <label> b14 b15 b17

Both variants must print the same `evals` and `fp` (same work, same final state); only the time differs.

Netlist export for the standalone layout ablation (tests/ablation_layout.cpp --netlist):

    python tests/ablation_eval.py --export <reactor_build_dir> b15 out.net [raw]

writes the gate array (type, output, sources) after reset and warm-up plus the benchmark's input vectors. `raw`
exports the unoptimized (as-parsed) layout instead of the optimized one.

Cost of the UI coupling and API latency (run pinned: taskset -c 2):

    python tests/ablation_eval.py --ui-cost <reactor_build_dir> b15 prop|sweep   # engine time with the visual queue active vs blind
    python tests/ablation_eval.py --latency <reactor_build_dir> b15              # per-call API latency (median, p99, max)
"""
import os, sys, random, gc, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
    print(__doc__); sys.exit(0)
EXPORT = sys.argv[1] == "--export"
MODE_FLAG = sys.argv[1] if sys.argv[1] in ("--ui-cost", "--latency") else None
if EXPORT or MODE_FLAG:
    sys.argv.pop(1)
rdir, label = sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else ""
sys.path.insert(0, ROOT + "/tests/src"); sys.path.insert(0, ROOT + "/tests"); sys.path.insert(0, ROOT)
sys.path.insert(0, ROOT + "/editor/tools")
sys.path.insert(0, rdir)
import Const, Circuit
assert os.path.dirname(os.path.abspath(Circuit.__file__)) == os.path.abspath(rdir), Circuit.__file__
import benchmark_iwls as B
LOGICAL = int(os.environ.get("LOGICAL", 3000)); REPS = int(os.environ.get("REPS", 3))


SUITES = {"itc99": ("IWLS2005/itc99", True), "opencores": ("IWLS2005/opencores", True), "iscas85": ("ISCAS85", False), "epfl": ("EPFL_parsed", False)}

def _runner(spec, mode, optimize=True):
    """spec is `circuit` (ITC99) or `suite/circuit`. IWLS suites are sequential (reset sequence, own runner);
    ISCAS85 and EPFL are combinational (benchmark.VerilogRunner, no reset)."""
    suite, name = spec.split("/") if "/" in spec else ("itc99", spec)
    sub, iwls = SUITES[suite]
    path = f"{ROOT}/tests/{sub}/{name}.v"
    sm = "compile" if mode == "sweep" else "simulate"
    if iwls:
        return B.IWLSVerilogRunner(path, Circuit.Circuit, Const, is_reactor=True, mode="reactor", use_optimize=optimize, sim_mode=sm)
    import benchmark as BM
    return BM.VerilogRunner(path, Circuit.Circuit, Const, is_reactor=True, use_optimize=optimize, mode="reactor", sim_mode=sm)

def _warm(r, c, bs, nin, vectors):
    if hasattr(r, "build_reset_batches"):
        c.batch_toggle([x for b in r.build_reset_batches(50) for x in b], bs)
    rng = random.Random(42)
    lg = [[rng.randint(0, 1) for _ in range(nin)] for _ in range(vectors)]
    c.batch_toggle([x for b in r.build_batches(lg[:20]) for x in b], bs)
    return lg

def export(name, path, optimize):
    r = _runner(name, "prop", optimize)
    c = r.circuit
    Const.set_MODE(Const.SIMULATE)
    nin = len(r.input_vars)
    bs = nin + (1 if getattr(r, "const_1_node", None) is not None else 0) + (1 if getattr(r, "const_0_node", None) is not None else 0)
    lg = _warm(r, c, bs, nin, LOGICAL)
    vecs = r.build_batches(lg[20:])
    gates = list(c.gate_verse)
    assert all(g.location == i for i, g in enumerate(gates))
    with open(path, "w") as f:
        f.write(f"{len(gates)} {len(vecs)}\n")
        for g in gates:
            src = [s for s in g._sources if s != -1] if g.id != 9 else []
            f.write(f"{g.id} {g.output} {len(src)} {' '.join(map(str, src))}\n")
        for v in vecs:
            f.write(f"{len(v)} {' '.join(f'{l} {x}' for l, x in v)}\n")
    print(f"exported {name} ({'optimized' if optimize else 'raw'}): {len(gates)} gates, {len(vecs)} vectors -> {path}")

def _settled(name, mode, vectors=200):
    r = _runner(name, mode)
    c = r.circuit
    Const.set_MODE(Const.COMPILE if mode == "sweep" else Const.SIMULATE)
    nin = len(r.input_vars)
    bs = nin + (1 if getattr(r, "const_1_node", None) is not None else 0) + (1 if getattr(r, "const_0_node", None) is not None else 0)
    lg = _warm(r, c, bs, nin, max(vectors, LOGICAL))
    return r, c, nin, bs, lg

def ui_cost(name, mode):
    """Engine time of batch_toggle with every gate's update flag cleared (each changed gate is pushed once into
    visual_queue, as with a UI attached) versus set (nothing queued), plus the Python drain of that queue."""
    import statistics as st
    r, c, nin, bs, lg = _settled(name, mode, LOGICAL)
    flat = r.flatten_batches(r.build_batches(lg[20:LOGICAL]))
    gates = list(c.gate_verse)
    def prep(flag):
        c.visual_queue_clear()
        for g in gates: g.update = flag
    res = {"blind": [], "ui-queue": [], "ui-queue+drain": []}; keys = list(res); qn = 0
    gc.collect(); gc.disable()
    for rep in range(7):                                  # rotate the variant order every repeat
        for k in keys[rep % 3:] + keys[:rep % 3]:
            prep(k == "blind"); ms = c.batch_toggle(flat, bs); drain = 0.0
            qn = c.visual_queue_size() if k != "blind" else qn
            if k == "ui-queue+drain":
                t = time.perf_counter()
                while not c.visual_queue_empty(): c.pop_visual_queue()
                drain = (time.perf_counter() - t) * 1e3
            res[k].append((ms, drain))
    gc.enable()
    b = st.median(x[0] for x in res["blind"])
    print(f"{name} {mode}: {len(gates)} gates, {len(flat)} toggles, distinct gates queued per run {qn}")
    for k, v in res.items():
        e = st.median(x[0] for x in v)
        print(f"  {k:15s} engine {e:9.1f} ms ({e / b:5.3f}x blind, spread {100 * (max(x[0] for x in v) - min(x[0] for x in v)) / e:4.1f}%)  python drain {st.median(x[1] for x in v):7.2f} ms")

def latency(name, n=20000):
    """Per-call latency of the Python-facing API on a settled circuit (median / p99 / max, microseconds)."""
    r, c, nin, bs, lg = _settled(name, "prop")
    locs = [v.location for v in r.input_vars]; rng = random.Random(1); state = [0] * nin
    outs = r.output_objects
    def single(i):
        k = rng.randrange(nin); state[k] ^= 1; c.toggle(locs[k], state[k])
    def batch1(i):
        k = rng.randrange(nin); state[k] ^= 1; c.batch_toggle([(locs[k], state[k])], 1)
    def vec_all(i):
        for k in range(nin): state[k] = rng.randint(0, 1)
        c.batch_toggle([(locs[k], state[k]) for k in range(nin)], nin)
    cases = (("empty cpdef call (floor)", lambda i: c.visual_queue_size()), ("read gate.output", lambda i: outs[i % len(outs)].output),
             ("toggle(loc, val)", single), ("batch_toggle, 1 input", batch1), ("batch_toggle, all inputs", vec_all))
    gc.collect(); gc.disable()
    print(f"{name}: {len(list(c.gate_verse))} gates, {nin} inputs, {n} calls each")
    for nm, fn in cases:
        t = []
        for i in range(n):
            a = time.perf_counter_ns(); fn(i); t.append(time.perf_counter_ns() - a)
        t.sort()
        print(f"  {nm:26s} median {t[n // 2] / 1e3:8.2f} us   p99 {t[int(n * .99)] / 1e3:8.2f} us   max {t[-1] / 1e3:9.1f} us")
    gc.enable()

def one(name, mode):
    r = B.IWLSVerilogRunner(f"{ROOT}/tests/IWLS2005/itc99/{name}.v", Circuit.Circuit, Const, is_reactor=True, mode="reactor",
                            use_optimize=True, sim_mode=("compile" if mode == "sweep" else "simulate"))
    c = r.circuit
    Const.set_MODE(Const.COMPILE if mode == "sweep" else Const.SIMULATE)
    nin = len(r.input_vars)
    bs = nin + (1 if r.const_1_node is not None else 0) + (1 if r.const_0_node is not None else 0)
    c.batch_toggle(r.flatten_batches(r.build_reset_batches(50)), bs)
    rng = random.Random(42)
    lg = [[rng.randint(0, 1) for _ in range(nin)] for _ in range(LOGICAL)]
    c.batch_toggle(r.flatten_batches(r.build_batches(lg[:20])), bs)
    flat = r.flatten_batches(r.build_batches(lg[20:]))
    c.eval_count = 0; gc.collect(); gc.disable()
    ms = c.batch_toggle(flat, bs)
    gc.enable()
    # fingerprint of final state so we can confirm both variants computed the same thing; it is weighted by gate
    # position, so compare it across builds of the same mode only (prop and sweep lay out gate_verse differently)
    fp = sum((g.output & 3) * (i % 7 + 1) for i, g in enumerate(c.gate_verse)) & 0xFFFFFFFF
    return ms, c.eval_count, fp

if MODE_FLAG == "--ui-cost":
    ui_cost(label, sys.argv[3]); sys.exit(0)
if MODE_FLAG == "--latency":
    latency(label); sys.exit(0)
if EXPORT:
    export(label, sys.argv[3], not (len(sys.argv) > 4 and sys.argv[4] == "raw"))
    sys.exit(0)
for name in sys.argv[3:]:
    for mode in ("prop", "sweep"):
        res = [one(name, mode) for _ in range(REPS)]
        best = min(x[0] for x in res)
        assert len({x[2] for x in res}) == 1
        print(f"{label:6s} {name:4s} {mode:5s} best {best:9.1f} ms  all {[round(x[0],1) for x in res]}  evals {res[0][1]}  fp {res[0][2]}", flush=True)
