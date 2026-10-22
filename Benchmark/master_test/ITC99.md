# Master Test Unified Benchmark Report: tests/IWLS2005/itc99

**Execution Parameters:**
- **Target Suite / Path:** `tests/IWLS2005/itc99`
- **Circuits Benchmarked:** 21
- **Simulation Vectors (Phase 3):** 50,000 (Warmup: 10)
- **Verification Vectors (Phase 2):** 100
- **Hardware Profiler:** Linux `perf` kernel PMU counters
- **Note (2026-10-22):** re-run after the Verilator library fix: Verilator now compiles `iwls_sequential_harness.verilator_gsclib()` (the cell library with its sequential UDPs as nonblocking modules), because Verilator 5.052 lowers the original UDP flops to blocking assignments, which is order-dependent and slow. Icarus uses the original library; Darion simulates every flop as the 10-gate NAND master-slave of `tests/src/DFFSR.json`, so the flop models differ between the three tools (not a same-netlist comparison). The previous report (blocking-UDP Verilator) is in git history.

---

## 1. Zero-Testbench Memory Footprint (Phase 1)

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

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

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

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

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

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

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

### Total Gate Evaluations

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

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `3.81x`
- **rx-sweep (Linear Compiled):** `3.96x`
- **rx-oop (OOP Graph):** `1.85x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `26.63x`

### Gate Evaluation Highlights

- **Reactor Sweep vs Propagate Total Evaluations Ratio:** `0.82x` (propagate performed more evaluations)

### Cross-Engine Comparisons

- **Reactor Sweep vs Propagate Ratio:** `1.04x` (sweep faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

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
