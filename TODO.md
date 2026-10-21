# TODO

State as of 2026-10-21. Findings live in `research/Claims.md` (Claim 13 and "Still open"); this file is only the task list. The laptop (Ryzen 5 PRO 5675U) work is finished and committed; its data is in `Benchmark/5675U/`. Do not commit unless the user asks.

## Done (do not redo)
* [x] Claims audit, gate mutation fix (`Gate.retype`), SIMA `switch` ablation, timing suites, state verification (0 mismatches vs Icarus).
* [x] Fan-in guard (committed as `3a3c370`).
* [x] Flop-cut experiment run, documented as Claim 12, code removed.
* [x] OOP versus data-oriented evidence collected from existing benchmarks and written up as Claim 13: ITC99 PMU counters for b15/b17/b18/b19 (`Benchmark/master_test/ITC99.md`, 2.1-2.4x fewer cycles), 67-size chain and tree sweeps to about 985k gates (`Benchmark/perf/Cache_data*.md`).
* [x] ESSENT/GSIM baselines dropped from scope.
* [x] Laptop (second-platform) work, 2026-10-21: full-engine PMU repeats, ablation harness on real and synthetic netlists, ISCAS85 and OpenCores runs, and reruns for struct size, L3 cliff, predictor memorization and SMT noise (quiet run with the sibling offline). Results in Claim 13, data in `Benchmark/5675U/`.

## Open, in order

### 1. Documentation fixes (light, no CPU)
* [x] `README.md`: replace "Very accurate to real-life circuit behavior" with wording that matches the timing report ("exact for its delay model, not calibrated to a cell library").
* [x] `tests/benchmark_documentation.md`: scope "95-98% of the circuit is idle" and "Reactor is 1.6x to 2.03x faster than Verilator" to the Cadence-UDP netlists they came from; note that the IWLS runs in the claims doc have Verilator winning 17 of 21. Mark the UDP-trigger / branch-miss explanation of the Verilator slowdown as unchecked next to the measured code-footprint and IPC mechanism.

### 2. Consolidate `tests/` (merge, do not delete; keep the old files until outputs match)
* [x] `workload_tv80.py` into `verify_state.py` as a `--workload tv80` mode (drop the duplicated loader).
* [x] `test_timing_verification.py` + `test_timing_extended.py` + `bench_timed_vs_icarus.py` into one `test_timing.py` with `--suite topologies|extended|bench`; `timing_lib.py` stays as helper. Verify old and new outputs match side by side.
* [x] `test_retype.py` into `tests/integrity_test.py` next to its existing `test_transfer_info`.
* [x] `ablation_eval.py`: keep standalone, next to `cache_perf.py` / `pmu_harness.py`.
* [x] Update filenames in the claims doc, `research/Timing_Report.md` and docstrings afterwards.
* [x] The tv80 Verilator testbench disagrees with Icarus from half-cycle 25 (Darion matches Icarus), also with a longer reset. Dropped the Verilator leg; root cause not investigated.

### 3. OOP versus data-oriented: remaining experiments (CPU-exclusive, run one at a time)
* [x] Standalone C++ ablation harness (outside `reactor/`) with four variants: (a) heap objects + virtual `compute()` (as `reactor_oop`), (b) the same objects packed in an arena, still virtual, (c) flat 24-byte structs with `switch(type)`, (d) flat structs with the SIMA rule. Same algorithm and traversal; check identical evaluation counts and final-state fingerprints. Step a-to-b is layout only, b-to-c is the vtable only, c-to-d is the evaluation rule.
* [x] Repeats: 7-10 interleaved runs, pinned core, median and spread, for the harness over a size sweep and for the ITC99 `rx-prop` vs `rx-oop` counters on b15/b17/b18/b19. First check whether `tests/src/perf.py` already averages iterations.
* [x] Predictor-memorization test (optional): randomize the input each iteration in the chain benchmark and see whether the OOP misprediction onset at about 600 gates moves.
* [x] Optional: 24- versus 32-byte struct (done in the harness, variants e and g).
* [x] Write the results into Claim 13, separating the vtable and layout parts; if they interact, say so.

### 4. Before writing the paper
* [x] Scope stated: engine and API only, no rendering (Paper_Notes section 1).
* [x] Second-machine run sheet written (Paper_Notes 6b). **The author runs it** on a second CPU and brings back the logs. Run on a Ryzen 5 PRO 5675U laptop 2026-10-21 (plus reruns for struct size, predictor and SMT noise), results in Claim 13; ARM and Intel still not covered.
* [x] Maurer patents read in full; SIMA-versus-Maurer comparison in `research/Related_Works.md` 0.5. Maurer's ICCAD 2000 paper read in full too (audit 0.5); his 1994 Inversion paper is the primary citation for counting.
* [x] Bug-localisation case study on tv80 (`tests/verify_state.py --case-study`), results in the claims doc (Claim 7).
* [x] Oscillation test against Digital (ring oscillator, NAND latch), results in Paper_Notes 3e.
* [x] Paper outline (Paper_Notes section 8).

### 4b. Needs other hardware (found by the laptop work)
* [ ] Run the Paper_Notes 6b sheet on an ARM machine and an Intel machine; only one older x86 (Zen 3) is covered.
* [ ] Repeat the Zen 5 struct-size and L3-cliff comparison across several processes (the current Zen 5 figures are single calls and the per-process slow mode may affect them).
* [ ] Find the cause of the per-process fast/slow mode (b17 `rx-prop` +35% cycles at identical instructions with the SMT sibling offline; harness slow mode at 500k+ gates). Hypothesis: page or cache-set placement of the gate array. Not tested.
* [ ] Explain why `rx-prop` loses ground relative to Icarus on ISCAS85 on the laptop while `rx-sweep` gains (sweep retires about half the instructions of prop; the machine-specific part is unexplained), and why the full-engine ratio sits above the harness ratio by more than 0.25 there.

### 5. Planned by the author (engine change, author implements)
* [ ] Replace the name heuristic for sequential ICs (`dff`/`flip`/`latch`/`tlat` in the IC name, `reactor/IC.pyx`, which sets `FLAG_BOUNDARY` on output pins) with an optional flip-flop flag in the IC's JSON; cut at the IC boundary when set. Afterwards, re-run `tests/verify_state.py b15` (rx-sweep) and the integrity tests.

## Parked
* Unverified citations (Digital simulator oscillation limit, VCS/Xcelium defaults, Wang and Maurer pages, Riedel pages, LCS reference); only matters for a paper.
* Delay calibration to a cell library (Tier 1: fit per-type delays, check against OpenSTA/SDF), EPFL large/mammoth and multi-clock Opencores verification, Verilator flop-quirk root cause.
