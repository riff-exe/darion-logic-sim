# Master Test Unified Benchmark Report: tests/IWLS2005/faraday

**Execution Parameters:**
- **Target Suite / Path:** `tests/IWLS2005/faraday`
- **Circuits Benchmarked:** 1
- **Simulation Vectors (Phase 3):** 50,000 (Warmup: 10)
- **Verification Vectors (Phase 2):** 100
- **Hardware Profiler:** Linux `perf` kernel PMU counters
- **Note (2026-10-22):** re-run after the Verilator library fix: Verilator now compiles `iwls_sequential_harness.verilator_gsclib()` (the cell library with its sequential UDPs as nonblocking modules), because Verilator 5.052 lowers the original UDP flops to blocking assignments, which is order-dependent and slow. Icarus uses the original library; Darion simulates every flop as the 10-gate NAND master-slave of `tests/src/DFFSR.json`, so the flop models differ between the three tools (not a same-netlist comparison). The previous report (blocking-UDP Verilator) is in git history.

---

## 1. Zero-Testbench Memory Footprint (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| DMA.v | 31,920 | 56.68 MB (85.3 MB peak) | N/A | 103.10 MB (111.0 MB peak) | 1.21 MB (4.9 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| DMA.v | 31,920 | 49.49 ms (9.369 ms opt) | N/A | 505.91 ms | 12.88 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| DMA.v | 5179.56 ms | 5506.47 ms | 9488.04 ms | N/A | 28.15 s | 516.93 ms |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| DMA.v | 5.44x | 5.11x | 2.97x | N/A | 1.00x | 54.46x |

### Total Gate Evaluations

| Circuit | Gates | rx-prop Evals | rx-sweep Evals | rx-oop Evals | Pure Python Evals |
|:---|---:|---:|---:|---:|---:|
| DMA.v | 31,920 | 2,055,265,005 | 2,046,739,752 | 2,057,788,417 | N/A |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `5.44x`
- **rx-sweep (Linear Compiled):** `5.11x`
- **rx-oop (OOP Graph):** `2.97x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `54.46x`

### Gate Evaluation Highlights

- **Reactor Sweep vs Propagate Total Evaluations Ratio:** `1.00x` (propagate performed more evaluations)

### Cross-Engine Comparisons

- **Reactor Sweep vs Propagate Ratio:** `0.94x` (propagate faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | Instructions | Cycles | IPC | L1 Loads | L1 Misses | L2 Loads | L2 Misses | L3 Loads | DRAM Loads | Branches | Branch Misses |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| DMA.v | rx-prop | 63.33B | 19.47B | 3.25 | 25.57B | 2.41B | 2.41B | 389.76M | 1.07B | 69.45M | 6.46B | 36.95M |
| DMA.v | rx-sweep (Linear) | 83.69B | 20.66B | 4.05 | 26.78B | 3.62B | 3.62B | 384.80M | 2.35B | 68.48M | 18.02B | 84.63M |
| DMA.v | rx-oop (OOP Engine) | 71.13B | 34.98B | 2.03 | 45.49B | 4.24B | 4.24B | 1.30B | 3.99B | 65.35M | 8.88B | 81.63M |
| DMA.v | Icarus Verilog | 373.71B | 105.57B | 3.54 | 171.84B | 4.69B | 4.69B | 2.63B | 4.57B | 23.69M | 71.17B | 230.71M |
| DMA.v | Verilator C++ | 3.40B | 1.86B | 1.83 | 1.95B | 302.85K | 302.85K | 12.59K | 148.20K | 128.38K | 17.60M | 152.48K |
