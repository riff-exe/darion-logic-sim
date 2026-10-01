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
| sin.v | 8,947 | 9.42 MB (37.0 MB peak) | N/A | 5.31 MB (13.1 MB peak) | 0.68 MB (4.4 MB peak) |
| voter.v | 27,720 | 30.17 MB (57.7 MB peak) | N/A | 17.89 MB (25.8 MB peak) | 1.21 MB (4.8 MB peak) |
| square.v | 35,687 | 36.63 MB (64.2 MB peak) | N/A | 22.55 MB (30.5 MB peak) | 1.27 MB (5.0 MB peak) |
| sqrt.v | 41,234 | 39.71 MB (67.2 MB peak) | N/A | 26.91 MB (34.8 MB peak) | 1.06 MB (4.8 MB peak) |
| multiplier.v | 50,760 | 48.72 MB (76.3 MB peak) | N/A | 32.89 MB (40.8 MB peak) | 1.34 MB (5.0 MB peak) |
| log2.v | 54,531 | 52.37 MB (79.8 MB peak) | N/A | 35.49 MB (43.3 MB peak) | 1.01 MB (4.7 MB peak) |
| mem_ctrl.v | 84,974 | 78.97 MB (106.5 MB peak) | N/A | 55.50 MB (63.3 MB peak) | 1.56 MB (5.2 MB peak) |
| div.v | 101,859 | 97.19 MB (124.8 MB peak) | N/A | 67.31 MB (75.2 MB peak) | 1.53 MB (5.2 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| sin.v | 8,947 | 5.87 ms (0.751 ms opt) | N/A | 40.39 ms | 2.95 s |
| voter.v | 27,720 | 18.07 ms (1.875 ms opt) | N/A | 133.81 ms | 4.53 s |
| square.v | 35,687 | 30.68 ms (7.250 ms opt) | N/A | 204.21 ms | 5.69 s |
| sqrt.v | 41,234 | 29.53 ms (3.598 ms opt) | N/A | 230.03 ms | 5.94 s |
| multiplier.v | 50,760 | 36.83 ms (7.479 ms opt) | N/A | 281.83 ms | 6.78 s |
| log2.v | 54,531 | 47.90 ms (16.465 ms opt) | N/A | 318.74 ms | 7.79 s |
| mem_ctrl.v | 84,974 | 64.76 ms (18.167 ms opt) | N/A | 878.76 ms | 13.12 s |
| div.v | 101,859 | 108.49 ms (16.444 ms opt) | N/A | 635.04 ms | 21.32 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| sin.v | 197.04 ms | 14.98 ms | N/A | N/A | 1593.26 ms | 1.15 ms |
| voter.v | 173.78 ms | 42.03 ms | N/A | N/A | 1476.02 ms | 2.86 ms |
| square.v | 155.01 ms | 61.85 ms | N/A | N/A | 1081.41 ms | 5.08 ms |
| sqrt.v | 20.35 s | 71.43 ms | N/A | N/A | 132.45 s | 3.37 ms |
| multiplier.v | 1244.75 ms | 82.46 ms | N/A | N/A | 9358.73 ms | 3.36 ms |
| log2.v | 5836.39 ms | 90.00 ms | N/A | N/A | 43.45 s | 5.23 ms |
| mem_ctrl.v | 200.48 ms | 161.15 ms | N/A | N/A | 1951.46 ms | 26.44 ms |
| div.v | 379.13 ms | 119.80 ms | N/A | N/A | 2854.64 ms | 46.37 ms |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| sin.v | 8.09x | 106.38x | N/A | N/A | 1.00x | 1379.89x |
| voter.v | 8.49x | 35.12x | N/A | N/A | 1.00x | 516.58x |
| square.v | 6.98x | 17.49x | N/A | N/A | 1.00x | 212.88x |
| sqrt.v | 6.51x | 1854.30x | N/A | N/A | 1.00x | 39243.77x |
| multiplier.v | 7.52x | 113.49x | N/A | N/A | 1.00x | 2787.11x |
| log2.v | 7.44x | 482.71x | N/A | N/A | 1.00x | 8311.23x |
| mem_ctrl.v | 9.73x | 12.11x | N/A | N/A | 1.00x | 73.81x |
| div.v | 7.53x | 23.83x | N/A | N/A | 1.00x | 61.57x |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `7.73x`
- **rx-sweep (Linear Compiled):** `81.33x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `943.29x`

### Cross-Engine Comparisons

- **Reactor Sweep vs Propagate Ratio:** `10.52x` (sweep faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | Instructions | Cycles | IPC | L1 Loads | L1 Misses | L2 Loads | L2 Misses | L3 Loads | DRAM Loads | Branches | Branch Misses |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| sin.v | rx-prop | 1.74B | 689.58M | 2.52 | 687.18M | 69.31M | 69.31M | 79.06K | 122.08K | 5.53K | 166.71M | 9.28M |
| sin.v | rx-sweep (Linear) | 58.33M | 38.43M | 1.52 | 36.44M | 3.01M | 3.01M | 888.00 | 13.22K | 986.00 | 14.24M | 1.04M |
| sin.v | Icarus Verilog | 14.24B | 5.70B | 2.50 | 8.08B | 348.08M | 348.08M | 47.76M | 58.70M | 30.45K | 2.86B | 46.04M |
| sin.v | Verilator C++ | 944.14K | 1.06M | 0.89 | 1.54M | 1.76K | 1.76K | 0.00 | 0.00 | 0.00 | 43.78K | 812.00 |
| voter.v | rx-prop | 1.40B | 616.41M | 2.27 | 563.88M | 61.83M | 61.83M | 6.50M | 10.43M | 32.98K | 136.36M | 8.47M |
| voter.v | rx-sweep (Linear) | 272.28M | 142.55M | 1.91 | 133.73M | 11.50M | 11.50M | 1.18M | 6.20M | 11.74K | 55.59M | 2.72M |
| voter.v | Icarus Verilog | 12.15B | 5.24B | 2.32 | 7.12B | 248.55M | 248.55M | 93.31M | 128.03M | 734.73K | 2.42B | 38.92M |
| voter.v | Verilator C++ | 1.76M | 6.17M | 0.28 | 7.25M | 1.22K | 1.22K | 928.00 | 1.09K | 0.00 | 800.01K | 46.89K |
| square.v | rx-prop | 1.10B | 542.81M | 2.03 | 427.64M | 53.02M | 53.02M | 7.55M | 12.50M | 6.93K | 105.69M | 5.61M |
| square.v | rx-sweep (Linear) | 351.32M | 211.86M | 1.66 | 159.38M | 14.05M | 14.05M | 2.01M | 10.30M | 2.55K | 65.59M | 4.18M |
| square.v | Icarus Verilog | 8.27B | 3.84B | 2.16 | 5.01B | 206.63M | 206.63M | 87.35M | 111.49M | 45.16K | 1.67B | 26.59M |
| square.v | Verilator C++ | 6.76M | 8.04M | 0.84 | 19.70M | 826.00 | 826.00 | 1.80K | 1.80K | 33.00 | 2.83M | 107.33K |
| sqrt.v | rx-prop | 119.03B | 72.41B | 1.64 | 45.86B | 6.26B | 6.26B | 2.61B | 4.06B | 916.33K | 11.28B | 527.30M |
| sqrt.v | rx-sweep (Linear) | 480.64M | 248.97M | 1.93 | 220.87M | 16.91M | 16.91M | 2.98M | 13.45M | 10.60K | 87.15M | 4.01M |
| sqrt.v | Icarus Verilog | 855.96B | 472.46B | 1.81 | 546.63B | 23.43B | 23.43B | 18.32B | 25.07B | 29.35M | 171.82B | 2.58B |
| sqrt.v | Verilator C++ | 2.79M | 8.60M | 0.32 | 13.02M | 4.35K | 4.35K | 1.56K | 1.56K | 607.00 | 209.80K | 16.13K |
| multiplier.v | rx-prop | 8.69B | 4.45B | 1.95 | 3.39B | 413.31M | 413.31M | 65.24M | 94.87M | 120.19K | 834.26M | 45.80M |
| multiplier.v | rx-sweep (Linear) | 553.93M | 294.80M | 1.88 | 234.52M | 21.30M | 21.30M | 4.06M | 18.73M | 26.30K | 103.55M | 4.81M |
| multiplier.v | Icarus Verilog | 61.72B | 33.38B | 1.85 | 39.83B | 1.50B | 1.50B | 1.07B | 1.46B | 8.12M | 12.36B | 198.13M |
| multiplier.v | Verilator C++ | 1.43M | 5.82M | 0.25 | 14.19M | 812.00 | 812.00 | 1.06K | 1.06K | 409.00 | 3.10M | 16.61K |
| log2.v | rx-prop | 37.11B | 20.76B | 1.79 | 14.30B | 1.70B | 1.70B | 521.34M | 881.92M | 241.62K | 3.53B | 172.27M |
| log2.v | rx-sweep (Linear) | 540.80M | 306.97M | 1.76 | 236.95M | 20.08M | 20.08M | 3.91M | 18.22M | 3.75K | 99.57M | 5.67M |
| log2.v | Icarus Verilog | 285.02B | 154.98B | 1.84 | 182.48B | 7.09B | 7.09B | 5.52B | 7.23B | 8.59M | 57.05B | 855.23M |
| log2.v | Verilator C++ | 2.80M | 10.79M | 0.26 | 16.68M | 291.00 | 291.00 | 2.45K | 2.45K | 28.00 | 106.21K | 6.12K |
| mem_ctrl.v | rx-prop | 1.20B | 703.36M | 1.71 | 467.55M | 66.15M | 66.15M | 30.78M | 54.89M | 40.63K | 115.83M | 3.62M |
| mem_ctrl.v | rx-sweep (Linear) | 853.48M | 565.95M | 1.51 | 412.72M | 36.89M | 36.89M | 8.48M | 36.93M | 29.25K | 163.94M | 11.26M |
| mem_ctrl.v | Icarus Verilog | 13.07B | 6.97B | 1.88 | 7.60B | 305.68M | 305.68M | 243.57M | 319.70M | 5.38M | 2.60B | 25.74M |
| mem_ctrl.v | Verilator C++ | 94.68M | 84.74M | 1.12 | 40.89M | 175.90K | 175.90K | 6.72M | 6.80M | 385.00 | 6.54M | 123.80K |
| div.v | rx-prop | 2.25B | 1.34B | 1.68 | 856.26M | 103.01M | 103.01M | 48.51M | 72.33M | 11.80K | 217.52M | 6.93M |
| div.v | rx-sweep (Linear) | 1.09B | 422.76M | 2.58 | 408.40M | 37.32M | 37.32M | 6.86M | 37.52M | 5.05K | 200.80M | 5.00M |
| div.v | Icarus Verilog | 18.97B | 10.20B | 1.86 | 10.24B | 481.91M | 481.91M | 289.45M | 380.04M | 16.77M | 3.82B | 29.89M |
| div.v | Verilator C++ | 63.35M | 163.03M | 0.39 | 39.77M | 64.52K | 64.52K | 1.08M | 1.10M | 37.00 | 10.80M | 16.63K |
