# Master Test Unified Benchmark Report: tests/EPFL_parsed

**Execution Parameters:**
- **Target Suite / Path:** `tests/EPFL_parsed`
- **Circuits Benchmarked:** 11
- **Simulation Vectors (Phase 3):** 10,000 (Warmup: 10)
- **Verification Vectors (Phase 2):** 100
- **Hardware Profiler:** Linux `perf` kernel PMU counters

---

## 1. Zero-Testbench Memory Footprint (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| ctrl.v | 340 | 0.62 MB (32.0 MB peak) | 0.47 MB (33.5 MB peak) | 0.17 MB (8.0 MB peak) | 0.72 MB (4.4 MB peak) |
| int2float.v | 461 | 0.73 MB (32.1 MB peak) | 0.64 MB (33.7 MB peak) | 0.18 MB (8.1 MB peak) | 0.70 MB (4.4 MB peak) |
| dec.v | 576 | 2.86 MB (34.2 MB peak) | 0.78 MB (33.8 MB peak) | 0.19 MB (8.0 MB peak) | 0.72 MB (4.4 MB peak) |
| router.v | 576 | 0.85 MB (32.1 MB peak) | 0.72 MB (33.7 MB peak) | 0.28 MB (8.1 MB peak) | 0.60 MB (4.3 MB peak) |
| cavlc.v | 1,300 | 1.53 MB (32.9 MB peak) | 1.70 MB (34.7 MB peak) | 0.61 MB (8.4 MB peak) | 0.71 MB (4.4 MB peak) |
| priority.v | 2,043 | 4.09 MB (35.5 MB peak) | 2.52 MB (35.5 MB peak) | 0.87 MB (8.7 MB peak) | 0.74 MB (4.4 MB peak) |
| adder.v | 2,547 | 2.55 MB (33.9 MB peak) | 2.97 MB (36.0 MB peak) | 1.16 MB (9.0 MB peak) | 0.74 MB (4.4 MB peak) |
| i2c.v | 2,480 | 2.59 MB (34.0 MB peak) | 2.95 MB (36.0 MB peak) | 1.12 MB (9.0 MB peak) | 0.75 MB (4.4 MB peak) |
| bar.v | 5,526 | 5.64 MB (37.0 MB peak) | 6.88 MB (40.0 MB peak) | 3.18 MB (11.0 MB peak) | 0.84 MB (4.5 MB peak) |
| max.v | 6,025 | 5.99 MB (37.3 MB peak) | 7.26 MB (40.3 MB peak) | 3.36 MB (11.2 MB peak) | 0.79 MB (4.5 MB peak) |
| arbiter.v | 23,618 | 24.65 MB (56.0 MB peak) | 29.12 MB (62.2 MB peak) | 15.18 MB (23.1 MB peak) | 0.84 MB (4.5 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| ctrl.v | 340 | 1.30 ms (0.031 ms opt) | 2.69 ms | 3.29 ms | 2.57 s |
| int2float.v | 461 | 1.33 ms (0.042 ms opt) | 3.19 ms | 3.64 ms | 2.58 s |
| dec.v | 576 | 1.42 ms (0.037 ms opt) | 3.16 ms | 3.26 ms | 2.58 s |
| router.v | 576 | 1.76 ms (0.042 ms opt) | 3.10 ms | 4.25 ms | 2.60 s |
| cavlc.v | 1,300 | 3.17 ms (0.108 ms opt) | 5.24 ms | 7.00 ms | 2.62 s |
| priority.v | 2,043 | 4.02 ms (0.117 ms opt) | 6.38 ms | 9.67 ms | 2.65 s |
| adder.v | 2,547 | 4.65 ms (0.127 ms opt) | 7.19 ms | 11.36 ms | 2.66 s |
| i2c.v | 2,480 | 4.83 ms (0.180 ms opt) | 7.41 ms | 12.21 ms | 2.64 s |
| bar.v | 5,526 | 11.59 ms (0.368 ms opt) | 15.67 ms | 26.66 ms | 3.18 s |
| max.v | 6,025 | 11.50 ms (0.352 ms opt) | 16.54 ms | 28.36 ms | 2.92 s |
| arbiter.v | 23,618 | 44.82 ms (1.335 ms opt) | 60.57 ms | 127.41 ms | 8.57 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| ctrl.v | 13.19 ms | 9.80 ms | 24.22 ms | 582.11 ms | 82.35 ms | 0.68 ms |
| int2float.v | 16.24 ms | 15.10 ms | 24.82 ms | 644.00 ms | 101.72 ms | 1.11 ms |
| dec.v | 3.34 ms | 6.33 ms | 4.39 ms | 286.99 ms | 34.72 ms | 0.67 ms |
| router.v | 18.92 ms | 14.73 ms | 28.81 ms | 742.47 ms | 146.20 ms | 1.55 ms |
| cavlc.v | 50.88 ms | 45.23 ms | 73.73 ms | 2030.57 ms | 287.49 ms | 1.91 ms |
| priority.v | 59.58 ms | 53.00 ms | 84.26 ms | 2892.45 ms | 2662.61 ms | 9.01 ms |
| adder.v | 123.63 ms | 71.57 ms | 163.09 ms | 5441.88 ms | 786.78 ms | 13.17 ms |
| i2c.v | 83.19 ms | 85.52 ms | 115.35 ms | 3088.74 ms | 567.56 ms | 5.66 ms |
| bar.v | 185.48 ms | 163.27 ms | 226.63 ms | 12.74 s | 1432.35 ms | 12.15 ms |
| max.v | 348.30 ms | 236.53 ms | 439.94 ms | 14.89 s | 2500.41 ms | 16.53 ms |
| arbiter.v | 594.55 ms | 508.60 ms | 828.85 ms | 39.49 s | 3548.22 ms | 36.76 ms |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| ctrl.v | 6.25x | 8.40x | 3.40x | 0.14x | 1.00x | 120.93x |
| int2float.v | 6.26x | 6.74x | 4.10x | 0.16x | 1.00x | 91.94x |
| dec.v | 10.39x | 5.49x | 7.90x | 0.12x | 1.00x | 52.15x |
| router.v | 7.73x | 9.92x | 5.07x | 0.20x | 1.00x | 94.50x |
| cavlc.v | 5.65x | 6.36x | 3.90x | 0.14x | 1.00x | 150.89x |
| priority.v | 44.69x | 50.24x | 31.60x | 0.92x | 1.00x | 295.40x |
| adder.v | 6.36x | 10.99x | 4.82x | 0.14x | 1.00x | 59.75x |
| i2c.v | 6.82x | 6.64x | 4.92x | 0.18x | 1.00x | 100.23x |
| bar.v | 7.72x | 8.77x | 6.32x | 0.11x | 1.00x | 117.90x |
| max.v | 7.18x | 10.57x | 5.68x | 0.17x | 1.00x | 151.28x |
| arbiter.v | 5.97x | 6.98x | 4.28x | 0.09x | 1.00x | 96.54x |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `8.21x`
- **rx-sweep (Linear Compiled):** `9.33x`
- **rx-oop (OOP Graph):** `5.80x`
- **Pure Python Engine:** `0.17x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `108.76x`

### Cross-Engine Comparisons

- **Cython Reactor (`rx-prop`) vs Pure Python:** `48.69x` faster
- **Cython Reactor (`rx-sweep`) vs Pure Python:** `55.32x` faster
- **Reactor Sweep vs Propagate Ratio:** `1.14x` (sweep faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | IPC | Cycles | Instructions | L1 Loads | L1 Hit% | L2 Hit% | LLC Misses | Brn Miss% |
|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| ctrl.v | rx-prop | 3.60 | 31.62M | 113.91M | 42.91M | 99.83% | 98.96% | 752 | 4.12% |
| ctrl.v | rx-sweep (Linear) | 3.20 | 32.38M | 103.48M | 34.29M | 99.81% | 95.68% | 3.80K | 2.90% |
| ctrl.v | rx-oop (OOP Engine) | 1.71 | 86.12M | 147.53M | 91.07M | 98.86% | 98.21% | 16.61K | 7.36% |
| ctrl.v | Pure Python Engine | 4.89 | 101.27M | 494.71M | 213.65M | 99.63% | 98.81% | 9.22K | 0.31% |
| ctrl.v | Icarus Verilog | 3.47 | 323.36M | 1.12B | 545.64M | 98.35% | 99.98% | 2.73K | 1.13% |
| int2float.v | rx-prop | 2.84 | 47.20M | 134.10M | 49.92M | 99.14% | 99.85% | 686 | 5.60% |
| int2float.v | rx-sweep (Linear) | 3.19 | 44.62M | 142.55M | 45.41M | 98.62% | 99.66% | 2.13K | 4.01% |
| int2float.v | rx-oop (OOP Engine) | 1.69 | 90.20M | 152.34M | 101.50M | 98.23% | 99.31% | 11.65K | 7.39% |
| int2float.v | Pure Python Engine | 5.00 | 111.23M | 556.63M | 242.63M | 99.53% | 98.97% | 3.76K | 0.22% |
| int2float.v | Icarus Verilog | 3.30 | 384.84M | 1.27B | 608.72M | 97.78% | 99.90% | 11.35K | 1.33% |
| dec.v | rx-prop | 397.34 | 44.27K | 17.59M | 5.14M | 97.57% | 96.13% | 4.87K | 1.15% |
| dec.v | rx-sweep (Linear) | 5.52 | 14.42M | 79.59M | 16.91M | 99.36% | 97.20% | 721 | 1.19% |
| dec.v | rx-oop (OOP Engine) | 4.64 | 6.72M | 31.17M | 11.72M | 98.24% | 98.49% | 3.12K | 1.26% |
| dec.v | Pure Python Engine | 5.06 | 43.26M | 218.70M | 75.86M | 99.63% | 96.66% | 3.94K | 0.11% |
| dec.v | Icarus Verilog | 4.17 | 134.92M | 562.20M | 227.10M | 97.78% | 99.95% | 6.09K | 0.71% |
| router.v | rx-prop | 2.40 | 69.53M | 166.71M | 65.09M | 99.20% | 98.45% | 9.32K | 7.25% |
| router.v | rx-sweep (Linear) | 3.28 | 62.22M | 204.26M | 61.04M | 97.56% | 98.14% | 26.83K | 2.62% |
| router.v | rx-oop (OOP Engine) | 1.48 | 106.37M | 156.97M | 111.47M | 97.84% | 99.64% | 11.00K | 9.01% |
| router.v | Pure Python Engine | 4.75 | 127.65M | 606.17M | 272.09M | 99.63% | 97.09% | 22.94K | 0.20% |
| router.v | Icarus Verilog | 3.62 | 581.35M | 2.10B | 970.61M | 98.20% | 99.97% | 4.53K | 0.96% |
| cavlc.v | rx-prop | 2.31 | 194.37M | 449.49M | 181.00M | 95.79% | 99.96% | 3.40K | 5.40% |
| cavlc.v | rx-sweep (Linear) | 2.61 | 170.60M | 444.80M | 156.46M | 92.75% | 99.98% | 1.71K | 4.76% |
| cavlc.v | rx-oop (OOP Engine) | 1.59 | 291.36M | 463.64M | 330.76M | 96.35% | 99.89% | 12.52K | 6.91% |
| cavlc.v | Pure Python Engine | 4.60 | 384.94M | 1.77B | 791.55M | 99.54% | 94.50% | 208.14K | 0.25% |
| cavlc.v | Icarus Verilog | 3.01 | 1.15B | 3.47B | 1.77B | 96.25% | 99.81% | 105.80K | 1.27% |
| priority.v | rx-prop | 3.17 | 252.56M | 800.06M | 285.45M | 94.64% | 99.58% | 62.14K | 2.43% |
| priority.v | rx-sweep (Linear) | 3.15 | 222.59M | 701.01M | 249.44M | 92.35% | 99.78% | 51.75K | 2.33% |
| priority.v | rx-oop (OOP Engine) | 2.09 | 352.34M | 737.58M | 442.70M | 94.57% | 99.78% | 66.67K | 3.22% |
| priority.v | Pure Python Engine | 4.65 | 558.36M | 2.60B | 1.18B | 99.63% | 87.03% | 581.45K | 0.26% |
| priority.v | Icarus Verilog | 3.77 | 10.77B | 40.55B | 19.41B | 97.36% | 99.82% | 899.92K | 0.70% |
| adder.v | rx-prop | 2.18 | 542.27M | 1.18B | 505.12M | 94.16% | 99.64% | 124.69K | 4.53% |
| adder.v | rx-sweep (Linear) | 3.53 | 318.35M | 1.12B | 380.77M | 93.03% | 99.64% | 91.49K | 1.98% |
| adder.v | rx-oop (OOP Engine) | 1.62 | 683.03M | 1.11B | 777.31M | 94.79% | 99.78% | 86.30K | 5.58% |
| adder.v | Pure Python Engine | 4.57 | 1.07B | 4.87B | 2.23B | 99.62% | 75.91% | 2.06M | 0.29% |
| adder.v | Icarus Verilog | 3.61 | 3.16B | 11.40B | 5.35B | 97.00% | 99.13% | 1.41M | 0.66% |
| i2c.v | rx-prop | 2.28 | 351.57M | 800.48M | 328.78M | 92.30% | 99.71% | 74.59K | 4.54% |
| i2c.v | rx-sweep (Linear) | 2.50 | 366.07M | 913.49M | 341.04M | 92.69% | 99.66% | 82.17K | 4.81% |
| i2c.v | rx-oop (OOP Engine) | 1.57 | 463.85M | 728.49M | 518.40M | 94.68% | 99.81% | 52.70K | 6.43% |
| i2c.v | Pure Python Engine | 4.58 | 591.14M | 2.71B | 1.22B | 99.58% | 77.13% | 1.17M | 0.23% |
| i2c.v | Icarus Verilog | 3.45 | 2.29B | 7.90B | 3.79B | 96.77% | 99.50% | 618.16K | 0.90% |
| bar.v | rx-prop | 3.66 | 745.64M | 2.73B | 881.17M | 87.68% | 99.97% | 37.31K | 0.39% |
| bar.v | rx-sweep (Linear) | 3.03 | 669.76M | 2.03B | 715.18M | 92.18% | 99.94% | 32.37K | 3.55% |
| bar.v | rx-oop (OOP Engine) | 2.63 | 927.27M | 2.44B | 1.34B | 92.08% | 99.75% | 211.85K | 0.70% |
| bar.v | Pure Python Engine | 4.55 | 455.44M | 2.07B | 907.39M | 99.41% | 59.64% | 2.21M | 0.18% |
| bar.v | Icarus Verilog | 3.71 | 5.72B | 21.20B | 9.82B | 94.56% | 83.31% | 89.20M | 0.35% |
| max.v | rx-prop | 2.36 | 1.49B | 3.50B | 1.43B | 90.68% | 99.73% | 378.38K | 3.60% |
| max.v | rx-sweep (Linear) | 2.58 | 1.03B | 2.66B | 1.05B | 93.23% | 99.56% | 336.85K | 4.27% |
| max.v | rx-oop (OOP Engine) | 1.70 | 1.84B | 3.12B | 2.15B | 93.07% | 99.15% | 1.31M | 4.51% |
| max.v | Pure Python Engine | 4.22 | 549.77M | 2.32B | 1.07B | 99.53% | 56.34% | 2.22M | 0.34% |
| max.v | Icarus Verilog | 3.28 | 10.06B | 33.00B | 16.51B | 96.34% | 81.98% | 108.99M | 0.81% |
| arbiter.v | rx-prop | 2.60 | 2.39B | 6.23B | 2.07B | 86.18% | 83.24% | 48.06M | 0.90% |
| arbiter.v | rx-sweep (Linear) | 3.42 | 2.07B | 7.07B | 2.26B | 90.92% | 89.41% | 21.70M | 1.12% |
| arbiter.v | rx-oop (OOP Engine) | 1.80 | 3.34B | 6.03B | 3.48B | 91.38% | 58.90% | 123.16M | 1.49% |
| arbiter.v | Pure Python Engine | 3.48 | 703.04M | 2.44B | 1.09B | 99.33% | 45.12% | 4.00M | 0.12% |
| arbiter.v | Icarus Verilog | 3.26 | 14.16B | 46.20B | 21.75B | 94.07% | 47.96% | 671.43M | 0.24% |
