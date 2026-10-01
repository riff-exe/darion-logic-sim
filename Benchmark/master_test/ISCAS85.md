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
| c432.v | 203 | 0.63 MB (28.2 MB peak) | 0.32 MB (33.4 MB peak) | 0.07 MB (7.9 MB peak) | 0.68 MB (4.4 MB peak) |
| c499.v | 275 | 0.70 MB (28.3 MB peak) | 0.42 MB (33.4 MB peak) | 0.25 MB (8.1 MB peak) | 0.71 MB (4.4 MB peak) |
| c880.v | 469 | 0.88 MB (28.5 MB peak) | 0.63 MB (33.7 MB peak) | 0.23 MB (8.1 MB peak) | 0.68 MB (4.4 MB peak) |
| c1355.v | 619 | 1.01 MB (28.6 MB peak) | 0.84 MB (33.9 MB peak) | 0.29 MB (8.2 MB peak) | 0.68 MB (4.4 MB peak) |
| c1908.v | 938 | 1.30 MB (28.9 MB peak) | 1.18 MB (34.3 MB peak) | 0.39 MB (8.3 MB peak) | 0.72 MB (4.4 MB peak) |
| c2670.v | 1,642 | 1.92 MB (29.5 MB peak) | 2.04 MB (35.1 MB peak) | 0.82 MB (8.6 MB peak) | 0.85 MB (4.4 MB peak) |
| c3540.v | 1,741 | 2.00 MB (29.6 MB peak) | 2.25 MB (35.3 MB peak) | 0.87 MB (8.7 MB peak) | 0.72 MB (4.4 MB peak) |
| c5315.v | 2,608 | 2.84 MB (30.4 MB peak) | 3.30 MB (36.2 MB peak) | 1.23 MB (9.1 MB peak) | 0.86 MB (4.4 MB peak) |
| c6288.v | 2,480 | 2.74 MB (30.3 MB peak) | 3.20 MB (36.2 MB peak) | 1.22 MB (9.1 MB peak) | 0.86 MB (4.5 MB peak) |
| c7552.v | 3,828 | 3.94 MB (31.5 MB peak) | 4.68 MB (37.6 MB peak) | 1.82 MB (9.7 MB peak) | 0.82 MB (4.5 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| c432.v | 203 | 0.18 ms (0.023 ms opt) | 0.68 ms | 2.93 ms | 2.51 s |
| c499.v | 275 | 0.21 ms (0.025 ms opt) | 2.11 ms | 2.87 ms | 2.56 s |
| c880.v | 469 | 0.35 ms (0.045 ms opt) | 2.36 ms | 3.67 ms | 2.51 s |
| c1355.v | 619 | 0.42 ms (0.051 ms opt) | 2.53 ms | 4.72 ms | 2.52 s |
| c1908.v | 938 | 0.63 ms (0.082 ms opt) | 2.93 ms | 5.62 ms | 2.51 s |
| c2670.v | 1,642 | 1.01 ms (0.122 ms opt) | 3.67 ms | 7.97 ms | 2.54 s |
| c3540.v | 1,741 | 1.09 ms (0.143 ms opt) | 3.89 ms | 8.84 ms | 2.54 s |
| c5315.v | 2,608 | 1.63 ms (0.210 ms opt) | 5.39 ms | 11.92 ms | 2.60 s |
| c6288.v | 2,480 | 1.56 ms (0.149 ms opt) | 4.96 ms | 11.99 ms | 2.67 s |
| c7552.v | 3,828 | 2.39 ms (0.330 ms opt) | 7.98 ms | 17.28 ms | 2.87 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| c432.v | 37.86 ms | 50.61 ms | N/A | N/A | 424.11 ms | 5.11 ms |
| c499.v | 47.78 ms | 51.37 ms | N/A | N/A | 492.34 ms | 6.20 ms |
| c880.v | 76.21 ms | 101.74 ms | N/A | N/A | 807.99 ms | 8.89 ms |
| c1355.v | 133.99 ms | 111.84 ms | N/A | N/A | 1126.41 ms | 10.31 ms |
| c1908.v | 244.05 ms | 159.77 ms | N/A | N/A | 1942.97 ms | 10.28 ms |
| c2670.v | 340.11 ms | 333.65 ms | N/A | N/A | 3571.82 ms | 36.24 ms |
| c3540.v | 391.18 ms | 342.81 ms | N/A | N/A | 3309.86 ms | 19.29 ms |
| c5315.v | 740.82 ms | 653.83 ms | N/A | N/A | 6723.90 ms | 31.70 ms |
| c6288.v | 4938.91 ms | 401.82 ms | N/A | N/A | 33.62 s | 44.34 ms |
| c7552.v | 1109.60 ms | 848.29 ms | N/A | N/A | 9819.42 ms | 46.30 ms |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| c432.v | 11.20x | 8.38x | N/A | N/A | 1.00x | 82.99x |
| c499.v | 10.30x | 9.58x | N/A | N/A | 1.00x | 79.46x |
| c880.v | 10.60x | 7.94x | N/A | N/A | 1.00x | 90.89x |
| c1355.v | 8.41x | 10.07x | N/A | N/A | 1.00x | 109.21x |
| c1908.v | 7.96x | 12.16x | N/A | N/A | 1.00x | 189.10x |
| c2670.v | 10.50x | 10.71x | N/A | N/A | 1.00x | 98.55x |
| c3540.v | 8.46x | 9.66x | N/A | N/A | 1.00x | 171.61x |
| c5315.v | 9.08x | 10.28x | N/A | N/A | 1.00x | 212.09x |
| c6288.v | 6.81x | 83.67x | N/A | N/A | 1.00x | 758.27x |
| c7552.v | 8.85x | 11.58x | N/A | N/A | 1.00x | 212.08x |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `9.12x`
- **rx-sweep (Linear Compiled):** `12.32x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `153.24x`

### Cross-Engine Comparisons

- **Reactor Sweep vs Propagate Ratio:** `1.35x` (sweep faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | Instructions | Cycles | IPC | L1 Loads | L1 Misses | L2 Loads | L2 Misses | L3 Loads | DRAM Loads | Branches | Branch Misses |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| c432.v | rx-prop | 387.87M | 147.45M | 2.63 | 208.16M | 1.79M | 1.79M | 32.70K | 425.70K | 370.17K | 50.54M | 2.45M |
| c432.v | rx-sweep (Linear) | 307.18M | 196.76M | 1.56 | 182.60M | 1.47M | 1.47M | 17.95K | 544.15K | 517.14K | 67.62M | 4.27M |
| c432.v | Icarus Verilog | 5.38B | 1.53B | 3.52 | 2.44B | 22.98M | 22.98M | 2.19K | 11.10K | 2.64K | 1.06B | 12.31M |
| c432.v | Verilator C++ | 21.40M | 13.38M | 1.60 | 39.53M | 108.42K | 108.42K | 4.35K | 81.42K | 326.00 | 4.44M | 118.56K |
| c499.v | rx-prop | 594.31M | 186.49M | 3.19 | 274.64M | 2.03M | 2.03M | 35.30K | 689.14K | 669.97K | 71.74M | 1.70M |
| c499.v | rx-sweep (Linear) | 440.15M | 186.51M | 2.36 | 240.54M | 1.99M | 1.99M | 33.02K | 1.04M | 1.02M | 83.73M | 3.58M |
| c499.v | Icarus Verilog | 6.67B | 1.77B | 3.77 | 3.00B | 41.09M | 41.09M | 1.36K | 10.55K | 2.73K | 1.33B | 12.44M |
| c499.v | Verilator C++ | 40.17M | 17.04M | 2.36 | 39.49M | 96.87K | 96.87K | 2.92K | 107.93K | 509.00 | 4.46M | 17.67K |
| c880.v | rx-prop | 859.28M | 295.72M | 2.91 | 396.24M | 4.43M | 4.43M | 63.30K | 2.05M | 1.94M | 110.89M | 4.54M |
| c880.v | rx-sweep (Linear) | 684.62M | 393.91M | 1.74 | 358.96M | 4.46M | 4.46M | 52.84K | 2.22M | 2.16M | 138.30M | 8.21M |
| c880.v | Icarus Verilog | 10.08B | 2.88B | 3.50 | 4.71B | 85.44M | 85.44M | 4.49K | 14.32K | 8.91K | 1.99B | 22.53M |
| c880.v | Verilator C++ | 56.04M | 23.07M | 2.43 | 31.55M | 49.98K | 49.98K | 681.00 | 79.33K | 600.00 | 6.30M | 141.66K |
| c1355.v | rx-prop | 1.45B | 505.30M | 2.88 | 603.51M | 14.63M | 14.63M | 67.27K | 1.51M | 1.45M | 156.59M | 7.41M |
| c1355.v | rx-sweep (Linear) | 821.47M | 414.58M | 1.98 | 409.26M | 12.49M | 12.49M | 55.88K | 820.45K | 792.53K | 161.21M | 6.95M |
| c1355.v | Icarus Verilog | 14.72B | 4.06B | 3.63 | 6.77B | 127.56M | 127.56M | 21.89K | 40.32K | 7.20K | 2.95B | 29.50M |
| c1355.v | Verilator C++ | 52.32M | 26.61M | 1.97 | 33.41M | 41.02K | 41.02K | 618.00 | 77.79K | 42.81K | 7.00M | 284.77K |
| c1908.v | rx-prop | 2.56B | 891.69M | 2.87 | 1.03B | 33.93M | 33.93M | 52.44K | 635.43K | 593.20K | 253.56M | 12.54M |
| c1908.v | rx-sweep (Linear) | 1.19B | 589.98M | 2.01 | 514.49M | 35.25M | 35.25M | 77.65K | 928.36K | 868.22K | 223.56M | 8.79M |
| c1908.v | Icarus Verilog | 22.63B | 6.95B | 3.26 | 11.12B | 292.95M | 292.95M | 31.98K | 45.88K | 7.91K | 4.52B | 55.10M |
| c1908.v | Verilator C++ | 50.95M | 26.74M | 1.91 | 31.57M | 53.39K | 53.39K | 506.00 | 34.90K | 477.00 | 6.56M | 175.92K |
| c2670.v | rx-prop | 3.71B | 1.39B | 2.67 | 1.67B | 76.98M | 76.98M | 422.31K | 11.40M | 10.84M | 493.15M | 20.12M |
| c2670.v | rx-sweep (Linear) | 2.63B | 1.36B | 1.93 | 1.31B | 81.35M | 81.35M | 426.90K | 11.29M | 10.79M | 553.41M | 24.97M |
| c2670.v | Icarus Verilog | 45.03B | 12.82B | 3.51 | 21.48B | 484.36M | 484.36M | 478.27K | 820.68K | 49.84K | 8.86B | 88.21M |
| c2670.v | Verilator C++ | 215.21M | 127.64M | 1.69 | 111.67M | 181.23K | 181.23K | 2.96K | 155.85K | 58.15K | 12.29M | 1.68M |
| c3540.v | rx-prop | 3.97B | 1.44B | 2.76 | 1.61B | 68.88M | 68.88M | 108.08K | 1.90M | 1.80M | 405.46M | 22.22M |
| c3540.v | rx-sweep (Linear) | 2.08B | 1.27B | 1.64 | 946.46M | 72.08M | 72.08M | 90.41K | 2.28M | 2.23M | 391.91M | 26.05M |
| c3540.v | Icarus Verilog | 35.02B | 11.91B | 2.94 | 18.00B | 597.33M | 597.33M | 279.38K | 366.73K | 8.78K | 7.01B | 108.82M |
| c3540.v | Verilator C++ | 115.31M | 73.11M | 1.58 | 79.92M | 105.79K | 105.79K | 3.40K | 47.08K | 3.07K | 10.64M | 276.14K |
| c5315.v | rx-prop | 7.48B | 2.78B | 2.69 | 3.08B | 185.01M | 185.01M | 281.74K | 8.53M | 8.07M | 799.65M | 39.90M |
| c5315.v | rx-sweep (Linear) | 4.02B | 2.47B | 1.63 | 1.99B | 134.69M | 134.69M | 332.54K | 8.31M | 7.88M | 769.49M | 53.11M |
| c5315.v | Icarus Verilog | 73.44B | 24.07B | 3.05 | 36.35B | 1.23B | 1.23B | 13.17M | 19.26M | 45.54K | 14.66B | 197.52M |
| c5315.v | Verilator C++ | 230.05M | 111.12M | 2.07 | 139.16M | 129.99K | 129.99K | 2.99K | 103.34K | 76.73K | 13.55M | 857.78K |
| c6288.v | rx-prop | 43.70B | 17.70B | 2.47 | 17.03B | 1.16B | 1.16B | 195.08K | 784.27K | 460.59K | 4.10B | 278.75M |
| c6288.v | rx-sweep (Linear) | 3.63B | 1.45B | 2.50 | 1.56B | 110.15M | 110.15M | 56.99K | 828.81K | 808.49K | 639.78M | 21.25M |
| c6288.v | Icarus Verilog | 434.53B | 121.04B | 3.59 | 193.40B | 8.38B | 8.38B | 33.14M | 52.61M | 44.58K | 86.33B | 696.64M |
| c6288.v | Verilator C++ | 234.94M | 146.88M | 1.60 | 128.30M | 42.01K | 42.01K | 2.00K | 97.91K | 495.00 | 23.44M | 2.21M |
| c7552.v | rx-prop | 10.65B | 4.15B | 2.56 | 4.36B | 351.48M | 351.48M | 597.90K | 10.89M | 10.12M | 1.13B | 58.31M |
| c7552.v | rx-sweep (Linear) | 5.60B | 3.22B | 1.74 | 2.57B | 188.12M | 188.12M | 564.59K | 10.99M | 10.42M | 1.06B | 64.78M |
| c7552.v | Icarus Verilog | 102.41B | 35.16B | 2.91 | 52.59B | 1.91B | 1.91B | 180.60M | 253.19M | 61.75K | 20.41B | 279.98M |
| c7552.v | Verilator C++ | 310.16M | 164.06M | 1.89 | 165.73M | 215.44K | 215.44K | 3.09K | 131.49K | 9.43K | 20.22M | 1.64M |
