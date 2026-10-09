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
| sin.v | 8,947 | 8.56 MB (36.1 MB peak) | N/A | 5.38 MB (13.2 MB peak) | 0.80 MB (4.5 MB peak) |
| voter.v | 27,720 | 26.30 MB (53.8 MB peak) | N/A | 17.91 MB (25.7 MB peak) | 1.16 MB (4.9 MB peak) |
| square.v | 35,687 | 34.01 MB (61.6 MB peak) | N/A | 22.68 MB (30.6 MB peak) | 1.27 MB (5.0 MB peak) |
| sqrt.v | 41,234 | 37.84 MB (65.4 MB peak) | N/A | 27.05 MB (34.9 MB peak) | 1.01 MB (4.7 MB peak) |
| multiplier.v | 50,760 | 48.75 MB (76.3 MB peak) | N/A | 32.90 MB (40.8 MB peak) | 1.08 MB (4.8 MB peak) |
| log2.v | 54,531 | 50.55 MB (78.1 MB peak) | N/A | 35.49 MB (43.4 MB peak) | 1.02 MB (4.7 MB peak) |
| mem_ctrl.v | 84,974 | 78.59 MB (106.1 MB peak) | N/A | 55.49 MB (63.3 MB peak) | 1.55 MB (5.3 MB peak) |
| div.v | 101,859 | 95.55 MB (123.0 MB peak) | N/A | 67.37 MB (75.2 MB peak) | 1.75 MB (5.3 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| sin.v | 8,947 | 6.53 ms (0.709 ms opt) | N/A | 38.34 ms | 2.88 s |
| voter.v | 27,720 | 19.03 ms (2.136 ms opt) | N/A | 139.90 ms | 4.45 s |
| square.v | 35,687 | 24.66 ms (4.647 ms opt) | N/A | 180.20 ms | 5.44 s |
| sqrt.v | 41,234 | 29.37 ms (3.412 ms opt) | N/A | 218.80 ms | 5.80 s |
| multiplier.v | 50,760 | 37.57 ms (7.621 ms opt) | N/A | 270.63 ms | 6.53 s |
| log2.v | 54,531 | 39.67 ms (9.418 ms opt) | N/A | 307.13 ms | 7.56 s |
| mem_ctrl.v | 84,974 | 68.91 ms (19.349 ms opt) | N/A | 845.24 ms | 13.17 s |
| div.v | 101,859 | 107.59 ms (15.462 ms opt) | N/A | 625.45 ms | 21.33 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| sin.v | 202.32 ms | 14.76 ms | 489.24 ms | N/A | 1583.50 ms | 1.23 ms |
| voter.v | 175.66 ms | 39.97 ms | 407.38 ms | N/A | 1415.94 ms | 2.91 ms |
| square.v | 155.18 ms | 61.64 ms | 333.83 ms | N/A | 1073.62 ms | 5.34 ms |
| sqrt.v | 19.28 s | 68.02 ms | 33.89 s | N/A | 130.05 s | 3.29 ms |
| multiplier.v | 1214.17 ms | 78.86 ms | 2803.32 ms | N/A | 9106.76 ms | 3.44 ms |
| log2.v | 5377.27 ms | 86.70 ms | 12.29 s | N/A | 43.69 s | 5.21 ms |
| mem_ctrl.v | 198.23 ms | 163.06 ms | 408.61 ms | N/A | 1906.44 ms | 25.93 ms |
| div.v | 370.35 ms | 117.35 ms | 578.91 ms | N/A | 2728.54 ms | 46.20 ms |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| sin.v | 7.83x | 107.30x | 3.24x | N/A | 1.00x | 1284.27x |
| voter.v | 8.06x | 35.42x | 3.48x | N/A | 1.00x | 485.97x |
| square.v | 6.92x | 17.42x | 3.22x | N/A | 1.00x | 200.97x |
| sqrt.v | 6.75x | 1912.05x | 3.84x | N/A | 1.00x | 39513.71x |
| multiplier.v | 7.50x | 115.47x | 3.25x | N/A | 1.00x | 2647.44x |
| log2.v | 8.13x | 503.93x | 3.56x | N/A | 1.00x | 8388.94x |
| mem_ctrl.v | 9.62x | 11.69x | 4.67x | N/A | 1.00x | 73.51x |
| div.v | 7.37x | 23.25x | 4.71x | N/A | 1.00x | 59.05x |

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

- **rx-prop (Wavefront BFS):** `7.73x`
- **rx-sweep (Linear Compiled):** `81.79x`
- **rx-oop (OOP Graph):** `3.70x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `911.82x`

### Gate Evaluation Highlights

- **Reactor Sweep vs Propagate Total Evaluations Ratio:** `0.09x` (propagate performed more evaluations)

### Cross-Engine Comparisons

- **Reactor Sweep vs Propagate Ratio:** `10.58x` (sweep faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | Instructions | Cycles | IPC | L1 Loads | L1 Misses | L2 Loads | L2 Misses | L3 Loads | DRAM Loads | Branches | Branch Misses |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| sin.v | rx-prop | 1.66B | 717.82M | 2.31 | 648.49M | 65.55M | 65.55M | 46.80K | 88.37K | 3.80K | 158.30M | 9.27M |
| sin.v | rx-sweep (Linear) | 55.32M | 36.97M | 1.50 | 36.33M | 2.66M | 2.66M | 906.00 | 12.78K | 1.50K | 13.47M | 1.03M |
| sin.v | rx-oop (OOP Engine) | 1.99B | 1.75B | 1.14 | 1.65B | 97.44M | 97.44M | 706.66K | 1.22M | 12.74K | 240.78M | 24.09M |
| sin.v | Icarus Verilog | 14.24B | 5.69B | 2.50 | 7.94B | 346.80M | 346.80M | 41.22M | 51.78M | 98.26K | 2.86B | 46.19M |
| sin.v | Verilator C++ | 1.48M | 1.67M | 0.88 | 3.02M | 1.90K | 1.90K | 8.00 | 8.00 | 0.00 | 85.18K | 1.58K |
| voter.v | rx-prop | 1.31B | 619.54M | 2.11 | 523.75M | 55.02M | 55.02M | 5.38M | 8.61M | 23.00K | 125.98M | 8.30M |
| voter.v | rx-sweep (Linear) | 283.83M | 137.78M | 2.06 | 130.93M | 10.06M | 10.06M | 836.43K | 4.96M | 17.65K | 56.34M | 2.63M |
| voter.v | rx-oop (OOP Engine) | 1.59B | 1.46B | 1.09 | 1.32B | 75.85M | 75.85M | 10.95M | 16.72M | 80.03K | 192.95M | 19.12M |
| voter.v | Icarus Verilog | 12.23B | 5.09B | 2.40 | 7.11B | 246.06M | 246.06M | 89.89M | 124.47M | 35.42K | 2.43B | 38.91M |
| voter.v | Verilator C++ | 1.28M | 5.62M | 0.23 | 6.63M | 6.25K | 6.25K | 1.32K | 1.32K | 981.00 | 744.95K | 41.12K |
| square.v | rx-prop | 1.04B | 544.32M | 1.91 | 404.20M | 47.82M | 47.82M | 6.39M | 10.96M | 4.02K | 99.75M | 5.60M |
| square.v | rx-sweep (Linear) | 337.66M | 201.00M | 1.68 | 162.08M | 12.17M | 12.17M | 1.94M | 8.62M | 2.22K | 63.91M | 4.21M |
| square.v | rx-oop (OOP Engine) | 1.20B | 1.19B | 1.01 | 1.04B | 65.47M | 65.47M | 11.30M | 18.44M | 70.16K | 145.63M | 14.20M |
| square.v | Icarus Verilog | 8.32B | 3.85B | 2.16 | 5.00B | 205.86M | 205.86M | 87.54M | 113.58M | 95.07K | 1.67B | 26.34M |
| square.v | Verilator C++ | 3.31M | 9.58M | 0.35 | 16.56M | 1.45K | 1.45K | 2.66K | 2.66K | 195.00 | 3.08M | 102.95K |
| sqrt.v | rx-prop | 112.12B | 69.29B | 1.62 | 43.31B | 5.70B | 5.70B | 1.92B | 3.09B | 327.48K | 10.51B | 520.83M |
| sqrt.v | rx-sweep (Linear) | 464.57M | 233.51M | 1.99 | 218.71M | 14.43M | 14.43M | 2.32M | 11.26M | 6.69K | 87.21M | 3.91M |
| sqrt.v | rx-oop (OOP Engine) | 116.66B | 121.69B | 0.96 | 98.40B | 6.79B | 6.79B | 4.02B | 5.88B | 1.70M | 14.05B | 1.13B |
| sqrt.v | Icarus Verilog | 856.00B | 467.19B | 1.83 | 542.77B | 23.39B | 23.39B | 18.25B | 25.05B | 4.10M | 171.83B | 2.59B |
| sqrt.v | Verilator C++ | 5.16M | 8.02M | 0.64 | 7.01M | 1.97K | 1.97K | 1.20K | 1.20K | 0.00 | 119.43K | 8.19K |
| multiplier.v | rx-prop | 8.19B | 4.35B | 1.88 | 3.21B | 372.36M | 372.36M | 43.86M | 64.42M | 28.53K | 786.30M | 45.75M |
| multiplier.v | rx-sweep (Linear) | 528.39M | 265.99M | 1.99 | 237.24M | 18.49M | 18.49M | 3.79M | 15.63M | 3.37K | 99.70M | 4.69M |
| multiplier.v | rx-oop (OOP Engine) | 9.66B | 10.06B | 0.96 | 8.51B | 513.80M | 513.80M | 171.93M | 247.91M | 322.99K | 1.17B | 114.39M |
| multiplier.v | Icarus Verilog | 61.73B | 32.69B | 1.89 | 39.41B | 1.49B | 1.49B | 1.06B | 1.46B | 5.20M | 12.35B | 198.82M |
| multiplier.v | Verilator C++ | 5.06M | 8.21M | 0.62 | 12.99M | 1.86K | 1.86K | 914.00 | 914.00 | 0.00 | 2.84M | 16.12K |
| log2.v | rx-prop | 35.03B | 19.31B | 1.81 | 13.57B | 1.69B | 1.69B | 412.18M | 690.52M | 357.76K | 3.32B | 171.58M |
| log2.v | rx-sweep (Linear) | 538.52M | 300.19M | 1.79 | 248.59M | 18.08M | 18.08M | 3.28M | 15.66M | 4.56K | 102.81M | 5.84M |
| log2.v | rx-oop (OOP Engine) | 41.19B | 44.07B | 0.93 | 36.47B | 2.31B | 2.31B | 1.15B | 1.67B | 1.64M | 4.98B | 464.08M |
| log2.v | Icarus Verilog | 284.74B | 156.88B | 1.82 | 182.04B | 7.10B | 7.10B | 5.52B | 7.23B | 27.53M | 57.00B | 854.92M |
| log2.v | Verilator C++ | 4.19M | 5.19M | 0.81 | 18.54M | 846.00 | 846.00 | 1.70K | 1.70K | 28.00 | 74.83K | 4.07K |
| mem_ctrl.v | rx-prop | 1.14B | 708.30M | 1.61 | 446.74M | 60.02M | 60.02M | 26.01M | 46.69M | 34.67K | 110.44M | 3.68M |
| mem_ctrl.v | rx-sweep (Linear) | 842.27M | 580.99M | 1.45 | 440.01M | 34.40M | 34.40M | 9.84M | 32.78M | 34.81K | 174.28M | 11.55M |
| mem_ctrl.v | rx-oop (OOP Engine) | 1.49B | 1.46B | 1.01 | 1.22B | 84.94M | 84.94M | 51.27M | 76.39M | 131.68K | 180.80M | 11.83M |
| mem_ctrl.v | Icarus Verilog | 13.09B | 6.82B | 1.92 | 7.84B | 307.11M | 307.11M | 245.15M | 324.77M | 3.52M | 2.61B | 25.67M |
| mem_ctrl.v | Verilator C++ | 93.66M | 82.82M | 1.13 | 41.42M | 132.93K | 132.93K | 6.31M | 6.31M | 214.00 | 6.68M | 122.50K |
| div.v | rx-prop | 2.12B | 1.31B | 1.62 | 816.55M | 108.63M | 108.63M | 45.21M | 66.57M | 55.15K | 205.22M | 6.76M |
| div.v | rx-sweep (Linear) | 1.07B | 406.33M | 2.64 | 412.40M | 33.50M | 33.50M | 6.49M | 33.88M | 6.22K | 198.55M | 5.04M |
| div.v | rx-oop (OOP Engine) | 2.38B | 2.06B | 1.16 | 1.74B | 134.46M | 134.46M | 67.52M | 100.76M | 241.73K | 289.23M | 14.68M |
| div.v | Icarus Verilog | 19.01B | 9.78B | 1.94 | 10.37B | 481.75M | 481.75M | 291.02M | 384.73M | 12.62M | 3.82B | 29.70M |
| div.v | Verilator C++ | 60.82M | 157.73M | 0.39 | 38.13M | 17.18K | 17.18K | 1.62M | 1.62M | 298.00 | 10.50M | 14.44K |
