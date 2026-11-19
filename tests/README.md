# Tests and benchmarks

Run everything from the repository root with the system `python3` and `PYTHONPATH=editor/tools` (several scripts import the engine from `reactor/`). Build the engine first with `bash scripts/build.sh` (`--reactor-oop` for the OOP comparison engine). Install and build details for the project itself are in the top-level README.

## What the benchmarks need besides Python

| Need | Why | Setup |
|---|---|---|
| `perf` | PMU counters (`src/perf.py`, `cache_perf.py`, `master_test.py`) | `sudo sysctl -w kernel.perf_event_paranoid=2` or lower (user-mode counters are enough) |
| Icarus Verilog (`iverilog`, `vvp`) | reference simulator and correctness oracle | system package |
| Verilator | reference simulator; builds use a nonblocking copy of the cell library (`iwls_sequential_harness.verilator_gsclib`) | system package |
| numpy, matplotlib, orjson, psutil | plots, JSON, memory measurement | system packages |

Pin every timing run to one core (`taskset -c 2`), run nothing else at the same time, and report the median of repeats.

## Tools

| Script | Use |
|---|---|
| `master_test.py <suite dir>` | the full pipeline per suite: memory, load time, wall-clock of rx-prop / rx-sweep / rx-oop / Icarus / Verilator, PMU counters. `run_all_test.sh` lists the exact invocations. |
| `src/benchmark.py`, `benchmark_89.py`, `benchmark_iwls.py` | per-engine runners: combinational (ISCAS85, EPFL), ISCAS89, IWLS/ITC99/OpenCores/Faraday |
| `src/load.py` | memory footprint and load time |
| `src/perf.py` | PMU counters for rx-prop and rx-oop (one call is one run, loop for repeats) |
| `src/verifier.py`, `verifier_89.py`, `verifier_iwls.py` | output verification against Icarus and Verilator |
| `verify_state.py <circuit>` | every flop and output against Icarus/Verilator over long runs (`--all-clocks`, `--gls-flops`, `--workload tv80`, `--case-study`) |
| `integrity_test.py` | functional and stress suite (28,265 tests, including macro flops, connect and edits after `optimize()`) |
| `test_timing.py --suite topologies\|extended\|bench` (with `timing_lib.py`) | delay-model suite |
| `ablation_eval.py` | SIMA against `switch(type)`, UI-queue cost, API latency, netlist export, `--layouts` (mode against sort order) |
| `ablation_layout.cpp` | standalone C++ layout harness (variants a to g; options in its header) |
| `cache_test.py`, `cache_perf.py` | synthetic chain and tree sweeps with PMU counters; `cache_perf.py --from-json` re-plots a stored result |
| `geometry.py` | topology statistics |
| `CLI.py` | interactive terminal menu |
| `src/iscas89_sequential_harness.py`, `iwls_sequential_harness.py` | reference testbench generators |
| `../scripts/{iscas,iwls,epfl}_parser.py` | netlist to Darion JSON (benchmark tooling only) |

## Environment switches

| Variable | Effect |
|---|---|
| `REACTOR_DIR` | run `integrity_test.py`, `test_timing.py`, `verify_state.py`, `cache_test.py` against another engine build (a scratch copy) |
| `NETLIST_ROOT` | root of the suite directories for `ablation_eval.py` and `verify_state.py` (for example a copy holding other netlists) |
| `DARION_GLS_FLOPS=1` | Icarus and Verilator compile the cell library with the same gate-level flops Darion simulates |

## Where results go

Generated reports land in `tests/test_result/` (git-ignored). Reports worth keeping are copied to `Benchmark/` (`master_test.md`, `9700X.md`, `5675U.md`, `perf/Cache_data.md`); the numbers behind each claim are in `research/Claims.md`.
