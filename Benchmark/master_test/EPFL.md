# Master Test Unified Benchmark Report: tests/EPFL_parsed

**Execution Parameters:**
- **Target Suite / Path:** `tests/EPFL_parsed`
- **Circuits Benchmarked:** 11
- **Simulation Vectors (Phase 3):** 50,000 (Warmup: 10)
- **Verification Vectors (Phase 2):** 100
- **Hardware Profiler:** Linux `perf` kernel PMU counters

---

## 1. Zero-Testbench Memory Footprint (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| ctrl.v | 340 | 0.75 MB (28.3 MB peak) | 0.54 MB (33.5 MB peak) | 0.08 MB (8.0 MB peak) | 0.71 MB (4.4 MB peak) |
| int2float.v | 461 | 0.86 MB (28.4 MB peak) | 0.63 MB (33.7 MB peak) | 0.19 MB (8.1 MB peak) | 0.70 MB (4.4 MB peak) |
| dec.v | 576 | 0.98 MB (28.5 MB peak) | 0.82 MB (33.9 MB peak) | 0.20 MB (8.1 MB peak) | 0.75 MB (4.4 MB peak) |
| router.v | 576 | 0.92 MB (28.5 MB peak) | 0.76 MB (33.8 MB peak) | 0.33 MB (8.2 MB peak) | 0.74 MB (4.4 MB peak) |
| cavlc.v | 1,300 | 3.55 MB (31.1 MB peak) | 1.74 MB (34.8 MB peak) | 0.66 MB (8.5 MB peak) | 0.74 MB (4.4 MB peak) |
| priority.v | 2,043 | 2.27 MB (29.8 MB peak) | 2.51 MB (35.5 MB peak) | 0.87 MB (8.8 MB peak) | 0.64 MB (4.3 MB peak) |
| adder.v | 2,547 | 2.52 MB (30.1 MB peak) | 3.00 MB (36.0 MB peak) | 1.12 MB (9.0 MB peak) | 0.76 MB (4.5 MB peak) |
| i2c.v | 2,480 | 2.55 MB (30.1 MB peak) | 3.01 MB (36.0 MB peak) | 1.12 MB (9.0 MB peak) | 0.75 MB (4.4 MB peak) |
| bar.v | 5,526 | 5.64 MB (33.1 MB peak) | 6.85 MB (39.9 MB peak) | 3.13 MB (11.0 MB peak) | 0.80 MB (4.5 MB peak) |
| max.v | 6,025 | 5.95 MB (33.5 MB peak) | 7.23 MB (40.3 MB peak) | 3.37 MB (11.3 MB peak) | 0.88 MB (4.6 MB peak) |
| arbiter.v | 23,618 | 25.12 MB (52.6 MB peak) | 29.12 MB (62.2 MB peak) | 15.23 MB (23.1 MB peak) | 0.85 MB (4.5 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| ctrl.v | 340 | 0.87 ms (0.026 ms opt) | 2.74 ms | 3.77 ms | 2.49 s |
| int2float.v | 461 | 1.10 ms (0.039 ms opt) | 3.09 ms | 3.52 ms | 2.51 s |
| dec.v | 576 | 1.13 ms (0.030 ms opt) | 3.14 ms | 3.23 ms | 2.51 s |
| router.v | 576 | 1.31 ms (0.059 ms opt) | 3.25 ms | 4.19 ms | 2.52 s |
| cavlc.v | 1,300 | 2.70 ms (0.111 ms opt) | 4.69 ms | 7.18 ms | 2.55 s |
| priority.v | 2,043 | 3.74 ms (0.123 ms opt) | 6.29 ms | 9.49 ms | 2.58 s |
| adder.v | 2,547 | 4.40 ms (0.118 ms opt) | 7.29 ms | 11.21 ms | 2.59 s |
| i2c.v | 2,480 | 4.49 ms (0.185 ms opt) | 7.05 ms | 12.97 ms | 2.60 s |
| bar.v | 5,526 | 10.45 ms (0.360 ms opt) | 16.77 ms | 25.61 ms | 3.11 s |
| max.v | 6,025 | 10.77 ms (0.354 ms opt) | 17.30 ms | 26.25 ms | 2.90 s |
| arbiter.v | 23,618 | 44.14 ms (1.858 ms opt) | 60.59 ms | 118.53 ms | 8.28 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| ctrl.v | 49.93 ms | 51.94 ms | 115.77 ms | 2833.20 ms | 408.86 ms | 4.29 ms |
| int2float.v | 50.61 ms | 85.48 ms | 122.98 ms | 3248.10 ms | 504.34 ms | 5.18 ms |
| dec.v | 17.83 ms | 22.99 ms | 27.56 ms | 1392.25 ms | 173.33 ms | 3.65 ms |
| router.v | 71.33 ms | 65.03 ms | 139.77 ms | 3784.71 ms | 754.86 ms | 7.01 ms |
| cavlc.v | 157.97 ms | 241.43 ms | 372.46 ms | 9613.83 ms | 1409.46 ms | 9.00 ms |
| priority.v | 252.90 ms | 232.65 ms | 415.19 ms | 14.53 s | 13.46 s | 44.38 ms |
| adder.v | 407.76 ms | 345.94 ms | 807.70 ms | 26.37 s | 3848.10 ms | 64.25 ms |
| i2c.v | 280.52 ms | 474.94 ms | 586.50 ms | 15.22 s | 2891.85 ms | 26.96 ms |
| bar.v | 687.60 ms | 829.40 ms | 1166.14 ms | 63.80 s | 7123.64 ms | 59.43 ms |
| max.v | 1038.78 ms | 1251.83 ms | 2153.58 ms | 73.24 s | 12.53 s | 84.22 ms |
| arbiter.v | 2046.32 ms | 1877.00 ms | 3982.43 ms | 171.94 s | 17.68 s | 171.33 ms |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| ctrl.v | 8.19x | 7.87x | 3.53x | 0.14x | 1.00x | 95.25x |
| int2float.v | 9.97x | 5.90x | 4.10x | 0.16x | 1.00x | 97.41x |
| dec.v | 9.72x | 7.54x | 6.29x | 0.12x | 1.00x | 47.52x |
| router.v | 10.58x | 11.61x | 5.40x | 0.20x | 1.00x | 107.67x |
| cavlc.v | 8.92x | 5.84x | 3.78x | 0.15x | 1.00x | 156.58x |
| priority.v | 53.23x | 57.86x | 32.42x | 0.93x | 1.00x | 303.35x |
| adder.v | 9.44x | 11.12x | 4.76x | 0.15x | 1.00x | 59.89x |
| i2c.v | 10.31x | 6.09x | 4.93x | 0.19x | 1.00x | 107.25x |
| bar.v | 10.36x | 8.59x | 6.11x | 0.11x | 1.00x | 119.86x |
| max.v | 12.06x | 10.01x | 5.82x | 0.17x | 1.00x | 148.74x |
| arbiter.v | 8.64x | 9.42x | 4.44x | 0.10x | 1.00x | 103.20x |

### Total Gate Evaluations

| Circuit | Gates | rx-prop Evals | rx-sweep Evals | rx-oop Evals | Pure Python Evals |
|:---|---:|---:|---:|---:|---:|
| ctrl.v | 340 | 15,739,886 | 10,974,418 | 15,658,106 | 17,074,033 |
| int2float.v | 461 | 16,766,693 | 14,242,630 | 16,766,560 | 18,880,814 |
| dec.v | 576 | 6,880,271 | 6,441,978 | 6,880,271 | 9,484,429 |
| router.v | 576 | 16,461,182 | 13,361,600 | 16,464,462 | 18,929,784 |
| cavlc.v | 1,300 | 49,456,726 | 39,193,325 | 49,467,635 | 58,016,557 |
| priority.v | 2,043 | 69,396,620 | 52,597,845 | 69,396,620 | 77,015,512 |
| adder.v | 2,547 | 96,619,453 | 77,846,568 | 96,759,181 | 133,602,661 |
| i2c.v | 2,480 | 75,127,544 | 67,254,459 | 75,136,112 | 82,893,418 |
| bar.v | 5,526 | 259,663,641 | 170,503,222 | 260,675,986 | 346,748,531 |
| max.v | 6,025 | 298,198,879 | 195,360,744 | 298,204,263 | 365,421,111 |
| arbiter.v | 23,618 | 648,660,275 | 563,934,808 | 648,660,275 | 884,846,328 |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `11.39x`
- **rx-sweep (Linear Compiled):** `9.75x`
- **rx-oop (OOP Graph):** `5.74x`
- **Pure Python Engine:** `0.17x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `109.32x`

### Gate Evaluation Highlights

- **Reactor Sweep vs Propagate Total Evaluations Ratio:** `0.79x` (propagate performed more evaluations)

### Cross-Engine Comparisons

- **Cython Reactor (`rx-prop`) vs Pure Python:** `65.90x` faster
- **Cython Reactor (`rx-sweep`) vs Pure Python:** `56.38x` faster
- **Reactor Sweep vs Propagate Ratio:** `0.86x` (propagate faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | Instructions | Cycles | IPC | L1 Loads | L1 Misses | L2 Loads | L2 Misses | L3 Loads | DRAM Loads | Branches | Branch Misses |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| ctrl.v | rx-prop | 528.81M | 169.73M | 3.12 | 228.19M | 494.39K | 494.39K | 2.70K | 22.78K | 6.90K | 55.02M | 1.83M |
| ctrl.v | rx-sweep (Linear) | 318.25M | 159.53M | 1.99 | 171.40M | 631.25K | 631.25K | 4.53K | 20.74K | 17.74K | 68.01M | 3.62M |
| ctrl.v | rx-oop (OOP Engine) | 588.27M | 414.82M | 1.42 | 471.05M | 4.73M | 4.73M | 3.60K | 42.19K | 5.41K | 76.71M | 5.33M |
| ctrl.v | Pure Python Engine | 403.66M | 86.00M | 4.69 | 195.10M | 733.11K | 733.11K | 2.52K | 10.29K | 4.63K | 55.76M | 135.06K |
| ctrl.v | Icarus Verilog | 5.10B | 1.47B | 3.47 | 2.43B | 39.97M | 39.97M | 1.20K | 10.11K | 1.26K | 1.02B | 10.98M |
| ctrl.v | Verilator C++ | 5.30M | 15.31M | 0.35 | 22.60M | 42.50K | 42.50K | 210.00 | 438.00 | 0.00 | 5.51M | 81.16K |
| int2float.v | rx-prop | 545.52M | 171.48M | 3.18 | 233.52M | 1.36M | 1.36M | 9.14K | 43.76K | 14.41K | 54.60M | 1.65M |
| int2float.v | rx-sweep (Linear) | 488.23M | 297.09M | 1.64 | 255.28M | 1.71M | 1.71M | 5.00K | 40.00K | 10.97K | 90.82M | 6.69M |
| int2float.v | rx-oop (OOP Engine) | 608.09M | 433.75M | 1.40 | 496.77M | 9.03M | 9.03M | 13.12K | 73.98K | 40.52K | 77.29M | 5.52M |
| int2float.v | Pure Python Engine | 473.43M | 106.38M | 4.45 | 227.04M | 879.07K | 879.07K | 23.41K | 43.34K | 1.55K | 68.72M | 155.41K |
| int2float.v | Icarus Verilog | 5.70B | 1.81B | 3.16 | 2.81B | 62.07M | 62.07M | 15.04K | 27.94K | 12.28K | 1.15B | 15.30M |
| int2float.v | Verilator C++ | 15.27M | 11.38M | 1.34 | 31.41M | 35.07K | 35.07K | 1.07K | 35.08K | 184.00 | 3.79M | 138.81K |
| dec.v | rx-prop | 175.43M | 54.18M | 3.24 | 78.88M | 296.17K | 296.17K | 1.90K | 24.04K | 4.75K | 14.61M | 235.40K |
| dec.v | rx-sweep (Linear) | 198.71M | 71.99M | 2.76 | 93.68M | 480.40K | 480.40K | 2.34K | 21.36K | 1.72K | 47.64M | 1.11M |
| dec.v | rx-oop (OOP Engine) | 198.84M | 94.38M | 2.11 | 125.13M | 1.12M | 1.12M | 4.99K | 39.98K | 15.52K | 23.77M | 352.39K |
| dec.v | Pure Python Engine | 185.92M | 39.38M | 4.72 | 81.41M | 286.46K | 286.46K | 13.02K | 14.36K | 1.19K | 25.89M | 27.99K |
| dec.v | Icarus Verilog | 2.34B | 603.67M | 3.87 | 1.13B | 24.02M | 24.02M | 4.42K | 12.62K | 6.93K | 505.13M | 3.82M |
| dec.v | Verilator C++ | 23.14M | 12.44M | 1.86 | 30.40M | 41.83K | 41.83K | 1.12K | 32.92K | 28.00 | 5.32M | 49.18K |
| router.v | rx-prop | 740.04M | 299.46M | 2.47 | 364.42M | 5.28M | 5.28M | 177.51K | 2.88M | 2.79M | 110.61M | 4.34M |
| router.v | rx-sweep (Linear) | 658.58M | 263.57M | 2.50 | 318.65M | 4.19M | 4.19M | 139.03K | 2.27M | 2.17M | 145.10M | 4.04M |
| router.v | rx-oop (OOP Engine) | 748.74M | 533.21M | 1.40 | 570.13M | 13.37M | 13.37M | 87.42K | 2.34M | 2.11M | 115.76M | 7.29M |
| router.v | Pure Python Engine | 510.24M | 111.82M | 4.56 | 261.44M | 876.91K | 876.91K | 4.33K | 29.00K | 21.35K | 72.75M | 203.05K |
| router.v | Icarus Verilog | 9.40B | 2.72B | 3.46 | 4.41B | 79.05M | 79.05M | 27.98K | 51.81K | 8.80K | 1.86B | 19.36M |
| router.v | Verilator C++ | 30.05M | 9.57M | 3.14 | 32.60M | 135.24K | 135.24K | 4.53K | 126.35K | 344.00 | 2.25M | 22.17K |
| cavlc.v | rx-prop | 1.63B | 560.92M | 2.91 | 642.88M | 33.11M | 33.11M | 6.65K | 40.76K | 14.78K | 159.13M | 4.75M |
| cavlc.v | rx-sweep (Linear) | 1.38B | 861.68M | 1.60 | 671.62M | 39.46M | 39.46M | 3.16K | 32.69K | 22.40K | 254.97M | 19.10M |
| cavlc.v | rx-oop (OOP Engine) | 1.86B | 1.34B | 1.39 | 1.43B | 53.43M | 53.43M | 27.46K | 105.39K | 32.39K | 224.39M | 15.44M |
| cavlc.v | Pure Python Engine | 1.55B | 328.84M | 4.71 | 702.36M | 3.19M | 3.19M | 58.85K | 83.06K | 5.88K | 213.63M | 414.41K |
| cavlc.v | Icarus Verilog | 15.34B | 5.07B | 3.02 | 7.84B | 297.95M | 297.95M | 162.85K | 249.50K | 15.43K | 3.08B | 39.64M |
| cavlc.v | Verilator C++ | 53.63M | 27.09M | 1.98 | 32.33M | 16.25K | 16.25K | 203.00 | 16.96K | 115.00 | 5.25M | 137.84K |
| priority.v | rx-prop | 2.84B | 995.81M | 2.85 | 1.20B | 64.61M | 64.61M | 278.15K | 5.97M | 5.70M | 351.26M | 8.03M |
| priority.v | rx-sweep (Linear) | 2.36B | 917.69M | 2.57 | 1.01B | 66.72M | 66.72M | 298.74K | 6.08M | 5.89M | 477.31M | 13.43M |
| priority.v | rx-oop (OOP Engine) | 3.01B | 1.56B | 1.93 | 1.92B | 109.53M | 109.53M | 186.44K | 5.30M | 4.57M | 412.88M | 13.20M |
| priority.v | Pure Python Engine | 2.31B | 502.87M | 4.59 | 1.07B | 4.06M | 4.06M | 441.78K | 708.92K | 53.12K | 320.99M | 934.20K |
| priority.v | Icarus Verilog | 182.18B | 48.54B | 3.75 | 86.93B | 2.31B | 2.31B | 1.84M | 2.73M | 47.36K | 36.42B | 256.98M |
| priority.v | Verilator C++ | 189.68M | 158.36M | 1.20 | 134.74M | 94.41K | 94.41K | 2.27K | 125.42K | 6.11K | 17.05M | 749.28K |
| adder.v | rx-prop | 4.29B | 1.65B | 2.59 | 1.87B | 104.64M | 104.64M | 549.60K | 12.66M | 12.05M | 569.46M | 17.85M |
| adder.v | rx-sweep (Linear) | 3.79B | 1.43B | 2.65 | 1.68B | 111.06M | 111.06M | 458.36K | 12.56M | 12.01M | 780.11M | 18.13M |
| adder.v | rx-oop (OOP Engine) | 4.45B | 3.06B | 1.45 | 3.36B | 169.66M | 169.66M | 341.73K | 11.47M | 10.24M | 644.82M | 36.55M |
| adder.v | Pure Python Engine | 4.26B | 915.92M | 4.65 | 1.98B | 8.24M | 8.24M | 1.77M | 3.23M | 67.57K | 602.85M | 1.35M |
| adder.v | Icarus Verilog | 50.51B | 13.79B | 3.66 | 23.88B | 724.49M | 724.49M | 12.35M | 20.36M | 79.72K | 9.96B | 66.75M |
| adder.v | Verilator C++ | 252.78M | 231.92M | 1.09 | 176.00M | 227.59K | 227.59K | 7.93K | 156.59K | 114.40K | 14.44M | 1.27M |
| i2c.v | rx-prop | 2.96B | 1.12B | 2.65 | 1.28B | 88.21M | 88.21M | 373.53K | 7.55M | 7.25M | 360.53M | 12.14M |
| i2c.v | rx-sweep (Linear) | 2.90B | 1.82B | 1.59 | 1.44B | 96.78M | 96.78M | 332.22K | 6.75M | 6.63M | 600.27M | 38.97M |
| i2c.v | rx-oop (OOP Engine) | 3.07B | 2.18B | 1.41 | 2.34B | 132.33M | 132.33M | 244.62K | 6.33M | 5.38M | 424.82M | 26.27M |
| i2c.v | Pure Python Engine | 2.38B | 525.27M | 4.52 | 1.10B | 4.64M | 4.64M | 846.17K | 1.34M | 59.49K | 335.53M | 843.56K |
| i2c.v | Icarus Verilog | 35.09B | 10.40B | 3.37 | 17.01B | 548.73M | 548.73M | 2.71M | 3.74M | 48.67K | 6.98B | 64.81M |
| i2c.v | Verilator C++ | 216.90M | 89.72M | 2.42 | 106.15M | 96.92K | 96.92K | 1.55K | 101.59K | 5.66K | 13.94M | 1.03M |
| bar.v | rx-prop | 8.97B | 2.54B | 3.53 | 3.46B | 312.44M | 312.44M | 100.12K | 5.08M | 4.76M | 911.58M | 4.70M |
| bar.v | rx-sweep (Linear) | 6.23B | 3.05B | 2.04 | 2.87B | 196.62M | 196.62M | 261.76K | 5.36M | 5.01M | 1.18B | 60.68M |
| bar.v | rx-oop (OOP Engine) | 9.80B | 4.27B | 2.30 | 5.49B | 472.48M | 472.48M | 1.02M | 7.09M | 4.84M | 1.24B | 9.50M |
| bar.v | Pure Python Engine | 1.82B | 423.32M | 4.30 | 840.44M | 4.52M | 4.52M | 1.94M | 3.02M | 22.17K | 253.85M | 411.75K |
| bar.v | Icarus Verilog | 93.86B | 25.54B | 3.67 | 42.99B | 2.37B | 2.37B | 387.63M | 519.68M | 65.21K | 18.86B | 65.82M |
| bar.v | Verilator C++ | 339.35M | 197.15M | 1.72 | 215.00M | 135.48K | 135.48K | 2.38K | 149.97K | 6.65K | 22.38M | 1.49M |
| max.v | rx-prop | 11.90B | 4.16B | 2.86 | 4.94B | 444.99M | 444.99M | 1.51M | 28.19M | 26.77M | 1.44B | 26.88M |
| max.v | rx-sweep (Linear) | 8.83B | 4.92B | 1.80 | 4.40B | 309.83M | 309.83M | 1.54M | 28.35M | 26.99M | 1.78B | 97.20M |
| max.v | rx-oop (OOP Engine) | 12.56B | 8.10B | 1.55 | 9.11B | 662.45M | 662.45M | 3.43M | 27.69M | 21.66M | 1.72B | 79.62M |
| max.v | Pure Python Engine | 2.07B | 489.49M | 4.22 | 949.56M | 5.64M | 5.64M | 2.05M | 3.49M | 26.34K | 287.28M | 855.27K |
| max.v | Icarus Verilog | 146.41B | 44.97B | 3.26 | 74.02B | 2.68B | 2.68B | 453.87M | 656.27M | 192.60K | 28.84B | 233.04M |
| max.v | Verilator C++ | 743.21M | 287.93M | 2.58 | 385.15M | 381.49K | 381.49K | 6.62K | 347.53K | 176.22K | 48.86M | 716.00K |
| arbiter.v | rx-prop | 22.10B | 7.52B | 2.94 | 8.49B | 695.78M | 695.78M | 29.01M | 210.80M | 12.32M | 2.21B | 20.97M |
| arbiter.v | rx-sweep (Linear) | 22.06B | 6.91B | 3.19 | 7.69B | 722.90M | 722.90M | 58.72M | 284.87M | 12.25M | 4.25B | 63.12M |
| arbiter.v | rx-oop (OOP Engine) | 24.22B | 14.42B | 1.68 | 14.50B | 1.36B | 1.36B | 478.22M | 824.30M | 9.82M | 3.02B | 44.52M |
| arbiter.v | Pure Python Engine | 2.17B | 543.14M | 3.99 | 970.46M | 6.08M | 6.08M | 3.35M | 5.49M | 413.64K | 299.58M | 763.32K |
| arbiter.v | Icarus Verilog | 205.62B | 63.41B | 3.24 | 97.72B | 5.83B | 5.83B | 2.91B | 5.44B | 1.02M | 41.17B | 99.20M |
| arbiter.v | Verilator C++ | 705.70M | 602.41M | 1.17 | 547.19M | 223.51K | 223.51K | 4.73K | 229.57K | 68.62K | 25.22M | 3.81M |
