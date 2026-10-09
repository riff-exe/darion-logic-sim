# Master Test Unified Benchmark Report: tests/IWLS2005/faraday

**Execution Parameters:**
- **Target Suite / Path:** `tests/IWLS2005/faraday`
- **Circuits Benchmarked:** 1
- **Simulation Vectors (Phase 3):** 50,000 (Warmup: 10)
- **Verification Vectors (Phase 2):** 100
- **Hardware Profiler:** Linux `perf` kernel PMU counters

---

## 1. Zero-Testbench Memory Footprint (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| DMA.v | 31,920 | 55.73 MB (84.5 MB peak) | N/A | 103.22 MB (111.1 MB peak) | 1.42 MB (5.1 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| DMA.v | 31,920 | 48.30 ms (10.734 ms opt) | N/A | 496.70 ms | 21.17 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| DMA.v | 6168.55 ms | 5971.54 ms | 9932.17 ms | N/A | 28.39 s | 3425.52 ms |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| DMA.v | 4.60x | 4.75x | 2.86x | N/A | 1.00x | 8.29x |

### Total Gate Evaluations

| Circuit | Gates | rx-prop Evals | rx-sweep Evals | rx-oop Evals | Pure Python Evals |
|:---|---:|---:|---:|---:|---:|
| DMA.v | 31,920 | 2,055,140,384 | 2,049,004,779 | 2,057,788,417 | N/A |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `4.60x`
- **rx-sweep (Linear Compiled):** `4.75x`
- **rx-oop (OOP Graph):** `2.86x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `8.29x`

### Gate Evaluation Highlights

- **Reactor Sweep vs Propagate Total Evaluations Ratio:** `1.00x` (propagate performed more evaluations)

### Cross-Engine Comparisons

- **Reactor Sweep vs Propagate Ratio:** `1.03x` (sweep faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | Instructions | Cycles | IPC | L1 Loads | L1 Misses | L2 Loads | L2 Misses | L3 Loads | DRAM Loads | Branches | Branch Misses |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| DMA.v | rx-prop | 65.96B | 23.06B | 2.86 | 25.47B | 2.62B | 2.62B | 370.82M | 1.44B | 70.11M | 6.46B | 34.69M |
| DMA.v | rx-sweep (Linear) | 86.18B | 22.33B | 3.86 | 26.76B | 3.64B | 3.64B | 457.03M | 2.69B | 68.60M | 18.01B | 116.55M |
| DMA.v | rx-oop (OOP Engine) | 70.50B | 36.61B | 1.93 | 41.39B | 4.41B | 4.41B | 1.44B | 4.52B | 64.80M | 8.89B | 79.25M |
| DMA.v | Icarus Verilog | 373.69B | 106.46B | 3.51 | 171.24B | 4.59B | 4.59B | 2.61B | 4.50B | 10.74M | 71.21B | 221.04M |
| DMA.v | Verilator C++ | 19.35B | 12.23B | 1.58 | 9.15B | 10.56M | 10.56M | 742.72M | 745.69M | 209.71K | 1.27B | 6.78M |
