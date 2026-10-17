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
| ctrl.v | 340 | 0.59 MB (28.4 MB peak) | 0.43 MB (33.4 MB peak) | 0.16 MB (8.0 MB peak) | 0.71 MB (4.4 MB peak) |
| int2float.v | 461 | 0.63 MB (28.6 MB peak) | 0.55 MB (33.6 MB peak) | 0.21 MB (8.1 MB peak) | 0.73 MB (4.4 MB peak) |
| dec.v | 576 | 0.78 MB (28.7 MB peak) | 0.71 MB (33.7 MB peak) | 0.21 MB (8.1 MB peak) | 0.62 MB (4.3 MB peak) |
| router.v | 576 | 0.76 MB (28.5 MB peak) | 0.69 MB (33.7 MB peak) | 0.31 MB (8.1 MB peak) | 0.71 MB (4.4 MB peak) |
| cavlc.v | 1,300 | 1.42 MB (29.4 MB peak) | 1.64 MB (34.7 MB peak) | 0.64 MB (8.5 MB peak) | 0.71 MB (4.4 MB peak) |
| priority.v | 2,043 | 1.91 MB (30.0 MB peak) | 2.48 MB (35.5 MB peak) | 0.97 MB (8.9 MB peak) | 0.85 MB (4.4 MB peak) |
| adder.v | 2,547 | 2.41 MB (30.2 MB peak) | 2.93 MB (35.9 MB peak) | 1.22 MB (9.1 MB peak) | 0.79 MB (4.5 MB peak) |
| i2c.v | 2,480 | 2.42 MB (30.3 MB peak) | 2.88 MB (36.0 MB peak) | 1.18 MB (9.0 MB peak) | 0.73 MB (4.4 MB peak) |
| bar.v | 5,526 | 5.45 MB (33.4 MB peak) | 6.84 MB (39.8 MB peak) | 3.23 MB (11.0 MB peak) | 0.80 MB (4.5 MB peak) |
| max.v | 6,025 | 5.79 MB (33.7 MB peak) | 7.18 MB (40.3 MB peak) | 3.41 MB (11.3 MB peak) | 0.89 MB (4.6 MB peak) |
| arbiter.v | 23,618 | 23.36 MB (51.2 MB peak) | 29.18 MB (62.2 MB peak) | 15.18 MB (23.1 MB peak) | 0.88 MB (4.6 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| ctrl.v | 340 | 0.87 ms (0.027 ms opt) | 2.59 ms | 3.71 ms | 2.49 s |
| int2float.v | 461 | 1.09 ms (0.037 ms opt) | 2.85 ms | 3.87 ms | 2.50 s |
| dec.v | 576 | 1.13 ms (0.031 ms opt) | 2.89 ms | 3.75 ms | 2.51 s |
| router.v | 576 | 1.24 ms (0.038 ms opt) | 3.00 ms | 4.18 ms | 2.50 s |
| cavlc.v | 1,300 | 2.63 ms (0.105 ms opt) | 4.75 ms | 6.98 ms | 2.51 s |
| priority.v | 2,043 | 3.73 ms (0.120 ms opt) | 6.14 ms | 9.76 ms | 2.55 s |
| adder.v | 2,547 | 4.39 ms (0.121 ms opt) | 6.92 ms | 11.20 ms | 2.56 s |
| i2c.v | 2,480 | 4.46 ms (0.183 ms opt) | 7.16 ms | 12.20 ms | 2.56 s |
| bar.v | 5,526 | 10.45 ms (0.347 ms opt) | 15.76 ms | 25.07 ms | 3.10 s |
| max.v | 6,025 | 10.86 ms (0.346 ms opt) | 16.42 ms | 26.38 ms | 2.80 s |
| arbiter.v | 23,618 | 44.03 ms (1.779 ms opt) | 61.99 ms | 118.41 ms | 8.24 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| ctrl.v | 44.57 ms | 48.68 ms | 117.98 ms | 2918.00 ms | 407.91 ms | 5.05 ms |
| int2float.v | 45.19 ms | 85.77 ms | 124.05 ms | 3156.56 ms | 501.51 ms | 4.38 ms |
| dec.v | 14.03 ms | 25.26 ms | 27.89 ms | 1406.11 ms | 169.63 ms | 3.68 ms |
| router.v | 65.80 ms | 67.11 ms | 138.25 ms | 3693.82 ms | 717.83 ms | 7.09 ms |
| cavlc.v | 137.25 ms | 241.30 ms | 370.33 ms | 9463.58 ms | 1410.29 ms | 8.23 ms |
| priority.v | 237.33 ms | 233.74 ms | 413.63 ms | 14.21 s | 13.48 s | 43.78 ms |
| adder.v | 379.93 ms | 348.20 ms | 797.78 ms | 26.38 s | 3776.22 ms | 65.25 ms |
| i2c.v | 257.95 ms | 475.16 ms | 578.53 ms | 14.94 s | 2830.91 ms | 26.12 ms |
| bar.v | 604.25 ms | 834.51 ms | 1159.79 ms | 63.07 s | 7122.56 ms | 58.93 ms |
| max.v | 934.92 ms | 1268.26 ms | 2225.22 ms | 68.91 s | 12.45 s | 81.98 ms |
| arbiter.v | 1855.19 ms | 1843.70 ms | 4028.27 ms | 166.80 s | 18.03 s | 175.26 ms |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| ctrl.v | 9.15x | 8.38x | 3.46x | 0.14x | 1.00x | 80.83x |
| int2float.v | 11.10x | 5.85x | 4.04x | 0.16x | 1.00x | 114.50x |
| dec.v | 12.09x | 6.71x | 6.08x | 0.12x | 1.00x | 46.12x |
| router.v | 10.91x | 10.70x | 5.19x | 0.19x | 1.00x | 101.31x |
| cavlc.v | 10.28x | 5.84x | 3.81x | 0.15x | 1.00x | 171.43x |
| priority.v | 56.81x | 57.68x | 32.60x | 0.95x | 1.00x | 308.00x |
| adder.v | 9.94x | 10.84x | 4.73x | 0.14x | 1.00x | 57.87x |
| i2c.v | 10.97x | 5.96x | 4.89x | 0.19x | 1.00x | 108.40x |
| bar.v | 11.79x | 8.54x | 6.14x | 0.11x | 1.00x | 120.86x |
| max.v | 13.31x | 9.81x | 5.59x | 0.18x | 1.00x | 151.83x |
| arbiter.v | 9.72x | 9.78x | 4.48x | 0.11x | 1.00x | 102.90x |

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

- **rx-prop (Wavefront BFS):** `12.63x`
- **rx-sweep (Linear Compiled):** `9.59x`
- **rx-oop (OOP Graph):** `5.67x`
- **Pure Python Engine:** `0.17x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `109.47x`

### Gate Evaluation Highlights

- **Reactor Sweep vs Propagate Total Evaluations Ratio:** `0.79x` (propagate performed more evaluations)

### Cross-Engine Comparisons

- **Cython Reactor (`rx-prop`) vs Pure Python:** `72.60x` faster
- **Cython Reactor (`rx-sweep`) vs Pure Python:** `55.12x` faster
- **Reactor Sweep vs Propagate Ratio:** `0.76x` (propagate faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | Instructions | Cycles | IPC | L1 Loads | L1 Misses | L2 Loads | L2 Misses | L3 Loads | DRAM Loads | Branches | Branch Misses |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| ctrl.v | rx-prop | 519.96M | 154.91M | 3.36 | 218.85M | 396.86K | 396.86K | 2.19K | 25.68K | 8.84K | 54.44M | 1.81M |
| ctrl.v | rx-sweep (Linear) | 351.30M | 166.81M | 2.11 | 165.01M | 245.71K | 245.71K | 3.55K | 26.09K | 21.23K | 71.84M | 3.45M |
| ctrl.v | rx-oop (OOP Engine) | 607.69M | 419.03M | 1.45 | 461.98M | 4.23M | 4.23M | 6.62K | 49.30K | 18.11K | 75.10M | 5.29M |
| ctrl.v | Pure Python Engine | 359.47M | 78.63M | 4.57 | 215.70M | 791.48K | 791.48K | 3.35K | 6.80K | 4.00K | 58.25M | 173.39K |
| ctrl.v | Icarus Verilog | 5.07B | 1.45B | 3.49 | 2.47B | 41.04M | 41.04M | 1.43K | 10.95K | 836.00 | 1.02B | 11.44M |
| ctrl.v | Verilator C++ | 3.55M | 15.98M | 0.22 | 24.67M | 36.53K | 36.53K | 545.00 | 26.11K | 31.00 | 4.66M | 67.79K |
| int2float.v | rx-prop | 538.00M | 155.80M | 3.45 | 218.83M | 1.90M | 1.90M | 2.27K | 32.10K | 11.40K | 54.09M | 1.64M |
| int2float.v | rx-sweep (Linear) | 472.98M | 298.22M | 1.59 | 259.79M | 1.54M | 1.54M | 1.71K | 32.18K | 18.08K | 92.93M | 6.88M |
| int2float.v | rx-oop (OOP Engine) | 619.46M | 439.14M | 1.41 | 490.37M | 7.96M | 7.96M | 10.00K | 71.22K | 45.55K | 75.89M | 5.34M |
| int2float.v | Pure Python Engine | 479.68M | 102.50M | 4.68 | 218.41M | 838.83K | 838.83K | 5.86K | 6.88K | 4.70K | 67.92M | 149.77K |
| int2float.v | Icarus Verilog | 5.70B | 1.80B | 3.17 | 2.83B | 62.04M | 62.04M | 2.81K | 13.57K | 3.49K | 1.14B | 15.37M |
| int2float.v | Verilator C++ | 5.86M | 9.27M | 0.63 | 28.21M | 39.86K | 39.86K | 452.00 | 26.77K | 81.00 | 4.32M | 152.45K |
| dec.v | rx-prop | 153.73M | 47.72M | 3.22 | 85.07M | 244.07K | 244.07K | 3.35K | 16.39K | 2.28K | 17.72M | 285.84K |
| dec.v | rx-sweep (Linear) | 202.56M | 74.86M | 2.71 | 90.83M | 369.65K | 369.65K | 366.00 | 19.54K | 2.08K | 45.95M | 1.09M |
| dec.v | rx-oop (OOP Engine) | 187.86M | 92.90M | 2.02 | 121.22M | 1.28M | 1.28M | 1.14K | 43.78K | 8.70K | 23.12M | 344.71K |
| dec.v | Pure Python Engine | 171.75M | 38.03M | 4.52 | 81.13M | 296.37K | 296.37K | 6.70K | 6.70K | 3.00K | 25.57M | 28.77K |
| dec.v | Icarus Verilog | 2.44B | 603.49M | 4.04 | 1.08B | 23.40M | 23.40M | 2.71K | 12.32K | 5.42K | 491.90M | 3.75M |
| dec.v | Verilator C++ | 10.84M | 8.60M | 1.26 | 33.47M | 35.61K | 35.61K | 1.18K | 27.62K | 301.00 | 4.36M | 43.25K |
| router.v | rx-prop | 666.42M | 259.83M | 2.56 | 315.96M | 4.08M | 4.08M | 87.86K | 2.39M | 2.35M | 88.31M | 4.19M |
| router.v | rx-sweep (Linear) | 609.84M | 265.50M | 2.30 | 295.77M | 3.81M | 3.81M | 91.67K | 2.21M | 2.11M | 132.88M | 4.12M |
| router.v | rx-oop (OOP Engine) | 730.41M | 522.36M | 1.40 | 564.00M | 12.61M | 12.61M | 63.23K | 2.36M | 2.04M | 108.46M | 7.44M |
| router.v | Pure Python Engine | 523.21M | 114.24M | 4.58 | 256.77M | 995.58K | 995.58K | 4.35K | 26.07K | 22.72K | 72.92M | 207.72K |
| router.v | Icarus Verilog | 9.34B | 2.57B | 3.63 | 4.39B | 79.43M | 79.43M | 9.59K | 17.79K | 6.39K | 1.85B | 17.87M |
| router.v | Verilator C++ | 60.66M | 21.40M | 2.83 | 38.92M | 72.62K | 72.62K | 3.24K | 152.45K | 467.00 | 5.68M | 27.30K |
| cavlc.v | rx-prop | 1.58B | 492.50M | 3.22 | 638.08M | 32.80M | 32.80M | 2.46K | 33.66K | 11.25K | 159.31M | 4.79M |
| cavlc.v | rx-sweep (Linear) | 1.32B | 862.14M | 1.53 | 688.93M | 41.36M | 41.36M | 2.02K | 31.06K | 9.42K | 254.34M | 19.22M |
| cavlc.v | rx-oop (OOP Engine) | 1.83B | 1.32B | 1.39 | 1.44B | 54.67M | 54.67M | 20.48K | 93.80K | 26.32K | 223.57M | 15.51M |
| cavlc.v | Pure Python Engine | 1.54B | 323.16M | 4.77 | 693.29M | 3.17M | 3.17M | 56.74K | 83.45K | 6.58K | 212.87M | 389.77K |
| cavlc.v | Icarus Verilog | 15.35B | 5.07B | 3.02 | 7.85B | 300.88M | 300.88M | 34.91K | 68.06K | 14.04K | 3.08B | 39.34M |
| cavlc.v | Verilator C++ | 46.22M | 23.80M | 1.94 | 30.95M | 18.98K | 18.98K | 132.00 | 31.50K | 1.46K | 4.97M | 125.71K |
| priority.v | rx-prop | 2.65B | 926.69M | 2.86 | 1.16B | 65.46M | 65.46M | 207.07K | 5.23M | 5.05M | 332.89M | 8.25M |
| priority.v | rx-sweep (Linear) | 2.23B | 916.15M | 2.43 | 963.38M | 66.68M | 66.68M | 253.71K | 5.81M | 5.69M | 455.87M | 13.42M |
| priority.v | rx-oop (OOP Engine) | 2.98B | 1.54B | 1.93 | 1.92B | 108.40M | 108.40M | 163.30K | 4.99M | 4.25M | 407.11M | 13.12M |
| priority.v | Pure Python Engine | 2.26B | 488.58M | 4.62 | 1.05B | 4.69M | 4.69M | 365.31K | 575.28K | 50.26K | 319.35M | 788.03K |
| priority.v | Icarus Verilog | 182.26B | 48.61B | 3.75 | 88.00B | 2.33B | 2.33B | 3.36M | 5.16M | 24.41K | 36.45B | 259.79M |
| priority.v | Verilator C++ | 180.17M | 148.94M | 1.21 | 128.49M | 93.77K | 93.77K | 3.00K | 155.36K | 8.30K | 15.87M | 673.45K |
| adder.v | rx-prop | 4.03B | 1.54B | 2.62 | 1.78B | 103.53M | 103.53M | 393.92K | 11.80M | 11.38M | 522.42M | 17.83M |
| adder.v | rx-sweep (Linear) | 3.54B | 1.42B | 2.49 | 1.56B | 110.86M | 110.86M | 416.85K | 12.53M | 12.02M | 725.80M | 18.38M |
| adder.v | rx-oop (OOP Engine) | 4.44B | 3.01B | 1.48 | 3.34B | 170.64M | 170.64M | 317.91K | 11.88M | 10.60M | 638.81M | 36.59M |
| adder.v | Pure Python Engine | 4.26B | 913.02M | 4.67 | 1.97B | 7.61M | 7.61M | 1.61M | 3.12M | 101.65K | 603.79M | 1.44M |
| adder.v | Icarus Verilog | 50.67B | 13.58B | 3.73 | 23.94B | 714.24M | 714.24M | 4.55M | 6.45M | 61.12K | 9.97B | 68.34M |
| adder.v | Verilator C++ | 249.73M | 223.87M | 1.12 | 167.83M | 229.85K | 229.85K | 3.13K | 154.77K | 50.29K | 13.66M | 1.24M |
| i2c.v | rx-prop | 2.76B | 1.02B | 2.70 | 1.23B | 88.65M | 88.65M | 342.41K | 7.14M | 6.88M | 334.42M | 12.34M |
| i2c.v | rx-sweep (Linear) | 2.77B | 1.82B | 1.52 | 1.39B | 98.26M | 98.26M | 345.47K | 7.22M | 7.13M | 569.37M | 39.06M |
| i2c.v | rx-oop (OOP Engine) | 3.05B | 2.15B | 1.42 | 2.34B | 132.80M | 132.80M | 179.97K | 5.58M | 4.79M | 434.67M | 26.29M |
| i2c.v | Pure Python Engine | 2.38B | 514.30M | 4.63 | 1.07B | 4.58M | 4.58M | 862.42K | 1.34M | 62.51K | 331.17M | 716.37K |
| i2c.v | Icarus Verilog | 35.13B | 10.19B | 3.45 | 16.86B | 547.72M | 547.72M | 1.55M | 2.24M | 50.28K | 6.98B | 64.09M |
| i2c.v | Verilator C++ | 226.51M | 91.79M | 2.47 | 110.02M | 102.69K | 102.69K | 2.54K | 121.81K | 54.79K | 14.75M | 1.10M |
| bar.v | rx-prop | 8.56B | 2.24B | 3.82 | 3.38B | 312.54M | 312.54M | 77.32K | 5.28M | 5.00M | 883.86M | 4.66M |
| bar.v | rx-sweep (Linear) | 5.89B | 3.06B | 1.92 | 2.92B | 198.76M | 198.76M | 318.91K | 4.19M | 3.79M | 1.16B | 61.88M |
| bar.v | rx-oop (OOP Engine) | 9.77B | 4.24B | 2.31 | 5.50B | 475.62M | 475.62M | 1.73M | 7.99M | 4.62M | 1.24B | 8.71M |
| bar.v | Pure Python Engine | 1.79B | 408.89M | 4.39 | 839.28M | 4.58M | 4.58M | 2.01M | 3.09M | 20.34K | 253.88M | 437.67K |
| bar.v | Icarus Verilog | 93.90B | 25.55B | 3.67 | 43.31B | 2.36B | 2.36B | 384.66M | 505.90M | 70.68K | 18.86B | 66.49M |
| bar.v | Verilator C++ | 340.33M | 207.58M | 1.64 | 214.70M | 200.43K | 200.43K | 2.99K | 85.59K | 5.97K | 25.09M | 1.52M |
| max.v | rx-prop | 11.22B | 3.76B | 2.99 | 4.70B | 447.35M | 447.35M | 1.17M | 27.78M | 26.88M | 1.34B | 26.88M |
| max.v | rx-sweep (Linear) | 8.22B | 4.90B | 1.68 | 4.24B | 311.65M | 311.65M | 1.39M | 27.45M | 26.15M | 1.69B | 98.42M |
| max.v | rx-oop (OOP Engine) | 12.57B | 8.35B | 1.51 | 9.25B | 667.78M | 667.78M | 17.17M | 48.60M | 21.67M | 1.72B | 79.64M |
| max.v | Pure Python Engine | 2.06B | 462.45M | 4.46 | 935.63M | 4.37M | 4.37M | 1.87M | 3.16M | 45.91K | 289.86M | 529.40K |
| max.v | Icarus Verilog | 146.42B | 44.72B | 3.27 | 73.27B | 2.68B | 2.68B | 465.76M | 669.20M | 104.76K | 28.85B | 239.94M |
| max.v | Verilator C++ | 788.43M | 296.06M | 2.66 | 372.70M | 363.92K | 363.92K | 5.50K | 286.90K | 216.68K | 52.95M | 761.44K |
| arbiter.v | rx-prop | 21.13B | 6.82B | 3.10 | 8.39B | 686.33M | 686.33M | 36.53M | 197.98M | 11.63M | 2.16B | 21.96M |
| arbiter.v | rx-sweep (Linear) | 21.15B | 6.78B | 3.12 | 7.57B | 725.11M | 725.11M | 56.66M | 290.19M | 12.17M | 4.20B | 64.55M |
| arbiter.v | rx-oop (OOP Engine) | 24.25B | 14.58B | 1.66 | 14.51B | 1.37B | 1.37B | 482.69M | 825.47M | 10.82M | 3.01B | 46.05M |
| arbiter.v | Pure Python Engine | 2.14B | 525.64M | 4.07 | 966.42M | 6.25M | 6.25M | 3.45M | 5.51M | 450.07K | 299.69M | 184.69K |
| arbiter.v | Icarus Verilog | 205.62B | 64.71B | 3.18 | 97.19B | 5.89B | 5.89B | 3.22B | 5.61B | 404.45K | 41.16B | 99.37M |
| arbiter.v | Verilator C++ | 719.73M | 624.69M | 1.15 | 545.22M | 252.84K | 252.84K | 6.77K | 238.46K | 81.46K | 25.55M | 3.83M |
