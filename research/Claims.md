# Research Claims and Empirical Achievements
**Project:** Darion Logic Sim (`darion-logic-sim`)  
**Target Venue:** undecided (exploratory research)  
**Hardware Profiling Platform:** AMD Ryzen 7 9700X 8-Core Processor (Zen 5) | Linux PMU Kernel Subsystem (`perf`)  
**Status of this document:** audited against the code and re-measured (2026-10-20). Each claim carries a status: **HOLDS**, **HOLDS WITH CAVEATS**, **REFUTED / REWRITTEN**, or **UNPROVEN**. The timing/delay engine is documented separately in `Timing_Report.md`.

---

## Summary

| Claim | Status |
|---|---|
| 1. Uniform gate representation (SIMA): one 24-byte struct, one evaluation rule | HOLDS (correct; not novel in itself) |
| 2. Runtime gate-type mutation as a 3-byte write | **REFUTED**; reduced to a side effect of Claim 1 (bug fixed, tested) |
| 3a. Oscillation budget, DAG tier (\|V\|+1) | HOLDS (sound, but loose) |
| 3b. Oscillation budget, sequential tier (2\|V\|) | UNPROVEN heuristic |
| 3c. Non-fatal promotion of cycling cones to the timed queue | HOLDS WITH CAVEATS |
| 4. 24-byte POD layout | HOLDS (size); field-order claim is **vacuous** |
| 13. Data-oriented engine removes the OOP object-graph overhead (branch and cache optimization) | **HOLDS WITH CAVEATS**: about 2× faster than the OOP engine on ITC99; the OOP cost is vtable dispatch plus heap-object pointer chasing; branch and cache parts are not separately isolated against the OOP engine |
| 5. Bounded topological sweep with back-edge escape | HOLDS |
| 6. Inertial glitch absorption | HOLDS (see timing report) |
| 7. Decoupled visual interface | Engineering, not a research claim |
| 8. Turnaround vs. Verilator | HOLDS WITH CAVEATS |
| 9. Faster than Verilator on large netlists | Numbers HOLD; the **activity explanation is REFUTED**, the real driver is design size |
| 10. 1,756× vs. Icarus | HOLDS but **misleading** |
| 11. IPC of 4.03–4.48 | **REFUTED** on real circuits |
| 12. Native flop evaluation (flop-cut experiment, not a Darion feature) | **HOLDS** as an experiment (bit-exact on 8 ITC99 circuits); evidence for a future macro/native-element direction |
| Verification: 0 mismatches | HOLDS (extended; see section 4) |

---

## 1. Algorithmic Claims

### Claim 1: Uniform gate representation (Single-Invariant Masked Accumulator, SIMA)
* **Statement:** All eight gate types live in one flat array of identical 24-byte structs and are evaluated by one rule, parameterized by `(seed, mask, invert)`:
  `output = bool(logic & mask) ^ (flags & 1)`
  `logic` is an incrementally maintained count of inputs equal to `seed`. `mask = 0xFF` gives an existential test (AND/NAND/OR/NOR/BUF/NOT). `mask = 0x01` gives parity (XOR/XNOR).
* **Verified:** exhaustive fan-in sweeps (2–513) for every n-ary type, and 6 × 150 random circuits in propagate and sweep modes (with and without topological optimization) against an independent fixed-point oracle: **0 mismatches in about 800k gate reads**.
* **Limits:** `logic` and the port count are uint8. Fan-in of 256 or more used to give wrong results for AND/NAND/OR/NOR (XOR survived because the wrap preserves the parity bit). This is now guarded in the engine: `Gate.setlimits` returns False above 255 and the JSON loader raises `ValueError`; test H1 asserts it. 3-state (`X`) semantics are optimistic: a partially-`X` gate can resolve to a definite value.
* **Honest novelty assessment:** this is classical input counting (Abramovici et al. 1990, Szygenda & Thompson 1975) with parity read from the low bit of the ones-count. It is also close to prior art found in the 2026-10-21 audit: Maurer's patents US 5,856,933 (1999) and US 6,131,081 (2000) count dominant-valued inputs per gate, defer output inversion and handle XOR/XNOR/NOT/BUFFER by input-change events for the same eight gate types, and Maurer's ICCAD 2000 paper removes state-testing code from event-driven gate simulation (see `Related_Works.md` section 0). SIMA is an arithmetic variant of that family, not a new idea. It is clean engineering, not a new algorithm. The "single CPU cycle" wording is unsupported: `evaluate()` also carries an `inputlimit` branch, and the cost is dominated by memory access.
* **Ablation (measured):** the only earlier comparison (`rx-oop`) also changed dispatch, layout and graph representation, so I isolated the evaluation rule. Same source, same flags, same 24-byte layout, same accumulators; the only change is `evaluate()` becoming a `switch(type)` (`-DDARION_EVAL_SWITCH`, `tests/ablation_eval.py`). Both variants perform identical work (identical evaluation counts and final-state fingerprints). Best of 3, benchmark stimulus:

  | Circuit | rx-prop: switch / SIMA | rx-sweep: switch / SIMA |
  |---|---:|---:|
  | b14 | 285.1 / 169.0 ms = **1.69×** | 178.9 / 121.0 ms = **1.48×** |
  | b15 | 113.8 / 79.7 ms = **1.43×** | 116.9 / 95.5 ms = **1.22×** |
  | b17 | 368.4 / 267.1 ms = **1.38×** | 353.9 / 299.8 ms = **1.18×** |
  | b19 | 1051.7 / 749.8 ms = **1.40×** | 885.0 / 802.2 ms = **1.10×** |

  Mechanism: the switch costs more branch mispredictions (b15 whole run: 12.5M versus 8.0M, +57%; cycles +13%). So the unified rule is worth roughly 10–70% on the evaluation step, a real but modest engineering gain. The switch is the natural alternative, not the only one (for example a per-type lookup table), so state it as "versus a type switch". With the switch evaluator Darion still beats Verilator on b19 (1.05 s versus 1.79 s) and still loses on b14, so the Claim 9 conclusion does not depend on SIMA.
* **Code:** `reactor/Profile.h` (`CPP_Gate::evaluate`, `compute`), `reactor/Store.pyx` (per-type seed/mask/flags).

### Claim 2: Runtime gate-type mutation (REFUTED, rewritten)
* **Previous claim:** any gate can be morphed into any other with a 3-byte write.
* **Finding:** no such code existed. The only type-change path, `Circuit.transfer_info` (called by the `TransferInfo` command; only the CLI test tool uses it, the GUI does not), changed `type` and `id` but **not** `seed`, `mask` or `flags`. Tested on all 30 n-ary source→target pairs and on BUF↔NOT: **the gate kept its old logic in every case**. The existing integrity test checked only the id and object list, never behavior.
* **Fixed:** `Gate.retype` (`reactor/Gates.pyx`) now rewrites type, seed, mask, invert flag, slot count, the `logic` counter and the `seed`/`logic`/`index` cached in the sources' hitlist entries; `Circuit.transfer_info` calls it. `test_retype_exhaustive` in `tests/integrity_test.py` (moved there from a standalone script) covers 1,980 cases (every type pair, partial wiring, pins in non-zero slots, downstream consumer, toggling afterwards, propagate and sweep) against an independent oracle. It fails on the pre-fix build and passes on the fixed one.
* **Why a "3-byte write" is wrong even in principle:** within a seed family (AND/NAND/NOT use seed 0; OR/NOR/XOR/XNOR/BUF use seed 1) a change is O(1): only `mask` and the invert bit change. Across families the `logic` counter must be recomputed and every incoming `Profile.seed`/`Profile.logic` rewritten. Those profiles live in the sources' hitlists, so the cost is O(fan-in).
* **What remains:** mutation is not a headline feature. It is a side effect of Claim 1's uniform representation.

### Claim 3: Oscillation handling
* **3a. DAG tier (\|V\|+1): HOLDS.** In a DAG, a zero-delay wavefront cannot survive past the longest path, which is at most \|V\|. Measured: a NOT chain of n gates needs exactly \|V\| waves (minimal budget found by search for n = 10, 100 and 1000), and chains up to 5,000 gates give no false positive. *Caveat:* the real bound is the circuit's depth, and \|V\|+1 is tight only for a single chain. On realistic circuits, detection of a true cycle waits roughly \|V\| waves.
* **3a+. The live-size budget: formal statement and measurements (2026-10-21).**
  - *Mechanism* (`propagate`, `Circuit.pyx`): budget W = (live gates) × m + o, with live = array entries minus deleted ones (`hidden`). It is recomputed at every propagation call and maintained in O(1) under editing: `delobj`/`renewobj` adjust `hidden`. One unit is spent per non-empty wave. When W is exhausted, the remaining frontier goes to the timed queue with load-dependent delays, and simulation continues. Combinational mode: m=1, o=1. Sequential mode (default): m=2, o=0.
  - *Theorem (soundness on acyclic logic).* A gate processed in wave k is the end of a causal chain of k distinct gates. In an acyclic graph, k ≤ depth (levels) ≤ V, so any W ≥ V never promotes; V+1 adds one wave of slack.
  - *Corollary (certificate).* Reaching wave V+1 implies a causal chain longer than V, which repeats a gate (pigeonhole). A feedback loop was actually traversed, so a promotion under V+1 never comes from acyclic logic.
  - *Not implied:* that the loop oscillates forever. Converging feedback (latches) can need more than V waves: the 3b search found settles of up to 0.92 × 2V = 1.84V. Hence 2V in sequential mode. No linear bound can be guaranteed in general, since a cyclic network's state space is 2^V.
  - *Measured soundness and looseness* (scratch probe, binary search for the smallest constant budget with no promotion over 300 random vectors, 60 for EPFL large; `set_wave_limit(0, K)`). 30 acyclic circuits: ISCAS85 (11), EPFL (11) and EPFL large (8), 13 to 101,859 gates.
    - **V+1 never promoted.**
    - The budget needed was always ≤ the structural depth, as the theorem requires. Examples: c432 19/19, c6288 109/126, div 434/8,686, sqrt 1,242/9,033.
    - V exceeds the budget needed by 2.6x (c17) to 1,687x (arbiter), with a median of about 40x.
  - *Cost of that looseness when a real oscillation occurs* (scratch, a NAND + 2 NOT ring with an enable input appended to the circuit's JSON, 5 repeats, pinned core):
    - Detection takes exactly V edge evaluations under V+1 (2V under 2V), because each wave carries only the ring's frontier: b15 (V = 24,333) 0.07 ms, b19 (V = 356,403) 0.92 ms (2V: 0.13 and 1.84 ms).
    - Over 19 later vectors, the outputs match the same circuit without the ring exactly (0 mismatches).
    - The b15/b19 latches settled under V+1 with no promotion.
  - *Why V and not depth:* depth would be up to three orders of magnitude tighter. But it needs a levelization of the current graph, changes with every edit, and is undefined on cyclic graphs. V is maintained in O(1) and costs at most about 1 ms on the largest circuit tested.
* **3a++. Single feedback loops need no second pass (2026-10-21).**
  - *Argument:* side inputs are fixed during one propagation. Take a loop of L gates entered by a change through a tail of t gates. A loop gate whose side input is at its controlling value blocks the change, so it dies within t + L waves. If no gate blocks it, the change returns to its entry gate after L waves. With an even inversion count the entry gate is consistent and nothing changes, so the loop has settled. With an odd count it flips on every return and never settles. So a single loop either settles within t + L + 1 ≤ V + 1 waves or oscillates forever.
  - *Measured* (scratch `loop_probe.py`, 2,000 random tail+loop networks, AND/NAND/OR/NOR/XOR loop gates with side inputs, 8 vectors each starting from all-unknown): 1,314 settled, 686 oscillated. Worst budget needed = 1.00 × (t + L + 1), the bound exactly and never above it; at most 0.75 V.
  - *Interacting loops* (2,000 networks of 2-4 loops cross-coupled through side inputs): 611 settled, 1,389 oscillated, worst 0.88 V. The earlier search (3b) found up to 1.84 V. Settling beyond V comes from changes that leave one loop, pass through another and re-trigger the first, not from a second pass around one loop.
  - *XOR interacting loops exceed 2V:* 2,000 networks of 2-4 cross-coupled loops with only XOR/XNOR gates, which never block a change: 33 settled, 1,967 oscillated, and the worst settling case needed 2.19 V. The author reports cases of up to about 9 V with more complex XOR loops (not reproduced here). **2V is therefore not a bound; it is a calculated guess** (author's description) that covers every non-XOR case measured.
  - *Why a guess is acceptable here:* exceeding the budget is not fatal. The remaining activity is promoted to the timed queue and continues with gate delays. A network that would have settled after 2.19 V is therefore simulated in timed mode from that point, rather than stopped or reported as an error.
  - *Literature context (Shiple, Brayton, Berry and Sangiovanni-Vincentelli 2002, read).* Linear step bounds are known for monotone ternary analysis: ternary simulation converges in at most m steps, and Malik's algorithm within k rounds for k feedback vertices. For binary settling, the known general bound (Brzozowski and Seger) is exponential, (2^m − 2)·D. So a linear 2V cannot be a general guarantee, consistent with the XOR result below. Cite these next to V+1/2V.
  - *Consequence:* V+1 is sufficient for acyclic logic (proven, 3a+) and for any single loop (argument above, matched exactly by the data). 2V is a default margin for interacting loops: empirical, exceeded by XOR-heavy feedback, and not provable in general (a network of V gates has 2^V states). The multiplier can be raised with `set_wave_limit`.
* **3b. Sequential tier (2\|V\|): UNPROVEN.** It is a heuristic with no proof. I searched 16,129 converging random cyclic networks (4–12 gates) for one needing more than 2\|V\| waves and found none (worst case 0.92×). So it holds in practice, but "mathematically rigorous" does not apply to this tier. A false trigger is not fatal, because the cone is promoted, but it changes semantics from zero-delay to timed.
* **3c. Non-fatal promotion: HOLDS WITH CAVEATS.** With a running asyncio loop, a ring oscillator (NAND + 2 NOT) is promoted and runs (the clock advances). *Caveat:* without a running event loop (scripts, benchmarks, tests) the promoted tasks stay in `time_queue` and `runner` stays `None` until someone calls `drain_timed_queue()` or a later `propagate` starts the runner.
* **3d. Non-fatal versus fatal handling, measured against Digital 0.31 (2026-10-21).** Two small gate-level circuits, each with ISCAS85 c17 alongside as ordinary logic. Both were exported gate for gate to Digital with `scripts/iscas_parser.py --export dig` and to Darion JSON from the same `.v`, with the same 40 input vectors and expected c17 outputs computed independently in Python. Scratch scripts are in the session scratchpad, not the repo.
  - (1) **Ring:** a NAND + 2 NOT ring oscillator, enabled at step 10. Digital raises "Logic seems to oscillate" at step 10 and closes the model. Every later step returns frozen outputs: 26 of 90 checked bits wrong, all after step 10. Darion promotes the ring to the timed queue; c17 stays correct on all 40 steps (0 of 90 wrong). The ring's output toggles in the timed queue (period of 4 timed events) and stops when the enable returns to 0.
  - (2) **Latch:** a cross-coupled NAND set/reset latch held (SN=RN=1) from power-up. Digital's lock-step update oscillates at step 0, as its own documentation predicts for an RS flip-flop, and closes the model: 53 of 115 checked bits wrong, latch and c17 both frozen. Darion settles the latch to Q=0, then sets, holds and resets it correctly, with c17 correct throughout (0 of 115 wrong).
  - *Caveats:* the latch's power-up value is not defined in hardware (Icarus would give x). Darion's resolution to 0 is deterministic but arbitrary, and was not checked. Digital has an optional noise mode that avoids the latch failure (see Paper_Notes 3d, tv80). These are two small circuits showing the mechanism, not a statistic.
* **Other simulators (checked online):** ModelSim/Questa has a configurable iteration limit (`IterationLimit`; older manual default 5000, newer vsim messages 10 million, so version dependent) and exceeding it is a fatal "possible zero delay oscillation" error; Verilator stops after `--converge-limit` (default 100 in 4.x and 5.020, 10000 in the current guide); Logisim detects oscillation after a user-configurable iteration cutoff with a default of 1,000 (the earlier "150" figure was wrong); Digital stops after 1,000 micro-steps (verified in its source and observed, 3d). The default limits of VCS and Xcelium could not be verified and should not be stated.
* **Code:** `reactor/Circuit.pyx` (`set_wave_mode`, `propagate`).

---

## 2. Microarchitectural and Systems Claims

### Claim 4: 24-byte POD gate struct
* **Holds:** `static_assert(sizeof(CPP_Gate) == 24)`; 24 MB per million gates for the struct array.
* **Corrections:**
  - Ordering fields "from hottest to coldest by PMU profiling" has no effect: bytes 0–7 share one 8-byte word, so their order cannot change cache behavior.
  - 24 bytes does not tile 64-byte lines: 2 of every 8 structs (25%) straddle a cache line. Padding to 32 bytes is an untested alternative.
  - Fan-out lists are per-gate `malloc`ed arrays (`HitList`), so edges are not contiguous. A CSR edge array would be.
  - Resident memory is about 390 MB for 420k gates (roughly 930 B/gate), dominated by Python `Gate` objects and fan-out lists, not by the struct.
  - The gate counts in the benchmark reports are Verilog cell counts. The engine holds more entries after DFF expansion (b19: 356,399 entries versus 257,489 reported gates).
* **Code:** `reactor/Profile.h`.

### Claim 13: A flat, branch-free data-oriented engine removes the cost of an object graph — HOLDS WITH CAVEATS
* **Statement.** The central design claim: gates as plain 24-byte structs in one contiguous array, one branch-free evaluation rule (Claim 1), and a topologically reordered layout avoid the costs of an object-oriented gate graph. In `reactor_oop` every gate is a heap-allocated C++ subclass with a virtual `compute()`, so each evaluation is an indirect call through the vtable (an indirect-branch prediction problem) plus a pointer dereference per gate and per fan-out edge (a cache problem).
* **Evidence in `Benchmark/` (measured earlier, not rerun in this audit):**
  - *Whole-engine, real circuits* (`Benchmark/master_test/ITC99.md`): geomean speedup over Icarus is 3.88× for `rx-prop` and 3.54× for `rx-sweep`, against 1.78× for `rx-oop` (the Cython object graph). That is about 2.2× (prop) and 2.0× (sweep) over the OOP engine on the same circuits. Evaluation counts are close for prop and oop (b18: 5.05G versus 5.07G), so the gap comes from execution cost, not less work.
  - *Scaling sweep, chains and trees* (`Benchmark/perf/Cache_data.md` linear chain and `Cache_data_tree.md` complete binary tree; 67 sizes from 100 to about 985k gates, `perf` counters per iteration, deliberately fragmented placement). Time per iteration, OOP divided by optimized BFS layout (chain): 1.3× at 100 gates, 2.3× at 913, 4.0× at 8.5k, 6.6× at 280k, 21.6× at 985k (OOP 111.5 ms versus 5.2 ms; the unoptimized BFS layout takes 20.3 ms, so layout alone is 5.5× and reordering a further 3.9×). The tree topology gives the same shape (1.3× at 100, 3.6× at 2.4k, 6.3× at 370k). OOP IPC falls from 4.04 to 0.26 over the chain sweep (tree: 3.18 to 0.31) while the optimized BFS engine stays at 4.1–4.7 and the sweep at 3.8–5.9. Details at one size: at 523 gates: OOP needs about 5.1 µs per iteration, unoptimized BFS layout 3.6 µs, optimized BFS layout 3.2 µs, linear sweep 2.8 µs. OOP issues about 48% more L1 loads than the BFS engines (41.5K versus 28.0K) and about 1.6–1.8× the L1 misses (2.44K versus 1.35K and 1.49K per iteration). Topological reordering is worth about 11% (3.6 versus 3.2 µs).
  - *Large real circuits, PMU counters* (`Benchmark/master_test/ITC99.md`, Phase 3, whole-run `perf` totals, `rx-prop` versus `rx-oop`; one run each):

    | Circuit | cycles OOP / prop | L1 misses OOP / prop | L2 misses OOP / prop | branch misses OOP / prop | IPC prop / OOP |
    |---|---:|---:|---:|---:|---:|
    | b15 | 10.94B / 4.88B = **2.24×** | 1.26B / 0.70B = 1.79× | 93.6M / 13.1M = 7.1× | 54.8M / 10.4M = 5.3× | 3.61 / 1.86 |
    | b17 | 35.11B / 15.63B = **2.25×** | 3.71B / 2.10B = 1.77× | 1.03B / 257M = 4.0× | 142M / 26.3M = 5.4× | 3.28 / 1.68 |
    | b18 | 127.7B / 53.4B = **2.39×** | 10.23B / 5.86B = 1.75× | 3.50B / 1.28B = 2.7× | 931M / 368M = 2.5× | 2.73 / 1.31 |
    | b19 | 186.8B / 90.0B = **2.08×** | 17.77B / 10.21B = 1.74× | 6.10B / 2.63B = 2.3× | 950M / 378M = 2.5× | 2.79 / 1.55 |

    The OOP engine retires about 15% more instructions (and evaluates about the same number of gates) but needs about 2.1–2.4× the cycles, with 1.7–1.8× the L1 misses, 2–7× the L2 misses and 2.5–5× the branch mispredictions. This already covers the large-circuit counter data; the 2× is consistent across 17k–257k gates. The columns are whole-run totals from one run each, so treat the ratios as indicative until repeated.
  - *Branch side, direct evidence* (`Cache_data.md`, Phase 3): on chains `rx-oop` mispredicts about 3–5 branches per iteration up to about 600 gates, like the flat engines, then grows: 129 at 691 gates, 591 at 913, 1.1K at 1.2k, 9.6K at 5.6k, 39.7K at 22.6k, 647K at 370k and 1.75M at 985k, about one misprediction per gate evaluation. The optimized BFS engine reaches only 240 at 985k and the sweep 22. The onset near 600 gates fits an indirect-call predictor that can memorize a repeated sequence of vtable targets up to a few hundred entries and not beyond, but that explanation is a hypothesis (the BTB and history length were not tested), and because the same input repeats every iteration the memorization effect may flatter the small sizes.
  - *Nearest isolated analog* (this audit, Claim 1): replacing the unified rule with `switch(type)` on the same flat layout costs 1.1–1.7× and 57% more branch mispredictions (b15). A switch is a jump-table indirect branch, so this is a lower-level analog of the vtable cost, not a measurement of it.
  - *Repeated ITC99 counters* (`tests/src/perf.py`, `rx-prop` versus `rx-oop`, 5,000 vectors, pinned to one core, 9 repeats; `perf.py` itself runs each engine once per call and does not average, so the repeats are separate calls). Median [min, max] of the per-repeat OOP/prop ratio:

    | Circuit | cycles | L1 misses | L2 misses | branch misses | instructions | IPC prop / OOP |
    |---|---:|---:|---:|---:|---:|---:|
    | b15 | **2.05** [1.99, 2.11] | 1.67 [1.55, 1.68] | 7.2 [5.1, 9.6] | 5.4 [5.3, 5.7] | 1.18 | 3.54 / 2.03 |
    | b17 | **2.04** [1.98, 2.07] | 1.60 [1.57, 1.64] | 3.2 [2.7, 3.3] | 5.9 [5.5, 6.2] | 1.17 | 3.13 / 1.80 |
    | b18 | **2.12** [2.10, 2.22] | 1.62 [1.58, 1.63] | 2.6 [2.5, 2.7] | 2.5 [2.5, 2.6] | 1.16 | 2.61 / 1.43 |
    | b19 | **1.90** [1.86, 2.01] | 1.60 [1.57, 1.64] | 2.3 [2.3, 2.5] | 2.4 [2.2, 2.6] | 1.16 | 2.63 / 1.59 |

    The spread of `rx-prop` cycles across repeats is 3-5%. The repeats confirm the 2x but sit slightly below the single runs above (b18 2.12 versus 2.39, b19 1.90 versus 2.08); use the repeated figures.
  - *Isolated ablation, standalone C++ harness* (`tests/ablation_layout.cpp`, outside `reactor/`; AMD Ryzen 7 9700X, one pinned core, `-O3 -march=native`, 9 interleaved repeats with the variant order rotated each repeat, PMU read in-process, user mode). Four to six gate representations run the same propagate loop on the same netlist, input vectors and placement; every one of the 75 configurations produced identical evaluation counts, changed-gate counts and final-state fingerprints. Variants: **a** heap-allocated C++ subclasses with a virtual `compute()` (40 B, as `reactor_oop`); **b** the same objects placed contiguously in an arena (still virtual); **c** flat 24-byte structs with `switch(type)`; **d** flat 24-byte structs with the SIMA rule; **g** SIMA at 40 B; **e** SIMA at 32 B. Medians, ns per edge evaluation (paired spread within a configuration is mostly under 3%; the 1M-gate rows reach 5-20%):

    | Netlist (topological placement) | a heap+virtual | b arena+virtual | c flat+switch | d flat+SIMA | a / d |
    |---|---:|---:|---:|---:|---:|
    | NOT chain, 100 to 1M gates | 4.9-5.0 | 4.9-5.0 | 2.5-2.6 | 2.6-2.8 | 1.9 |
    | mixed-gate chain, 1k | 4.9 | 4.9 | 2.6 | 2.6 | 1.9 |
    | mixed-gate chain, 10k to 1M | 8.5 | 8.5 | 7.8 | 2.6 | 3.3 |
    | random DAG, 1k / 10k / 100k / 1M | 10.9 / 13.1 / 17.8 / 32.0 | 10.7 / 13.1 / 17.6 / 28.9 | 9.8 / 10.7 / 14.2 / 22.2 | 4.7 / 5.0 / 7.6 / 15.7 | 2.3 / 2.6 / 2.3 / 2.0 |
    | binary tree (XOR), 1k to 1M | 3.7-21.2 | 3.7-18.5 | 2.6-15.3 | 2.6-14.9 | 1.4 |

    What separates the effects:
    1. **Dispatch and evaluation rule dominate; layout does not.** With topological placement, a to b (layout only) is 0.99-1.04x up to 100k gates and 1.1-1.26x at 1M. The cost is in the call: even where nothing is mispredicted (NOT chain: 0.00 branch misses per edge) the virtual call costs about 2x (4.9 versus 2.6 ns) because it cannot be inlined or overlapped. On mixed gate kinds the indirect call also mispredicts (0.7-1.5 misses per edge for a versus 0.0-0.6 for d) and the ratio rises to 2.0-3.3x (4.9x at 10k for the varying chain).
    2. **`switch` is not a fix.** c (jump-table switch on a 24 B struct) is 0.8-0.9x the time of a on mixed gates and about 1.0x on uniform chains, i.e. most of the vtable cost reappears as a mispredicted indirect jump. The remaining c to d step (the branch-free rule) is 1.0-3x. This matches the engine-level switch ablation in Claim 1 (1.1-1.7x).
    3. **Layout matters only when placement is scattered and the working set leaves cache.** With shuffled placement and `--frag 192` (junk allocations between objects), a to b is 1.3-1.5x at 100k-gate chains and trees and 1.8-2.0x at 1M-gate chains (a 84.5 versus b 42.8 ns), and the a/d ratio reaches 6.4x. With shuffled placement but no fragmentation, a to b is 1.1-1.3x at 1M. At 1M gates the flat 24 B array (24 MB) fits in the 32 MB L3 while the 40 B objects do not.
    4. **Struct size is a cliff at the L3 boundary, not a smooth cost.** With shuffled placement at 1M gates d (24 B) is 12.6-13.0 ns, e (32 B) 27-29 ns and g (40 B) 44 ns on the chains; with topological placement or below 100k gates the three sizes are within about 10% of each other (hardware prefetch hides it). So 24 versus 32 B matters only for very large, scattered netlists, and part of that cliff is the separately allocated fan-out lists competing for the same L3.
    5. **Predictor memorization is real and depends on a repeated sequence.** On the mixed-gate chain (8 distinct virtual targets in a fixed order) the virtual-call misprediction rate is 0.00 per edge up to 1k gates and 0.88 from 10k; when random side inputs make the evaluated sequence differ from iteration to iteration (`--vary`) it is 0.00 at 100 gates, 0.70 at 1k and 0.98 at 10k. The onset moves down by about a decade, so the roughly 600-gate onset in the existing chain data is partly flattered by repeating the same input; the hypothesis that the predictor memorizes short repeated target sequences is supported, the BTB and history length themselves were not probed.
  - *Ablation on the real ITC99 netlists* (same harness, `--netlist`: Darion's gate array after reset and warm-up exported by `tests/ablation_eval.py --export`, replaying the benchmark's own input vectors; optimized layout and the as-parsed `raw` layout; 9 interleaved repeats, spread 1-12%, identical fingerprints in all 16 configurations). Median ns per edge evaluation and the ratio of a to d:

    | Circuit (gates) | a heap+virtual | b arena | c switch | d SIMA | a/d time | a/d cycles per edge | branch misses per edge, a / d |
    |---|---:|---:|---:|---:|---:|---:|---:|
    | b15 (24k) | 4.12 | 4.05 | 3.30 | 2.28 | 1.81 | 22.6 / 12.5 | 0.141 / 0.026 |
    | b17 (73k) | 4.78 | 4.72 | 3.72 | 2.72 | 1.76 | 26.3 / 15.0 | 0.135 / 0.023 |
    | b18 (182k) | 6.33 | 6.05 | 4.95 | 3.29 | 1.92 | 34.8 / 18.1 | 0.294 / 0.109 |
    | b19 (356k) | 5.71 | 5.42 | 4.54 | 3.36 | 1.70 | 31.4 / 18.5 | 0.179 / 0.064 |

    These are the optimized layouts with topological placement; the raw layout gives 1.5-1.8x. The in-harness loop therefore reproduces the engine-level gap measured with `perf.py` (1.9-2.1x cycles for the full Cython engines), which supports using the harness to attribute it. On real circuits the split is: layout (a to b) 1.01-1.09x (1.2-1.4x on b18 and b19 when placement is shuffled and fragmented), the virtual call versus `switch` (a to c) 1.2-1.3x, and the branch-free rule (c to d) a further 1.35-1.5x. Struct size (24 versus 32 or 40 bytes) costs 3-15% on real circuits at these sizes, no cliff (the whole array stays within L3). Real circuits mispredict far less than the random-DAG synthetic case (0.13-0.29 versus 1.4 misses per edge for a), which is why the real-circuit ratio is 1.7-1.9x rather than 2-3x.
  - *Other suites: ISCAS85, EPFL, OpenCores* (same method; exporter generalized to `suite/circuit`; 19 circuits harness-only plus the 5 ITC99 above = 24 circuits for the comparison below; 7 repeats of `perf.py` per circuit for the engine ratio, 9 repeats for the harness; no fingerprint mismatch in 46 harness configurations). The data-oriented advantage is not specific to ITC99:

    | Suite | circuits (gates) | harness a/d (topological) | engine OOP/prop cycles (median of 7) |
    |---|---|---:|---:|
    | ISCAS85 | c1908, c3540, c5315, c6288, c7552 (0.9k-3.8k) | 2.14, 2.38, 2.27, **1.46**, 2.19 | 2.43, 2.71, 2.35, **1.48**, 2.28 |
    | EPFL | adder, bar, max, arbiter, cavlc (1.3k-24k) | 2.01, 1.43, 1.99, 1.46, 2.53 | 1.96, 1.80, 2.03, 2.04, 3.38 |
    | OpenCores | des_area, systemcaes, tv80, ac97_ctrl, mem_ctrl, aes_core, des_perf, usb_funct, wb_conmax, vga_lcd (8k-444k) | 2.31, 1.77, 1.56, 1.39, 1.57, 2.42, 2.04, 1.51, 1.49, 1.31 | 2.36, 2.02, 1.74, 1.77, 1.90, 2.59, 2.29, 1.76, 1.67, 1.67 |

    Over all 24 circuits the harness a/d ratio (median 1.79, range 1.31-2.53) and the full-engine cycle ratio (median 2.04, range 1.48-3.38) correlate with Pearson r = 0.89, so the harness ranks circuits correctly, but it underestimates the engine ratio by about 0.25 on average and the engine ratio falls inside the harness's [topological, shuffled+fragmented] bracket for only 6 of 24 circuits. Whatever `reactor_oop` pays beyond the harness (extra instructions in the Cython loop, about 15-20% more retired instructions in every circuit, allocation behaviour) is not captured; the attribution to dispatch/rule is therefore a lower bound, not the whole story. The size of the gap follows how often the OOP engine mispredicts: harness a/d correlates with the harness branch misses per edge of the OOP variant at r = 0.90 (c6288, a multiplier with 0.35 misses per edge and uniform behaviour, gives the smallest gain, 1.46x; mixed-type ISCAS85 and DES circuits at 0.5-0.7 misses per edge give 2.1-2.4x; `vga_lcd`, 0.007 per edge, 1.3x). Layout (a to b) is again small (1.00-1.10x topological), except for the largest scattered cases (`des_perf` 1.78x and `vga_lcd` 1.65x with shuffled, fragmented placement).
    Unreliable engine figures, not used above: c880, router and priority (469-2k gates; the instruction ratios between the two engines vary 7-50x between repeats and cycle ratios have ranges of 3-10x, so fixed per-run overhead dominates the whole-run counters), and the tv80 shuffled harness run (33% spread).
  - *Second platform: AMD Ryzen 5 PRO 5675U (Zen 3 laptop, 6 cores, 16 MB L3, performance governor, on AC)* (2026-10-21, logs in `Benchmark/5675U/`; the machine record is `Machine.md`; core 2, 9 repeats, same commands as Paper_Notes 6b; integrity suite 28,115 passed, 0 failed first). Full engines, `perf.py`, median [min, max] of the per-repeat OOP/prop cycle ratio:

    | Circuit | cycles OOP / prop | IPC prop / OOP | branch misses prop / OOP (M) | L2 misses OOP / prop |
    |---|---:|---:|---:|---:|
    | b15 | **1.84** [1.54, 1.88] | 2.20 / 1.40 | 1.8 / 10.2 | 1.98 |
    | b17 | **1.65** [1.48, 1.86] | 1.92 / 1.35 | 6.2 / 23.4 | 2.95 |
    | b18 | **2.11** [1.76, 2.17] | 2.06 / 1.13 | 50.9 / 141.2 | 3.06 |
    | b19 | **2.59** [2.47, 2.69] | 2.05 / 0.92 | 52.4 / 153.8 | 2.98 |

    The ratio is 1.65-2.59x, against 1.90-2.12x on Zen 5 (table above), so the advantage is present on a different, older core with half the L3, but it is not the same number: b15/b17 are lower, b19 is higher, and the per-repeat spread is much wider (up to 0.4x within a circuit versus under 0.25x on the desktop). The wide spread was first attributed to the SMT sibling, and that attribution was wrong or at best incomplete. What was measured (`ITC99_PMU.md`): (1) `perf.py` pins to core 2, whose SMT sibling is cpu 3; a busy loop on the sibling costs +16% (b17 prop) to +40% (b19 prop 15.7B to 22.0B) cycles and +37-39% for rx-oop, so sibling contention is real. (2) But with the sibling taken offline (root, quiet machine, 9 repeats) `rx-prop` is still bimodal on b15, b17 and b18 at identical instruction counts: b17 prop is 3.03-3.25B cycles in five processes and 4.10-4.15B in four (6.59-6.60B instructions in all nine), b18 8.97-9.22B or 10.05-10.96B, b15 1.03-1.04B or 1.12-1.30B. Only b19 prop is steady (15.58-15.76B, 1% spread). The OOP engine is steadier on b15-b18 (4-9%) and varies 11% on b19. So the run-to-run switching between a fast and a slow mode comes from the process, not from a neighbour thread; it has the same signature as the harness slow mode in `Ablation_reruns.md` (about +35% cycles for the same work, per-process, appearing from a large working set) and is probably the same cause (page or cache-set placement of the gate array), but that was not tested. Quiet results with the sibling offline, median [min, max] of the per-repeat OOP/prop cycles: b15 1.81x [1.43, 1.97], b17 1.72x [1.35, 1.86], b18 1.92x [1.76, 2.19], b19 2.45x [2.39, 2.65] (prop 1.04B, 3.25B, 10.05B, 15.71B; OOP 1.91B, 5.64B, 19.22B, 38.46B; OOP IPC 1.38, 1.35, 1.13, 0.97 against prop 2.17, 2.03, 1.86, 2.05). Dividing OOP's median by prop's fast-mode cycles gives b15 1.85x, b17 1.86x, b18 2.14x, which is close to the sibling-busy table and to Zen 5's 2.0x; the median-of-ratios figures are lower because slow-mode prop runs enter them. Use the range 1.7-2.5x for this CPU and report the bimodality with it; do not quote a single ratio. Cycle counts on this laptop are not comparable with the desktop's in absolute terms. Why b19 is higher was not investigated; its OOP IPC falls to 0.97 and L2 misses are about 3x, which is consistent with, but does not show, the smaller L3 hurting the pointer-based engine more.

    Sibling-controlled repeat (`ITC99_PMU.md`, run afterwards with a constant busy loop on cpu 3 so every run sees the same SMT contention, 9 repeats, IDE open, so absolute cycles are inflated: prop 1.46B, 4.33B, 13.0B and 24.4B for b15, b17, b18, b19): OOP/prop cycles b15 1.78x [1.74, 1.81], b17 1.87x [1.86, 1.90], b18 2.24x [2.17, 2.31], b19 2.93x [2.78, 3.46]. The spread of `rx-prop` cycles is 2-5%; the OOP engine's is 1-7% except b19 (22%), so the OOP engine is the more load-sensitive one at the largest size. Against the quiet table above this changes b17 (1.65x to 1.87x, the quiet value was prop noise) and leaves b15, b18 within 0.15x; b19 is 2.6-2.9x depending on conditions. Use 1.8-2.9x across these four circuits on this machine, with b19 condition-dependent. The ratio is also not constant in size here: it rises from b15 to b19 on this CPU (with 16 MB L3), while on Zen 5 it stayed near 2.0x.

    OpenCores prop-only benchmark and load on the laptop (`Opencores.md`, `Opencores.md`; 21 circuits, 10,000 vectors, one run each, rx-prop only, cell library Cadence GSCLib): rx-prop is faster than Icarus on 17 of 21 circuits and faster than Verilator on 1 of 21 (usb_funct, 1.73x); Verilator is ahead on the other 20, as the claims doc already states for ITC99 (Verilator ahead on 17 of 21 there). Load (DESIGN mode, `Opencores.md`): 0.4 ms for 184 gates, 13 ms for 6.4k, 36 ms for 14k, 581 ms for 112k and 1,113 ms for 187k gates (vga_lcd), with `optimize()` 0.0-208 ms of that; Icarus compile takes 6.1 s for vga_lcd. These match the interactive-turnaround claim (Claim 8) on a second machine; they are single runs.

    Ablation harness on the real ITC99 netlists (same method, optimized layout, topological placement, 9 repeats, identical fingerprints for all five). Median ns per edge evaluation, and time relative to a:

    | Circuit (gates) | a heap+virtual | d flat+SIMA | a / d | b arena / a | c switch / a | branch misses per edge, a / d |
    |---|---:|---:|---:|---:|---:|---:|
    | b14 (14k) | 11.76 | 6.11 | 1.92 | 1.035 | 0.81 | 0.636 / 0.235 |
    | b15 (24k) | 8.51 | 5.24 | 1.62 | 0.96 | 0.76 | 0.187 / 0.030 |
    | b17 (73k) | 9.05 | 6.11 | 1.48 | 1.03 | 0.82 | 0.170 / 0.036 |
    | b18 (182k) | 11.13 | 7.10 | 1.57 | 0.98 | 0.80 | 0.334 / 0.115 |
    | b19 (356k) | 12.44 | 8.78 | 1.42 | 1.02 | 0.77 | 0.207 / 0.069 |

    The split has the same shape as on Zen 5: layout alone (a to b) is 0.96-1.04x, the `switch` recovers about a fifth (c is 0.76-0.82 of a), and the remainder comes from the branch-free rule. The a/d ratio is 1.42-1.92 here against 1.70-1.92 on Zen 5, and absolute times are higher (d is 5.2-8.8 ns versus 2.3-3.4 ns per edge on the desktop, about 2.3-2.6x slower per edge). The full-engine ratio is above the harness ratio on all four circuits shown (b15 1.84 vs 1.62, b17 1.65 vs 1.48, b18 2.11 vs 1.57, b19 2.59 vs 1.42), a larger gap than the 0.25 seen on Zen 5, which was not explained.

    Struct size against L3 (`Ablation.md`, shuffled placement with `--frag 192`, chain, 1M gates, `-O3 -march=native`): flat24+SIMA takes 60 ns per evaluation here against 12.6-13.0 ns on Zen 5; flat32 takes 74 ns (Zen 5: 27-29) and flat40 84 ns (Zen 5: 44). On Zen 5 the 24 MB array of 24-byte gates fits the 32 MB L3 and the 32/40-byte arrays do not, which produced the size cliff. On this machine's 16 MB L3 none of the three fits, all are bound by memory latency, and the gap between sizes shrinks (24 B is still the fastest). This is the move of the cliff with L3 size that the run sheet predicted; the 1M-gate numbers are about 5x slower than the desktop's for the 24-byte variant for the same reason.

    Branch-free is not the same as branchless end to end (`Ablation.md`, random DAG, 1k to 1M gates): the flat24+SIMA variant still mispredicts 0.57-0.65 branches per evaluation, against 1.27-1.40 for the virtual and `switch` variants (`switch` only 1.27 versus 1.39 for the virtual call). On the mixed-gate and uniform chains and the trees its rate is 0.00-0.04, so the residue comes from data-dependent control flow (for example whether an output changed and a fan-out is queued) on irregular graphs, not from gate dispatch. This was measured on the laptop only.

    ISCAS85 master_test on the laptop (`Benchmark/5675U/ISCAS85.md`, 50,000 vectors, 10 circuits, one run each, geomean speedup over Icarus, laptop against the stored Zen 5 report): rx-prop 8.42x (Zen 5: 9.64x), rx-sweep 14.14x (12.70x), rx-oop 4.69x (4.58x), Verilator 181.5x (156.8x). The prop-over-OOP ratio falls from 2.10x to 1.80x on this suite, because rx-prop loses ground relative to Icarus while rx-sweep gains; the reason was not investigated (the laptop's L1d is 32 KB and L2 512 KB per core against 48 KB and 1 MB, which is one possible factor). Counters repeated quietly (SMT sibling offline, 5 repeats, 5 circuits, `ISCAS85.md`): cycles OOP/prop are c1908 1.93x, c3540 2.27x, c5315 1.85x, c6288 1.44x, c7552 1.97x, and rx-prop needs 1.41-1.96x the cycles of rx-sweep on four circuits and 12.8x on c6288, because it retires 1.8-2.1x the instructions (11.7x on c6288; c1908 287M against 136M; c6288 5.06G against 431M; the evaluation counts above give the same ratio). The sweep has the lowest cycles on every circuit, the highest IPC only on c6288, and the fewest mispredictions except on c3540, c5315 and c7552, where it has more than prop. These counters show where the prop-versus-sweep gap comes from (evaluation count) but not why it is larger on the laptop than the desktop (wall-clock prop/sweep c1908 1.97 against 1.55, c3540 1.38 against 1.15), which remains unexplained. On c6288 propagate performs 1.29G evaluations against 116M for the sweep and the sweep is 12.5x faster, as on the desktop.

    Synthetic sweep (`Ablation.md`, 32 configurations plus the `--vary` run; topological placement, a/d time): NOT chain 1.35-1.42x from 1k to 1M gates (Zen 5 table: 1.9), tree 1.24-1.54x, mixed-gate chain 2.25-2.32x up to 100k and 1.51x at 1M (Zen 5: 3.3), random DAG 1.96, 2.14, 1.67 and 1.19x at 1k, 10k, 100k and 1M. With shuffled placement and `--frag 192` the chain ratio rises to 2.09x at 10k and 2.53x at 100k, tree to 2.15x at 131k, and mixed-gate chain to 2.87-2.90x at 10k-100k; at 1M it is 1.76-1.92x, because d itself slows (60-72 ns versus 6.5-12 ns topological). So the dispatch-only gap on a uniform chain is smaller on Zen 3 than on Zen 5, the scattered-placement effect is present and starts at 10k gates, and the large-size numbers are dominated by memory latency. 

    Struct size at 500k-2M gates does not give a stable answer in single calls (rerun, `Ablation_reruns.md`: mixed-gate chain, topological, 100k to 2M gates, variants a, d, e, g, 3 separate processes each). At 100k-300k gates every variant is stable (d 5.1-5.7 ns, e 4.8-5.8, g 4.8-6.1). From 500k gates a variant in a given process often lands in a "slow mode" about 5.7 ns higher (d 6.0 or 11.8 ns, e 6.3 or 11.4, g 6.9 or 11.7, a 12.1 or 17.7) with L1 misses per evaluation jumping from 1.14 to 2.15 (d), 1.27 to 2.28 (e), 1.39 to 2.40 (g) and 1.52 to 3.92 (a). Which variant and which call it hits changes from call to call at the same size, so it is a property of the process (page placement or alignment of the arrays), not of the struct size. The earlier reading that the 24-byte struct loses to 32/40 bytes on this machine at 1M gates is therefore not supported: in this rerun d is the fastest in every fast-mode case from 300k gates up (at 100k, e and g are 0.3 ns faster, 4.8 against 5.1 ns) and the 32/40-byte variants show no consistent advantage. Two consequences: single-call numbers at 500k gates and above carry a bimodal +5.7 ns error, and the 1M-gate size comparisons quoted above (Zen 5 and laptop, shuffled placement) come from single calls; the shuffled-chain comparison was therefore repeated across processes on the laptop (`Ablation_reruns.md`: chain, 1M gates, shuffled, `--frag 192`, 7 separate processes, 5 reps each, with the IDE open, so not a quiet-machine run). Median [min, max] ns per evaluation: a heap+virtual 121 [121, 123], d flat24+SIMA 78 [77, 87], e flat32 86 [86, 98], g flat40 94 [93, 101]; one process in seven was 10-12% slower for d, e and g. A quiet repeat afterwards (SMT sibling offline, IDE closed, 7 processes, `Ablation_reruns.md`) gave a 116.3 [116.1, 117.7], d 61.7 [59.1, 63.3], e 74.7 [72.8, 76.9], g 84.4 [83.7, 85.2] ns, i.e. e/d 1.21 and g/d 1.37, with no slow-mode runs; so the IDE-open absolute values above are about 25% too high and the quiet ones should be used. The ordering d < e < g < a is the same in every process and the spread between sizes is small (e/d 1.10, g/d 1.20), against 2.2 and 3.5 for the single Zen 5 calls (12.6, 27-29, 44 ns), so the compression of the size gap on the 16 MB L3 holds. The absolute values depend on machine state: the quiet single call gave d 60, e 74, g 84 ns, 20-30% lower than here. The Zen 5 figures were not repeated across processes.

    Predictor memorization (rerun, `Ablation_reruns.md`: mixed-gate chain, 54 to 10k gates, a and d only, static and `--vary`): the virtual-call variant mispredicts 0.60 per evaluation at 54 gates, 0.76 at 104, 0.80 at 206, 0.83 at 409, 0.86 from 713 gates, and the same with `--vary` (0.58-0.88). There is no region of perfect prediction: Zen 3 does not memorize even the shortest sequence tested, and static and varied inputs look the same. On Zen 5 the same chain gave 0.00 up to 1k gates when static. The flat SIMA variant stays at 0.00-0.01 throughout. The onset on Zen 3 lies below 54 gates and was not located. This supports the predictor memorization being a property of the CPU, and Zen 5 hides the virtual-call cost on short repeated sequences much better than Zen 3. (The `--vary` run at 54 gates ran with one iteration and is invalid.)

* **Caveats.**
  - `rx-oop` differs from `rx-prop` in dispatch, layout and graph representation at once, so the ITC99 2× is the total effect of the design. The standalone harness splits it on synthetic netlists: mostly dispatch plus evaluation rule (1.9-3.3x), with layout adding little unless placement is scattered and the working set exceeds cache. The harness also runs the real ITC99 netlists (above). It is not the Cython engines: its loop mirrors `propagate()` but omits wave limits, the visual queue, the Python layer and timing, and `reactor_oop`'s IC input/output pin gate classes are merged into the BUF class. The match with the `perf.py` ratios is evidence the attribution transfers, not a proof.
  - The chain and tree tests are synthetic (one or two fan-ins per gate, one wave, a repeated input, deliberately shuffled placement, the worst case for OOP), so the 21.6× at 985k gates is an upper bound, not a prediction for real circuits; the real-circuit ratio is the 2.1–2.4× above. All of these are single runs and none separates dispatch from layout.
  - The ITC99 geomean mixes small and large circuits; per-circuit ratios vary.
  - IPC alone is not evidence (OOP also reaches about 4 IPC on 100-gate chains); use cycles and time (Claim 11).
  - The structure has known inefficiencies (Claim 4): 25% of 24-byte structs straddle cache lines and fan-out lists are separately allocated.
* **Not done:** probing BTB and history length directly; a second CPU is now done for the full engines and the harness (Zen 3 laptop above), but only that one and no ARM or Intel; all the other numbers above are Zen 5 only; ISCAS89 (different sequential harness), EPFL large/mammoth and Faraday; explaining why the engine ratio exceeds the harness ratio.
* **Code:** `reactor/Profile.h`, `reactor/Gates.pyx`, `reactor/Circuit.pyx` (`optimize`), `tests/ablation_layout.cpp`.

### Claim 5: Dynamic bounded topological sweep with back-edge escape: HOLDS
* `sweep()` walks the contiguous array between the lowest and highest triggered gate, skips unmarked gates by flag test, and hands back-edges (`target <= curr`) to `propagate`. Correctness verified by the fuzz in Claim 1 (COMPILE mode, optimized and unoptimized layouts).
* **Feedback and oscillation (2026-10-21).**
  - The sweep needs no static loop analysis. A change reaching a gate at or behind the cursor (`target <= curr`) is a back edge and is handed to `propagate` on the same data, with the live-size budget and non-fatal timed promotion (Claim 3).
  - Measured with a live 3-gate ring oscillator appended to b15 and b19 (scratch `ring_*.json`), in COMPILE (sweep) mode: the ring is promoted to the timed queue, and over 39 later vectors the outputs match the ring-free circuit exactly (0 mismatches), the same as propagate mode.
  - The sweep was also verified at flip-flop-state level against Icarus on ITC99, whose gate-level flip-flops are latch loops (`tests/verify_state.py`, rx-sweep).
  - *Prior art:* LECSIM (Wang and Maurer 1990, read in full from TR DA-19, 1988) finds SCCs by DFS and breaks the identified feedback paths to levelize. Small SCCs become compiled iteration blocks (cap 2^m+1 for m feedback arcs, else a user default, then an error routine). For large SCCs its top-level scheduler sets an `unstable` flag when a block is inserted into an already-scanned level and repeats the full level scan up to a user-specified limit. **That runtime back-edge test is the same as Darion's `target <= curr`**, so Darion cites it and does not claim it. Verilator detects loops at compile time (UNOPTFLAT) and stops with a fatal "didn't converge" at runtime. EPICS (IEEE 2025, fault simulation) mixes compiled and event-driven simulation for SCCs after static analysis.
  - *Preprocessing cost:* one Kahn topological sort, O(V+E), in `optimize()`; no strongly-connected-component analysis.
    - When the sort stalls on a cycle, the remaining gates are forced in (in-degree set to 0) and placed breadth-first, so each cyclic group lands contiguously.
    - Edges into the output pins of sequential ICs are ignored by the sort (`FLAG_BOUNDARY`). Today these ICs are recognised by name (`dff`, `flip`, `latch` or `tlat` in the IC name, `reactor/IC.pyx`). The author plans to replace this with an optional flip-flop flag in the IC's JSON, cutting at the IC boundary when it is set.
  - *Distinct here (narrowed 2026-10-21 after LECSIM):* levels come from one Kahn sort with forced placement, with no SCC or feedback-arc analysis; a back edge is delegated to the event-driven engine on the same structure under the live-size budget, instead of a repeated full pass with a fixed cap; the oscillation path is non-fatal; and nothing is recompiled or re-analysed when an edit creates a loop (LECSIM names recompilation after each modification as its major problem). Claim with "to our knowledge".
  - *Efficiency:* on deep arithmetic the sweep does 200x fewer evaluations than propagate (hyp: 129M versus 25.6G, Claim 10).
* **Code:** `reactor/Circuit.pyx` (`sweep`).

### Claim 6: Inertial delay glitch absorption: HOLDS
* See `Timing_Report.md`. Known defect B8 (phantom flip re-stamping `gate_clocks`) is listed there.

### Claim 7: Decoupled visual interface (engineering, not research)
* The UI holds integer gate indices, and changed gates are reported through a `visual_queue` deque. The simulation core is single-threaded and cooperative (asyncio), so there is no concurrency for the "lockless / no thread locking" wording to apply to. This is sound design but is not a research contribution.
* **Measured cost of the UI coupling (engine side):** `batch_toggle` over 3,000 benchmark vectors with every gate's update flag cleared (so each changed gate is pushed once into `visual_queue`) versus all flags set (nothing queued), pinned core, 7 interleaved repeats: b15 and b17, propagate and sweep, 0.995-1.002x (one 1.017x case with spread 3.6%), i.e. within noise. 8.6k (b15) and 18.4k (b17) distinct gates were queued per run; draining them with `pop_visual_queue` from Python took 0.3 and 0.7 ms. Reproduce with `tests/ablation_eval.py --ui-cost <reactor_dir> b15 prop`.
* **API latency** (`tests/ablation_eval.py --latency <reactor_dir> b15`, pinned core, 20,000 calls each, settled circuit, random single-input changes): an empty `cpdef` call is 0.05-0.06 us, reading `gate.output` 0.07 us, `toggle(loc, val)` 0.25-0.34 us median (b15 24k gates, b19 356k gates), `batch_toggle` with one input 0.53-0.60 us. The tail is the propagation itself: p99 13.7 us on b15 and 243 us on b19, worst observed 48 us and 0.69 ms; a whole 38-input vector change takes 14 us (b15) and 195 us (b19). All of it is far below a 16 ms frame. Single-event calls are synchronous in `SIMULATE`/`COMPILE` mode; the asyncio runner is used only for the real-delay engine. Not measured: rendering and the cadence of a real UI.
* **Case study: locating a bug in a running CPU** (`tests/verify_state.py --case-study --seed N`, 2026-10-21, pinned core, 5 seeds).
  - *Setup:* tv80 runs the Z80 program of the tv80 workload for 2,000 cycles. A copy has one injected bug: a 2-input cell swapped, NAND2 to NOR2 or the reverse, in the Verilog for Icarus and as the same gate's type in Darion's JSON. The selection was untimed, chose bugs at random, and kept the first one that reaches the bus and is latent: no gate differs until the program runs.
  - *Task:* using the golden design as the reference, find the first half-cycle at which the bus differs, the first half-cycle at which any internal signal differs, and the gate that causes it (a differing gate whose inputs all agree).
  - *Darion:* load both copies and run them side by side through the API until the bus differs. Then reload, replay, and after every half-cycle compare the gates either copy reports as changed (the visual queue). This was checked against a full compare of all 15,992 gates after every step on 6 bugs: same answer.
  - *Icarus:* compile both copies with `$dumpvars` of every tv80 net, run the program, diff the two bus traces, then find the first difference and the root net in the two VCDs using the netlist's cell connections. X against a known value is not counted as a difference: under 4-state X, NAND and NOR resolve X inputs differently.

  | Seed | Injected bug | Bus differs (half-cycle) | First internal difference | Root found | Darion total | Icarus total (compile + run with dump + analysis) |
  |---|---|---:|---:|---|---:|---:|
  | 1 | g35785 NAND2->NOR2 | 37 | 21 | injected cell, both | 171 ms | 27.3 s (15.5 + 11.1 + 0.7) |
  | 2 | g35828 NOR2->NAND2 | 85 | 21 | injected cell, both | 140 ms | 27.1 s (15.0 + 11.2 + 0.9) |
  | 3 | g33371 NAND2->NOR2 | 81 | 75 | injected cell, both | 189 ms | 28.2 s (15.3 + 11.5 + 1.4) |
  | 4 | g37522 NAND2->NOR2 | 101 | 57 | injected cell, both | 179 ms | 28.3 s (15.4 + 11.6 + 1.3) |
  | 5 | g29330 NAND2->NOR2 | 101 | 51 | injected cell, both | 157 ms | 27.9 s (15.1 + 11.5 + 1.4) |

  - *Agreement:* both workflows agree on every number in every seed, and both name the injected gate as the only root. Darion's totals include loading both copies twice (about 30 ms per load). Icarus's include two compilations (about 7.5 s each) and two runs.
  - *Fixed cost of an Icarus run:* starting the compiled simulation dominates, not simulating the program. One design runs to the failing half-cycle in 5.3-5.5 s and through all 4,000 half-cycles in 5.5-5.6 s, without the dump. A user who already knew the failing step would still pay roughly 7.5 s compile plus 5.3 s run per design and per change to the testbench. The VCD was 3-6 MB per design for this short run.
  - *How to say it:* "a bug in a CPU running a program was located through the API in under 0.2 s from load, versus about 27 s for a compile, dump and analyse flow with Icarus that reached the same answer." Icarus's 4-state view is stricter; the test does not claim Darion is the more informative simulator.
  - *Caveats:* one design, five bugs, all single-gate type swaps; the Icarus flow is automated by a script here, while a person using a waveform viewer would take longer; Icarus also has an interactive mode (`$stop`, VPI), which was not used; Verilator was not part of this test.

---

## 3. Empirical Claims

All numbers below were reproduced on this machine unless marked otherwise. Benchmark stimulus is uniformly random inputs, including the reset pin, with both engines fed identical vectors.

### Claim 8: Turnaround vs. Verilator: HOLDS WITH CAVEATS

| Circuit | Verilator build | Darion load + optimize (from .json) | Darion from .v (in-Python parser) |
|---|---:|---:|---:|
| b14 | 5.99 s | 9.79 ms | 53 ms (re-measured) |
| b17 | 23.22 s | 66.43 ms | 293 ms (re-measured) |
| b19 | 160.60 s | 554.24 ms | 1,793 ms (re-measured) |

* The headline times load a pre-parsed `.json`. Including the Verilog parse the advantage is still about 90× on b19.
* Against Icarus, whose build time includes parsing, the advantage is only about 2.6–8× (b19: 4.66 s versus about 0.55–1.8 s).
* **What the load time contains** (`tests/src/load.py`, `Benchmark/master_test/ITC99.md` Phase 1): the loader builds the full editable circuit in DESIGN mode (per-gate Python wrappers, inspectable and interactive) and `optimize()` is timed separately (b19: 554 ms load plus 118 ms optimize). Verilator's time yields only a compiled binary that runs and dumps. So the comparison is load-to-interactive versus compile-to-run.
* **The price is memory** (Phase 1 footprint): b19 261.5 MB (peak 332 MB) for Darion, 828 MB for Icarus, 3.4 MB (peak 7 MB) for Verilator; b14 17.4 / 36.9 / 1.1 MB. Darion uses less than Icarus (about 2-3x) and far more than Verilator (about 15-75x at b14-b19 sizes, more on small circuits). The gate counts in these tables are Verilog cell counts; the engine holds more entries after DFF expansion (b19: 356,399).
* A fast `-O0` Verilator build was not measured; the attempt on b19 had not finished after more than 10 minutes and was stopped.

### Claim 9: Faster than Verilator on large netlists (numbers HOLD; explanation REFUTED)
* **Reproduced** (3,000 logical vectors, `rx-prop` / `rx-sweep` versus Verilator at its default `-Os`):

| Circuit | Verilator vs. Darion |
|---|---|
| b14 (14k entries) | Verilator 6–7× faster |
| b15 | Verilator about 2× faster (fresh run) |
| b17 (73k) | about parity (`rx-prop` 1.1–1.2×) |
| b19 (356k) | Darion 2.3× (benchmark stimulus) to 3.6× faster (sparse inputs) |

* **Full ITC99 picture:** Verilator is faster on 17 of 21 circuits. The "up to 2.49×" figure comes from the four largest ones. Report both.
* **The old explanation (low switching activity) is wrong.** Measured gate-output activity is about 9.5–10.4% for b15, b17, b18 and b19, and 18.6% for b14. The previous document stated 2–6%. Circuits with the same activity (b15 versus b19) give opposite outcomes. Activity also does not fall when inputs go quiet: at a 0.5% input toggle rate b17 still visits about 15k edges per vector, because the clock and the gate-level DFF latches keep switching. That activity floor comes from Darion's DFF expansion.
* **Supported explanation: compiled-code footprint (size sweep, benchmark stimulus, 1,500 logical vectors).** Verilator's cost per gate per vector rises as its generated code outgrows the instruction cache, while Darion's cost per gate depends on activity and grows only slowly with size:

  | Circuit | engine entries | Verilator code | Verilator IPC | Verilator L1i misses / 1k instr | Verilator ns/gate/vec | `rx-prop` ns/gate/vec | Verilator ÷ `rx-prop` time |
  |---|---:|---:|---:|---:|---:|---:|---:|
  | b14 | 14,299 | 0.75 MB | 1.97 | 9.0 | 0.31 | 2.00 | 0.16× |
  | b15 | 24,329 | 1.20 MB | 2.38 | 5.6 | 0.28 | 0.56 | 0.50× |
  | b20 | 31,189 | 1.67 MB | 2.24 | 8.8 | 0.34 | 1.30 | 0.26× |
  | b22 | 45,448 | 2.43 MB | 1.71 | 13.9 | 0.48 | 1.73 | 0.28× |
  | b17 | 73,475 | 3.80 MB | 1.23 | 19.4 | 0.69 | 0.64 | 1.09× |
  | b18 | 182,380 | 11.39 MB | 0.67 | 15.9 | 1.48 | 0.86 | 1.72× |
  | b19 | 356,399 | 21.97 MB | 0.67 | 17.1 | 1.74 | 0.75 | 2.31× |

  Verilator's ns/gate rises 5.6× and its IPC falls from about 2.0 to 0.67 as code grows from 0.75 MB to 22 MB; the crossover (parity) sits near 3–4 MB of generated code. Darion's per-gate cost varies with activity (b14, b20 and b22 are higher). This is a correlation across seven circuits of different structure.
* **Controlled size experiment (confirms the Verilator side, refines the Darion side).** I replicated one block (b14) k times side by side with shared clock and reset and independent data inputs, so structure and per-copy activity are fixed and only size changes (`500` logical vectors, benchmark stimulus):

  | k | engine entries | Verilator code | Verilator IPC | Verilator ns/gate/vec | `rx-prop` ns/gate/vec | `rx-sweep` ns/gate/vec | Verilator ÷ `rx-prop` | Verilator ÷ `rx-sweep` |
  |---:|---:|---:|---:|---:|---:|---:|---:|---:|
  | 1 | 14,299 | 0.75 MB | 2.02 | 0.31 | 1.95 | 1.35 | 0.16× | 0.23× |
  | 2 | 28,598 | 1.36 MB | 1.98 | 0.33 | 2.19 | 1.55 | 0.15× | 0.21× |
  | 4 | 57,196 | 2.62 MB | 1.54 | 0.43 | 2.22 | 1.59 | 0.20× | 0.27× |
  | 8 | 114,392 | 5.09 MB | 0.88 | 0.75 | 2.35 | 1.57 | 0.32× | 0.48× |
  | 16 | 228,784 | 10.54 MB | 0.59 | 1.13 | 2.71 | 1.80 | 0.42× | 0.63× |
  | 32 | 457,568 | 20.30 MB | 0.54 | 1.23 | 3.19 | 2.01 | 0.38× | 0.61× |

  With structure fixed, Verilator's cost per gate rises 4× and its IPC falls from 2.0 to 0.54 as its generated code grows from 0.75 MB to 20 MB: this is **causal evidence for the code-footprint mechanism**. But Darion's own cost per gate also rises (+63% for `rx-prop`), and on this high-activity block (about 18%) Darion never overtakes Verilator even at 457k gates. With a quiet stimulus (reset deasserted, 2% bit flips) the ratio improves (0.32× at k=1 to 0.47× at k=32 for `rx-prop`) but still does not cross. So the crossover depends on size **and** on the structure and activity of the design: b17/b19 (about 10% activity) cross at about 70k gates, b14 blocks do not cross by 457k. Do not state a single size threshold.
* **What sets Darion's activity floor: the clock.** Holding the clock fixed drops measured gate activity from about 8–10% to 0.2–1.9% (b15: 10.1% → 1.9% at 50% input toggling, 8.2% → 0.25% at 5%; b17: 9.8% → 1.3% and 8.2% → 0.17%). Data-input activity alone is therefore very low; the floor is the clock tree plus the gate-level DFF expansion, whose internal gates switch on every edge. This is consistent with, but does not separately measure, the cost of the latch expansion. This was then tested directly: a native flop (Claim 12) removes the floor and speeds Darion up by 2.2–5.1×.
* **Baseline fairness:** Verilator's default `-Os` is not a handicap: rebuilding b17 at `-O2`/`-O3` made it about 3× slower. GCC profile-guided optimization was tried (generate, run, rebuild with the profile): PGO on `-Os` changes nothing (0.94–1.00×), PGO on `-O2` gives 1.26× (b14), 1.08× (b17) and 1.14× (b19), so b19 stays at 1.6 s versus Darion's 0.8 s. Verilator's own `--prof-pgo` option only guides multithreaded scheduling and does not apply to this single-threaded comparison; multithreaded Verilator was not tried.
* **Citation fix:** the DAC 2020 paper "Efficiently Exploiting Low Activity Factors to Accelerate RTL Simulation" is by Beamer and Donofrio (ESSENT), not "Beamer, Nijssen, Pandian".

### Claim 10: Speedup over Icarus Verilog (HOLDS, misleading)
* hyp.v: Icarus 1,496 s versus `rx-sweep` 0.85 s. But on the same circuit `rx-prop` performs 25.6G evaluations against `rx-sweep`'s 129M (a 200× gap inside Darion), and Verilator is 3.5× faster than `rx-sweep`.
* The result is mostly the known advantage of glitch-free levelized evaluation over zero-delay event-driven evaluation on a deep arithmetic netlist. It is not a property of Darion specifically. State it as such, or drop it from headline claims.

### Claim 11: IPC saturation (REFUTED on real circuits)
* The 4.03–4.86 IPC figures are real measurements, but on synthetic topologies (linear chains and complete binary trees, `Benchmark/perf/Cache_data*.md`). They are not an L1 artifact: the optimized BFS engine holds IPC 4.1–4.7 and the sweep 3.8–5.9 from 100 to about 985k gates (24 MB of gate data). What makes them synthetic is the workload: every gate has one or two fan-ins, activity is a single wave, and the same input repeats each iteration.
* On real netlists IPC is lower: hyp.v shows 1.31 (`rx-prop`) and 1.50 (`rx-sweep`); the ITC99 large circuits show 2.7–3.6 for `rx-prop` (`Benchmark/master_test/ITC99.md`).
* IPC is not a performance metric in itself: `rx-oop` also reaches 4.0 IPC on 100-gate chains. It is informative as a comparison, though: `rx-oop` falls from 4.04 to 0.26 IPC as the chain grows to 985k gates, while the flat engines stay at about 4.7. Do not cite IPC as an achievement; cite cycles and time.

---

### Claim 12: Native flop evaluation removes the clock/latch activity floor (flop-cut experiment) — HOLDS
* **Status of this work.** Flop-cut is a measurement experiment, not part of Darion's planned feature set. The author intends to add macros later; the result below is evidence of what a native sequential element could buy. The experiment's engine hooks and scripts (`set_flops`, `commit_flops`, `tests/flopcut.py`, `tests/verify_flopcut.py`) have since been removed from the repository; the numbers below were measured before removal and cannot be reproduced without restoring them. A later attempt to extend it to Opencores circuits (async set, more netlists) was stopped and is not reported as verified.
* **Idea.** Darion's gate-level DFF expansion (about 10 gates per flop, wired as latches) switches on every clock edge whether or not data changes; holding the clock fixed drops measured activity from 8–10% to 0.2–1.9% (Claim 9). Flop-cut replaces each DFF IC by one state variable `S` (`Q = AND(RN, S)`, `QN = NAND(RN, S)`) and evaluates all flops at the clock edge in one native pass, `Circuit.commit_flops(rising)`: sample every D and every reset first, then update all states and propagate once. This is the usual RTL meaning of a flop.
* **Code (removed).** A circuit rewrite script, a native commit loop in `Circuit.pyx` and a verification driver. Prototype scope: all flops share one clock edge, set input tied high, no latches or gated clocks (true for every ITC99 circuit used).
* **Correctness (12 runs, 8 circuits, both stimuli): 0 mismatches.** Every primary output and every flop's state, on every vector, flop-cut `rx-prop` and `rx-sweep` against Icarus (4-state golden, 2.4M–53M bits per run) and against the gate-level Darion model. An early version had a real bug (a flop whose D or RN is driven directly by another flop's output sampled a hidden pin; this broke b18 and b22 with 2,206 and 33,456 mismatches); the two-pass rewrite fixed it, and b18/b22 are exact. The fix is why every run was repeated.
* **Speed (3,000 physical vectors, benchmark stimulus, engine time only, same vectors for every engine):**

  | Circuit | gate-level `rx-prop` | flop-cut `rx-prop` | flop-cut speedup | Verilator | flop-cut `rx-prop` vs Verilator |
  |---|---:|---:|---:|---:|---:|
  | b14 | 84.7 ms | 36.8 ms (`rx-sweep` 32.2) | 2.3× | 13.4 ms | Verilator 2.4× faster |
  | b15 | 43.3 ms | 12.3 ms | 3.5× | 20.8 ms | **Darion 1.7× faster** |
  | b17 | 148.4 ms | 28.9 ms | 5.1× | 158.1 ms | **Darion 5.5× faster** |
  | b18 | 495.0 ms | 199.3 ms | 2.5× | 798.6 ms | **Darion 4.0× faster** |
  | b19 | 833.9 ms | 241.4 ms | 3.5× | 1,831.7 ms | **Darion 7.6× faster** |
  | b20 | 122.5 ms | 51.4 ms (`rx-sweep` 43.7) | 2.4× | 33.4 ms | Verilator 1.3× faster |
  | b21 | 109.3 ms | 40.3 ms (`rx-sweep` 38.3) | 2.7× | 31.3 ms | Verilator 1.2× faster |
  | b22 | 229.4 ms | 105.3 ms (`rx-sweep` 97.5) | 2.2× | 62.2 ms | Verilator 1.5× faster |

  Flop-cut is 2.2–5.1× faster than the gate-level model on every circuit. Against Verilator it wins on the four circuits with the largest or least active netlists (b15, b17, b18, b19) and loses on b14, b20, b21 and b22 (the b14-derived, higher-activity cores). Best of `rx-prop`/`rx-sweep` is used where a small circuit prefers sweep.
* **What it does and does not show.** It confirms that the clock-tree and latch-expansion switching, not data activity, was the dominant cost, and that a native sequential element removes it. It does not make Darion faster than Verilator in general: small and high-activity designs still favor compiled code. Both engines use the same netlist and Verilator models flops behaviorally, so the comparison is like-for-like on logic; Darion's timing includes the new commit loop and the per-vector Python call overhead (about 3,000 calls), which a pure-native driver would reduce.
* **Limits.** ITC99 circuits only; one clock; random stimulus (no real workload). A preliminary run on Opencores netlists (earlier version of the code, not re-verified, not reported as a result) did not generalize: Verilator was faster on most of them (for example aes_core and des_area by roughly 7×) and flop-cut won only on tv80; the 2-state Darion model was compared against Icarus after a reset warmup, where 0.00% of reference bits were `X`.

## 4. Verification and Soundness

* **Combinational:** `tests/src/verifier.py`, all engines against random vectors.
* **Sequential:** `tests/src/verifier_iwls.py`. I reran b14 and b15 at 3,000 vectors against Icarus and Verilator: **all pass**.
* **Scope limits of the original verifier:** primary outputs only; reference `X` bits count as matches; 100 vectors by default; reset deasserted while the benchmark stimulus randomizes it. The extended verifier below addresses each of these.
* **Extended verification (`tests/verify_state.py`):** compares **every flip-flop's Q plus all primary outputs** on every vector, with Darion run in the benchmark configurations (rx-prop = BFS layout, rx-sweep = DFS layout), against Icarus (4-state golden reference) and Verilator (2-state). The netlist is rewritten to expose each flop's Q as an extra port for the references; Darion's flop IC output is read directly. Two stimuli: `bench` (all inputs and reset uniformly random) and `run` (reset deasserted, inputs toggling with probability 0.1). Results:

  | Circuit | flops | logical cycles vs Icarus | bits compared vs Icarus (per stimulus) | Darion (prop and sweep) vs Icarus |
  |---|---:|---:|---:|---|
  | b14 | 245 | 50,000 | 29.9M | **0 mismatches**, both stimuli |
  | b15 | 449 | 50,000 | 51.9M | **0 mismatches**, both stimuli |
  | b17 | 1,415 | 20,000 | 60.5M | **0 mismatches**, both stimuli |
  | b19 | 6,594 | 3,000 | 39.7M | **0 mismatches**, both stimuli |

  After the warmup (10 reset cycles then clocking) **0.00% of Icarus reference bits were `X`**, so the earlier worry that "`X` matches everything" hid errors does not apply to this protocol.
* **Verilator is the odd one out, not Darion.** Against Verilator, Darion matches on every bit except the `Q` of the `state_reg[0]` flops (b14: 1 flop; b19: the 4 `*_state_reg[0]` flops; b15 and b17: none). Icarus and Verilator disagree with *each other* on exactly those flops (for example b14, 642 of 2,000 vectors), and Darion agrees with Icarus. These flops leave `Q` unconnected in the netlist and drive their logic from `QN`. **The disagreement disappears (0 of 2,000 vectors, versus 642 of 2,000) when the flop's `QN` net is also made an observed output**, so it is a Verilator evaluation-order artifact that depends on what is observed, not a semantic difference. I did not trace the exact scheduling path inside Verilator. Report it as a reference-tool discrepancy; do not use Verilator as the sole golden reference for flop state.
* **Other suites, repo verifiers re-run at larger vector counts (rx-prop and rx-sweep against Icarus and Verilator, primary-output comparison as these verifiers define it):** ISCAS-89, 15 circuits (s27 to s38417), 20,000 vectors each: 15/15 pass, 0 failures. ISCAS-85, 11 circuits (c17 to c7552), 20,000 vectors: 11/11 pass. EPFL standard suite, 11 circuits (ctrl to arbiter), 5,000 vectors: 11/11 pass. These verifiers compare primary outputs only, not internal state.
* **Remaining limits:** internal-state comparison covers ITC99 b14, b15, b17, b18, b19, b20, b21, b22 (flop-cut runs) and b14, b15, b17, b19 (gate-level runs); b19 gate-level was compared against Icarus for 3,000 cycles only (Verilator, 10,000 cycles, with the four discrepant flops above). The EPFL large and mammoth suites and the Opencores circuits (vga_lcd etc.) were not verified in this audit. Darion is a two-state engine by construction.
* **Fuzzing (this audit):** gate-level logic agrees with an independent oracle across propagate and sweep on random DAGs (Claim 1).

---

## 5. Honest Assessment and Open Work

### What is real (in order of strength)
0. **Data-oriented design over an OOP object graph** (Claim 13): about 2.1–2.4× fewer cycles than the OOP engine on the large ITC99 circuits (17k–257k gates, PMU counters), and a gap that grows with size on synthetic chains and trees (1.3× at 100 gates to 6.6× at 280k and 21.6× at 985k, worst case), where the OOP engine's IPC collapses (4.0 to 0.26) and it mispredicts about once per gate evaluation. Repeated ITC99 counters give 1.9–2.1× fewer cycles. A standalone ablation attributes most of it to dispatch plus the branch-free rule (about 2× even with perfect prediction, 2–3× on mixed gates) and little to heap layout unless placement is scattered and exceeds L3; a switch recovers little. This is the central engineering result.
1. **Native sequential evaluation (an experiment, motivating macros) beat compiled simulation on the largest ITC99 gate-level netlists only** (Claim 12; not shown to generalize to Opencores): bit-exact against Icarus on 8 circuits, 2.2–5.1× faster than Darion's own gate-level flops, and 1.7–7.6× faster than Verilator on b15, b17, b18 and b19, with a measured mechanism (below).
2. **The mechanism is measured, not assumed.** Compiled code's footprint outgrows the instruction cache (Verilator cost per gate rises 4× at fixed structure as code grows 0.75 → 20 MB, IPC 2.0 → 0.54), while a data-driven engine's instruction footprint does not grow; and Darion's activity floor was the clock tree plus latch expansion, which a native flop removes.
3. **Non-fatal promotion of zero-delay cycles to timed simulation**, together with the timing engine (see `Timing_Report.md`).
4. **Interactive turnaround** at industrial netlist scale (practical value, modest research value).

### What is not a contribution
SIMA as an algorithm (a measured 1.1–1.7× engineering gain over a type switch, not a new idea), the field ordering inside the 24-byte struct, the decoupled UI, IPC numbers, and "mutation".

### Honest limits of the headline result
* Speed results are ITC99 only with uniformly random stimulus. The one real workload (a Z80 program on tv80, `tests/verify_state.py --workload tv80`) is verified for correctness on Darion's gate-level model (RAM check passes, 0 bus mismatches against Icarus over 5,000 cycles); the Verilator leg was dropped: a Verilator testbench running the same environment diverges from Icarus within the first instructions (half-cycle 25) even with a longer reset, while Darion matches Icarus, so its trace is not a usable reference or speed baseline. Root cause not investigated (possibly the Verilator UDP flop quirk listed as open). Small and high-activity designs (b14, b20, b21, b22) still favor Verilator by 1.2–2.4×.
* The comparison point is one compiled simulator (Verilator, default `-Os`; GCC PGO and `-O2` do not change the result). Darion is single-threaded, so single-thread Verilator is the fair comparison; other simulator classes were not compared.
* Flop-cut is an experiment only (single clock edge, no latches or gated clocks). It is not on the roadmap; macros are.
* Darion's per-gate cost also grows with size (+63% over a 32× size increase on replicated b14) and with activity; the crossover is a function of size, structure and activity, not a single threshold.

### Done in this audit
* `transfer_info` fixed (`Gate.retype`) with `test_retype_exhaustive` in `tests/integrity_test.py` (1,980 cases).
* SIMA ablation versus a `switch(type)` evaluator (`-DDARION_EVAL_SWITCH`, `tests/ablation_eval.py`): 1.1–1.7×.
* Size sweep (7 circuits), controlled replication experiment (k = 1…32), clock-floor measurement, GCC PGO check.
* Extended state verification (`tests/verify_state.py`): 0 mismatches against Icarus on b14, b15, b17, b19, for the gate-level model.
* Flop-cut experiment (since removed from the repo): 0 mismatches on 8 ITC99 circuits.
* Citations fixed or flagged in `Related_Works.md` (Beamer and Donofrio; Shiple co-authors; Edwards pages; Logisim default 1,000; Questa behavior; unverifiable Hansen entry removed).

### Still open
* Macros (planned): the flop-cut numbers are the motivation; no further flop-cut work is planned.
* Speed comparison on the real tv80 workload (Verilator testbench disagrees with Icarus and must be fixed first), other non-ITC99 netlists, and verification of the EPFL large/mammoth and multi-clock Opencores circuits.
* Root cause inside Verilator for the observation-dependent `Q` of unconnected-`Q` flops.
* Verify or remove: Digital's oscillation limit, VCS/Xcelium defaults, Wang & Maurer's DAC venue/pages, Riedel & Bruck pages, and a verified levelized-compiled-simulation reference.
* Not done by choice: fan-in guard at 255 in `Gate.setlimits` (unused in practice).
