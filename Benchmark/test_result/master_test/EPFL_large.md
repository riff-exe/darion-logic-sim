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
| sin.v | 8,947 | 9.52 MB (40.8 MB peak) | N/A | 5.34 MB (13.2 MB peak) | 0.78 MB (4.5 MB peak) |
| voter.v | 27,720 | 29.32 MB (60.6 MB peak) | N/A | 17.91 MB (25.8 MB peak) | 1.14 MB (4.8 MB peak) |
| square.v | 35,687 | 37.15 MB (68.6 MB peak) | N/A | 22.64 MB (30.5 MB peak) | 1.27 MB (5.0 MB peak) |
| sqrt.v | 41,234 | 40.15 MB (71.6 MB peak) | N/A | 27.10 MB (35.0 MB peak) | 1.16 MB (4.7 MB peak) |
| multiplier.v | 50,760 | 49.16 MB (80.5 MB peak) | N/A | 33.05 MB (40.9 MB peak) | 1.13 MB (4.8 MB peak) |
| log2.v | 54,531 | 52.97 MB (84.4 MB peak) | N/A | 35.51 MB (43.3 MB peak) | 1.10 MB (4.8 MB peak) |
| mem_ctrl.v | 84,974 | 79.09 MB (110.5 MB peak) | N/A | 55.34 MB (63.2 MB peak) | 1.47 MB (5.2 MB peak) |
| div.v | 101,859 | 99.99 MB (131.3 MB peak) | N/A | 67.19 MB (75.1 MB peak) | 1.66 MB (5.3 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| sin.v | 8,947 | 6.97 ms (0.668 ms opt) | N/A | 43.51 ms | 3.06 s |
| voter.v | 27,720 | 20.96 ms (2.128 ms opt) | N/A | 149.89 ms | 4.62 s |
| square.v | 35,687 | 27.14 ms (3.936 ms opt) | N/A | 192.75 ms | 5.77 s |
| sqrt.v | 41,234 | 30.96 ms (3.993 ms opt) | N/A | 230.03 ms | 6.00 s |
| multiplier.v | 50,760 | 40.27 ms (6.584 ms opt) | N/A | 282.96 ms | 6.93 s |
| log2.v | 54,531 | 44.50 ms (8.144 ms opt) | N/A | 319.64 ms | 7.86 s |
| mem_ctrl.v | 84,974 | 76.94 ms (18.834 ms opt) | N/A | 889.49 ms | 13.74 s |
| div.v | 101,859 | 114.49 ms (16.394 ms opt) | N/A | 652.82 ms | 21.85 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| sin.v | 327.81 ms | 15.38 ms | 502.21 ms | N/A | 1581.87 ms | 1.02 ms |
| voter.v | 273.25 ms | 43.37 ms | 425.62 ms | N/A | 1430.40 ms | 2.73 ms |
| square.v | 239.96 ms | 63.28 ms | 349.40 ms | N/A | 1088.49 ms | 5.00 ms |
| sqrt.v | 29.42 s | 69.06 ms | 36.41 s | N/A | 133.52 s | 3.21 ms |
| multiplier.v | 1794.47 ms | 87.47 ms | 2924.84 ms | N/A | 9413.57 ms | 3.58 ms |
| log2.v | 8321.81 ms | 94.33 ms | 13.12 s | N/A | 43.85 s | 5.19 ms |
| mem_ctrl.v | 262.77 ms | 165.37 ms | 426.73 ms | N/A | 2126.06 ms | 27.96 ms |
| div.v | 461.79 ms | 140.94 ms | 621.77 ms | N/A | 3278.70 ms | 46.37 ms |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| sin.v | 4.83x | 102.86x | 3.15x | N/A | 1.00x | 1555.97x |
| voter.v | 5.23x | 32.98x | 3.36x | N/A | 1.00x | 523.08x |
| square.v | 4.54x | 17.20x | 3.12x | N/A | 1.00x | 217.66x |
| sqrt.v | 4.54x | 1933.36x | 3.67x | N/A | 1.00x | 41607.45x |
| multiplier.v | 5.25x | 107.63x | 3.22x | N/A | 1.00x | 2625.94x |
| log2.v | 5.27x | 464.82x | 3.34x | N/A | 1.00x | 8449.77x |
| mem_ctrl.v | 8.09x | 12.86x | 4.98x | N/A | 1.00x | 76.04x |
| div.v | 7.10x | 23.26x | 5.27x | N/A | 1.00x | 70.70x |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `5.49x`
- **rx-sweep (Linear Compiled):** `80.06x`
- **rx-oop (OOP Graph):** `3.69x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `984.05x`

### Cross-Engine Comparisons

- **Reactor Sweep vs Propagate Ratio:** `14.58x` (sweep faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | IPC | Cycles | Instructions | L1 Loads | L1 Hit% | L2 Hit% | LLC Misses | Brn Miss% |
|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| sin.v | rx-prop | 1.76 | 1.30B | 2.28B | 936.21M | 91.37% | 99.65% | 271.74K | 8.65% |
| sin.v | rx-sweep (Linear) | 2.78 | 41.72M | 115.85M | 39.76M | 92.37% | 97.47% | 86.86K | 5.56% |
| sin.v | rx-oop (OOP Engine) | 1.24 | 2.01B | 2.50B | 1.93B | 94.20% | 98.69% | 1.43M | 10.02% |
| sin.v | Icarus Verilog | 2.53 | 6.34B | 16.02B | 8.93B | 95.65% | 88.40% | 44.82M | 1.61% |
| voter.v | rx-prop | 1.64 | 1.09B | 1.78B | 748.40M | 91.31% | 88.17% | 7.71M | 8.97% |
| voter.v | rx-sweep (Linear) | 3.28 | 155.42M | 509.36M | 156.34M | 92.78% | 88.26% | 1.43M | 3.47% |
| voter.v | rx-oop (OOP Engine) | 1.18 | 1.70B | 2.00B | 1.57B | 94.50% | 84.76% | 13.20M | 10.03% |
| voter.v | Icarus Verilog | 2.40 | 5.73B | 13.75B | 7.87B | 96.50% | 62.23% | 104.14M | 1.60% |
| square.v | rx-prop | 1.55 | 951.31M | 1.47B | 622.54M | 90.62% | 86.68% | 7.81M | 8.56% |
| square.v | rx-sweep (Linear) | 2.36 | 256.25M | 605.05M | 224.83M | 92.64% | 80.87% | 3.17M | 5.18% |
| square.v | rx-oop (OOP Engine) | 1.13 | 1.33B | 1.50B | 1.19B | 94.26% | 80.79% | 13.45M | 9.85% |
| square.v | Icarus Verilog | 2.17 | 4.31B | 9.35B | 5.57B | 95.87% | 57.44% | 98.55M | 1.59% |
| sqrt.v | rx-prop | 1.33 | 118.32B | 157.32B | 64.68B | 89.60% | 46.91% | 3.57B | 6.95% |
| sqrt.v | rx-sweep (Linear) | 3.09 | 261.16M | 806.00M | 276.10M | 92.77% | 79.41% | 4.09M | 2.68% |
| sqrt.v | rx-oop (OOP Engine) | 1.00 | 146.25B | 145.96B | 116.56B | 94.04% | 33.88% | 4.59B | 8.08% |
| sqrt.v | Icarus Verilog | 1.80 | 536.08B | 962.76B | 615.66B | 95.73% | 21.06% | 20.75B | 1.49% |
| multiplier.v | rx-prop | 1.54 | 7.20B | 11.10B | 4.72B | 90.45% | 80.63% | 87.17M | 8.16% |
| multiplier.v | rx-sweep (Linear) | 2.78 | 323.79M | 898.60M | 314.70M | 92.23% | 79.63% | 5.02M | 3.67% |
| multiplier.v | rx-oop (OOP Engine) | 1.03 | 11.77B | 12.13B | 10.04B | 94.20% | 63.03% | 214.67M | 9.83% |
| multiplier.v | Icarus Verilog | 1.84 | 37.77B | 69.59B | 44.27B | 96.21% | 27.92% | 1.21B | 1.61% |
| log2.v | rx-prop | 1.45 | 33.42B | 48.34B | 20.52B | 90.19% | 62.34% | 763.87M | 7.68% |
| log2.v | rx-sweep (Linear) | 2.53 | 367.74M | 931.65M | 334.31M | 92.76% | 83.11% | 4.10M | 4.62% |
| log2.v | rx-oop (OOP Engine) | 0.98 | 52.69B | 51.74B | 43.14B | 94.34% | 46.30% | 1.31B | 9.27% |
| log2.v | Icarus Verilog | 1.83 | 175.43B | 320.35B | 205.54B | 96.13% | 21.63% | 6.24B | 1.50% |
| mem_ctrl.v | rx-prop | 1.46 | 1.06B | 1.54B | 625.35M | 89.38% | 47.44% | 34.95M | 5.37% |
| mem_ctrl.v | rx-sweep (Linear) | 2.17 | 662.77M | 1.44B | 546.51M | 92.22% | 75.55% | 10.45M | 5.46% |
| mem_ctrl.v | rx-oop (OOP Engine) | 1.11 | 1.70B | 1.89B | 1.43B | 93.65% | 38.48% | 55.90M | 6.26% |
| mem_ctrl.v | Icarus Verilog | 1.75 | 8.49B | 14.82B | 8.50B | 95.97% | 19.64% | 275.79M | 0.99% |
| div.v | rx-prop | 1.67 | 1.83B | 3.05B | 1.17B | 89.73% | 55.89% | 52.38M | 4.65% |
| div.v | rx-sweep (Linear) | 3.31 | 553.51M | 1.83B | 603.16M | 92.35% | 83.00% | 7.89M | 1.82% |
| div.v | rx-oop (OOP Engine) | 1.21 | 2.48B | 3.01B | 2.11B | 93.22% | 48.99% | 73.63M | 5.05% |
| div.v | Icarus Verilog | 1.62 | 13.22B | 21.43B | 11.70B | 95.39% | 39.67% | 324.45M | 0.79% |
