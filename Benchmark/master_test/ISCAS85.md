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
| c432.v | 203 | 0.41 MB (28.3 MB peak) | 0.32 MB (33.3 MB peak) | 0.07 MB (8.0 MB peak) | 0.68 MB (4.4 MB peak) |
| c499.v | 275 | 0.51 MB (28.4 MB peak) | 0.35 MB (33.4 MB peak) | 0.16 MB (8.0 MB peak) | 0.75 MB (4.4 MB peak) |
| c880.v | 469 | 0.62 MB (28.5 MB peak) | 0.56 MB (33.6 MB peak) | 0.26 MB (8.1 MB peak) | 0.71 MB (4.4 MB peak) |
| c1355.v | 619 | 0.80 MB (28.7 MB peak) | 0.79 MB (33.8 MB peak) | 0.31 MB (8.2 MB peak) | 0.72 MB (4.4 MB peak) |
| c1908.v | 938 | 1.08 MB (29.0 MB peak) | 1.17 MB (34.1 MB peak) | 0.37 MB (8.3 MB peak) | 0.70 MB (4.4 MB peak) |
| c2670.v | 1,642 | 1.72 MB (29.6 MB peak) | 1.98 MB (35.1 MB peak) | 0.84 MB (8.7 MB peak) | 0.74 MB (4.4 MB peak) |
| c3540.v | 1,741 | 1.87 MB (29.7 MB peak) | 2.21 MB (35.2 MB peak) | 0.84 MB (8.7 MB peak) | 0.72 MB (4.4 MB peak) |
| c5315.v | 2,608 | 2.62 MB (30.6 MB peak) | 3.20 MB (36.3 MB peak) | 1.25 MB (9.2 MB peak) | 0.75 MB (4.5 MB peak) |
| c6288.v | 2,480 | 2.57 MB (30.5 MB peak) | 3.13 MB (36.2 MB peak) | 1.25 MB (9.1 MB peak) | 0.83 MB (4.5 MB peak) |
| c7552.v | 3,828 | 3.74 MB (31.6 MB peak) | 4.64 MB (37.6 MB peak) | 1.89 MB (9.8 MB peak) | 0.81 MB (4.5 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| c432.v | 203 | 0.17 ms (0.017 ms opt) | 0.68 ms | 2.95 ms | 2.49 s |
| c499.v | 275 | 0.20 ms (0.019 ms opt) | 1.93 ms | 3.41 ms | 2.51 s |
| c880.v | 469 | 0.34 ms (0.039 ms opt) | 2.16 ms | 3.85 ms | 2.51 s |
| c1355.v | 619 | 0.42 ms (0.043 ms opt) | 2.33 ms | 4.36 ms | 2.49 s |
| c1908.v | 938 | 0.62 ms (0.074 ms opt) | 2.74 ms | 5.35 ms | 2.50 s |
| c2670.v | 1,642 | 1.01 ms (0.111 ms opt) | 3.41 ms | 7.95 ms | 2.52 s |
| c3540.v | 1,741 | 1.10 ms (0.133 ms opt) | 3.68 ms | 9.25 ms | 2.55 s |
| c5315.v | 2,608 | 1.63 ms (0.216 ms opt) | 4.79 ms | 12.34 ms | 2.57 s |
| c6288.v | 2,480 | 1.53 ms (0.143 ms opt) | 4.75 ms | 11.84 ms | 2.66 s |
| c7552.v | 3,828 | 2.31 ms (0.297 ms opt) | 7.73 ms | 17.44 ms | 2.84 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| c432.v | 37.77 ms | 50.78 ms | 67.49 ms | 2458.13 ms | 416.84 ms | 5.52 ms |
| c499.v | 43.64 ms | 50.40 ms | 79.59 ms | 9516.30 ms | 494.96 ms | 5.24 ms |
| c880.v | 73.60 ms | 100.17 ms | 181.15 ms | 4932.40 ms | 817.02 ms | 9.25 ms |
| c1355.v | 125.83 ms | 109.24 ms | 230.86 ms | 15.14 s | 1129.17 ms | 8.28 ms |
| c1908.v | 225.05 ms | 145.45 ms | 513.79 ms | 16.45 s | 1913.20 ms | 10.93 ms |
| c2670.v | 326.93 ms | 328.63 ms | 760.48 ms | 19.68 s | 3550.88 ms | 35.23 ms |
| c3540.v | 371.23 ms | 322.97 ms | 919.23 ms | 28.29 s | 3340.98 ms | 18.74 ms |
| c5315.v | 688.47 ms | 631.90 ms | 1658.16 ms | 48.98 s | 6634.78 ms | 32.12 ms |
| c6288.v | 4568.57 ms | 398.37 ms | 7055.99 ms | 472.72 s | 33.52 s | 45.21 ms |
| c7552.v | 1032.10 ms | 790.61 ms | 2453.34 ms | 76.23 s | 9751.47 ms | 44.93 ms |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| c432.v | 11.04x | 8.21x | 6.18x | 0.17x | 1.00x | 75.57x |
| c499.v | 11.34x | 9.82x | 6.22x | 0.05x | 1.00x | 94.46x |
| c880.v | 11.10x | 8.16x | 4.51x | 0.17x | 1.00x | 88.35x |
| c1355.v | 8.97x | 10.34x | 4.89x | 0.07x | 1.00x | 136.31x |
| c1908.v | 8.50x | 13.15x | 3.72x | 0.12x | 1.00x | 175.12x |
| c2670.v | 10.86x | 10.81x | 4.67x | 0.18x | 1.00x | 100.80x |
| c3540.v | 9.00x | 10.34x | 3.63x | 0.12x | 1.00x | 178.25x |
| c5315.v | 9.64x | 10.50x | 4.00x | 0.14x | 1.00x | 206.57x |
| c6288.v | 7.34x | 84.16x | 4.75x | 0.07x | 1.00x | 741.57x |
| c7552.v | 9.45x | 12.33x | 3.97x | 0.13x | 1.00x | 217.04x |

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

- **rx-prop (Wavefront BFS):** `9.64x`
- **rx-sweep (Linear Compiled):** `12.70x`
- **rx-oop (OOP Graph):** `4.58x`
- **Pure Python Engine:** `0.11x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `156.82x`

### Gate Evaluation Highlights

- **Reactor Sweep vs Propagate Total Evaluations Ratio:** `0.50x` (propagate performed more evaluations)

### Cross-Engine Comparisons

- **Cython Reactor (`rx-prop`) vs Pure Python:** `85.49x` faster
- **Cython Reactor (`rx-sweep`) vs Pure Python:** `112.62x` faster
- **Reactor Sweep vs Propagate Ratio:** `1.32x` (sweep faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | Instructions | Cycles | IPC | L1 Loads | L1 Misses | L2 Loads | L2 Misses | L3 Loads | DRAM Loads | Branches | Branch Misses |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| c432.v | rx-prop | 328.24M | 142.56M | 2.30 | 184.88M | 1.66M | 1.66M | 1.66K | 288.05K | 251.35K | 50.25M | 2.49M |
| c432.v | rx-sweep (Linear) | 269.00M | 187.20M | 1.44 | 170.94M | 1.45M | 1.45M | 23.25K | 121.87K | 110.33K | 63.62M | 4.41M |
| c432.v | rx-oop (OOP Engine) | 365.76M | 240.28M | 1.52 | 303.06M | 2.73M | 2.73M | 48.38K | 872.26K | 708.90K | 53.07M | 3.53M |
| c432.v | Pure Python Engine | 327.45M | 74.26M | 4.41 | 171.76M | 516.71K | 516.71K | 3.21K | 11.50K | 10.01K | 53.30M | 131.93K |
| c432.v | Icarus Verilog | 5.33B | 1.49B | 3.59 | 2.43B | 23.76M | 23.76M | 19.67K | 43.83K | 10.47K | 1.05B | 10.93M |
| c432.v | Verilator C++ | 22.10M | 14.16M | 1.56 | 32.37M | 110.93K | 110.93K | 4.63K | 19.86K | 0.00 | 5.75M | 94.81K |
| c499.v | rx-prop | 513.95M | 168.12M | 3.06 | 248.08M | 1.86M | 1.86M | 41.02K | 774.42K | 758.96K | 62.76M | 1.82M |
| c499.v | rx-sweep (Linear) | 466.99M | 203.24M | 2.30 | 233.19M | 2.56M | 2.56M | 57.22K | 1.63M | 1.60M | 98.98M | 3.79M |
| c499.v | rx-oop (OOP Engine) | 578.33M | 296.48M | 1.95 | 413.09M | 4.07M | 4.07M | 59.97K | 1.20M | 1.00M | 79.05M | 2.75M |
| c499.v | Pure Python Engine | 1.57B | 321.87M | 4.89 | 699.32M | 1.86M | 1.86M | 2.37K | 18.22K | 15.70K | 217.53M | 459.89K |
| c499.v | Icarus Verilog | 6.65B | 1.77B | 3.75 | 2.99B | 41.16M | 41.16M | 1.43K | 10.34K | 7.22K | 1.32B | 12.56M |
| c499.v | Verilator C++ | 34.13M | 10.54M | 3.24 | 40.57M | 144.73K | 144.73K | 1.23K | 115.69K | 292.00 | 3.74M | 20.97K |
| c880.v | rx-prop | 755.66M | 287.90M | 2.62 | 339.97M | 3.89M | 3.89M | 65.94K | 1.99M | 1.94M | 92.10M | 4.55M |
| c880.v | rx-sweep (Linear) | 651.57M | 390.18M | 1.67 | 329.83M | 4.12M | 4.12M | 65.21K | 2.32M | 2.19M | 132.48M | 8.12M |
| c880.v | rx-oop (OOP Engine) | 844.30M | 680.37M | 1.24 | 690.96M | 14.77M | 14.77M | 58.62K | 2.15M | 1.88M | 119.86M | 9.81M |
| c880.v | Pure Python Engine | 764.06M | 164.35M | 4.65 | 349.43M | 1.11M | 1.11M | 4.30K | 23.85K | 21.69K | 106.72M | 334.44K |
| c880.v | Icarus Verilog | 10.12B | 2.94B | 3.44 | 4.69B | 85.51M | 85.51M | 9.62K | 20.25K | 6.83K | 2.00B | 24.00M |
| c880.v | Verilator C++ | 45.90M | 21.02M | 2.18 | 34.28M | 52.48K | 52.48K | 2.48K | 119.95K | 404.00 | 6.19M | 144.99K |
| c1355.v | rx-prop | 1.26B | 463.23M | 2.71 | 562.09M | 11.22M | 11.22M | 57.46K | 875.87K | 811.37K | 128.34M | 7.47M |
| c1355.v | rx-sweep (Linear) | 778.43M | 405.12M | 1.92 | 393.70M | 7.88M | 7.88M | 38.76K | 725.26K | 712.28K | 159.06M | 7.05M |
| c1355.v | rx-oop (OOP Engine) | 1.40B | 836.15M | 1.68 | 968.11M | 30.16M | 30.16M | 79.08K | 1.30M | 1.09M | 174.76M | 9.57M |
| c1355.v | Pure Python Engine | 2.45B | 512.10M | 4.79 | 1.10B | 3.70M | 3.70M | 14.34K | 40.39K | 16.59K | 339.06M | 772.46K |
| c1355.v | Icarus Verilog | 14.69B | 4.06B | 3.62 | 6.76B | 125.49M | 125.49M | 16.93K | 27.66K | 5.63K | 2.94B | 29.97M |
| c1355.v | Verilator C++ | 47.31M | 21.62M | 2.19 | 33.36M | 53.42K | 53.42K | 2.67K | 104.27K | 366.00 | 6.28M | 291.44K |
| c1908.v | rx-prop | 2.25B | 805.61M | 2.80 | 992.20M | 27.77M | 27.77M | 77.83K | 810.32K | 757.66K | 225.96M | 12.65M |
| c1908.v | rx-sweep (Linear) | 1.13B | 533.03M | 2.13 | 491.97M | 27.96M | 27.96M | 57.99K | 630.56K | 618.84K | 217.70M | 8.42M |
| c1908.v | rx-oop (OOP Engine) | 2.83B | 1.87B | 1.52 | 2.07B | 50.43M | 50.43M | 59.59K | 529.78K | 443.37K | 353.26M | 22.89M |
| c1908.v | Pure Python Engine | 2.72B | 563.37M | 4.83 | 1.25B | 4.86M | 4.86M | 35.16K | 53.53K | 14.92K | 378.90M | 743.11K |
| c1908.v | Icarus Verilog | 22.69B | 6.90B | 3.29 | 11.10B | 291.16M | 291.16M | 23.40K | 38.14K | 9.38K | 4.53B | 54.43M |
| c1908.v | Verilator C++ | 60.18M | 43.42M | 1.39 | 47.85M | 93.28K | 93.28K | 1.56K | 36.59K | 25.00 | 8.84M | 327.69K |
| c2670.v | rx-prop | 3.29B | 1.33B | 2.47 | 1.47B | 66.72M | 66.72M | 381.54K | 11.30M | 10.86M | 422.06M | 20.11M |
| c2670.v | rx-sweep (Linear) | 2.43B | 1.33B | 1.82 | 1.16B | 71.40M | 71.40M | 335.39K | 11.56M | 11.12M | 503.63M | 24.98M |
| c2670.v | rx-oop (OOP Engine) | 3.83B | 2.88B | 1.33 | 2.98B | 111.21M | 111.21M | 289.01K | 10.56M | 9.45M | 549.10M | 39.32M |
| c2670.v | Pure Python Engine | 3.16B | 675.44M | 4.68 | 1.47B | 5.49M | 5.49M | 333.92K | 547.64K | 88.38K | 445.31M | 1.23M |
| c2670.v | Icarus Verilog | 45.07B | 12.79B | 3.52 | 21.58B | 486.58M | 486.58M | 355.43K | 513.30K | 55.59K | 8.88B | 88.27M |
| c2670.v | Verilator C++ | 217.53M | 124.01M | 1.75 | 111.34M | 156.06K | 156.06K | 3.94K | 174.12K | 30.34K | 13.02M | 1.66M |
| c3540.v | rx-prop | 3.58B | 1.36B | 2.63 | 1.52B | 61.67M | 61.67M | 108.54K | 2.14M | 2.09M | 367.56M | 22.28M |
| c3540.v | rx-sweep (Linear) | 1.98B | 1.19B | 1.66 | 933.97M | 60.76M | 60.76M | 118.48K | 2.25M | 2.21M | 383.13M | 25.34M |
| c3540.v | rx-oop (OOP Engine) | 4.27B | 3.31B | 1.29 | 3.37B | 102.73M | 102.73M | 119.38K | 524.35K | 302.27K | 539.15M | 46.97M |
| c3540.v | Pure Python Engine | 4.64B | 987.24M | 4.70 | 2.12B | 8.29M | 8.29M | 363.34K | 521.99K | 20.47K | 647.87M | 1.58M |
| c3540.v | Icarus Verilog | 35.02B | 12.04B | 2.91 | 17.96B | 597.21M | 597.21M | 123.56K | 142.79K | 8.62K | 7.00B | 108.91M |
| c3540.v | Verilator C++ | 118.73M | 64.91M | 1.83 | 73.28M | 99.04K | 99.04K | 1.19K | 48.78K | 911.00 | 10.38M | 251.63K |
| c5315.v | rx-prop | 6.67B | 2.58B | 2.58 | 2.88B | 160.88M | 160.88M | 298.46K | 7.95M | 7.52M | 715.45M | 39.59M |
| c5315.v | rx-sweep (Linear) | 3.76B | 2.38B | 1.58 | 1.92B | 118.05M | 118.05M | 297.39K | 8.20M | 7.76M | 733.50M | 52.37M |
| c5315.v | rx-oop (OOP Engine) | 7.80B | 6.04B | 1.29 | 6.11B | 268.31M | 268.31M | 406.63K | 7.75M | 6.50M | 1.00B | 81.81M |
| c5315.v | Pure Python Engine | 1.44B | 324.28M | 4.45 | 664.21M | 2.75M | 2.75M | 495.54K | 716.61K | 15.05K | 199.09M | 687.11K |
| c5315.v | Icarus Verilog | 73.45B | 23.89B | 3.07 | 36.27B | 1.23B | 1.23B | 5.94M | 8.55M | 57.78K | 14.65B | 196.42M |
| c5315.v | Verilator C++ | 236.03M | 112.46M | 2.10 | 144.08M | 186.11K | 186.11K | 4.66K | 171.38K | 15.10K | 13.28M | 878.91K |
| c6288.v | rx-prop | 39.40B | 16.49B | 2.39 | 16.32B | 961.33M | 961.33M | 219.06K | 725.15K | 402.24K | 3.72B | 277.94M |
| c6288.v | rx-sweep (Linear) | 3.46B | 1.44B | 2.40 | 1.57B | 98.24M | 98.24M | 46.04K | 444.53K | 418.13K | 639.40M | 21.89M |
| c6288.v | rx-oop (OOP Engine) | 45.71B | 25.43B | 1.80 | 27.91B | 1.73B | 1.73B | 190.28K | 873.75K | 487.25K | 5.49B | 298.25M |
| c6288.v | Pure Python Engine | 15.17B | 3.23B | 4.69 | 6.82B | 29.88M | 29.88M | 1.30M | 2.08M | 8.54K | 2.10B | 4.89M |
| c6288.v | Icarus Verilog | 434.55B | 120.99B | 3.59 | 192.31B | 8.40B | 8.40B | 15.28M | 21.88M | 24.91K | 86.32B | 697.91M |
| c6288.v | Verilator C++ | 248.90M | 159.39M | 1.56 | 135.64M | 43.23K | 43.23K | 844.00 | 86.04K | 372.00 | 24.90M | 2.32M |
| c7552.v | rx-prop | 9.56B | 3.86B | 2.48 | 4.07B | 308.37M | 308.37M | 521.80K | 10.35M | 9.79M | 1.01B | 57.86M |
| c7552.v | rx-sweep (Linear) | 5.26B | 2.99B | 1.76 | 2.50B | 163.95M | 163.95M | 493.05K | 10.56M | 10.14M | 1.01B | 63.08M |
| c7552.v | rx-oop (OOP Engine) | 12.01B | 8.95B | 1.34 | 9.02B | 480.65M | 480.65M | 1.06M | 10.73M | 8.16M | 1.52B | 114.22M |
| c7552.v | Pure Python Engine | 2.24B | 492.02M | 4.54 | 1.04B | 4.19M | 4.19M | 1.36M | 1.97M | 21.54K | 310.98M | 751.64K |
| c7552.v | Icarus Verilog | 102.49B | 35.05B | 2.92 | 52.64B | 1.90B | 1.90B | 150.17M | 203.25M | 43.34K | 20.43B | 279.51M |
| c7552.v | Verilator C++ | 305.03M | 156.30M | 1.95 | 163.25M | 226.05K | 226.05K | 3.65K | 143.14K | 23.04K | 20.50M | 1.61M |
