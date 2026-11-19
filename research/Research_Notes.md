# Research notes: design, measurements and their scope

This file explains the ideas behind the measurements in `Claims.md`, what each result does and does not show, and how to reproduce it. Numbers are in `Claims.md`; where the two files differ, `Claims.md` applies. The timing and delay model is documented in `Timing_Report.md`. No publication venue or deadline is set: this is an open research effort on the engine and its measurements.

---

## 1. Scope and positioning

**What Darion is.** A gate-level logic simulator with an API and a UI: a simulator that can be inspected while it runs. A netlist loads in milliseconds, inputs can be toggled, any gate can be read, changed gates are reported through a queue, and real propagation delays can optionally be simulated. The engine is designed so that this interactivity costs little speed.

**Reference points.** Icarus Verilog (event-driven reference) and Verilator (compiled simulator) serve as correctness oracles and as reference points for what event-driven and compiled simulation deliver. The second comparison is Darion's own object-oriented engine (`reactor_oop`), used for the data-oriented design comparison. Comparisons with the Digital simulator (sections 3b-3d) are additional material and use scratch scripts that are not in the repository. Darion is single-threaded and is not designed to match Verilator's throughput; its purpose is an observable, interactive engine at usable speed.

**Circuit coverage.** Every circuit in the repository's suites appears in the master-test reports (`Benchmark/master_test.md`): ITC99 21, OpenCores 21, EPFL 11, EPFL large 8, ISCAS85 10 (c17 excluded as trivial), ISCAS89 15, plus DMA and Hyp (the EPFL mammoth set, one circuit, `hyp`). Some OpenCores designs and the large Faraday designs (only DMA is in the repository) are not included: they need high-impedance (tri-state) values, which Darion does not model (it has 0, 1 and unknown), or were not run. Circuits that require high-impedance values are outside the current scope.

**Tooling.** The netlist parsers and exporters in this repository are test and benchmark scripts, not part of Darion. Load times measured from `.v` files come from that tooling; Darion's own input is its JSON format.

**What is measured.** The engine and its API: simulation cost, API call latency, and the cost of keeping changed-gate information for a client (the visual queue) and draining it. Rendering and UI frame rates are not measured.

**Authorship.** The engine and the API are the author's work; the UI was developed by a collaborator. UI features, usability and rendering performance are not part of the measurements; the UI shows that the API supports an interactive client.

**Earlier statement of the goal.** ESCAPE (Fleurkens, PhD thesis, TU Eindhoven 1996) argued that an interactive design and simulation system need not cost simulator performance; it embedded an event-driven simulator in an editor with incremental model updates and an API. Darion addresses the same goal at gate level on current hardware, with a data-oriented engine, SIMA, a live-size oscillation budget and the sweep schedule, and with a measured observation cost.

**Measured position.** The engine loads netlists in milliseconds and exposes every gate. Its throughput is a fixed factor below a compiled simulator. After the Verilator library correction (2026-10-22, Claim 9), Verilator is faster on all 88 master-test circuits, with suite geomeans of 7.0x on ITC99, 13.3x on OpenCores, 10.0x on DMA and 9-16x on ISCAS85, ISCAS89 and EPFL (`rx-sweep` is 11x behind on EPFL large). On the sequential suites part of this gap is the flop model: Darion simulates each flop as 10 gates (or as a macro), Verilator as one behavioural register. A same-netlist comparison with gate-level flops in Icarus and Verilator is in progress (`TODO.md`). Earlier figures ("within a small factor", Darion ahead on b17, b18, b19 and vga_lcd) came from Verilator's blocking lowering of the library flops and were replaced.

**Statements the data does not support.** Darion being faster than Verilator in any form; timing accuracy against real hardware (the delay model is exact for its own definition and is not calibrated to a cell library); anything about multithreaded Verilator (not tested); and the earlier "low switching activity" and "code footprint" explanations of a large-netlist lead (no such lead exists with the corrected model).

---

## 1b. Summary of results and relation to prior work (2026-10-21, updated)

**No prior implementation found** in the literature reviewed (Maurer 1993-2000, Teiche/Apple 2019, classical input counting, and the oscillation limits of Logisim, Digital, Verilator, GHDL, Vivado and ModelSim):
1. SIMA: (seed, mask, invert) over one incrementally kept count, with existence and parity from one masked AND. Measured 1.35-1.5x over a type switch.
2. A type-agnostic O(1) edge update `logic += (new == edge.seed) - edge.last`: one instruction stream for every gate.
3. A live-size oscillation budget V+1: O(1) under editing, sound on acyclic logic, certifies a traversed loop, sufficient for any single loop. 0 false alarms on 30 circuits; a ring caught in 0.92 ms on 356k gates.
4. Non-fatal handoff of non-convergence to timed simulation (the other tools reviewed stop with an error), which makes the 2V default safe.
5. A measurement: the dispatch trade-off Maurer argued for in 2000 has reversed on modern CPUs (about 2x, attributed by ablation).

**Supported results that are not new in themselves:** the data-oriented engine (enabled by SIMA); state-level correctness against Icarus and Verilator, including a CPU program; near-zero observation cost and the bug-localisation case study; the Verilator reference problem (blocking lowering of UDP flops) and the corrected speed comparison; millisecond turnaround; breadth up to 420k gates; native-flop evidence for macros.

**Other results (no re-runs):**
- **Sweep (Claim 5).** The only preprocessing is one O(V+E) topological sort, which places cyclic groups contiguously when it stalls; there is no loop analysis. Sequential ICs are cut at their output boundary (currently by name). Loops are detected at runtime by one index comparison and handed to the event-driven engine. That path is non-fatal for oscillation, and nothing has to be re-analysed after an edit. The index comparison is LECSIM's (1988/1990: insertion into an already-scanned level sets an `unstable` flag). LECSIM needs DFS SCC detection and feedback-path breaking before it can levelize, answers a back edge with a repeated full pass under a fixed cap (2^m+1 or a user limit), and must recompile after every edit. EPICS also needs static SCCs; Verilator stops with a fatal error. Event-driven simulation does not need loop analysis (Ulrich 1969 says so explicitly) and levelized simulation does; the sweep keeps levelized order without the analysis by falling back to event-driven evaluation on back edges. Verified with a live ring in b15 and b19 (0 mismatches). It also does 200x fewer evaluations than propagate on hyp and accounts for the c6288 result; it is a second engine mode in the same structure.
- **Turnaround (Claim 8).** Holds on every suite. The trade-off itself (a fixed engine loading data, first results far sooner, small speed cost) is Maurer's 1996 argument, so it is reported as a measurement at current scale. Claim 9's earlier crossover and code-footprint explanation were measured against Verilator's blocking-UDP flop model; with the corrected model Verilator is ahead on all 88 circuits (2026-10-22).
- **Native flops (Claim 12):** 2.2-5.1x over gate-level flops and 0 mismatches; the evidence base for macros.
- **Claims 10 and 11** are supporting evidence, not speed claims: 10 supports the sweep (the 1,756x figure against Icarus is a single-circuit maximum); 11 is the OOP IPC drop (4.04 to 0.26) against about 4.7 for the flat engines, supporting Claim 13.
- **Claims 4 and 6:** the 24-byte record and inertial delay.
- **Retyping (Claim 2):** a bug found by the exhaustive suite and fixed; not a user feature.

**Limits:** two x86 machines (Zen 5 desktop, Zen 3 laptop), no Intel or ARM; single-threaded; no high-Z; 2V is a calculated default that XOR-heavy loops exceed; the ablation harness reads about 0.25 below the engine.

## 2. Concepts

### 2.1 Event-driven versus cycle-based simulation
- *Cycle-based / compiled* (Verilator): the whole circuit is turned into straight-line code. Every cycle executes all of it, whether or not anything changed. Fast per gate, no scheduling cost, but cost scales with circuit size, and the generated code can become huge.
- *Event-driven* (Icarus, Darion): only gates whose inputs changed are evaluated; changes are pushed through the fan-out. Cost scales with *activity*, but each evaluation has overhead (queues, pointer following).
- Darion has two schedules over the same engine: `propagate` (queue-driven, true event-driven) and `sweep` (walks the topologically ordered array between the lowest and highest changed gate and skips unmarked gates). `sweep` is cheaper per gate when activity is moderate; `propagate` wins when activity is very sparse.
- Important and counter-intuitive (Claim 9): Darion's "activity" is not low. About 9–10% of gate outputs change per vector on b15–b19, and the floor does not fall when data inputs go quiet, because the clock and the gate-level flip-flop expansion keep switching. So do not explain Darion's wins by "circuits are mostly idle".

### 2.2 The gate representation (SIMA, Claim 1)
Every gate is the same 24-byte struct. `logic` is a running count of inputs equal to the gate's `seed` (0 for AND/NAND/NOT-style, 1 for OR/NOR/XOR/XNOR/BUF). One rule evaluates all types: `output = bool(logic & mask) ^ invert`. `mask = 0xFF` asks "is the count non-zero" (existential), `mask = 1` asks "is the count odd" (parity). Each fan-out edge (`Profile`, 16 B) caches the target's seed and the last contribution, so a source changing updates the target's counter in O(1) without reading its other inputs.
- **Novelty (superseded by "What SIMA really is" below; kept for the citation list):** the counting idea is classical (input counting, 1970s–1990) and close prior art exists (Maurer's US patents 5,856,933 and 6,131,081, and his ICCAD 2000 paper on event-driven simulation without conditionals: counting of dominant inputs, deferred output inversion, XOR/XNOR by change events, eight gate types). The new element is the uniform arithmetic formulation, its verification and the measured effect against a type switch, not the algorithm; Maurer's work is the closest prior art.
- **Why it matters for performance:** there is no per-type branch to mispredict. That is the whole point of the ablation below.

**What SIMA is (2026-10-21).** The new element is the formulation, not the idea of counting.
1. *One instruction for two predicates.* The eight elementary gates are symmetric functions, and only two questions are asked of the input count: "non-zero?" (AND/OR/NAND/NOR/BUF/NOT) and "odd?" (XOR/XNOR). Both are `(count & mask) != 0`, with mask 0xFF for existence and 0x01 for parity. A single AND instruction implements both, so no table and no per-type code are needed.
2. *A factorisation of the gate basis* into three independent one-byte parameters: what to count (`seed`), which question (`mask`), polarity (invert bit). XOR and OR share one counter and differ only in the mask. Maurer used per-class routines; Teiche/Apple uses a table; SIMA is arithmetic.
3. *A type-agnostic update.* `target.logic += (new == edge.seed) - edge.last` contains no gate type and no branch. Classical counting branches on type and value; Maurer swaps code pointers. The whole hot path (update, evaluate, enqueue) is the same instruction stream for every gate.
4. *Edge-local inputs to the update.* The seed cached on the edge lets the contribution be computed from the source's output and edge data only, off the critical path of the target's load. `evaluate()` reads only `logic`, `mask`, `flags` and `inputlimit`, all in the target's first 8 bytes (one word).
5. *Cost independent of fan-in and type.* One byte counts only inputs at one value; nothing is rescanned or stored per input except the edge's cached byte.
6. *The enabler of the data-oriented engine.* Because every gate runs identical code, gates need no types, objects or vtables, so they can be identical 24-byte records in one ordered array. Measured: the rule alone 1.35-1.5x over a type switch (harness, real circuits), 1.1-1.7x on the evaluation step in the real engine (Claim 1); removing per-gate objects and dispatch about 2x over the OOP engine (Claim 13).
- *Novelty statement:* "To our knowledge, no prior work encodes the gate basis as (seed, mask, invert) over a single incrementally maintained count, evaluates existence and parity with one masked AND, and keeps the edge update type-agnostic" (prior art checked: Maurer 1993-2000, Teiche/Apple 2019, classical input counting; audit 0.3-0.5).
- *Limits to state:* the unknown value is handled outside the rule by a separate, normally predictable branch; the 8-bit count caps fan-in at 255.

### 2.3 What "OOP" and "data-oriented" mean here
- **OOP engine (`reactor_oop`):** each gate is a separately heap-allocated C++ object of a subclass (AND_Gate, OR_Gate, ...), 40 bytes (a vtable pointer plus fields). Evaluating a gate calls a virtual `compute()` through the vtable.
- **Data-oriented engine (`reactor`):** all gates are 24-byte plain structs in one contiguous array, evaluated by the single rule above; gate "identity" is an array index; the array is reordered topologically (`optimize`), so processing order matches memory order.
- Both keep fan-out lists as separately allocated arrays of the same 16-byte `Profile` entries, so edge storage is *not* a difference.

### 2.4 The microarchitecture vocabulary
- **Branch misprediction:** the CPU guesses which way a branch goes to keep its pipeline full. A wrong guess flushes the pipeline (on the order of 15–20 cycles lost; not measured on this CPU). Data-dependent branches that vary per gate are the expensive kind.
- **Indirect branch / virtual call:** the target address comes from memory (the vtable), not from the instruction. The CPU needs a *target* prediction, not just taken/not-taken. If consecutive gates have different types the target changes and predictions fail. Besides misprediction, an indirect call also cannot be inlined, so the compiler cannot overlap the work with neighbours: measured ~2× per evaluation even with **zero** mispredictions (Section 4, finding 1).
- **`switch(type)` is also an indirect branch** (compiled to a jump table), which is why it recovers little of the virtual-call cost. This is the key counter-argument to "just use a switch".
- **Predictor memorization:** modern predictors use branch/target *history*. If the same sequence of gate types repeats every iteration (a repeated test vector) and is short enough, the predictor learns it and mispredicts almost nothing. Real simulation does not repeat, so micro-benchmarks that repeat the same input flatter the OOP engine at small sizes (measured: the misprediction onset moves down about a decade when the sequence varies).
- **Cache levels:** L1 (small, fast), L2, L3 (shared, 32 MB here), DRAM. A structure that fits a level is fast; crossing the level costs a step, not a slope. Pointer-chasing to scattered heap objects is the worst case; contiguous arrays are prefetched by hardware.
- **IPC (instructions per cycle) alone is not evidence of speed.** OOP also reaches ~4 IPC on tiny circuits. Use cycles/time, and use IPC only to explain *why* (Claim 11). An IPC figure on its own is not reported as a result.
- **PMU counters** (`perf`): cycles, instructions, branch misses, L1/L2 misses. Whole-run totals are noisy across runs by a few percent; always report repeats and spread.

### 2.5 Why fan-out edge walking is the unit of cost
The engine's work is "visit an edge": read the profile, update the target's counter, re-evaluate the target, maybe enqueue it. All results are therefore reported per **edge evaluation** (ns/edge, cycles/edge), which is identical across variants because they do the same work (verified by identical counts and fingerprints).

---

## 3. Evidence map: claim, evidence, strength, scope

| # | Claim | Evidence | Strength | Statement the data supports | Statement the data does not support |
|---|---|---|---|---|---|
| A | Engine is correct | 0 mismatches vs an independent oracle (~800k reads, fuzz); state of every flip-flop plus outputs vs Icarus (ITC99 b14, b15, b17, b19; Verilator too; since 2026-10-22 also all 21 OpenCores designs and Faraday DMA, the multi-clock ones with every clock driven as a clock); output verifiers on ISCAS85, ISCAS89, EPFL, EPFL large and hyp; tv80 Z80 program trace vs Icarus (318k bus bits, 0 mismatches, RAM check passes; re-run 2026-10-22); 1,980-case retype test; 22-topology and 44-case timing suites | Strong | "matches Icarus and Verilator at the state level on ITC99 and a real CPU workload" | "formally verified"; Icarus is 4-state, Verilator 2-state, X bits are skipped and counted |
| B | Gate retyping (used when ICs are created) is correct | `Gate.retype`, exhaustive pair test (fails on pre-fix, passes on fixed) | Strong, but minor | one sentence in the verification section, as a bug found and fixed by testing | listing it as a feature or a live-editing capability; "3-byte write" (not supported) |
| C | The data-oriented engine needs about half the cycles of the OOP engine on real circuits (headline: full-engine runs in `Benchmark/master_test.md`, per suite) | all 88 master-test circuits in 8 suites: median 2.08x the cycles for OOP (single runs; suite medians 1.67-2.57x, 87 of 88 at 1.5x or more); `perf.py` repeats: 1.90–2.12x on b15/b17/b18/b19 (9 repeats, spread 3–5%); 1.5–3.2x on 20 other circuits (7 repeats, re-measured 2026-10-22; 3.4x in the earlier run); Zen 3 laptop 1.7–2.9x | Strong on Zen 5, confirmed on Zen 3 | "about 2x fewer cycles across eight benchmark suites" | one circuit's single-run number as the headline |
| D | The gap is mostly dispatch + evaluation rule, not layout | ablation harness on synthetic AND on 24 real netlists (ITC99, ISCAS85, EPFL, OpenCores); harness ratio correlates r=0.89 with the full-engine cycle ratio but underestimates it by ~0.25 (Section 4) | Strong on ranking, moderate on magnitude | "attributed; the harness gives a lower bound on the dispatch/rule share" | "layout does not matter" (it does when placement is scattered / exceeds cache) |
| E | UI coupling costs the engine nothing | visual-queue active vs blind: 0.995–1.004x; drain 0.2–0.7 ms; API latency 0.25–0.34 us median per toggle, worst seen 0.69 ms on 356k gates | Strong for the engine side | "decoupling is free on the engine side; interaction latency is far below a frame" | anything about rendering cost (not measured) |
| F | Turnaround advantage | all suites: load faster than Icarus compile on 88/88 circuits (2.4–27x) and than a Verilator build on 87/87 (143–22,455x); ITC99: Verilator build 6–161 s versus Darion load 10–554 ms (JSON, plus 1–118 ms `optimize()`), ~90x including parse on b19. The load builds the full inspectable DESIGN-mode circuit; the price is memory: median 4.2x Verilator's (16–113x on the largest designs), and more than Icarus on the combinational suites (49 of 88 circuits). Prior art for the trade-off: Maurer 1996, LECSIM | Strong as a measurement, not new as an idea | "no compile step; the loaded circuit is immediately inspectable; costs several times Verilator's resident memory" | headline 237x/1,756x without qualifiers; "uses less memory than Icarus" in general |
| G | Throughput vs Verilator | Verilator faster on all 88 master-test circuits once its flop model is correct (ITC99 2.6-15x, OpenCores 5.2-42x, DMA 10x; combinational suites 9-16x); the earlier Darion leads on b17, b18, b19 and vga_lcd came from Verilator's blocking lowering of the library UDP flops (Claim 9, 2026-10-22) | Strong (as positioning) | "a fixed factor behind a compiled simulator, while interactive and loading in milliseconds"; state that on sequential suites Darion simulates gate-level flops and Verilator behavioural registers | "faster than Verilator"; "crossover"; "because of low activity"/"code footprint" |
| H | Delay model | exact for its linear load model, 156 gate/fan-in/fan-out combos, independent oracle + Icarus with same #delays | Strong within scope | "exact for its model, not calibrated" | "accurate to real hardware" |

Statements with weak or no support: the 1,756x figure against Icarus (a single-circuit maximum), IPC 4+ as a result (not supported on real circuits), the low-activity explanation (not supported by the measured activity), "single cycle" evaluation and "lockless" wording.

---

### 3b. Digital comparison (reserve material, not the main narrative; scratch scripts, not in the repo)
Same gate-level netlists, each vector fully settled. Digital 0.31 is driven directly through its engine (a small Java program against `Digital.jar`: load, two untimed warm-up passes, then 5 timed repeats of "set all inputs, `model.doStep()`" with no parsing or comparison; an untimed pass checks every output bit, 0 mismatching vectors). Buffers are merged into wires for Digital and still evaluated by Darion (favours Digital by up to about 13% of the work). Darion is timed as a per-vector API call (`batch_toggle` of one vector) pinned to one core; its first 5,000 vectors were bit-checked, 0 mismatches.

| Circuit | Digital us/vec | Darion `rx-prop` us/vec | ratio | Darion `rx-sweep` us/vec | ratio |
|---|---:|---:|---:|---:|---:|
| c880 | 9.32 | 2.07 | 4.5x | 2.62 | 3.6x |
| c3540 | 57.0 | 8.15 | 7.0x | 7.21 | 7.9x |
| c6288 | 719 | 95.1 | 7.6x | 8.93 | 80x |
| c7552 | 151.8 | 22.5 | 6.8x | 17.4 | 8.7x |
| EPFL adder | 39.6 | 9.49 | 4.2x | 8.99 | 4.4x |
| EPFL bar | 108.0 | 14.45 | 7.5x | 17.7 | 6.1x |
| EPFL arbiter | 415 (351 on 4 cores) | 38.4 | 10.8x | 37.2 | 11.2x |

Darion through its API is 4.2 to 10.8x faster than Digital's engine in propagate mode on these seven combinational circuits (3.6 to 11x in sweep mode, 80x on the c6288 multiplier, where nearly every gate switches every vector). An earlier version that timed Digital's command-line test runner (parsing and comparison inside the run) gave 5.9 to 9.3x and is superseded; the arbiter moved the other way between the two (unexplained).

Sequential circuits use the same method with Darion's own JSON, flip-flop ICs expanded into the same NAND/NOT gates, and the benchmark's physical sequence (50 reset steps, 20 warm-up and 2,500 logical vectors, two clock phases each):

| Circuit | Digital us/step | Darion `rx-prop` us/step | ratio | Darion `rx-sweep` us/step | ratio | Verification |
|---|---:|---:|---:|---:|---:|---|
| ISCAS89 s5378 (179 flops) | 42.3 | 6.70 | 6.3x | 7.90 | 5.4x | 0 mismatching steps in both |
| ITC99 b15 (449 flops) | 126.7 | 14.30 | 8.9x | 16.11 | 7.9x | 0 mismatching steps in both |

**tv80 does not run correctly in Digital, so its speed is not reported.** With an error observer attached to Digital's `Model`, the first step raises `NodeException: Logic seems to oscillate.` (Digital's own limiter, 1,000 micro-steps plus 100 collection steps); `errorOccurred` then closes the model without throwing, all later `doStep()` calls do nothing and the outputs stay frozen. In noise mode (random update order) there is no error and the CPU runs, but the result is nondeterministic and does not match Darion exactly.

Caveats: Digital on JVM defaults, one core (four cores are 5 to 20% faster); two sequential circuits only; Darion's per-step figure includes the Python call around `batch_toggle`.

### 3d+. The V+1 / 2V budget: what it is and how to present it (claims doc, Claim 3a+)
- **Idea:** the oscillation cutoff is the live size of the circuit (gates minus deleted ones), recomputed at every propagation and maintained in O(1) under editing. It is not a constant a user must tune. Every other tool checked uses a fixed constant (1,000 to 10 million) and most stop with an error.
- **Why V+1 is right, in one line:** a change in wave k has a chain of k gates behind it, each causing the next; without a loop that chain can't repeat a gate, so it is at most V long. Hence (a) V+1 never fires on acyclic logic, and (b) if it fires, a real loop was traversed (pigeonhole).
- **Evidence:** 0 false alarms on 30 acyclic circuits (13 to 101,859 gates). The budget actually needed was always ≤ depth. A real ring on b19 (356k gates) is caught in 0.92 ms and the rest of the circuit stays exact.
- **Alternative bound considered:** "V is loose; depth is tighter (up to 1,687x)." Depth depth must be recomputed after every edit and is undefined on cyclic graphs; V costs O(1). Its looseness costs V times the oscillating frontier, not V times the circuit: under 1 ms on the largest circuit.
- **Where 2V comes from (author's model, refined by measurement):** the intuition is that a wave runs to the end of a chain, the loop returns it to the start, and it needs another pass. For a *single* loop the second pass never happens. The returning change either finds the entry gate consistent (even inversions: settled within t + L + 1 ≤ V + 1 waves) or flips it forever (odd: an oscillator). Measured on 2,000 single-loop networks, the worst case is exactly t + L + 1. The extra pass is real for *interacting* loops, where a change leaves one loop and re-triggers another, up to 1.84V measured. So: "V + 1 suffices for acyclic logic (proof) and for any single feedback loop (argument + data); 2V is an empirical default for interacting loops." It is exceeded by XOR-heavy interacting loops: 2.19V measured on random XOR networks, and up to about 9V reported by the author. Present 2V as a calculated default whose failure is safe (promotion to timed simulation, adjustable with `set_wave_limit`), never as a bound.
- **What not to claim:** that bounding settling by depth is new (that is levelization), or that 2V is proven. 2V is a measured heuristic (16,129 converging random networks, worst 1.84V) for feedback that settles.
- **Summary statement:** "Darion bounds zero-delay propagation by the live size of the netlist. The bound is maintained in constant time as the circuit is edited, never fires on acyclic logic, and when it fires it certifies that a feedback loop was traversed; the remaining activity is then simulated with gate delays instead of being reported as an error."

### 3e. Oscillation: fatal in Digital, non-fatal in Darion (claims doc, Claim 3d)
Two small circuits, each with c17 beside a feedback structure. The same `.v` was exported to Digital and to Darion JSON, with the same vectors.
- **Ring oscillator enabled at step 10:** Digital stops with "Logic seems to oscillate" and closes the model. Its c17 outputs then freeze, giving 26 wrong bits out of 90. In Darion the ring runs in the timed queue and c17 stays correct (0 wrong out of 90).
- **NAND latch held from power-up:** Digital fails at step 0, as its own documentation predicts ("a RS-FF typically does not start"). Darion settles the latch and then operates it correctly (0 wrong out of 115).

Digital's choice is deliberate and documented, and it has a noise mode; this is a design difference, not a defect.

## 4. The ablation: method and results

**Question:** "The OOP baseline is the author's own code. How is it known the 2x is caused by what you say and is not a weak baseline?"

**Answer:** a standalone C++ harness (`tests/ablation_layout.cpp`) re-implements the same propagate loop with the gate representation as the *only* variable, and it reproduces the engine-level gap on the real exported netlists.

Variants (each differs from the previous in one thing):

| Step | What changes | What it isolates |
|---|---|---|
| a to b | heap objects to the same objects packed in an arena | allocation / layout only |
| b to g | 40 B virtual objects to 40 B flat struct with the branch-free rule | virtual call + rule, equal size |
| g to d | 40 B to 24 B | struct size only |
| b to c | virtual to `switch` (also 40 B to 24 B) | indirect-call flavour (confounded with size; say so) |
| c to d | `switch` to the unified rule, same struct | evaluation rule only |
| d to e | 24 B to 32 B | struct size / line alignment |

Safeguards that make it credible: identical work (evaluation counts, changed counts, final-state fingerprint identical in all 91 configurations), variants interleaved with rotated order every repeat, one pinned core, 9 repeats, PMU read in-process, results are medians with spread, paired ratios.

**Findings, in the order to present them:**
1. *Dispatch and the evaluation rule dominate.* A virtual call costs ~2x per edge even when nothing is mispredicted (NOT chain: 4.9 vs 2.6 ns), because it cannot be inlined or overlapped. On mixed gate kinds it also mispredicts and the gap reaches 2–3.3x on synthetic circuits; on the real ITC99 netlists a/d is 1.7–1.9x (cycles per edge 22.6 vs 12.5 on b15), matching the 1.9–2.1x of the full Cython engines.
2. *`switch` is not a fix.* It is an indirect branch too: a to c is only 1.2–1.3x; the remaining c to d gain is 1.35–1.5x on real circuits.
3. *Layout is secondary unless placement is scattered and the working set is large.* On real circuits a to b is 1.01–1.09x; with shuffled and fragmented placement it rises to 1.2–1.4x (b18/b19) and on 1M-gate synthetic chains to 1.8–2.0x. Real engines allocate Python-driven and fragmented, so the scattered case is closer to `reactor_oop`'s reality than the tidy one.
4. *Struct size is a cliff at the L3 boundary, not a slope.* On 1M-gate synthetic chains with scattered placement, an idle machine gives 12.9 ns (24 B), 26.8 ns (32 B) and 43.4 ns (40 B) (re-measured 2026-10-22, matching the earlier single calls); with desktop activity, medians over 7 processes rose to 19.7, 40.2 and 53.6 ns. Quote the idle numbers with the ratios (32 B about 2.1x, 40 B about 3.4x the 24 B time) and say that absolute times at this size depend on machine activity; 24 MB fits the 32 MB L3, 32 and 40 MB do not. On real circuits at 24k–356k gates the penalty is only 3–15%. So 24 vs 32 B is a large-netlist concern.
5. *Predictor memorization is real.* Repeating the same input lets the predictor learn the virtual-target sequence up to a few thousand gates (0.00 misses per edge at 1k gates, 0.88 from 10k); when the evaluated sequence varies per iteration the onset drops to between 100 and 1k gates. This means micro-benchmarks with repeated inputs understate the OOP cost.

**Generality:** the same experiment on ISCAS85, EPFL and OpenCores (24 circuits in all) gives an OOP/data-oriented ratio of 1.5–3.2x in the full engines (median 2.0x; 3.4x on cavlc in the earlier run) and 1.3–2.5x in the harness (median 1.8x). The smallest gains are on circuits whose gate mix is uniform or rarely mispredicts (c6288 1.46x, vga_lcd 1.3x); the largest on mixed-type logic (ISCAS85 control logic, DES, AES). The harness underestimates the engine ratio (r=0.89, bias ~0.25): the rest is unexplained overhead in the Cython OOP loop, so present the harness as the attribution of the effect, not as its measurement. The measurement itself is the full-engine comparison already in `Benchmark/master_test.md*.md` (`rx-prop` vs `rx-oop`, wall-clock and PMU, all suites); the harness gap does not affect that headline.

**Limitations to state yourself (cheaper than being found out):** the harness is not the Cython engines (no wave limit, no Python layer, no visual queue; `reactor_oop`'s IC input/output pin classes are merged into BUF); one CPU (Zen 5, large L3 and strong predictor); ITC99, ISCAS85, EPFL and OpenCores only (no ISCAS89, EPFL large/mammoth or Faraday); random-input stimulus; branch/target-history depth was not probed directly, so the memorization explanation is a supported hypothesis.

---

## 5. Method questions and answers

1. **"Isn't this just data-oriented design, which is well known?"** The idea is known. The work provides a controlled, attributed measurement in gate-level simulation, a correctness argument and a design that keeps interactivity; it does not introduce a new algorithm.
2. **"Why not compare with commercial simulators or ESSENT/GSIM?"** Out of scope by design (Darion is an interactive API/UI, single-threaded); Verilator and Icarus serve as correctness oracles and reference points.
3. **"How does Darion's throughput compare with Verilator on large designs?"** Verilator is faster on all 88 circuits. An earlier measurement showed Darion ahead on b17, b18, b19 and vga_lcd, but that Verilator model was wrong: Verilator 5.052 lowers the cell library's sequential UDPs to blocking assignments, which is order-dependent (wrong flop states on 16 circuits) and slow. With a correct flop model Verilator is faster on all 88 circuits. Darion's case is interactivity, millisecond load, full observability and correctness at a fixed speed cost, not raw throughput; on the sequential suites that cost includes simulating every flop as 10 gates.
4. **"Is the 4-state/2-state difference a problem?"** Verified bits where Icarus has X are skipped and the fraction is reported; Verilator is 2-state. Darion's X handling is optimistic (a partially-X gate may resolve), a documented limit.
5. **"Is the UI really free?"** The engine side is: 0.995–1.004x with the queue active, drain 0.2–0.7 ms for 8–18k queued gates, API call 0.25–0.34 us. Rendering was not measured; if the GUI is slow, that is where.
6. **"Does the delay model match silicon?"** It is not calibrated to silicon. It is exact for a documented linear load-dependent model, validated against an independent reference simulator and Icarus gate primitives with the same delays; not calibrated to a library, no rise/fall, pin-arc or slew dependence. Known defect B8 (phantom flip re-stamping gate clocks) is reported openly.
7. **"Why is the OOP baseline fair?"** Same algorithm, same traversal, same edge structure; the harness variants show it step by step, and the harness reproduces the ranking of the full-engine ratio across 24 circuits (r = 0.89, about 0.25 lower in magnitude).
8. **"Single-threaded?"** Yes, by design; the core is cooperative (asyncio), so lock-free wording does not apply.
9. **"Statistics?"** State medians, ranges, repeat counts, pinning, and that spreads on large synthetic configurations reach 5–20%.

---

## 6. Reproduction cheat sheet (all pinned: `taskset -c 2`; nothing else running)

| What | Command |
|---|---|
| Build engine | `bash scripts/build.sh` (OOP: `--reactor-oop`) |
| Integrity + retype tests | `PYTHONPATH=editor/tools .venv/bin/python tests/integrity_test.py` |
| Timing suites | `.venv/bin/python tests/test_timing.py --suite topologies\|extended\|bench` |
| State verification vs Icarus/Verilator | `.venv/bin/python tests/verify_state.py b15`; other suites: `--suite opencores` (or `faraday`), `--no-verilator` for vga_lcd; real workload: `--workload tv80 --cycles 5000` |
| Output verification, combinational suites | `tests/src/verifier.py tests/ISCAS85 --vectors 20000 --no-engine` (EPFL: use `tests/EPFL_parsed`, `tests/EPFL_large_parsed`, `tests/EPFL_mammoth_parsed`, not the raw `tests/EPFL*` folders); ISCAS89: `tests/src/verifier_89.py tests/ISCAS89` |
| ITC99 PMU, prop vs oop | `PYTHONPATH=editor/tools .venv/bin/python tests/src/perf.py itc99 --filter b15.v --no-engine --no-rx-sweep --no-icarus --no-verilator` (repeat; `perf.py` does not average) |
| Ablation, synthetic | `g++ -O3 -march=native -std=c++20 -o abl tests/ablation_layout.cpp`; `taskset -c 2 ./abl --topology random --n 100000 --reps 9 --variants abcdge [--shuffle --frag 192]` |
| Ablation, real netlists | `PYTHONPATH=editor/tools .venv/bin/python tests/ablation_eval.py --export reactor b15 b15.net [raw]`; `taskset -c 2 ./abl --netlist b15.net --reps 9 --variants abcdge` |
| SIMA vs `switch` in the real engine | build a copy of `reactor/` with `-DDARION_EVAL_SWITCH`; `tests/ablation_eval.py <dir> <label> b14 b15 b17` |
| UI cost / API latency | `tests/ablation_eval.py --ui-cost reactor b15 prop`; `tests/ablation_eval.py --latency reactor b15` |

Machine for every number: AMD Ryzen 7 9700X (Zen 5), 8 cores, 32 MB L3, Linux, `perf` user-mode counters. Reference simulators used: Verilator 5.052 (2026-09-05), Icarus Verilog 13.0 (stable).

### 6b. Second-machine run sheet (open item 2)

Goal: show that the OOP-versus-data-oriented result is not specific to Zen 5. Best: an older x86 with a smaller L3 (Intel 8th-12th gen or Zen 2/3), or an ARM Linux machine. Icarus and Verilator are not needed. Nothing else should run during the measurements; close browsers and IDEs.

1. **Record the machine** (keep this output):
   ```bash
   lscpu; lscpu -C; uname -r; g++ --version | head -1; python3 --version
   cat /proc/sys/kernel/perf_event_paranoid      # must be 2 or lower for user-mode counters
   ```
   If it prints 3 or 4: `sudo sysctl kernel.perf_event_paranoid=2` (resets on reboot).
2. **Build** (from the repo root, with the project's venv set up as on the main machine):
   ```bash
   bash scripts/build.sh && bash scripts/build.sh --reactor-oop
   PYTHONPATH=editor/tools .venv/bin/python tests/integrity_test.py      # must pass before measuring anything
   ```
3. **Full-engine counters, the headline** (`perf.py` pins to core 2 itself and runs each engine once per call, so loop). Nine repeats, circuits interleaved:
   ```bash
   for r in 1 2 3 4 5 6 7 8 9; do for c in b15 b17 b18 b19; do
     PYTHONPATH=editor/tools .venv/bin/python tests/src/perf.py itc99 --filter $c.v --no-engine --no-rx-sweep --no-icarus --no-verilator \
       | grep -E "^\| [^|]+ \| rx-prop |^\|  \| rx-oop" | sed "s/^/$r $c /"
   done; done | tee pmu_second_machine.log
   ```
   On an SMT machine, check `cat /sys/devices/system/cpu/cpu2/topology/thread_siblings_list`: a busy sibling changed cycles by 16-40% on the laptop, so offline it or occupy it (root needed to offline). Even with it offline, `rx-prop` cycles were bimodal between processes on b15, b17 and b18 (about +35% on b17 at identical instruction counts), so take at least 9 repeats and report the median together with the fast-mode value. Check that the log has 72 lines (9 repeats x 4 circuits x 2 engines); the OOP row starts with `|  |`, so a narrower grep drops it.
4. **Ablation harness on the real netlists** (export once, then 9 interleaved repeats per netlist):
   ```bash
   g++ -O3 -march=native -std=c++20 -o abl tests/ablation_layout.cpp        # ARM: if -march=native fails, use -mcpu=native
   mkdir -p abl_nets
   for c in b14 b15 b17 b18 b19; do PYTHONPATH=editor/tools .venv/bin/python tests/ablation_eval.py --export reactor $c abl_nets/$c.net; done
   for c in b14 b15 b17 b18 b19; do taskset -c 2 ./abl --netlist abl_nets/$c.net --reps 9 --variants abcdge; done | tee abl_real.log
   ```
5. **Synthetic sweep** (layout and size cliff; L3 size matters here):
   ```bash
   for t in chain tree random mixchain; do for n in 1000 10000 100000 1000000; do
     taskset -c 2 ./abl --topology $t --n $n --reps 9 --variants abcdge
     taskset -c 2 ./abl --topology $t --n $n --reps 9 --variants abcdge --shuffle --frag 192
   done; done | tee abl_synth.log
   taskset -c 2 ./abl --topology mixchain --n 1000 --reps 9 --variants abcd --vary | tee -a abl_synth.log
   ```
6. **Bring back:** the machine record from step 1 and the three logs. They go into Claim 13 as a second-platform table next to the Zen 5 numbers.

What to expect and how to read it: the full-engine ratio (step 3) is the headline. If it stays near 2x the claim generalises. If it is smaller on a CPU with a weaker branch predictor or a smaller L3, report it as measured; the ablation (steps 4 and 5) then shows which part moved (dispatch, rule or layout). The size cliff in step 5 should move to wherever this machine's L3 ends.

### 6c. Bug-localisation case study (open item 6)

`PYTHONPATH=editor/tools .venv/bin/python tests/verify_state.py --case-study [--seed N --cycles 2000]`. tv80 runs the Z80 program; a copy has one injected bug (a 2-input cell swapped, AND2<->OR2 or NAND2<->NOR2). Both workflows must find the first point where the buggy run behaves differently from the golden design and the gate that causes it. Results and their interpretation are in the claims doc (Claim 7, case study).

---

## 7. Open items

00. **Digital's evaluation semantics (checked in the bytecode of `Model.doMicroStep`, Digital 0.31).** Standard gates have no delay attribute (`Keys.DELAY_TIME` is not used by the core gate classes). Each microstep collects the dirty nodes, then calls `readInputs()` on all of them before `writeOutputs()` on any of them, i.e. a lock-step (synchronous) update where one microstep acts as one implicit gate delay; `doStep()` repeats microsteps until nothing is dirty. An optional noise mode (`doStep(true)`) shuffles the dirty nodes and runs read+write node by node. So the comparison is against a zero-delay, lock-step engine: no per-gate timing work is hidden in Digital's number, and Darion's `propagate` is also wave-based (it evaluates a target as soon as a source edge is processed, so it is not strictly lock-step; evaluation counts per vector differ between the two engines). Darion's timed (priority-queue) mode was not compared. **tv80 diagnosis:** in plain mode Digital's tv80 is stuck (6.3 us/step because nothing happens); in noise mode it runs the CPU (92 us/step) and the mismatches against Darion fall from 5,000 steps / 29 outputs to 1,169 steps / 14 outputs, and the cause was then confirmed directly: the oscillation limiter fires at the first vector and Digital closes the model (see 3d). It is a property of Digital's evaluation model for gate-level feedback designs, shown on one circuit.

0. **No quantitative interactive-simulator comparison (decided).** A fair one needs the same gate-level netlist converted gate-for-gate into each tool's format (no LUTs or macros), verified output-equivalent, with Java and the jars; it was judged not necessary for the pitch, which rests on Darion's own measured properties. Replace it with a qualitative capability table (programmatic API, live per-gate state, headless mode, load time) whose every cell is verified from each tool's current documentation; do not write "cannot run headless" for Digital or Logisim (both have headless modes).
   *Profiling evidence collected (JFR sampling, headless, Temurin 21; one circuit each, not a benchmark):* Digital 0.31 `CLI test` on ISCAS85 c7552, 150,000 vectors: 1,431 samples, 91% of top frames in `de.neemann.digital.core`, no Swing/AWT/GUI frame in any stack, 0.2% with drawing-model frames (model construction). Logisim-evolution 5.0.0 `--tty table` on c432 with 16 free inputs (65,536 rows, 19.7 s): 948 samples, no Swing/AWT frames; top frames are `HashMap.getNode` (45%) and `com.cburch.logisim.circuit` (26%), i.e. its own simulator data structures; the 12% flagged as `gui` are `TtyInterface` (the headless driver). So in these headless modes neither tool showed UI-update cost; Logisim's overhead here is its engine design, not repaint. This does NOT cover their interactive (GUI) modes, other versions, or sequential circuits, and no timing comparison with Darion was run.

1. **Citations audited on 2026-10-21** (details in `Related_Works.md` section 0): metadata checked against Crossref; 7 wrong DOIs, one fabricated-looking combined entry (Agrawal and Dally) and one non-existent Verilator paper were corrected or replaced; claims about Verilator, Logisim and Digital checked against their documentation and source; new prior art added (Maurer patents and ICCAD 2000, Driesen and Hölzle, PyRTL, DigitalJS). **Complete reference status, with what to read, what to cite for what, and what to drop: `Related_Works.md` section 0.3b.** Maurer's two patents and his ICCAD 2000 paper were read in full on 2026-10-21 (comparison in the audit, section 0.5). The 2000 paper motivates its design from virtual-function dispatch replacing type codes, which is the trade-off Claim 13 measures in the opposite direction on a modern CPU: use that in the related-work and evaluation sections, carefully worded (audit 0.5). Cite his 1994 Inversion paper (ICCAD, DOI 10.1109/ICCAD.1994.629776, read in full) as the primary source for counting with deferred inversion, and Schuler 1972 (COMPCON 72, as cited by Maurer) as the origin of counting. Use the 1994 paper's branching pseudocode as the "before" next to SIMA in the design figure. *Reading status updated 2026-10-22:* Maurer 1994 and 1996, Wang and Maurer (LECSIM, tech-report version), Shiple et al. 2002, Edwards 2003, Chilimbi et al. (both PLDI 1999 papers), Driesen and Hölzle 1996, Ulrich 1969 and Fleurkens 1996 are read and their quoted facts re-checked against the PDFs in `~/Github/darion_research_papers` (audit 0.3b). Maurer 1996 turns out to be prior art for the turnaround argument (Claim 8), not for the code-footprint explanation (Claim 9). Still unread: Abramovici's treatment of XOR, Agrawal and Dally, Maurer 1993 (Shadow), Malik 1994 (known through Shiple et al. and Edwards), Riedel and Bruck, EPICS (paywalled), Driesen and Hölzle ISCA 1998, Burch 2002, DigitalJS; VCS and Xcelium defaults remain unverified.
2. ~~Run the ablation harness on a second CPU~~ **Done for one older x86 (Ryzen 5 PRO 5675U, Zen 3, 16 MB L3; claims doc Claim 13, second platform, logs in `Benchmark/5675U.md`).** Still open: an ARM machine and an Intel machine. On any SMT machine, offline or occupy core 2's sibling (a busy sibling raised cycles 16-40% on the laptop) and expect per-process bimodality in `rx-prop` cycles even then. Original text: Run the ablation harness on a second CPU (ideally one ARM, one older x86 with a smaller L3 and weaker predictor); extend to ISCAS89 and EPFL large; optionally explain the gap between the harness and engine ratios (not needed for the headline, which is the full-engine master-test data).
3. Probe the predictor memorization claim directly (history depth) or keep it as a stated hypothesis.
4. tv80: the Verilator testbench disagrees with Icarus (Darion matches Icarus); root cause not investigated, so the Verilator speed comparison on the workload was dropped. Possibly the Verilator UDP flip-flop quirk listed in the claims doc.
5. ~~Measure rendering and real-UI drain cadence, or scope the measurements to engine and API cost explicitly.~~ **Scoped (2026-10-21):** engine and API only; see "Scope of the measurements" in section 1.
6. ~~A user-facing case study.~~ **Done (2026-10-21):** tv80 running a program with an injected bug, located through the API in 140-190 ms versus about 27 s for a compile, dump and analyse flow with Icarus, with the same answer on 5 of 5 seeds (claims doc, Claim 7; command in 6c). It uses only loading, replaying an input sequence through the API, reading gate states and the changed-gate queue. Retyping is not used: the bug is in the circuit file.
7. Delay calibration to a cell library (OpenSTA/SDF) if you want any timing-accuracy claim beyond "exact for its model".
8. Multithreaded Verilator and a non-default Verilator configuration were not tried.

---

## 8. Index of results

| Topic | Where |
|---|---|
| Gate record, SIMA, evaluation rule | Claims 1 and 4; section 2.2 |
| Schedules (propagate, bounded sweep) | Claim 5; section 2.1 |
| Oscillation budget and timed handoff | Claims 3a-3d; sections 3d+ and 3e |
| Correctness against Icarus and Verilator | `Claims.md` section 4; evidence row A |
| Data-oriented versus OOP engines | Claim 13; sections 2.3 and 4 |
| Turnaround and memory | Claim 8; evidence row F |
| Throughput relative to Verilator | Claim 9; evidence row G |
| Observation cost (visual queue, API latency) | Claim 7; evidence row E |
| Delay model | `Timing_Report.md`; evidence row H |
| Macros and native flops | Claim 12; `Design_Notes.md` |
| Digital comparisons | sections 3b-3e |
| Scope and limits | sections 1 and 1b |
