# Master Test Unified Benchmark Report: tests/EPFL_large_parsed

**Execution Parameters:**
- **Target Suite / Path:** `tests/EPFL_large_parsed`
- **Circuits Benchmarked:** 8
- **Simulation Vectors (Phase 3):** 500 (Warmup: 10)
- **Verification Vectors (Phase 2):** 100
- **Hardware Profiler:** Linux `perf` kernel PMU counters

---

## 1. Zero-Testbench Memory Footprint (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| sin.v | 8,947 | 10.67 MB (42.0 MB peak) | N/A | 5.31 MB (13.2 MB peak) | 0.79 MB (4.5 MB peak) |
| voter.v | 27,720 | 27.15 MB (58.4 MB peak) | N/A | 17.79 MB (25.7 MB peak) | 1.20 MB (4.9 MB peak) |
| square.v | 35,687 | 36.05 MB (67.4 MB peak) | N/A | 22.63 MB (30.5 MB peak) | 1.30 MB (5.0 MB peak) |
| sqrt.v | 41,234 | 40.06 MB (71.4 MB peak) | N/A | 27.11 MB (35.0 MB peak) | 1.07 MB (4.8 MB peak) |
| multiplier.v | 50,760 | 49.69 MB (81.0 MB peak) | N/A | 33.08 MB (40.9 MB peak) | 1.31 MB (4.9 MB peak) |
| log2.v | 54,531 | 52.04 MB (83.4 MB peak) | N/A | 35.49 MB (43.3 MB peak) | 0.92 MB (4.6 MB peak) |
| mem_ctrl.v | 84,974 | 79.78 MB (111.1 MB peak) | N/A | 55.38 MB (63.2 MB peak) | 1.50 MB (5.2 MB peak) |
| div.v | 101,859 | 97.98 MB (129.4 MB peak) | N/A | 67.34 MB (75.2 MB peak) | 1.56 MB (5.3 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| sin.v | 8,947 | 17.59 ms (0.954 ms opt) | N/A | 56.43 ms | 4.09 s |
| voter.v | 27,720 | 35.93 ms (2.517 ms opt) | N/A | 181.40 ms | 5.77 s |
| square.v | 35,687 | 44.56 ms (4.722 ms opt) | N/A | 252.57 ms | 7.05 s |
| sqrt.v | 41,234 | 50.99 ms (4.732 ms opt) | N/A | 303.45 ms | 7.39 s |
| multiplier.v | 50,760 | 63.83 ms (8.064 ms opt) | N/A | 377.13 ms | 8.64 s |
| log2.v | 54,531 | 72.38 ms (10.673 ms opt) | N/A | 432.35 ms | 10.08 s |
| mem_ctrl.v | 84,974 | 97.05 ms (18.632 ms opt) | N/A | 1.19 s | 16.08 s |
| div.v | 101,859 | 154.46 ms (17.411 ms opt) | N/A | 845.22 ms | 27.68 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| sin.v | 475.06 ms | 22.63 ms | 539.94 ms | N/A | 2307.47 ms | 1.70 ms |
| voter.v | 388.27 ms | 64.16 ms | 469.10 ms | N/A | 2088.70 ms | 3.94 ms |
| square.v | 340.51 ms | 91.84 ms | 396.69 ms | N/A | 1567.47 ms | 7.65 ms |
| sqrt.v | 42.20 s | 101.63 ms | 45.57 s | N/A | 195.16 s | 4.74 ms |
| multiplier.v | 2669.32 ms | 129.80 ms | 3431.59 ms | N/A | 13.86 s | 5.34 ms |
| log2.v | 12.15 s | 140.15 ms | 15.92 s | N/A | 63.89 s | 7.51 ms |
| mem_ctrl.v | 378.04 ms | 240.04 ms | 546.01 ms | N/A | 2950.59 ms | 40.41 ms |
| div.v | 681.44 ms | 205.54 ms | 804.95 ms | N/A | 4253.52 ms | 67.31 ms |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| sin.v | 4.86x | 101.95x | 4.27x | N/A | 1.00x | 1357.28x |
| voter.v | 5.38x | 32.55x | 4.45x | N/A | 1.00x | 530.63x |
| square.v | 4.60x | 17.07x | 3.95x | N/A | 1.00x | 204.77x |
| sqrt.v | 4.63x | 1920.31x | 4.28x | N/A | 1.00x | 41134.03x |
| multiplier.v | 5.19x | 106.79x | 4.04x | N/A | 1.00x | 2596.45x |
| log2.v | 5.26x | 455.84x | 4.01x | N/A | 1.00x | 8501.80x |
| mem_ctrl.v | 7.81x | 12.29x | 5.40x | N/A | 1.00x | 73.01x |
| div.v | 6.24x | 20.69x | 5.28x | N/A | 1.00x | 63.20x |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `5.42x`
- **rx-sweep (Linear Compiled):** `77.83x`
- **rx-oop (OOP Graph):** `4.43x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `941.59x`

### Cross-Engine Comparisons

- **Reactor Sweep vs Propagate Ratio:** `14.37x` (sweep faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | IPC | Cycles | Instructions | L1 Loads | L1 Hit% | L2 Hit% | LLC Misses | Brn Miss% |
|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| sin.v | rx-prop | 1.77 | 1.28B | 2.26B | 915.09M | 91.27% | 99.20% | 634.39K | 8.11% |
| sin.v | rx-sweep (Linear) | 2.75 | 46.90M | 128.76M | 42.87M | 91.90% | 95.07% | 170.32K | 5.52% |
| sin.v | rx-oop (OOP Engine) | 1.69 | 1.47B | 2.47B | 1.11B | 90.45% | 98.56% | 1.55M | 8.91% |
| sin.v | Icarus Verilog | 2.54 | 6.32B | 16.02B | 8.84B | 95.59% | 87.92% | 47.06M | 1.57% |
| voter.v | rx-prop | 1.67 | 1.07B | 1.79B | 752.08M | 91.29% | 87.95% | 7.94M | 8.32% |
| voter.v | rx-sweep (Linear) | 3.05 | 164.33M | 502.01M | 167.15M | 92.86% | 88.64% | 1.43M | 3.49% |
| voter.v | rx-oop (OOP Engine) | 1.54 | 1.29B | 1.98B | 908.73M | 90.83% | 84.03% | 13.31M | 8.75% |
| voter.v | Icarus Verilog | 2.40 | 5.73B | 13.73B | 7.88B | 96.48% | 62.27% | 104.59M | 1.56% |
| square.v | rx-prop | 1.60 | 919.48M | 1.47B | 619.15M | 90.57% | 86.77% | 7.82M | 7.97% |
| square.v | rx-sweep (Linear) | 2.39 | 241.36M | 576.47M | 218.37M | 92.60% | 82.02% | 2.90M | 5.15% |
| square.v | rx-oop (OOP Engine) | 1.39 | 1.09B | 1.51B | 708.45M | 90.31% | 81.10% | 13.07M | 8.77% |
| square.v | Icarus Verilog | 2.17 | 4.30B | 9.36B | 5.55B | 95.82% | 56.72% | 100.44M | 1.53% |
| sqrt.v | rx-prop | 1.36 | 115.90B | 157.28B | 64.63B | 89.57% | 49.14% | 3.43B | 6.47% |
| sqrt.v | rx-sweep (Linear) | 3.04 | 270.20M | 822.41M | 280.17M | 92.90% | 78.16% | 4.39M | 2.67% |
| sqrt.v | rx-oop (OOP Engine) | 1.17 | 125.11B | 145.95B | 65.00B | 89.20% | 34.02% | 4.63B | 7.16% |
| sqrt.v | Icarus Verilog | 1.80 | 534.82B | 962.89B | 605.63B | 95.64% | 21.91% | 20.64B | 1.47% |
| multiplier.v | rx-prop | 1.52 | 7.30B | 11.11B | 4.75B | 90.54% | 78.85% | 95.19M | 8.14% |
| multiplier.v | rx-sweep (Linear) | 2.73 | 340.41M | 928.77M | 329.01M | 92.60% | 78.48% | 5.24M | 3.78% |
| multiplier.v | rx-oop (OOP Engine) | 1.27 | 9.43B | 11.98B | 5.67B | 90.30% | 64.04% | 197.74M | 8.82% |
| multiplier.v | Icarus Verilog | 1.83 | 38.02B | 69.55B | 44.02B | 96.18% | 28.18% | 1.21B | 1.56% |
| log2.v | rx-prop | 1.45 | 33.33B | 48.41B | 20.44B | 90.14% | 62.62% | 754.62M | 7.24% |
| log2.v | rx-sweep (Linear) | 2.58 | 359.60M | 928.00M | 326.90M | 92.85% | 80.41% | 4.77M | 4.65% |
| log2.v | rx-oop (OOP Engine) | 1.17 | 43.71B | 51.30B | 24.08B | 89.70% | 43.39% | 1.40B | 8.26% |
| log2.v | Icarus Verilog | 1.83 | 175.36B | 320.51B | 202.36B | 96.04% | 22.27% | 6.23B | 1.47% |
| mem_ctrl.v | rx-prop | 1.50 | 1.03B | 1.54B | 624.17M | 89.27% | 47.76% | 35.01M | 5.11% |
| mem_ctrl.v | rx-sweep (Linear) | 2.18 | 658.33M | 1.44B | 550.28M | 92.24% | 76.40% | 10.10M | 5.40% |
| mem_ctrl.v | rx-oop (OOP Engine) | 1.24 | 1.49B | 1.85B | 821.70M | 89.13% | 38.52% | 54.86M | 5.77% |
| mem_ctrl.v | Icarus Verilog | 1.82 | 8.10B | 14.78B | 8.40B | 95.89% | 20.12% | 275.92M | 0.98% |
| div.v | rx-prop | 1.64 | 1.87B | 3.06B | 1.18B | 89.84% | 55.98% | 52.91M | 4.40% |
| div.v | rx-sweep (Linear) | 3.42 | 541.33M | 1.85B | 584.58M | 92.20% | 82.87% | 7.86M | 1.83% |
| div.v | rx-oop (OOP Engine) | 1.35 | 2.20B | 2.98B | 1.23B | 88.70% | 49.27% | 70.59M | 4.86% |
| div.v | Icarus Verilog | 1.84 | 11.64B | 21.40B | 11.54B | 95.31% | 39.96% | 320.92M | 0.81% |
