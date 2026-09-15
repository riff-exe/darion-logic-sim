# Master Test Unified Benchmark Report: tests/ISCAS89

**Execution Parameters:**
- **Target Suite / Path:** `tests/ISCAS89`
- **Circuits Benchmarked:** 15
- **Simulation Vectors (Phase 3):** 10,000 (Warmup: 10)
- **Verification Vectors (Phase 2):** 100
- **Hardware Profiler:** Linux `perf` kernel PMU counters

---

## 1. Zero-Testbench Memory Footprint (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| s27.v | 19 | 0.59 MB (33.8 MB peak) | 0.18 MB (33.2 MB peak) | 0.02 MB (7.9 MB peak) | 0.68 MB (4.4 MB peak) |
| s420.v | 254 | 0.88 MB (32.1 MB peak) | 0.64 MB (33.7 MB peak) | 0.16 MB (8.0 MB peak) | 0.60 MB (4.3 MB peak) |
| s382.v | 189 | 0.90 MB (32.2 MB peak) | 0.63 MB (33.6 MB peak) | 0.18 MB (8.0 MB peak) | 0.74 MB (4.4 MB peak) |
| s641.v | 458 | 1.12 MB (32.5 MB peak) | 0.92 MB (34.0 MB peak) | 0.26 MB (8.1 MB peak) | 0.73 MB (4.4 MB peak) |
| s713.v | 471 | 1.11 MB (32.5 MB peak) | 0.94 MB (34.0 MB peak) | 0.29 MB (8.2 MB peak) | 0.71 MB (4.4 MB peak) |
| s1238.v | 555 | 1.23 MB (32.6 MB peak) | 1.07 MB (34.0 MB peak) | 0.41 MB (8.3 MB peak) | 0.73 MB (4.4 MB peak) |
| s1423.v | 754 | 2.16 MB (33.5 MB peak) | 2.23 MB (35.3 MB peak) | 0.57 MB (8.5 MB peak) | 0.71 MB (4.4 MB peak) |
| s1488.v | 687 | 1.27 MB (32.6 MB peak) | 1.03 MB (34.1 MB peak) | 0.41 MB (8.2 MB peak) | 0.73 MB (4.4 MB peak) |
| s5378.v | 3,043 | 7.43 MB (38.7 MB peak) | 6.62 MB (39.6 MB peak) | 2.18 MB (10.1 MB peak) | 0.72 MB (4.4 MB peak) |
| s9234.v | 5,884 | 8.43 MB (39.8 MB peak) | 10.38 MB (43.5 MB peak) | 4.32 MB (12.1 MB peak) | 0.74 MB (4.4 MB peak) |
| s13207.v | 8,804 | 19.69 MB (51.1 MB peak) | 18.65 MB (51.8 MB peak) | 8.06 MB (15.9 MB peak) | 0.82 MB (4.5 MB peak) |
| s15850.v | 10,534 | 18.35 MB (49.8 MB peak) | 18.97 MB (52.0 MB peak) | 8.49 MB (16.3 MB peak) | 0.79 MB (4.5 MB peak) |
| s35932.v | 18,149 | 47.18 MB (78.5 MB peak) | 44.83 MB (77.9 MB peak) | 18.82 MB (26.7 MB peak) | 0.91 MB (4.6 MB peak) |
| s38584.v | 21,022 | 42.98 MB (74.3 MB peak) | 43.76 MB (76.8 MB peak) | 20.06 MB (28.0 MB peak) | 0.91 MB (4.6 MB peak) |
| s38417.v | 23,950 | 48.68 MB (80.1 MB peak) | 51.84 MB (84.9 MB peak) | 22.54 MB (30.4 MB peak) | 0.97 MB (4.6 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| s27.v | 19 | 0.45 ms (0.010 ms opt) | 0.79 ms | 3.23 ms | 3.59 s |
| s420.v | 254 | 0.78 ms (0.061 ms opt) | 11.16 ms | 4.42 ms | 3.61 s |
| s382.v | 189 | 0.81 ms (0.060 ms opt) | 11.80 ms | 4.11 ms | 3.55 s |
| s641.v | 458 | 0.96 ms (0.078 ms opt) | 11.53 ms | 5.16 ms | 3.62 s |
| s713.v | 471 | 1.01 ms (0.085 ms opt) | 11.62 ms | 5.43 ms | 3.61 s |
| s1238.v | 555 | 1.20 ms (0.134 ms opt) | 12.35 ms | 6.38 ms | 3.61 s |
| s1423.v | 754 | 1.86 ms (0.177 ms opt) | 13.51 ms | 7.68 ms | 3.61 s |
| s1488.v | 687 | 1.11 ms (0.127 ms opt) | 11.79 ms | 7.33 ms | 3.62 s |
| s5378.v | 3,043 | 5.19 ms (0.512 ms opt) | 22.82 ms | 24.55 ms | 3.72 s |
| s9234.v | 5,884 | 8.93 ms (0.951 ms opt) | 29.67 ms | 42.75 ms | 3.79 s |
| s13207.v | 8,804 | 16.92 ms (1.978 ms opt) | 45.49 ms | 73.08 ms | 3.94 s |
| s15850.v | 10,534 | 17.66 ms (1.996 ms opt) | 47.25 ms | 103.76 ms | 4.11 s |
| s35932.v | 18,149 | 39.76 ms (5.389 ms opt) | 115.72 ms | 151.97 ms | 5.08 s |
| s38584.v | 21,022 | 42.09 ms (8.084 ms opt) | 119.12 ms | 215.62 ms | 7.59 s |
| s38417.v | 23,950 | 44.21 ms (7.164 ms opt) | 125.10 ms | 220.95 ms | 5.98 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| s27.v | 4.24 ms | 3.86 ms | 3.30 ms | 3750.62 ms | 27.50 ms | 1.11 ms |
| s420.v | 16.00 ms | 20.52 ms | 15.68 ms | 17.16 s | 98.29 ms | 2.73 ms |
| s382.v | 15.89 ms | 20.99 ms | 18.28 ms | 19.92 s | 54.24 ms | 1.26 ms |
| s641.v | 28.90 ms | 34.53 ms | 31.87 ms | 28.09 s | 184.56 ms | 3.64 ms |
| s713.v | 30.40 ms | 36.88 ms | 33.72 ms | 29.80 s | 190.61 ms | 3.09 ms |
| s1238.v | 49.40 ms | 56.43 ms | 56.96 ms | 44.84 s | 242.59 ms | 5.74 ms |
| s1423.v | 87.89 ms | 99.33 ms | 92.57 ms | 84.22 s | 241.45 ms | 4.98 ms |
| s1488.v | 20.57 ms | 28.98 ms | 23.00 ms | 22.90 s | 153.92 ms | 5.03 ms |
| s5378.v | 259.53 ms | 281.76 ms | 266.58 ms | 1298.72 s | 687.04 ms | 8.23 ms |
| s9234.v | 277.51 ms | 337.48 ms | 299.82 ms | 1512.92 s | 856.23 ms | 6.56 ms |
| s13207.v | 663.46 ms | 845.43 ms | 862.81 ms | 3625.26 s | 1512.05 ms | 17.62 ms |
| s15850.v | 622.95 ms | 800.56 ms | 825.23 ms | 3530.62 s | 1958.14 ms | 20.32 ms |
| s35932.v | 2418.52 ms | 2459.73 ms | 3292.48 ms | 14925.58 s | 6071.29 ms | 56.12 ms |
| s38584.v | 2764.47 ms | 3042.80 ms | 3786.84 ms | 12489.86 s | 6865.86 ms | 50.97 ms |
| s38417.v | 1867.40 ms | 2138.32 ms | 2684.56 ms | 21757.73 s | 4242.46 ms | 48.32 ms |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| s27.v | 6.48x | 7.12x | 8.33x | 0.01x | 1.00x | 24.86x |
| s420.v | 6.15x | 4.79x | 6.27x | 0.01x | 1.00x | 35.99x |
| s382.v | 3.41x | 2.58x | 2.97x | 0.00x | 1.00x | 42.88x |
| s641.v | 6.38x | 5.34x | 5.79x | 0.01x | 1.00x | 50.64x |
| s713.v | 6.27x | 5.17x | 5.65x | 0.01x | 1.00x | 61.60x |
| s1238.v | 4.91x | 4.30x | 4.26x | 0.01x | 1.00x | 42.26x |
| s1423.v | 2.75x | 2.43x | 2.61x | 0.00x | 1.00x | 48.48x |
| s1488.v | 7.48x | 5.31x | 6.69x | 0.01x | 1.00x | 30.60x |
| s5378.v | 2.65x | 2.44x | 2.58x | 0.00x | 1.00x | 83.45x |
| s9234.v | 3.09x | 2.54x | 2.86x | 0.00x | 1.00x | 130.54x |
| s13207.v | 2.28x | 1.79x | 1.75x | 0.00x | 1.00x | 85.82x |
| s15850.v | 3.14x | 2.45x | 2.37x | 0.00x | 1.00x | 96.38x |
| s35932.v | 2.51x | 2.47x | 1.84x | 0.00x | 1.00x | 108.19x |
| s38584.v | 2.48x | 2.26x | 1.81x | 0.00x | 1.00x | 134.71x |
| s38417.v | 2.27x | 1.98x | 1.58x | 0.00x | 1.00x | 87.79x |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `3.78x`
- **rx-sweep (Linear Compiled):** `3.21x`
- **rx-oop (OOP Graph):** `3.30x`
- **Pure Python Engine:** `0.00x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `62.49x`

### Cross-Engine Comparisons

- **Cython Reactor (`rx-prop`) vs Pure Python:** `2318.69x` faster
- **Cython Reactor (`rx-sweep`) vs Pure Python:** `1972.92x` faster
- **Reactor Sweep vs Propagate Ratio:** `0.85x` (propagate faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | IPC | Cycles | Instructions | L1 Loads | L1 Hit% | L2 Hit% | LLC Misses | Brn Miss% |
|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| s27.v | rx-prop | 8.17 | 3.65M | 29.80M | 2.12M | 99.79% | 71.71% | 1.28K | 0.64% |
| s27.v | rx-sweep (Linear) | 903.16 | 18.21K | 16.45M | 2.51M | 99.97% | 0.00% | 3.22K | 0.74% |
| s27.v | rx-oop (OOP Engine) | 285.75 | 20.16K | 5.76M | 4.56M | 99.82% | 50.48% | 3.38K | 0.57% |
| s27.v | Pure Python Engine | 6.24 | 15.68M | 97.78M | 32.54M | 99.86% | 91.74% | 3.70K | 0.27% |
| s27.v | Icarus Verilog | 3.82 | 74.16M | 283.58M | 118.49M | 99.99% | 81.92% | 1.73K | 1.27% |
| s420.v | rx-prop | 4.42 | 35.96M | 158.94M | 50.15M | 99.83% | 94.19% | 5.61K | 1.25% |
| s420.v | rx-sweep (Linear) | 4.35 | 49.07M | 213.35M | 59.64M | 99.71% | 97.70% | 6.87K | 1.03% |
| s420.v | rx-oop (OOP Engine) | 4.35 | 37.40M | 162.50M | 51.29M | 99.34% | 97.84% | 6.55K | 1.37% |
| s420.v | Pure Python Engine | 4.93 | 103.87M | 512.21M | 221.44M | 99.52% | 99.09% | 7.98K | 0.20% |
| s420.v | Icarus Verilog | 4.07 | 255.99M | 1.04B | 467.76M | 99.25% | 99.66% | 11.29K | 0.70% |
| s382.v | rx-prop | 4.99 | 35.27M | 175.97M | 50.97M | 99.90% | 91.12% | 215 | 0.42% |
| s382.v | rx-sweep (Linear) | 4.75 | 46.54M | 220.91M | 65.51M | 99.70% | 96.80% | 3.97K | 0.51% |
| s382.v | rx-oop (OOP Engine) | 3.86 | 43.76M | 169.04M | 55.01M | 98.77% | 99.03% | 4.07K | 0.42% |
| s382.v | Pure Python Engine | 4.97 | 115.20M | 572.87M | 246.20M | 99.47% | 99.01% | 16.04K | 0.18% |
| s382.v | Icarus Verilog | 3.94 | 147.25M | 579.51M | 268.87M | 99.08% | 99.67% | 5.31K | 0.83% |
| s641.v | rx-prop | 3.46 | 84.69M | 292.92M | 98.24M | 98.47% | 98.74% | 18.95K | 2.22% |
| s641.v | rx-sweep (Linear) | 3.68 | 92.24M | 339.29M | 101.23M | 97.01% | 99.71% | 10.15K | 1.45% |
| s641.v | rx-oop (OOP Engine) | 2.88 | 88.18M | 254.13M | 95.73M | 96.26% | 99.45% | 21.71K | 2.65% |
| s641.v | Pure Python Engine | 4.74 | 176.42M | 836.92M | 378.39M | 99.51% | 98.64% | 26.84K | 0.23% |
| s641.v | Icarus Verilog | 4.03 | 508.80M | 2.05B | 935.68M | 98.72% | 99.96% | 7.36K | 0.65% |
| s713.v | rx-prop | 3.48 | 89.51M | 311.09M | 107.44M | 98.34% | 98.43% | 33.93K | 1.84% |
| s713.v | rx-sweep (Linear) | 3.78 | 97.21M | 367.75M | 107.56M | 96.80% | 99.49% | 16.23K | 1.50% |
| s713.v | rx-oop (OOP Engine) | 2.96 | 92.12M | 272.32M | 96.33M | 96.20% | 99.43% | 23.90K | 2.81% |
| s713.v | Pure Python Engine | 4.80 | 186.04M | 893.16M | 394.00M | 99.53% | 98.76% | 23.16K | 0.24% |
| s713.v | Icarus Verilog | 4.04 | 522.27M | 2.11B | 957.38M | 98.69% | 99.95% | 5.53K | 0.67% |
| s1238.v | rx-prop | 2.66 | 132.22M | 352.14M | 127.10M | 96.71% | 99.90% | 3.88K | 4.63% |
| s1238.v | rx-sweep (Linear) | 2.85 | 153.43M | 436.93M | 145.72M | 94.78% | 99.96% | 3.57K | 3.38% |
| s1238.v | rx-oop (OOP Engine) | 2.44 | 145.50M | 355.32M | 130.54M | 94.37% | 99.65% | 29.40K | 5.23% |
| s1238.v | Pure Python Engine | 4.51 | 286.96M | 1.29B | 591.92M | 99.21% | 98.60% | 72.60K | 0.27% |
| s1238.v | Icarus Verilog | 3.09 | 662.38M | 2.05B | 995.97M | 97.20% | 99.98% | 5.10K | 1.38% |
| s1423.v | rx-prop | 3.42 | 231.16M | 790.23M | 248.80M | 92.42% | 99.91% | 22.19K | 1.28% |
| s1423.v | rx-sweep (Linear) | 3.89 | 260.10M | 1.01B | 302.67M | 89.11% | 99.94% | 19.07K | 1.00% |
| s1423.v | rx-oop (OOP Engine) | 3.21 | 252.36M | 810.77M | 266.03M | 88.70% | 99.96% | 8.12K | 1.50% |
| s1423.v | Pure Python Engine | 4.69 | 551.46M | 2.58B | 1.15B | 99.42% | 95.71% | 289.81K | 0.17% |
| s1423.v | Icarus Verilog | 3.85 | 658.83M | 2.54B | 1.21B | 97.52% | 99.85% | 43.78K | 0.71% |
| s1488.v | rx-prop | 3.79 | 47.47M | 179.80M | 55.63M | 97.24% | 99.76% | 4.67K | 1.89% |
| s1488.v | rx-sweep (Linear) | 3.74 | 74.57M | 279.13M | 81.90M | 97.19% | 99.90% | 2.68K | 1.24% |
| s1488.v | rx-oop (OOP Engine) | 3.05 | 64.24M | 196.12M | 72.16M | 95.80% | 99.33% | 21.20K | 2.22% |
| s1488.v | Pure Python Engine | 4.75 | 142.87M | 678.43M | 295.31M | 99.57% | 98.96% | 13.49K | 0.23% |
| s1488.v | Icarus Verilog | 3.41 | 417.27M | 1.42B | 668.03M | 97.49% | 99.94% | 9.92K | 1.14% |
| s5378.v | rx-prop | 2.98 | 721.22M | 2.15B | 713.11M | 89.75% | 99.89% | 75.18K | 2.15% |
| s5378.v | rx-sweep (Linear) | 3.65 | 764.85M | 2.80B | 859.92M | 88.02% | 99.86% | 141.73K | 1.44% |
| s5378.v | rx-oop (OOP Engine) | 2.83 | 739.86M | 2.10B | 741.20M | 87.39% | 99.71% | 267.49K | 2.37% |
| s5378.v | Pure Python Engine | 4.33 | 306.42M | 1.33B | 599.50M | 99.44% | 54.93% | 1.52M | 0.32% |
| s5378.v | Icarus Verilog | 3.48 | 1.88B | 6.54B | 3.22B | 97.04% | 97.08% | 2.80M | 0.84% |
| s9234.v | rx-prop | 3.06 | 759.63M | 2.33B | 773.33M | 89.04% | 99.66% | 275.17K | 1.78% |
| s9234.v | rx-sweep (Linear) | 3.61 | 924.58M | 3.34B | 1.04B | 86.40% | 98.86% | 1.59M | 1.06% |
| s9234.v | rx-oop (OOP Engine) | 2.86 | 824.39M | 2.36B | 826.79M | 85.74% | 99.50% | 623.30K | 2.00% |
| s9234.v | Pure Python Engine | 4.25 | 374.04M | 1.59B | 716.97M | 99.46% | 44.75% | 2.14M | 0.16% |
| s9234.v | Icarus Verilog | 3.33 | 2.33B | 7.75B | 3.97B | 96.90% | 86.74% | 16.38M | 0.73% |
| s13207.v | rx-prop | 3.19 | 1.83B | 5.84B | 1.94B | 86.95% | 98.50% | 3.83M | 1.49% |
| s13207.v | rx-sweep (Linear) | 3.55 | 2.32B | 8.23B | 2.57B | 87.99% | 94.34% | 17.46M | 1.31% |
| s13207.v | rx-oop (OOP Engine) | 2.47 | 2.37B | 5.84B | 2.07B | 85.01% | 85.88% | 43.85M | 1.65% |
| s13207.v | Pure Python Engine | 4.20 | 889.82M | 3.74B | 1.68B | 99.42% | 20.98% | 7.78M | 0.21% |
| s13207.v | Icarus Verilog | 3.24 | 4.12B | 13.37B | 6.99B | 96.90% | 73.69% | 57.10M | 0.58% |
| s15850.v | rx-prop | 3.17 | 1.72B | 5.45B | 1.82B | 87.82% | 98.04% | 4.33M | 1.45% |
| s15850.v | rx-sweep (Linear) | 3.51 | 2.18B | 7.65B | 2.35B | 87.54% | 90.19% | 28.86M | 1.04% |
| s15850.v | rx-oop (OOP Engine) | 2.49 | 2.26B | 5.61B | 1.99B | 86.76% | 84.09% | 41.79M | 1.68% |
| s15850.v | Pure Python Engine | 4.25 | 858.10M | 3.64B | 1.64B | 99.43% | 24.56% | 7.10M | 0.17% |
| s15850.v | Icarus Verilog | 3.15 | 5.35B | 16.86B | 8.72B | 96.72% | 66.10% | 96.88M | 0.59% |
| s35932.v | rx-prop | 3.11 | 6.63B | 20.61B | 6.50B | 84.79% | 82.45% | 173.66M | 0.19% |
| s35932.v | rx-sweep (Linear) | 3.94 | 6.75B | 26.58B | 7.96B | 87.35% | 89.45% | 106.60M | 0.20% |
| s35932.v | rx-oop (OOP Engine) | 2.33 | 9.00B | 20.95B | 7.01B | 83.39% | 64.87% | 408.95M | 0.27% |
| s35932.v | Pure Python Engine | 3.96 | 3.70B | 14.68B | 6.59B | 99.39% | 23.75% | 30.98M | 0.14% |
| s35932.v | Icarus Verilog | 3.93 | 16.61B | 65.21B | 30.40B | 94.49% | 71.49% | 477.73M | 0.09% |
| s38584.v | rx-prop | 2.30 | 7.56B | 17.40B | 6.04B | 87.20% | 77.52% | 173.96M | 2.59% |
| s38584.v | rx-sweep (Linear) | 2.75 | 8.35B | 22.97B | 7.70B | 89.07% | 85.31% | 123.52M | 2.36% |
| s38584.v | rx-oop (OOP Engine) | 1.70 | 10.39B | 17.68B | 6.63B | 85.75% | 52.23% | 451.14M | 2.82% |
| s38584.v | Pure Python Engine | 3.67 | 3.10B | 11.39B | 5.16B | 99.44% | 15.66% | 24.61M | 0.17% |
| s38584.v | Icarus Verilog | 2.46 | 18.78B | 46.18B | 25.77B | 95.77% | 49.81% | 547.11M | 0.94% |
| s38417.v | rx-prop | 2.90 | 5.13B | 14.86B | 4.81B | 85.42% | 83.57% | 115.20M | 0.82% |
| s38417.v | rx-sweep (Linear) | 3.58 | 5.85B | 20.94B | 6.41B | 87.58% | 89.35% | 84.94M | 0.72% |
| s38417.v | rx-oop (OOP Engine) | 2.11 | 7.31B | 15.42B | 5.30B | 84.42% | 58.33% | 344.47M | 0.93% |
| s38417.v | Pure Python Engine | 3.98 | 1.20B | 4.79B | 2.15B | 99.42% | 16.98% | 10.45M | 0.13% |
| s38417.v | Icarus Verilog | 3.24 | 11.62B | 37.68B | 19.47B | 96.13% | 63.75% | 273.40M | 0.36% |
