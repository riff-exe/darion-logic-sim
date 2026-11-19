# Master test reports (Zen 5, Ryzen 7 9700X)

Full-engine reports from `tests/master_test.py`, one section per suite: memory footprint, load and compile time, wall-clock and speedup of rx-prop / rx-sweep / rx-oop / Icarus / Verilator, evaluation counts and PMU counters. ITC99, OpenCores and DMA were re-run on 2026-10-22 with the nonblocking cell library for Verilator.

Contents: ITC99, Opencores, DMA, EPFL, EPFL_large, ISCAS85, ISCAS89, Hyp.

## ITC99

**Execution Parameters:**
- **Target Suite / Path:** `tests/IWLS2005/itc99`
- **Circuits Benchmarked:** 21
- **Simulation Vectors (Phase 3):** 50,000 (Warmup: 10)
- **Verification Vectors (Phase 2):** 100
- **Hardware Profiler:** Linux `perf` kernel PMU counters
- **Note (2026-10-22):** re-run after the Verilator library fix: Verilator now compiles `iwls_sequential_harness.verilator_gsclib()` (the cell library with its sequential UDPs as nonblocking modules), because Verilator 5.052 lowers the original UDP flops to blocking assignments, which is order-dependent and slow. Icarus uses the original library; Darion simulates every flop as the 10-gate NAND master-slave of `tests/src/DFFSR.json`, so the flop models differ between the three tools (not a same-netlist comparison). The previous report (blocking-UDP Verilator) is in git history.

---

### 1. Zero-Testbench Memory Footprint (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| b02.v | 52 | 0.53 MB (28.1 MB peak) | N/A | 0.38 MB (8.3 MB peak) | 0.70 MB (4.4 MB peak) |
| b01.v | 101 | 0.64 MB (28.2 MB peak) | N/A | 0.49 MB (8.4 MB peak) | 0.70 MB (4.4 MB peak) |
| b06.v | 100 | 0.71 MB (28.3 MB peak) | N/A | 0.57 MB (8.4 MB peak) | 0.70 MB (4.4 MB peak) |
| b08.v | 309 | 1.04 MB (28.6 MB peak) | N/A | 1.17 MB (9.1 MB peak) | 0.71 MB (4.4 MB peak) |
| b09.v | 331 | 1.22 MB (30.7 MB peak) | N/A | 1.33 MB (9.2 MB peak) | 0.69 MB (4.4 MB peak) |
| b10.v | 417 | 1.12 MB (28.7 MB peak) | N/A | 1.46 MB (9.3 MB peak) | 0.71 MB (4.4 MB peak) |
| b03.v | 549 | 1.47 MB (29.0 MB peak) | N/A | 1.81 MB (9.7 MB peak) | 0.74 MB (4.4 MB peak) |
| b13.v | 540 | 1.80 MB (29.4 MB peak) | N/A | 2.11 MB (10.0 MB peak) | 0.75 MB (4.4 MB peak) |
| b07.v | 859 | 2.04 MB (29.6 MB peak) | N/A | 3.07 MB (10.9 MB peak) | 0.71 MB (4.4 MB peak) |
| b11.v | 1,046 | 1.91 MB (29.5 MB peak) | N/A | 3.09 MB (11.0 MB peak) | 0.82 MB (4.4 MB peak) |
| b04.v | 1,259 | 2.59 MB (30.2 MB peak) | N/A | 3.73 MB (11.6 MB peak) | 0.70 MB (4.4 MB peak) |
| b05.v | 1,292 | 2.09 MB (29.7 MB peak) | N/A | 3.85 MB (11.7 MB peak) | 0.75 MB (4.4 MB peak) |
| b12.v | 2,937 | 4.94 MB (32.5 MB peak) | N/A | 8.77 MB (16.7 MB peak) | 0.76 MB (4.5 MB peak) |
| b14.v | 10,624 | 15.31 MB (42.7 MB peak) | N/A | 36.80 MB (44.7 MB peak) | 0.92 MB (4.6 MB peak) |
| b15.v | 17,594 | 23.77 MB (53.2 MB peak) | N/A | 56.73 MB (64.7 MB peak) | 1.01 MB (4.7 MB peak) |
| b21.v | 23,092 | 28.02 MB (58.6 MB peak) | N/A | 78.53 MB (86.4 MB peak) | 1.05 MB (4.7 MB peak) |
| b20.v | 23,839 | 27.02 MB (58.0 MB peak) | N/A | 79.95 MB (87.8 MB peak) | 1.07 MB (4.8 MB peak) |
| b22.v | 34,903 | 34.62 MB (65.9 MB peak) | N/A | 119.02 MB (126.9 MB peak) | 1.00 MB (4.7 MB peak) |
| b17.v | 52,250 | 59.12 MB (92.1 MB peak) | N/A | 172.98 MB (180.8 MB peak) | 1.29 MB (5.0 MB peak) |
| b18.v | 132,940 | 137.55 MB (185.2 MB peak) | N/A | 429.06 MB (437.0 MB peak) | 1.78 MB (5.5 MB peak) |
| b19.v | 257,489 | 264.50 MB (335.1 MB peak) | N/A | 827.90 MB (835.8 MB peak) | 2.66 MB (6.4 MB peak) |

---

### 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| b02.v | 52 | 0.15 ms (0.013 ms opt) | N/A | 4.32 ms | 2.50 s |
| b01.v | 101 | 0.17 ms (0.017 ms opt) | N/A | 4.79 ms | 2.51 s |
| b06.v | 100 | 0.20 ms (0.021 ms opt) | N/A | 4.96 ms | 2.50 s |
| b08.v | 309 | 0.48 ms (0.058 ms opt) | N/A | 7.48 ms | 2.54 s |
| b09.v | 331 | 0.56 ms (0.063 ms opt) | N/A | 7.98 ms | 2.53 s |
| b10.v | 417 | 0.50 ms (0.068 ms opt) | N/A | 8.45 ms | 2.58 s |
| b03.v | 549 | 0.69 ms (0.083 ms opt) | N/A | 10.16 ms | 2.56 s |
| b13.v | 540 | 0.97 ms (0.114 ms opt) | N/A | 10.84 ms | 2.61 s |
| b07.v | 859 | 1.12 ms (0.140 ms opt) | N/A | 14.90 ms | 2.65 s |
| b11.v | 1,046 | 1.03 ms (0.134 ms opt) | N/A | 16.30 ms | 2.60 s |
| b04.v | 1,259 | 1.50 ms (0.187 ms opt) | N/A | 19.24 ms | 2.68 s |
| b05.v | 1,292 | 1.22 ms (0.165 ms opt) | N/A | 18.87 ms | 2.66 s |
| b12.v | 2,937 | 3.20 ms (0.395 ms opt) | N/A | 40.48 ms | 2.93 s |
| b14.v | 10,624 | 10.08 ms (1.249 ms opt) | N/A | 173.71 ms | 4.74 s |
| b15.v | 17,594 | 17.42 ms (2.428 ms opt) | N/A | 278.12 ms | 6.95 s |
| b21.v | 23,092 | 22.20 ms (3.545 ms opt) | N/A | 401.02 ms | 8.10 s |
| b20.v | 23,839 | 23.38 ms (3.947 ms opt) | N/A | 406.81 ms | 8.67 s |
| b22.v | 34,903 | 35.86 ms (8.218 ms opt) | N/A | 614.18 ms | 12.40 s |
| b17.v | 52,250 | 66.34 ms (15.768 ms opt) | N/A | 936.95 ms | 20.26 s |
| b18.v | 132,940 | 253.64 ms (46.697 ms opt) | N/A | 2.36 s | 59.78 s |
| b19.v | 257,489 | 571.30 ms (107.646 ms opt) | N/A | 4.65 s | 139.13 s |

---

### 3. High-Throughput Simulation Performance (Phase 3)

#### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| b02.v | 18.37 ms | 14.00 ms | 31.22 ms | N/A | 147.92 ms | 3.58 ms |
| b01.v | 25.84 ms | 20.62 ms | 51.11 ms | N/A | 179.54 ms | 3.59 ms |
| b06.v | 34.01 ms | 28.71 ms | 68.23 ms | N/A | 158.53 ms | 3.72 ms |
| b08.v | 51.22 ms | 54.63 ms | 96.56 ms | N/A | 253.39 ms | 8.10 ms |
| b09.v | 58.16 ms | 53.61 ms | 102.09 ms | N/A | 249.56 ms | 5.00 ms |
| b10.v | 69.57 ms | 71.99 ms | 161.86 ms | N/A | 429.71 ms | 9.08 ms |
| b03.v | 91.68 ms | 93.48 ms | 197.65 ms | N/A | 274.19 ms | 5.99 ms |
| b13.v | 115.78 ms | 114.59 ms | 192.99 ms | N/A | 364.81 ms | 7.85 ms |
| b07.v | 106.11 ms | 110.47 ms | 193.04 ms | N/A | 302.15 ms | 20.27 ms |
| b11.v | 120.84 ms | 124.31 ms | 311.16 ms | N/A | 391.33 ms | 19.66 ms |
| b04.v | 272.61 ms | 297.83 ms | 577.90 ms | N/A | 1404.76 ms | 29.36 ms |
| b05.v | 77.55 ms | 104.37 ms | 157.74 ms | N/A | 191.01 ms | 29.80 ms |
| b12.v | 286.39 ms | 304.60 ms | 462.65 ms | N/A | 889.25 ms | 50.72 ms |
| b14.v | 2934.68 ms | 2044.79 ms | 6956.60 ms | N/A | 6630.32 ms | 247.61 ms |
| b15.v | 1381.66 ms | 1588.27 ms | 2807.82 ms | N/A | 5449.71 ms | 306.21 ms |
| b21.v | 3731.71 ms | 2999.47 ms | 8982.68 ms | N/A | 8624.67 ms | 554.89 ms |
| b20.v | 4095.24 ms | 3621.43 ms | 10.08 s | N/A | 9953.74 ms | 606.18 ms |
| b22.v | 7853.97 ms | 6221.34 ms | 19.58 s | N/A | 20.15 s | 795.72 ms |
| b17.v | 4608.05 ms | 5248.30 ms | 9387.13 ms | N/A | 13.26 s | 893.88 ms |
| b18.v | 15.72 s | 14.93 s | 33.12 s | N/A | 103.42 s | 3055.64 ms |
| b19.v | 26.45 s | 27.04 s | 53.34 s | N/A | 148.01 s | 5905.81 ms |

#### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| b02.v | 8.05x | 10.57x | 4.74x | N/A | 1.00x | 41.29x |
| b01.v | 6.95x | 8.71x | 3.51x | N/A | 1.00x | 50.06x |
| b06.v | 4.66x | 5.52x | 2.32x | N/A | 1.00x | 42.65x |
| b08.v | 4.95x | 4.64x | 2.62x | N/A | 1.00x | 31.27x |
| b09.v | 4.29x | 4.66x | 2.44x | N/A | 1.00x | 49.96x |
| b10.v | 6.18x | 5.97x | 2.65x | N/A | 1.00x | 47.35x |
| b03.v | 2.99x | 2.93x | 1.39x | N/A | 1.00x | 45.80x |
| b13.v | 3.15x | 3.18x | 1.89x | N/A | 1.00x | 46.46x |
| b07.v | 2.85x | 2.74x | 1.57x | N/A | 1.00x | 14.90x |
| b11.v | 3.24x | 3.15x | 1.26x | N/A | 1.00x | 19.90x |
| b04.v | 5.15x | 4.72x | 2.43x | N/A | 1.00x | 47.84x |
| b05.v | 2.46x | 1.83x | 1.21x | N/A | 1.00x | 6.41x |
| b12.v | 3.11x | 2.92x | 1.92x | N/A | 1.00x | 17.53x |
| b14.v | 2.26x | 3.24x | 0.95x | N/A | 1.00x | 26.78x |
| b15.v | 3.94x | 3.43x | 1.94x | N/A | 1.00x | 17.80x |
| b21.v | 2.31x | 2.88x | 0.96x | N/A | 1.00x | 15.54x |
| b20.v | 2.43x | 2.75x | 0.99x | N/A | 1.00x | 16.42x |
| b22.v | 2.57x | 3.24x | 1.03x | N/A | 1.00x | 25.32x |
| b17.v | 2.88x | 2.53x | 1.41x | N/A | 1.00x | 14.83x |
| b18.v | 6.58x | 6.92x | 3.12x | N/A | 1.00x | 33.84x |
| b19.v | 5.60x | 5.47x | 2.77x | N/A | 1.00x | 25.06x |

#### Total Gate Evaluations

| Circuit | Gates | rx-prop Evals | rx-sweep Evals | rx-oop Evals | Pure Python Evals |
|:---|---:|---:|---:|---:|---:|
| b02.v | 52 | 7,941,850 | 6,175,688 | 7,948,584 | N/A |
| b01.v | 101 | 11,224,069 | 8,635,502 | 11,515,676 | N/A |
| b06.v | 100 | 16,480,200 | 13,046,519 | 17,072,476 | N/A |
| b08.v | 309 | 24,540,857 | 22,386,735 | 24,667,328 | N/A |
| b09.v | 331 | 29,142,996 | 26,427,389 | 29,143,065 | N/A |
| b10.v | 417 | 29,852,475 | 23,471,435 | 29,922,007 | N/A |
| b03.v | 549 | 45,067,585 | 36,229,120 | 44,978,925 | N/A |
| b13.v | 540 | 52,595,027 | 50,521,445 | 53,616,228 | N/A |
| b07.v | 859 | 54,724,837 | 48,711,593 | 54,757,552 | N/A |
| b11.v | 1,046 | 53,469,298 | 39,657,746 | 55,966,154 | N/A |
| b04.v | 1,259 | 103,641,535 | 93,188,210 | 104,151,250 | N/A |
| b05.v | 1,292 | 41,330,601 | 37,554,924 | 41,447,568 | N/A |
| b12.v | 2,937 | 124,645,762 | 120,094,694 | 124,671,592 | N/A |
| b14.v | 10,624 | 895,716,536 | 570,794,848 | 897,512,210 | N/A |
| b15.v | 17,594 | 614,286,344 | 525,645,178 | 625,279,820 | N/A |
| b21.v | 23,092 | 1,177,457,505 | 837,390,518 | 1,200,077,577 | N/A |
| b20.v | 23,839 | 1,264,117,541 | 974,914,071 | 1,267,767,760 | N/A |
| b22.v | 34,903 | 2,149,329,575 | 1,527,593,309 | 2,227,894,840 | N/A |
| b17.v | 52,250 | 1,795,910,135 | 1,574,202,709 | 1,811,990,766 | N/A |
| b18.v | 132,940 | 5,042,190,066 | 3,786,300,169 | 5,065,773,791 | N/A |
| b19.v | 257,489 | 8,756,077,937 | 7,269,614,276 | 8,814,481,416 | N/A |

#### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `3.81x`
- **rx-sweep (Linear Compiled):** `3.96x`
- **rx-oop (OOP Graph):** `1.85x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `26.63x`

#### Gate Evaluation Highlights

- **Reactor Sweep vs Propagate Total Evaluations Ratio:** `0.82x` (propagate performed more evaluations)

#### Cross-Engine Comparisons

- **Reactor Sweep vs Propagate Ratio:** `1.04x` (sweep faster)

---

### 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | Instructions | Cycles | IPC | L1 Loads | L1 Misses | L2 Loads | L2 Misses | L3 Loads | DRAM Loads | Branches | Branch Misses |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| b02.v | rx-prop | 268.91M | 60.31M | 4.46 | 106.93M | 26.75K | 26.75K | 959.00 | 28.19K | 11.88K | 29.12M | 67.19K |
| b02.v | rx-sweep (Linear) | 254.25M | 52.86M | 4.81 | 92.77M | 579.06K | 579.06K | 24.11K | 26.78K | 25.91K | 46.04M | 72.77K |
| b02.v | rx-oop (OOP Engine) | 284.31M | 104.82M | 2.71 | 202.64M | 152.14K | 152.14K | 4.45K | 48.18K | 17.68K | 38.46M | 288.93K |
| b02.v | Icarus Verilog | 2.09B | 545.55M | 3.83 | 990.06M | 1.20M | 1.20M | 12.74K | 100.72K | 10.04K | 405.94M | 3.54M |
| b02.v | Verilator C++ | 22.71K | 4.94M | 0.00 | 8.02M | 13.11K | 13.11K | 335.00 | 23.41K | 0.00 | 3.52M | 15.62K |
| b01.v | rx-prop | 360.61M | 84.79M | 4.25 | 156.58M | 95.09K | 95.09K | 2.31K | 35.64K | 14.73K | 38.27M | 165.51K |
| b01.v | rx-sweep (Linear) | 322.39M | 70.88M | 4.55 | 144.72M | 808.91K | 808.91K | 14.77K | 25.21K | 24.28K | 66.32M | 283.58K |
| b01.v | rx-oop (OOP Engine) | 424.87M | 172.45M | 2.46 | 301.68M | 441.56K | 441.56K | 6.30K | 59.47K | 7.79K | 54.82M | 976.87K |
| b01.v | Icarus Verilog | 2.57B | 663.32M | 3.88 | 1.21B | 6.05M | 6.05M | 21.09K | 90.88K | 14.12K | 505.81M | 4.05M |
| b01.v | Verilator C++ | 11.60M | 8.81M | 1.32 | 20.59M | 27.59K | 27.59K | 1.27K | 1.27K | 0.00 | 7.01M | 23.62K |
| b06.v | rx-prop | 525.99M | 118.39M | 4.44 | 214.45M | 70.77K | 70.77K | 2.28K | 35.84K | 18.36K | 54.05M | 143.07K |
| b06.v | rx-sweep (Linear) | 469.87M | 102.38M | 4.59 | 195.57M | 843.50K | 843.50K | 34.10K | 45.37K | 25.93K | 93.57M | 411.69K |
| b06.v | rx-oop (OOP Engine) | 623.30M | 234.82M | 2.65 | 422.44M | 753.61K | 753.61K | 7.51K | 64.86K | 26.78K | 77.25M | 1.03M |
| b06.v | Icarus Verilog | 2.50B | 599.73M | 4.17 | 1.12B | 3.28M | 3.28M | 20.53K | 75.47K | 1.63K | 481.28M | 3.15M |
| b06.v | Verilator C++ | 3.92M | 8.39M | 0.47 | 29.67M | 16.78K | 16.78K | 1.78K | 38.89K | 311.00 | 8.72M | 52.78K |
| b08.v | rx-prop | 793.79M | 192.50M | 4.12 | 320.14M | 1.53M | 1.53M | 24.20K | 61.34K | 28.60K | 85.40M | 516.04K |
| b08.v | rx-sweep (Linear) | 906.85M | 202.63M | 4.48 | 336.31M | 2.49M | 2.49M | 30.96K | 338.03K | 312.29K | 191.34M | 1.35M |
| b08.v | rx-oop (OOP Engine) | 901.12M | 359.57M | 2.51 | 568.88M | 6.83M | 6.83M | 29.36K | 106.96K | 65.21K | 115.85M | 1.60M |
| b08.v | Icarus Verilog | 3.85B | 985.23M | 3.91 | 1.72B | 29.28M | 29.28M | 40.53K | 104.78K | 36.20K | 749.21M | 5.51M |
| b08.v | Verilator C++ | 56.79M | 24.09M | 2.36 | 35.27M | 4.13K | 4.13K | 63.00 | 24.47K | 31.00 | 7.29M | 13.60K |
| b09.v | rx-prop | 838.12M | 206.01M | 4.07 | 346.92M | 1.09M | 1.09M | 7.13K | 26.48K | 15.84K | 83.85M | 234.33K |
| b09.v | rx-sweep (Linear) | 978.87M | 193.74M | 5.05 | 328.01M | 1.50M | 1.50M | 25.16K | 36.66K | 18.40K | 209.26M | 536.38K |
| b09.v | rx-oop (OOP Engine) | 985.35M | 362.00M | 2.72 | 602.52M | 10.47M | 10.47M | 29.83K | 100.69K | 35.68K | 118.87M | 618.54K |
| b09.v | Icarus Verilog | 3.88B | 936.73M | 4.14 | 1.76B | 58.20M | 58.20M | 38.16K | 69.43K | 21.17K | 748.23M | 3.28M |
| b09.v | Verilator C++ | 10.63M | 9.88M | 1.08 | 27.45M | 44.85K | 44.85K | 864.00 | 18.57K | 1.58K | 5.97M | 18.42K |
| b10.v | rx-prop | 992.11M | 263.28M | 3.77 | 398.18M | 3.70M | 3.70M | 37.66K | 100.03K | 75.03K | 108.75M | 1.21M |
| b10.v | rx-sweep (Linear) | 981.44M | 266.84M | 3.68 | 369.19M | 3.81M | 3.81M | 51.22K | 793.16K | 765.62K | 199.67M | 2.50M |
| b10.v | rx-oop (OOP Engine) | 1.05B | 578.36M | 1.82 | 805.13M | 13.18M | 13.18M | 49.05K | 197.74K | 141.41K | 139.94M | 5.20M |
| b10.v | Icarus Verilog | 6.03B | 1.60B | 3.78 | 2.84B | 86.53M | 86.53M | 131.48K | 311.97K | 43.34K | 1.20B | 9.00M |
| b10.v | Verilator C++ | 58.63M | 24.84M | 2.36 | 52.46M | 12.80K | 12.80K | 2.92K | 52.63K | 915.00 | 7.54M | 78.55K |
| b03.v | rx-prop | 1.34B | 335.71M | 3.99 | 560.29M | 8.95M | 8.95M | 33.48K | 88.66K | 72.40K | 136.22M | 727.44K |
| b03.v | rx-sweep (Linear) | 1.46B | 351.64M | 4.16 | 475.99M | 12.97M | 12.97M | 127.34K | 994.86K | 946.59K | 279.70M | 2.08M |
| b03.v | rx-oop (OOP Engine) | 1.53B | 712.09M | 2.15 | 1.04B | 31.20M | 31.20M | 24.57K | 132.19K | 61.88K | 181.93M | 4.77M |
| b03.v | Icarus Verilog | 4.00B | 1.05B | 3.81 | 1.85B | 60.06M | 60.06M | 84.22K | 189.84K | 66.48K | 788.52M | 5.24M |
| b03.v | Verilator C++ | 38.43M | 12.59M | 3.05 | 50.56M | 23.57K | 23.57K | 1.49K | 44.18K | 997.00 | 5.94M | 21.32K |
| b13.v | rx-prop | 1.56B | 419.90M | 3.70 | 671.72M | 18.23M | 18.23M | 43.83K | 447.18K | 422.55K | 161.96M | 680.80K |
| b13.v | rx-sweep (Linear) | 1.94B | 430.24M | 4.50 | 638.45M | 26.61M | 26.61M | 51.87K | 383.81K | 338.75K | 396.48M | 1.69M |
| b13.v | rx-oop (OOP Engine) | 1.82B | 692.59M | 2.63 | 1.12B | 65.80M | 65.80M | 69.22K | 515.40K | 376.80K | 228.18M | 1.28M |
| b13.v | Icarus Verilog | 5.51B | 1.39B | 3.97 | 2.48B | 83.47M | 83.47M | 133.07K | 314.06K | 67.52K | 1.07B | 7.58M |
| b13.v | Verilator C++ | 61.02M | 22.57M | 2.70 | 39.93M | 5.62K | 5.62K | 100.00 | 23.23K | 436.00 | 6.95M | 39.41K |
| b07.v | rx-prop | 1.57B | 374.17M | 4.20 | 623.68M | 12.86M | 12.86M | 3.64K | 35.49K | 25.15K | 143.54M | 347.46K |
| b07.v | rx-sweep (Linear) | 1.88B | 392.33M | 4.79 | 608.75M | 43.23M | 43.23M | 6.22K | 32.16K | 26.41K | 396.63M | 814.02K |
| b07.v | rx-oop (OOP Engine) | 1.81B | 687.88M | 2.63 | 1.10B | 60.14M | 60.14M | 19.84K | 89.45K | 64.31K | 216.60M | 1.55M |
| b07.v | Icarus Verilog | 4.64B | 1.15B | 4.03 | 2.17B | 87.89M | 87.89M | 245.25K | 505.29K | 52.94K | 935.57M | 4.31M |
| b07.v | Verilator C++ | 105.94M | 70.46M | 1.50 | 78.31M | 13.06K | 13.06K | 2.67K | 2.73K | 5.00 | 8.15M | 35.46K |
| b11.v | rx-prop | 1.61B | 434.48M | 3.72 | 651.62M | 18.92M | 18.92M | 29.68K | 78.53K | 51.55K | 157.31M | 2.03M |
| b11.v | rx-sweep (Linear) | 1.77B | 455.56M | 3.89 | 576.24M | 37.45M | 37.45M | 33.16K | 615.42K | 588.06K | 373.26M | 3.40M |
| b11.v | rx-oop (OOP Engine) | 1.90B | 1.10B | 1.72 | 1.49B | 49.41M | 49.41M | 48.78K | 163.72K | 114.16K | 238.88M | 10.74M |
| b11.v | Icarus Verilog | 5.43B | 1.52B | 3.57 | 2.52B | 72.04M | 72.04M | 77.16K | 202.62K | 50.59K | 1.06B | 9.45M |
| b11.v | Verilator C++ | 100.21M | 64.86M | 1.54 | 70.62M | 17.53K | 17.53K | 1.48K | 3.67K | 336.00 | 7.73M | 9.72K |
| b04.v | rx-prop | 3.08B | 990.17M | 3.11 | 1.26B | 84.04M | 84.04M | 66.63K | 632.20K | 581.67K | 293.69M | 7.94M |
| b04.v | rx-sweep (Linear) | 3.44B | 1.08B | 3.20 | 1.24B | 118.75M | 118.75M | 77.94K | 828.22K | 766.20K | 666.74M | 13.10M |
| b04.v | rx-oop (OOP Engine) | 3.56B | 2.09B | 1.71 | 2.57B | 144.14M | 144.14M | 177.86K | 845.97K | 576.72K | 426.87M | 20.57M |
| b04.v | Icarus Verilog | 16.95B | 5.16B | 3.29 | 8.41B | 261.36M | 261.36M | 2.59M | 4.35M | 119.43K | 3.34B | 37.66M |
| b04.v | Verilator C++ | 180.10M | 102.12M | 1.76 | 109.30M | 42.20K | 42.20K | 444.00 | 21.16K | 253.00 | 8.71M | 27.01K |
| b05.v | rx-prop | 1.18B | 270.73M | 4.34 | 489.88M | 5.39M | 5.39M | 11.83K | 43.76K | 25.67K | 112.82M | 264.43K |
| b05.v | rx-sweep (Linear) | 1.82B | 377.99M | 4.81 | 511.54M | 51.73M | 51.73M | 10.93K | 57.89K | 32.18K | 387.03M | 844.38K |
| b05.v | rx-oop (OOP Engine) | 1.40B | 562.17M | 2.49 | 918.61M | 30.77M | 30.77M | 72.80K | 169.18K | 60.19K | 167.18M | 2.24M |
| b05.v | Icarus Verilog | 3.21B | 788.85M | 4.08 | 1.43B | 53.84M | 53.84M | 107.86K | 205.34K | 50.68K | 627.92M | 2.97M |
| b05.v | Verilator C++ | 128.68M | 109.30M | 1.18 | 103.58M | 27.92K | 27.92K | 1.39K | 4.67K | 3.00 | 8.48M | 37.85K |
| b12.v | rx-prop | 3.64B | 1.04B | 3.51 | 1.43B | 137.75M | 137.75M | 77.47K | 140.17K | 46.02K | 338.85M | 1.27M |
| b12.v | rx-sweep (Linear) | 5.17B | 1.11B | 4.66 | 1.51B | 226.39M | 226.39M | 123.09K | 971.39K | 898.92K | 1.11B | 3.93M |
| b12.v | rx-oop (OOP Engine) | 4.17B | 1.66B | 2.51 | 2.61B | 248.47M | 248.47M | 164.09K | 457.17K | 101.61K | 493.93M | 5.99M |
| b12.v | Icarus Verilog | 12.85B | 3.40B | 3.78 | 6.01B | 260.14M | 260.14M | 7.68M | 13.21M | 279.06K | 2.52B | 15.70M |
| b12.v | Verilator C++ | 308.52M | 179.55M | 1.72 | 211.15M | 31.05K | 31.05K | 1.33K | 3.66K | 96.00 | 8.35M | 41.22K |
| b14.v | rx-prop | 26.02B | 10.54B | 2.47 | 10.60B | 1.07B | 1.07B | 15.82M | 37.20M | 2.67M | 2.37B | 141.22M |
| b14.v | rx-sweep (Linear) | 22.09B | 7.35B | 3.01 | 7.42B | 995.62M | 995.62M | 10.05M | 28.09M | 3.46M | 3.77B | 90.91M |
| b14.v | rx-oop (OOP Engine) | 29.99B | 24.92B | 1.20 | 25.14B | 1.53B | 1.53B | 129.38M | 217.27M | 3.22M | 3.54B | 306.92M |
| b14.v | Icarus Verilog | 69.75B | 24.77B | 2.82 | 36.30B | 1.58B | 1.58B | 371.87M | 521.61M | 1.72M | 13.82B | 153.68M |
| b14.v | Verilator C++ | 1.26B | 887.61M | 1.41 | 939.41M | 70.96K | 70.96K | 1.13K | 47.48K | 42.56K | 9.86M | 50.82K |
| b15.v | rx-prop | 17.69B | 5.02B | 3.53 | 6.95B | 731.16M | 731.16M | 13.05M | 28.61M | 3.25M | 1.60B | 9.57M |
| b15.v | rx-sweep (Linear) | 24.45B | 5.75B | 4.25 | 6.99B | 1.15B | 1.15B | 22.73M | 92.14M | 3.73M | 5.22B | 28.02M |
| b15.v | rx-oop (OOP Engine) | 20.57B | 10.11B | 2.03 | 13.89B | 1.16B | 1.16B | 84.97M | 178.64M | 2.40M | 2.44B | 55.12M |
| b15.v | Icarus Verilog | 70.13B | 21.05B | 3.33 | 32.55B | 1.36B | 1.36B | 526.31M | 982.00M | 1.63M | 13.64B | 61.05M |
| b15.v | Verilator C++ | 1.98B | 1.11B | 1.79 | 1.20B | 102.34K | 102.34K | 2.44K | 16.16K | 2.09K | 14.20M | 121.44K |
| b21.v | rx-prop | 33.95B | 13.44B | 2.53 | 13.68B | 1.44B | 1.44B | 112.83M | 220.97M | 2.72M | 3.06B | 147.84M |
| b21.v | rx-sweep (Linear) | 36.01B | 10.80B | 3.34 | 11.09B | 1.69B | 1.69B | 86.25M | 403.84M | 3.30M | 6.86B | 100.65M |
| b21.v | rx-oop (OOP Engine) | 39.78B | 32.26B | 1.23 | 32.69B | 2.17B | 2.17B | 434.25M | 850.38M | 2.89M | 4.69B | 342.96M |
| b21.v | Icarus Verilog | 92.08B | 32.87B | 2.80 | 46.95B | 2.04B | 2.04B | 675.76M | 1.17B | 2.36M | 18.19B | 168.37M |
| b21.v | Verilator C++ | 2.74B | 1.99B | 1.38 | 2.17B | 121.58K | 121.58K | 6.56K | 132.37K | 123.78K | 9.17M | 44.56K |
| b20.v | rx-prop | 36.66B | 14.74B | 2.49 | 14.83B | 1.57B | 1.57B | 129.29M | 264.80M | 2.84M | 3.31B | 172.85M |
| b20.v | rx-sweep (Linear) | 40.40B | 13.03B | 3.10 | 12.88B | 1.92B | 1.92B | 109.95M | 492.92M | 2.46M | 7.38B | 136.78M |
| b20.v | rx-oop (OOP Engine) | 42.35B | 36.20B | 1.17 | 35.63B | 2.31B | 2.31B | 503.86M | 904.87M | 2.96M | 5.00B | 397.24M |
| b20.v | Icarus Verilog | 102.17B | 37.72B | 2.71 | 52.92B | 2.30B | 2.30B | 762.98M | 1.26B | 2.13M | 20.20B | 206.92M |
| b20.v | Verilator C++ | 2.90B | 2.18B | 1.33 | 2.28B | 128.45K | 128.45K | 4.75K | 11.46K | 1.14K | 12.42M | 18.76K |
| b22.v | rx-prop | 62.51B | 28.19B | 2.22 | 25.52B | 2.87B | 2.87B | 454.38M | 1.05B | 2.69M | 5.67B | 353.63M |
| b22.v | rx-sweep (Linear) | 62.23B | 22.34B | 2.79 | 20.39B | 3.04B | 3.04B | 278.34M | 1.35B | 3.31M | 11.07B | 258.63M |
| b22.v | rx-oop (OOP Engine) | 74.80B | 70.34B | 1.06 | 65.44B | 4.15B | 4.15B | 1.12B | 2.05B | 3.96M | 8.81B | 814.48M |
| b22.v | Icarus Verilog | 174.56B | 75.15B | 2.32 | 97.28B | 4.20B | 4.20B | 2.04B | 3.10B | 23.59M | 34.68B | 410.29M |
| b22.v | Verilator C++ | 4.23B | 2.87B | 1.47 | 3.19B | 161.45K | 161.45K | 42.82K | 52.66K | 10.46K | 12.75M | 56.70K |
| b17.v | rx-prop | 51.31B | 16.58B | 3.10 | 20.14B | 2.14B | 2.14B | 325.25M | 996.50M | 3.75M | 4.56B | 23.91M |
| b17.v | rx-sweep (Linear) | 73.09B | 18.87B | 3.87 | 20.87B | 3.46B | 3.46B | 303.72M | 2.34B | 4.76M | 15.59B | 86.66M |
| b17.v | rx-oop (OOP Engine) | 59.45B | 33.70B | 1.76 | 41.07B | 3.41B | 3.41B | 972.45M | 2.56B | 4.98M | 6.99B | 142.02M |
| b17.v | Icarus Verilog | 130.31B | 51.79B | 2.52 | 64.31B | 3.48B | 3.48B | 1.80B | 3.44B | 26.25M | 25.67B | 125.39M |
| b17.v | Verilator C++ | 5.17B | 3.22B | 1.60 | 3.10B | 116.32K | 116.32K | 211.35K | 275.85K | 95.16K | 13.86M | 163.31K |
| b18.v | rx-prop | 145.61B | 56.37B | 2.58 | 57.89B | 5.87B | 5.87B | 1.28B | 3.92B | 9.42M | 13.04B | 365.30M |
| b18.v | rx-sweep (Linear) | 178.15B | 53.65B | 3.32 | 52.48B | 8.46B | 8.46B | 1.16B | 8.09B | 6.12M | 38.35B | 376.70M |
| b18.v | rx-oop (OOP Engine) | 168.89B | 118.62B | 1.42 | 125.77B | 9.43B | 9.43B | 3.11B | 8.85B | 35.81M | 19.83B | 918.35M |
| b18.v | Icarus Verilog | 35.39B | 18.27B | 1.94 | 16.63B | 864.20M | 864.20M | 195.53M | 319.70M | 47.02M | 7.45B | 108.33M |
| b18.v | Verilator C++ | 13.20B | 10.94B | 1.21 | 7.30B | 14.00M | 14.00M | 710.65M | 711.50M | 8.15K | 15.94M | 116.90K |
| b19.v | rx-prop | 251.16B | 94.94B | 2.65 | 98.94B | 10.18B | 10.18B | 2.65B | 9.18B | 18.11M | 22.31B | 375.03M |
| b19.v | rx-sweep (Linear) | 345.20B | 96.85B | 3.56 | 97.16B | 16.43B | 16.43B | 2.77B | 17.42B | 22.22M | 74.34B | 469.02M |
| b19.v | rx-oop (OOP Engine) | 291.41B | 191.32B | 1.52 | 208.75B | 16.60B | 16.60B | 6.03B | 17.92B | 145.64M | 34.18B | 967.93M |
| b19.v | Icarus Verilog | 57.69B | 32.74B | 1.76 | 25.49B | 1.43B | 1.43B | 340.04M | 575.88M | 144.05M | 12.24B | 169.46M |
| b19.v | Verilator C++ | 24.56B | 21.15B | 1.16 | 13.39B | 118.00M | 118.00M | 1.70B | 1.70B | 156.79K | 15.81M | 185.36K |

## Opencores

**Execution Parameters:**
- **Target Suite / Path:** `tests/IWLS2005/opencores`
- **Circuits Benchmarked:** 21
- **Simulation Vectors (Phase 3):** 50,000 (Warmup: 10)
- **Verification Vectors (Phase 2):** 100
- **Hardware Profiler:** Linux `perf` kernel PMU counters
- **Note (2026-10-22):** re-run after the Verilator library fix: Verilator now compiles `iwls_sequential_harness.verilator_gsclib()` (the cell library with its sequential UDPs as nonblocking modules), because Verilator 5.052 lowers the original UDP flops to blocking assignments, which is order-dependent and slow. Icarus uses the original library; Darion simulates every flop as the 10-gate NAND master-slave of `tests/src/DFFSR.json`, so the flop models differ between the three tools (not a same-netlist comparison). The previous report (blocking-UDP Verilator) is in git history.

---

### 1. Zero-Testbench Memory Footprint (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | 184 | 0.58 MB (28.2 MB peak) | N/A | 0.48 MB (8.4 MB peak) | 0.69 MB (4.4 MB peak) |
| steppermotordrive.v | 258 | 1.07 MB (28.6 MB peak) | N/A | 1.07 MB (8.9 MB peak) | 0.80 MB (4.4 MB peak) |
| ss_pcm.v | 648 | 2.44 MB (30.0 MB peak) | N/A | 2.14 MB (10.0 MB peak) | 0.74 MB (4.4 MB peak) |
| usb_phy.v | 715 | 2.59 MB (30.1 MB peak) | N/A | 2.49 MB (10.4 MB peak) | 0.71 MB (4.4 MB peak) |
| sasc.v | 1,125 | 3.28 MB (30.8 MB peak) | N/A | 2.66 MB (10.6 MB peak) | 0.70 MB (4.4 MB peak) |
| simple_spi.v | 1,489 | 3.78 MB (31.4 MB peak) | N/A | 3.99 MB (11.9 MB peak) | 0.71 MB (4.3 MB peak) |
| pci_spoci_ctrl.v | 1,696 | 2.93 MB (30.5 MB peak) | N/A | 5.29 MB (13.1 MB peak) | 0.72 MB (4.4 MB peak) |
| i2c.v | 1,496 | 3.74 MB (31.3 MB peak) | N/A | 5.37 MB (13.2 MB peak) | 0.74 MB (4.4 MB peak) |
| systemcdes.v | 4,326 | 8.04 MB (35.6 MB peak) | N/A | 13.67 MB (21.6 MB peak) | 0.69 MB (4.4 MB peak) |
| spi.v | 4,531 | 7.90 MB (35.5 MB peak) | N/A | 14.99 MB (22.9 MB peak) | 0.71 MB (4.4 MB peak) |
| wb_dma.v | 5,720 | 15.85 MB (43.4 MB peak) | N/A | 15.95 MB (23.8 MB peak) | 0.78 MB (4.5 MB peak) |
| des_area.v | 6,445 | 9.01 MB (36.6 MB peak) | N/A | 18.95 MB (26.8 MB peak) | 0.91 MB (4.6 MB peak) |
| tv80.v | 10,607 | 17.81 MB (45.4 MB peak) | N/A | 31.08 MB (38.9 MB peak) | N/A |
| systemcaes.v | 14,071 | 24.79 MB (53.2 MB peak) | N/A | 40.89 MB (48.8 MB peak) | 1.02 MB (4.7 MB peak) |
| mem_ctrl.v | 16,796 | 29.34 MB (56.9 MB peak) | N/A | 54.03 MB (61.9 MB peak) | 0.97 MB (4.6 MB peak) |
| ac97_ctrl.v | 19,069 | 47.02 MB (74.5 MB peak) | N/A | 65.62 MB (73.4 MB peak) | 0.99 MB (4.7 MB peak) |
| usb_funct.v | 18,282 | 41.78 MB (69.3 MB peak) | N/A | 59.27 MB (67.1 MB peak) | 0.95 MB (4.6 MB peak) |
| aes_core.v | 25,565 | 31.69 MB (62.3 MB peak) | N/A | 78.79 MB (86.7 MB peak) | 1.10 MB (4.8 MB peak) |
| wb_conmax.v | 49,326 | 46.79 MB (79.4 MB peak) | N/A | 144.04 MB (152.0 MB peak) | 1.09 MB (4.8 MB peak) |
| des_perf.v | 111,781 | 204.47 MB (242.7 MB peak) | N/A | 440.60 MB (448.5 MB peak) | 1.84 MB (5.5 MB peak) |
| vga_lcd.v | 187,445 | 374.18 MB (417.9 MB peak) | N/A | 592.75 MB (600.5 MB peak) | 1.92 MB (5.5 MB peak) |

---

### 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | 184 | 0.17 ms (0.015 ms opt) | N/A | 5.03 ms | 2.55 s |
| steppermotordrive.v | 258 | 0.46 ms (0.058 ms opt) | N/A | 7.17 ms | 2.54 s |
| ss_pcm.v | 648 | 1.29 ms (0.134 ms opt) | N/A | 11.37 ms | 2.58 s |
| usb_phy.v | 715 | 1.45 ms (0.173 ms opt) | N/A | 13.28 ms | 2.62 s |
| sasc.v | 1,125 | 1.82 ms (0.197 ms opt) | N/A | 13.95 ms | 2.61 s |
| simple_spi.v | 1,489 | 2.20 ms (0.246 ms opt) | N/A | 21.00 ms | 2.67 s |
| pci_spoci_ctrl.v | 1,696 | 1.71 ms (0.223 ms opt) | N/A | 24.22 ms | 2.71 s |
| i2c.v | 1,496 | 2.26 ms (0.339 ms opt) | N/A | 28.73 ms | 2.76 s |
| systemcdes.v | 4,326 | 5.19 ms (0.595 ms opt) | N/A | 71.38 ms | 3.25 s |
| spi.v | 4,531 | 5.63 ms (0.739 ms opt) | N/A | 69.14 ms | 3.30 s |
| wb_dma.v | 5,720 | 10.18 ms (0.990 ms opt) | N/A | 72.35 ms | 3.37 s |
| des_area.v | 6,445 | 5.76 ms (0.741 ms opt) | N/A | 92.55 ms | 4.11 s |
| tv80.v | 10,607 | 11.64 ms (1.470 ms opt) | N/A | 155.32 ms | N/A |
| systemcaes.v | 14,071 | 16.35 ms (1.905 ms opt) | N/A | 197.38 ms | 6.86 s |
| mem_ctrl.v | 16,796 | 24.78 ms (4.010 ms opt) | N/A | 270.30 ms | 6.91 s |
| ac97_ctrl.v | 19,069 | 38.56 ms (7.096 ms opt) | N/A | 307.52 ms | 7.59 s |
| usb_funct.v | 18,282 | 32.95 ms (6.161 ms opt) | N/A | 307.31 ms | 7.63 s |
| aes_core.v | 25,565 | 25.83 ms (5.089 ms opt) | N/A | 418.64 ms | 10.13 s |
| wb_conmax.v | 49,326 | 49.67 ms (14.317 ms opt) | N/A | 835.96 ms | 15.65 s |
| des_perf.v | 111,781 | 323.86 ms (64.407 ms opt) | N/A | 2.36 s | 63.72 s |
| vga_lcd.v | 187,445 | 609.23 ms (104.237 ms opt) | N/A | 3.24 s | 106.23 s |

---

### 3. High-Throughput Simulation Performance (Phase 3)

#### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | 22.54 ms | 29.70 ms | 36.52 ms | N/A | 877.75 ms | 1.94 ms |
| steppermotordrive.v | 48.64 ms | 59.63 ms | 87.33 ms | N/A | 97.76 ms | 6.65 ms |
| ss_pcm.v | 221.33 ms | 250.89 ms | 382.96 ms | N/A | 576.78 ms | 16.42 ms |
| usb_phy.v | 235.72 ms | 252.44 ms | 414.58 ms | N/A | 422.20 ms | 14.53 ms |
| sasc.v | 296.90 ms | 296.19 ms | 528.22 ms | N/A | 519.86 ms | 14.36 ms |
| simple_spi.v | 278.60 ms | 267.45 ms | 428.21 ms | N/A | 602.93 ms | 14.47 ms |
| pci_spoci_ctrl.v | 200.01 ms | 198.04 ms | 460.86 ms | N/A | 815.63 ms | 24.69 ms |
| i2c.v | 331.52 ms | 307.97 ms | 585.56 ms | N/A | 1125.19 ms | 36.50 ms |
| systemcdes.v | 2587.60 ms | 1901.04 ms | 6435.16 ms | N/A | 15.49 s | 96.57 ms |
| spi.v | 522.38 ms | 577.61 ms | 815.41 ms | N/A | 2356.33 ms | 87.64 ms |
| wb_dma.v | 1365.93 ms | 1487.89 ms | 2361.64 ms | N/A | 5750.42 ms | 61.48 ms |
| des_area.v | 2699.96 ms | 2103.28 ms | 6356.31 ms | N/A | 50.67 s | 97.00 ms |
| tv80.v | 782.90 ms | 1025.87 ms | 1346.10 ms | N/A | 1007.47 ms | 142.39 ms |
| systemcaes.v | 2210.62 ms | 2463.63 ms | 4542.47 ms | N/A | 20.43 s | 306.11 ms |
| mem_ctrl.v | 2185.83 ms | 2745.03 ms | 4351.62 ms | N/A | 7315.70 ms | 255.29 ms |
| ac97_ctrl.v | 4006.17 ms | 4009.63 ms | 7273.42 ms | N/A | 4909.58 ms | 179.87 ms |
| usb_funct.v | 1554.53 ms | 2446.42 ms | 2780.79 ms | N/A | 8042.32 ms | 226.04 ms |
| aes_core.v | 8714.54 ms | 9556.95 ms | 22.59 s | N/A | 28.09 s | 235.17 ms |
| wb_conmax.v | 3807.83 ms | 5422.98 ms | 6655.43 ms | N/A | 103.69 s | 732.21 ms |
| des_perf.v | 103.19 s | 108.08 s | 251.11 s | N/A | 558.60 s | 2466.37 ms |
| vga_lcd.v | 38.29 s | 39.37 s | 70.41 s | N/A | 59.76 s | 2171.85 ms |

#### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | 38.94x | 29.55x | 24.03x | N/A | 1.00x | 453.47x |
| steppermotordrive.v | 2.01x | 1.64x | 1.12x | N/A | 1.00x | 14.70x |
| ss_pcm.v | 2.61x | 2.30x | 1.51x | N/A | 1.00x | 35.12x |
| usb_phy.v | 1.79x | 1.67x | 1.02x | N/A | 1.00x | 29.05x |
| sasc.v | 1.75x | 1.76x | 0.98x | N/A | 1.00x | 36.19x |
| simple_spi.v | 2.16x | 2.25x | 1.41x | N/A | 1.00x | 41.66x |
| pci_spoci_ctrl.v | 4.08x | 4.12x | 1.77x | N/A | 1.00x | 33.03x |
| i2c.v | 3.39x | 3.65x | 1.92x | N/A | 1.00x | 30.82x |
| systemcdes.v | 5.99x | 8.15x | 2.41x | N/A | 1.00x | 160.41x |
| spi.v | 4.51x | 4.08x | 2.89x | N/A | 1.00x | 26.89x |
| wb_dma.v | 4.21x | 3.86x | 2.43x | N/A | 1.00x | 93.53x |
| des_area.v | 18.77x | 24.09x | 7.97x | N/A | 1.00x | 522.40x |
| tv80.v | 1.29x | 0.98x | 0.75x | N/A | 1.00x | 7.08x |
| systemcaes.v | 9.24x | 8.29x | 4.50x | N/A | 1.00x | 66.73x |
| mem_ctrl.v | 3.35x | 2.67x | 1.68x | N/A | 1.00x | 28.66x |
| ac97_ctrl.v | 1.23x | 1.22x | 0.68x | N/A | 1.00x | 27.30x |
| usb_funct.v | 5.17x | 3.29x | 2.89x | N/A | 1.00x | 35.58x |
| aes_core.v | 3.22x | 2.94x | 1.24x | N/A | 1.00x | 119.47x |
| wb_conmax.v | 27.23x | 19.12x | 15.58x | N/A | 1.00x | 141.61x |
| des_perf.v | 5.41x | 5.17x | 2.22x | N/A | 1.00x | 226.49x |
| vga_lcd.v | 1.56x | 1.52x | 0.85x | N/A | 1.00x | 27.52x |

#### Total Gate Evaluations

| Circuit | Gates | rx-prop Evals | rx-sweep Evals | rx-oop Evals | Pure Python Evals |
|:---|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | 184 | 5,392,574 | 5,120,319 | 5,392,574 | N/A |
| steppermotordrive.v | 258 | 23,717,113 | 23,611,913 | 23,717,113 | N/A |
| ss_pcm.v | 648 | 89,309,054 | 87,878,978 | 89,532,104 | N/A |
| usb_phy.v | 715 | 94,303,037 | 93,846,669 | 94,354,187 | N/A |
| sasc.v | 1,125 | 121,402,307 | 111,250,788 | 124,377,711 | N/A |
| simple_spi.v | 1,489 | 119,413,667 | 114,375,704 | 119,440,293 | N/A |
| pci_spoci_ctrl.v | 1,696 | 90,088,151 | 71,150,933 | 89,778,069 | N/A |
| i2c.v | 1,496 | 144,790,757 | 133,856,428 | 145,278,617 | N/A |
| systemcdes.v | 4,326 | 772,228,933 | 461,566,720 | 788,685,222 | N/A |
| spi.v | 4,531 | 234,455,303 | 227,362,614 | 234,702,648 | N/A |
| wb_dma.v | 5,720 | 572,583,673 | 548,443,835 | 576,577,418 | N/A |
| des_area.v | 6,445 | 737,296,590 | 416,181,580 | 757,389,026 | N/A |
| tv80.v | 10,607 | 335,979,209 | 337,627,357 | 339,703,774 | N/A |
| systemcaes.v | 14,071 | 899,077,652 | 835,961,603 | 908,136,485 | N/A |
| mem_ctrl.v | 16,796 | 936,995,633 | 902,722,740 | 938,916,603 | N/A |
| ac97_ctrl.v | 19,069 | 1,647,126,400 | 1,637,956,615 | 1,647,138,602 | N/A |
| usb_funct.v | 18,282 | 582,823,894 | 577,881,813 | 583,041,399 | N/A |
| aes_core.v | 25,565 | 2,147,934,816 | 2,098,290,932 | 2,180,414,370 | N/A |
| wb_conmax.v | 49,326 | 1,282,138,675 | 1,225,583,003 | 1,283,273,835 | N/A |
| des_perf.v | 111,781 | 20,771,797,777 | 19,213,988,869 | 20,807,534,081 | N/A |
| vga_lcd.v | 187,445 | 14,127,284,006 | 14,022,765,964 | 14,127,453,690 | N/A |

#### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `4.11x`
- **rx-sweep (Linear Compiled):** `3.78x`
- **rx-oop (OOP Graph):** `2.16x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `54.62x`

#### Gate Evaluation Highlights

- **Reactor Sweep vs Propagate Total Evaluations Ratio:** `0.91x` (propagate performed more evaluations)

#### Cross-Engine Comparisons

- **Reactor Sweep vs Propagate Ratio:** `0.92x` (propagate faster)

---

### 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | Instructions | Cycles | IPC | L1 Loads | L1 Misses | L2 Loads | L2 Misses | L3 Loads | DRAM Loads | Branches | Branch Misses |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| pci_conf_cyc_addr_dec.v | rx-prop | 206.40M | 86.60M | 2.38 | 145.75M | 1.12M | 1.12M | 19.73K | 100.78K | 83.94K | 38.25M | 1.24M |
| pci_conf_cyc_addr_dec.v | rx-sweep (Linear) | 242.22M | 117.39M | 2.06 | 146.37M | 1.57M | 1.57M | 28.73K | 704.31K | 678.88K | 54.64M | 2.15M |
| pci_conf_cyc_addr_dec.v | rx-oop (OOP Engine) | 278.41M | 146.75M | 1.90 | 203.34M | 2.35M | 2.35M | 58.00K | 1.18M | 1.03M | 44.24M | 1.71M |
| pci_conf_cyc_addr_dec.v | Icarus Verilog | 12.77B | 3.23B | 3.95 | 4.96B | 27.61M | 27.61M | 58.86K | 108.83K | 12.84K | 2.73B | 13.46M |
| pci_conf_cyc_addr_dec.v | Verilator C++ | 26.99M | 11.06M | 2.44 | 12.96M | 59.23K | 59.23K | 2.51K | 2.51K | 0.00 | 6.38M | 1.62K |
| steppermotordrive.v | rx-prop | 695.55M | 166.96M | 4.17 | 295.28M | 584.40K | 584.40K | 6.20K | 37.94K | 28.89K | 71.98M | 199.96K |
| steppermotordrive.v | rx-sweep (Linear) | 869.10M | 209.31M | 4.15 | 335.87M | 1.24M | 1.24M | 21.23K | 36.71K | 28.69K | 188.45M | 1.37M |
| steppermotordrive.v | rx-oop (OOP Engine) | 817.62M | 298.63M | 2.74 | 514.06M | 3.13M | 3.13M | 14.61K | 73.24K | 45.88K | 98.16M | 733.95K |
| steppermotordrive.v | Icarus Verilog | 1.58B | 399.71M | 3.95 | 648.06M | 1.33M | 1.33M | 37.07K | 101.99K | 13.44K | 321.65M | 2.17M |
| steppermotordrive.v | Verilator C++ | 14.94M | 6.33M | 2.36 | 25.72M | 19.61K | 19.61K | 485.00 | 34.01K | 56.00 | 3.40M | 24.99K |
| ss_pcm.v | rx-prop | 2.80B | 818.34M | 3.42 | 1.13B | 82.79M | 82.79M | 105.17K | 2.31M | 2.23M | 284.92M | 3.14M |
| ss_pcm.v | rx-sweep (Linear) | 3.24B | 930.12M | 3.48 | 1.15B | 116.84M | 116.84M | 92.10K | 1.97M | 1.91M | 640.04M | 9.05M |
| ss_pcm.v | rx-oop (OOP Engine) | 3.17B | 1.40B | 2.27 | 1.98B | 144.09M | 144.09M | 69.76K | 964.96K | 845.29K | 386.37M | 6.35M |
| ss_pcm.v | Icarus Verilog | 8.07B | 2.19B | 3.68 | 3.69B | 72.47M | 72.47M | 130.72K | 214.22K | 17.06K | 1.58B | 14.24M |
| ss_pcm.v | Verilator C++ | 80.01M | 57.96M | 1.38 | 53.41M | 10.01K | 10.01K | 207.00 | 65.68K | 469.00 | 11.62M | 55.00K |
| usb_phy.v | rx-prop | 2.92B | 874.04M | 3.34 | 1.16B | 93.36M | 93.36M | 87.78K | 1.46M | 1.41M | 288.46M | 3.30M |
| usb_phy.v | rx-sweep (Linear) | 3.46B | 928.00M | 3.72 | 1.19B | 123.82M | 123.82M | 72.07K | 1.37M | 1.34M | 678.81M | 7.52M |
| usb_phy.v | rx-oop (OOP Engine) | 3.26B | 1.49B | 2.19 | 2.08B | 176.33M | 176.33M | 85.24K | 633.73K | 475.99K | 394.66M | 7.00M |
| usb_phy.v | Icarus Verilog | 5.68B | 1.63B | 3.48 | 2.57B | 49.84M | 49.84M | 168.40K | 360.00K | 11.32K | 1.12B | 12.08M |
| usb_phy.v | Verilator C++ | 61.03M | 41.83M | 1.46 | 59.08M | 51.65K | 51.65K | 3.28K | 43.63K | 16.34K | 7.26M | 49.29K |
| sasc.v | rx-prop | 3.74B | 1.09B | 3.42 | 1.49B | 136.18M | 136.18M | 83.24K | 1.93M | 1.86M | 371.33M | 3.67M |
| sasc.v | rx-sweep (Linear) | 4.20B | 1.09B | 3.87 | 1.42B | 157.54M | 157.54M | 87.11K | 1.53M | 1.51M | 847.34M | 8.97M |
| sasc.v | rx-oop (OOP Engine) | 4.39B | 1.92B | 2.28 | 2.77B | 235.05M | 235.05M | 95.89K | 613.25K | 429.10K | 529.94M | 8.98M |
| sasc.v | Icarus Verilog | 7.01B | 1.96B | 3.58 | 3.28B | 73.23M | 73.23M | 295.79K | 610.33K | 37.41K | 1.39B | 12.88M |
| sasc.v | Verilator C++ | 89.99M | 39.91M | 2.25 | 70.22M | 94.74K | 94.74K | 642.00 | 91.20K | 10.04K | 7.73M | 78.98K |
| simple_spi.v | rx-prop | 3.62B | 1.02B | 3.55 | 1.43B | 142.70M | 142.70M | 93.72K | 1.42M | 1.32M | 352.10M | 1.67M |
| simple_spi.v | rx-sweep (Linear) | 4.51B | 993.34M | 4.54 | 1.39B | 177.29M | 177.29M | 98.68K | 2.25M | 2.22M | 941.73M | 4.07M |
| simple_spi.v | rx-oop (OOP Engine) | 4.10B | 1.54B | 2.66 | 2.50B | 264.51M | 264.51M | 46.22K | 704.22K | 585.08K | 496.69M | 3.51M |
| simple_spi.v | Icarus Verilog | 8.82B | 2.32B | 3.81 | 3.95B | 109.06M | 109.06M | 204.34K | 385.31K | 21.78K | 1.73B | 12.73M |
| simple_spi.v | Verilator C++ | 104.96M | 35.91M | 2.92 | 70.17M | 11.21K | 11.21K | 595.00 | 9.68K | 16.00 | 6.77M | 40.56K |
| pci_spoci_ctrl.v | rx-prop | 2.74B | 736.33M | 3.72 | 1.14B | 56.42M | 56.42M | 35.16K | 801.40K | 771.52K | 283.98M | 1.87M |
| pci_spoci_ctrl.v | rx-sweep (Linear) | 3.18B | 752.04M | 4.22 | 1.01B | 112.17M | 112.17M | 80.45K | 2.31M | 2.27M | 655.98M | 3.65M |
| pci_spoci_ctrl.v | rx-oop (OOP Engine) | 3.20B | 1.70B | 1.89 | 2.30B | 119.60M | 119.60M | 91.38K | 2.41M | 2.16M | 400.17M | 14.05M |
| pci_spoci_ctrl.v | Icarus Verilog | 11.15B | 3.15B | 3.54 | 5.17B | 148.79M | 148.79M | 459.73K | 1.03M | 71.28K | 2.17B | 20.36M |
| pci_spoci_ctrl.v | Verilator C++ | 204.34M | 86.38M | 2.37 | 123.75M | 12.45K | 12.45K | 3.84K | 130.22K | 95.76K | 12.16M | 49.95K |
| i2c.v | rx-prop | 4.30B | 1.21B | 3.55 | 1.73B | 155.54M | 155.54M | 115.31K | 1.97M | 1.87M | 418.12M | 2.28M |
| i2c.v | rx-sweep (Linear) | 5.00B | 1.14B | 4.39 | 1.62B | 194.16M | 194.16M | 84.71K | 2.16M | 2.14M | 1.02B | 5.38M |
| i2c.v | rx-oop (OOP Engine) | 5.01B | 2.13B | 2.35 | 3.19B | 273.15M | 273.15M | 106.33K | 2.03M | 1.70M | 605.12M | 10.32M |
| i2c.v | Icarus Verilog | 16.18B | 4.21B | 3.84 | 7.41B | 308.98M | 308.98M | 9.70M | 15.76M | 94.27K | 3.18B | 19.09M |
| i2c.v | Verilator C++ | 221.81M | 136.63M | 1.62 | 132.13M | 76.60K | 76.60K | 1.05K | 11.73K | 1.76K | 12.71M | 46.41K |
| systemcdes.v | rx-prop | 24.19B | 9.49B | 2.55 | 9.95B | 908.26M | 908.26M | 2.50M | 17.27M | 12.93M | 2.42B | 122.87M |
| systemcdes.v | rx-sweep (Linear) | 16.82B | 7.04B | 2.39 | 6.72B | 638.75M | 638.75M | 968.60K | 14.88M | 13.32M | 2.87B | 117.38M |
| systemcdes.v | rx-oop (OOP Engine) | 28.37B | 23.25B | 1.22 | 23.71B | 1.37B | 1.37B | 18.73M | 42.33M | 11.72M | 3.46B | 298.03M |
| systemcdes.v | Icarus Verilog | 154.60B | 56.28B | 2.75 | 83.28B | 2.93B | 2.93B | 611.60M | 872.27M | 1.16M | 30.40B | 401.00M |
| systemcdes.v | Verilator C++ | 553.59M | 341.72M | 1.62 | 333.71M | 250.12K | 250.12K | 4.94K | 256.03K | 241.51K | 9.45M | 63.12K |
| spi.v | rx-prop | 7.01B | 1.94B | 3.62 | 2.80B | 306.15M | 306.15M | 440.96K | 5.08M | 4.35M | 685.57M | 3.47M |
| spi.v | rx-sweep (Linear) | 9.43B | 2.13B | 4.43 | 2.90B | 425.77M | 425.77M | 315.57K | 4.83M | 4.48M | 2.03B | 10.95M |
| spi.v | rx-oop (OOP Engine) | 8.01B | 2.98B | 2.69 | 4.82B | 480.32M | 480.32M | 1.01M | 5.79M | 3.73M | 966.88M | 8.61M |
| spi.v | Icarus Verilog | 34.48B | 8.93B | 3.86 | 15.65B | 617.52M | 617.52M | 103.27M | 194.22M | 551.00K | 6.75B | 31.98M |
| spi.v | Verilator C++ | 552.01M | 310.88M | 1.78 | 325.71M | 111.94K | 111.94K | 3.61K | 103.99K | 93.33K | 11.83M | 81.21K |
| wb_dma.v | rx-prop | 18.52B | 5.20B | 3.56 | 7.50B | 777.61M | 777.61M | 1.88M | 23.51M | 20.29M | 1.98B | 13.69M |
| wb_dma.v | rx-sweep (Linear) | 21.55B | 5.65B | 3.82 | 7.43B | 932.60M | 932.60M | 2.82M | 26.84M | 21.43M | 4.45B | 48.49M |
| wb_dma.v | rx-oop (OOP Engine) | 20.98B | 8.67B | 2.42 | 12.87B | 1.29B | 1.29B | 60.36M | 136.88M | 17.93M | 2.66B | 26.23M |
| wb_dma.v | Icarus Verilog | 87.81B | 21.61B | 4.06 | 38.64B | 604.24M | 604.24M | 128.72M | 219.29M | 878.86K | 16.97B | 73.12M |
| wb_dma.v | Verilator C++ | 498.68M | 216.84M | 2.30 | 258.48M | 52.68K | 52.68K | 1.21K | 217.31K | 180.34K | 14.92M | 52.81K |
| des_area.v | rx-prop | 24.17B | 10.01B | 2.41 | 10.15B | 816.48M | 816.48M | 2.60M | 26.62M | 22.59M | 2.58B | 143.08M |
| des_area.v | rx-sweep (Linear) | 16.66B | 7.86B | 2.12 | 7.08B | 581.39M | 581.39M | 2.61M | 27.70M | 22.87M | 3.09B | 153.19M |
| des_area.v | rx-oop (OOP Engine) | 28.19B | 23.09B | 1.22 | 23.48B | 1.31B | 1.31B | 34.60M | 73.45M | 21.59M | 3.54B | 295.84M |
| des_area.v | Icarus Verilog | 582.67B | 183.26B | 3.18 | 228.41B | 5.68B | 5.68B | 1.12B | 1.42B | 3.18M | 137.18B | 788.26M |
| des_area.v | Verilator C++ | 795.49M | 341.13M | 2.33 | 456.18M | 123.75K | 123.75K | 4.65K | 156.58K | 155.22K | 9.07M | 123.47K |
| tv80.v | rx-prop | 9.97B | 2.82B | 3.54 | 3.91B | 445.97M | 445.97M | 1.62M | 3.92M | 714.07K | 927.47M | 5.07M |
| tv80.v | rx-sweep (Linear) | 15.79B | 3.69B | 4.28 | 4.54B | 714.26M | 714.26M | 11.56M | 28.88M | 728.56K | 3.43B | 19.43M |
| tv80.v | rx-oop (OOP Engine) | 11.65B | 4.82B | 2.42 | 7.30B | 726.75M | 726.75M | 11.81M | 22.77M | 1.37M | 1.38B | 17.98M |
| tv80.v | Icarus Verilog | 13.97B | 4.40B | 3.17 | 6.34B | 241.18M | 241.18M | 28.06M | 41.84M | 603.68K | 2.85B | 25.76M |
| tv80.v | Verilator C++ | 705.95M | 508.94M | 1.39 | 531.19M | 25.03K | 25.03K | 1.79K | 34.87K | 2.38K | 8.87M | 37.75K |
| systemcaes.v | rx-prop | 27.92B | 8.26B | 3.38 | 11.26B | 1.07B | 1.07B | 44.36M | 120.78M | 26.59M | 2.86B | 30.26M |
| systemcaes.v | rx-sweep (Linear) | 33.82B | 9.19B | 3.68 | 11.17B | 1.43B | 1.43B | 92.72M | 368.83M | 25.59M | 6.96B | 75.18M |
| systemcaes.v | rx-oop (OOP Engine) | 31.93B | 16.61B | 1.92 | 21.30B | 1.74B | 1.74B | 333.77M | 689.90M | 22.15M | 3.96B | 86.23M |
| systemcaes.v | Icarus Verilog | 308.24B | 75.05B | 4.11 | 137.81B | 4.29B | 4.29B | 1.17B | 2.02B | 3.96M | 56.52B | 177.96M |
| systemcaes.v | Verilator C++ | 1.93B | 1.09B | 1.76 | 891.98M | 84.36K | 84.36K | 3.04K | 43.38K | 41.73K | 13.77M | 99.35K |
| mem_ctrl.v | rx-prop | 28.18B | 8.00B | 3.52 | 11.11B | 1.15B | 1.15B | 41.41M | 81.20M | 10.98M | 2.70B | 16.12M |
| mem_ctrl.v | rx-sweep (Linear) | 37.76B | 9.95B | 3.80 | 11.85B | 1.74B | 1.74B | 126.46M | 558.03M | 11.19M | 8.11B | 67.91M |
| mem_ctrl.v | rx-oop (OOP Engine) | 32.28B | 15.65B | 2.06 | 20.42B | 2.00B | 2.00B | 484.54M | 1.11B | 9.44M | 3.90B | 40.22M |
| mem_ctrl.v | Icarus Verilog | 101.46B | 27.92B | 3.63 | 45.51B | 1.21B | 1.21B | 536.38M | 913.50M | 2.51M | 19.68B | 77.69M |
| mem_ctrl.v | Verilator C++ | 1.73B | 917.72M | 1.89 | 1.01B | 172.63K | 172.63K | 3.97K | 33.42K | 23.01K | 15.44M | 128.42K |
| ac97_ctrl.v | rx-prop | 48.71B | 14.42B | 3.38 | 19.07B | 2.04B | 2.04B | 220.18M | 571.32M | 7.98M | 4.51B | 8.88M |
| ac97_ctrl.v | rx-sweep (Linear) | 63.35B | 14.48B | 4.38 | 19.54B | 2.73B | 2.73B | 200.35M | 1.28B | 8.80M | 13.30B | 50.18M |
| ac97_ctrl.v | rx-oop (OOP Engine) | 56.13B | 26.10B | 2.15 | 34.45B | 3.67B | 3.67B | 1.21B | 3.39B | 6.70M | 6.67B | 18.76M |
| ac97_ctrl.v | Icarus Verilog | 67.28B | 19.26B | 3.49 | 27.83B | 1.02B | 1.02B | 493.01M | 968.97M | 3.44M | 13.99B | 38.70M |
| ac97_ctrl.v | Verilator C++ | 1.21B | 638.68M | 1.90 | 682.15M | 44.47K | 44.47K | 2.48K | 195.67K | 144.02K | 15.02M | 64.73K |
| usb_funct.v | rx-prop | 17.76B | 5.71B | 3.11 | 7.15B | 770.53M | 770.53M | 86.15M | 223.47M | 12.34M | 1.77B | 9.98M |
| usb_funct.v | rx-sweep (Linear) | 34.19B | 8.91B | 3.84 | 9.28B | 1.61B | 1.61B | 143.17M | 588.28M | 12.77M | 8.04B | 60.63M |
| usb_funct.v | rx-oop (OOP Engine) | 20.22B | 10.08B | 2.01 | 12.79B | 1.28B | 1.28B | 372.17M | 841.08M | 10.94M | 2.49B | 21.78M |
| usb_funct.v | Icarus Verilog | 116.15B | 30.63B | 3.79 | 50.68B | 1.68B | 1.68B | 504.34M | 854.15M | 2.28M | 22.63B | 74.33M |
| usb_funct.v | Verilator C++ | 1.15B | 796.79M | 1.45 | 907.18M | 42.90K | 42.90K | 2.38K | 33.64K | 4.09K | 10.26M | 109.07K |
| aes_core.v | rx-prop | 67.82B | 31.59B | 2.15 | 27.68B | 3.31B | 3.31B | 567.71M | 1.01B | 25.28M | 6.77B | 334.48M |
| aes_core.v | rx-sweep (Linear) | 79.12B | 34.57B | 2.29 | 29.70B | 3.86B | 3.86B | 504.88M | 1.52B | 25.63M | 11.79B | 428.82M |
| aes_core.v | rx-oop (OOP Engine) | 79.76B | 81.42B | 0.98 | 75.07B | 4.46B | 4.46B | 1.28B | 2.13B | 24.99M | 9.66B | 906.27M |
| aes_core.v | Icarus Verilog | 277.48B | 103.60B | 2.68 | 147.79B | 3.85B | 3.85B | 2.00B | 2.55B | 9.19M | 52.89B | 597.56M |
| aes_core.v | Verilator C++ | 1.59B | 834.22M | 1.90 | 969.73M | 84.07K | 84.07K | 7.50K | 43.81K | 35.24K | 9.49M | 39.73K |
| wb_conmax.v | rx-prop | 44.43B | 15.10B | 2.94 | 18.72B | 1.77B | 1.77B | 337.90M | 857.20M | 114.91M | 5.34B | 39.99M |
| wb_conmax.v | rx-sweep (Linear) | 65.05B | 20.89B | 3.11 | 21.38B | 3.00B | 3.00B | 377.38M | 1.98B | 112.80M | 14.89B | 185.78M |
| wb_conmax.v | rx-oop (OOP Engine) | 47.65B | 25.46B | 1.87 | 30.77B | 2.67B | 2.67B | 920.57M | 1.98B | 98.77M | 6.52B | 89.58M |
| wb_conmax.v | Icarus Verilog | 1447.85B | 379.78B | 3.81 | 646.82B | 39.51B | 39.51B | 6.29B | 9.07B | 144.97M | 274.09B | 577.96M |
| wb_conmax.v | Verilator C++ | 5.94B | 2.63B | 2.26 | 3.15B | 293.12K | 293.12K | 1.36M | 1.61M | 231.62K | 14.66M | 209.48K |
| des_perf.v | rx-prop | 629.92B | 370.48B | 1.70 | 252.79B | 32.22B | 32.22B | 17.25B | 35.03B | 70.48M | 59.16B | 2.95B |
| des_perf.v | rx-sweep (Linear) | 642.95B | 388.38B | 1.66 | 271.30B | 30.18B | 30.18B | 13.31B | 31.52B | 85.06M | 99.92B | 4.99B |
| des_perf.v | rx-oop (OOP Engine) | 733.71B | 901.88B | 0.81 | 669.81B | 42.84B | 42.84B | 28.84B | 50.11B | 1.77B | 86.91B | 6.78B |
| des_perf.v | Icarus Verilog | 59.59B | 50.04B | 1.19 | 33.53B | 1.35B | 1.35B | 861.43M | 1.15B | 263.21M | 12.26B | 179.84M |
| des_perf.v | Verilator C++ | 10.79B | 8.81B | 1.23 | 6.75B | 13.81M | 13.81M | 608.72M | 610.80M | 97.23K | 11.41M | 67.36K |
| vga_lcd.v | rx-prop | 412.98B | 137.56B | 3.00 | 160.33B | 17.76B | 17.76B | 4.48B | 19.53B | 25.31M | 37.45B | 33.91M |
| vga_lcd.v | rx-sweep (Linear) | 540.05B | 141.37B | 3.82 | 170.27B | 23.56B | 23.56B | 4.57B | 25.12B | 58.63M | 113.71B | 588.75M |
| vga_lcd.v | rx-oop (OOP Engine) | 477.46B | 252.12B | 1.89 | 294.53B | 30.30B | 30.30B | 10.15B | 35.91B | 756.41M | 56.23B | 94.48M |
| vga_lcd.v | Icarus Verilog | 38.61B | 18.42B | 2.10 | 15.65B | 821.75M | 821.75M | 178.27M | 271.78M | 33.20M | 8.32B | 87.68M |
| vga_lcd.v | Verilator C++ | 7.05B | 7.76B | 0.91 | 5.68B | 6.74M | 6.74M | 185.03M | 187.09M | 37.83K | 17.10M | 146.23K |

## DMA

**Execution Parameters:**
- **Target Suite / Path:** `tests/IWLS2005/faraday`
- **Circuits Benchmarked:** 1
- **Simulation Vectors (Phase 3):** 50,000 (Warmup: 10)
- **Verification Vectors (Phase 2):** 100
- **Hardware Profiler:** Linux `perf` kernel PMU counters
- **Note (2026-10-22):** re-run after the Verilator library fix: Verilator now compiles `iwls_sequential_harness.verilator_gsclib()` (the cell library with its sequential UDPs as nonblocking modules), because Verilator 5.052 lowers the original UDP flops to blocking assignments, which is order-dependent and slow. Icarus uses the original library; Darion simulates every flop as the 10-gate NAND master-slave of `tests/src/DFFSR.json`, so the flop models differ between the three tools (not a same-netlist comparison). The previous report (blocking-UDP Verilator) is in git history.

---

### 1. Zero-Testbench Memory Footprint (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| DMA.v | 31,920 | 56.68 MB (85.3 MB peak) | N/A | 103.10 MB (111.0 MB peak) | 1.21 MB (4.9 MB peak) |

---

### 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| DMA.v | 31,920 | 49.49 ms (9.369 ms opt) | N/A | 505.91 ms | 12.88 s |

---

### 3. High-Throughput Simulation Performance (Phase 3)

#### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| DMA.v | 5179.56 ms | 5506.47 ms | 9488.04 ms | N/A | 28.15 s | 516.93 ms |

#### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| DMA.v | 5.44x | 5.11x | 2.97x | N/A | 1.00x | 54.46x |

#### Total Gate Evaluations

| Circuit | Gates | rx-prop Evals | rx-sweep Evals | rx-oop Evals | Pure Python Evals |
|:---|---:|---:|---:|---:|---:|
| DMA.v | 31,920 | 2,055,265,005 | 2,046,739,752 | 2,057,788,417 | N/A |

#### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `5.44x`
- **rx-sweep (Linear Compiled):** `5.11x`
- **rx-oop (OOP Graph):** `2.97x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `54.46x`

#### Gate Evaluation Highlights

- **Reactor Sweep vs Propagate Total Evaluations Ratio:** `1.00x` (propagate performed more evaluations)

#### Cross-Engine Comparisons

- **Reactor Sweep vs Propagate Ratio:** `0.94x` (propagate faster)

---

### 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | Instructions | Cycles | IPC | L1 Loads | L1 Misses | L2 Loads | L2 Misses | L3 Loads | DRAM Loads | Branches | Branch Misses |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| DMA.v | rx-prop | 63.33B | 19.47B | 3.25 | 25.57B | 2.41B | 2.41B | 389.76M | 1.07B | 69.45M | 6.46B | 36.95M |
| DMA.v | rx-sweep (Linear) | 83.69B | 20.66B | 4.05 | 26.78B | 3.62B | 3.62B | 384.80M | 2.35B | 68.48M | 18.02B | 84.63M |
| DMA.v | rx-oop (OOP Engine) | 71.13B | 34.98B | 2.03 | 45.49B | 4.24B | 4.24B | 1.30B | 3.99B | 65.35M | 8.88B | 81.63M |
| DMA.v | Icarus Verilog | 373.71B | 105.57B | 3.54 | 171.84B | 4.69B | 4.69B | 2.63B | 4.57B | 23.69M | 71.17B | 230.71M |
| DMA.v | Verilator C++ | 3.40B | 1.86B | 1.83 | 1.95B | 302.85K | 302.85K | 12.59K | 148.20K | 128.38K | 17.60M | 152.48K |

## EPFL

**Execution Parameters:**
- **Target Suite / Path:** `tests/EPFL_parsed`
- **Circuits Benchmarked:** 11
- **Simulation Vectors (Phase 3):** 50,000 (Warmup: 10)
- **Verification Vectors (Phase 2):** 100
- **Hardware Profiler:** Linux `perf` kernel PMU counters

---

### 1. Zero-Testbench Memory Footprint (Phase 1)

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

### 2. Zero-Testbench Load & Compilation Times (Phase 1)

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

### 3. High-Throughput Simulation Performance (Phase 3)

#### Simulation Wall-Clock Time (ms)

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

#### Speedup Analysis (vs Baseline: Icarus = 1.00x)

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

#### Total Gate Evaluations

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

#### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `12.63x`
- **rx-sweep (Linear Compiled):** `9.59x`
- **rx-oop (OOP Graph):** `5.67x`
- **Pure Python Engine:** `0.17x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `109.47x`

#### Gate Evaluation Highlights

- **Reactor Sweep vs Propagate Total Evaluations Ratio:** `0.79x` (propagate performed more evaluations)

#### Cross-Engine Comparisons

- **Cython Reactor (`rx-prop`) vs Pure Python:** `72.60x` faster
- **Cython Reactor (`rx-sweep`) vs Pure Python:** `55.12x` faster
- **Reactor Sweep vs Propagate Ratio:** `0.76x` (propagate faster)

---

### 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

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

## EPFL_large

**Execution Parameters:**
- **Target Suite / Path:** `tests/EPFL_large_parsed`
- **Circuits Benchmarked:** 8
- **Simulation Vectors (Phase 3):** 500 (Warmup: 10)
- **Verification Vectors (Phase 2):** 100
- **Hardware Profiler:** Linux `perf` kernel PMU counters

---

### 1. Zero-Testbench Memory Footprint (Phase 1)

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

### 2. Zero-Testbench Load & Compilation Times (Phase 1)

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

### 3. High-Throughput Simulation Performance (Phase 3)

#### Simulation Wall-Clock Time (ms)

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

#### Speedup Analysis (vs Baseline: Icarus = 1.00x)

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

#### Total Gate Evaluations

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

#### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `8.84x`
- **rx-sweep (Linear Compiled):** `82.19x`
- **rx-oop (OOP Graph):** `3.69x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `921.36x`

#### Gate Evaluation Highlights

- **Reactor Sweep vs Propagate Total Evaluations Ratio:** `0.09x` (propagate performed more evaluations)

#### Cross-Engine Comparisons

- **Reactor Sweep vs Propagate Ratio:** `9.29x` (sweep faster)

---

### 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

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

## ISCAS85

**Execution Parameters:**
- **Target Suite / Path:** `tests/ISCAS85`
- **Circuits Benchmarked:** 10
- **Simulation Vectors (Phase 3):** 50,000 (Warmup: 10)
- **Verification Vectors (Phase 2):** 100
- **Hardware Profiler:** Linux `perf` kernel PMU counters

---

### 1. Zero-Testbench Memory Footprint (Phase 1)

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

### 2. Zero-Testbench Load & Compilation Times (Phase 1)

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

### 3. High-Throughput Simulation Performance (Phase 3)

#### Simulation Wall-Clock Time (ms)

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

#### Speedup Analysis (vs Baseline: Icarus = 1.00x)

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

#### Total Gate Evaluations

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

#### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `9.64x`
- **rx-sweep (Linear Compiled):** `12.70x`
- **rx-oop (OOP Graph):** `4.58x`
- **Pure Python Engine:** `0.11x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `156.82x`

#### Gate Evaluation Highlights

- **Reactor Sweep vs Propagate Total Evaluations Ratio:** `0.50x` (propagate performed more evaluations)

#### Cross-Engine Comparisons

- **Cython Reactor (`rx-prop`) vs Pure Python:** `85.49x` faster
- **Cython Reactor (`rx-sweep`) vs Pure Python:** `112.62x` faster
- **Reactor Sweep vs Propagate Ratio:** `1.32x` (sweep faster)

---

### 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

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

## ISCAS89

**Execution Parameters:**
- **Target Suite / Path:** `tests/ISCAS89`
- **Circuits Benchmarked:** 15
- **Simulation Vectors (Phase 3):** 50,000 (Warmup: 10)
- **Verification Vectors (Phase 2):** 100
- **Hardware Profiler:** Linux `perf` kernel PMU counters

---

### 1. Zero-Testbench Memory Footprint (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| s27.v | 19 | 0.32 MB (28.1 MB peak) | 0.08 MB (33.2 MB peak) | 0.09 MB (7.8 MB peak) | 0.70 MB (4.4 MB peak) |
| s420.v | 254 | 0.68 MB (28.5 MB peak) | 0.57 MB (33.6 MB peak) | 0.25 MB (8.0 MB peak) | 0.67 MB (4.4 MB peak) |
| s382.v | 189 | 0.69 MB (28.6 MB peak) | 0.63 MB (33.6 MB peak) | 0.17 MB (8.0 MB peak) | 0.66 MB (4.4 MB peak) |
| s641.v | 458 | 0.91 MB (28.8 MB peak) | 0.86 MB (33.9 MB peak) | 0.32 MB (8.2 MB peak) | 0.81 MB (4.4 MB peak) |
| s713.v | 471 | 0.92 MB (28.8 MB peak) | 0.90 MB (33.9 MB peak) | 0.28 MB (8.2 MB peak) | 0.72 MB (4.4 MB peak) |
| s1238.v | 555 | 1.03 MB (28.8 MB peak) | 0.98 MB (34.0 MB peak) | 0.36 MB (8.2 MB peak) | 0.70 MB (4.4 MB peak) |
| s1423.v | 754 | 1.89 MB (29.8 MB peak) | 2.19 MB (35.2 MB peak) | 0.73 MB (8.6 MB peak) | 0.72 MB (4.4 MB peak) |
| s1488.v | 687 | 1.02 MB (28.9 MB peak) | 0.98 MB (33.9 MB peak) | 0.39 MB (8.3 MB peak) | 0.83 MB (4.4 MB peak) |
| s5378.v | 3,043 | 5.29 MB (33.2 MB peak) | 6.59 MB (39.6 MB peak) | 2.10 MB (10.0 MB peak) | 0.72 MB (4.4 MB peak) |
| s9234.v | 5,884 | 8.94 MB (36.8 MB peak) | 11.39 MB (44.4 MB peak) | 4.45 MB (12.2 MB peak) | 0.83 MB (4.4 MB peak) |
| s13207.v | 8,804 | 19.23 MB (47.1 MB peak) | 18.56 MB (51.6 MB peak) | 7.97 MB (15.9 MB peak) | 0.77 MB (4.5 MB peak) |
| s15850.v | 10,534 | 18.54 MB (46.4 MB peak) | 18.88 MB (51.9 MB peak) | 8.54 MB (16.4 MB peak) | 0.82 MB (4.5 MB peak) |
| s35932.v | 18,149 | 37.14 MB (65.0 MB peak) | 44.72 MB (77.8 MB peak) | 18.80 MB (26.8 MB peak) | 0.89 MB (4.6 MB peak) |
| s38584.v | 21,022 | 36.27 MB (64.1 MB peak) | 43.69 MB (76.7 MB peak) | 20.12 MB (28.0 MB peak) | 0.80 MB (4.5 MB peak) |
| s38417.v | 23,950 | 41.55 MB (69.4 MB peak) | 51.87 MB (84.9 MB peak) | 22.43 MB (30.3 MB peak) | 0.91 MB (4.6 MB peak) |

---

### 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| s27.v | 19 | 0.11 ms (0.009 ms opt) | 0.55 ms | 2.43 ms | 2.47 s |
| s420.v | 254 | 0.34 ms (0.040 ms opt) | 2.23 ms | 3.34 ms | 2.47 s |
| s382.v | 189 | 0.33 ms (0.040 ms opt) | 2.22 ms | 3.19 ms | 2.48 s |
| s641.v | 458 | 0.45 ms (0.055 ms opt) | 2.59 ms | 3.91 ms | 2.49 s |
| s713.v | 471 | 0.46 ms (0.056 ms opt) | 2.48 ms | 3.95 ms | 2.48 s |
| s1238.v | 555 | 0.54 ms (0.084 ms opt) | 2.62 ms | 4.46 ms | 2.51 s |
| s1423.v | 754 | 1.03 ms (0.126 ms opt) | 3.73 ms | 5.59 ms | 2.49 s |
| s1488.v | 687 | 0.56 ms (0.081 ms opt) | 2.62 ms | 5.06 ms | 2.49 s |
| s5378.v | 3,043 | 3.08 ms (0.349 ms opt) | 9.66 ms | 18.22 ms | 2.55 s |
| s9234.v | 5,884 | 5.46 ms (0.636 ms opt) | 13.75 ms | 31.98 ms | 2.63 s |
| s13207.v | 8,804 | 10.83 ms (1.236 ms opt) | 26.49 ms | 48.13 ms | 2.75 s |
| s15850.v | 10,534 | 11.16 ms (1.366 ms opt) | 26.01 ms | 66.64 ms | 2.91 s |
| s35932.v | 18,149 | 25.73 ms (3.774 ms opt) | 75.51 ms | 103.89 ms | 3.69 s |
| s38584.v | 21,022 | 26.59 ms (4.723 ms opt) | 76.78 ms | 151.10 ms | 5.49 s |
| s38417.v | 23,950 | 29.67 ms (4.521 ms opt) | 85.76 ms | 140.16 ms | 4.43 s |

---

### 3. High-Throughput Simulation Performance (Phase 3)

#### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| s27.v | 11.61 ms | 9.70 ms | 16.48 ms | 64.79 s | 95.38 ms | 3.02 ms |
| s420.v | 40.69 ms | 50.55 ms | 78.50 ms | 284.39 s | 336.57 ms | 7.93 ms |
| s382.v | 43.28 ms | 45.50 ms | 86.96 ms | 343.32 s | 175.16 ms | 3.73 ms |
| s641.v | 75.05 ms | 87.36 ms | 157.55 ms | 466.34 s | 652.63 ms | 10.76 ms |
| s713.v | 79.93 ms | 90.22 ms | 168.77 ms | 502.15 s | 659.54 ms | 10.27 ms |
| s1238.v | 114.70 ms | 197.51 ms | 288.33 ms | 735.79 s | 823.37 ms | 19.42 ms |
| s1423.v | 217.20 ms | 240.49 ms | 450.35 ms | 1395.68 s | 833.30 ms | 14.09 ms |
| s1488.v | 49.57 ms | 69.63 ms | 132.37 ms | 377.28 s | 524.78 ms | 15.10 ms |
| s5378.v | 614.55 ms | 761.95 ms | 1205.15 ms | 21330.77 s | 2346.84 ms | 29.00 ms |
| s9234.v | 645.12 ms | 872.53 ms | 1358.08 ms | 24996.73 s | 2887.70 ms | 22.31 ms |
| s13207.v | 1551.07 ms | 2229.17 ms | 3471.58 ms | 59799.06 s | 5117.28 ms | 57.82 ms |
| s15850.v | 1443.59 ms | 1958.45 ms | 3402.15 ms | 57937.81 s | 6712.50 ms | 70.61 ms |
| s35932.v | 5490.39 ms | 5475.36 ms | 10.99 s | 234919.76 s | 20.58 s | 189.67 ms |
| s38584.v | 5868.94 ms | 8173.49 ms | 13.45 s | 194068.36 s | 23.00 s | 173.41 ms |
| s38417.v | 4263.36 ms | 5341.47 ms | 9459.19 ms | 354702.02 s | 14.58 s | 163.68 ms |

#### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| s27.v | 8.21x | 9.83x | 5.79x | 0.00x | 1.00x | 31.58x |
| s420.v | 8.27x | 6.66x | 4.29x | 0.00x | 1.00x | 42.42x |
| s382.v | 4.05x | 3.85x | 2.01x | 0.00x | 1.00x | 46.91x |
| s641.v | 8.70x | 7.47x | 4.14x | 0.00x | 1.00x | 60.66x |
| s713.v | 8.25x | 7.31x | 3.91x | 0.00x | 1.00x | 64.24x |
| s1238.v | 7.18x | 4.17x | 2.86x | 0.00x | 1.00x | 42.41x |
| s1423.v | 3.84x | 3.46x | 1.85x | 0.00x | 1.00x | 59.14x |
| s1488.v | 10.59x | 7.54x | 3.96x | 0.00x | 1.00x | 34.76x |
| s5378.v | 3.82x | 3.08x | 1.95x | 0.00x | 1.00x | 80.92x |
| s9234.v | 4.48x | 3.31x | 2.13x | 0.00x | 1.00x | 129.41x |
| s13207.v | 3.30x | 2.30x | 1.47x | 0.00x | 1.00x | 88.50x |
| s15850.v | 4.65x | 3.43x | 1.97x | 0.00x | 1.00x | 95.07x |
| s35932.v | 3.75x | 3.76x | 1.87x | 0.00x | 1.00x | 108.49x |
| s38584.v | 3.92x | 2.81x | 1.71x | 0.00x | 1.00x | 132.61x |
| s38417.v | 3.42x | 2.73x | 1.54x | 0.00x | 1.00x | 89.08x |

#### Total Gate Evaluations

| Circuit | Gates | rx-prop Evals | rx-sweep Evals | rx-oop Evals | Pure Python Evals |
|:---|---:|---:|---:|---:|---:|
| s27.v | 19 | 3,451,929 | 3,444,161 | 3,451,929 | 354,096,105 |
| s420.v | 254 | 17,495,742 | 17,346,964 | 17,495,742 | 1,775,497,381 |
| s382.v | 189 | 21,491,042 | 21,396,363 | 21,491,021 | 2,180,479,021 |
| s641.v | 458 | 26,641,680 | 25,172,013 | 26,641,778 | 2,779,187,827 |
| s713.v | 471 | 28,013,653 | 25,890,687 | 28,226,385 | 2,964,328,240 |
| s1238.v | 555 | 40,189,466 | 36,891,918 | 40,325,248 | 4,576,355,056 |
| s1423.v | 754 | 88,327,556 | 85,688,630 | 89,134,848 | 9,111,795,644 |
| s1488.v | 687 | 21,064,253 | 20,927,185 | 21,083,358 | 2,369,085,374 |
| s5378.v | 3,043 | 231,910,316 | 225,307,618 | 232,070,594 | 124,281,573,976 |
| s9234.v | 5,884 | 257,192,414 | 247,982,197 | 261,305,316 | 145,633,418,542 |
| s13207.v | 8,804 | 654,653,253 | 655,738,161 | 660,907,801 | 344,673,169,471 |
| s15850.v | 10,534 | 602,347,501 | 584,962,381 | 625,958,227 | 333,083,900,946 |
| s35932.v | 18,149 | 2,271,812,624 | 2,296,735,173 | 2,360,123,354 | 1,346,504,726,763 |
| s38584.v | 21,022 | 1,945,083,372 | 1,938,302,482 | 2,000,027,077 | 1,047,715,137,161 |
| s38417.v | 23,950 | 1,698,232,965 | 1,682,564,708 | 1,766,351,854 | 1,969,782,220,304 |

#### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `5.31x`
- **rx-sweep (Linear Compiled):** `4.33x`
- **rx-oop (OOP Graph):** `2.51x`
- **Pure Python Engine:** `0.00x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `66.91x`

#### Gate Evaluation Highlights

- **Reactor Sweep vs Propagate Total Evaluations Ratio:** `0.98x` (propagate performed more evaluations)

#### Cross-Engine Comparisons

- **Cython Reactor (`rx-prop`) vs Pure Python:** `15770.43x` faster
- **Cython Reactor (`rx-sweep`) vs Pure Python:** `12839.41x` faster
- **Reactor Sweep vs Propagate Ratio:** `0.81x` (propagate faster)

---

### 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | Instructions | Cycles | IPC | L1 Loads | L1 Misses | L2 Loads | L2 Misses | L3 Loads | DRAM Loads | Branches | Branch Misses |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| s27.v | rx-prop | 128.27M | 40.00M | 3.21 | 65.07M | 30.53K | 30.53K | 3.33K | 18.21K | 6.43K | 18.24M | 117.03K |
| s27.v | rx-sweep (Linear) | 125.17M | 26.74M | 4.68 | 46.00M | 23.04K | 23.04K | 334.00 | 18.86K | 1.61K | 21.32M | 109.57K |
| s27.v | rx-oop (OOP Engine) | 115.90M | 45.76M | 2.53 | 99.14M | 291.47K | 291.47K | 4.44K | 37.22K | 12.74K | 19.54M | 200.31K |
| s27.v | Pure Python Engine | 15.85M | 9.59M | 1.65 | 36.45M | 25.41K | 25.41K | 1.91K | 1.91K | 1.42K | 9.18M | 23.41K |
| s27.v | Icarus Verilog | 1.20B | 333.33M | 3.60 | 578.10M | 47.42K | 47.42K | 5.53K | 24.15K | 2.42K | 231.95M | 2.95M |
| s27.v | Verilator C++ | 282.65K | 2.82M | 0.10 | 3.33M | 19.67K | 19.67K | 1.37K | 1.37K | 0.00 | 2.28M | 4.62K |
| s420.v | rx-prop | 630.63M | 159.37M | 3.96 | 258.95M | 1.61M | 1.61M | 37.92K | 703.37K | 675.00K | 70.98M | 734.25K |
| s420.v | rx-sweep (Linear) | 697.94M | 195.80M | 3.56 | 263.72M | 1.74M | 1.74M | 33.45K | 422.71K | 395.54K | 137.47M | 1.77M |
| s420.v | rx-oop (OOP Engine) | 676.43M | 297.74M | 2.27 | 432.95M | 3.90M | 3.90M | 63.05K | 1.02M | 881.93K | 93.87M | 1.76M |
| s420.v | Pure Python Engine | 404.24M | 82.82M | 4.88 | 185.92M | 937.72K | 937.72K | 3.01K | 17.09K | 14.45K | 56.26M | 106.70K |
| s420.v | Icarus Verilog | 4.64B | 1.20B | 3.86 | 2.15B | 14.73M | 14.73M | 9.77K | 36.51K | 13.69K | 901.91M | 7.33M |
| s420.v | Verilator C++ | 77.33M | 29.80M | 2.59 | 44.07M | 21.74K | 21.74K | 204.00 | 68.56K | 30.00 | 11.76M | 14.67K |
| s382.v | rx-prop | 626.69M | 140.64M | 4.46 | 274.56M | 302.17K | 302.17K | 3.16K | 17.08K | 3.70K | 63.73M | 240.19K |
| s382.v | rx-sweep (Linear) | 688.34M | 153.96M | 4.47 | 243.15M | 168.68K | 168.68K | 2.94K | 22.80K | 6.10K | 128.20M | 821.60K |
| s382.v | rx-oop (OOP Engine) | 736.40M | 302.54M | 2.43 | 454.21M | 2.82M | 2.82M | 6.12K | 42.43K | 12.17K | 91.37M | 1.02M |
| s382.v | Pure Python Engine | 486.19M | 107.36M | 4.53 | 237.27M | 1.19M | 1.19M | 2.53K | 5.13K | 3.56K | 72.82M | 184.60K |
| s382.v | Icarus Verilog | 2.50B | 626.81M | 3.99 | 1.22B | 10.76M | 10.76M | 3.05K | 18.07K | 860.00 | 486.74M | 3.16M |
| s382.v | Verilator C++ | 1.55M | 6.30M | 0.25 | 11.60M | 16.02K | 16.02K | 417.00 | 417.00 | 0.00 | 3.46M | 7.71K |
| s641.v | rx-prop | 1.01B | 300.34M | 3.37 | 437.91M | 4.95M | 4.95M | 62.77K | 2.36M | 2.32M | 131.89M | 2.67M |
| s641.v | rx-sweep (Linear) | 1.11B | 339.81M | 3.27 | 434.29M | 5.74M | 5.74M | 67.15K | 2.49M | 2.36M | 233.90M | 3.33M |
| s641.v | rx-oop (OOP Engine) | 1.13B | 602.18M | 1.87 | 736.82M | 19.36M | 19.36M | 99.87K | 2.41M | 2.15M | 164.22M | 5.25M |
| s641.v | Pure Python Engine | 699.92M | 143.38M | 4.88 | 348.14M | 1.67M | 1.67M | 8.11K | 33.18K | 25.73K | 100.62M | 181.50K |
| s641.v | Icarus Verilog | 9.14B | 2.35B | 3.88 | 4.22B | 53.13M | 53.13M | 2.74K | 21.40K | 565.00 | 1.78B | 13.60M |
| s641.v | Verilator C++ | 87.05M | 40.76M | 2.14 | 53.69M | 123.56K | 123.56K | 664.00 | 32.84K | 1.00 | 12.87M | 128.78K |
| s713.v | rx-prop | 1.07B | 319.84M | 3.34 | 441.84M | 5.47M | 5.47M | 62.72K | 2.36M | 2.33M | 131.42M | 2.93M |
| s713.v | rx-sweep (Linear) | 1.17B | 362.61M | 3.23 | 435.55M | 6.55M | 6.55M | 62.09K | 2.45M | 2.32M | 241.35M | 3.43M |
| s713.v | rx-oop (OOP Engine) | 1.15B | 629.83M | 1.82 | 760.73M | 19.57M | 19.57M | 74.38K | 2.54M | 2.22M | 156.63M | 6.04M |
| s713.v | Pure Python Engine | 778.05M | 163.90M | 4.75 | 348.48M | 1.65M | 1.65M | 8.04K | 34.67K | 26.46K | 107.86M | 212.38K |
| s713.v | Icarus Verilog | 9.41B | 2.38B | 3.96 | 4.32B | 55.71M | 55.71M | 20.46K | 46.91K | 2.86K | 1.83B | 13.26M |
| s713.v | Verilator C++ | 86.35M | 40.76M | 2.12 | 58.04M | 132.03K | 132.03K | 2.33K | 54.94K | 2.00 | 14.22M | 146.34K |
| s1238.v | rx-prop | 1.22B | 408.38M | 2.99 | 537.94M | 15.52M | 15.52M | 38.14K | 373.17K | 343.68K | 125.27M | 5.52M |
| s1238.v | rx-sweep (Linear) | 1.33B | 719.70M | 1.84 | 584.60M | 18.42M | 18.42M | 31.14K | 96.96K | 74.85K | 268.17M | 14.40M |
| s1238.v | rx-oop (OOP Engine) | 1.41B | 1.05B | 1.35 | 1.07B | 35.53M | 35.53M | 64.22K | 242.07K | 135.12K | 180.88M | 13.13M |
| s1238.v | Pure Python Engine | 1.10B | 236.72M | 4.66 | 527.03M | 2.32M | 2.32M | 7.08K | 21.47K | 12.90K | 153.83M | 508.69K |
| s1238.v | Icarus Verilog | 9.21B | 2.97B | 3.10 | 4.50B | 124.83M | 124.83M | 7.22K | 28.81K | 3.35K | 1.83B | 26.57M |
| s1238.v | Verilator C++ | 108.18M | 66.59M | 1.62 | 70.82M | 27.94K | 27.94K | 1.08K | 14.90K | 2.00 | 12.89M | 279.01K |
| s1423.v | rx-prop | 2.74B | 791.07M | 3.46 | 1.10B | 80.37M | 80.37M | 34.85K | 325.81K | 290.52K | 270.22M | 3.89M |
| s1423.v | rx-sweep (Linear) | 3.00B | 882.63M | 3.40 | 1.07B | 95.39M | 95.39M | 26.89K | 421.43K | 393.77K | 563.39M | 7.31M |
| s1423.v | rx-oop (OOP Engine) | 3.15B | 1.63B | 1.93 | 1.95B | 138.90M | 138.90M | 70.32K | 760.04K | 594.61K | 387.47M | 9.86M |
| s1423.v | Pure Python Engine | 2.23B | 462.47M | 4.83 | 1.03B | 5.97M | 5.97M | 140.05K | 222.06K | 15.70K | 310.64M | 508.87K |
| s1423.v | Icarus Verilog | 11.31B | 3.00B | 3.77 | 5.47B | 133.85M | 133.85M | 14.48K | 47.09K | 7.84K | 2.19B | 16.31M |
| s1423.v | Verilator C++ | 63.45M | 33.89M | 1.87 | 62.93M | 21.22K | 21.22K | 153.00 | 21.83K | 258.00 | 7.39M | 145.12K |
| s1488.v | rx-prop | 635.71M | 176.77M | 3.60 | 290.02M | 5.87M | 5.87M | 14.10K | 50.55K | 20.83K | 71.77M | 1.07M |
| s1488.v | rx-sweep (Linear) | 750.09M | 228.73M | 3.28 | 309.88M | 6.04M | 6.04M | 9.16K | 56.22K | 16.74K | 139.91M | 2.50M |
| s1488.v | rx-oop (OOP Engine) | 762.88M | 474.01M | 1.61 | 549.25M | 13.79M | 13.79M | 22.66K | 118.43K | 33.98K | 95.83M | 4.69M |
| s1488.v | Pure Python Engine | 548.84M | 114.67M | 4.79 | 262.80M | 1.13M | 1.13M | 7.55K | 11.83K | 7.98K | 75.99M | 161.18K |
| s1488.v | Icarus Verilog | 6.27B | 1.88B | 3.34 | 3.04B | 74.73M | 74.73M | 26.26K | 60.55K | 2.77K | 1.25B | 14.79M |
| s1488.v | Verilator C++ | 87.47M | 46.17M | 1.89 | 71.83M | 16.87K | 16.87K | 1.89K | 54.78K | 33.00 | 8.39M | 84.24K |
| s5378.v | rx-prop | 7.23B | 2.26B | 3.20 | 2.92B | 232.44M | 232.44M | 147.52K | 2.51M | 2.40M | 717.55M | 17.51M |
| s5378.v | rx-sweep (Linear) | 8.63B | 2.79B | 3.10 | 3.02B | 319.58M | 319.58M | 136.63K | 2.73M | 2.61M | 1.69B | 30.63M |
| s5378.v | rx-oop (OOP Engine) | 8.27B | 4.38B | 1.89 | 5.20B | 499.47M | 499.47M | 209.82K | 2.71M | 2.21M | 1.02B | 31.58M |
| s5378.v | Pure Python Engine | 1.13B | 261.26M | 4.33 | 528.83M | 3.02M | 3.02M | 1.27M | 1.82M | 13.56K | 160.95M | 439.39K |
| s5378.v | Icarus Verilog | 29.12B | 8.43B | 3.45 | 14.42B | 434.65M | 434.65M | 8.93M | 17.12M | 17.75K | 5.64B | 48.01M |
| s5378.v | Verilator C++ | 151.46M | 94.51M | 1.60 | 137.18M | 149.61K | 149.61K | 1.89K | 27.68K | 7.00 | 14.90M | 183.29K |
| s9234.v | rx-prop | 8.08B | 2.37B | 3.41 | 3.20B | 275.73M | 275.73M | 303.67K | 3.09M | 2.60M | 797.14M | 12.64M |
| s9234.v | rx-sweep (Linear) | 10.50B | 3.19B | 3.29 | 3.43B | 418.40M | 418.40M | 186.29K | 2.93M | 2.76M | 2.16B | 28.16M |
| s9234.v | rx-oop (OOP Engine) | 9.41B | 4.93B | 1.91 | 5.95B | 581.17M | 581.17M | 1.60M | 5.16M | 2.30M | 1.16B | 33.44M |
| s9234.v | Pure Python Engine | 1.33B | 310.17M | 4.28 | 637.78M | 3.53M | 3.53M | 1.85M | 2.68M | 13.06K | 193.62M | 366.88K |
| s9234.v | Icarus Verilog | 34.57B | 10.37B | 3.33 | 17.75B | 550.98M | 550.98M | 54.91M | 83.90M | 36.51K | 6.71B | 51.75M |
| s9234.v | Verilator C++ | 125.61M | 79.66M | 1.58 | 117.96M | 165.75K | 165.75K | 4.15K | 142.47K | 27.00 | 11.76M | 430.83K |
| s13207.v | rx-prop | 19.98B | 5.64B | 3.54 | 7.97B | 719.90M | 719.90M | 5.06M | 14.51M | 5.21M | 1.93B | 25.44M |
| s13207.v | rx-sweep (Linear) | 25.42B | 8.09B | 3.14 | 8.82B | 1.00B | 1.00B | 15.27M | 34.69M | 5.87M | 5.12B | 81.77M |
| s13207.v | rx-oop (OOP Engine) | 23.21B | 12.52B | 1.85 | 14.67B | 1.61B | 1.61B | 143.21M | 257.52M | 4.66M | 2.83B | 63.42M |
| s13207.v | Pure Python Engine | 3.27B | 767.62M | 4.26 | 1.49B | 8.85M | 8.85M | 6.87M | 10.08M | 36.09K | 461.88M | 762.83K |
| s13207.v | Icarus Verilog | 59.33B | 18.39B | 3.23 | 31.38B | 968.67M | 968.67M | 244.76M | 504.62M | 72.34K | 11.32B | 67.68M |
| s13207.v | Verilator C++ | 306.39M | 198.92M | 1.54 | 257.13M | 226.65K | 226.65K | 1.57K | 228.72K | 13.81K | 11.93M | 582.66K |
| s15850.v | rx-prop | 18.70B | 5.27B | 3.55 | 7.41B | 659.97M | 659.97M | 8.75M | 23.64M | 6.29M | 1.82B | 22.69M |
| s15850.v | rx-sweep (Linear) | 23.60B | 7.13B | 3.31 | 7.78B | 969.20M | 969.20M | 17.68M | 48.56M | 7.06M | 4.83B | 59.72M |
| s15850.v | rx-oop (OOP Engine) | 22.37B | 12.29B | 1.82 | 14.35B | 1.37B | 1.37B | 138.25M | 234.42M | 5.99M | 2.74B | 68.24M |
| s15850.v | Pure Python Engine | 3.25B | 754.74M | 4.31 | 1.46B | 8.35M | 8.35M | 6.25M | 9.29M | 77.91K | 450.73M | 651.46K |
| s15850.v | Icarus Verilog | 74.92B | 24.10B | 3.11 | 39.40B | 1.28B | 1.28B | 428.24M | 740.09M | 108.77K | 14.52B | 94.17M |
| s15850.v | Verilator C++ | 404.28M | 251.59M | 1.61 | 293.60M | 84.52K | 84.52K | 1.15K | 264.14K | 22.21K | 21.07M | 1.25M |
| s35932.v | rx-prop | 68.87B | 19.74B | 3.49 | 26.96B | 3.00B | 3.00B | 335.98M | 1.73B | 2.66M | 6.47B | 11.44M |
| s35932.v | rx-sweep (Linear) | 78.20B | 19.68B | 3.97 | 26.41B | 3.24B | 3.24B | 218.32M | 1.76B | 2.63M | 14.14B | 40.89M |
| s35932.v | rx-oop (OOP Engine) | 82.81B | 39.47B | 2.10 | 46.75B | 5.81B | 5.81B | 1.49B | 4.78B | 2.24M | 9.93B | 37.13M |
| s35932.v | Pure Python Engine | 12.99B | 3.04B | 4.28 | 5.83B | 36.64M | 36.64M | 28.20M | 43.48M | 1.06M | 1.81B | 2.44M |
| s35932.v | Icarus Verilog | 289.57B | 73.85B | 3.92 | 135.51B | 7.32B | 7.32B | 2.13B | 5.53B | 303.67K | 56.87B | 58.25M |
| s35932.v | Verilator C++ | 605.98M | 683.72M | 0.89 | 646.17M | 78.64K | 78.64K | 612.00 | 38.34K | 293.00 | 12.95M | 48.42K |
| s38584.v | rx-prop | 58.74B | 21.08B | 2.79 | 23.52B | 2.41B | 2.41B | 443.27M | 1.34B | 2.38M | 5.51B | 114.84M |
| s38584.v | rx-sweep (Linear) | 70.11B | 29.36B | 2.39 | 27.01B | 2.94B | 2.94B | 381.79M | 1.71B | 2.94M | 13.20B | 373.52M |
| s38584.v | rx-oop (OOP Engine) | 69.59B | 48.29B | 1.44 | 46.98B | 4.57B | 4.57B | 1.67B | 3.46B | 3.25M | 8.35B | 271.92M |
| s38584.v | Pure Python Engine | 10.07B | 2.50B | 4.03 | 4.57B | 26.11M | 26.11M | 21.99M | 33.00M | 502.14K | 1.40B | 2.77M |
| s38584.v | Icarus Verilog | 204.39B | 82.61B | 2.47 | 115.64B | 4.72B | 4.72B | 2.35B | 3.63B | 298.55K | 39.99B | 391.69M |
| s38584.v | Verilator C++ | 867.21M | 623.23M | 1.39 | 722.85M | 156.23K | 156.23K | 4.64K | 143.65K | 1.02K | 16.72M | 752.42K |
| s38417.v | rx-prop | 50.83B | 15.33B | 3.32 | 20.08B | 1.90B | 1.90B | 274.49M | 911.13M | 2.07M | 4.72B | 38.17M |
| s38417.v | rx-sweep (Linear) | 64.33B | 19.19B | 3.35 | 21.26B | 2.62B | 2.62B | 203.72M | 1.39B | 2.37M | 12.93B | 124.60M |
| s38417.v | rx-oop (OOP Engine) | 61.09B | 33.93B | 1.80 | 36.97B | 4.10B | 4.10B | 1.27B | 3.31B | 2.19M | 7.32B | 91.82M |
| s38417.v | Pure Python Engine | 4.21B | 1.01B | 4.17 | 1.94B | 12.89M | 12.89M | 9.46M | 13.96M | 168.16K | 584.45M | 1.22M |
| s38417.v | Icarus Verilog | 168.39B | 52.36B | 3.22 | 87.44B | 3.32B | 3.32B | 1.20B | 2.43B | 323.95K | 32.46B | 126.10M |
| s38417.v | Verilator C++ | 833.90M | 591.45M | 1.41 | 591.78M | 155.04K | 155.04K | 1.44K | 121.13K | 330.00 | 13.78M | 137.21K |

## Hyp

**Execution Parameters:**
- **Target Suite / Path:** `tests/EPFL_mammoth_parsed`
- **Circuits Benchmarked:** 1
- **Simulation Vectors (Phase 3):** 500 (Warmup: 10)
- **Verification Vectors (Phase 2):** 100
- **Hardware Profiler:** Linux `perf` kernel PMU counters

---

### 1. Zero-Testbench Memory Footprint (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| hyp.v | 420,896 | 392.25 MB (419.8 MB peak) | N/A | 280.49 MB (288.4 MB peak) | 3.54 MB (7.2 MB peak) |

---

### 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| hyp.v | 420,896 | 613.74 ms (100.939 ms opt) | N/A | 2.62 s | 116.02 s |

---

### 3. High-Throughput Simulation Performance (Phase 3)

#### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| hyp.v | 180.48 s | 851.64 ms | 301.93 s | N/A | 1496.10 s | 245.20 ms |

#### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| hyp.v | 8.29x | 1756.72x | 4.96x | N/A | 1.00x | 6101.61x |

#### Total Gate Evaluations

| Circuit | Gates | rx-prop Evals | rx-sweep Evals | rx-oop Evals | Pure Python Evals |
|:---|---:|---:|---:|---:|---:|
| hyp.v | 420,896 | 25,609,842,152 | 129,253,082 | 26,040,243,146 | N/A |

#### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `8.29x`
- **rx-sweep (Linear Compiled):** `1756.72x`
- **rx-oop (OOP Graph):** `4.96x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `6101.61x`

#### Gate Evaluation Highlights

- **Reactor Sweep vs Propagate Total Evaluations Ratio:** `0.01x` (propagate performed more evaluations)

#### Cross-Engine Comparisons

- **Reactor Sweep vs Propagate Ratio:** `211.92x` (sweep faster)

---

### 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | Instructions | Cycles | IPC | L1 Loads | L1 Misses | L2 Loads | L2 Misses | L3 Loads | DRAM Loads | Branches | Branch Misses |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| hyp.v | rx-prop | 850.36B | 647.66B | 1.31 | 327.92B | 43.64B | 43.64B | 28.19B | 46.49B | 110.24M | 80.07B | 3.93B |
| hyp.v | rx-sweep (Linear) | 4.52B | 3.02B | 1.50 | 2.10B | 152.09M | 152.09M | 38.85M | 149.72M | 15.30M | 840.87M | 44.86M |
| hyp.v | rx-oop (OOP Engine) | 963.99B | 1083.53B | 0.89 | 819.76B | 56.64B | 56.64B | 44.56B | 65.35B | 342.92M | 116.21B | 9.32B |
| hyp.v | Icarus Verilog | 6743.95B | 5369.88B | 1.26 | 4341.59B | 176.92B | 176.92B | 151.12B | 211.83B | 18.03B | 1352.22B | 19.39B |
| hyp.v | Verilator C++ | 268.15M | 866.95M | 0.31 | 168.78M | 7.39M | 7.39M | 20.65M | 21.20M | 6.03K | 40.72M | 1.18M |
