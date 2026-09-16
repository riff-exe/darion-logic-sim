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
| b02.v | 52 | 0.51 MB (31.9 MB peak) | N/A | 0.47 MB (8.3 MB peak) | 0.73 MB (4.4 MB peak) |
| b01.v | 101 | 0.65 MB (31.8 MB peak) | N/A | 0.66 MB (8.4 MB peak) | 0.75 MB (4.4 MB peak) |
| b06.v | 100 | 0.62 MB (32.0 MB peak) | N/A | 0.55 MB (8.4 MB peak) | 0.71 MB (4.4 MB peak) |
| b08.v | 309 | 1.07 MB (32.4 MB peak) | N/A | 1.14 MB (9.0 MB peak) | 0.70 MB (4.4 MB peak) |
| b09.v | 331 | 1.13 MB (32.6 MB peak) | N/A | 1.36 MB (9.2 MB peak) | 0.64 MB (4.3 MB peak) |
| b10.v | 417 | 1.01 MB (32.4 MB peak) | N/A | 1.44 MB (9.2 MB peak) | 0.62 MB (4.3 MB peak) |
| b03.v | 549 | 1.39 MB (32.8 MB peak) | N/A | 1.79 MB (9.6 MB peak) | 0.71 MB (4.4 MB peak) |
| b13.v | 540 | 1.75 MB (33.1 MB peak) | N/A | 2.17 MB (10.0 MB peak) | 0.72 MB (4.4 MB peak) |
| b07.v | 859 | 1.96 MB (33.3 MB peak) | N/A | 3.13 MB (10.9 MB peak) | 0.73 MB (4.4 MB peak) |
| b11.v | 1,046 | 1.93 MB (33.1 MB peak) | N/A | 3.27 MB (11.1 MB peak) | 0.74 MB (4.4 MB peak) |
| b04.v | 1,259 | 4.49 MB (35.9 MB peak) | N/A | 3.82 MB (11.6 MB peak) | 0.75 MB (4.4 MB peak) |
| b05.v | 1,292 | 2.12 MB (33.5 MB peak) | N/A | 3.86 MB (11.8 MB peak) | 0.76 MB (4.4 MB peak) |
| b12.v | 2,937 | 6.80 MB (38.2 MB peak) | N/A | 8.79 MB (16.6 MB peak) | 0.77 MB (4.5 MB peak) |
| b14.v | 10,624 | 14.68 MB (46.9 MB peak) | N/A | 36.88 MB (44.7 MB peak) | 0.93 MB (4.6 MB peak) |
| b15.v | 17,594 | 24.47 MB (56.7 MB peak) | N/A | 56.71 MB (64.6 MB peak) | 1.16 MB (4.8 MB peak) |
| b21.v | 23,092 | 28.05 MB (62.3 MB peak) | N/A | 78.52 MB (86.4 MB peak) | 1.14 MB (4.8 MB peak) |
| b20.v | 23,839 | 28.23 MB (62.6 MB peak) | N/A | 79.95 MB (87.7 MB peak) | 1.32 MB (4.9 MB peak) |
| b22.v | 34,903 | 38.16 MB (76.0 MB peak) | N/A | 119.04 MB (126.9 MB peak) | 1.38 MB (5.1 MB peak) |
| b17.v | 52,250 | 58.80 MB (94.2 MB peak) | N/A | 172.93 MB (180.8 MB peak) | 1.46 MB (5.2 MB peak) |
| b18.v | 132,940 | 138.23 MB (187.3 MB peak) | N/A | 429.04 MB (436.9 MB peak) | 2.30 MB (6.0 MB peak) |
| b19.v | 257,489 | 268.13 MB (336.1 MB peak) | N/A | 828.22 MB (836.1 MB peak) | 3.20 MB (6.9 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| b02.v | 52 | 0.38 ms (0.013 ms opt) | N/A | 4.24 ms | 2.59 s |
| b01.v | 101 | 0.59 ms (0.025 ms opt) | N/A | 4.72 ms | 2.60 s |
| b06.v | 100 | 8.32 ms (0.023 ms opt) | N/A | 4.65 ms | 2.63 s |
| b08.v | 309 | 1.20 ms (0.060 ms opt) | N/A | 8.17 ms | 2.62 s |
| b09.v | 331 | 8.48 ms (0.068 ms opt) | N/A | 7.77 ms | 2.63 s |
| b10.v | 417 | 0.95 ms (0.068 ms opt) | N/A | 8.10 ms | 2.60 s |
| b03.v | 549 | 8.72 ms (0.115 ms opt) | N/A | 9.80 ms | 2.68 s |
| b13.v | 540 | 8.89 ms (0.115 ms opt) | N/A | 11.07 ms | 2.68 s |
| b07.v | 859 | 9.42 ms (0.185 ms opt) | N/A | 17.20 ms | 2.71 s |
| b11.v | 1,046 | 9.08 ms (0.165 ms opt) | N/A | 16.60 ms | 2.67 s |
| b04.v | 1,259 | 9.54 ms (0.191 ms opt) | N/A | 18.62 ms | 2.74 s |
| b05.v | 1,292 | 9.47 ms (0.174 ms opt) | N/A | 19.38 ms | 2.75 s |
| b12.v | 2,937 | 11.26 ms (0.365 ms opt) | N/A | 41.00 ms | 3.07 s |
| b14.v | 10,624 | 19.06 ms (1.410 ms opt) | N/A | 180.10 ms | 6.37 s |
| b15.v | 17,594 | 26.93 ms (2.857 ms opt) | N/A | 306.51 ms | 8.81 s |
| b21.v | 23,092 | 32.73 ms (4.934 ms opt) | N/A | 413.18 ms | 10.83 s |
| b20.v | 23,839 | 32.78 ms (4.874 ms opt) | N/A | 426.04 ms | 11.17 s |
| b22.v | 34,903 | 47.72 ms (10.236 ms opt) | N/A | 639.13 ms | 16.52 s |
| b17.v | 52,250 | 72.70 ms (18.614 ms opt) | N/A | 959.76 ms | 23.85 s |
| b18.v | 132,940 | 267.81 ms (57.088 ms opt) | N/A | 2.45 s | 70.54 s |
| b19.v | 257,489 | 606.24 ms (127.086 ms opt) | N/A | 4.89 s | 166.17 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| b02.v | 4.52 ms | 4.36 ms | 6.22 ms | N/A | 30.28 ms | 0.78 ms |
| b01.v | 6.26 ms | 5.63 ms | 10.06 ms | N/A | 36.56 ms | 1.12 ms |
| b06.v | 8.24 ms | 8.45 ms | 13.38 ms | N/A | 31.75 ms | 2.13 ms |
| b08.v | 12.44 ms | 17.23 ms | 20.46 ms | N/A | 51.54 ms | 4.82 ms |
| b09.v | 14.17 ms | 18.45 ms | 20.35 ms | N/A | 49.27 ms | 3.49 ms |
| b10.v | 18.01 ms | 19.89 ms | 31.99 ms | N/A | 84.64 ms | 5.49 ms |
| b03.v | 24.24 ms | 29.87 ms | 41.63 ms | N/A | 55.16 ms | 5.35 ms |
| b13.v | 28.76 ms | 38.37 ms | 40.13 ms | N/A | 74.60 ms | 9.00 ms |
| b07.v | 27.93 ms | 37.57 ms | 38.90 ms | N/A | 58.65 ms | 8.09 ms |
| b11.v | 33.37 ms | 38.84 ms | 63.03 ms | N/A | 79.54 ms | 9.56 ms |
| b04.v | 80.10 ms | 85.48 ms | 115.99 ms | N/A | 284.24 ms | 14.98 ms |
| b05.v | 21.15 ms | 36.63 ms | 34.25 ms | N/A | 38.98 ms | 9.99 ms |
| b12.v | 74.06 ms | 100.45 ms | 95.22 ms | N/A | 178.46 ms | 33.12 ms |
| b14.v | 982.81 ms | 592.20 ms | 1471.24 ms | N/A | 1356.56 ms | 92.17 ms |
| b15.v | 372.84 ms | 515.20 ms | 613.04 ms | N/A | 1248.13 ms | 139.41 ms |
| b21.v | 1238.03 ms | 874.44 ms | 1894.29 ms | N/A | 1739.67 ms | 206.12 ms |
| b20.v | 1565.46 ms | 1037.40 ms | 2112.28 ms | N/A | 2013.93 ms | 220.28 ms |
| b22.v | 2866.47 ms | 1817.48 ms | 4171.92 ms | N/A | 4122.46 ms | 449.08 ms |
| b17.v | 1306.15 ms | 1564.87 ms | 2071.56 ms | N/A | 2680.28 ms | 1191.11 ms |
| b18.v | 5029.58 ms | 4245.01 ms | 7058.85 ms | N/A | 21.06 s | 5615.75 ms |
| b19.v | 8163.51 ms | 7978.28 ms | 11.38 s | N/A | 31.96 s | 13.02 s |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| b02.v | 6.70x | 6.94x | 4.87x | N/A | 1.00x | 38.81x |
| b01.v | 5.84x | 6.50x | 3.63x | N/A | 1.00x | 32.69x |
| b06.v | 3.85x | 3.76x | 2.37x | N/A | 1.00x | 14.91x |
| b08.v | 4.14x | 2.99x | 2.52x | N/A | 1.00x | 10.69x |
| b09.v | 3.48x | 2.67x | 2.42x | N/A | 1.00x | 14.12x |
| b10.v | 4.70x | 4.26x | 2.65x | N/A | 1.00x | 15.41x |
| b03.v | 2.28x | 1.85x | 1.32x | N/A | 1.00x | 10.30x |
| b13.v | 2.59x | 1.94x | 1.86x | N/A | 1.00x | 8.29x |
| b07.v | 2.10x | 1.56x | 1.51x | N/A | 1.00x | 7.25x |
| b11.v | 2.38x | 2.05x | 1.26x | N/A | 1.00x | 8.32x |
| b04.v | 3.55x | 3.33x | 2.45x | N/A | 1.00x | 18.98x |
| b05.v | 1.84x | 1.06x | 1.14x | N/A | 1.00x | 3.90x |
| b12.v | 2.41x | 1.78x | 1.87x | N/A | 1.00x | 5.39x |
| b14.v | 1.38x | 2.29x | 0.92x | N/A | 1.00x | 14.72x |
| b15.v | 3.35x | 2.42x | 2.04x | N/A | 1.00x | 8.95x |
| b21.v | 1.41x | 1.99x | 0.92x | N/A | 1.00x | 8.44x |
| b20.v | 1.29x | 1.94x | 0.95x | N/A | 1.00x | 9.14x |
| b22.v | 1.44x | 2.27x | 0.99x | N/A | 1.00x | 9.18x |
| b17.v | 2.05x | 1.71x | 1.29x | N/A | 1.00x | 2.25x |
| b18.v | 4.19x | 4.96x | 2.98x | N/A | 1.00x | 3.75x |
| b19.v | 3.91x | 4.01x | 2.81x | N/A | 1.00x | 2.46x |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `2.77x`
- **rx-sweep (Linear Compiled):** `2.64x`
- **rx-oop (OOP Graph):** `1.82x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `9.20x`

### Cross-Engine Comparisons

- **Reactor Sweep vs Propagate Ratio:** `0.95x` (propagate faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | IPC | Cycles | Instructions | L1 Loads | L1 Hit% | L2 Hit% | LLC Misses | Brn Miss% |
|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| b02.v | rx-prop | 49.42 | 849.95K | 42.00M | 1.09M | 99.72% | 62.81% | 4.10K | 0.26% |
| b02.v | rx-sweep (Linear) | 28.84 | 1.51M | 43.48M | 1.05M | 99.33% | 43.62% | 4.12K | 0.35% |
| b02.v | rx-oop (OOP Engine) | 4.71 | 17.30M | 81.45M | 27.58M | 99.94% | 89.87% | 1.70K | 0.61% |
| b02.v | Icarus Verilog | 3.99 | 120.08M | 478.75M | 215.23M | 99.85% | 90.62% | 31.16K | 0.88% |
| b01.v | rx-prop | 8.34 | 8.16M | 68.07M | 13.77M | 99.98% | 56.58% | 1.52K | 0.25% |
| b01.v | rx-sweep (Linear) | 7.66 | 7.96M | 60.98M | 13.32M | 99.99% | 89.18% | 2.84K | 0.47% |
| b01.v | rx-oop (OOP Engine) | 3.11 | 30.61M | 95.22M | 54.17M | 99.88% | 93.53% | 4.87K | 1.60% |
| b01.v | Icarus Verilog | 4.02 | 159.42M | 640.37M | 261.74M | 99.52% | 98.07% | 28.76K | 0.96% |
| b06.v | rx-prop | 4.75 | 31.39M | 149.13M | 53.63M | 99.68% | 96.37% | 6.47K | 0.24% |
| b06.v | rx-sweep (Linear) | 5.62 | 26.01M | 146.22M | 39.29M | 99.88% | 86.91% | 5.80K | 0.43% |
| b06.v | rx-oop (OOP Engine) | 3.27 | 43.40M | 141.98M | 63.65M | 99.84% | 98.79% | 1.21K | 1.22% |
| b06.v | Icarus Verilog | 4.24 | 137.98M | 585.58M | 252.43M | 99.64% | 98.16% | 21.07K | 0.68% |
| b08.v | rx-prop | 4.98 | 34.34M | 171.10M | 53.39M | 99.35% | 98.54% | 5.08K | 0.63% |
| b08.v | rx-sweep (Linear) | 5.12 | 50.78M | 260.01M | 64.93M | 99.21% | 99.52% | 2.52K | 0.85% |
| b08.v | rx-oop (OOP Engine) | 2.79 | 69.12M | 192.65M | 108.39M | 98.70% | 99.53% | 14.07K | 1.55% |
| b08.v | Icarus Verilog | 3.99 | 230.21M | 919.33M | 390.07M | 98.24% | 99.37% | 42.25K | 0.86% |
| b09.v | rx-prop | 5.02 | 49.27M | 247.23M | 68.70M | 99.38% | 99.66% | 1.70K | 0.33% |
| b09.v | rx-sweep (Linear) | 4.37 | 63.84M | 278.73M | 87.87M | 98.35% | 99.69% | 3.99K | 0.39% |
| b09.v | rx-oop (OOP Engine) | 3.33 | 62.86M | 209.42M | 109.75M | 98.46% | 99.52% | 8.37K | 0.49% |
| b09.v | Icarus Verilog | 4.46 | 216.22M | 964.75M | 387.39M | 96.65% | 99.75% | 56.18K | 0.57% |
| b10.v | rx-prop | 4.66 | 57.92M | 269.76M | 70.38M | 98.88% | 99.61% | 3.30K | 1.68% |
| b10.v | rx-sweep (Linear) | 4.20 | 67.74M | 284.49M | 83.22M | 98.26% | 99.67% | 5.69K | 1.20% |
| b10.v | rx-oop (OOP Engine) | 2.27 | 111.52M | 252.94M | 150.58M | 98.21% | 99.55% | 11.94K | 4.09% |
| b10.v | Icarus Verilog | 4.03 | 366.48M | 1.48B | 633.03M | 97.05% | 99.73% | 47.44K | 0.79% |
| b03.v | rx-prop | 4.30 | 87.15M | 375.09M | 110.41M | 97.35% | 99.77% | 9.13K | 0.63% |
| b03.v | rx-sweep (Linear) | 3.96 | 109.84M | 435.17M | 129.28M | 93.66% | 99.99% | 656 | 0.82% |
| b03.v | rx-oop (OOP Engine) | 2.32 | 159.06M | 368.77M | 228.60M | 96.43% | 99.67% | 26.67K | 2.57% |
| b03.v | Icarus Verilog | 4.07 | 238.19M | 968.26M | 414.43M | 96.68% | 99.42% | 81.82K | 0.75% |
| b13.v | rx-prop | 4.23 | 110.98M | 469.35M | 138.46M | 95.78% | 99.96% | 2.33K | 0.29% |
| b13.v | rx-sweep (Linear) | 4.29 | 136.46M | 585.88M | 163.34M | 90.28% | 99.95% | 3.98K | 0.51% |
| b13.v | rx-oop (OOP Engine) | 2.84 | 157.88M | 448.47M | 235.65M | 93.51% | 99.94% | 8.21K | 0.58% |
| b13.v | Icarus Verilog | 4.01 | 324.45M | 1.30B | 577.34M | 96.61% | 99.35% | 128.01K | 0.66% |
| b07.v | rx-prop | 4.45 | 100.11M | 445.68M | 133.07M | 96.17% | 99.88% | 6.27K | 0.20% |
| b07.v | rx-sweep (Linear) | 4.24 | 138.50M | 587.29M | 167.64M | 89.20% | 100.00% | 2.57K | 0.46% |
| b07.v | rx-oop (OOP Engine) | 3.13 | 145.68M | 455.90M | 228.40M | 93.66% | 99.89% | 15.93K | 0.64% |
| b07.v | Icarus Verilog | 3.81 | 321.04M | 1.22B | 537.83M | 96.11% | 99.65% | 77.50K | 0.56% |
| b11.v | rx-prop | 3.94 | 115.74M | 455.73M | 134.34M | 96.48% | 99.80% | 9.63K | 1.53% |
| b11.v | rx-sweep (Linear) | 3.76 | 144.39M | 542.95M | 155.19M | 88.86% | 99.98% | 8.20K | 1.04% |
| b11.v | rx-oop (OOP Engine) | 2.02 | 240.82M | 487.00M | 310.40M | 96.05% | 99.66% | 42.79K | 4.33% |
| b11.v | Icarus Verilog | 3.51 | 385.07M | 1.35B | 617.09M | 97.12% | 99.33% | 115.48K | 0.96% |
| b04.v | rx-prop | 3.07 | 278.98M | 856.26M | 283.85M | 91.88% | 99.90% | 23.12K | 3.22% |
| b04.v | rx-sweep (Linear) | 3.25 | 337.50M | 1.10B | 346.18M | 89.57% | 99.95% | 23.69K | 1.90% |
| b04.v | rx-oop (OOP Engine) | 1.89 | 467.92M | 883.73M | 572.85M | 93.84% | 99.87% | 44.29K | 4.44% |
| b04.v | Icarus Verilog | 3.27 | 1.24B | 4.07B | 1.94B | 96.90% | 98.75% | 761.44K | 1.13% |
| b05.v | rx-prop | 5.23 | 69.12M | 361.69M | 96.51M | 98.06% | 99.56% | 8.14K | 0.29% |
| b05.v | rx-sweep (Linear) | 3.98 | 131.16M | 522.22M | 144.38M | 86.66% | 99.96% | 9.78K | 0.44% |
| b05.v | rx-oop (OOP Engine) | 2.71 | 120.75M | 327.18M | 199.46M | 94.39% | 99.84% | 16.39K | 1.35% |
| b05.v | Icarus Verilog | 3.59 | 255.84M | 917.29M | 401.57M | 96.42% | 99.14% | 117.65K | 0.61% |
| b12.v | rx-prop | 3.63 | 291.32M | 1.06B | 335.35M | 87.24% | 99.93% | 33.21K | 0.35% |
| b12.v | rx-sweep (Linear) | 4.32 | 371.69M | 1.61B | 455.49M | 84.64% | 99.95% | 36.45K | 0.40% |
| b12.v | rx-oop (OOP Engine) | 2.66 | 386.97M | 1.03B | 592.64M | 90.47% | 99.86% | 84.59K | 1.09% |
| b12.v | Icarus Verilog | 3.67 | 895.22M | 3.29B | 1.44B | 95.73% | 97.08% | 1.76M | 0.72% |
| b14.v | rx-prop | 2.05 | 3.95B | 8.10B | 2.99B | 89.88% | 96.08% | 11.90M | 6.15% |
| b14.v | rx-sweep (Linear) | 2.56 | 2.38B | 6.10B | 2.07B | 87.77% | 94.65% | 13.57M | 3.41% |
| b14.v | rx-oop (OOP Engine) | 1.25 | 5.92B | 7.37B | 5.70B | 93.54% | 87.94% | 44.41M | 8.56% |
| b14.v | Icarus Verilog | 2.72 | 6.36B | 17.32B | 8.82B | 95.62% | 77.46% | 87.20M | 1.14% |
| b15.v | rx-prop | 3.46 | 1.49B | 5.17B | 1.63B | 87.22% | 96.94% | 6.36M | 0.69% |
| b15.v | rx-sweep (Linear) | 3.61 | 2.06B | 7.43B | 2.24B | 84.42% | 92.89% | 24.78M | 0.71% |
| b15.v | rx-oop (OOP Engine) | 2.06 | 2.44B | 5.03B | 3.14B | 91.06% | 89.26% | 30.22M | 2.27% |
| b15.v | Icarus Verilog | 2.81 | 6.56B | 18.43B | 8.40B | 95.70% | 65.46% | 125.04M | 0.61% |
| b21.v | rx-prop | 2.09 | 4.98B | 10.41B | 3.77B | 89.34% | 87.54% | 50.11M | 5.16% |
| b21.v | rx-sweep (Linear) | 2.79 | 3.49B | 9.73B | 3.16B | 85.81% | 89.56% | 46.89M | 2.10% |
| b21.v | rx-oop (OOP Engine) | 1.29 | 7.58B | 9.76B | 7.31B | 92.90% | 75.36% | 128.05M | 7.30% |
| b21.v | Icarus Verilog | 2.68 | 9.06B | 24.23B | 11.98B | 95.54% | 69.82% | 161.59M | 1.01% |
| b20.v | rx-prop | 1.95 | 6.31B | 12.31B | 4.56B | 89.37% | 88.18% | 57.43M | 5.97% |
| b20.v | rx-sweep (Linear) | 2.61 | 4.16B | 10.85B | 3.60B | 86.37% | 89.77% | 50.34M | 2.67% |
| b20.v | rx-oop (OOP Engine) | 1.24 | 8.45B | 10.45B | 8.01B | 93.21% | 74.06% | 141.67M | 7.81% |
| b20.v | Icarus Verilog | 2.64 | 10.15B | 26.81B | 13.53B | 95.56% | 70.28% | 177.85M | 1.09% |
| b22.v | rx-prop | 1.71 | 11.48B | 19.66B | 7.55B | 89.31% | 80.03% | 161.27M | 7.14% |
| b22.v | rx-sweep (Linear) | 2.33 | 7.28B | 16.96B | 5.89B | 87.26% | 86.61% | 100.60M | 3.51% |
| b22.v | rx-oop (OOP Engine) | 1.10 | 16.70B | 18.37B | 14.78B | 93.35% | 66.98% | 324.29M | 9.13% |
| b22.v | Icarus Verilog | 2.28 | 19.79B | 45.06B | 24.27B | 95.59% | 56.13% | 470.36M | 1.22% |
| b17.v | rx-prop | 2.95 | 5.23B | 15.41B | 4.95B | 87.12% | 80.40% | 124.93M | 0.90% |
| b17.v | rx-sweep (Linear) | 3.54 | 6.26B | 22.17B | 6.73B | 84.89% | 94.13% | 59.80M | 0.79% |
| b17.v | rx-oop (OOP Engine) | 1.77 | 8.27B | 14.61B | 9.29B | 90.90% | 59.61% | 342.67M | 2.06% |
| b17.v | Icarus Verilog | 2.42 | 15.65B | 37.84B | 17.61B | 94.45% | 56.06% | 429.38M | 0.71% |
| b18.v | rx-prop | 2.14 | 20.13B | 43.07B | 15.09B | 88.52% | 69.85% | 523.70M | 3.57% |
| b18.v | rx-sweep (Linear) | 3.19 | 17.01B | 54.21B | 16.88B | 85.29% | 90.44% | 237.30M | 1.13% |
| b18.v | rx-oop (OOP Engine) | 1.47 | 28.31B | 41.62B | 28.32B | 92.22% | 57.93% | 930.42M | 4.53% |
| b18.v | Icarus Verilog | 1.90 | 20.89B | 39.78B | 18.64B | 94.80% | 77.02% | 222.18M | 1.44% |
| b19.v | rx-prop | 2.27 | 32.69B | 74.11B | 25.00B | 87.65% | 64.29% | 1.10B | 2.17% |
| b19.v | rx-sweep (Linear) | 3.26 | 31.87B | 104.07B | 31.59B | 84.78% | 88.78% | 539.65M | 0.77% |
| b19.v | rx-oop (OOP Engine) | 1.58 | 45.48B | 71.66B | 45.67B | 91.25% | 51.01% | 1.96B | 2.71% |
| b19.v | Icarus Verilog | 1.72 | 37.65B | 64.84B | 28.83B | 94.36% | 75.91% | 392.49M | 1.40% |
