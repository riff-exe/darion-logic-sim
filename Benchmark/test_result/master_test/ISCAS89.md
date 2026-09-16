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
| s27.v | 19 | 0.42 MB (31.9 MB peak) | 0.18 MB (33.1 MB peak) | 0.13 MB (7.9 MB peak) | 0.70 MB (4.4 MB peak) |
| s420.v | 254 | 0.84 MB (32.2 MB peak) | 0.61 MB (33.7 MB peak) | 0.26 MB (8.1 MB peak) | 0.71 MB (4.4 MB peak) |
| s382.v | 189 | 2.86 MB (34.2 MB peak) | 0.65 MB (33.7 MB peak) | 0.18 MB (8.1 MB peak) | 0.70 MB (4.4 MB peak) |
| s641.v | 458 | 1.09 MB (32.5 MB peak) | 0.91 MB (34.0 MB peak) | 0.28 MB (8.1 MB peak) | 0.73 MB (4.4 MB peak) |
| s713.v | 471 | 1.09 MB (32.5 MB peak) | 0.95 MB (34.0 MB peak) | 0.36 MB (8.1 MB peak) | 0.71 MB (4.4 MB peak) |
| s1238.v | 555 | 3.14 MB (34.5 MB peak) | 1.08 MB (34.1 MB peak) | 0.44 MB (8.3 MB peak) | 0.72 MB (4.4 MB peak) |
| s1423.v | 754 | 2.05 MB (33.4 MB peak) | 2.27 MB (35.4 MB peak) | 0.71 MB (8.6 MB peak) | 0.70 MB (4.3 MB peak) |
| s1488.v | 687 | 1.21 MB (34.6 MB peak) | 1.03 MB (34.1 MB peak) | 0.28 MB (8.2 MB peak) | 0.68 MB (4.4 MB peak) |
| s5378.v | 3,043 | 5.59 MB (36.9 MB peak) | 6.68 MB (39.7 MB peak) | 2.21 MB (10.1 MB peak) | 0.74 MB (4.4 MB peak) |
| s9234.v | 5,884 | 8.38 MB (39.7 MB peak) | 11.78 MB (44.8 MB peak) | 4.23 MB (12.1 MB peak) | 0.75 MB (4.4 MB peak) |
| s13207.v | 8,804 | 20.74 MB (52.0 MB peak) | 18.62 MB (51.7 MB peak) | 8.05 MB (15.9 MB peak) | 0.77 MB (4.5 MB peak) |
| s15850.v | 10,534 | 19.05 MB (50.4 MB peak) | 18.97 MB (52.1 MB peak) | 8.44 MB (16.3 MB peak) | 0.80 MB (4.5 MB peak) |
| s35932.v | 18,149 | 42.44 MB (73.8 MB peak) | 44.86 MB (77.8 MB peak) | 18.96 MB (26.8 MB peak) | 0.80 MB (4.5 MB peak) |
| s38584.v | 21,022 | 42.11 MB (73.4 MB peak) | 43.72 MB (76.8 MB peak) | 20.08 MB (27.9 MB peak) | 0.93 MB (4.6 MB peak) |
| s38417.v | 23,950 | 45.38 MB (76.8 MB peak) | 51.85 MB (84.8 MB peak) | 22.48 MB (30.3 MB peak) | 0.88 MB (4.6 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| s27.v | 19 | 0.32 ms (0.008 ms opt) | 0.58 ms | 2.23 ms | 2.62 s |
| s420.v | 254 | 0.63 ms (0.043 ms opt) | 10.14 ms | 3.07 ms | 2.59 s |
| s382.v | 189 | 0.60 ms (0.042 ms opt) | 2.49 ms | 2.94 ms | 2.59 s |
| s641.v | 458 | 0.74 ms (0.058 ms opt) | 10.41 ms | 3.72 ms | 2.58 s |
| s713.v | 471 | 0.73 ms (0.060 ms opt) | 10.23 ms | 3.89 ms | 2.59 s |
| s1238.v | 555 | 0.88 ms (0.090 ms opt) | 10.61 ms | 4.77 ms | 2.62 s |
| s1423.v | 754 | 1.39 ms (0.134 ms opt) | 11.78 ms | 5.35 ms | 2.61 s |
| s1488.v | 687 | 0.80 ms (0.085 ms opt) | 10.37 ms | 5.50 ms | 2.65 s |
| s5378.v | 3,043 | 3.62 ms (0.354 ms opt) | 18.09 ms | 16.10 ms | 2.65 s |
| s9234.v | 5,884 | 6.49 ms (0.682 ms opt) | 23.28 ms | 31.79 ms | 2.73 s |
| s13207.v | 8,804 | 13.49 ms (1.729 ms opt) | 34.91 ms | 59.99 ms | 2.85 s |
| s15850.v | 10,534 | 12.50 ms (1.603 ms opt) | 35.35 ms | 70.54 ms | 3.03 s |
| s35932.v | 18,149 | 28.99 ms (4.077 ms opt) | 89.17 ms | 113.73 ms | 3.87 s |
| s38584.v | 21,022 | 31.01 ms (5.348 ms opt) | 95.12 ms | 185.49 ms | 5.74 s |
| s38417.v | 23,950 | 34.49 ms (6.408 ms opt) | 96.53 ms | 169.49 ms | 4.76 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| s27.v | 2.45 ms | 2.49 ms | 3.13 ms | 2479.22 ms | 20.23 ms | 0.71 ms |
| s420.v | 9.78 ms | 13.45 ms | 15.63 ms | 12.04 s | 68.64 ms | 1.84 ms |
| s382.v | 10.21 ms | 13.93 ms | 17.46 ms | 13.82 s | 37.33 ms | 0.81 ms |
| s641.v | 19.94 ms | 23.00 ms | 30.84 ms | 19.51 s | 128.80 ms | 2.52 ms |
| s713.v | 20.43 ms | 23.98 ms | 32.77 ms | 20.47 s | 136.40 ms | 2.00 ms |
| s1238.v | 33.82 ms | 38.91 ms | 58.10 ms | 29.99 s | 166.52 ms | 4.33 ms |
| s1423.v | 59.84 ms | 66.96 ms | 87.22 ms | 57.03 s | 164.59 ms | 3.44 ms |
| s1488.v | 13.98 ms | 19.95 ms | 25.86 ms | 16.07 s | 107.38 ms | 3.14 ms |
| s5378.v | 177.04 ms | 190.67 ms | 242.03 ms | 865.36 s | 472.31 ms | 5.51 ms |
| s9234.v | 187.54 ms | 226.30 ms | 272.77 ms | 1016.85 s | 586.18 ms | 4.68 ms |
| s13207.v | 457.32 ms | 572.99 ms | 714.18 ms | 2461.89 s | 1062.36 ms | 11.84 ms |
| s15850.v | 422.83 ms | 526.03 ms | 706.38 ms | 2413.33 s | 1364.32 ms | 14.47 ms |
| s35932.v | 1645.58 ms | 1684.65 ms | 2258.43 ms | 11034.92 s | 4113.05 ms | 38.26 ms |
| s38584.v | 1865.15 ms | 2060.80 ms | 2922.62 ms | 9197.92 s | 4706.42 ms | 34.63 ms |
| s38417.v | 1274.60 ms | 1445.88 ms | 1976.69 ms | 16359.45 s | 2926.74 ms | 33.02 ms |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| s27.v | 8.26x | 8.13x | 6.47x | 0.01x | 1.00x | 28.67x |
| s420.v | 7.02x | 5.10x | 4.39x | 0.01x | 1.00x | 37.35x |
| s382.v | 3.66x | 2.68x | 2.14x | 0.00x | 1.00x | 46.36x |
| s641.v | 6.46x | 5.60x | 4.18x | 0.01x | 1.00x | 51.19x |
| s713.v | 6.68x | 5.69x | 4.16x | 0.01x | 1.00x | 68.03x |
| s1238.v | 4.92x | 4.28x | 2.87x | 0.01x | 1.00x | 38.44x |
| s1423.v | 2.75x | 2.46x | 1.89x | 0.00x | 1.00x | 47.91x |
| s1488.v | 7.68x | 5.38x | 4.15x | 0.01x | 1.00x | 34.23x |
| s5378.v | 2.67x | 2.48x | 1.95x | 0.00x | 1.00x | 85.67x |
| s9234.v | 3.13x | 2.59x | 2.15x | 0.00x | 1.00x | 125.38x |
| s13207.v | 2.32x | 1.85x | 1.49x | 0.00x | 1.00x | 89.76x |
| s15850.v | 3.23x | 2.59x | 1.93x | 0.00x | 1.00x | 94.30x |
| s35932.v | 2.50x | 2.44x | 1.82x | 0.00x | 1.00x | 107.51x |
| s38584.v | 2.52x | 2.28x | 1.61x | 0.00x | 1.00x | 135.91x |
| s38417.v | 2.30x | 2.02x | 1.48x | 0.00x | 1.00x | 88.64x |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `3.94x`
- **rx-sweep (Linear Compiled):** `3.33x`
- **rx-oop (OOP Graph):** `2.55x`
- **Pure Python Engine:** `0.00x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `64.15x`

### Cross-Engine Comparisons

- **Cython Reactor (`rx-prop`) vs Pure Python:** `2415.12x` faster
- **Cython Reactor (`rx-sweep`) vs Pure Python:** `2042.90x` faster
- **Reactor Sweep vs Propagate Ratio:** `0.85x` (propagate faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | IPC | Cycles | Instructions | L1 Loads | L1 Hit% | L2 Hit% | LLC Misses | Brn Miss% |
|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| s27.v | rx-prop | 0.00 | 0 | 0 | 902.41K | 99.98% | 0.00% | 4.31K | 0.78% |
| s27.v | rx-sweep (Linear) | 0.00 | 0 | 0 | 3.14K | 95.34% | 0.00% | 1.19K | 9.53% |
| s27.v | rx-oop (OOP Engine) | 12.44 | 1.14M | 14.18M | 2.72M | 99.71% | 71.87% | 2.21K | 0.81% |
| s27.v | Pure Python Engine | 7.48 | 8.08M | 60.43M | 11.98M | 99.98% | 93.38% | 168 | 0.20% |
| s27.v | Icarus Verilog | 3.67 | 79.45M | 291.68M | 117.87M | 99.99% | 84.66% | 2.61K | 1.30% |
| s420.v | rx-prop | 4.82 | 30.53M | 147.19M | 53.24M | 99.75% | 97.59% | 6.08K | 1.13% |
| s420.v | rx-sweep (Linear) | 4.82 | 47.29M | 227.85M | 61.74M | 99.68% | 98.00% | 3.95K | 1.01% |
| s420.v | rx-oop (OOP Engine) | 2.71 | 61.03M | 165.13M | 87.07M | 99.44% | 98.86% | 5.62K | 2.17% |
| s420.v | Pure Python Engine | 4.84 | 110.73M | 536.25M | 228.12M | 99.51% | 99.14% | 10.39K | 0.20% |
| s420.v | Icarus Verilog | 3.90 | 274.19M | 1.07B | 478.03M | 99.29% | 99.56% | 9.93K | 0.81% |
| s382.v | rx-prop | 5.22 | 29.72M | 154.98M | 47.41M | 99.94% | 96.37% | 1.06K | 0.41% |
| s382.v | rx-sweep (Linear) | 5.22 | 38.53M | 201.23M | 54.24M | 99.86% | 99.65% | 5.05K | 0.49% |
| s382.v | rx-oop (OOP Engine) | 2.87 | 61.15M | 175.33M | 89.93M | 99.14% | 99.77% | 1.68K | 1.26% |
| s382.v | Pure Python Engine | 5.11 | 119.08M | 608.72M | 252.30M | 99.48% | 99.51% | 6.61K | 0.17% |
| s382.v | Icarus Verilog | 4.00 | 148.61M | 594.08M | 261.45M | 99.08% | 99.63% | 6.07K | 0.75% |
| s641.v | rx-prop | 4.10 | 63.73M | 261.34M | 76.91M | 98.90% | 98.81% | 6.78K | 2.67% |
| s641.v | rx-sweep (Linear) | 3.63 | 96.61M | 350.91M | 114.80M | 97.27% | 99.41% | 18.60K | 1.20% |
| s641.v | rx-oop (OOP Engine) | 2.23 | 111.72M | 249.27M | 154.41M | 97.75% | 99.31% | 26.36K | 3.65% |
| s641.v | Pure Python Engine | 4.82 | 184.59M | 888.78M | 386.99M | 99.51% | 98.40% | 35.28K | 0.23% |
| s641.v | Icarus Verilog | 3.96 | 516.01M | 2.04B | 937.01M | 98.74% | 99.92% | 8.79K | 0.70% |
| s713.v | rx-prop | 3.50 | 74.10M | 259.04M | 91.94M | 98.86% | 99.07% | 14.91K | 2.81% |
| s713.v | rx-sweep (Linear) | 3.68 | 93.17M | 342.90M | 108.31M | 97.42% | 99.65% | 8.98K | 1.49% |
| s713.v | rx-oop (OOP Engine) | 2.21 | 125.11M | 276.56M | 157.82M | 97.83% | 99.54% | 16.19K | 4.14% |
| s713.v | Pure Python Engine | 4.75 | 191.36M | 908.93M | 409.96M | 99.45% | 98.49% | 36.52K | 0.20% |
| s713.v | Icarus Verilog | 3.87 | 544.29M | 2.11B | 967.69M | 98.71% | 99.85% | 19.24K | 0.78% |
| s1238.v | rx-prop | 2.87 | 119.47M | 342.73M | 115.27M | 96.44% | 99.89% | 4.64K | 4.76% |
| s1238.v | rx-sweep (Linear) | 3.25 | 128.32M | 417.27M | 125.57M | 94.43% | 99.93% | 5.62K | 3.32% |
| s1238.v | rx-oop (OOP Engine) | 1.49 | 225.15M | 335.84M | 244.42M | 96.81% | 99.80% | 18.47K | 7.42% |
| s1238.v | Pure Python Engine | 4.76 | 278.59M | 1.33B | 565.65M | 99.55% | 98.03% | 53.07K | 0.25% |
| s1238.v | Icarus Verilog | 3.11 | 664.79M | 2.07B | 1.01B | 97.25% | 99.94% | 13.88K | 1.43% |
| s1423.v | rx-prop | 3.38 | 230.28M | 778.06M | 245.13M | 92.06% | 99.96% | 9.41K | 1.23% |
| s1423.v | rx-sweep (Linear) | 3.88 | 256.54M | 995.06M | 299.45M | 88.73% | 99.97% | 9.92K | 0.98% |
| s1423.v | rx-oop (OOP Engine) | 2.37 | 321.18M | 760.35M | 438.27M | 92.50% | 99.93% | 22.35K | 2.48% |
| s1423.v | Pure Python Engine | 4.79 | 541.17M | 2.59B | 1.14B | 99.41% | 96.88% | 211.90K | 0.17% |
| s1423.v | Icarus Verilog | 3.88 | 651.38M | 2.53B | 1.21B | 97.55% | 99.99% | 6.17K | 0.68% |
| s1488.v | rx-prop | 3.92 | 45.08M | 176.64M | 50.82M | 97.49% | 99.87% | 1.69K | 1.98% |
| s1488.v | rx-sweep (Linear) | 3.72 | 63.85M | 237.49M | 84.08M | 97.03% | 99.74% | 6.29K | 1.22% |
| s1488.v | rx-oop (OOP Engine) | 2.05 | 88.49M | 181.31M | 116.28M | 97.43% | 99.74% | 7.83K | 5.09% |
| s1488.v | Pure Python Engine | 4.61 | 139.81M | 644.62M | 283.38M | 99.43% | 98.42% | 31.53K | 0.35% |
| s1488.v | Icarus Verilog | 3.32 | 430.39M | 1.43B | 672.59M | 97.56% | 99.97% | 4.78K | 1.19% |
| s5378.v | rx-prop | 2.99 | 710.70M | 2.12B | 710.67M | 89.79% | 99.95% | 31.22K | 2.19% |
| s5378.v | rx-sweep (Linear) | 3.61 | 773.05M | 2.79B | 863.75M | 88.07% | 99.95% | 52.18K | 1.43% |
| s5378.v | rx-oop (OOP Engine) | 2.12 | 962.55M | 2.04B | 1.23B | 91.89% | 99.75% | 241.53K | 3.15% |
| s5378.v | Pure Python Engine | 4.40 | 300.04M | 1.32B | 582.25M | 99.42% | 55.04% | 1.54M | 0.26% |
| s5378.v | Icarus Verilog | 3.45 | 1.90B | 6.54B | 3.26B | 97.06% | 97.72% | 2.21M | 0.84% |
| s9234.v | rx-prop | 3.14 | 744.84M | 2.34B | 768.78M | 89.04% | 99.88% | 96.09K | 1.80% |
| s9234.v | rx-sweep (Linear) | 3.70 | 905.76M | 3.35B | 1.02B | 86.38% | 99.82% | 258.15K | 1.06% |
| s9234.v | rx-oop (OOP Engine) | 2.12 | 1.10B | 2.34B | 1.44B | 91.40% | 99.22% | 958.36K | 2.81% |
| s9234.v | Pure Python Engine | 4.42 | 354.26M | 1.57B | 691.83M | 99.44% | 43.61% | 2.19M | 0.17% |
| s9234.v | Icarus Verilog | 3.34 | 2.31B | 7.73B | 3.92B | 96.87% | 86.95% | 16.02M | 0.78% |
| s13207.v | rx-prop | 3.17 | 1.85B | 5.87B | 1.93B | 86.81% | 98.67% | 3.40M | 1.50% |
| s13207.v | rx-sweep (Linear) | 3.57 | 2.32B | 8.26B | 2.58B | 88.00% | 94.64% | 16.63M | 1.29% |
| s13207.v | rx-oop (OOP Engine) | 2.01 | 2.87B | 5.77B | 3.56B | 90.79% | 87.27% | 41.70M | 2.23% |
| s13207.v | Pure Python Engine | 4.20 | 892.80M | 3.75B | 1.69B | 99.40% | 21.16% | 7.90M | 0.17% |
| s13207.v | Icarus Verilog | 3.19 | 4.18B | 13.33B | 7.00B | 96.91% | 68.89% | 67.27M | 0.61% |
| s15850.v | rx-prop | 3.19 | 1.71B | 5.45B | 1.80B | 87.56% | 97.87% | 4.79M | 1.46% |
| s15850.v | rx-sweep (Linear) | 3.60 | 2.11B | 7.60B | 2.36B | 87.45% | 94.25% | 16.92M | 1.05% |
| s15850.v | rx-oop (OOP Engine) | 1.97 | 2.84B | 5.58B | 3.49B | 91.83% | 84.92% | 42.82M | 2.44% |
| s15850.v | Pure Python Engine | 4.26 | 861.99M | 3.67B | 1.64B | 99.42% | 25.08% | 7.04M | 0.15% |
| s15850.v | Icarus Verilog | 3.10 | 5.44B | 16.87B | 8.82B | 96.77% | 62.76% | 106.39M | 0.63% |
| s35932.v | rx-prop | 3.13 | 6.58B | 20.57B | 6.48B | 84.77% | 82.43% | 173.83M | 0.19% |
| s35932.v | rx-sweep (Linear) | 3.95 | 6.74B | 26.59B | 7.96B | 87.31% | 89.20% | 109.17M | 0.21% |
| s35932.v | rx-oop (OOP Engine) | 2.28 | 9.04B | 20.61B | 11.46B | 89.04% | 67.25% | 411.44M | 0.40% |
| s35932.v | Pure Python Engine | 3.68 | 3.98B | 14.64B | 6.63B | 99.36% | 24.72% | 31.98M | 0.16% |
| s35932.v | Icarus Verilog | 3.97 | 16.44B | 65.27B | 30.76B | 94.62% | 70.87% | 482.26M | 0.10% |
| s38584.v | rx-prop | 2.33 | 7.47B | 17.43B | 6.04B | 86.99% | 78.53% | 168.81M | 2.59% |
| s38584.v | rx-sweep (Linear) | 2.79 | 8.24B | 22.96B | 7.67B | 89.05% | 85.13% | 124.98M | 2.37% |
| s38584.v | rx-oop (OOP Engine) | 1.48 | 11.73B | 17.40B | 11.67B | 91.39% | 55.08% | 451.29M | 3.23% |
| s38584.v | Pure Python Engine | 3.42 | 3.31B | 11.33B | 5.16B | 99.21% | 39.04% | 24.76M | 0.17% |
| s38584.v | Icarus Verilog | 2.45 | 18.86B | 46.12B | 26.16B | 95.90% | 50.11% | 535.80M | 0.98% |
| s38417.v | rx-prop | 2.92 | 5.08B | 14.86B | 4.81B | 86.07% | 82.18% | 119.83M | 0.84% |
| s38417.v | rx-sweep (Linear) | 3.64 | 5.77B | 20.99B | 6.41B | 87.55% | 89.23% | 85.84M | 0.72% |
| s38417.v | rx-oop (OOP Engine) | 1.92 | 7.91B | 15.19B | 9.03B | 90.42% | 61.87% | 330.42M | 1.17% |
| s38417.v | Pure Python Engine | 3.58 | 1.32B | 4.74B | 2.15B | 99.40% | 17.87% | 10.92M | 0.21% |
| s38417.v | Icarus Verilog | 3.22 | 11.72B | 37.71B | 19.63B | 96.18% | 63.78% | 271.96M | 0.39% |
