# Master Test Unified Benchmark Report: tests/ISCAS85

**Execution Parameters:**
- **Target Suite / Path:** `tests/ISCAS85`
- **Circuits Benchmarked:** 10
- **Simulation Vectors (Phase 3):** 50,000 (Warmup: 10)
- **Verification Vectors (Phase 2):** 100
- **Hardware Profiler:** Linux `perf` kernel PMU counters

---

## 1. Zero-Testbench Memory Footprint (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| c432.v | 203 | 0.59 MB (28.1 MB peak) | 0.38 MB (33.4 MB peak) | 0.16 MB (8.0 MB peak) | 0.71 MB (4.3 MB peak) |
| c499.v | 275 | 0.66 MB (28.2 MB peak) | 0.41 MB (33.5 MB peak) | 0.17 MB (8.0 MB peak) | 0.74 MB (4.4 MB peak) |
| c880.v | 469 | 0.84 MB (28.4 MB peak) | 0.62 MB (33.6 MB peak) | 0.17 MB (8.0 MB peak) | 0.75 MB (4.4 MB peak) |
| c1355.v | 619 | 0.98 MB (28.6 MB peak) | 0.84 MB (33.9 MB peak) | 0.34 MB (8.2 MB peak) | 0.73 MB (4.4 MB peak) |
| c1908.v | 938 | 1.31 MB (28.9 MB peak) | 1.25 MB (34.3 MB peak) | 0.47 MB (8.4 MB peak) | 0.71 MB (4.4 MB peak) |
| c2670.v | 1,642 | 1.92 MB (29.4 MB peak) | 2.04 MB (35.0 MB peak) | 0.80 MB (8.6 MB peak) | 0.72 MB (4.4 MB peak) |
| c3540.v | 1,741 | 4.00 MB (31.5 MB peak) | 2.24 MB (35.3 MB peak) | 0.90 MB (8.7 MB peak) | 0.72 MB (4.4 MB peak) |
| c5315.v | 2,608 | 2.91 MB (30.4 MB peak) | 3.30 MB (36.3 MB peak) | 1.29 MB (9.1 MB peak) | 0.77 MB (4.5 MB peak) |
| c6288.v | 2,480 | 2.75 MB (30.3 MB peak) | 3.20 MB (36.2 MB peak) | 1.26 MB (9.1 MB peak) | 0.82 MB (4.5 MB peak) |
| c7552.v | 3,828 | 3.90 MB (31.4 MB peak) | 4.75 MB (37.8 MB peak) | 1.77 MB (9.7 MB peak) | 0.81 MB (4.5 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| c432.v | 203 | 0.17 ms (0.016 ms opt) | 0.83 ms | 2.48 ms | 2.61 s |
| c499.v | 275 | 0.23 ms (0.020 ms opt) | 2.14 ms | 3.13 ms | 2.55 s |
| c880.v | 469 | 0.36 ms (0.040 ms opt) | 2.80 ms | 3.72 ms | 2.53 s |
| c1355.v | 619 | 0.44 ms (0.043 ms opt) | 2.79 ms | 4.50 ms | 2.52 s |
| c1908.v | 938 | 0.63 ms (0.072 ms opt) | 2.92 ms | 6.02 ms | 2.52 s |
| c2670.v | 1,642 | 1.05 ms (0.120 ms opt) | 4.20 ms | 7.66 ms | 2.53 s |
| c3540.v | 1,741 | 1.15 ms (0.134 ms opt) | 4.17 ms | 8.97 ms | 2.54 s |
| c5315.v | 2,608 | 1.67 ms (0.214 ms opt) | 5.29 ms | 12.16 ms | 2.59 s |
| c6288.v | 2,480 | 1.65 ms (0.141 ms opt) | 5.00 ms | 12.17 ms | 2.66 s |
| c7552.v | 3,828 | 2.45 ms (0.291 ms opt) | 8.59 ms | 16.79 ms | 2.90 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| c432.v | 40.35 ms | 50.27 ms | 67.58 ms | 2538.18 ms | 423.69 ms | 5.62 ms |
| c499.v | 50.22 ms | 54.13 ms | 80.61 ms | 9849.60 ms | 502.26 ms | 5.07 ms |
| c880.v | 79.03 ms | 102.67 ms | 179.31 ms | 5013.59 ms | 831.15 ms | 9.43 ms |
| c1355.v | 140.04 ms | 110.79 ms | 232.29 ms | 15.31 s | 1142.00 ms | 10.21 ms |
| c1908.v | 252.49 ms | 147.93 ms | 516.34 ms | 16.80 s | 1918.82 ms | 10.01 ms |
| c2670.v | 348.84 ms | 332.08 ms | 750.05 ms | 20.16 s | 3611.76 ms | 35.76 ms |
| c3540.v | 403.18 ms | 327.01 ms | 920.78 ms | 29.48 s | 3343.88 ms | 19.80 ms |
| c5315.v | 749.41 ms | 638.40 ms | 1667.13 ms | 47.31 s | 6718.27 ms | 31.96 ms |
| c6288.v | 5034.30 ms | 402.80 ms | 7109.53 ms | 479.96 s | 33.70 s | 45.98 ms |
| c7552.v | 1132.31 ms | 797.06 ms | 2457.65 ms | 81.34 s | 9696.68 ms | 47.84 ms |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| c432.v | 10.50x | 8.43x | 6.27x | 0.17x | 1.00x | 75.33x |
| c499.v | 10.00x | 9.28x | 6.23x | 0.05x | 1.00x | 99.14x |
| c880.v | 10.52x | 8.10x | 4.64x | 0.17x | 1.00x | 88.10x |
| c1355.v | 8.16x | 10.31x | 4.92x | 0.07x | 1.00x | 111.82x |
| c1908.v | 7.60x | 12.97x | 3.72x | 0.11x | 1.00x | 191.69x |
| c2670.v | 10.35x | 10.88x | 4.82x | 0.18x | 1.00x | 100.99x |
| c3540.v | 8.29x | 10.23x | 3.63x | 0.11x | 1.00x | 168.85x |
| c5315.v | 8.96x | 10.52x | 4.03x | 0.14x | 1.00x | 210.18x |
| c6288.v | 6.69x | 83.66x | 4.74x | 0.07x | 1.00x | 732.82x |
| c7552.v | 8.56x | 12.17x | 3.95x | 0.12x | 1.00x | 202.71x |

### Total Gate Evaluations

| Circuit | Gates | rx-prop Evals | rx-sweep Evals | rx-oop Evals | Pure Python Evals |
|:---|---:|---:|---:|---:|---:|
| c432.v | 203 | 9,128,966 | 6,971,040 | 9,130,346 | 13,857,840 |
| c499.v | 275 | 15,063,495 | 11,407,155 | 15,094,832 | 63,115,231 |
| c880.v | 469 | 19,695,830 | 15,217,400 | 19,696,070 | 26,327,794 |
| c1355.v | 619 | 39,549,415 | 22,635,449 | 39,537,628 | 98,136,287 |
| c1908.v | 938 | 72,900,551 | 32,794,630 | 78,891,181 | 105,221,706 |
| c2670.v | 1,642 | 80,777,771 | 49,866,061 | 87,144,800 | 109,705,911 |
| c3540.v | 1,741 | 111,177,579 | 56,818,394 | 116,831,656 | 174,716,886 |
| c5315.v | 2,608 | 199,896,792 | 106,287,491 | 207,289,686 | 275,769,571 |
| c6288.v | 2,480 | 1,288,764,182 | 116,272,301 | 1,300,998,782 | 3,121,550,301 |
| c7552.v | 3,828 | 286,320,899 | 146,608,515 | 317,587,492 | 440,708,682 |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `8.87x`
- **rx-sweep (Linear Compiled):** `12.60x`
- **rx-oop (OOP Graph):** `4.61x`
- **Pure Python Engine:** `0.11x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `154.01x`

### Gate Evaluation Highlights

- **Reactor Sweep vs Propagate Total Evaluations Ratio:** `0.50x` (propagate performed more evaluations)

### Cross-Engine Comparisons

- **Cython Reactor (`rx-prop`) vs Pure Python:** `79.74x` faster
- **Cython Reactor (`rx-sweep`) vs Pure Python:** `113.25x` faster
- **Reactor Sweep vs Propagate Ratio:** `1.42x` (sweep faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | Instructions | Cycles | IPC | L1 Loads | L1 Misses | L2 Loads | L2 Misses | L3 Loads | DRAM Loads | Branches | Branch Misses |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| c432.v | rx-prop | 401.22M | 163.21M | 2.46 | 199.04M | 2.00M | 2.00M | 36.71K | 1.29M | 1.21M | 56.05M | 2.53M |
| c432.v | rx-sweep (Linear) | 350.13M | 208.06M | 1.68 | 192.22M | 1.86M | 1.86M | 42.48K | 1.57M | 1.55M | 76.64M | 4.57M |
| c432.v | rx-oop (OOP Engine) | 386.74M | 257.61M | 1.50 | 288.22M | 2.61M | 2.61M | 26.53K | 426.16K | 342.03K | 58.22M | 3.43M |
| c432.v | Pure Python Engine | 345.12M | 74.86M | 4.61 | 189.99M | 569.28K | 569.28K | 5.63K | 15.22K | 8.35K | 51.18M | 193.82K |
| c432.v | Icarus Verilog | 5.32B | 1.51B | 3.53 | 2.47B | 25.37M | 25.37M | 12.27K | 26.77K | 8.55K | 1.06B | 11.20M |
| c432.v | Verilator C++ | 31.67M | 14.14M | 2.24 | 37.70M | 115.76K | 115.76K | 2.19K | 95.80K | 226.00 | 3.70M | 105.83K |
| c499.v | rx-prop | 542.01M | 189.80M | 2.86 | 259.42M | 1.93M | 1.93M | 44.76K | 1.10M | 1.02M | 65.70M | 1.84M |
| c499.v | rx-sweep (Linear) | 435.23M | 201.16M | 2.16 | 232.29M | 2.37M | 2.37M | 44.72K | 420.64K | 398.85K | 91.43M | 3.63M |
| c499.v | rx-oop (OOP Engine) | 584.46M | 301.85M | 1.94 | 411.06M | 5.54M | 5.54M | 52.76K | 1.24M | 1.07M | 79.28M | 2.73M |
| c499.v | Pure Python Engine | 1.57B | 338.46M | 4.63 | 729.92M | 1.92M | 1.92M | 7.49K | 23.30K | 15.58K | 222.44M | 745.56K |
| c499.v | Icarus Verilog | 6.67B | 1.81B | 3.70 | 3.00B | 41.15M | 41.15M | 1.05K | 10.35K | 7.25K | 1.33B | 12.17M |
| c499.v | Verilator C++ | 4.42M | 8.96M | 0.49 | 22.41M | 97.25K | 97.25K | 5.90K | 82.46K | 0.00 | 4.64M | 10.12K |
| c880.v | rx-prop | 808.53M | 307.84M | 2.63 | 369.76M | 4.07M | 4.07M | 64.24K | 2.03M | 1.98M | 102.16M | 4.52M |
| c880.v | rx-sweep (Linear) | 705.49M | 398.02M | 1.77 | 377.74M | 5.00M | 5.00M | 75.56K | 2.38M | 2.29M | 151.55M | 8.22M |
| c880.v | rx-oop (OOP Engine) | 826.26M | 670.89M | 1.23 | 688.43M | 15.85M | 15.85M | 69.19K | 2.30M | 1.99M | 122.17M | 9.92M |
| c880.v | Pure Python Engine | 662.42M | 153.64M | 4.31 | 386.42M | 1.23M | 1.23M | 5.17K | 25.38K | 20.51K | 110.27M | 320.07K |
| c880.v | Icarus Verilog | 9.96B | 2.96B | 3.36 | 4.69B | 87.09M | 87.09M | 4.89K | 16.81K | 6.48K | 1.99B | 23.56M |
| c880.v | Verilator C++ | 53.63M | 24.17M | 2.22 | 31.46M | 47.31K | 47.31K | 882.00 | 73.82K | 2.73K | 5.92M | 140.47K |
| c1355.v | rx-prop | 1.30B | 511.60M | 2.54 | 563.11M | 14.40M | 14.40M | 52.46K | 1.06M | 988.56K | 129.85M | 7.45M |
| c1355.v | rx-sweep (Linear) | 807.26M | 401.45M | 2.01 | 440.27M | 9.84M | 9.84M | 52.09K | 325.68K | 312.31K | 176.12M | 7.01M |
| c1355.v | rx-oop (OOP Engine) | 1.41B | 846.45M | 1.67 | 969.82M | 30.60M | 30.60M | 62.28K | 978.71K | 810.44K | 179.17M | 9.70M |
| c1355.v | Pure Python Engine | 2.50B | 531.73M | 4.71 | 1.14B | 3.89M | 3.89M | 11.14K | 33.78K | 15.68K | 349.23M | 803.83K |
| c1355.v | Icarus Verilog | 14.70B | 4.09B | 3.59 | 6.76B | 126.53M | 126.53M | 8.93K | 22.28K | 7.82K | 2.94B | 29.87M |
| c1355.v | Verilator C++ | 61.73M | 38.77M | 1.59 | 46.57M | 109.95K | 109.95K | 2.42K | 43.94K | 13.00 | 8.71M | 431.04K |
| c1908.v | rx-prop | 2.37B | 913.82M | 2.59 | 959.09M | 25.89M | 25.89M | 25.66K | 135.41K | 94.47K | 229.85M | 12.55M |
| c1908.v | rx-sweep (Linear) | 1.20B | 549.03M | 2.18 | 503.92M | 28.46M | 28.46M | 76.23K | 748.73K | 722.22K | 222.15M | 8.45M |
| c1908.v | rx-oop (OOP Engine) | 2.81B | 1.85B | 1.52 | 2.07B | 52.29M | 52.29M | 37.82K | 281.01K | 193.55K | 350.31M | 22.83M |
| c1908.v | Pure Python Engine | 2.76B | 581.74M | 4.75 | 1.25B | 4.86M | 4.86M | 14.50K | 38.26K | 14.47K | 380.54M | 866.92K |
| c1908.v | Icarus Verilog | 22.67B | 6.91B | 3.28 | 11.02B | 291.07M | 291.07M | 51.38K | 68.42K | 12.14K | 4.53B | 54.65M |
| c1908.v | Verilator C++ | 69.32M | 38.35M | 1.81 | 44.11M | 94.04K | 94.04K | 984.00 | 39.16K | 83.00 | 9.10M | 286.07K |
| c2670.v | rx-prop | 3.55B | 1.43B | 2.49 | 1.58B | 67.62M | 67.62M | 436.17K | 11.38M | 10.83M | 483.15M | 19.74M |
| c2670.v | rx-sweep (Linear) | 2.60B | 1.35B | 1.93 | 1.28B | 71.16M | 71.16M | 476.58K | 11.37M | 10.76M | 550.86M | 25.31M |
| c2670.v | rx-oop (OOP Engine) | 3.80B | 2.83B | 1.34 | 2.98B | 113.34M | 113.34M | 328.72K | 10.15M | 9.03M | 552.12M | 39.22M |
| c2670.v | Pure Python Engine | 3.19B | 689.74M | 4.62 | 1.48B | 5.54M | 5.54M | 270.33K | 467.11K | 87.27K | 441.64M | 1.43M |
| c2670.v | Icarus Verilog | 45.08B | 13.01B | 3.47 | 21.48B | 484.65M | 484.65M | 447.31K | 702.06K | 56.41K | 8.87B | 87.37M |
| c2670.v | Verilator C++ | 224.29M | 127.91M | 1.75 | 114.07M | 156.91K | 156.91K | 3.04K | 159.19K | 38.38K | 13.47M | 1.67M |
| c3540.v | rx-prop | 3.77B | 1.48B | 2.55 | 1.50B | 62.17M | 62.17M | 100.51K | 2.07M | 2.00M | 374.76M | 21.66M |
| c3540.v | rx-sweep (Linear) | 2.07B | 1.21B | 1.71 | 941.92M | 61.36M | 61.36M | 105.65K | 2.02M | 1.98M | 393.74M | 25.51M |
| c3540.v | rx-oop (OOP Engine) | 4.32B | 3.32B | 1.30 | 3.37B | 103.75M | 103.75M | 107.19K | 1.96M | 1.65M | 532.26M | 47.33M |
| c3540.v | Pure Python Engine | 4.55B | 999.17M | 4.55 | 2.16B | 10.38M | 10.38M | 435.62K | 585.60K | 21.60K | 629.82M | 1.83M |
| c3540.v | Icarus Verilog | 35.05B | 12.05B | 2.91 | 17.87B | 594.25M | 594.25M | 335.26K | 520.79K | 9.81K | 7.00B | 109.06M |
| c3540.v | Verilator C++ | 100.52M | 60.24M | 1.67 | 65.62M | 45.34K | 45.34K | 810.00 | 45.35K | 829.00 | 9.27M | 220.79K |
| c5315.v | rx-prop | 7.03B | 2.81B | 2.50 | 2.90B | 158.94M | 158.94M | 312.55K | 8.59M | 7.98M | 743.79M | 39.04M |
| c5315.v | rx-sweep (Linear) | 4.00B | 2.41B | 1.66 | 1.98B | 116.53M | 116.53M | 345.08K | 8.22M | 7.77M | 765.22M | 52.78M |
| c5315.v | rx-oop (OOP Engine) | 7.81B | 6.09B | 1.28 | 6.11B | 273.75M | 273.75M | 469.85K | 8.02M | 6.62M | 1.01B | 81.66M |
| c5315.v | Pure Python Engine | 1.42B | 307.63M | 4.63 | 657.08M | 2.52M | 2.52M | 480.59K | 686.73K | 15.95K | 195.85M | 468.07K |
| c5315.v | Icarus Verilog | 73.48B | 24.18B | 3.04 | 36.26B | 1.22B | 1.22B | 15.66M | 24.16M | 34.31K | 14.67B | 198.71M |
| c5315.v | Verilator C++ | 246.12M | 105.05M | 2.34 | 140.95M | 182.75K | 182.75K | 4.72K | 192.05K | 10.89K | 12.25M | 840.84K |
| c6288.v | rx-prop | 41.13B | 18.17B | 2.26 | 16.01B | 921.41M | 921.41M | 252.79K | 1.54M | 1.13M | 3.73B | 278.83M |
| c6288.v | rx-sweep (Linear) | 3.68B | 1.46B | 2.51 | 1.56B | 98.01M | 98.01M | 71.91K | 1.61M | 1.58M | 651.72M | 21.71M |
| c6288.v | rx-oop (OOP Engine) | 45.73B | 25.63B | 1.78 | 27.93B | 1.75B | 1.75B | 301.15K | 1.87M | 1.25M | 5.49B | 298.57M |
| c6288.v | Pure Python Engine | 15.22B | 3.27B | 4.65 | 6.88B | 29.21M | 29.21M | 1.54M | 2.43M | 10.32K | 2.09B | 5.41M |
| c6288.v | Icarus Verilog | 434.53B | 121.51B | 3.58 | 196.51B | 8.40B | 8.40B | 30.28M | 45.86M | 75.53K | 86.33B | 697.93M |
| c6288.v | Verilator C++ | 248.31M | 167.32M | 1.48 | 143.28M | 84.55K | 84.55K | 1.79K | 41.96K | 2.63K | 25.68M | 2.42M |
| c7552.v | rx-prop | 10.01B | 4.22B | 2.37 | 4.10B | 305.48M | 305.48M | 615.35K | 11.50M | 10.74M | 1.05B | 57.57M |
| c7552.v | rx-sweep (Linear) | 5.56B | 3.02B | 1.84 | 2.56B | 161.88M | 161.88M | 583.94K | 11.03M | 10.43M | 1.06B | 62.47M |
| c7552.v | rx-oop (OOP Engine) | 11.99B | 8.94B | 1.34 | 9.04B | 480.57M | 480.57M | 685.63K | 10.30M | 8.48M | 1.52B | 114.01M |
| c7552.v | Pure Python Engine | 2.26B | 540.79M | 4.17 | 1.09B | 4.30M | 4.30M | 1.35M | 1.91M | 20.47K | 324.95M | 1.40M |
| c7552.v | Icarus Verilog | 102.46B | 34.85B | 2.94 | 51.85B | 1.90B | 1.90B | 127.35M | 184.39M | 52.38K | 20.43B | 278.23M |
| c7552.v | Verilator C++ | 305.63M | 168.80M | 1.81 | 173.79M | 210.70K | 210.70K | 4.92K | 202.27K | 13.93K | 20.83M | 1.68M |
