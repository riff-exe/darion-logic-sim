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
| sin.v | 8,947 | 8.32 MB (36.2 MB peak) | N/A | 5.40 MB (13.2 MB peak) | 0.87 MB (4.5 MB peak) |
| voter.v | 27,720 | 28.47 MB (56.2 MB peak) | N/A | 17.81 MB (25.7 MB peak) | 1.15 MB (4.9 MB peak) |
| square.v | 35,687 | 34.35 MB (62.2 MB peak) | N/A | 22.56 MB (30.4 MB peak) | 1.23 MB (4.9 MB peak) |
| sqrt.v | 41,234 | 37.52 MB (65.5 MB peak) | N/A | 27.04 MB (35.0 MB peak) | 1.08 MB (4.8 MB peak) |
| multiplier.v | 50,760 | 47.06 MB (74.9 MB peak) | N/A | 33.05 MB (40.9 MB peak) | 1.24 MB (4.9 MB peak) |
| log2.v | 54,531 | 52.49 MB (80.4 MB peak) | N/A | 35.41 MB (43.3 MB peak) | 1.06 MB (4.8 MB peak) |
| mem_ctrl.v | 84,974 | 77.56 MB (105.4 MB peak) | N/A | 55.38 MB (63.3 MB peak) | 1.55 MB (5.3 MB peak) |
| div.v | 101,859 | 95.70 MB (123.6 MB peak) | N/A | 67.35 MB (75.2 MB peak) | 1.60 MB (5.3 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| sin.v | 8,947 | 6.34 ms (0.704 ms opt) | N/A | 40.05 ms | 2.89 s |
| voter.v | 27,720 | 18.95 ms (2.044 ms opt) | N/A | 133.07 ms | 4.41 s |
| square.v | 35,687 | 24.76 ms (3.924 ms opt) | N/A | 178.17 ms | 5.41 s |
| sqrt.v | 41,234 | 29.20 ms (3.710 ms opt) | N/A | 212.38 ms | 5.69 s |
| multiplier.v | 50,760 | 37.53 ms (7.194 ms opt) | N/A | 269.43 ms | 6.63 s |
| log2.v | 54,531 | 40.13 ms (8.849 ms opt) | N/A | 302.69 ms | 7.45 s |
| mem_ctrl.v | 84,974 | 66.25 ms (18.053 ms opt) | N/A | 902.39 ms | 13.02 s |
| div.v | 101,859 | 104.85 ms (15.521 ms opt) | N/A | 621.58 ms | 21.18 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| sin.v | 181.22 ms | 14.77 ms | 489.69 ms | N/A | 1585.27 ms | 1.13 ms |
| voter.v | 157.13 ms | 40.22 ms | 401.86 ms | N/A | 1420.59 ms | 2.83 ms |
| square.v | 135.95 ms | 59.85 ms | 335.11 ms | N/A | 1068.62 ms | 5.21 ms |
| sqrt.v | 16.76 s | 68.72 ms | 33.94 s | N/A | 130.88 s | 3.36 ms |
| multiplier.v | 1003.86 ms | 76.27 ms | 2750.85 ms | N/A | 9108.34 ms | 3.57 ms |
| log2.v | 4677.60 ms | 86.53 ms | 12.36 s | N/A | 42.98 s | 5.30 ms |
| mem_ctrl.v | 170.71 ms | 158.85 ms | 406.82 ms | N/A | 1848.45 ms | 24.46 ms |
| div.v | 312.37 ms | 113.86 ms | 572.58 ms | N/A | 2662.85 ms | 44.91 ms |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| sin.v | 8.75x | 107.35x | 3.24x | N/A | 1.00x | 1397.02x |
| voter.v | 9.04x | 35.32x | 3.54x | N/A | 1.00x | 502.42x |
| square.v | 7.86x | 17.86x | 3.19x | N/A | 1.00x | 205.04x |
| sqrt.v | 7.81x | 1904.65x | 3.86x | N/A | 1.00x | 38919.10x |
| multiplier.v | 9.07x | 119.42x | 3.31x | N/A | 1.00x | 2548.97x |
| log2.v | 9.19x | 496.73x | 3.48x | N/A | 1.00x | 8116.10x |
| mem_ctrl.v | 10.83x | 11.64x | 4.54x | N/A | 1.00x | 75.58x |
| div.v | 8.52x | 23.39x | 4.65x | N/A | 1.00x | 59.30x |

### Total Gate Evaluations

| Circuit | Gates | rx-prop Evals | rx-sweep Evals | rx-oop Evals | Pure Python Evals |
|:---|---:|---:|---:|---:|---:|
| sin.v | 8,947 | 49,861,993 | 2,500,692 | 53,215,082 | N/A |
| voter.v | 27,720 | 39,634,421 | 8,096,431 | 42,507,804 | N/A |
| square.v | 35,687 | 31,161,785 | 10,001,625 | 31,956,737 | N/A |
| sqrt.v | 41,234 | 3,391,656,561 | 14,436,886 | 3,172,089,918 | N/A |
| multiplier.v | 50,760 | 241,547,037 | 16,050,498 | 254,265,116 | N/A |
| log2.v | 54,531 | 1,045,537,924 | 15,721,187 | 1,104,142,382 | N/A |
| mem_ctrl.v | 84,974 | 34,129,877 | 23,859,879 | 39,409,969 | N/A |
| div.v | 101,859 | 63,202,150 | 30,616,061 | 63,102,026 | N/A |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `8.84x`
- **rx-sweep (Linear Compiled):** `82.19x`
- **rx-oop (OOP Graph):** `3.69x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `921.36x`

### Gate Evaluation Highlights

- **Reactor Sweep vs Propagate Total Evaluations Ratio:** `0.09x` (propagate performed more evaluations)

### Cross-Engine Comparisons

- **Reactor Sweep vs Propagate Ratio:** `9.29x` (sweep faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | Instructions | Cycles | IPC | L1 Loads | L1 Misses | L2 Loads | L2 Misses | L3 Loads | DRAM Loads | Branches | Branch Misses |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| sin.v | rx-prop | 1.59B | 640.80M | 2.47 | 657.97M | 66.35M | 66.35M | 37.77K | 81.86K | 5.80K | 157.14M | 9.18M |
| sin.v | rx-sweep (Linear) | 58.01M | 40.35M | 1.44 | 37.27M | 2.65M | 2.65M | 864.00 | 7.36K | 727.00 | 14.80M | 1.05M |
| sin.v | rx-oop (OOP Engine) | 1.98B | 1.74B | 1.14 | 1.63B | 97.60M | 97.60M | 755.57K | 1.35M | 17.30K | 238.66M | 23.85M |
| sin.v | Icarus Verilog | 14.28B | 5.70B | 2.50 | 7.99B | 347.24M | 347.24M | 45.95M | 56.41M | 7.83K | 2.86B | 46.18M |
| sin.v | Verilator C++ | 9.01K | 66.58K | 0.14 | 3.24K | 377.00 | 377.00 | 0.00 | 0.00 | 0.00 | 3.60K | 223.00 |
| voter.v | rx-prop | 1.25B | 552.19M | 2.27 | 540.21M | 56.60M | 56.60M | 5.43M | 8.52M | 7.84K | 126.91M | 8.36M |
| voter.v | rx-sweep (Linear) | 272.58M | 139.36M | 1.96 | 131.60M | 10.15M | 10.15M | 869.90K | 4.98M | 19.04K | 56.44M | 2.67M |
| voter.v | rx-oop (OOP Engine) | 1.59B | 1.45B | 1.10 | 1.32B | 75.84M | 75.84M | 10.62M | 16.03M | 65.63K | 193.43M | 19.26M |
| voter.v | Icarus Verilog | 12.21B | 5.11B | 2.39 | 7.09B | 247.05M | 247.05M | 92.37M | 128.36M | 40.37K | 2.43B | 38.98M |
| voter.v | Verilator C++ | 6.67M | 4.91M | 1.36 | 5.97M | 3.27K | 3.27K | 983.00 | 983.00 | 0.00 | 519.85K | 38.27K |
| square.v | rx-prop | 992.28M | 474.08M | 2.09 | 412.83M | 48.22M | 48.22M | 6.56M | 10.80M | 7.78K | 99.11M | 5.59M |
| square.v | rx-sweep (Linear) | 323.40M | 201.50M | 1.60 | 162.94M | 12.15M | 12.15M | 1.66M | 8.34M | 2.22K | 65.94M | 4.32M |
| square.v | rx-oop (OOP Engine) | 1.20B | 1.19B | 1.01 | 1.05B | 65.42M | 65.42M | 11.11M | 18.24M | 55.79K | 145.77M | 14.21M |
| square.v | Icarus Verilog | 8.31B | 3.83B | 2.17 | 5.04B | 206.22M | 206.22M | 90.45M | 115.22M | 59.27K | 1.66B | 26.30M |
| square.v | Verilator C++ | 9.25M | 10.66M | 0.87 | 21.25M | 714.00 | 714.00 | 2.21K | 2.21K | 95.00 | 3.34M | 120.81K |
| sqrt.v | rx-prop | 107.78B | 60.16B | 1.79 | 43.69B | 5.74B | 5.74B | 1.96B | 3.11B | 160.23K | 10.51B | 521.68M |
| sqrt.v | rx-sweep (Linear) | 446.51M | 236.41M | 1.89 | 223.50M | 14.36M | 14.36M | 2.57M | 11.66M | 4.56K | 87.28M | 4.13M |
| sqrt.v | rx-oop (OOP Engine) | 116.66B | 121.86B | 0.96 | 98.61B | 6.83B | 6.83B | 4.14B | 6.02B | 802.28K | 14.05B | 1.13B |
| sqrt.v | Icarus Verilog | 856.16B | 469.93B | 1.82 | 550.37B | 23.41B | 23.41B | 18.55B | 25.12B | 4.18M | 171.83B | 2.59B |
| sqrt.v | Verilator C++ | 4.74M | 10.31M | 0.46 | 12.28M | 2.78K | 2.78K | 811.00 | 1.85K | 0.00 | 199.85K | 14.11K |
| multiplier.v | rx-prop | 7.87B | 3.60B | 2.18 | 3.25B | 373.06M | 373.06M | 39.03M | 59.29M | 18.12K | 788.84M | 45.77M |
| multiplier.v | rx-sweep (Linear) | 519.27M | 266.77M | 1.95 | 235.52M | 18.29M | 18.29M | 3.68M | 15.50M | 2.81K | 101.52M | 4.60M |
| multiplier.v | rx-oop (OOP Engine) | 9.66B | 9.88B | 0.98 | 8.44B | 513.29M | 513.29M | 167.73M | 244.98M | 191.80K | 1.17B | 115.17M |
| multiplier.v | Icarus Verilog | 61.83B | 32.72B | 1.89 | 39.81B | 1.50B | 1.50B | 1.08B | 1.46B | 676.53K | 12.37B | 198.25M |
| multiplier.v | Verilator C++ | 13.22M | 11.92M | 1.11 | 22.62M | 876.00 | 876.00 | 647.00 | 1.91K | 0.00 | 5.38M | 25.98K |
| log2.v | rx-prop | 33.50B | 16.81B | 1.99 | 13.78B | 1.70B | 1.70B | 464.58M | 753.29M | 61.87K | 3.32B | 171.73M |
| log2.v | rx-sweep (Linear) | 515.94M | 298.41M | 1.73 | 249.62M | 17.78M | 17.78M | 3.32M | 15.78M | 4.14K | 102.26M | 5.83M |
| log2.v | rx-oop (OOP Engine) | 41.27B | 44.35B | 0.93 | 36.65B | 2.28B | 2.28B | 1.17B | 1.70B | 424.37K | 4.98B | 462.20M |
| log2.v | Icarus Verilog | 285.00B | 154.42B | 1.85 | 181.56B | 7.10B | 7.10B | 5.57B | 7.23B | 1.88M | 57.03B | 855.89M |
| log2.v | Verilator C++ | 9.70M | 8.03M | 1.21 | 20.64M | 2.30K | 2.30K | 585.00 | 1.90K | 25.00 | 82.71K | 5.44K |
| mem_ctrl.v | rx-prop | 1.11B | 613.57M | 1.81 | 444.72M | 59.30M | 59.30M | 25.51M | 46.30M | 41.58K | 109.96M | 3.65M |
| mem_ctrl.v | rx-sweep (Linear) | 818.71M | 565.94M | 1.45 | 425.95M | 33.26M | 33.26M | 10.13M | 34.25M | 33.97K | 163.72M | 11.37M |
| mem_ctrl.v | rx-oop (OOP Engine) | 1.49B | 1.46B | 1.02 | 1.22B | 84.88M | 84.88M | 51.22M | 76.35M | 110.47K | 181.19M | 11.78M |
| mem_ctrl.v | Icarus Verilog | 13.08B | 6.62B | 1.98 | 7.69B | 306.64M | 306.64M | 247.68M | 323.43M | 2.07M | 2.60B | 25.99M |
| mem_ctrl.v | Verilator C++ | 87.15M | 73.10M | 1.19 | 45.89M | 146.21K | 146.21K | 5.95M | 5.95M | 1.56K | 6.53M | 130.79K |
| div.v | rx-prop | 2.04B | 1.11B | 1.85 | 821.66M | 107.18M | 107.18M | 45.17M | 65.29M | 8.30K | 207.34M | 6.84M |
| div.v | rx-sweep (Linear) | 1.03B | 396.96M | 2.59 | 421.21M | 33.41M | 33.41M | 6.17M | 33.20M | 6.49K | 201.42M | 5.29M |
| div.v | rx-oop (OOP Engine) | 2.38B | 2.03B | 1.17 | 1.74B | 134.51M | 134.51M | 66.31M | 99.14M | 123.39K | 288.26M | 14.58M |
| div.v | Icarus Verilog | 19.04B | 9.54B | 2.00 | 10.34B | 479.85M | 479.85M | 288.20M | 374.58M | 10.29M | 3.81B | 30.19M |
| div.v | Verilator C++ | 54.91M | 144.09M | 0.38 | 41.82M | 53.84K | 53.84K | 1.14M | 1.14M | 1.45K | 10.53M | 16.57K |
