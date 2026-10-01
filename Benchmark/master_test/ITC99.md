# Master Test Unified Benchmark Report: tests/IWLS2005/itc99

**Execution Parameters:**
- **Target Suite / Path:** `tests/IWLS2005/itc99`
- **Circuits Benchmarked:** 21
- **Simulation Vectors (Phase 3):** 50,000 (Warmup: 10)
- **Verification Vectors (Phase 2):** 100
- **Hardware Profiler:** Linux `perf` kernel PMU counters

---

## 1. Zero-Testbench Memory Footprint (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| b02.v | 52 | 0.60 MB (28.2 MB peak) | N/A | 0.38 MB (8.2 MB peak) | 0.70 MB (4.4 MB peak) |
| b01.v | 101 | 4.65 MB (32.2 MB peak) | N/A | 0.52 MB (8.4 MB peak) | 0.69 MB (4.4 MB peak) |
| b06.v | 100 | 0.74 MB (28.3 MB peak) | N/A | 0.63 MB (8.5 MB peak) | 0.71 MB (4.4 MB peak) |
| b08.v | 309 | 1.07 MB (28.6 MB peak) | N/A | 1.21 MB (9.0 MB peak) | 0.71 MB (4.4 MB peak) |
| b09.v | 331 | 1.25 MB (28.9 MB peak) | N/A | 1.41 MB (9.2 MB peak) | 0.73 MB (4.4 MB peak) |
| b10.v | 417 | 1.15 MB (28.7 MB peak) | N/A | 1.43 MB (9.3 MB peak) | 0.70 MB (4.4 MB peak) |
| b03.v | 549 | 1.48 MB (29.0 MB peak) | N/A | 1.86 MB (9.7 MB peak) | 0.74 MB (4.4 MB peak) |
| b13.v | 540 | 1.84 MB (29.4 MB peak) | N/A | 2.08 MB (9.9 MB peak) | 0.76 MB (4.4 MB peak) |
| b07.v | 859 | 2.00 MB (29.7 MB peak) | N/A | 3.01 MB (10.9 MB peak) | 0.82 MB (4.4 MB peak) |
| b11.v | 1,046 | 1.93 MB (29.5 MB peak) | N/A | 3.19 MB (11.0 MB peak) | 0.72 MB (4.4 MB peak) |
| b04.v | 1,259 | 2.59 MB (30.2 MB peak) | N/A | 3.79 MB (11.7 MB peak) | 0.71 MB (4.4 MB peak) |
| b05.v | 1,292 | 2.16 MB (29.7 MB peak) | N/A | 3.80 MB (11.7 MB peak) | 0.71 MB (4.4 MB peak) |
| b12.v | 2,937 | 4.94 MB (32.5 MB peak) | N/A | 8.88 MB (16.8 MB peak) | 0.79 MB (4.5 MB peak) |
| b14.v | 10,624 | 16.59 MB (44.9 MB peak) | N/A | 36.88 MB (44.7 MB peak) | 1.05 MB (4.7 MB peak) |
| b15.v | 17,594 | 23.47 MB (52.1 MB peak) | N/A | 56.82 MB (64.7 MB peak) | 1.11 MB (4.8 MB peak) |
| b21.v | 23,092 | 29.02 MB (59.7 MB peak) | N/A | 78.61 MB (86.4 MB peak) | 1.10 MB (4.8 MB peak) |
| b20.v | 23,839 | 28.27 MB (59.3 MB peak) | N/A | 79.94 MB (87.8 MB peak) | 1.23 MB (4.9 MB peak) |
| b22.v | 34,903 | 38.01 MB (71.8 MB peak) | N/A | 119.11 MB (126.9 MB peak) | 1.39 MB (5.1 MB peak) |
| b17.v | 52,250 | 58.88 MB (91.4 MB peak) | N/A | 173.09 MB (180.9 MB peak) | 1.47 MB (5.1 MB peak) |
| b18.v | 132,940 | 135.86 MB (182.8 MB peak) | N/A | 429.05 MB (436.9 MB peak) | 2.48 MB (6.2 MB peak) |
| b19.v | 257,489 | 264.71 MB (332.4 MB peak) | N/A | 827.55 MB (835.4 MB peak) | 3.38 MB (7.1 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| b02.v | 52 | 0.14 ms (0.018 ms opt) | N/A | 4.15 ms | 2.52 s |
| b01.v | 101 | 0.28 ms (0.023 ms opt) | N/A | 4.64 ms | 2.54 s |
| b06.v | 100 | 0.20 ms (0.026 ms opt) | N/A | 5.40 ms | 2.53 s |
| b08.v | 309 | 0.44 ms (0.064 ms opt) | N/A | 7.87 ms | 2.57 s |
| b09.v | 331 | 0.54 ms (0.080 ms opt) | N/A | 7.58 ms | 2.58 s |
| b10.v | 417 | 0.47 ms (0.075 ms opt) | N/A | 8.32 ms | 2.54 s |
| b03.v | 549 | 0.67 ms (0.093 ms opt) | N/A | 10.43 ms | 2.57 s |
| b13.v | 540 | 0.89 ms (0.122 ms opt) | N/A | 10.92 ms | 2.60 s |
| b07.v | 859 | 1.05 ms (0.141 ms opt) | N/A | 15.03 ms | 2.60 s |
| b11.v | 1,046 | 1.00 ms (0.141 ms opt) | N/A | 15.87 ms | 2.61 s |
| b04.v | 1,259 | 1.41 ms (0.187 ms opt) | N/A | 19.11 ms | 2.64 s |
| b05.v | 1,292 | 1.18 ms (0.169 ms opt) | N/A | 19.09 ms | 2.64 s |
| b12.v | 2,937 | 2.98 ms (0.382 ms opt) | N/A | 38.33 ms | 2.98 s |
| b14.v | 10,624 | 9.93 ms (1.297 ms opt) | N/A | 172.10 ms | 6.10 s |
| b15.v | 17,594 | 17.26 ms (2.315 ms opt) | N/A | 289.77 ms | 8.51 s |
| b21.v | 23,092 | 21.47 ms (3.393 ms opt) | N/A | 400.42 ms | 10.38 s |
| b20.v | 23,839 | 22.77 ms (3.587 ms opt) | N/A | 407.44 ms | 10.58 s |
| b22.v | 34,903 | 33.47 ms (7.572 ms opt) | N/A | 622.06 ms | 15.80 s |
| b17.v | 52,250 | 58.86 ms (18.524 ms opt) | N/A | 928.73 ms | 23.14 s |
| b18.v | 132,940 | 243.07 ms (48.829 ms opt) | N/A | 2.37 s | 67.56 s |
| b19.v | 257,489 | 558.70 ms (113.629 ms opt) | N/A | 4.73 s | 160.41 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| b02.v | 20.62 ms | 14.72 ms | N/A | N/A | 146.77 ms | 4.00 ms |
| b01.v | 27.37 ms | 20.80 ms | N/A | N/A | 179.28 ms | 5.04 ms |
| b06.v | 37.86 ms | 28.57 ms | N/A | N/A | 157.24 ms | 11.35 ms |
| b08.v | 58.62 ms | 65.00 ms | N/A | N/A | 259.13 ms | 20.24 ms |
| b09.v | 65.73 ms | 63.70 ms | N/A | N/A | 244.97 ms | 19.00 ms |
| b10.v | 76.44 ms | 80.47 ms | N/A | N/A | 430.22 ms | 26.33 ms |
| b03.v | 106.00 ms | 111.72 ms | N/A | N/A | 271.03 ms | 28.29 ms |
| b13.v | 128.13 ms | 138.89 ms | N/A | N/A | 353.21 ms | 41.66 ms |
| b07.v | 126.53 ms | 141.00 ms | N/A | N/A | 294.16 ms | 37.30 ms |
| b11.v | 137.00 ms | 151.58 ms | N/A | N/A | 387.87 ms | 45.99 ms |
| b04.v | 301.95 ms | 355.15 ms | N/A | N/A | 1398.61 ms | 75.19 ms |
| b05.v | 91.39 ms | 137.88 ms | N/A | N/A | 190.98 ms | 52.84 ms |
| b12.v | 322.47 ms | 366.84 ms | N/A | N/A | 879.93 ms | 129.65 ms |
| b14.v | 3128.71 ms | 2278.61 ms | N/A | N/A | 6689.06 ms | 444.67 ms |
| b15.v | 1630.18 ms | 2029.09 ms | N/A | N/A | 5439.29 ms | 684.98 ms |
| b21.v | 4125.89 ms | 3298.98 ms | N/A | N/A | 8536.47 ms | 1020.78 ms |
| b20.v | 4543.52 ms | 3892.31 ms | N/A | N/A | 9858.63 ms | 1081.97 ms |
| b22.v | 8831.57 ms | 6959.63 ms | N/A | N/A | 19.82 s | 2165.12 ms |
| b17.v | 5579.84 ms | 6242.19 ms | N/A | N/A | 12.60 s | 5431.04 ms |
| b18.v | 18.64 s | 17.54 s | N/A | N/A | 94.91 s | 28.03 s |
| b19.v | 31.76 s | 32.42 s | N/A | N/A | 149.42 s | 64.06 s |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| b02.v | 7.12x | 9.97x | N/A | N/A | 1.00x | 36.66x |
| b01.v | 6.55x | 8.62x | N/A | N/A | 1.00x | 35.59x |
| b06.v | 4.15x | 5.50x | N/A | N/A | 1.00x | 13.86x |
| b08.v | 4.42x | 3.99x | N/A | N/A | 1.00x | 12.80x |
| b09.v | 3.73x | 3.85x | N/A | N/A | 1.00x | 12.89x |
| b10.v | 5.63x | 5.35x | N/A | N/A | 1.00x | 16.34x |
| b03.v | 2.56x | 2.43x | N/A | N/A | 1.00x | 9.58x |
| b13.v | 2.76x | 2.54x | N/A | N/A | 1.00x | 8.48x |
| b07.v | 2.32x | 2.09x | N/A | N/A | 1.00x | 7.89x |
| b11.v | 2.83x | 2.56x | N/A | N/A | 1.00x | 8.43x |
| b04.v | 4.63x | 3.94x | N/A | N/A | 1.00x | 18.60x |
| b05.v | 2.09x | 1.39x | N/A | N/A | 1.00x | 3.61x |
| b12.v | 2.73x | 2.40x | N/A | N/A | 1.00x | 6.79x |
| b14.v | 2.14x | 2.94x | N/A | N/A | 1.00x | 15.04x |
| b15.v | 3.34x | 2.68x | N/A | N/A | 1.00x | 7.94x |
| b21.v | 2.07x | 2.59x | N/A | N/A | 1.00x | 8.36x |
| b20.v | 2.17x | 2.53x | N/A | N/A | 1.00x | 9.11x |
| b22.v | 2.24x | 2.85x | N/A | N/A | 1.00x | 9.16x |
| b17.v | 2.26x | 2.02x | N/A | N/A | 1.00x | 2.32x |
| b18.v | 5.09x | 5.41x | N/A | N/A | 1.00x | 3.39x |
| b19.v | 4.70x | 4.61x | N/A | N/A | 1.00x | 2.33x |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `3.32x`
- **rx-sweep (Linear Compiled):** `3.37x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `9.22x`

### Cross-Engine Comparisons

- **Reactor Sweep vs Propagate Ratio:** `1.02x` (sweep faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | Instructions | Cycles | IPC | L1 Loads | L1 Misses | L2 Loads | L2 Misses | L3 Loads | DRAM Loads | Branches | Branch Misses |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| b02.v | rx-prop | 300.66M | 73.94M | 4.07 | 142.17M | 722.41K | 722.41K | 17.92K | 34.14K | 14.90K | 38.86M | 92.27K |
| b02.v | rx-sweep (Linear) | 250.24M | 57.01M | 4.39 | 90.03M | 622.61K | 622.61K | 1.03K | 35.95K | 15.80K | 47.67M | 106.74K |
| b02.v | Icarus Verilog | 2.10B | 548.14M | 3.83 | 973.94M | 1.34M | 1.34M | 29.52K | 109.09K | 4.86K | 413.02M | 3.48M |
| b02.v | Verilator C++ | 10.62M | 6.83M | 1.56 | 30.55M | 21.05K | 21.05K | 1.42K | 28.32K | 280.00 | 9.33M | 47.98K |
| b01.v | rx-prop | 402.12M | 91.39M | 4.40 | 152.37M | 47.74K | 47.74K | 1.00K | 33.13K | 4.25K | 39.77M | 93.59K |
| b01.v | rx-sweep (Linear) | 348.14M | 76.43M | 4.56 | 137.35M | 851.92K | 851.92K | 23.95K | 39.68K | 17.45K | 64.51M | 157.47K |
| b01.v | Icarus Verilog | 2.59B | 671.95M | 3.85 | 1.19B | 6.12M | 6.12M | 22.53K | 80.70K | 4.25K | 509.70M | 4.12M |
| b01.v | Verilator C++ | 27.98M | 11.44M | 2.45 | 39.71M | 27.09K | 27.09K | 964.00 | 24.29K | 141.00 | 11.65M | 78.95K |
| b06.v | rx-prop | 592.94M | 138.08M | 4.29 | 232.02M | 267.47K | 267.47K | 2.88K | 30.19K | 17.25K | 59.81M | 136.57K |
| b06.v | rx-sweep (Linear) | 483.69M | 111.21M | 4.35 | 187.14M | 690.32K | 690.32K | 11.99K | 33.91K | 14.65K | 100.90M | 264.36K |
| b06.v | Icarus Verilog | 2.46B | 583.40M | 4.21 | 1.14B | 4.10M | 4.10M | 33.19K | 39.10K | 2.55K | 479.07M | 3.01M |
| b06.v | Verilator C++ | 69.65M | 36.66M | 1.90 | 38.91M | 19.26K | 19.26K | 937.00 | 3.42K | 179.00 | 11.68M | 126.32K |
| b08.v | rx-prop | 819.87M | 217.82M | 3.76 | 358.07M | 1.91M | 1.91M | 13.98K | 68.62K | 46.98K | 94.22M | 593.73K |
| b08.v | rx-sweep (Linear) | 950.11M | 245.45M | 3.87 | 334.07M | 3.63M | 3.63M | 32.69K | 321.26K | 296.33K | 191.93M | 1.56M |
| b08.v | Icarus Verilog | 3.86B | 994.71M | 3.88 | 1.71B | 29.39M | 29.39M | 39.40K | 117.48K | 4.55K | 744.72M | 5.89M |
| b08.v | Verilator C++ | 121.93M | 68.80M | 1.77 | 71.94M | 8.69K | 8.69K | 909.00 | 31.88K | 0.00 | 18.18M | 175.76K |
| b09.v | rx-prop | 936.86M | 233.63M | 4.01 | 357.80M | 1.24M | 1.24M | 5.61K | 29.06K | 8.69K | 89.30M | 185.32K |
| b09.v | rx-sweep (Linear) | 982.45M | 227.57M | 4.32 | 330.80M | 2.09M | 2.09M | 2.91K | 29.99K | 13.67K | 204.92M | 728.16K |
| b09.v | Icarus Verilog | 3.86B | 927.73M | 4.16 | 1.78B | 58.23M | 58.23M | 35.03K | 119.39K | 7.69K | 749.50M | 3.32M |
| b09.v | Verilator C++ | 125.94M | 54.82M | 2.30 | 91.87M | 14.51K | 14.51K | 1.90K | 30.44K | 459.00 | 21.12M | 91.15K |
| b10.v | rx-prop | 1.06B | 286.11M | 3.72 | 417.78M | 5.04M | 5.04M | 32.66K | 385.89K | 355.73K | 110.62M | 1.31M |
| b10.v | rx-sweep (Linear) | 1.02B | 302.10M | 3.39 | 374.95M | 5.53M | 5.53M | 50.11K | 1.13M | 1.10M | 206.22M | 2.83M |
| b10.v | Icarus Verilog | 6.15B | 1.63B | 3.79 | 2.83B | 84.59M | 84.59M | 29.85K | 131.60K | 21.92K | 1.21B | 9.66M |
| b10.v | Verilator C++ | 154.23M | 90.91M | 1.70 | 97.55M | 11.44K | 11.44K | 244.00 | 41.22K | 31.00 | 17.32M | 180.86K |
| b03.v | rx-prop | 1.46B | 381.78M | 3.83 | 568.25M | 11.95M | 11.95M | 5.70K | 49.04K | 39.35K | 140.67M | 623.80K |
| b03.v | rx-sweep (Linear) | 1.43B | 407.00M | 3.52 | 490.99M | 22.77M | 22.77M | 36.74K | 84.88K | 56.91K | 288.31M | 2.28M |
| b03.v | Icarus Verilog | 4.03B | 1.05B | 3.86 | 1.85B | 58.71M | 58.71M | 41.01K | 118.11K | 37.80K | 787.75M | 5.16M |
| b03.v | Verilator C++ | 206.70M | 98.70M | 2.09 | 111.91M | 10.69K | 10.69K | 465.00 | 6.36K | 2.00 | 23.11M | 199.76K |
| b13.v | rx-prop | 1.75B | 466.60M | 3.75 | 690.58M | 19.99M | 19.99M | 41.66K | 343.84K | 314.77K | 173.86M | 638.19K |
| b13.v | rx-sweep (Linear) | 1.95B | 512.99M | 3.81 | 641.13M | 55.61M | 55.61M | 62.59K | 615.44K | 579.68K | 393.49M | 1.85M |
| b13.v | Icarus Verilog | 5.52B | 1.36B | 4.05 | 2.48B | 82.43M | 82.43M | 80.18K | 161.03K | 25.57K | 1.07B | 6.41M |
| b13.v | Verilator C++ | 251.47M | 144.68M | 1.74 | 161.52M | 20.38K | 20.38K | 655.00 | 4.94K | 2.00 | 33.49M | 265.88K |
| b07.v | rx-prop | 1.78B | 448.98M | 3.97 | 660.58M | 19.65M | 19.65M | 7.68K | 38.53K | 20.93K | 163.15M | 328.60K |
| b07.v | rx-sweep (Linear) | 2.01B | 506.15M | 3.97 | 592.78M | 72.38M | 72.38M | 2.73K | 31.86K | 17.76K | 404.91M | 1.25M |
| b07.v | Icarus Verilog | 4.72B | 1.14B | 4.14 | 2.13B | 83.67M | 83.67M | 72.20K | 187.49K | 16.49K | 934.25M | 4.19M |
| b07.v | Verilator C++ | 296.42M | 134.10M | 2.21 | 164.14M | 17.59K | 17.59K | 572.00 | 3.22K | 3.00 | 33.74M | 99.54K |
| b11.v | rx-prop | 1.78B | 490.94M | 3.62 | 698.31M | 24.87M | 24.87M | 16.98K | 76.14K | 47.23K | 176.57M | 2.16M |
| b11.v | rx-sweep (Linear) | 1.85B | 558.89M | 3.30 | 583.64M | 66.28M | 66.28M | 33.08K | 337.26K | 280.38K | 381.68M | 3.84M |
| b11.v | Icarus Verilog | 5.41B | 1.50B | 3.62 | 2.53B | 71.78M | 71.78M | 69.27K | 218.13K | 27.91K | 1.05B | 8.99M |
| b11.v | Verilator C++ | 274.85M | 164.92M | 1.67 | 166.77M | 15.10K | 15.10K | 221.00 | 4.92K | 13.00 | 25.63M | 324.63K |
| b04.v | rx-prop | 3.43B | 1.10B | 3.12 | 1.33B | 98.47M | 98.47M | 124.68K | 1.35M | 1.18M | 333.18M | 8.43M |
| b04.v | rx-sweep (Linear) | 3.51B | 1.28B | 2.74 | 1.24B | 142.88M | 142.88M | 61.74K | 894.79K | 856.99K | 670.52M | 16.18M |
| b04.v | Icarus Verilog | 17.03B | 5.16B | 3.30 | 8.44B | 257.92M | 257.92M | 1.64M | 2.82M | 32.06K | 3.34B | 37.61M |
| b04.v | Verilator C++ | 441.74M | 254.00M | 1.74 | 249.74M | 7.71K | 7.71K | 1.64K | 51.43K | 679.00 | 39.98M | 777.92K |
| b05.v | rx-prop | 1.34B | 325.48M | 4.13 | 499.55M | 7.18M | 7.18M | 1.63K | 30.50K | 13.31K | 124.62M | 155.47K |
| b05.v | rx-sweep (Linear) | 1.79B | 491.71M | 3.64 | 515.04M | 80.87M | 80.87M | 27.08K | 35.29K | 24.50K | 383.63M | 1.51M |
| b05.v | Icarus Verilog | 3.23B | 785.21M | 4.12 | 1.43B | 52.53M | 52.53M | 87.21K | 235.07K | 15.90K | 629.74M | 2.98M |
| b05.v | Verilator C++ | 281.52M | 173.78M | 1.62 | 181.28M | 21.21K | 21.21K | 2.29K | 24.55K | 751.00 | 28.05M | 159.20K |
| b12.v | rx-prop | 3.99B | 1.15B | 3.46 | 1.53B | 127.06M | 127.06M | 56.02K | 115.83K | 47.20K | 378.91M | 1.26M |
| b12.v | rx-sweep (Linear) | 5.25B | 1.33B | 3.94 | 1.49B | 251.19M | 251.19M | 43.17K | 335.05K | 300.99K | 1.10B | 4.40M |
| b12.v | Icarus Verilog | 12.93B | 3.38B | 3.83 | 5.99B | 256.53M | 256.53M | 4.81M | 8.39M | 108.00K | 2.53B | 15.14M |
| b12.v | Verilator C++ | 884.83M | 464.35M | 1.91 | 470.09M | 29.78K | 29.78K | 2.66K | 33.91K | 6.23K | 68.04M | 272.97K |
| b14.v | rx-prop | 28.98B | 11.27B | 2.57 | 11.12B | 1.14B | 1.14B | 28.47M | 62.37M | 2.93M | 2.68B | 145.66M |
| b14.v | rx-sweep (Linear) | 20.30B | 8.21B | 2.47 | 6.78B | 965.86M | 965.86M | 16.17M | 44.24M | 3.32M | 3.73B | 119.22M |
| b14.v | Icarus Verilog | 69.75B | 24.76B | 2.82 | 36.54B | 1.58B | 1.58B | 377.33M | 550.57M | 812.87K | 13.81B | 152.96M |
| b14.v | Verilator C++ | 3.27B | 1.60B | 2.04 | 1.84B | 24.02K | 24.02K | 6.36K | 39.39K | 32.59K | 266.27M | 2.62M |
| b15.v | rx-prop | 19.70B | 5.89B | 3.34 | 7.36B | 765.58M | 765.58M | 15.76M | 36.76M | 3.34M | 1.83B | 10.03M |
| b15.v | rx-sweep (Linear) | 24.84B | 7.31B | 3.40 | 7.02B | 1.30B | 1.30B | 48.71M | 225.61M | 3.82M | 5.28B | 40.52M |
| b15.v | Icarus Verilog | 70.16B | 20.92B | 3.35 | 32.53B | 1.37B | 1.37B | 537.46M | 971.30M | 1.01M | 13.64B | 62.25M |
| b15.v | Verilator C++ | 6.10B | 2.47B | 2.47 | 3.01B | 31.88K | 31.88K | 27.24K | 95.27K | 67.83K | 529.13M | 739.90K |
| b21.v | rx-prop | 37.84B | 14.78B | 2.56 | 14.43B | 1.58B | 1.58B | 143.75M | 297.38M | 2.93M | 3.48B | 149.80M |
| b21.v | rx-sweep (Linear) | 32.91B | 11.83B | 2.78 | 9.86B | 1.71B | 1.71B | 90.98M | 588.40M | 2.98M | 6.71B | 121.83M |
| b21.v | Icarus Verilog | 92.11B | 32.57B | 2.83 | 47.13B | 2.06B | 2.06B | 699.48M | 1.18B | 2.99M | 18.17B | 168.94M |
| b21.v | Verilator C++ | 8.32B | 3.68B | 2.26 | 4.38B | 249.09K | 249.09K | 810.42K | 884.11K | 48.22K | 675.16M | 3.71M |
| b20.v | rx-prop | 40.86B | 16.22B | 2.52 | 15.57B | 1.68B | 1.68B | 179.65M | 381.53M | 3.23M | 3.76B | 174.79M |
| b20.v | rx-sweep (Linear) | 36.82B | 14.00B | 2.63 | 11.40B | 1.90B | 1.90B | 120.12M | 705.62M | 3.30M | 7.19B | 160.17M |
| b20.v | Icarus Verilog | 102.20B | 37.16B | 2.75 | 52.70B | 2.29B | 2.29B | 750.90M | 1.26B | 2.74M | 20.22B | 205.43M |
| b20.v | Verilator C++ | 8.79B | 3.88B | 2.26 | 4.54B | 1.16M | 1.16M | 5.77M | 5.93M | 9.83K | 701.37M | 4.09M |
| b22.v | rx-prop | 69.72B | 31.74B | 2.20 | 26.67B | 3.05B | 3.05B | 548.37M | 1.24B | 2.60M | 6.41B | 353.69M |
| b22.v | rx-sweep (Linear) | 56.91B | 25.00B | 2.28 | 18.64B | 2.90B | 2.90B | 313.40M | 1.65B | 2.53M | 10.89B | 333.21M |
| b22.v | Icarus Verilog | 174.38B | 74.05B | 2.36 | 96.65B | 4.22B | 4.22B | 2.04B | 3.08B | 5.72M | 34.63B | 410.39M |
| b22.v | Verilator C++ | 13.65B | 7.72B | 1.77 | 6.86B | 6.83M | 6.83M | 288.07M | 288.22M | 74.85K | 991.22M | 7.11M |
| b17.v | rx-prop | 57.28B | 20.08B | 2.85 | 21.34B | 2.24B | 2.24B | 332.90M | 1.15B | 3.78M | 5.23B | 26.13M |
| b17.v | rx-sweep (Linear) | 74.11B | 22.44B | 3.30 | 20.74B | 3.89B | 3.89B | 234.74M | 2.77B | 4.32M | 15.81B | 124.01M |
| b17.v | Icarus Verilog | 130.42B | 49.54B | 2.63 | 63.17B | 3.52B | 3.52B | 1.84B | 3.44B | 7.71M | 25.72B | 124.12M |
| b17.v | Verilator C++ | 23.10B | 19.27B | 1.20 | 10.71B | 32.92M | 32.92M | 1.51B | 1.51B | 16.40K | 1.70B | 31.56M |
| b18.v | rx-prop | 162.54B | 66.86B | 2.43 | 61.02B | 6.22B | 6.22B | 1.53B | 5.01B | 4.17M | 14.85B | 360.42M |
| b18.v | rx-sweep (Linear) | 180.32B | 63.01B | 2.86 | 51.79B | 9.41B | 9.41B | 1.00B | 9.13B | 4.94M | 38.71B | 453.01M |
| b18.v | Icarus Verilog | 35.35B | 17.54B | 2.02 | 16.66B | 862.67M | 862.67M | 197.10M | 321.91M | 26.54M | 7.46B | 107.65M |
| b18.v | Verilator C++ | 67.02B | 99.70B | 0.67 | 34.28B | 154.56M | 154.56M | 5.19B | 5.22B | 139.05K | 4.08B | 593.94M |
| b19.v | rx-prop | 280.75B | 113.70B | 2.47 | 104.79B | 11.09B | 11.09B | 3.28B | 11.04B | 14.10M | 25.57B | 381.12M |
| b19.v | rx-sweep (Linear) | 348.99B | 115.83B | 3.01 | 97.69B | 18.37B | 18.37B | 2.27B | 19.10B | 31.12M | 75.13B | 599.75M |
| b19.v | Icarus Verilog | 57.77B | 32.59B | 1.77 | 25.65B | 1.46B | 1.46B | 348.52M | 583.59M | 123.07M | 12.21B | 170.09M |
| b19.v | Verilator C++ | 152.79B | 226.91B | 0.67 | 75.37B | 799.58M | 799.58M | 12.06B | 12.24B | 11.57M | 8.16B | 1.55B |
