# Master Test Unified Benchmark Report: tests/IWLS2005/itc99

**Execution Parameters:**
- **Target Suite / Path:** `tests/IWLS2005/itc99`
- **Circuits Benchmarked:** 21
- **Simulation Vectors (Phase 3):** 10,000 (Warmup: 10)
- **Verification Vectors (Phase 2):** 100
- **Hardware Profiler:** Linux `perf` kernel PMU counters

---

## 1. Zero-Testbench Memory Footprint (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| b02.v | 52 | 0.59 MB (31.9 MB peak) | N/A | 0.40 MB (8.3 MB peak) | 0.73 MB (4.4 MB peak) |
| b01.v | 101 | 0.65 MB (32.0 MB peak) | N/A | 0.54 MB (8.4 MB peak) | 0.69 MB (4.4 MB peak) |
| b06.v | 100 | 0.69 MB (32.1 MB peak) | N/A | 0.62 MB (8.5 MB peak) | 0.71 MB (4.4 MB peak) |
| b08.v | 309 | 3.04 MB (34.4 MB peak) | N/A | 1.27 MB (9.1 MB peak) | 0.71 MB (4.4 MB peak) |
| b09.v | 331 | 1.19 MB (32.5 MB peak) | N/A | 1.29 MB (9.2 MB peak) | 0.70 MB (4.4 MB peak) |
| b10.v | 417 | 1.11 MB (32.5 MB peak) | N/A | 1.50 MB (9.3 MB peak) | 0.72 MB (4.4 MB peak) |
| b03.v | 549 | 1.45 MB (32.8 MB peak) | N/A | 1.81 MB (9.6 MB peak) | 0.70 MB (4.4 MB peak) |
| b13.v | 540 | 3.77 MB (35.1 MB peak) | N/A | 2.15 MB (10.0 MB peak) | 0.74 MB (4.4 MB peak) |
| b07.v | 859 | 2.03 MB (33.3 MB peak) | N/A | 3.08 MB (10.9 MB peak) | 0.73 MB (4.4 MB peak) |
| b11.v | 1,046 | 1.91 MB (33.2 MB peak) | N/A | 3.21 MB (11.1 MB peak) | 0.81 MB (4.4 MB peak) |
| b04.v | 1,259 | 2.63 MB (33.9 MB peak) | N/A | 3.79 MB (11.7 MB peak) | 0.75 MB (4.4 MB peak) |
| b05.v | 1,292 | 4.17 MB (35.4 MB peak) | N/A | 3.87 MB (11.7 MB peak) | 0.75 MB (4.4 MB peak) |
| b12.v | 2,937 | 6.91 MB (38.2 MB peak) | N/A | 8.76 MB (16.7 MB peak) | 0.80 MB (4.5 MB peak) |
| b14.v | 10,624 | 15.96 MB (48.0 MB peak) | N/A | 36.96 MB (44.7 MB peak) | 1.04 MB (4.7 MB peak) |
| b15.v | 17,594 | 25.92 MB (58.1 MB peak) | N/A | 56.83 MB (64.7 MB peak) | 1.14 MB (4.9 MB peak) |
| b21.v | 23,092 | 29.44 MB (63.7 MB peak) | N/A | 78.68 MB (86.4 MB peak) | 1.25 MB (5.0 MB peak) |
| b20.v | 23,839 | 29.44 MB (64.1 MB peak) | N/A | 79.87 MB (87.8 MB peak) | 1.16 MB (4.9 MB peak) |
| b22.v | 34,903 | 39.43 MB (76.9 MB peak) | N/A | 119.04 MB (126.9 MB peak) | 1.27 MB (5.0 MB peak) |
| b17.v | 52,250 | 59.71 MB (94.8 MB peak) | N/A | 173.07 MB (180.9 MB peak) | 1.33 MB (5.0 MB peak) |
| b18.v | 132,940 | 138.13 MB (187.1 MB peak) | N/A | 429.16 MB (436.9 MB peak) | 2.30 MB (6.0 MB peak) |
| b19.v | 257,489 | 269.66 MB (338.1 MB peak) | N/A | 828.45 MB (836.3 MB peak) | 3.32 MB (7.0 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| b02.v | 52 | 0.53 ms (0.017 ms opt) | N/A | 5.65 ms | 3.58 s |
| b01.v | 101 | 0.57 ms (0.028 ms opt) | N/A | 6.85 ms | 3.60 s |
| b06.v | 100 | 8.24 ms (0.057 ms opt) | N/A | 7.11 ms | 3.59 s |
| b08.v | 309 | 9.20 ms (0.076 ms opt) | N/A | 10.27 ms | 3.61 s |
| b09.v | 331 | 8.81 ms (0.099 ms opt) | N/A | 10.70 ms | 3.63 s |
| b10.v | 417 | 8.71 ms (0.092 ms opt) | N/A | 11.66 ms | 3.64 s |
| b03.v | 549 | 9.00 ms (0.126 ms opt) | N/A | 14.22 ms | 3.68 s |
| b13.v | 540 | 9.75 ms (0.159 ms opt) | N/A | 15.37 ms | 3.69 s |
| b07.v | 859 | 9.60 ms (0.197 ms opt) | N/A | 24.83 ms | 3.72 s |
| b11.v | 1,046 | 9.54 ms (0.188 ms opt) | N/A | 22.40 ms | 3.68 s |
| b04.v | 1,259 | 10.22 ms (0.264 ms opt) | N/A | 25.76 ms | 3.74 s |
| b05.v | 1,292 | 10.47 ms (0.252 ms opt) | N/A | 26.32 ms | 3.74 s |
| b12.v | 2,937 | 12.80 ms (0.546 ms opt) | N/A | 54.34 ms | 4.15 s |
| b14.v | 10,624 | 23.21 ms (2.032 ms opt) | N/A | 232.19 ms | 8.10 s |
| b15.v | 17,594 | 37.61 ms (3.740 ms opt) | N/A | 382.36 ms | 10.96 s |
| b21.v | 23,092 | 41.63 ms (5.531 ms opt) | N/A | 549.57 ms | 13.22 s |
| b20.v | 23,839 | 42.65 ms (5.862 ms opt) | N/A | 544.72 ms | 13.29 s |
| b22.v | 34,903 | 60.34 ms (11.031 ms opt) | N/A | 809.80 ms | 19.77 s |
| b17.v | 52,250 | 96.62 ms (21.482 ms opt) | N/A | 1.20 s | 28.56 s |
| b18.v | 132,940 | 333.00 ms (62.686 ms opt) | N/A | 3.07 s | 82.79 s |
| b19.v | 257,489 | 709.12 ms (133.535 ms opt) | N/A | 6.00 s | 204.14 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| b02.v | 6.63 ms | 5.82 ms | 6.17 ms | N/A | 42.65 ms | 1.25 ms |
| b01.v | 8.50 ms | 8.68 ms | 8.59 ms | N/A | 53.76 ms | 1.35 ms |
| b06.v | 12.80 ms | 11.55 ms | 13.79 ms | N/A | 45.45 ms | 2.71 ms |
| b08.v | 18.66 ms | 25.09 ms | 22.42 ms | N/A | 73.52 ms | 6.85 ms |
| b09.v | 20.64 ms | 27.15 ms | 24.16 ms | N/A | 70.91 ms | 5.39 ms |
| b10.v | 26.05 ms | 28.91 ms | 29.24 ms | N/A | 122.24 ms | 7.80 ms |
| b03.v | 34.95 ms | 43.20 ms | 37.26 ms | N/A | 78.16 ms | 7.41 ms |
| b13.v | 42.36 ms | 55.13 ms | 50.50 ms | N/A | 105.80 ms | 12.07 ms |
| b07.v | 40.52 ms | 56.02 ms | 47.26 ms | N/A | 83.78 ms | 11.36 ms |
| b11.v | 48.39 ms | 56.27 ms | 56.88 ms | N/A | 112.44 ms | 13.65 ms |
| b04.v | 115.29 ms | 124.52 ms | 120.96 ms | N/A | 405.31 ms | 23.21 ms |
| b05.v | 28.46 ms | 50.15 ms | 33.23 ms | N/A | 56.30 ms | 15.10 ms |
| b12.v | 108.75 ms | 143.89 ms | 109.16 ms | N/A | 255.71 ms | 38.10 ms |
| b14.v | 1453.55 ms | 876.79 ms | 1471.10 ms | N/A | 1932.04 ms | 131.00 ms |
| b15.v | 541.82 ms | 758.32 ms | 684.27 ms | N/A | 1587.27 ms | 209.79 ms |
| b21.v | 1803.68 ms | 1267.85 ms | 2012.35 ms | N/A | 2515.67 ms | 319.20 ms |
| b20.v | 2290.01 ms | 1513.76 ms | 2281.37 ms | N/A | 2942.70 ms | 321.19 ms |
| b22.v | 4226.43 ms | 2666.06 ms | 4542.30 ms | N/A | 5990.82 ms | 697.41 ms |
| b17.v | 1926.04 ms | 2301.71 ms | 2645.34 ms | N/A | 3909.87 ms | 1674.66 ms |
| b18.v | 7391.53 ms | 6215.95 ms | 8817.53 ms | N/A | 26.37 s | 8397.23 ms |
| b19.v | 11.60 s | 11.22 s | 14.90 s | N/A | 41.26 s | 20.11 s |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| b02.v | 6.43x | 7.33x | 6.91x | N/A | 1.00x | 34.12x |
| b01.v | 6.33x | 6.19x | 6.26x | N/A | 1.00x | 39.80x |
| b06.v | 3.55x | 3.93x | 3.30x | N/A | 1.00x | 16.75x |
| b08.v | 3.94x | 2.93x | 3.28x | N/A | 1.00x | 10.73x |
| b09.v | 3.44x | 2.61x | 2.94x | N/A | 1.00x | 13.16x |
| b10.v | 4.69x | 4.23x | 4.18x | N/A | 1.00x | 15.67x |
| b03.v | 2.24x | 1.81x | 2.10x | N/A | 1.00x | 10.55x |
| b13.v | 2.50x | 1.92x | 2.09x | N/A | 1.00x | 8.76x |
| b07.v | 2.07x | 1.50x | 1.77x | N/A | 1.00x | 7.37x |
| b11.v | 2.32x | 2.00x | 1.98x | N/A | 1.00x | 8.24x |
| b04.v | 3.52x | 3.25x | 3.35x | N/A | 1.00x | 17.46x |
| b05.v | 1.98x | 1.12x | 1.69x | N/A | 1.00x | 3.73x |
| b12.v | 2.35x | 1.78x | 2.34x | N/A | 1.00x | 6.71x |
| b14.v | 1.33x | 2.20x | 1.31x | N/A | 1.00x | 14.75x |
| b15.v | 2.93x | 2.09x | 2.32x | N/A | 1.00x | 7.57x |
| b21.v | 1.39x | 1.98x | 1.25x | N/A | 1.00x | 7.88x |
| b20.v | 1.29x | 1.94x | 1.29x | N/A | 1.00x | 9.16x |
| b22.v | 1.42x | 2.25x | 1.32x | N/A | 1.00x | 8.59x |
| b17.v | 2.03x | 1.70x | 1.48x | N/A | 1.00x | 2.33x |
| b18.v | 3.57x | 4.24x | 2.99x | N/A | 1.00x | 3.14x |
| b19.v | 3.56x | 3.68x | 2.77x | N/A | 1.00x | 2.05x |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `2.69x`
- **rx-sweep (Linear Compiled):** `2.57x`
- **rx-oop (OOP Graph):** `2.40x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `9.07x`

### Cross-Engine Comparisons

- **Reactor Sweep vs Propagate Ratio:** `0.96x` (propagate faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | IPC | Cycles | Instructions | L1 Loads | L1 Hit% | L2 Hit% | LLC Misses | Brn Miss% |
|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| b02.v | rx-prop | 4.87 | 21.04M | 102.47M | 30.04M | 99.64% | 88.51% | 12.01K | 0.26% |
| b02.v | rx-sweep (Linear) | 6.25 | 9.89M | 61.76M | 10.07M | 99.95% | 96.56% | 179 | 0.34% |
| b02.v | rx-oop (OOP Engine) | 7.57 | 6.29M | 47.61M | 10.20M | 99.94% | 95.87% | 5.82K | 0.25% |
| b02.v | Icarus Verilog | 3.77 | 131.21M | 494.31M | 230.09M | 99.82% | 91.21% | 32.73K | 0.78% |
| b01.v | rx-prop | 5.88 | 17.52M | 103.04M | 25.11M | 99.93% | 77.62% | 3.79K | 0.31% |
| b01.v | rx-sweep (Linear) | 4.97 | 21.06M | 104.63M | 29.21M | 99.93% | 82.37% | 3.79K | 0.47% |
| b01.v | rx-oop (OOP Engine) | 5.10 | 22.09M | 112.68M | 36.31M | 99.63% | 86.83% | 19.25K | 0.27% |
| b01.v | Icarus Verilog | 3.73 | 161.18M | 600.53M | 270.41M | 99.45% | 97.52% | 32.30K | 0.87% |
| b06.v | rx-prop | 5.66 | 20.92M | 118.36M | 39.63M | 99.84% | 92.40% | 5.11K | 0.29% |
| b06.v | rx-sweep (Linear) | 5.66 | 23.47M | 132.80M | 36.40M | 99.81% | 94.07% | 4.09K | 0.34% |
| b06.v | rx-oop (OOP Engine) | 4.98 | 27.77M | 138.34M | 38.28M | 99.78% | 98.08% | 7.46K | 0.32% |
| b06.v | Icarus Verilog | 4.39 | 132.82M | 582.96M | 258.75M | 99.62% | 98.20% | 18.09K | 0.63% |
| b08.v | rx-prop | 4.48 | 44.18M | 198.12M | 65.03M | 99.42% | 99.70% | 1.16K | 0.67% |
| b08.v | rx-sweep (Linear) | 4.14 | 65.43M | 271.12M | 83.18M | 98.92% | 99.46% | 5.18K | 0.85% |
| b08.v | rx-oop (OOP Engine) | 4.18 | 49.26M | 205.67M | 61.96M | 97.98% | 99.45% | 10.57K | 0.84% |
| b08.v | Icarus Verilog | 4.02 | 229.20M | 921.32M | 390.33M | 98.22% | 99.40% | 46.15K | 0.77% |
| b09.v | rx-prop | 4.85 | 49.40M | 239.63M | 67.00M | 99.32% | 99.87% | 4.24K | 0.31% |
| b09.v | rx-sweep (Linear) | 4.53 | 66.59M | 301.37M | 87.29M | 98.06% | 99.75% | 4.83K | 0.37% |
| b09.v | rx-oop (OOP Engine) | 4.03 | 60.25M | 242.62M | 73.25M | 97.97% | 99.64% | 6.31K | 0.38% |
| b09.v | Icarus Verilog | 4.15 | 225.76M | 936.94M | 413.56M | 96.69% | 99.68% | 51.73K | 0.45% |
| b10.v | rx-prop | 3.89 | 65.88M | 256.44M | 89.57M | 98.77% | 99.70% | 3.32K | 1.44% |
| b10.v | rx-sweep (Linear) | 3.99 | 75.69M | 302.13M | 92.52M | 98.30% | 99.37% | 6.17K | 1.23% |
| b10.v | rx-oop (OOP Engine) | 3.71 | 69.37M | 257.23M | 82.04M | 97.07% | 99.45% | 12.85K | 1.73% |
| b10.v | Icarus Verilog | 3.85 | 377.73M | 1.45B | 650.27M | 97.02% | 99.68% | 56.33K | 0.72% |
| b03.v | rx-prop | 4.24 | 88.21M | 373.99M | 115.06M | 97.11% | 99.92% | 2.16K | 0.56% |
| b03.v | rx-sweep (Linear) | 3.90 | 118.64M | 462.69M | 136.14M | 93.71% | 99.90% | 8.67K | 0.81% |
| b03.v | rx-oop (OOP Engine) | 3.93 | 99.62M | 391.35M | 121.48M | 94.66% | 99.85% | 4.08K | 0.67% |
| b03.v | Icarus Verilog | 3.82 | 256.49M | 980.20M | 444.00M | 96.82% | 99.34% | 98.73K | 0.70% |
| b13.v | rx-prop | 4.09 | 110.03M | 450.34M | 143.54M | 95.45% | 99.91% | 5.69K | 0.29% |
| b13.v | rx-sweep (Linear) | 4.13 | 146.36M | 604.28M | 179.57M | 90.61% | 99.95% | 7.87K | 0.51% |
| b13.v | rx-oop (OOP Engine) | 3.54 | 124.94M | 442.10M | 138.60M | 89.70% | 99.95% | 7.11K | 0.35% |
| b13.v | Icarus Verilog | 3.91 | 341.63M | 1.33B | 597.61M | 96.72% | 99.48% | 115.99K | 0.66% |
| b07.v | rx-prop | 4.25 | 110.36M | 468.89M | 150.92M | 96.14% | 99.78% | 12.87K | 0.19% |
| b07.v | rx-sweep (Linear) | 4.14 | 149.20M | 617.59M | 175.84M | 89.44% | 99.94% | 9.35K | 0.47% |
| b07.v | rx-oop (OOP Engine) | 3.99 | 109.73M | 438.31M | 130.23M | 89.91% | 99.85% | 26.05K | 0.25% |
| b07.v | Icarus Verilog | 3.94 | 307.65M | 1.21B | 534.23M | 96.09% | 99.58% | 87.92K | 0.49% |
| b11.v | rx-prop | 3.62 | 131.50M | 475.86M | 153.03M | 96.60% | 99.90% | 6.85K | 1.51% |
| b11.v | rx-sweep (Linear) | 3.57 | 151.25M | 540.26M | 165.80M | 89.05% | 99.97% | 4.24K | 1.04% |
| b11.v | rx-oop (OOP Engine) | 3.25 | 150.36M | 488.67M | 163.32M | 92.70% | 99.85% | 14.70K | 1.92% |
| b11.v | Icarus Verilog | 3.50 | 393.18M | 1.38B | 615.47M | 97.11% | 99.62% | 60.44K | 0.88% |
| b04.v | rx-prop | 2.85 | 309.82M | 883.82M | 302.92M | 92.20% | 99.92% | 22.22K | 2.98% |
| b04.v | rx-sweep (Linear) | 3.26 | 338.76M | 1.11B | 350.62M | 89.68% | 99.91% | 31.55K | 1.95% |
| b04.v | rx-oop (OOP Engine) | 2.69 | 331.30M | 892.10M | 318.22M | 86.95% | 99.91% | 33.37K | 3.28% |
| b04.v | Icarus Verilog | 3.31 | 1.22B | 4.05B | 1.94B | 96.89% | 98.95% | 648.50K | 1.06% |
| b05.v | rx-prop | 4.87 | 68.88M | 335.74M | 97.87M | 98.02% | 99.80% | 4.47K | 0.21% |
| b05.v | rx-sweep (Linear) | 4.07 | 127.89M | 520.98M | 154.42M | 86.72% | 99.97% | 6.27K | 0.43% |
| b05.v | rx-oop (OOP Engine) | 4.40 | 68.23M | 300.52M | 90.00M | 89.72% | 99.85% | 15.88K | 0.32% |
| b05.v | Icarus Verilog | 3.70 | 254.18M | 940.13M | 385.64M | 96.31% | 99.24% | 129.01K | 0.65% |
| b12.v | rx-prop | 3.63 | 290.65M | 1.06B | 327.72M | 87.15% | 99.96% | 18.68K | 0.35% |
| b12.v | rx-sweep (Linear) | 4.12 | 393.63M | 1.62B | 474.66M | 84.76% | 99.98% | 11.46K | 0.37% |
| b12.v | rx-oop (OOP Engine) | 3.57 | 292.11M | 1.04B | 335.06M | 85.09% | 99.91% | 43.34K | 0.39% |
| b12.v | Icarus Verilog | 3.61 | 918.15M | 3.31B | 1.48B | 95.84% | 97.57% | 1.47M | 0.66% |
| b14.v | rx-prop | 2.03 | 4.00B | 8.12B | 3.00B | 89.96% | 94.01% | 18.05M | 6.10% |
| b14.v | rx-sweep (Linear) | 2.53 | 2.41B | 6.09B | 2.08B | 87.78% | 92.93% | 17.94M | 3.45% |
| b14.v | rx-oop (OOP Engine) | 1.89 | 4.04B | 7.65B | 2.98B | 88.11% | 87.43% | 44.47M | 6.04% |
| b14.v | Icarus Verilog | 2.77 | 6.25B | 17.32B | 8.77B | 95.59% | 78.06% | 84.33M | 1.10% |
| b15.v | rx-prop | 3.46 | 1.50B | 5.18B | 1.65B | 87.13% | 96.68% | 7.06M | 0.68% |
| b15.v | rx-sweep (Linear) | 3.61 | 2.05B | 7.40B | 2.23B | 84.45% | 92.64% | 25.55M | 0.71% |
| b15.v | rx-oop (OOP Engine) | 2.79 | 1.88B | 5.23B | 1.73B | 85.51% | 87.16% | 32.37M | 0.76% |
| b15.v | Icarus Verilog | 3.14 | 5.87B | 18.44B | 8.34B | 95.66% | 67.06% | 119.24M | 0.61% |
| b21.v | rx-prop | 2.10 | 4.96B | 10.41B | 3.78B | 89.28% | 88.46% | 46.69M | 5.13% |
| b21.v | rx-sweep (Linear) | 2.82 | 3.45B | 9.74B | 3.15B | 85.76% | 89.87% | 45.51M | 2.09% |
| b21.v | rx-oop (OOP Engine) | 1.85 | 5.50B | 10.17B | 3.89B | 87.81% | 74.97% | 118.75M | 5.19% |
| b21.v | Icarus Verilog | 2.74 | 8.88B | 24.35B | 11.99B | 95.58% | 70.16% | 158.39M | 0.99% |
| b20.v | rx-prop | 1.96 | 6.30B | 12.37B | 4.60B | 89.34% | 87.52% | 61.01M | 5.90% |
| b20.v | rx-sweep (Linear) | 2.60 | 4.16B | 10.82B | 3.62B | 86.30% | 89.65% | 51.36M | 2.65% |
| b20.v | rx-oop (OOP Engine) | 1.74 | 6.24B | 10.88B | 4.24B | 87.89% | 73.75% | 134.78M | 5.66% |
| b20.v | Icarus Verilog | 2.63 | 10.20B | 26.80B | 13.47B | 95.58% | 70.46% | 175.89M | 1.05% |
| b22.v | rx-prop | 1.70 | 11.59B | 19.65B | 7.59B | 89.29% | 78.75% | 172.57M | 7.11% |
| b22.v | rx-sweep (Linear) | 2.32 | 7.30B | 16.92B | 5.89B | 87.28% | 86.68% | 99.92M | 3.52% |
| b22.v | rx-oop (OOP Engine) | 1.53 | 12.47B | 19.10B | 7.68B | 87.84% | 67.97% | 299.59M | 6.81% |
| b22.v | Icarus Verilog | 2.29 | 19.68B | 45.10B | 23.99B | 95.52% | 56.32% | 470.08M | 1.19% |
| b17.v | rx-prop | 2.92 | 5.26B | 15.34B | 4.96B | 87.11% | 80.31% | 126.05M | 0.92% |
| b17.v | rx-sweep (Linear) | 3.52 | 6.28B | 22.13B | 6.74B | 84.87% | 93.74% | 63.91M | 0.79% |
| b17.v | rx-oop (OOP Engine) | 2.12 | 7.19B | 15.23B | 5.12B | 85.42% | 56.67% | 323.21M | 1.01% |
| b17.v | Icarus Verilog | 2.45 | 15.45B | 37.82B | 17.69B | 94.52% | 56.18% | 424.72M | 0.70% |
| b18.v | rx-prop | 2.12 | 20.29B | 43.09B | 15.23B | 88.54% | 70.01% | 524.25M | 3.57% |
| b18.v | rx-sweep (Linear) | 3.17 | 17.11B | 54.23B | 16.95B | 85.31% | 89.93% | 250.76M | 1.13% |
| b18.v | rx-oop (OOP Engine) | 1.78 | 24.18B | 43.15B | 15.93B | 86.93% | 54.26% | 952.32M | 3.57% |
| b18.v | Icarus Verilog | 2.07 | 19.27B | 39.81B | 18.60B | 94.77% | 77.39% | 220.08M | 1.43% |
| b19.v | rx-prop | 2.33 | 31.83B | 74.19B | 24.99B | 87.69% | 64.48% | 1.09B | 2.17% |
| b19.v | rx-sweep (Linear) | 3.37 | 30.82B | 104.00B | 31.55B | 84.78% | 89.00% | 527.79M | 0.77% |
| b19.v | rx-oop (OOP Engine) | 1.82 | 40.80B | 74.30B | 26.37B | 86.12% | 46.90% | 1.94B | 2.18% |
| b19.v | Icarus Verilog | 1.82 | 35.66B | 64.85B | 28.78B | 94.39% | 76.04% | 387.87M | 1.37% |
