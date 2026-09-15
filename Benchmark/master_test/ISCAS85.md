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
| c432.v | 203 | 0.58 MB (31.9 MB peak) | 0.32 MB (33.4 MB peak) | 0.15 MB (8.0 MB peak) | 0.71 MB (4.4 MB peak) |
| c499.v | 275 | 0.66 MB (32.0 MB peak) | 0.42 MB (33.5 MB peak) | 0.05 MB (8.0 MB peak) | 0.60 MB (4.3 MB peak) |
| c880.v | 469 | 0.86 MB (32.2 MB peak) | 0.62 MB (33.7 MB peak) | 0.16 MB (8.0 MB peak) | 0.71 MB (4.4 MB peak) |
| c1355.v | 619 | 1.02 MB (32.4 MB peak) | 0.84 MB (33.9 MB peak) | 0.29 MB (8.2 MB peak) | 0.73 MB (4.4 MB peak) |
| c1908.v | 938 | 1.34 MB (32.6 MB peak) | 1.21 MB (34.3 MB peak) | 0.55 MB (8.4 MB peak) | 0.70 MB (4.4 MB peak) |
| c2670.v | 1,642 | 1.91 MB (33.3 MB peak) | 2.07 MB (35.1 MB peak) | 0.80 MB (8.6 MB peak) | 0.75 MB (4.4 MB peak) |
| c3540.v | 1,741 | 2.09 MB (33.4 MB peak) | 2.28 MB (35.4 MB peak) | 0.79 MB (8.7 MB peak) | 0.70 MB (4.4 MB peak) |
| c5315.v | 2,608 | 2.88 MB (34.2 MB peak) | 3.31 MB (36.3 MB peak) | 1.29 MB (9.1 MB peak) | 0.76 MB (4.5 MB peak) |
| c6288.v | 2,480 | 2.73 MB (34.2 MB peak) | 3.21 MB (36.2 MB peak) | 1.22 MB (9.1 MB peak) | 0.82 MB (4.5 MB peak) |
| c7552.v | 3,828 | 3.95 MB (35.3 MB peak) | 4.71 MB (37.7 MB peak) | 1.88 MB (9.7 MB peak) | 0.75 MB (4.4 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| c432.v | 203 | 1.01 ms (0.029 ms opt) | 1.44 ms | 4.38 ms | 3.69 s |
| c499.v | 275 | 0.57 ms (0.028 ms opt) | 10.78 ms | 4.20 ms | 3.54 s |
| c880.v | 469 | 0.80 ms (0.059 ms opt) | 11.30 ms | 4.86 ms | 3.57 s |
| c1355.v | 619 | 0.94 ms (0.067 ms opt) | 11.41 ms | 5.85 ms | 3.56 s |
| c1908.v | 938 | 1.23 ms (0.118 ms opt) | 12.18 ms | 8.44 ms | 3.59 s |
| c2670.v | 1,642 | 2.42 ms (0.171 ms opt) | 13.36 ms | 11.18 ms | 3.58 s |
| c3540.v | 1,741 | 1.94 ms (0.199 ms opt) | 13.65 ms | 12.37 ms | 3.62 s |
| c5315.v | 2,608 | 2.74 ms (0.295 ms opt) | 15.34 ms | 17.86 ms | 3.66 s |
| c6288.v | 2,480 | 2.62 ms (0.231 ms opt) | 14.97 ms | 16.27 ms | 3.76 s |
| c7552.v | 3,828 | 3.96 ms (0.432 ms opt) | 19.90 ms | 24.13 ms | 3.83 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| c432.v | 14.68 ms | 13.61 ms | 15.05 ms | 731.26 ms | 118.63 ms | 1.97 ms |
| c499.v | 15.60 ms | 16.92 ms | 15.74 ms | 2859.69 ms | 146.65 ms | 1.82 ms |
| c880.v | 33.18 ms | 30.14 ms | 34.78 ms | 1470.50 ms | 237.33 ms | 2.66 ms |
| c1355.v | 45.21 ms | 36.90 ms | 47.11 ms | 4560.74 ms | 323.97 ms | 3.32 ms |
| c1908.v | 89.84 ms | 53.34 ms | 98.59 ms | 4927.53 ms | 560.31 ms | 3.07 ms |
| c2670.v | 133.11 ms | 104.19 ms | 150.04 ms | 5924.12 ms | 1041.84 ms | 11.44 ms |
| c3540.v | 162.32 ms | 95.06 ms | 172.32 ms | 8555.40 ms | 960.75 ms | 6.21 ms |
| c5315.v | 297.85 ms | 179.96 ms | 322.18 ms | 14.36 s | 1945.15 ms | 9.77 ms |
| c6288.v | 1465.41 ms | 140.46 ms | 1684.27 ms | 140.86 s | 9880.55 ms | 13.61 ms |
| c7552.v | 451.92 ms | 255.31 ms | 485.82 ms | 23.39 s | 2838.13 ms | 13.58 ms |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| c432.v | 8.08x | 8.72x | 7.88x | 0.16x | 1.00x | 60.22x |
| c499.v | 9.40x | 8.66x | 9.31x | 0.05x | 1.00x | 80.78x |
| c880.v | 7.15x | 7.87x | 6.82x | 0.16x | 1.00x | 89.23x |
| c1355.v | 7.17x | 8.78x | 6.88x | 0.07x | 1.00x | 97.51x |
| c1908.v | 6.24x | 10.50x | 5.68x | 0.11x | 1.00x | 182.64x |
| c2670.v | 7.83x | 10.00x | 6.94x | 0.18x | 1.00x | 91.07x |
| c3540.v | 5.92x | 10.11x | 5.58x | 0.11x | 1.00x | 154.82x |
| c5315.v | 6.53x | 10.81x | 6.04x | 0.14x | 1.00x | 199.16x |
| c6288.v | 6.74x | 70.35x | 5.87x | 0.07x | 1.00x | 726.20x |
| c7552.v | 6.28x | 11.12x | 5.84x | 0.12x | 1.00x | 208.93x |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `7.07x`
- **rx-sweep (Linear Compiled):** `11.67x`
- **rx-oop (OOP Graph):** `6.60x`
- **Pure Python Engine:** `0.11x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `141.83x`

### Cross-Engine Comparisons

- **Cython Reactor (`rx-prop`) vs Pure Python:** `64.57x` faster
- **Cython Reactor (`rx-sweep`) vs Pure Python:** `106.62x` faster
- **Reactor Sweep vs Propagate Ratio:** `1.65x` (sweep faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | IPC | Cycles | Instructions | L1 Loads | L1 Hit% | L2 Hit% | LLC Misses | Brn Miss% |
|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| c432.v | rx-prop | 2.82 | 29.70M | 83.79M | 31.74M | 99.88% | 90.68% | 3.19K | 6.19% |
| c432.v | rx-sweep (Linear) | 2.79 | 29.18M | 81.36M | 28.24M | 99.89% | 98.47% | 2.13K | 6.12% |
| c432.v | rx-oop (OOP Engine) | 3.22 | 21.71M | 69.85M | 30.42M | 99.26% | 97.13% | 6.43K | 6.37% |
| c432.v | Pure Python Engine | 4.80 | 87.67M | 421.20M | 188.87M | 99.66% | 99.03% | 2.69K | 0.25% |
| c432.v | Icarus Verilog | 3.75 | 322.30M | 1.21B | 541.09M | 99.07% | 99.93% | 3.29K | 1.02% |
| c499.v | rx-prop | 4.20 | 32.06M | 134.55M | 39.91M | 99.82% | 94.16% | 4.17K | 2.73% |
| c499.v | rx-sweep (Linear) | 3.28 | 48.19M | 158.20M | 49.91M | 99.26% | 94.65% | 22.69K | 2.81% |
| c499.v | rx-oop (OOP Engine) | 3.50 | 40.92M | 143.31M | 48.09M | 98.90% | 98.34% | 9.28K | 3.13% |
| c499.v | Pure Python Engine | 4.78 | 378.44M | 1.81B | 798.32M | 99.69% | 98.66% | 32.87K | 0.22% |
| c499.v | Icarus Verilog | 3.82 | 390.57M | 1.49B | 655.41M | 98.62% | 99.95% | 4.51K | 0.97% |
| c880.v | rx-prop | 2.26 | 86.21M | 194.97M | 84.44M | 99.06% | 99.26% | 5.99K | 6.86% |
| c880.v | rx-sweep (Linear) | 2.39 | 79.31M | 189.81M | 69.31M | 98.39% | 98.87% | 8.90K | 6.20% |
| c880.v | rx-oop (OOP Engine) | 2.08 | 94.56M | 196.47M | 84.59M | 96.60% | 99.38% | 17.43K | 7.15% |
| c880.v | Pure Python Engine | 4.72 | 187.36M | 884.99M | 395.61M | 99.68% | 98.89% | 12.04K | 0.27% |
| c880.v | Icarus Verilog | 3.50 | 654.52M | 2.29B | 1.05B | 98.14% | 99.97% | 3.53K | 1.13% |
| c1355.v | rx-prop | 3.19 | 115.62M | 368.67M | 121.90M | 97.32% | 99.24% | 28.62K | 3.78% |
| c1355.v | rx-sweep (Linear) | 2.74 | 93.94M | 257.00M | 87.83M | 95.86% | 99.82% | 7.64K | 4.08% |
| c1355.v | rx-oop (OOP Engine) | 2.87 | 121.28M | 348.47M | 120.43M | 94.86% | 99.84% | 5.45K | 4.83% |
| c1355.v | Pure Python Engine | 4.69 | 606.69M | 2.85B | 1.28B | 99.66% | 98.95% | 46.82K | 0.22% |
| c1355.v | Icarus Verilog | 3.73 | 888.63M | 3.31B | 1.48B | 98.11% | 99.98% | 7.43K | 0.95% |
| c1908.v | rx-prop | 2.55 | 242.06M | 616.54M | 226.20M | 96.46% | 99.93% | 5.41K | 4.74% |
| c1908.v | rx-sweep (Linear) | 2.68 | 140.22M | 375.93M | 129.43M | 93.36% | 99.95% | 4.52K | 3.23% |
| c1908.v | rx-oop (OOP Engine) | 2.71 | 263.23M | 713.13M | 259.68M | 95.50% | 99.79% | 18.57K | 5.21% |
| c1908.v | Pure Python Engine | 4.75 | 660.48M | 3.14B | 1.40B | 99.61% | 98.76% | 60.38K | 0.20% |
| c1908.v | Icarus Verilog | 3.35 | 1.53B | 5.13B | 2.44B | 97.28% | 99.82% | 129.19K | 1.16% |
| c2670.v | rx-prop | 2.27 | 388.92M | 884.59M | 368.72M | 95.33% | 99.55% | 76.12K | 4.89% |
| c2670.v | rx-sweep (Linear) | 2.49 | 299.22M | 744.21M | 287.14M | 93.53% | 99.59% | 77.05K | 4.39% |
| c2670.v | rx-oop (OOP Engine) | 2.19 | 427.11M | 933.48M | 402.31M | 93.83% | 99.64% | 92.28K | 5.61% |
| c2670.v | Pure Python Engine | 4.61 | 793.24M | 3.66B | 1.66B | 99.62% | 93.99% | 375.67K | 0.25% |
| c2670.v | Icarus Verilog | 3.52 | 2.87B | 10.11B | 4.82B | 97.74% | 99.96% | 47.08K | 0.97% |
| c3540.v | rx-prop | 2.28 | 442.95M | 1.01B | 379.65M | 95.81% | 99.91% | 14.33K | 6.06% |
| c3540.v | rx-sweep (Linear) | 2.58 | 258.84M | 666.66M | 237.56M | 92.61% | 99.93% | 12.99K | 4.72% |
| c3540.v | rx-oop (OOP Engine) | 2.27 | 472.45M | 1.07B | 420.49M | 94.55% | 99.92% | 20.33K | 6.75% |
| c3540.v | Pure Python Engine | 4.60 | 1.15B | 5.27B | 2.40B | 99.49% | 95.14% | 574.81K | 0.24% |
| c3540.v | Icarus Verilog | 2.97 | 2.65B | 7.85B | 3.98B | 96.59% | 99.94% | 82.93K | 1.49% |
| c5315.v | rx-prop | 2.19 | 845.55M | 1.85B | 724.40M | 93.28% | 99.81% | 96.60K | 5.27% |
| c5315.v | rx-sweep (Linear) | 2.47 | 511.82M | 1.27B | 473.62M | 93.33% | 99.77% | 73.99K | 4.85% |
| c5315.v | rx-oop (OOP Engine) | 2.19 | 905.36M | 1.99B | 788.08M | 92.41% | 99.74% | 153.45K | 5.97% |
| c5315.v | Pure Python Engine | 4.49 | 367.76M | 1.65B | 744.34M | 99.62% | 78.71% | 593.88K | 0.28% |
| c5315.v | Icarus Verilog | 3.08 | 5.35B | 16.51B | 8.09B | 96.60% | 98.04% | 5.39M | 1.30% |
| c6288.v | rx-prop | 2.67 | 4.04B | 10.80B | 3.44B | 91.73% | 99.95% | 157.17K | 4.40% |
| c6288.v | rx-sweep (Linear) | 3.35 | 382.23M | 1.28B | 411.85M | 93.34% | 99.97% | 8.93K | 2.28% |
| c6288.v | rx-oop (OOP Engine) | 2.58 | 4.66B | 12.03B | 4.00B | 90.02% | 99.99% | 53.81K | 4.58% |
| c6288.v | Pure Python Engine | 4.65 | 3.70B | 17.19B | 7.74B | 99.57% | 94.62% | 1.79M | 0.23% |
| c6288.v | Icarus Verilog | 3.58 | 27.26B | 97.45B | 43.13B | 95.64% | 99.42% | 10.78M | 0.81% |
| c7552.v | rx-prop | 2.09 | 1.27B | 2.66B | 1.01B | 91.34% | 99.78% | 195.42K | 5.34% |
| c7552.v | rx-sweep (Linear) | 2.46 | 723.83M | 1.78B | 670.24M | 93.34% | 99.57% | 190.02K | 5.01% |
| c7552.v | rx-oop (OOP Engine) | 2.22 | 1.36B | 3.02B | 1.18B | 90.79% | 99.89% | 115.18K | 5.82% |
| c7552.v | Pure Python Engine | 4.46 | 599.41M | 2.67B | 1.18B | 99.48% | 73.21% | 1.64M | 0.24% |
| c7552.v | Icarus Verilog | 2.96 | 7.80B | 23.12B | 11.76B | 96.34% | 91.29% | 37.54M | 1.32% |
