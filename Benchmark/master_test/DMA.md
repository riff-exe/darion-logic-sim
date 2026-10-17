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
| DMA.v | 31,920 | 55.78 MB (84.3 MB peak) | N/A | 103.19 MB (111.1 MB peak) | 1.31 MB (5.0 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| DMA.v | 31,920 | 54.31 ms (10.078 ms opt) | N/A | 491.09 ms | 20.77 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| DMA.v | 5177.11 ms | 6317.11 ms | 10.26 s | N/A | 28.17 s | 3337.03 ms |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| DMA.v | 5.44x | 4.46x | 2.75x | N/A | 1.00x | 8.44x |

### Total Gate Evaluations

| Circuit | Gates | rx-prop Evals | rx-sweep Evals | rx-oop Evals | Pure Python Evals |
|:---|---:|---:|---:|---:|---:|
| DMA.v | 31,920 | 2,055,140,384 | 2,049,004,779 | 2,057,788,417 | N/A |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `5.44x`
- **rx-sweep (Linear Compiled):** `4.46x`
- **rx-oop (OOP Graph):** `2.75x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `8.44x`

### Gate Evaluation Highlights

- **Reactor Sweep vs Propagate Total Evaluations Ratio:** `1.00x` (propagate performed more evaluations)

### Cross-Engine Comparisons

- **Reactor Sweep vs Propagate Ratio:** `0.82x` (propagate faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | Instructions | Cycles | IPC | L1 Loads | L1 Misses | L2 Loads | L2 Misses | L3 Loads | DRAM Loads | Branches | Branch Misses |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| DMA.v | rx-prop | 62.62B | 19.46B | 3.22 | 25.13B | 2.61B | 2.61B | 388.63M | 1.47B | 69.78M | 6.19B | 35.89M |
| DMA.v | rx-sweep (Linear) | 82.86B | 23.55B | 3.52 | 26.30B | 3.64B | 3.64B | 411.88M | 2.65B | 68.44M | 17.76B | 131.29M |
| DMA.v | rx-oop (OOP Engine) | 70.52B | 37.84B | 1.86 | 42.50B | 4.57B | 4.57B | 1.41B | 4.27B | 64.25M | 8.89B | 84.38M |
| DMA.v | Icarus Verilog | 373.75B | 105.73B | 3.53 | 171.47B | 4.60B | 4.60B | 2.66B | 4.51B | 4.82M | 71.21B | 229.24M |
| DMA.v | Verilator C++ | 19.34B | 11.92B | 1.62 | 9.16B | 15.53M | 15.53M | 752.21M | 755.09M | 213.18K | 1.26B | 8.58M |
