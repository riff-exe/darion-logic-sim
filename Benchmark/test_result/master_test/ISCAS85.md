# Master Test Unified Benchmark Report: tests/ISCAS85

**Execution Parameters:**
- **Target Suite / Path:** `tests/ISCAS85`
- **Circuits Benchmarked:** 10
- **Simulation Vectors (Phase 3):** 10,000 (Warmup: 10)
- **Verification Vectors (Phase 2):** 100
- **Hardware Profiler:** Linux `perf` kernel PMU counters

---

## 1. Zero-Testbench Memory Footprint (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| c432.v | 203 | 0.50 MB (31.9 MB peak) | 0.34 MB (33.4 MB peak) | 0.04 MB (7.9 MB peak) | 0.71 MB (4.4 MB peak) |
| c499.v | 275 | 0.57 MB (31.9 MB peak) | 0.45 MB (33.5 MB peak) | 0.19 MB (8.0 MB peak) | 0.67 MB (4.4 MB peak) |
| c880.v | 469 | 0.78 MB (32.2 MB peak) | 0.62 MB (33.7 MB peak) | 0.18 MB (8.0 MB peak) | 0.71 MB (4.4 MB peak) |
| c1355.v | 619 | 0.93 MB (32.4 MB peak) | 0.81 MB (33.9 MB peak) | 0.29 MB (8.2 MB peak) | 0.70 MB (4.4 MB peak) |
| c1908.v | 938 | 1.21 MB (32.6 MB peak) | 1.18 MB (34.2 MB peak) | 0.48 MB (8.3 MB peak) | 0.71 MB (4.4 MB peak) |
| c2670.v | 1,642 | 1.86 MB (33.3 MB peak) | 2.06 MB (35.1 MB peak) | 0.71 MB (8.6 MB peak) | 0.76 MB (4.4 MB peak) |
| c3540.v | 1,741 | 2.00 MB (33.4 MB peak) | 2.22 MB (35.3 MB peak) | 0.85 MB (8.7 MB peak) | 0.73 MB (4.4 MB peak) |
| c5315.v | 2,608 | 2.83 MB (34.2 MB peak) | 3.27 MB (36.4 MB peak) | 1.24 MB (9.0 MB peak) | 0.75 MB (4.4 MB peak) |
| c6288.v | 2,480 | 2.73 MB (34.1 MB peak) | 3.20 MB (36.2 MB peak) | 1.20 MB (9.0 MB peak) | 0.91 MB (4.5 MB peak) |
| c7552.v | 3,828 | 3.93 MB (35.3 MB peak) | 4.70 MB (37.8 MB peak) | 1.71 MB (9.6 MB peak) | 0.82 MB (4.5 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| c432.v | 203 | 0.37 ms (0.017 ms opt) | 0.76 ms | 2.93 ms | 2.61 s |
| c499.v | 275 | 0.47 ms (0.021 ms opt) | 2.51 ms | 3.18 ms | 2.57 s |
| c880.v | 469 | 0.73 ms (0.045 ms opt) | 2.35 ms | 3.60 ms | 2.54 s |
| c1355.v | 619 | 0.66 ms (0.049 ms opt) | 2.55 ms | 4.11 ms | 2.59 s |
| c1908.v | 938 | 0.95 ms (0.077 ms opt) | 2.93 ms | 5.25 ms | 2.56 s |
| c2670.v | 1,642 | 1.85 ms (0.194 ms opt) | 4.03 ms | 7.76 ms | 2.58 s |
| c3540.v | 1,741 | 1.46 ms (0.139 ms opt) | 3.88 ms | 8.62 ms | 2.59 s |
| c5315.v | 2,608 | 2.07 ms (0.205 ms opt) | 5.07 ms | 12.07 ms | 2.62 s |
| c6288.v | 2,480 | 1.92 ms (0.260 ms opt) | 5.08 ms | 11.52 ms | 2.75 s |
| c7552.v | 3,828 | 2.74 ms (0.297 ms opt) | 8.32 ms | 17.36 ms | 2.88 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| c432.v | 9.77 ms | 9.12 ms | 13.65 ms | 504.10 ms | 85.06 ms | 1.17 ms |
| c499.v | 10.60 ms | 11.88 ms | 14.73 ms | 1958.43 ms | 102.05 ms | 0.95 ms |
| c880.v | 22.32 ms | 19.84 ms | 36.05 ms | 1044.42 ms | 167.26 ms | 2.07 ms |
| c1355.v | 30.61 ms | 24.20 ms | 45.43 ms | 3180.56 ms | 229.28 ms | 1.93 ms |
| c1908.v | 63.34 ms | 35.89 ms | 102.16 ms | 3440.41 ms | 383.82 ms | 2.24 ms |
| c2670.v | 92.81 ms | 69.88 ms | 152.24 ms | 4006.23 ms | 725.44 ms | 7.21 ms |
| c3540.v | 111.90 ms | 67.33 ms | 190.15 ms | 6016.52 ms | 661.78 ms | 4.47 ms |
| c5315.v | 211.03 ms | 123.69 ms | 334.17 ms | 9661.32 ms | 1380.45 ms | 6.08 ms |
| c6288.v | 1011.10 ms | 97.58 ms | 1444.14 ms | 97.97 s | 6812.41 ms | 9.11 ms |
| c7552.v | 320.15 ms | 174.99 ms | 513.15 ms | 16.18 s | 1982.67 ms | 9.32 ms |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| c432.v | 8.70x | 9.33x | 6.23x | 0.17x | 1.00x | 72.41x |
| c499.v | 9.63x | 8.59x | 6.93x | 0.05x | 1.00x | 107.82x |
| c880.v | 7.49x | 8.43x | 4.64x | 0.16x | 1.00x | 80.99x |
| c1355.v | 7.49x | 9.47x | 5.05x | 0.07x | 1.00x | 118.56x |
| c1908.v | 6.06x | 10.70x | 3.76x | 0.11x | 1.00x | 171.10x |
| c2670.v | 7.82x | 10.38x | 4.76x | 0.18x | 1.00x | 100.56x |
| c3540.v | 5.91x | 9.83x | 3.48x | 0.11x | 1.00x | 148.14x |
| c5315.v | 6.54x | 11.16x | 4.13x | 0.14x | 1.00x | 227.14x |
| c6288.v | 6.74x | 69.82x | 4.72x | 0.07x | 1.00x | 747.86x |
| c7552.v | 6.19x | 11.33x | 3.86x | 0.12x | 1.00x | 212.84x |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `7.17x`
- **rx-sweep (Linear Compiled):** `12.00x`
- **rx-oop (OOP Graph):** `4.65x`
- **Pure Python Engine:** `0.11x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `152.74x`

### Cross-Engine Comparisons

- **Cython Reactor (`rx-prop`) vs Pure Python:** `64.82x` faster
- **Cython Reactor (`rx-sweep`) vs Pure Python:** `108.43x` faster
- **Reactor Sweep vs Propagate Ratio:** `1.67x` (sweep faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | IPC | Cycles | Instructions | L1 Loads | L1 Hit% | L2 Hit% | LLC Misses | Brn Miss% |
|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| c432.v | rx-prop | 2.40 | 32.15M | 77.15M | 31.31M | 99.85% | 85.96% | 6.50K | 6.18% |
| c432.v | rx-sweep (Linear) | 2.67 | 32.39M | 86.36M | 31.01M | 99.07% | 96.90% | 9.42K | 4.20% |
| c432.v | rx-oop (OOP Engine) | 1.84 | 44.01M | 80.83M | 48.69M | 99.65% | 97.52% | 4.37K | 7.53% |
| c432.v | Pure Python Engine | 4.95 | 87.05M | 430.95M | 176.78M | 99.70% | 98.91% | 4.98K | 0.27% |
| c432.v | Icarus Verilog | 3.84 | 311.29M | 1.19B | 514.50M | 99.05% | 99.77% | 11.81K | 1.12% |
| c499.v | rx-prop | 4.10 | 30.45M | 124.72M | 41.87M | 99.71% | 93.87% | 2.11K | 2.64% |
| c499.v | rx-sweep (Linear) | 3.41 | 31.79M | 108.41M | 36.44M | 99.77% | 97.30% | 2.45K | 4.35% |
| c499.v | rx-oop (OOP Engine) | 2.32 | 63.85M | 147.93M | 95.46M | 99.06% | 96.26% | 34.44K | 2.63% |
| c499.v | Pure Python Engine | 4.82 | 375.21M | 1.81B | 786.86M | 99.74% | 99.46% | 9.98K | 0.21% |
| c499.v | Icarus Verilog | 3.75 | 406.39M | 1.52B | 659.61M | 98.62% | 99.93% | 8.77K | 1.06% |
| c880.v | rx-prop | 2.38 | 86.69M | 206.44M | 80.17M | 99.16% | 99.71% | 1.89K | 7.12% |
| c880.v | rx-sweep (Linear) | 2.65 | 68.08M | 180.21M | 63.22M | 98.76% | 99.78% | 1.69K | 5.82% |
| c880.v | rx-oop (OOP Engine) | 1.34 | 130.77M | 174.59M | 144.73M | 98.02% | 99.70% | 8.38K | 10.37% |
| c880.v | Pure Python Engine | 4.42 | 194.22M | 857.96M | 397.12M | 99.67% | 97.51% | 17.21K | 0.34% |
| c880.v | Icarus Verilog | 3.41 | 674.50M | 2.30B | 1.05B | 98.16% | 99.90% | 29.73K | 1.21% |
| c1355.v | rx-prop | 3.02 | 117.07M | 353.20M | 120.35M | 97.47% | 99.75% | 4.99K | 4.54% |
| c1355.v | rx-sweep (Linear) | 2.81 | 92.40M | 260.06M | 89.51M | 95.62% | 99.79% | 8.00K | 4.15% |
| c1355.v | rx-oop (OOP Engine) | 1.93 | 172.06M | 331.31M | 209.11M | 97.09% | 99.78% | 13.50K | 5.75% |
| c1355.v | Pure Python Engine | 4.60 | 618.90M | 2.85B | 1.28B | 99.66% | 97.47% | 126.09K | 0.25% |
| c1355.v | Icarus Verilog | 3.62 | 924.23M | 3.34B | 1.49B | 98.10% | 99.84% | 32.94K | 1.00% |
| c1908.v | rx-prop | 2.50 | 251.69M | 628.64M | 223.46M | 96.47% | 99.89% | 5.90K | 5.28% |
| c1908.v | rx-sweep (Linear) | 2.76 | 133.46M | 367.71M | 126.39M | 93.06% | 99.93% | 9.73K | 3.12% |
| c1908.v | rx-oop (OOP Engine) | 1.79 | 387.95M | 694.19M | 450.63M | 97.42% | 99.89% | 12.81K | 6.71% |
| c1908.v | Pure Python Engine | 4.76 | 658.28M | 3.13B | 1.38B | 99.62% | 99.29% | 25.64K | 0.29% |
| c1908.v | Icarus Verilog | 3.31 | 1.55B | 5.13B | 2.50B | 97.38% | 99.99% | 5.54K | 1.20% |
| c2670.v | rx-prop | 2.23 | 395.68M | 882.03M | 364.92M | 95.35% | 99.61% | 66.97K | 5.14% |
| c2670.v | rx-sweep (Linear) | 2.46 | 306.30M | 752.12M | 281.29M | 93.51% | 99.64% | 61.02K | 4.32% |
| c2670.v | rx-oop (OOP Engine) | 1.48 | 622.88M | 919.03M | 672.25M | 96.22% | 99.68% | 89.52K | 7.51% |
| c2670.v | Pure Python Engine | 4.64 | 775.97M | 3.60B | 1.65B | 99.63% | 94.03% | 368.51K | 0.27% |
| c2670.v | Icarus Verilog | 3.49 | 2.91B | 10.13B | 4.83B | 97.75% | 99.80% | 229.94K | 0.99% |
| c3540.v | rx-prop | 2.23 | 453.78M | 1.01B | 382.01M | 95.90% | 99.88% | 19.47K | 6.25% |
| c3540.v | rx-sweep (Linear) | 2.64 | 253.52M | 669.03M | 227.88M | 92.60% | 99.77% | 36.64K | 4.78% |
| c3540.v | rx-oop (OOP Engine) | 1.40 | 761.18M | 1.07B | 793.54M | 96.98% | 99.77% | 56.05K | 9.16% |
| c3540.v | Pure Python Engine | 4.55 | 1.15B | 5.23B | 2.37B | 99.60% | 93.53% | 609.36K | 0.26% |
| c3540.v | Icarus Verilog | 2.95 | 2.65B | 7.82B | 3.98B | 96.67% | 99.87% | 209.97K | 1.54% |
| c5315.v | rx-prop | 2.15 | 843.99M | 1.81B | 709.62M | 93.41% | 99.75% | 103.53K | 5.79% |
| c5315.v | rx-sweep (Linear) | 2.50 | 504.67M | 1.26B | 457.08M | 93.34% | 99.80% | 74.65K | 4.79% |
| c5315.v | rx-oop (OOP Engine) | 1.41 | 1.36B | 1.92B | 1.42B | 95.63% | 99.87% | 96.90K | 8.15% |
| c5315.v | Pure Python Engine | 4.53 | 354.79M | 1.61B | 738.13M | 99.62% | 79.19% | 578.28K | 0.27% |
| c5315.v | Icarus Verilog | 2.98 | 5.53B | 16.51B | 8.22B | 96.67% | 93.91% | 16.68M | 1.35% |
| c6288.v | rx-prop | 2.65 | 4.07B | 10.80B | 3.43B | 91.63% | 99.91% | 248.90K | 4.39% |
| c6288.v | rx-sweep (Linear) | 3.28 | 388.37M | 1.27B | 416.68M | 93.34% | 99.93% | 19.60K | 2.38% |
| c6288.v | rx-oop (OOP Engine) | 1.93 | 5.83B | 11.27B | 6.84B | 93.86% | 99.96% | 190.97K | 5.52% |
| c6288.v | Pure Python Engine | 4.57 | 3.75B | 17.14B | 7.71B | 99.57% | 94.37% | 1.87M | 0.20% |
| c6288.v | Icarus Verilog | 3.57 | 27.31B | 97.48B | 44.05B | 95.74% | 99.55% | 8.46M | 0.81% |
| c7552.v | rx-prop | 2.02 | 1.31B | 2.65B | 1.03B | 91.56% | 99.86% | 123.42K | 5.98% |
| c7552.v | rx-sweep (Linear) | 2.46 | 727.63M | 1.79B | 667.18M | 93.34% | 99.73% | 119.05K | 4.88% |
| c7552.v | rx-oop (OOP Engine) | 1.44 | 2.08B | 2.99B | 2.16B | 94.85% | 99.65% | 405.98K | 7.65% |
| c7552.v | Pure Python Engine | 4.32 | 609.17M | 2.63B | 1.20B | 99.60% | 67.63% | 1.55M | 0.40% |
| c7552.v | Icarus Verilog | 2.91 | 7.95B | 23.12B | 11.72B | 96.37% | 89.85% | 43.18M | 1.38% |
