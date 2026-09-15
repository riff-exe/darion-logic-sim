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
| ctrl.v | 340 | 0.66 MB (32.0 MB peak) | 0.47 MB (33.6 MB peak) | 0.31 MB (8.1 MB peak) | 0.68 MB (4.4 MB peak) |
| int2float.v | 461 | 2.76 MB (34.1 MB peak) | 0.61 MB (33.7 MB peak) | 0.14 MB (8.0 MB peak) | 0.71 MB (4.4 MB peak) |
| dec.v | 576 | 0.84 MB (32.2 MB peak) | 0.84 MB (33.9 MB peak) | 0.16 MB (8.1 MB peak) | 0.73 MB (4.4 MB peak) |
| router.v | 576 | 0.81 MB (32.2 MB peak) | 0.74 MB (33.8 MB peak) | 0.26 MB (8.1 MB peak) | 0.68 MB (4.4 MB peak) |
| cavlc.v | 1,300 | 1.56 MB (32.9 MB peak) | 1.68 MB (34.7 MB peak) | 0.72 MB (8.5 MB peak) | 0.71 MB (4.4 MB peak) |
| priority.v | 2,043 | 2.29 MB (33.6 MB peak) | 2.49 MB (35.6 MB peak) | 0.98 MB (8.8 MB peak) | 0.74 MB (4.4 MB peak) |
| adder.v | 2,547 | 2.66 MB (34.0 MB peak) | 2.98 MB (36.1 MB peak) | 1.20 MB (9.0 MB peak) | 0.77 MB (4.5 MB peak) |
| i2c.v | 2,480 | 2.67 MB (34.0 MB peak) | 2.96 MB (36.0 MB peak) | 1.06 MB (9.0 MB peak) | 0.75 MB (4.5 MB peak) |
| bar.v | 5,526 | 7.58 MB (38.9 MB peak) | 6.88 MB (39.9 MB peak) | 3.09 MB (11.0 MB peak) | 0.78 MB (4.5 MB peak) |
| max.v | 6,025 | 6.07 MB (37.5 MB peak) | 7.26 MB (40.3 MB peak) | 3.42 MB (11.2 MB peak) | 0.86 MB (4.6 MB peak) |
| arbiter.v | 23,618 | 24.61 MB (55.9 MB peak) | 29.15 MB (62.3 MB peak) | 15.20 MB (23.1 MB peak) | 0.87 MB (4.5 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| ctrl.v | 340 | 1.63 ms (0.044 ms opt) | 3.74 ms | 4.51 ms | 3.55 s |
| int2float.v | 461 | 1.90 ms (0.051 ms opt) | 4.65 ms | 5.00 ms | 3.54 s |
| dec.v | 576 | 1.99 ms (0.050 ms opt) | 4.48 ms | 5.40 ms | 3.57 s |
| router.v | 576 | 2.07 ms (0.054 ms opt) | 4.60 ms | 6.12 ms | 3.61 s |
| cavlc.v | 1,300 | 4.23 ms (0.148 ms opt) | 7.49 ms | 9.70 ms | 3.60 s |
| priority.v | 2,043 | 5.77 ms (0.168 ms opt) | 9.40 ms | 13.40 ms | 3.63 s |
| adder.v | 2,547 | 6.68 ms (0.177 ms opt) | 10.35 ms | 15.43 ms | 3.61 s |
| i2c.v | 2,480 | 6.84 ms (0.258 ms opt) | 10.30 ms | 17.08 ms | 3.63 s |
| bar.v | 5,526 | 15.36 ms (0.471 ms opt) | 31.27 ms | 35.37 ms | 4.22 s |
| max.v | 6,025 | 16.79 ms (0.494 ms opt) | 31.77 ms | 37.32 ms | 3.90 s |
| arbiter.v | 23,618 | 63.50 ms (1.783 ms opt) | 92.51 ms | 165.35 ms | 10.99 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| ctrl.v | 19.58 ms | 14.53 ms | 21.35 ms | 858.26 ms | 117.37 ms | 0.94 ms |
| int2float.v | 23.45 ms | 21.56 ms | 25.96 ms | 947.29 ms | 143.91 ms | 1.40 ms |
| dec.v | 4.56 ms | 8.65 ms | 4.98 ms | 397.69 ms | 49.10 ms | 1.32 ms |
| router.v | 26.79 ms | 21.08 ms | 29.85 ms | 1048.15 ms | 209.62 ms | 2.34 ms |
| cavlc.v | 74.60 ms | 66.57 ms | 81.06 ms | 2821.18 ms | 407.68 ms | 2.74 ms |
| priority.v | 85.35 ms | 76.13 ms | 94.72 ms | 4178.72 ms | 3862.49 ms | 13.23 ms |
| adder.v | 175.26 ms | 103.16 ms | 189.06 ms | 7856.48 ms | 1101.16 ms | 19.22 ms |
| i2c.v | 117.88 ms | 123.84 ms | 122.82 ms | 4620.01 ms | 831.31 ms | 8.06 ms |
| bar.v | 271.11 ms | 238.71 ms | 271.24 ms | 18.91 s | 2087.59 ms | 17.53 ms |
| max.v | 507.48 ms | 344.69 ms | 502.24 ms | 21.20 s | 3722.62 ms | 24.26 ms |
| arbiter.v | 875.58 ms | 748.07 ms | 1093.02 ms | 49.01 s | 5444.63 ms | 50.30 ms |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| ctrl.v | 6.00x | 8.08x | 5.50x | 0.14x | 1.00x | 125.46x |
| int2float.v | 6.14x | 6.68x | 5.54x | 0.15x | 1.00x | 103.13x |
| dec.v | 10.76x | 5.68x | 9.86x | 0.12x | 1.00x | 37.33x |
| router.v | 7.83x | 9.94x | 7.02x | 0.20x | 1.00x | 89.61x |
| cavlc.v | 5.46x | 6.12x | 5.03x | 0.14x | 1.00x | 148.70x |
| priority.v | 45.25x | 50.74x | 40.78x | 0.92x | 1.00x | 291.97x |
| adder.v | 6.28x | 10.67x | 5.82x | 0.14x | 1.00x | 57.29x |
| i2c.v | 7.05x | 6.71x | 6.77x | 0.18x | 1.00x | 103.10x |
| bar.v | 7.70x | 8.75x | 7.70x | 0.11x | 1.00x | 119.09x |
| max.v | 7.34x | 10.80x | 7.41x | 0.18x | 1.00x | 153.47x |
| arbiter.v | 6.22x | 7.28x | 4.98x | 0.11x | 1.00x | 108.25x |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `8.24x`
- **rx-sweep (Linear Compiled):** `9.33x`
- **rx-oop (OOP Graph):** `7.59x`
- **Pure Python Engine:** `0.17x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `107.41x`

### Cross-Engine Comparisons

- **Cython Reactor (`rx-prop`) vs Pure Python:** `48.12x` faster
- **Cython Reactor (`rx-sweep`) vs Pure Python:** `54.47x` faster
- **Reactor Sweep vs Propagate Ratio:** `1.13x` (sweep faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | IPC | Cycles | Instructions | L1 Loads | L1 Hit% | L2 Hit% | LLC Misses | Brn Miss% |
|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| ctrl.v | rx-prop | 3.14 | 47.59M | 149.38M | 48.64M | 99.57% | 96.93% | 6.89K | 4.12% |
| ctrl.v | rx-sweep (Linear) | 3.69 | 30.00M | 110.67M | 34.24M | 99.41% | 99.90% | 167 | 3.05% |
| ctrl.v | rx-oop (OOP Engine) | 2.82 | 43.51M | 122.57M | 49.90M | 98.57% | 99.12% | 6.67K | 4.76% |
| ctrl.v | Pure Python Engine | 4.77 | 106.29M | 507.31M | 220.50M | 99.64% | 98.10% | 11.72K | 0.23% |
| ctrl.v | Icarus Verilog | 3.62 | 320.47M | 1.16B | 531.13M | 98.31% | 99.95% | 4.75K | 1.02% |
| int2float.v | rx-prop | 2.70 | 56.61M | 153.07M | 54.99M | 98.97% | 99.23% | 1.93K | 5.64% |
| int2float.v | rx-sweep (Linear) | 3.05 | 52.48M | 160.05M | 50.58M | 98.44% | 99.74% | 2.18K | 3.99% |
| int2float.v | rx-oop (OOP Engine) | 2.34 | 63.65M | 149.15M | 60.07M | 97.33% | 99.81% | 3.13K | 6.31% |
| int2float.v | Pure Python Engine | 4.84 | 119.30M | 576.96M | 245.77M | 99.62% | 98.86% | 14.76K | 0.22% |
| int2float.v | Icarus Verilog | 3.32 | 387.53M | 1.29B | 616.08M | 97.76% | 99.91% | 12.41K | 1.25% |
| dec.v | rx-prop | 36.58 | 525.39K | 19.22M | 3.03M | 97.77% | 93.26% | 4.54K | 1.03% |
| dec.v | rx-sweep (Linear) | 4.42 | 17.81M | 78.77M | 17.54M | 99.31% | 97.46% | 3.05K | 1.38% |
| dec.v | rx-oop (OOP Engine) | 7.66 | 7.25M | 55.49M | 4.73M | 93.87% | 96.15% | 11.18K | 0.96% |
| dec.v | Pure Python Engine | 4.96 | 43.89M | 217.81M | 95.08M | 99.49% | 97.53% | 9.95K | 0.11% |
| dec.v | Icarus Verilog | 4.36 | 124.94M | 544.51M | 223.22M | 97.80% | 99.89% | 3.73K | 0.72% |
| router.v | rx-prop | 2.38 | 70.96M | 168.66M | 70.64M | 99.15% | 97.86% | 16.95K | 6.42% |
| router.v | rx-sweep (Linear) | 3.18 | 60.18M | 191.13M | 63.54M | 98.14% | 98.45% | 18.12K | 2.96% |
| router.v | rx-oop (OOP Engine) | 2.05 | 82.17M | 168.12M | 72.45M | 96.89% | 99.37% | 15.98K | 8.09% |
| router.v | Pure Python Engine | 4.75 | 132.84M | 630.99M | 288.24M | 99.67% | 97.94% | 19.84K | 0.21% |
| router.v | Icarus Verilog | 3.68 | 571.29M | 2.10B | 977.68M | 98.21% | 99.99% | 1.35K | 0.93% |
| cavlc.v | rx-prop | 2.43 | 192.45M | 466.82M | 180.47M | 95.71% | 99.86% | 11.27K | 5.43% |
| cavlc.v | rx-sweep (Linear) | 2.52 | 179.05M | 450.57M | 162.61M | 92.81% | 99.95% | 5.58K | 4.80% |
| cavlc.v | rx-oop (OOP Engine) | 2.11 | 215.36M | 454.81M | 193.86M | 94.14% | 99.91% | 10.33K | 6.09% |
| cavlc.v | Pure Python Engine | 4.79 | 370.10M | 1.77B | 787.86M | 99.55% | 96.99% | 108.94K | 0.19% |
| cavlc.v | Icarus Verilog | 3.08 | 1.12B | 3.46B | 1.74B | 96.16% | 99.96% | 20.72K | 1.23% |
| priority.v | rx-prop | 3.13 | 242.38M | 758.98M | 272.86M | 94.71% | 99.76% | 46.12K | 2.48% |
| priority.v | rx-sweep (Linear) | 3.22 | 220.33M | 709.33M | 248.96M | 92.33% | 99.82% | 44.45K | 2.29% |
| priority.v | rx-oop (OOP Engine) | 2.75 | 262.86M | 723.14M | 261.66M | 91.47% | 99.81% | 53.01K | 2.85% |
| priority.v | Pure Python Engine | 4.74 | 555.31M | 2.63B | 1.17B | 99.63% | 85.64% | 633.47K | 0.23% |
| priority.v | Icarus Verilog | 3.80 | 10.67B | 40.56B | 19.48B | 97.33% | 99.94% | 325.85K | 0.68% |
| adder.v | rx-prop | 2.24 | 510.23M | 1.14B | 485.67M | 94.34% | 99.70% | 90.97K | 4.62% |
| adder.v | rx-sweep (Linear) | 3.61 | 311.19M | 1.12B | 387.89M | 93.09% | 99.72% | 76.78K | 1.91% |
| adder.v | rx-oop (OOP Engine) | 1.96 | 544.34M | 1.07B | 489.28M | 92.38% | 99.73% | 97.86K | 5.54% |
| adder.v | Pure Python Engine | 4.66 | 1.05B | 4.89B | 2.22B | 99.61% | 74.43% | 2.19M | 0.23% |
| adder.v | Icarus Verilog | 3.74 | 3.04B | 11.37B | 5.35B | 96.98% | 99.69% | 510.31K | 0.68% |
| i2c.v | rx-prop | 2.36 | 337.50M | 798.06M | 326.27M | 92.47% | 99.77% | 56.89K | 4.43% |
| i2c.v | rx-sweep (Linear) | 2.50 | 356.12M | 888.75M | 337.67M | 92.61% | 99.77% | 58.08K | 5.03% |
| i2c.v | rx-oop (OOP Engine) | 2.16 | 349.58M | 753.90M | 320.10M | 91.36% | 99.84% | 48.13K | 5.12% |
| i2c.v | Pure Python Engine | 4.53 | 598.70M | 2.71B | 1.23B | 99.58% | 78.20% | 1.15M | 0.28% |
| i2c.v | Icarus Verilog | 3.46 | 2.27B | 7.87B | 3.80B | 96.76% | 98.99% | 1.22M | 0.88% |
| bar.v | rx-prop | 3.65 | 753.11M | 2.75B | 881.96M | 87.86% | 99.98% | 31.18K | 0.40% |
| bar.v | rx-sweep (Linear) | 3.04 | 662.97M | 2.02B | 716.66M | 92.11% | 99.91% | 59.83K | 3.51% |
| bar.v | rx-oop (OOP Engine) | 3.26 | 751.54M | 2.45B | 813.14M | 87.45% | 99.72% | 311.55K | 0.51% |
| bar.v | Pure Python Engine | 4.44 | 472.22M | 2.10B | 921.08M | 99.36% | 61.84% | 2.26M | 0.15% |
| bar.v | Icarus Verilog | 3.71 | 5.72B | 21.20B | 9.64B | 94.44% | 83.80% | 87.00M | 0.34% |
| max.v | rx-prop | 2.42 | 1.46B | 3.53B | 1.42B | 90.59% | 99.72% | 375.15K | 3.50% |
| max.v | rx-sweep (Linear) | 2.65 | 1.01B | 2.68B | 1.04B | 93.17% | 99.66% | 247.73K | 4.33% |
| max.v | rx-oop (OOP Engine) | 2.14 | 1.43B | 3.07B | 1.32B | 89.30% | 98.78% | 1.73M | 4.11% |
| max.v | Pure Python Engine | 4.33 | 544.67M | 2.36B | 1.06B | 99.54% | 57.13% | 2.12M | 0.18% |
| max.v | Icarus Verilog | 3.24 | 10.19B | 32.99B | 16.54B | 96.34% | 82.96% | 103.21M | 0.81% |
| arbiter.v | rx-prop | 2.58 | 2.42B | 6.24B | 2.07B | 86.20% | 81.37% | 53.17M | 0.89% |
| arbiter.v | rx-sweep (Linear) | 3.40 | 2.08B | 7.06B | 2.25B | 90.85% | 89.40% | 21.82M | 1.11% |
| arbiter.v | rx-oop (OOP Engine) | 2.01 | 3.01B | 6.04B | 2.12B | 86.36% | 60.24% | 115.33M | 1.09% |
| arbiter.v | Pure Python Engine | 4.10 | 595.03M | 2.44B | 1.09B | 99.38% | 45.24% | 3.69M | 0.07% |
| arbiter.v | Icarus Verilog | 3.10 | 14.91B | 46.18B | 21.78B | 94.13% | 48.47% | 659.09M | 0.24% |
