# Master Test Unified Benchmark Report: tests/ISCAS89

**Execution Parameters:**
- **Target Suite / Path:** `tests/ISCAS89`
- **Circuits Benchmarked:** 15
- **Simulation Vectors (Phase 3):** 50,000 (Warmup: 10)
- **Verification Vectors (Phase 2):** 100
- **Hardware Profiler:** Linux `perf` kernel PMU counters

---

## 1. Zero-Testbench Memory Footprint (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| s27.v | 19 | 0.55 MB (28.1 MB peak) | 0.16 MB (33.2 MB peak) | 0.07 MB (7.9 MB peak) | 0.70 MB (4.4 MB peak) |
| s420.v | 254 | 0.95 MB (28.6 MB peak) | 0.61 MB (33.6 MB peak) | 0.23 MB (8.1 MB peak) | 0.71 MB (4.4 MB peak) |
| s382.v | 189 | 0.95 MB (28.4 MB peak) | 0.65 MB (33.6 MB peak) | 0.25 MB (8.1 MB peak) | 0.69 MB (4.4 MB peak) |
| s641.v | 458 | 1.13 MB (28.8 MB peak) | 0.97 MB (34.1 MB peak) | 0.30 MB (8.1 MB peak) | 0.67 MB (4.4 MB peak) |
| s713.v | 471 | 1.19 MB (28.7 MB peak) | 0.98 MB (34.0 MB peak) | 0.24 MB (8.2 MB peak) | 0.71 MB (4.4 MB peak) |
| s1238.v | 555 | 1.29 MB (28.8 MB peak) | 1.05 MB (34.1 MB peak) | 0.42 MB (8.3 MB peak) | 0.71 MB (4.4 MB peak) |
| s1423.v | 754 | 2.16 MB (29.7 MB peak) | 2.30 MB (35.3 MB peak) | 0.74 MB (8.5 MB peak) | 0.75 MB (4.4 MB peak) |
| s1488.v | 687 | 1.28 MB (28.9 MB peak) | 1.06 MB (34.1 MB peak) | 0.45 MB (8.3 MB peak) | 0.73 MB (4.4 MB peak) |
| s5378.v | 3,043 | 7.48 MB (35.1 MB peak) | 6.68 MB (39.8 MB peak) | 2.24 MB (10.1 MB peak) | 0.84 MB (4.4 MB peak) |
| s9234.v | 5,884 | 9.89 MB (37.5 MB peak) | 10.36 MB (43.3 MB peak) | 4.47 MB (12.2 MB peak) | 0.68 MB (4.4 MB peak) |
| s13207.v | 8,804 | 19.70 MB (47.4 MB peak) | 18.62 MB (51.7 MB peak) | 7.99 MB (15.9 MB peak) | 0.78 MB (4.5 MB peak) |
| s15850.v | 10,534 | 18.78 MB (46.4 MB peak) | 18.95 MB (52.0 MB peak) | 8.55 MB (16.4 MB peak) | 0.83 MB (4.5 MB peak) |
| s35932.v | 18,149 | 44.80 MB (72.4 MB peak) | 44.92 MB (78.0 MB peak) | 18.86 MB (26.8 MB peak) | 0.78 MB (4.5 MB peak) |
| s38584.v | 21,022 | 41.43 MB (69.0 MB peak) | 43.76 MB (76.7 MB peak) | 20.16 MB (28.0 MB peak) | 0.90 MB (4.6 MB peak) |
| s38417.v | 23,950 | 43.47 MB (71.0 MB peak) | 51.84 MB (84.9 MB peak) | 22.38 MB (30.3 MB peak) | 0.75 MB (4.4 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| s27.v | 19 | 0.10 ms (0.013 ms opt) | 0.54 ms | 2.91 ms | 2.50 s |
| s420.v | 254 | 0.34 ms (0.047 ms opt) | 2.39 ms | 3.16 ms | 2.54 s |
| s382.v | 189 | 0.35 ms (0.047 ms opt) | 2.44 ms | 2.94 ms | 2.51 s |
| s641.v | 458 | 0.46 ms (0.060 ms opt) | 2.72 ms | 4.40 ms | 2.55 s |
| s713.v | 471 | 0.47 ms (0.065 ms opt) | 2.56 ms | 4.05 ms | 2.53 s |
| s1238.v | 555 | 0.57 ms (0.093 ms opt) | 2.62 ms | 4.95 ms | 2.53 s |
| s1423.v | 754 | 1.14 ms (0.133 ms opt) | 3.85 ms | 5.46 ms | 2.55 s |
| s1488.v | 687 | 0.57 ms (0.088 ms opt) | 2.66 ms | 5.10 ms | 2.52 s |
| s5378.v | 3,043 | 3.22 ms (0.360 ms opt) | 10.45 ms | 16.86 ms | 2.61 s |
| s9234.v | 5,884 | 5.71 ms (0.732 ms opt) | 14.68 ms | 31.62 ms | 2.64 s |
| s13207.v | 8,804 | 11.14 ms (1.301 ms opt) | 26.15 ms | 57.05 ms | 2.84 s |
| s15850.v | 10,534 | 11.73 ms (1.362 ms opt) | 26.09 ms | 69.62 ms | 2.96 s |
| s35932.v | 18,149 | 26.24 ms (3.042 ms opt) | 80.36 ms | 106.20 ms | 3.85 s |
| s38584.v | 21,022 | 28.56 ms (6.053 ms opt) | 85.04 ms | 153.79 ms | 5.64 s |
| s38417.v | 23,950 | 30.60 ms (5.107 ms opt) | 88.84 ms | 161.04 ms | 4.60 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| s27.v | 11.26 ms | 9.53 ms | N/A | N/A | 98.72 ms | 3.07 ms |
| s420.v | 44.27 ms | 50.32 ms | N/A | N/A | 336.65 ms | 7.75 ms |
| s382.v | 49.47 ms | 46.68 ms | N/A | N/A | 179.73 ms | 3.63 ms |
| s641.v | 81.17 ms | 90.42 ms | N/A | N/A | 647.83 ms | 11.53 ms |
| s713.v | 87.08 ms | 91.93 ms | N/A | N/A | 684.41 ms | 9.88 ms |
| s1238.v | 128.13 ms | 205.51 ms | N/A | N/A | 833.03 ms | 18.87 ms |
| s1423.v | 252.60 ms | 256.34 ms | N/A | N/A | 826.32 ms | 16.78 ms |
| s1488.v | 55.14 ms | 70.08 ms | N/A | N/A | 530.56 ms | 14.24 ms |
| s5378.v | 696.29 ms | 803.97 ms | N/A | N/A | 2326.21 ms | 28.29 ms |
| s9234.v | 743.20 ms | 913.47 ms | N/A | N/A | 2941.36 ms | 21.66 ms |
| s13207.v | 1815.12 ms | 2391.91 ms | N/A | N/A | 5266.72 ms | 56.96 ms |
| s15850.v | 1691.09 ms | 2069.47 ms | N/A | N/A | 6793.10 ms | 70.83 ms |
| s35932.v | 6754.95 ms | 6068.54 ms | N/A | N/A | 20.68 s | 193.47 ms |
| s38584.v | 6998.96 ms | 8401.31 ms | N/A | N/A | 23.35 s | 172.86 ms |
| s38417.v | 5163.76 ms | 5508.66 ms | N/A | N/A | 14.49 s | 164.86 ms |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| s27.v | 8.77x | 10.36x | N/A | N/A | 1.00x | 32.20x |
| s420.v | 7.60x | 6.69x | N/A | N/A | 1.00x | 43.46x |
| s382.v | 3.63x | 3.85x | N/A | N/A | 1.00x | 49.53x |
| s641.v | 7.98x | 7.17x | N/A | N/A | 1.00x | 56.18x |
| s713.v | 7.86x | 7.44x | N/A | N/A | 1.00x | 69.27x |
| s1238.v | 6.50x | 4.05x | N/A | N/A | 1.00x | 44.14x |
| s1423.v | 3.27x | 3.22x | N/A | N/A | 1.00x | 49.25x |
| s1488.v | 9.62x | 7.57x | N/A | N/A | 1.00x | 37.26x |
| s5378.v | 3.34x | 2.89x | N/A | N/A | 1.00x | 82.21x |
| s9234.v | 3.96x | 3.22x | N/A | N/A | 1.00x | 135.82x |
| s13207.v | 2.90x | 2.20x | N/A | N/A | 1.00x | 92.46x |
| s15850.v | 4.02x | 3.28x | N/A | N/A | 1.00x | 95.91x |
| s35932.v | 3.06x | 3.41x | N/A | N/A | 1.00x | 106.87x |
| s38584.v | 3.34x | 2.78x | N/A | N/A | 1.00x | 135.09x |
| s38417.v | 2.81x | 2.63x | N/A | N/A | 1.00x | 87.91x |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `4.74x`
- **rx-sweep (Linear Compiled):** `4.22x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `67.49x`

### Cross-Engine Comparisons

- **Reactor Sweep vs Propagate Ratio:** `0.89x` (propagate faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | Instructions | Cycles | IPC | L1 Loads | L1 Misses | L2 Loads | L2 Misses | L3 Loads | DRAM Loads | Branches | Branch Misses |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| s27.v | rx-prop | 138.57M | 42.19M | 3.28 | 67.31M | 32.54K | 32.54K | 1.74K | 19.76K | 8.88K | 17.49M | 123.52K |
| s27.v | rx-sweep (Linear) | 133.77M | 30.77M | 4.35 | 54.21M | 98.32K | 98.32K | 1.72K | 21.15K | 6.09K | 22.71M | 108.37K |
| s27.v | Icarus Verilog | 1.22B | 352.30M | 3.48 | 558.70M | 28.44K | 28.44K | 1.11K | 18.18K | 283.00 | 233.44M | 3.38M |
| s27.v | Verilator C++ | 1.91M | 3.17M | 0.60 | 6.17M | 13.93K | 13.93K | 703.00 | 703.00 | 0.00 | 2.70M | 8.78K |
| s420.v | rx-prop | 663.80M | 171.03M | 3.88 | 298.12M | 1.87M | 1.87M | 38.04K | 662.00K | 597.29K | 81.42M | 671.48K |
| s420.v | rx-sweep (Linear) | 730.29M | 197.13M | 3.70 | 281.46M | 1.88M | 1.88M | 35.42K | 906.22K | 881.60K | 140.30M | 1.64M |
| s420.v | Icarus Verilog | 4.67B | 1.21B | 3.87 | 2.16B | 15.58M | 15.58M | 4.71K | 27.13K | 12.88K | 906.38M | 7.16M |
| s420.v | Verilator C++ | 17.94M | 17.19M | 1.04 | 60.11M | 109.07K | 109.07K | 2.64K | 100.56K | 30.48K | 8.80M | 18.32K |
| s382.v | rx-prop | 683.70M | 167.50M | 4.08 | 286.36M | 201.57K | 201.57K | 2.91K | 23.07K | 7.15K | 68.77M | 313.77K |
| s382.v | rx-sweep (Linear) | 723.07M | 166.03M | 4.36 | 273.27M | 1.05M | 1.05M | 1.32K | 22.63K | 17.84K | 141.05M | 808.97K |
| s382.v | Icarus Verilog | 2.53B | 642.54M | 3.94 | 1.21B | 10.86M | 10.86M | 5.20K | 21.35K | 292.00 | 484.58M | 3.61M |
| s382.v | Verilator C++ | 3.13K | 4.34M | 0.00 | 22.13M | 13.69K | 13.69K | 1.17K | 19.21K | 335.00 | 5.86M | 17.07K |
| s641.v | rx-prop | 1.10B | 322.28M | 3.42 | 485.38M | 7.11M | 7.11M | 70.62K | 2.10M | 2.06M | 143.63M | 2.51M |
| s641.v | rx-sweep (Linear) | 1.19B | 358.02M | 3.34 | 460.68M | 8.39M | 8.39M | 64.82K | 2.35M | 2.30M | 249.56M | 3.21M |
| s641.v | Icarus Verilog | 9.12B | 2.30B | 3.97 | 4.17B | 53.20M | 53.20M | 3.10K | 23.01K | 15.72K | 1.77B | 12.82M |
| s641.v | Verilator C++ | 73.62M | 36.08M | 2.04 | 52.53M | 141.74K | 141.74K | 4.05K | 61.95K | 10.13K | 12.93M | 114.52K |
| s713.v | rx-prop | 1.20B | 352.20M | 3.40 | 500.46M | 6.87M | 6.87M | 65.75K | 2.26M | 2.22M | 155.83M | 2.90M |
| s713.v | rx-sweep (Linear) | 1.20B | 362.15M | 3.31 | 470.23M | 9.36M | 9.36M | 58.44K | 2.43M | 2.39M | 251.68M | 3.32M |
| s713.v | Icarus Verilog | 9.37B | 2.43B | 3.85 | 4.33B | 55.48M | 55.48M | 33.28K | 84.85K | 13.18K | 1.82B | 14.02M |
| s713.v | Verilator C++ | 40.53M | 22.40M | 1.81 | 55.09M | 164.53K | 164.53K | 3.07K | 53.50K | 14.00 | 10.93M | 105.75K |
| s1238.v | rx-prop | 1.39B | 472.66M | 2.95 | 564.69M | 18.81M | 18.81M | 63.64K | 669.37K | 595.76K | 143.50M | 5.47M |
| s1238.v | rx-sweep (Linear) | 1.36B | 736.82M | 1.84 | 600.26M | 25.76M | 25.76M | 34.09K | 127.82K | 100.24K | 269.22M | 14.67M |
| s1238.v | Icarus Verilog | 9.15B | 2.98B | 3.07 | 4.56B | 127.40M | 127.40M | 25.20K | 57.08K | 9.34K | 1.82B | 26.19M |
| s1238.v | Verilator C++ | 116.49M | 65.59M | 1.78 | 73.80M | 17.13K | 17.13K | 190.00 | 63.66K | 33.00 | 13.34M | 304.53K |
| s1423.v | rx-prop | 3.02B | 907.08M | 3.33 | 1.18B | 87.26M | 87.26M | 43.76K | 445.59K | 363.29K | 298.86M | 3.86M |
| s1423.v | rx-sweep (Linear) | 3.13B | 926.99M | 3.38 | 1.08B | 117.09M | 117.09M | 23.99K | 741.43K | 713.76K | 562.95M | 7.13M |
| s1423.v | Icarus Verilog | 11.24B | 2.96B | 3.80 | 5.43B | 134.21M | 134.21M | 71.60K | 170.70K | 15.63K | 2.19B | 15.70M |
| s1423.v | Verilator C++ | 100.15M | 58.92M | 1.70 | 69.61M | 21.35K | 21.35K | 2.24K | 99.81K | 1.67K | 12.28M | 150.81K |
| s1488.v | rx-prop | 739.80M | 201.76M | 3.67 | 300.86M | 7.08M | 7.08M | 14.43K | 53.92K | 39.34K | 80.59M | 952.09K |
| s1488.v | rx-sweep (Linear) | 862.02M | 260.01M | 3.32 | 316.30M | 8.53M | 8.53M | 17.10K | 73.40K | 48.20K | 163.79M | 2.18M |
| s1488.v | Icarus Verilog | 6.29B | 1.91B | 3.30 | 3.01B | 74.86M | 74.86M | 13.22K | 30.88K | 10.79K | 1.25B | 14.98M |
| s1488.v | Verilator C++ | 82.32M | 39.75M | 2.07 | 70.37M | 21.15K | 21.15K | 958.00 | 28.93K | 324.00 | 7.83M | 85.95K |
| s5378.v | rx-prop | 8.00B | 2.55B | 3.14 | 3.09B | 266.49M | 266.49M | 279.11K | 2.86M | 2.44M | 792.47M | 17.46M |
| s5378.v | rx-sweep (Linear) | 9.03B | 2.91B | 3.11 | 3.04B | 369.71M | 369.71M | 218.55K | 3.14M | 2.87M | 1.70B | 30.77M |
| s5378.v | Icarus Verilog | 29.14B | 8.37B | 3.48 | 14.55B | 426.22M | 426.22M | 5.53M | 9.88M | 24.00K | 5.64B | 47.49M |
| s5378.v | Verilator C++ | 199.78M | 101.40M | 1.97 | 128.44M | 144.65K | 144.65K | 2.34K | 36.13K | 4.56K | 14.92M | 172.37K |
| s9234.v | rx-prop | 8.96B | 2.70B | 3.32 | 3.40B | 310.47M | 310.47M | 387.72K | 3.54M | 2.88M | 875.74M | 12.56M |
| s9234.v | rx-sweep (Linear) | 10.93B | 3.34B | 3.28 | 3.45B | 488.40M | 488.40M | 268.53K | 2.85M | 2.49M | 2.18B | 27.81M |
| s9234.v | Icarus Verilog | 34.55B | 10.55B | 3.28 | 17.88B | 552.16M | 552.16M | 64.20M | 98.81M | 57.49K | 6.70B | 52.50M |
| s9234.v | Verilator C++ | 128.50M | 73.86M | 1.74 | 113.26M | 140.02K | 140.02K | 1.36K | 117.94K | 2.64K | 11.07M | 382.27K |
| s13207.v | rx-prop | 22.24B | 6.59B | 3.37 | 8.45B | 801.16M | 801.16M | 10.98M | 27.19M | 4.45M | 2.15B | 25.11M |
| s13207.v | rx-sweep (Linear) | 26.45B | 8.66B | 3.05 | 8.89B | 1.16B | 1.16B | 29.54M | 94.54M | 5.84M | 5.15B | 82.69M |
| s13207.v | Icarus Verilog | 59.35B | 18.88B | 3.14 | 31.44B | 965.67M | 965.67M | 298.89M | 559.66M | 123.10K | 11.31B | 67.78M |
| s13207.v | Verilator C++ | 310.33M | 201.89M | 1.54 | 253.31M | 212.32K | 212.32K | 2.09K | 115.34K | 3.87K | 16.46M | 580.21K |
| s15850.v | rx-prop | 20.84B | 6.16B | 3.38 | 7.90B | 722.66M | 722.66M | 16.88M | 43.53M | 7.66M | 2.03B | 22.76M |
| s15850.v | rx-sweep (Linear) | 24.48B | 7.50B | 3.27 | 7.88B | 1.13B | 1.13B | 22.96M | 69.71M | 6.64M | 4.86B | 58.89M |
| s15850.v | Icarus Verilog | 74.98B | 24.32B | 3.08 | 39.41B | 1.28B | 1.28B | 434.77M | 753.40M | 241.23K | 14.52B | 91.48M |
| s15850.v | Verilator C++ | 397.01M | 249.57M | 1.59 | 301.69M | 264.20K | 264.20K | 300.00 | 81.84K | 709.00 | 20.81M | 1.23M |
| s35932.v | rx-prop | 76.35B | 24.19B | 3.16 | 28.31B | 3.33B | 3.33B | 438.72M | 2.11B | 3.18M | 7.16B | 9.87M |
| s35932.v | rx-sweep (Linear) | 82.15B | 21.78B | 3.77 | 26.68B | 3.75B | 3.75B | 270.32M | 2.37B | 2.68M | 14.24B | 34.12M |
| s35932.v | Icarus Verilog | 289.76B | 73.40B | 3.95 | 136.39B | 7.39B | 7.39B | 2.11B | 5.68B | 1.07M | 56.86B | 59.19M |
| s35932.v | Verilator C++ | 586.17M | 684.48M | 0.86 | 647.80M | 146.80K | 146.80K | 6.49K | 99.66K | 26.93K | 9.28M | 51.42K |
| s38584.v | rx-prop | 65.29B | 24.88B | 2.62 | 24.83B | 2.69B | 2.69B | 508.61M | 1.56B | 3.35M | 6.11B | 114.71M |
| s38584.v | rx-sweep (Linear) | 73.35B | 29.93B | 2.45 | 26.68B | 3.32B | 3.32B | 359.59M | 2.02B | 3.39M | 13.28B | 362.45M |
| s38584.v | Icarus Verilog | 204.37B | 83.28B | 2.45 | 114.91B | 4.79B | 4.79B | 2.44B | 3.68B | 814.20K | 39.98B | 393.61M |
| s38584.v | Verilator C++ | 852.35M | 606.69M | 1.40 | 724.20M | 158.04K | 158.04K | 3.32K | 50.72K | 4.14K | 15.54M | 749.91K |
| s38417.v | rx-prop | 56.46B | 18.40B | 3.07 | 21.12B | 2.15B | 2.15B | 321.35M | 1.13B | 2.13M | 5.26B | 37.95M |
| s38417.v | rx-sweep (Linear) | 66.92B | 19.75B | 3.39 | 21.09B | 3.07B | 3.07B | 191.85M | 1.85B | 2.18M | 12.97B | 108.69M |
| s38417.v | Icarus Verilog | 168.38B | 51.91B | 3.24 | 87.03B | 3.34B | 3.34B | 1.22B | 2.46B | 833.08K | 32.47B | 124.67M |
| s38417.v | Verilator C++ | 825.53M | 592.42M | 1.39 | 591.15M | 147.92K | 147.92K | 1.92K | 74.68K | 35.68K | 11.56M | 129.26K |
