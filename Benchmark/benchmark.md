# master_test/master_test_report_20260918_174018.md

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
| c432.v | 203 | 0.52 MB (31.8 MB peak) | 0.34 MB (33.4 MB peak) | 0.15 MB (8.0 MB peak) | 0.73 MB (4.4 MB peak) |
| c499.v | 275 | 0.57 MB (31.9 MB peak) | 0.45 MB (33.5 MB peak) | 0.19 MB (8.0 MB peak) | 0.71 MB (4.4 MB peak) |
| c880.v | 469 | 0.75 MB (32.1 MB peak) | 0.65 MB (33.7 MB peak) | 0.27 MB (8.1 MB peak) | 0.73 MB (4.4 MB peak) |
| c1355.v | 619 | 0.93 MB (32.3 MB peak) | 0.84 MB (33.8 MB peak) | 0.38 MB (8.2 MB peak) | 0.70 MB (4.4 MB peak) |
| c1908.v | 938 | 1.24 MB (32.6 MB peak) | 1.18 MB (34.3 MB peak) | 0.52 MB (8.3 MB peak) | 0.70 MB (4.4 MB peak) |
| c2670.v | 1,642 | 1.95 MB (33.2 MB peak) | 2.06 MB (35.1 MB peak) | 0.68 MB (8.5 MB peak) | 0.75 MB (4.4 MB peak) |
| c3540.v | 1,741 | 3.90 MB (35.3 MB peak) | 2.25 MB (35.2 MB peak) | 0.82 MB (8.7 MB peak) | 0.72 MB (4.4 MB peak) |
| c5315.v | 2,608 | 2.83 MB (34.2 MB peak) | 3.30 MB (36.3 MB peak) | 1.28 MB (9.1 MB peak) | 0.76 MB (4.4 MB peak) |
| c6288.v | 2,480 | 2.70 MB (34.1 MB peak) | 3.17 MB (36.2 MB peak) | 1.24 MB (9.1 MB peak) | 0.86 MB (4.5 MB peak) |
| c7552.v | 3,828 | 3.92 MB (35.3 MB peak) | 4.68 MB (37.8 MB peak) | 1.91 MB (9.7 MB peak) | 0.82 MB (4.5 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| c432.v | 203 | 0.39 ms (0.017 ms opt) | 0.69 ms | 2.93 ms | 2.52 s |
| c499.v | 275 | 0.49 ms (0.021 ms opt) | 2.12 ms | 2.81 ms | 2.57 s |
| c880.v | 469 | 0.58 ms (0.042 ms opt) | 2.24 ms | 3.90 ms | 2.53 s |
| c1355.v | 619 | 0.68 ms (0.047 ms opt) | 2.35 ms | 4.47 ms | 2.55 s |
| c1908.v | 938 | 0.87 ms (0.076 ms opt) | 3.20 ms | 5.26 ms | 2.59 s |
| c2670.v | 1,642 | 1.31 ms (0.113 ms opt) | 3.70 ms | 8.15 ms | 2.58 s |
| c3540.v | 1,741 | 1.60 ms (0.186 ms opt) | 4.41 ms | 8.99 ms | 2.60 s |
| c5315.v | 2,608 | 2.04 ms (0.201 ms opt) | 5.10 ms | 12.47 ms | 2.66 s |
| c6288.v | 2,480 | 2.29 ms (0.161 ms opt) | 5.04 ms | 12.36 ms | 2.84 s |
| c7552.v | 3,828 | 2.83 ms (0.293 ms opt) | 8.01 ms | 17.06 ms | 2.90 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| c432.v | 47.86 ms | 52.54 ms | 63.99 ms | 2479.13 ms | 416.06 ms | 5.07 ms |
| c499.v | 51.46 ms | 53.88 ms | 71.81 ms | 9696.51 ms | 506.54 ms | 5.03 ms |
| c880.v | 111.66 ms | 107.93 ms | 180.44 ms | 5025.88 ms | 813.43 ms | 9.39 ms |
| c1355.v | 154.98 ms | 120.70 ms | 222.02 ms | 15.43 s | 1133.84 ms | 8.48 ms |
| c1908.v | 322.35 ms | 167.44 ms | 499.50 ms | 16.93 s | 1922.77 ms | 10.33 ms |
| c2670.v | 468.73 ms | 352.90 ms | 754.28 ms | 20.12 s | 3567.17 ms | 37.32 ms |
| c3540.v | 576.47 ms | 365.89 ms | 924.47 ms | 29.36 s | 3325.96 ms | 19.56 ms |
| c5315.v | 1068.67 ms | 700.45 ms | 1676.87 ms | 48.76 s | 6710.23 ms | 32.06 ms |
| c6288.v | 5259.90 ms | 464.17 ms | 7029.74 ms | 483.30 s | 34.25 s | 45.51 ms |
| c7552.v | 1639.72 ms | 901.79 ms | 2452.38 ms | 79.87 s | 9846.58 ms | 47.46 ms |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| c432.v | 8.69x | 7.92x | 6.50x | 0.17x | 1.00x | 82.00x |
| c499.v | 9.84x | 9.40x | 7.05x | 0.05x | 1.00x | 100.74x |
| c880.v | 7.28x | 7.54x | 4.51x | 0.16x | 1.00x | 86.60x |
| c1355.v | 7.32x | 9.39x | 5.11x | 0.07x | 1.00x | 133.69x |
| c1908.v | 5.96x | 11.48x | 3.85x | 0.11x | 1.00x | 186.20x |
| c2670.v | 7.61x | 10.11x | 4.73x | 0.18x | 1.00x | 95.58x |
| c3540.v | 5.77x | 9.09x | 3.60x | 0.11x | 1.00x | 170.02x |
| c5315.v | 6.28x | 9.58x | 4.00x | 0.14x | 1.00x | 209.29x |
| c6288.v | 6.51x | 73.78x | 4.87x | 0.07x | 1.00x | 752.42x |
| c7552.v | 6.01x | 10.92x | 4.02x | 0.12x | 1.00x | 207.48x |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `7.03x`
- **rx-sweep (Linear Compiled):** `11.57x`
- **rx-oop (OOP Graph):** `4.71x`
- **Pure Python Engine:** `0.11x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `157.60x`

### Cross-Engine Comparisons

- **Cython Reactor (`rx-prop`) vs Pure Python:** `63.26x` faster
- **Cython Reactor (`rx-sweep`) vs Pure Python:** `104.15x` faster
- **Reactor Sweep vs Propagate Ratio:** `1.65x` (sweep faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | IPC | Cycles | Instructions | L1 Loads | L1 Hit% | L2 Hit% | LLC Misses | Brn Miss% |
|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| c432.v | rx-prop | 2.66 | 203.77M | 541.02M | 218.34M | 99.52% | 98.03% | 31.83K | 4.34% |
| c432.v | rx-sweep (Linear) | 1.94 | 224.71M | 436.00M | 188.87M | 99.47% | 98.26% | 26.18K | 5.45% |
| c432.v | rx-oop (OOP Engine) | 1.82 | 270.71M | 494.02M | 324.83M | 99.43% | 98.50% | 37.17K | 6.15% |
| c432.v | Pure Python Engine | 4.96 | 87.03M | 431.93M | 176.23M | 99.71% | 99.05% | 4.84K | 0.28% |
| c432.v | Icarus Verilog | 3.60 | 1.68B | 6.04B | 2.73B | 99.05% | 99.98% | 5.34K | 1.09% |
| c499.v | rx-prop | 3.76 | 209.93M | 789.33M | 285.96M | 99.31% | 98.07% | 43.43K | 1.87% |
| c499.v | rx-sweep (Linear) | 2.69 | 224.04M | 602.82M | 240.65M | 99.43% | 98.00% | 33.01K | 2.98% |
| c499.v | rx-oop (OOP Engine) | 2.47 | 306.60M | 756.11M | 453.54M | 99.25% | 98.65% | 43.40K | 3.24% |
| c499.v | Pure Python Engine | 4.85 | 371.00M | 1.80B | 783.23M | 99.74% | 99.86% | 3.66K | 0.21% |
| c499.v | Icarus Verilog | 3.66 | 2.05B | 7.49B | 3.38B | 98.64% | 99.99% | 5.20K | 1.02% |
| c880.v | rx-prop | 2.46 | 477.14M | 1.17B | 482.94M | 98.81% | 98.59% | 87.17K | 4.88% |
| c880.v | rx-sweep (Linear) | 1.91 | 463.79M | 886.97M | 402.82M | 98.29% | 98.99% | 69.52K | 5.14% |
| c880.v | rx-oop (OOP Engine) | 1.37 | 765.79M | 1.05B | 817.28M | 97.89% | 99.49% | 89.90K | 8.78% |
| c880.v | Pure Python Engine | 4.87 | 173.59M | 845.47M | 358.49M | 99.65% | 97.59% | 29.95K | 0.28% |
| c880.v | Icarus Verilog | 3.47 | 3.28B | 11.40B | 5.24B | 98.17% | 100.00% | 4.03K | 1.16% |
| c1355.v | rx-prop | 2.90 | 644.05M | 1.87B | 707.80M | 97.52% | 99.65% | 61.33K | 3.89% |
| c1355.v | rx-sweep (Linear) | 2.23 | 508.00M | 1.13B | 467.10M | 95.76% | 99.70% | 57.82K | 3.50% |
| c1355.v | rx-oop (OOP Engine) | 1.97 | 917.37M | 1.81B | 1.13B | 97.09% | 99.83% | 53.92K | 5.92% |
| c1355.v | Pure Python Engine | 4.82 | 594.34M | 2.86B | 1.26B | 99.67% | 99.47% | 19.41K | 0.23% |
| c1355.v | Icarus Verilog | 3.64 | 4.58B | 16.64B | 7.54B | 98.12% | 99.97% | 53.43K | 0.99% |
| c1908.v | rx-prop | 2.46 | 1.31B | 3.23B | 1.24B | 96.69% | 99.85% | 66.23K | 4.92% |
| c1908.v | rx-sweep (Linear) | 2.32 | 689.01M | 1.60B | 595.22M | 92.36% | 99.87% | 58.85K | 3.11% |
| c1908.v | rx-oop (OOP Engine) | 1.78 | 2.00B | 3.55B | 2.40B | 97.46% | 99.89% | 73.17K | 7.19% |
| c1908.v | Pure Python Engine | 4.76 | 657.02M | 3.13B | 1.39B | 99.60% | 99.11% | 51.38K | 0.23% |
| c1908.v | Icarus Verilog | 3.29 | 7.77B | 25.56B | 12.35B | 97.36% | 99.99% | 30.90K | 1.21% |
| c2670.v | rx-prop | 2.22 | 2.06B | 4.57B | 1.97B | 95.51% | 99.37% | 561.36K | 4.81% |
| c2670.v | rx-sweep (Linear) | 2.07 | 1.59B | 3.29B | 1.44B | 93.21% | 99.47% | 547.62K | 4.19% |
| c2670.v | rx-oop (OOP Engine) | 1.47 | 3.19B | 4.69B | 3.50B | 96.28% | 99.73% | 348.06K | 7.70% |
| c2670.v | Pure Python Engine | 4.73 | 772.32M | 3.65B | 1.63B | 99.63% | 92.42% | 461.35K | 0.29% |
| c2670.v | Icarus Verilog | 3.53 | 14.35B | 50.60B | 24.04B | 97.74% | 99.90% | 574.49K | 0.99% |
| c3540.v | rx-prop | 2.23 | 2.36B | 5.27B | 2.08B | 96.06% | 99.75% | 197.76K | 5.76% |
| c3540.v | rx-sweep (Linear) | 1.79 | 1.52B | 2.73B | 1.14B | 91.90% | 99.83% | 155.06K | 5.75% |
| c3540.v | rx-oop (OOP Engine) | 1.44 | 3.77B | 5.42B | 4.05B | 96.95% | 99.86% | 166.86K | 9.72% |
| c3540.v | Pure Python Engine | 4.61 | 1.15B | 5.29B | 2.40B | 99.61% | 91.78% | 768.41K | 0.31% |
| c3540.v | Icarus Verilog | 2.94 | 13.40B | 39.45B | 19.88B | 96.64% | 99.92% | 557.88K | 1.55% |
| c5315.v | rx-prop | 2.11 | 4.42B | 9.31B | 3.80B | 93.70% | 99.83% | 429.42K | 5.73% |
| c5315.v | rx-sweep (Linear) | 1.77 | 2.96B | 5.26B | 2.31B | 92.81% | 99.71% | 495.57K | 5.92% |
| c5315.v | rx-oop (OOP Engine) | 1.42 | 6.83B | 9.73B | 7.23B | 95.70% | 99.85% | 466.44K | 8.93% |
| c5315.v | Pure Python Engine | 4.54 | 353.31M | 1.60B | 736.20M | 99.62% | 74.90% | 698.62K | 0.24% |
| c5315.v | Icarus Verilog | 3.06 | 27.04B | 82.62B | 41.02B | 96.65% | 99.67% | 4.44M | 1.36% |
| c6288.v | rx-prop | 2.58 | 21.08B | 54.28B | 18.50B | 92.25% | 99.97% | 361.36K | 4.37% |
| c6288.v | rx-sweep (Linear) | 2.69 | 1.89B | 5.08B | 1.81B | 92.24% | 99.95% | 75.62K | 2.30% |
| c6288.v | rx-oop (OOP Engine) | 2.01 | 28.27B | 56.85B | 33.61B | 93.70% | 99.98% | 425.36K | 6.10% |
| c6288.v | Pure Python Engine | 4.64 | 3.70B | 17.17B | 7.71B | 99.57% | 93.34% | 2.19M | 0.24% |
| c6288.v | Icarus Verilog | 3.55 | 137.61B | 488.69B | 221.33B | 95.78% | 99.37% | 59.35M | 0.81% |
| c7552.v | rx-prop | 2.00 | 6.77B | 13.52B | 5.48B | 91.93% | 99.71% | 1.32M | 5.89% |
| c7552.v | rx-sweep (Linear) | 1.91 | 3.81B | 7.28B | 3.07B | 92.51% | 99.61% | 890.76K | 5.27% |
| c7552.v | rx-oop (OOP Engine) | 1.48 | 10.05B | 14.90B | 10.82B | 94.65% | 99.81% | 1.10M | 8.37% |
| c7552.v | Pure Python Engine | 4.43 | 593.76M | 2.63B | 1.18B | 99.60% | 65.69% | 1.65M | 0.30% |
| c7552.v | Icarus Verilog | 2.92 | 39.51B | 115.32B | 58.84B | 96.36% | 91.93% | 172.83M | 1.37% |

---

# master_test/master_test_report_20260918_174431.md

# Master Test Unified Benchmark Report: tests/EPFL_parsed

**Execution Parameters:**
- **Target Suite / Path:** `tests/EPFL_parsed`
- **Circuits Benchmarked:** 11
- **Simulation Vectors (Phase 3):** 50,000 (Warmup: 10)
- **Verification Vectors (Phase 2):** 100
- **Hardware Profiler:** Linux `perf` kernel PMU counters

---

## 1. Zero-Testbench Memory Footprint (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| ctrl.v | 340 | 2.59 MB (33.9 MB peak) | 0.50 MB (33.5 MB peak) | 0.22 MB (8.0 MB peak) | 0.72 MB (4.4 MB peak) |
| int2float.v | 461 | 0.75 MB (32.1 MB peak) | 0.61 MB (33.7 MB peak) | 0.14 MB (7.9 MB peak) | 0.68 MB (4.4 MB peak) |
| dec.v | 576 | 0.88 MB (32.2 MB peak) | 0.78 MB (33.9 MB peak) | 0.25 MB (8.1 MB peak) | 0.73 MB (4.4 MB peak) |
| router.v | 576 | 0.82 MB (32.2 MB peak) | 0.79 MB (33.8 MB peak) | 0.29 MB (8.1 MB peak) | 0.69 MB (4.4 MB peak) |
| cavlc.v | 1,300 | 1.61 MB (32.9 MB peak) | 1.68 MB (34.7 MB peak) | 0.59 MB (8.4 MB peak) | 0.71 MB (4.4 MB peak) |
| priority.v | 2,043 | 2.16 MB (33.4 MB peak) | 2.49 MB (35.6 MB peak) | 1.00 MB (8.8 MB peak) | 0.73 MB (4.4 MB peak) |
| adder.v | 2,547 | 2.57 MB (33.9 MB peak) | 2.97 MB (36.0 MB peak) | 1.20 MB (9.0 MB peak) | 0.76 MB (4.4 MB peak) |
| i2c.v | 2,480 | 2.52 MB (33.9 MB peak) | 2.98 MB (36.0 MB peak) | 1.12 MB (8.9 MB peak) | 0.75 MB (4.4 MB peak) |
| bar.v | 5,526 | 5.64 MB (37.0 MB peak) | 6.88 MB (40.0 MB peak) | 3.06 MB (10.9 MB peak) | 0.85 MB (4.5 MB peak) |
| max.v | 6,025 | 5.98 MB (37.4 MB peak) | 7.26 MB (40.2 MB peak) | 3.36 MB (11.2 MB peak) | 0.87 MB (4.6 MB peak) |
| arbiter.v | 23,618 | 25.00 MB (56.4 MB peak) | 29.15 MB (62.2 MB peak) | 15.25 MB (23.1 MB peak) | 0.89 MB (4.6 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| ctrl.v | 340 | 1.13 ms (0.030 ms opt) | 2.90 ms | 3.79 ms | 2.57 s |
| int2float.v | 461 | 1.32 ms (0.039 ms opt) | 3.04 ms | 3.86 ms | 2.58 s |
| dec.v | 576 | 1.37 ms (0.038 ms opt) | 3.11 ms | 3.45 ms | 2.53 s |
| router.v | 576 | 1.69 ms (0.041 ms opt) | 3.21 ms | 4.23 ms | 2.63 s |
| cavlc.v | 1,300 | 3.17 ms (0.108 ms opt) | 4.99 ms | 7.16 ms | 2.68 s |
| priority.v | 2,043 | 4.36 ms (0.118 ms opt) | 6.48 ms | 9.99 ms | 2.64 s |
| adder.v | 2,547 | 4.73 ms (0.126 ms opt) | 7.24 ms | 11.07 ms | 2.66 s |
| i2c.v | 2,480 | 4.75 ms (0.182 ms opt) | 7.23 ms | 12.09 ms | 2.66 s |
| bar.v | 5,526 | 11.10 ms (0.346 ms opt) | 16.75 ms | 27.37 ms | 3.27 s |
| max.v | 6,025 | 11.47 ms (0.370 ms opt) | 16.79 ms | 27.84 ms | 2.91 s |
| arbiter.v | 23,618 | 46.27 ms (1.306 ms opt) | 83.36 ms | 127.76 ms | 8.75 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| ctrl.v | 68.80 ms | 52.97 ms | 109.29 ms | 2873.87 ms | 412.58 ms | 3.11 ms |
| int2float.v | 83.73 ms | 93.74 ms | 119.08 ms | 3300.09 ms | 511.98 ms | 5.26 ms |
| dec.v | 15.18 ms | 23.72 ms | 20.02 ms | 1373.23 ms | 171.67 ms | 3.62 ms |
| router.v | 92.29 ms | 69.09 ms | 138.89 ms | 3691.30 ms | 761.26 ms | 7.12 ms |
| cavlc.v | 263.47 ms | 266.64 ms | 353.81 ms | 9770.82 ms | 1415.50 ms | 8.58 ms |
| priority.v | 300.72 ms | 248.80 ms | 408.46 ms | 15.05 s | 13.54 s | 44.44 ms |
| adder.v | 616.52 ms | 361.63 ms | 830.20 ms | 26.76 s | 3739.31 ms | 64.29 ms |
| i2c.v | 420.46 ms | 511.72 ms | 587.18 ms | 15.41 s | 2888.70 ms | 36.47 ms |
| bar.v | 911.04 ms | 869.87 ms | 1081.81 ms | 63.62 s | 7137.06 ms | 58.79 ms |
| max.v | 1787.64 ms | 1355.91 ms | 2179.65 ms | 71.76 s | 12.51 s | 103.45 ms |
| arbiter.v | 2968.69 ms | 2232.29 ms | 4103.04 ms | 169.35 s | 17.91 s | 170.79 ms |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| ctrl.v | 6.00x | 7.79x | 3.78x | 0.14x | 1.00x | 132.54x |
| int2float.v | 6.11x | 5.46x | 4.30x | 0.16x | 1.00x | 97.37x |
| dec.v | 11.31x | 7.24x | 8.57x | 0.13x | 1.00x | 47.40x |
| router.v | 8.25x | 11.02x | 5.48x | 0.21x | 1.00x | 106.92x |
| cavlc.v | 5.37x | 5.31x | 4.00x | 0.14x | 1.00x | 164.89x |
| priority.v | 45.03x | 54.43x | 33.16x | 0.90x | 1.00x | 304.77x |
| adder.v | 6.07x | 10.34x | 4.50x | 0.14x | 1.00x | 58.17x |
| i2c.v | 6.87x | 5.65x | 4.92x | 0.19x | 1.00x | 79.22x |
| bar.v | 7.83x | 8.20x | 6.60x | 0.11x | 1.00x | 121.40x |
| max.v | 7.00x | 9.23x | 5.74x | 0.17x | 1.00x | 120.94x |
| arbiter.v | 6.03x | 8.02x | 4.36x | 0.11x | 1.00x | 104.84x |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `8.21x`
- **rx-sweep (Linear Compiled):** `9.08x`
- **rx-oop (OOP Graph):** `6.01x`
- **Pure Python Engine:** `0.17x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `108.00x`

### Cross-Engine Comparisons

- **Cython Reactor (`rx-prop`) vs Pure Python:** `47.56x` faster
- **Cython Reactor (`rx-sweep`) vs Pure Python:** `52.62x` faster
- **Reactor Sweep vs Propagate Ratio:** `1.11x` (sweep faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | IPC | Cycles | Instructions | L1 Loads | L1 Hit% | L2 Hit% | LLC Misses | Brn Miss% |
|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| ctrl.v | rx-prop | 3.02 | 274.82M | 828.65M | 308.31M | 99.53% | 97.68% | 33.01K | 3.98% |
| ctrl.v | rx-sweep (Linear) | 2.59 | 194.63M | 504.66M | 186.72M | 99.46% | 99.79% | 2.02K | 4.02% |
| ctrl.v | rx-oop (OOP Engine) | 1.74 | 435.91M | 759.06M | 536.07M | 99.08% | 99.61% | 29.45K | 7.50% |
| ctrl.v | Pure Python Engine | 5.08 | 97.80M | 496.68M | 222.45M | 99.64% | 98.96% | 9.56K | 0.27% |
| ctrl.v | Icarus Verilog | 3.49 | 1.65B | 5.76B | 2.74B | 98.34% | 99.98% | 9.17K | 1.08% |
| int2float.v | rx-prop | 2.48 | 330.39M | 817.85M | 333.59M | 99.29% | 99.55% | 12.06K | 5.53% |
| int2float.v | rx-sweep (Linear) | 1.79 | 376.17M | 674.24M | 289.11M | 98.82% | 99.71% | 13.32K | 6.70% |
| int2float.v | rx-oop (OOP Engine) | 1.67 | 473.29M | 789.55M | 571.66M | 98.42% | 99.89% | 10.11K | 7.78% |
| int2float.v | Pure Python Engine | 5.50 | 98.33M | 540.69M | 228.16M | 99.62% | 98.62% | 11.58K | 0.34% |
| int2float.v | Icarus Verilog | 3.15 | 2.05B | 6.44B | 3.19B | 97.74% | 99.99% | 8.55K | 1.34% |
| dec.v | rx-prop | 4.80 | 55.04M | 263.94M | 75.22M | 99.21% | 99.18% | 3.30K | 1.23% |
| dec.v | rx-sweep (Linear) | 3.94 | 85.73M | 337.73M | 109.37M | 98.85% | 98.19% | 22.90K | 1.98% |
| dec.v | rx-oop (OOP Engine) | 4.08 | 61.71M | 251.78M | 109.43M | 99.01% | 99.39% | 7.52K | 1.61% |
| dec.v | Pure Python Engine | 5.75 | 31.66M | 181.94M | 80.83M | 99.60% | 99.17% | 2.70K | 0.13% |
| dec.v | Icarus Verilog | 4.05 | 688.63M | 2.79B | 1.20B | 97.81% | 99.94% | 15.71K | 0.71% |
| router.v | rx-prop | 2.44 | 402.17M | 980.50M | 425.22M | 98.77% | 97.32% | 138.26K | 4.99% |
| router.v | rx-sweep (Linear) | 2.67 | 320.07M | 853.21M | 350.87M | 98.49% | 97.28% | 144.33K | 2.57% |
| router.v | rx-oop (OOP Engine) | 1.57 | 593.72M | 934.08M | 659.61M | 97.71% | 99.39% | 96.32K | 6.90% |
| router.v | Pure Python Engine | 4.78 | 128.95M | 616.13M | 275.07M | 99.67% | 98.86% | 10.20K | 0.39% |
| router.v | Icarus Verilog | 3.49 | 3.04B | 10.60B | 4.96B | 98.19% | 99.91% | 81.94K | 0.98% |
| cavlc.v | rx-prop | 2.30 | 1.06B | 2.43B | 1.02B | 96.12% | 99.97% | 9.65K | 5.46% |
| cavlc.v | rx-sweep (Linear) | 1.74 | 1.04B | 1.81B | 771.77M | 92.16% | 99.99% | 12.79K | 6.72% |
| cavlc.v | rx-oop (OOP Engine) | 1.62 | 1.41B | 2.29B | 1.68B | 96.43% | 99.92% | 49.23K | 7.70% |
| cavlc.v | Pure Python Engine | 4.70 | 376.66M | 1.77B | 786.21M | 99.48% | 96.45% | 167.66K | 0.21% |
| cavlc.v | Icarus Verilog | 3.04 | 5.69B | 17.30B | 8.87B | 96.22% | 99.92% | 298.16K | 1.28% |
| priority.v | rx-prop | 3.04 | 1.31B | 3.98B | 1.55B | 95.03% | 99.59% | 316.54K | 2.54% |
| priority.v | rx-sweep (Linear) | 2.78 | 1.10B | 3.05B | 1.18B | 92.04% | 99.70% | 281.89K | 2.46% |
| priority.v | rx-oop (OOP Engine) | 2.21 | 1.70B | 3.74B | 2.26B | 94.51% | 99.80% | 259.99K | 3.37% |
| priority.v | Pure Python Engine | 4.51 | 579.84M | 2.62B | 1.18B | 99.61% | 79.89% | 936.91K | 0.26% |
| priority.v | Icarus Verilog | 3.75 | 54.64B | 204.97B | 99.11B | 97.38% | 99.79% | 5.57M | 0.70% |
| adder.v | rx-prop | 2.21 | 2.70B | 5.98B | 2.66B | 94.87% | 99.52% | 648.63K | 4.68% |
| adder.v | rx-sweep (Linear) | 2.94 | 1.66B | 4.87B | 1.93B | 92.15% | 99.60% | 598.44K | 1.99% |
| adder.v | rx-oop (OOP Engine) | 1.56 | 3.51B | 5.47B | 3.97B | 94.88% | 99.71% | 618.38K | 6.13% |
| adder.v | Pure Python Engine | 4.70 | 1.03B | 4.85B | 2.20B | 99.63% | 77.46% | 1.86M | 0.24% |
| adder.v | Icarus Verilog | 3.79 | 15.05B | 57.01B | 26.89B | 96.97% | 99.35% | 5.32M | 0.67% |
| i2c.v | rx-prop | 2.30 | 1.81B | 4.15B | 1.79B | 92.94% | 99.65% | 443.56K | 4.50% |
| i2c.v | rx-sweep (Linear) | 1.72 | 2.18B | 3.75B | 1.67B | 91.84% | 99.67% | 446.92K | 6.19% |
| i2c.v | rx-oop (OOP Engine) | 1.56 | 2.44B | 3.81B | 2.76B | 94.57% | 99.77% | 337.19K | 6.64% |
| i2c.v | Pure Python Engine | 4.67 | 576.64M | 2.69B | 1.21B | 99.55% | 80.80% | 1.06M | 0.23% |
| i2c.v | Icarus Verilog | 3.41 | 11.58B | 39.51B | 18.99B | 96.75% | 98.85% | 7.09M | 0.93% |
| bar.v | rx-prop | 3.74 | 3.75B | 14.00B | 4.72B | 88.62% | 99.94% | 340.08K | 0.39% |
| bar.v | rx-sweep (Linear) | 2.28 | 3.59B | 8.20B | 3.36B | 91.36% | 99.91% | 277.16K | 4.23% |
| bar.v | rx-oop (OOP Engine) | 2.75 | 4.43B | 12.17B | 6.51B | 91.80% | 99.86% | 742.62K | 0.76% |
| bar.v | Pure Python Engine | 4.44 | 453.70M | 2.02B | 909.46M | 99.46% | 55.06% | 2.21M | 0.12% |
| bar.v | Icarus Verilog | 3.69 | 28.62B | 105.69B | 48.85B | 94.54% | 83.69% | 434.78M | 0.35% |
| max.v | rx-prop | 2.36 | 7.61B | 17.97B | 7.58B | 91.12% | 99.75% | 1.69M | 3.61% |
| max.v | rx-sweep (Linear) | 1.92 | 5.91B | 11.33B | 5.07B | 91.85% | 99.61% | 1.61M | 5.14% |
| max.v | rx-oop (OOP Engine) | 1.68 | 9.18B | 15.46B | 10.81B | 93.02% | 98.41% | 11.92M | 5.00% |
| max.v | Pure Python Engine | 4.44 | 531.03M | 2.36B | 1.05B | 99.54% | 56.71% | 2.13M | 0.21% |
| max.v | Icarus Verilog | 3.28 | 50.28B | 164.74B | 82.36B | 96.34% | 83.01% | 512.00M | 0.81% |
| arbiter.v | rx-prop | 2.63 | 12.12B | 31.86B | 11.11B | 87.04% | 82.55% | 251.31M | 0.91% |
| arbiter.v | rx-sweep (Linear) | 3.15 | 9.18B | 28.90B | 9.60B | 89.14% | 87.81% | 127.25M | 1.27% |
| arbiter.v | rx-oop (OOP Engine) | 1.81 | 16.66B | 30.20B | 17.30B | 91.25% | 58.69% | 625.25M | 1.64% |
| arbiter.v | Pure Python Engine | 4.07 | 603.60M | 2.46B | 1.08B | 99.35% | 45.16% | 3.83M | 0.07% |
| arbiter.v | Icarus Verilog | 3.23 | 71.54B | 231.32B | 110.79B | 94.05% | 50.34% | 3.27B | 0.24% |

---

# master_test/master_test_report_20260918_175159.md

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
| sin.v | 8,947 | 11.79 MB (43.0 MB peak) | N/A | 5.28 MB (13.1 MB peak) | 0.81 MB (4.5 MB peak) |
| voter.v | 27,720 | 27.64 MB (59.0 MB peak) | N/A | 17.87 MB (25.8 MB peak) | 1.15 MB (4.8 MB peak) |
| square.v | 35,687 | 35.51 MB (66.9 MB peak) | N/A | 22.62 MB (30.4 MB peak) | 1.25 MB (4.9 MB peak) |
| sqrt.v | 41,234 | 42.33 MB (73.7 MB peak) | N/A | 27.16 MB (34.9 MB peak) | 1.07 MB (4.8 MB peak) |
| multiplier.v | 50,760 | 51.15 MB (82.5 MB peak) | N/A | 33.04 MB (40.9 MB peak) | 1.14 MB (4.8 MB peak) |
| log2.v | 54,531 | 52.51 MB (83.8 MB peak) | N/A | 35.47 MB (43.3 MB peak) | 1.03 MB (4.7 MB peak) |
| mem_ctrl.v | 84,974 | 80.60 MB (111.9 MB peak) | N/A | 55.39 MB (63.2 MB peak) | 1.43 MB (5.1 MB peak) |
| div.v | 101,859 | 97.48 MB (128.8 MB peak) | N/A | 67.38 MB (75.2 MB peak) | 1.66 MB (5.4 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| sin.v | 8,947 | 6.73 ms (0.643 ms opt) | N/A | 38.89 ms | 2.91 s |
| voter.v | 27,720 | 20.67 ms (1.736 ms opt) | N/A | 131.78 ms | 4.48 s |
| square.v | 35,687 | 26.32 ms (3.470 ms opt) | N/A | 183.69 ms | 5.48 s |
| sqrt.v | 41,234 | 31.58 ms (3.427 ms opt) | N/A | 221.73 ms | 5.81 s |
| multiplier.v | 50,760 | 41.15 ms (6.024 ms opt) | N/A | 272.13 ms | 6.74 s |
| log2.v | 54,531 | 44.70 ms (7.819 ms opt) | N/A | 325.89 ms | 7.84 s |
| mem_ctrl.v | 84,974 | 82.22 ms (16.187 ms opt) | N/A | 899.49 ms | 13.11 s |
| div.v | 101,859 | 120.31 ms (15.571 ms opt) | N/A | 639.62 ms | 21.72 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| sin.v | 330.62 ms | 16.86 ms | 482.14 ms | N/A | 1585.64 ms | 1.01 ms |
| voter.v | 277.63 ms | 44.86 ms | 413.72 ms | N/A | 1422.17 ms | 2.90 ms |
| square.v | 242.89 ms | 64.52 ms | 342.75 ms | N/A | 1083.82 ms | 5.28 ms |
| sqrt.v | 29.28 s | 74.02 ms | 35.56 s | N/A | 131.40 s | 3.26 ms |
| multiplier.v | 1830.54 ms | 86.05 ms | 2857.59 ms | N/A | 9242.09 ms | 3.44 ms |
| log2.v | 8450.32 ms | 95.36 ms | 13.10 s | N/A | 43.52 s | 5.20 ms |
| mem_ctrl.v | 255.58 ms | 178.04 ms | 423.93 ms | N/A | 1979.69 ms | 27.80 ms |
| div.v | 482.15 ms | 131.12 ms | 612.07 ms | N/A | 3157.82 ms | 44.70 ms |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| sin.v | 4.80x | 94.06x | 3.29x | N/A | 1.00x | 1569.91x |
| voter.v | 5.12x | 31.70x | 3.44x | N/A | 1.00x | 490.88x |
| square.v | 4.46x | 16.80x | 3.16x | N/A | 1.00x | 205.12x |
| sqrt.v | 4.49x | 1775.16x | 3.70x | N/A | 1.00x | 40353.97x |
| multiplier.v | 5.05x | 107.40x | 3.23x | N/A | 1.00x | 2683.25x |
| log2.v | 5.15x | 456.40x | 3.32x | N/A | 1.00x | 8363.75x |
| mem_ctrl.v | 7.75x | 11.12x | 4.67x | N/A | 1.00x | 71.22x |
| div.v | 6.55x | 24.08x | 5.16x | N/A | 1.00x | 70.65x |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `5.33x`
- **rx-sweep (Linear Compiled):** `76.45x`
- **rx-oop (OOP Graph):** `3.69x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `959.83x`

### Cross-Engine Comparisons

- **Reactor Sweep vs Propagate Ratio:** `14.35x` (sweep faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | IPC | Cycles | Instructions | L1 Loads | L1 Hit% | L2 Hit% | LLC Misses | Brn Miss% |
|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| sin.v | rx-prop | 1.75 | 1.33B | 2.33B | 1.02B | 92.10% | 99.67% | 271.74K | 8.69% |
| sin.v | rx-sweep (Linear) | 2.03 | 53.33M | 108.11M | 38.50M | 92.02% | 96.39% | 110.19K | 6.53% |
| sin.v | rx-oop (OOP Engine) | 1.28 | 1.93B | 2.48B | 1.93B | 94.18% | 99.13% | 968.99K | 11.24% |
| sin.v | Icarus Verilog | 2.51 | 6.39B | 16.04B | 9.06B | 95.72% | 88.19% | 46.22M | 1.61% |
| voter.v | rx-prop | 1.63 | 1.12B | 1.83B | 808.34M | 91.97% | 88.37% | 7.52M | 9.01% |
| voter.v | rx-sweep (Linear) | 2.29 | 179.67M | 411.46M | 151.95M | 91.21% | 86.71% | 1.80M | 3.98% |
| voter.v | rx-oop (OOP Engine) | 1.20 | 1.67B | 1.99B | 1.57B | 94.46% | 84.98% | 13.12M | 11.06% |
| voter.v | Icarus Verilog | 2.40 | 5.73B | 13.73B | 7.97B | 96.52% | 63.27% | 102.11M | 1.60% |
| square.v | rx-prop | 1.59 | 943.10M | 1.50B | 664.77M | 91.31% | 86.72% | 7.75M | 8.62% |
| square.v | rx-sweep (Linear) | 1.93 | 246.46M | 474.48M | 187.56M | 91.26% | 82.19% | 2.92M | 5.36% |
| square.v | rx-oop (OOP Engine) | 1.10 | 1.37B | 1.50B | 1.23B | 94.36% | 81.06% | 13.23M | 10.93% |
| square.v | Icarus Verilog | 2.16 | 4.34B | 9.37B | 5.66B | 95.91% | 57.17% | 99.41M | 1.58% |
| sqrt.v | rx-prop | 1.36 | 117.87B | 160.18B | 69.99B | 90.42% | 46.82% | 3.56B | 6.96% |
| sqrt.v | rx-sweep (Linear) | 2.27 | 286.36M | 648.95M | 255.41M | 92.18% | 78.75% | 4.27M | 3.69% |
| sqrt.v | rx-oop (OOP Engine) | 1.02 | 142.61B | 145.41B | 116.38B | 94.04% | 33.70% | 4.60B | 9.06% |
| sqrt.v | Icarus Verilog | 1.83 | 527.38B | 962.88B | 613.52B | 95.70% | 21.95% | 20.60B | 1.50% |
| multiplier.v | rx-prop | 1.54 | 7.37B | 11.37B | 5.16B | 91.31% | 79.47% | 92.97M | 8.18% |
| multiplier.v | rx-sweep (Linear) | 2.21 | 322.46M | 711.66M | 282.90M | 90.83% | 78.05% | 5.72M | 3.73% |
| multiplier.v | rx-oop (OOP Engine) | 1.05 | 11.47B | 12.02B | 9.98B | 94.15% | 63.49% | 213.39M | 11.00% |
| multiplier.v | Icarus Verilog | 1.87 | 37.14B | 69.55B | 44.51B | 96.23% | 28.98% | 1.19B | 1.60% |
| log2.v | rx-prop | 1.47 | 33.73B | 49.44B | 22.25B | 91.00% | 61.77% | 767.13M | 7.71% |
| log2.v | rx-sweep (Linear) | 2.04 | 363.31M | 741.76M | 287.82M | 91.70% | 81.80% | 4.41M | 4.79% |
| log2.v | rx-oop (OOP Engine) | 0.98 | 52.55B | 51.40B | 43.24B | 94.35% | 46.19% | 1.32B | 10.42% |
| log2.v | Icarus Verilog | 1.84 | 174.47B | 320.44B | 204.55B | 96.09% | 22.19% | 6.22B | 1.50% |
| mem_ctrl.v | rx-prop | 1.55 | 1.01B | 1.56B | 668.60M | 90.12% | 47.66% | 34.72M | 5.38% |
| mem_ctrl.v | rx-sweep (Linear) | 1.63 | 705.46M | 1.15B | 497.93M | 91.16% | 74.40% | 11.28M | 6.23% |
| mem_ctrl.v | rx-oop (OOP Engine) | 1.08 | 1.71B | 1.85B | 1.45B | 93.70% | 38.62% | 55.89M | 7.32% |
| mem_ctrl.v | Icarus Verilog | 1.85 | 7.98B | 14.75B | 8.48B | 95.93% | 20.13% | 276.13M | 0.98% |
| div.v | rx-prop | 1.62 | 1.93B | 3.12B | 1.29B | 90.72% | 55.85% | 52.86M | 4.91% |
| div.v | rx-sweep (Linear) | 2.84 | 514.02M | 1.46B | 503.76M | 90.77% | 81.89% | 8.42M | 2.06% |
| div.v | rx-oop (OOP Engine) | 1.22 | 2.44B | 2.97B | 2.09B | 93.19% | 49.42% | 72.87M | 5.64% |
| div.v | Icarus Verilog | 1.68 | 12.74B | 21.40B | 11.72B | 95.37% | 39.92% | 326.59M | 0.79% |

---

# master_test/master_test_report_20260918_193450.md

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
| s27.v | 19 | 0.44 MB (31.7 MB peak) | 0.18 MB (33.3 MB peak) | 0.07 MB (7.9 MB peak) | 0.71 MB (4.4 MB peak) |
| s420.v | 254 | 0.80 MB (32.2 MB peak) | 0.64 MB (33.7 MB peak) | 0.15 MB (8.0 MB peak) | 0.71 MB (4.4 MB peak) |
| s382.v | 189 | 0.82 MB (32.2 MB peak) | 0.65 MB (33.6 MB peak) | 0.04 MB (7.9 MB peak) | 0.71 MB (4.4 MB peak) |
| s641.v | 458 | 1.08 MB (32.4 MB peak) | 0.93 MB (34.0 MB peak) | 0.25 MB (8.1 MB peak) | 0.82 MB (4.4 MB peak) |
| s713.v | 471 | 1.08 MB (32.4 MB peak) | 0.94 MB (34.0 MB peak) | 0.41 MB (8.1 MB peak) | 0.71 MB (4.4 MB peak) |
| s1238.v | 555 | 1.15 MB (32.6 MB peak) | 1.05 MB (34.1 MB peak) | 0.34 MB (8.2 MB peak) | 0.61 MB (4.3 MB peak) |
| s1423.v | 754 | 2.05 MB (33.4 MB peak) | 2.23 MB (35.3 MB peak) | 0.74 MB (8.6 MB peak) | 0.68 MB (4.4 MB peak) |
| s1488.v | 687 | 1.19 MB (32.6 MB peak) | 1.06 MB (34.0 MB peak) | 0.26 MB (8.1 MB peak) | 0.61 MB (4.3 MB peak) |
| s5378.v | 3,043 | 5.52 MB (36.9 MB peak) | 6.72 MB (39.8 MB peak) | 2.17 MB (10.0 MB peak) | 0.73 MB (4.4 MB peak) |
| s9234.v | 5,884 | 8.37 MB (39.6 MB peak) | 11.56 MB (44.6 MB peak) | 4.32 MB (12.2 MB peak) | 0.75 MB (4.4 MB peak) |
| s13207.v | 8,804 | 17.77 MB (49.0 MB peak) | 18.62 MB (51.7 MB peak) | 7.97 MB (15.8 MB peak) | 0.77 MB (4.5 MB peak) |
| s15850.v | 10,534 | 17.68 MB (49.1 MB peak) | 18.95 MB (52.0 MB peak) | 8.57 MB (16.4 MB peak) | 0.82 MB (4.5 MB peak) |
| s35932.v | 18,149 | 43.52 MB (74.9 MB peak) | 44.83 MB (77.8 MB peak) | 18.81 MB (26.7 MB peak) | 0.91 MB (4.6 MB peak) |
| s38584.v | 21,022 | 44.33 MB (75.7 MB peak) | 43.75 MB (76.8 MB peak) | 20.08 MB (27.9 MB peak) | 0.80 MB (4.5 MB peak) |
| s38417.v | 23,950 | 47.05 MB (78.4 MB peak) | 51.81 MB (84.9 MB peak) | 22.48 MB (30.3 MB peak) | 0.82 MB (4.5 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| s27.v | 19 | 0.52 ms (0.007 ms opt) | 0.54 ms | 2.41 ms | 2.53 s |
| s420.v | 254 | 0.79 ms (0.041 ms opt) | 9.88 ms | 3.01 ms | 2.58 s |
| s382.v | 189 | 0.57 ms (0.042 ms opt) | 10.11 ms | 3.14 ms | 2.54 s |
| s641.v | 458 | 0.75 ms (0.059 ms opt) | 10.68 ms | 4.17 ms | 2.62 s |
| s713.v | 471 | 0.73 ms (0.060 ms opt) | 10.45 ms | 3.84 ms | 2.57 s |
| s1238.v | 555 | 0.80 ms (0.083 ms opt) | 10.52 ms | 4.55 ms | 2.53 s |
| s1423.v | 754 | 1.33 ms (0.120 ms opt) | 4.04 ms | 5.89 ms | 2.60 s |
| s1488.v | 687 | 0.82 ms (0.082 ms opt) | 10.40 ms | 5.00 ms | 2.61 s |
| s5378.v | 3,043 | 3.63 ms (0.366 ms opt) | 18.12 ms | 18.70 ms | 2.68 s |
| s9234.v | 5,884 | 6.65 ms (0.685 ms opt) | 23.39 ms | 32.58 ms | 2.71 s |
| s13207.v | 8,804 | 12.56 ms (1.807 ms opt) | 35.27 ms | 60.81 ms | 2.83 s |
| s15850.v | 10,534 | 12.79 ms (1.452 ms opt) | 36.46 ms | 68.85 ms | 3.00 s |
| s35932.v | 18,149 | 29.29 ms (3.892 ms opt) | 88.33 ms | 114.95 ms | 3.90 s |
| s38584.v | 21,022 | 30.32 ms (6.549 ms opt) | 89.45 ms | 176.27 ms | 5.79 s |
| s38417.v | 23,950 | 33.34 ms (5.632 ms opt) | 94.90 ms | 168.02 ms | 4.65 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| s27.v | 2.34 ms | 1.96 ms | 2.85 ms | 2484.46 ms | 20.71 ms | 0.58 ms |
| s420.v | 9.63 ms | 10.70 ms | 15.56 ms | 11.82 s | 71.81 ms | 1.63 ms |
| s382.v | 10.25 ms | 9.98 ms | 16.36 ms | 13.83 s | 38.64 ms | 0.71 ms |
| s641.v | 19.81 ms | 18.63 ms | 29.37 ms | 19.44 s | 137.23 ms | 2.64 ms |
| s713.v | 20.64 ms | 19.04 ms | 32.54 ms | 19.83 s | 140.97 ms | 2.10 ms |
| s1238.v | 34.58 ms | 44.75 ms | 57.58 ms | 29.74 s | 169.13 ms | 3.99 ms |
| s1423.v | 59.71 ms | 57.30 ms | 91.95 ms | 57.24 s | 171.37 ms | 3.30 ms |
| s1488.v | 13.87 ms | 15.96 ms | 25.58 ms | 15.74 s | 113.05 ms | 3.17 ms |
| s5378.v | 176.71 ms | 175.58 ms | 231.59 ms | 835.02 s | 485.77 ms | 6.12 ms |
| s9234.v | 187.88 ms | 198.36 ms | 269.60 ms | 1065.77 s | 594.39 ms | 4.47 ms |
| s13207.v | 451.16 ms | 529.21 ms | 715.91 ms | 2477.43 s | 1051.00 ms | 11.76 ms |
| s15850.v | 428.28 ms | 461.09 ms | 692.95 ms | 2458.01 s | 1382.57 ms | 13.95 ms |
| s35932.v | 1584.95 ms | 1382.45 ms | 2260.93 ms | 10618.39 s | 4173.99 ms | 38.88 ms |
| s38584.v | 1883.10 ms | 2010.67 ms | 2817.92 ms | 9097.37 s | 4676.35 ms | 36.47 ms |
| s38417.v | 1234.41 ms | 1227.31 ms | 1953.28 ms | 15499.66 s | 2911.26 ms | 33.63 ms |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| s27.v | 8.87x | 10.58x | 7.28x | 0.01x | 1.00x | 35.53x |
| s420.v | 7.46x | 6.71x | 4.61x | 0.01x | 1.00x | 43.99x |
| s382.v | 3.77x | 3.87x | 2.36x | 0.00x | 1.00x | 54.75x |
| s641.v | 6.93x | 7.37x | 4.67x | 0.01x | 1.00x | 52.00x |
| s713.v | 6.83x | 7.40x | 4.33x | 0.01x | 1.00x | 67.14x |
| s1238.v | 4.89x | 3.78x | 2.94x | 0.01x | 1.00x | 42.44x |
| s1423.v | 2.87x | 2.99x | 1.86x | 0.00x | 1.00x | 51.93x |
| s1488.v | 8.15x | 7.08x | 4.42x | 0.01x | 1.00x | 35.69x |
| s5378.v | 2.75x | 2.77x | 2.10x | 0.00x | 1.00x | 79.39x |
| s9234.v | 3.16x | 3.00x | 2.20x | 0.00x | 1.00x | 132.86x |
| s13207.v | 2.33x | 1.99x | 1.47x | 0.00x | 1.00x | 89.34x |
| s15850.v | 3.23x | 3.00x | 2.00x | 0.00x | 1.00x | 99.13x |
| s35932.v | 2.63x | 3.02x | 1.85x | 0.00x | 1.00x | 107.37x |
| s38584.v | 2.48x | 2.33x | 1.66x | 0.00x | 1.00x | 128.24x |
| s38417.v | 2.36x | 2.37x | 1.49x | 0.00x | 1.00x | 86.57x |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `4.06x`
- **rx-sweep (Linear Compiled):** `3.98x`
- **rx-oop (OOP Graph):** `2.66x`
- **Pure Python Engine:** `0.00x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `67.27x`

### Cross-Engine Comparisons

- **Cython Reactor (`rx-prop`) vs Pure Python:** `2408.87x` faster
- **Cython Reactor (`rx-sweep`) vs Pure Python:** `2357.86x` faster
- **Reactor Sweep vs Propagate Ratio:** `0.98x` (propagate faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | IPC | Cycles | Instructions | L1 Loads | L1 Hit% | L2 Hit% | LLC Misses | Brn Miss% |
|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| s27.v | rx-prop | 0.00 | 0 | 0 | 325.59K | 99.64% | 0.00% | 1.58K | 1.14% |
| s27.v | rx-sweep (Linear) | 13.94 | 1.38M | 19.19M | 4.84M | 97.59% | 97.13% | 3.36K | 0.35% |
| s27.v | rx-oop (OOP Engine) | 5.89 | 7.84M | 46.19M | 11.30M | 98.88% | 91.46% | 14.48K | 0.75% |
| s27.v | Pure Python Engine | 8.10 | 7.77M | 62.89M | 10.65M | 99.89% | 98.77% | 2.16K | 0.29% |
| s27.v | Icarus Verilog | 3.56 | 80.90M | 288.01M | 113.96M | 99.97% | 86.47% | 1.58K | 1.21% |
| s420.v | rx-prop | 5.69 | 30.37M | 172.69M | 54.89M | 99.39% | 95.66% | 14.61K | 0.91% |
| s420.v | rx-sweep (Linear) | 4.23 | 32.10M | 135.72M | 50.77M | 99.83% | 94.86% | 4.55K | 1.18% |
| s420.v | rx-oop (OOP Engine) | 2.93 | 49.77M | 145.91M | 85.86M | 99.17% | 98.55% | 7.30K | 2.62% |
| s420.v | Pure Python Engine | 4.92 | 96.12M | 473.06M | 208.99M | 99.50% | 98.50% | 18.01K | 0.23% |
| s420.v | Icarus Verilog | 3.71 | 282.92M | 1.05B | 474.25M | 99.27% | 99.92% | 3.95K | 0.82% |
| s382.v | rx-prop | 4.75 | 31.21M | 148.22M | 51.45M | 99.91% | 88.31% | 5.18K | 0.43% |
| s382.v | rx-sweep (Linear) | 4.80 | 32.00M | 153.72M | 44.75M | 99.89% | 93.31% | 2.96K | 0.56% |
| s382.v | rx-oop (OOP Engine) | 2.92 | 63.29M | 184.65M | 106.45M | 99.49% | 97.99% | 7.45K | 1.19% |
| s382.v | Pure Python Engine | 4.95 | 119.63M | 591.65M | 254.60M | 99.51% | 97.93% | 26.52K | 0.30% |
| s382.v | Icarus Verilog | 3.79 | 153.84M | 582.39M | 270.17M | 99.02% | 99.58% | 12.04K | 0.69% |
| s641.v | rx-prop | 3.88 | 74.07M | 287.66M | 89.50M | 99.09% | 98.35% | 13.36K | 2.80% |
| s641.v | rx-sweep (Linear) | 3.81 | 73.28M | 279.35M | 90.75M | 97.85% | 99.05% | 24.13K | 1.35% |
| s641.v | rx-oop (OOP Engine) | 2.22 | 114.01M | 252.94M | 156.36M | 97.72% | 99.45% | 18.14K | 4.28% |
| s641.v | Pure Python Engine | 4.83 | 174.65M | 844.43M | 359.24M | 99.52% | 98.97% | 29.15K | 0.20% |
| s641.v | Icarus Verilog | 3.74 | 531.62M | 1.99B | 915.28M | 98.69% | 99.82% | 10.02K | 0.68% |
| s713.v | rx-prop | 3.54 | 78.72M | 278.86M | 106.71M | 98.54% | 98.41% | 19.21K | 2.23% |
| s713.v | rx-sweep (Linear) | 3.81 | 78.28M | 298.32M | 97.72M | 97.33% | 99.41% | 16.41K | 1.27% |
| s713.v | rx-oop (OOP Engine) | 2.02 | 128.14M | 259.48M | 170.89M | 97.85% | 99.53% | 17.31K | 4.80% |
| s713.v | Pure Python Engine | 4.95 | 178.15M | 881.88M | 384.43M | 99.54% | 99.78% | 3.76K | 0.19% |
| s713.v | Icarus Verilog | 3.76 | 554.32M | 2.08B | 944.51M | 98.67% | 99.96% | 7.64K | 0.72% |
| s1238.v | rx-prop | 2.60 | 129.57M | 336.96M | 131.62M | 96.76% | 99.85% | 6.43K | 4.60% |
| s1238.v | rx-sweep (Linear) | 2.02 | 170.04M | 343.82M | 131.81M | 94.80% | 99.96% | 4.00K | 5.38% |
| s1238.v | rx-oop (OOP Engine) | 1.50 | 224.09M | 335.88M | 246.33M | 96.91% | 99.89% | 9.59K | 8.41% |
| s1238.v | Pure Python Engine | 4.71 | 275.11M | 1.30B | 574.00M | 99.57% | 98.63% | 33.61K | 0.24% |
| s1238.v | Icarus Verilog | 3.06 | 672.72M | 2.06B | 1.01B | 97.24% | 99.93% | 22.75K | 1.45% |
| s1423.v | rx-prop | 3.42 | 236.95M | 810.27M | 266.75M | 92.56% | 99.93% | 14.25K | 1.26% |
| s1423.v | rx-sweep (Linear) | 3.52 | 225.75M | 794.81M | 258.65M | 87.99% | 99.97% | 16.61K | 1.24% |
| s1423.v | rx-oop (OOP Engine) | 2.23 | 346.56M | 772.56M | 440.65M | 92.28% | 99.68% | 108.29K | 2.89% |
| s1423.v | Pure Python Engine | 4.73 | 546.57M | 2.58B | 1.17B | 99.41% | 93.63% | 425.03K | 0.18% |
| s1423.v | Icarus Verilog | 3.73 | 680.55M | 2.54B | 1.20B | 97.52% | 99.93% | 18.47K | 0.73% |
| s1488.v | rx-prop | 3.70 | 61.64M | 227.80M | 72.88M | 97.45% | 99.23% | 14.16K | 1.84% |
| s1488.v | rx-sweep (Linear) | 3.80 | 55.89M | 212.40M | 63.43M | 96.65% | 99.77% | 4.85K | 1.79% |
| s1488.v | rx-oop (OOP Engine) | 1.94 | 96.85M | 188.27M | 127.00M | 97.35% | 99.45% | 19.17K | 5.10% |
| s1488.v | Pure Python Engine | 4.87 | 137.34M | 668.42M | 278.48M | 99.56% | 97.02% | 38.75K | 0.31% |
| s1488.v | Icarus Verilog | 3.20 | 441.22M | 1.41B | 674.76M | 97.46% | 99.97% | 8.38K | 1.20% |
| s5378.v | rx-prop | 3.03 | 713.65M | 2.16B | 754.59M | 90.33% | 99.87% | 94.16K | 2.21% |
| s5378.v | rx-sweep (Linear) | 3.28 | 705.08M | 2.31B | 762.01M | 86.76% | 99.93% | 73.23K | 1.80% |
| s5378.v | rx-oop (OOP Engine) | 2.18 | 936.92M | 2.04B | 1.23B | 91.66% | 99.86% | 149.14K | 3.47% |
| s5378.v | Pure Python Engine | 4.53 | 288.31M | 1.30B | 589.87M | 99.43% | 59.66% | 1.36M | 0.16% |
| s5378.v | Icarus Verilog | 3.40 | 1.91B | 6.51B | 3.18B | 96.99% | 96.90% | 2.95M | 0.86% |
| s9234.v | rx-prop | 3.16 | 739.77M | 2.34B | 822.54M | 89.57% | 99.83% | 152.88K | 1.82% |
| s9234.v | rx-sweep (Linear) | 3.46 | 801.64M | 2.78B | 923.27M | 85.39% | 99.42% | 784.40K | 1.32% |
| s9234.v | rx-oop (OOP Engine) | 2.16 | 1.08B | 2.33B | 1.41B | 91.64% | 99.66% | 398.52K | 3.25% |
| s9234.v | Pure Python Engine | 4.09 | 386.15M | 1.58B | 724.21M | 99.44% | 43.39% | 2.28M | 0.17% |
| s9234.v | Icarus Verilog | 3.25 | 2.38B | 7.74B | 3.98B | 96.87% | 88.91% | 13.83M | 0.76% |
| s13207.v | rx-prop | 3.26 | 1.83B | 5.96B | 2.05B | 87.73% | 98.80% | 2.97M | 1.51% |
| s13207.v | rx-sweep (Linear) | 3.17 | 2.14B | 6.78B | 2.31B | 86.74% | 92.64% | 22.65M | 1.65% |
| s13207.v | rx-oop (OOP Engine) | 2.00 | 2.88B | 5.78B | 3.49B | 90.40% | 83.40% | 55.71M | 2.49% |
| s13207.v | Pure Python Engine | 4.21 | 892.96M | 3.76B | 1.68B | 99.42% | 19.94% | 7.83M | 0.29% |
| s13207.v | Icarus Verilog | 3.17 | 4.20B | 13.33B | 7.04B | 96.89% | 74.35% | 56.15M | 0.60% |
| s15850.v | rx-prop | 3.20 | 1.73B | 5.54B | 1.92B | 88.58% | 97.85% | 4.73M | 1.49% |
| s15850.v | rx-sweep (Linear) | 3.37 | 1.85B | 6.25B | 2.07B | 86.02% | 92.86% | 20.54M | 1.28% |
| s15850.v | rx-oop (OOP Engine) | 2.00 | 2.79B | 5.57B | 3.44B | 91.56% | 83.65% | 47.52M | 2.72% |
| s15850.v | Pure Python Engine | 4.19 | 863.43M | 3.62B | 1.61B | 99.41% | 24.60% | 7.05M | 0.17% |
| s15850.v | Icarus Verilog | 3.04 | 5.54B | 16.84B | 8.85B | 96.74% | 65.87% | 98.55M | 0.64% |
| s35932.v | rx-prop | 3.30 | 6.33B | 20.90B | 6.86B | 85.71% | 82.37% | 172.88M | 0.21% |
| s35932.v | rx-sweep (Linear) | 3.92 | 5.51B | 21.59B | 6.72B | 85.80% | 87.54% | 119.10M | 0.24% |
| s35932.v | rx-oop (OOP Engine) | 2.27 | 9.05B | 20.58B | 11.34B | 88.76% | 68.98% | 395.77M | 0.39% |
| s35932.v | Pure Python Engine | 3.85 | 3.83B | 14.75B | 6.60B | 99.39% | 22.71% | 31.29M | 0.11% |
| s35932.v | Icarus Verilog | 3.90 | 16.75B | 65.26B | 30.59B | 94.53% | 71.19% | 481.32M | 0.10% |
| s38584.v | rx-prop | 2.35 | 7.50B | 17.60B | 6.40B | 88.11% | 78.02% | 167.80M | 2.64% |
| s38584.v | rx-sweep (Linear) | 2.38 | 8.04B | 19.14B | 7.08B | 88.18% | 84.29% | 131.73M | 2.78% |
| s38584.v | rx-oop (OOP Engine) | 1.54 | 11.31B | 17.36B | 11.37B | 91.09% | 55.52% | 450.94M | 3.62% |
| s38584.v | Pure Python Engine | 3.45 | 3.29B | 11.37B | 5.14B | 99.43% | 14.82% | 24.99M | 0.18% |
| s38584.v | Icarus Verilog | 2.47 | 18.71B | 46.13B | 26.07B | 95.82% | 50.12% | 543.07M | 0.98% |
| s38417.v | rx-prop | 3.05 | 4.93B | 15.03B | 5.08B | 86.72% | 80.53% | 131.27M | 0.84% |
| s38417.v | rx-sweep (Linear) | 3.51 | 4.90B | 17.17B | 5.55B | 85.74% | 85.94% | 111.14M | 0.87% |
| s38417.v | rx-oop (OOP Engine) | 1.94 | 7.84B | 15.22B | 8.85B | 89.86% | 60.94% | 350.73M | 1.30% |
| s38417.v | Pure Python Engine | 3.91 | 1.21B | 4.71B | 2.10B | 99.39% | 15.90% | 10.74M | 0.16% |
| s38417.v | Icarus Verilog | 3.22 | 11.69B | 37.70B | 19.64B | 96.15% | 63.86% | 273.81M | 0.38% |

---

# master_test/master_test_report_20260918_194929.md

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
| b02.v | 52 | 0.50 MB (31.8 MB peak) | N/A | 0.41 MB (8.2 MB peak) | 0.70 MB (4.4 MB peak) |
| b01.v | 101 | 0.56 MB (31.9 MB peak) | N/A | 0.51 MB (8.4 MB peak) | 0.72 MB (4.4 MB peak) |
| b06.v | 100 | 0.59 MB (32.0 MB peak) | N/A | 0.53 MB (8.3 MB peak) | 0.71 MB (4.4 MB peak) |
| b08.v | 309 | 0.98 MB (32.4 MB peak) | N/A | 1.17 MB (9.1 MB peak) | 0.82 MB (4.4 MB peak) |
| b09.v | 331 | 1.11 MB (32.5 MB peak) | N/A | 1.35 MB (9.2 MB peak) | 0.71 MB (4.4 MB peak) |
| b10.v | 417 | 1.04 MB (32.4 MB peak) | N/A | 1.41 MB (9.2 MB peak) | 0.64 MB (4.3 MB peak) |
| b03.v | 549 | 1.38 MB (32.7 MB peak) | N/A | 1.95 MB (9.7 MB peak) | 0.73 MB (4.4 MB peak) |
| b13.v | 540 | 1.77 MB (33.1 MB peak) | N/A | 2.09 MB (9.9 MB peak) | 0.73 MB (4.4 MB peak) |
| b07.v | 859 | 1.95 MB (33.4 MB peak) | N/A | 3.09 MB (10.9 MB peak) | 0.76 MB (4.4 MB peak) |
| b11.v | 1,046 | 1.85 MB (33.2 MB peak) | N/A | 3.28 MB (11.1 MB peak) | 0.73 MB (4.4 MB peak) |
| b04.v | 1,259 | 2.55 MB (33.8 MB peak) | N/A | 3.81 MB (11.6 MB peak) | 0.75 MB (4.4 MB peak) |
| b05.v | 1,292 | 2.11 MB (33.5 MB peak) | N/A | 3.90 MB (11.8 MB peak) | 0.75 MB (4.4 MB peak) |
| b12.v | 2,937 | 4.98 MB (36.3 MB peak) | N/A | 8.79 MB (16.6 MB peak) | 0.77 MB (4.5 MB peak) |
| b14.v | 10,624 | 15.66 MB (47.0 MB peak) | N/A | 36.77 MB (44.6 MB peak) | 1.06 MB (4.7 MB peak) |
| b15.v | 17,594 | 23.12 MB (56.4 MB peak) | N/A | 56.77 MB (64.7 MB peak) | 1.20 MB (4.9 MB peak) |
| b21.v | 23,092 | 27.86 MB (62.2 MB peak) | N/A | 78.62 MB (86.4 MB peak) | 1.20 MB (4.9 MB peak) |
| b20.v | 23,839 | 29.46 MB (63.8 MB peak) | N/A | 79.86 MB (87.8 MB peak) | 1.12 MB (4.8 MB peak) |
| b22.v | 34,903 | 40.00 MB (77.4 MB peak) | N/A | 119.10 MB (126.9 MB peak) | 1.21 MB (4.9 MB peak) |
| b17.v | 52,250 | 60.29 MB (96.1 MB peak) | N/A | 172.99 MB (180.8 MB peak) | 1.47 MB (5.1 MB peak) |
| b18.v | 132,940 | 138.15 MB (187.1 MB peak) | N/A | 429.13 MB (436.9 MB peak) | 2.32 MB (6.0 MB peak) |
| b19.v | 257,489 | 269.24 MB (337.7 MB peak) | N/A | 827.30 MB (835.2 MB peak) | 3.32 MB (7.0 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| b02.v | 52 | 0.39 ms (0.013 ms opt) | N/A | 4.16 ms | 2.58 s |
| b01.v | 101 | 0.41 ms (0.020 ms opt) | N/A | 4.83 ms | 2.62 s |
| b06.v | 100 | 0.48 ms (0.022 ms opt) | N/A | 5.04 ms | 2.57 s |
| b08.v | 309 | 0.67 ms (0.057 ms opt) | N/A | 7.81 ms | 2.60 s |
| b09.v | 331 | 0.98 ms (0.068 ms opt) | N/A | 7.92 ms | 2.56 s |
| b10.v | 417 | 0.70 ms (0.071 ms opt) | N/A | 9.03 ms | 2.59 s |
| b03.v | 549 | 0.93 ms (0.093 ms opt) | N/A | 10.53 ms | 2.65 s |
| b13.v | 540 | 1.48 ms (0.165 ms opt) | N/A | 11.03 ms | 2.63 s |
| b07.v | 859 | 9.07 ms (0.133 ms opt) | N/A | 15.64 ms | 2.73 s |
| b11.v | 1,046 | 1.51 ms (0.132 ms opt) | N/A | 16.77 ms | 2.67 s |
| b04.v | 1,259 | 1.79 ms (0.185 ms opt) | N/A | 19.15 ms | 2.68 s |
| b05.v | 1,292 | 9.20 ms (0.162 ms opt) | N/A | 19.10 ms | 2.67 s |
| b12.v | 2,937 | 3.64 ms (0.420 ms opt) | N/A | 38.70 ms | 3.02 s |
| b14.v | 10,624 | 19.19 ms (1.399 ms opt) | N/A | 188.70 ms | 6.25 s |
| b15.v | 17,594 | 27.02 ms (2.499 ms opt) | N/A | 297.37 ms | 8.54 s |
| b21.v | 23,092 | 23.91 ms (3.825 ms opt) | N/A | 417.65 ms | 10.75 s |
| b20.v | 23,839 | 33.50 ms (4.040 ms opt) | N/A | 422.13 ms | 11.06 s |
| b22.v | 34,903 | 50.83 ms (12.600 ms opt) | N/A | 663.45 ms | 16.08 s |
| b17.v | 52,250 | 74.94 ms (17.387 ms opt) | N/A | 963.58 ms | 23.88 s |
| b18.v | 132,940 | 284.81 ms (57.880 ms opt) | N/A | 2.52 s | 68.05 s |
| b19.v | 257,489 | 605.41 ms (129.140 ms opt) | N/A | 4.94 s | 164.94 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| b02.v | 4.67 ms | 3.35 ms | 5.49 ms | N/A | 31.24 ms | 0.76 ms |
| b01.v | 6.00 ms | 4.75 ms | 9.46 ms | N/A | 37.41 ms | 0.92 ms |
| b06.v | 8.07 ms | 6.35 ms | 12.72 ms | N/A | 32.93 ms | 2.30 ms |
| b08.v | 12.11 ms | 13.32 ms | 20.76 ms | N/A | 53.05 ms | 4.06 ms |
| b09.v | 13.74 ms | 13.01 ms | 20.34 ms | N/A | 50.05 ms | 4.15 ms |
| b10.v | 17.73 ms | 16.80 ms | 32.57 ms | N/A | 87.15 ms | 5.47 ms |
| b03.v | 24.23 ms | 24.15 ms | 39.41 ms | N/A | 54.95 ms | 5.30 ms |
| b13.v | 28.41 ms | 28.78 ms | 39.62 ms | N/A | 74.86 ms | 8.28 ms |
| b07.v | 27.11 ms | 27.03 ms | 38.23 ms | N/A | 59.14 ms | 8.31 ms |
| b11.v | 33.38 ms | 31.40 ms | 61.58 ms | N/A | 80.80 ms | 8.25 ms |
| b04.v | 79.76 ms | 77.74 ms | 113.58 ms | N/A | 285.21 ms | 14.92 ms |
| b05.v | 19.47 ms | 25.58 ms | 29.53 ms | N/A | 39.41 ms | 10.42 ms |
| b12.v | 73.22 ms | 73.17 ms | 92.25 ms | N/A | 177.91 ms | 25.41 ms |
| b14.v | 1024.85 ms | 572.46 ms | 1422.79 ms | N/A | 1351.70 ms | 89.51 ms |
| b15.v | 366.44 ms | 422.04 ms | 597.35 ms | N/A | 1099.89 ms | 142.19 ms |
| b21.v | 1246.85 ms | 773.63 ms | 1868.71 ms | N/A | 1741.74 ms | 203.98 ms |
| b20.v | 1613.53 ms | 963.02 ms | 2094.94 ms | N/A | 2023.83 ms | 217.43 ms |
| b22.v | 2958.67 ms | 1749.62 ms | 4024.80 ms | N/A | 4076.38 ms | 473.05 ms |
| b17.v | 1288.21 ms | 1266.09 ms | 2025.26 ms | N/A | 2626.99 ms | 1079.13 ms |
| b18.v | 5104.13 ms | 3535.54 ms | 7298.46 ms | N/A | 19.91 s | 5627.78 ms |
| b19.v | 8005.39 ms | 6361.40 ms | 11.16 s | N/A | 31.56 s | 12.89 s |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| b02.v | 6.69x | 9.31x | 5.69x | N/A | 1.00x | 41.23x |
| b01.v | 6.24x | 7.88x | 3.96x | N/A | 1.00x | 40.73x |
| b06.v | 4.08x | 5.19x | 2.59x | N/A | 1.00x | 14.34x |
| b08.v | 4.38x | 3.98x | 2.55x | N/A | 1.00x | 13.07x |
| b09.v | 3.64x | 3.85x | 2.46x | N/A | 1.00x | 12.06x |
| b10.v | 4.92x | 5.19x | 2.68x | N/A | 1.00x | 15.94x |
| b03.v | 2.27x | 2.28x | 1.39x | N/A | 1.00x | 10.37x |
| b13.v | 2.64x | 2.60x | 1.89x | N/A | 1.00x | 9.04x |
| b07.v | 2.18x | 2.19x | 1.55x | N/A | 1.00x | 7.12x |
| b11.v | 2.42x | 2.57x | 1.31x | N/A | 1.00x | 9.79x |
| b04.v | 3.58x | 3.67x | 2.51x | N/A | 1.00x | 19.11x |
| b05.v | 2.02x | 1.54x | 1.33x | N/A | 1.00x | 3.78x |
| b12.v | 2.43x | 2.43x | 1.93x | N/A | 1.00x | 7.00x |
| b14.v | 1.32x | 2.36x | 0.95x | N/A | 1.00x | 15.10x |
| b15.v | 3.00x | 2.61x | 1.84x | N/A | 1.00x | 7.74x |
| b21.v | 1.40x | 2.25x | 0.93x | N/A | 1.00x | 8.54x |
| b20.v | 1.25x | 2.10x | 0.97x | N/A | 1.00x | 9.31x |
| b22.v | 1.38x | 2.33x | 1.01x | N/A | 1.00x | 8.62x |
| b17.v | 2.04x | 2.07x | 1.30x | N/A | 1.00x | 2.43x |
| b18.v | 3.90x | 5.63x | 2.73x | N/A | 1.00x | 3.54x |
| b19.v | 3.94x | 4.96x | 2.83x | N/A | 1.00x | 2.45x |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `2.79x`
- **rx-sweep (Linear Compiled):** `3.25x`
- **rx-oop (OOP Graph):** `1.88x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `9.50x`

### Cross-Engine Comparisons

- **Reactor Sweep vs Propagate Ratio:** `1.16x` (sweep faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | IPC | Cycles | Instructions | L1 Loads | L1 Hit% | L2 Hit% | LLC Misses | Brn Miss% |
|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| b02.v | rx-prop | 30.04 | 1.46M | 43.71M | 4.50M | 99.97% | 73.22% | 1.84K | 0.29% |
| b02.v | rx-sweep (Linear) | 0.00 | 0 | 19.14M | 3.55M | 99.91% | 0.00% | 829 | 0.28% |
| b02.v | rx-oop (OOP Engine) | 20.33 | 1.39M | 28.20M | 12.16M | 99.54% | 97.08% | 1.68K | 0.34% |
| b02.v | Icarus Verilog | 3.94 | 128.12M | 504.72M | 212.20M | 99.83% | 91.13% | 27.98K | 1.00% |
| b01.v | rx-prop | 33.86 | 1.59M | 53.87M | 11.31M | 99.96% | 74.09% | 3.95K | 0.30% |
| b01.v | rx-sweep (Linear) | 8.09 | 8.05M | 65.13M | 10.79M | 99.99% | 93.67% | 695 | 0.38% |
| b01.v | rx-oop (OOP Engine) | 4.48 | 18.11M | 81.18M | 32.38M | 99.85% | 90.41% | 774 | 1.79% |
| b01.v | Icarus Verilog | 3.67 | 165.44M | 607.46M | 272.53M | 99.41% | 98.21% | 27.36K | 0.84% |
| b06.v | rx-prop | 6.10 | 22.99M | 140.32M | 32.21M | 99.90% | 95.90% | 1.30K | 0.31% |
| b06.v | rx-sweep (Linear) | 7.21 | 13.85M | 99.83M | 20.41M | 99.85% | 95.25% | 76 | 0.36% |
| b06.v | rx-oop (OOP Engine) | 3.62 | 31.76M | 115.10M | 53.78M | 99.71% | 98.83% | 1.79K | 1.11% |
| b06.v | Icarus Verilog | 4.11 | 144.58M | 594.02M | 256.44M | 99.55% | 97.38% | 30.19K | 0.69% |
| b08.v | rx-prop | 5.26 | 34.36M | 180.81M | 56.32M | 99.50% | 99.85% | 410 | 0.67% |
| b08.v | rx-sweep (Linear) | 4.91 | 44.55M | 218.72M | 56.73M | 99.03% | 99.79% | 1.15K | 0.86% |
| b08.v | rx-oop (OOP Engine) | 3.17 | 57.52M | 182.19M | 105.61M | 98.68% | 99.41% | 12.63K | 1.85% |
| b08.v | Icarus Verilog | 3.84 | 241.15M | 925.95M | 396.26M | 98.30% | 99.53% | 33.93K | 0.79% |
| b09.v | rx-prop | 6.19 | 32.04M | 198.27M | 58.91M | 99.71% | 96.85% | 5.42K | 0.29% |
| b09.v | rx-sweep (Linear) | 5.56 | 40.51M | 225.28M | 57.11M | 98.92% | 99.99% | 1.72K | 0.35% |
| b09.v | rx-oop (OOP Engine) | 3.31 | 63.47M | 209.91M | 110.31M | 97.89% | 99.51% | 3.52K | 0.50% |
| b09.v | Icarus Verilog | 4.16 | 231.54M | 963.36M | 409.82M | 96.80% | 99.76% | 31.47K | 0.52% |
| b10.v | rx-prop | 3.96 | 64.46M | 255.13M | 88.15M | 99.06% | 99.18% | 6.13K | 1.44% |
| b10.v | rx-sweep (Linear) | 3.86 | 62.10M | 239.81M | 76.42M | 98.31% | 99.81% | 2.40K | 1.39% |
| b10.v | rx-oop (OOP Engine) | 2.14 | 125.13M | 267.21M | 167.10M | 97.79% | 99.10% | 44.01K | 3.68% |
| b10.v | Icarus Verilog | 3.85 | 374.56M | 1.44B | 636.80M | 96.94% | 99.81% | 35.98K | 0.75% |
| b03.v | rx-prop | 5.01 | 76.34M | 382.48M | 105.88M | 97.23% | 99.73% | 4.29K | 0.73% |
| b03.v | rx-sweep (Linear) | 4.16 | 84.35M | 350.58M | 109.05M | 92.45% | 99.96% | 2.38K | 0.86% |
| b03.v | rx-oop (OOP Engine) | 2.62 | 134.94M | 352.92M | 198.94M | 95.95% | 99.91% | 19.24K | 2.91% |
| b03.v | Icarus Verilog | 3.79 | 262.20M | 994.49M | 430.47M | 96.86% | 99.57% | 58.11K | 0.71% |
| b13.v | rx-prop | 4.28 | 100.87M | 431.25M | 140.01M | 95.94% | 99.83% | 9.50K | 0.30% |
| b13.v | rx-sweep (Linear) | 4.44 | 105.11M | 467.10M | 138.14M | 88.55% | 99.98% | 4.69K | 0.44% |
| b13.v | rx-oop (OOP Engine) | 2.96 | 148.27M | 438.77M | 225.85M | 93.45% | 99.90% | 14.21K | 0.63% |
| b13.v | Icarus Verilog | 3.88 | 354.17M | 1.37B | 585.86M | 96.75% | 99.63% | 79.40K | 0.67% |
| b07.v | rx-prop | 4.45 | 97.39M | 433.49M | 138.15M | 95.94% | 99.80% | 12.45K | 0.20% |
| b07.v | rx-sweep (Linear) | 4.72 | 95.64M | 451.02M | 145.03M | 87.14% | 99.99% | 1.64K | 0.28% |
| b07.v | rx-oop (OOP Engine) | 3.10 | 139.04M | 430.77M | 222.46M | 91.78% | 99.97% | 7.21K | 0.68% |
| b07.v | Icarus Verilog | 3.79 | 321.75M | 1.22B | 538.26M | 96.08% | 99.61% | 91.97K | 0.54% |
| b11.v | rx-prop | 3.57 | 128.57M | 458.40M | 155.74M | 96.24% | 99.85% | 7.82K | 1.46% |
| b11.v | rx-sweep (Linear) | 3.75 | 120.60M | 452.48M | 137.13M | 87.03% | 99.97% | 5.02K | 1.06% |
| b11.v | rx-oop (OOP Engine) | 1.97 | 245.85M | 485.35M | 317.27M | 96.16% | 99.73% | 22.15K | 4.85% |
| b11.v | Icarus Verilog | 3.32 | 411.08M | 1.37B | 621.10M | 97.15% | 99.23% | 115.95K | 0.91% |
| b04.v | rx-prop | 2.85 | 314.13M | 896.69M | 316.51M | 92.59% | 99.97% | 7.97K | 3.12% |
| b04.v | rx-sweep (Linear) | 2.89 | 310.95M | 899.34M | 306.12M | 88.07% | 99.96% | 11.98K | 2.34% |
| b04.v | rx-oop (OOP Engine) | 1.91 | 451.79M | 862.01M | 555.79M | 93.60% | 99.95% | 16.07K | 5.25% |
| b04.v | Icarus Verilog | 3.22 | 1.26B | 4.04B | 1.96B | 96.93% | 98.61% | 825.98K | 1.13% |
| b05.v | rx-prop | 4.82 | 63.70M | 306.71M | 104.46M | 98.14% | 99.63% | 7.25K | 0.24% |
| b05.v | rx-sweep (Linear) | 4.39 | 96.19M | 422.23M | 130.59M | 84.63% | 99.98% | 5.03K | 0.39% |
| b05.v | rx-oop (OOP Engine) | 3.12 | 102.23M | 319.23M | 167.32M | 95.60% | 99.90% | 6.21K | 1.30% |
| b05.v | Icarus Verilog | 3.57 | 256.47M | 914.57M | 390.85M | 96.43% | 99.35% | 92.69K | 0.65% |
| b12.v | rx-prop | 3.74 | 285.14M | 1.07B | 344.45M | 88.13% | 99.98% | 13.21K | 0.35% |
| b12.v | rx-sweep (Linear) | 4.51 | 293.58M | 1.32B | 396.22M | 82.29% | 99.97% | 22.62K | 0.37% |
| b12.v | rx-oop (OOP Engine) | 2.82 | 361.06M | 1.02B | 559.05M | 90.45% | 99.92% | 42.74K | 1.26% |
| b12.v | Icarus Verilog | 3.56 | 924.06M | 3.29B | 1.49B | 95.84% | 97.79% | 1.40M | 0.71% |
| b14.v | rx-prop | 1.98 | 4.12B | 8.15B | 3.16B | 90.41% | 95.06% | 14.95M | 6.27% |
| b14.v | rx-sweep (Linear) | 2.29 | 2.28B | 5.22B | 1.90B | 86.81% | 93.50% | 16.44M | 3.74% |
| b14.v | rx-oop (OOP Engine) | 1.29 | 5.74B | 7.41B | 5.68B | 93.33% | 86.79% | 50.08M | 9.59% |
| b14.v | Icarus Verilog | 2.71 | 6.40B | 17.35B | 8.83B | 95.61% | 77.64% | 86.58M | 1.15% |
| b15.v | rx-prop | 3.52 | 1.48B | 5.22B | 1.73B | 87.81% | 97.26% | 5.72M | 0.69% |
| b15.v | rx-sweep (Linear) | 3.67 | 1.69B | 6.20B | 1.97B | 82.33% | 89.53% | 36.45M | 0.81% |
| b15.v | rx-oop (OOP Engine) | 2.14 | 2.39B | 5.10B | 3.09B | 91.18% | 87.46% | 34.11M | 2.38% |
| b15.v | Icarus Verilog | 3.08 | 5.98B | 18.42B | 8.35B | 95.65% | 68.00% | 116.26M | 0.62% |
| b21.v | rx-prop | 2.09 | 5.01B | 10.48B | 3.97B | 89.84% | 89.09% | 43.93M | 5.24% |
| b21.v | rx-sweep (Linear) | 2.70 | 3.09B | 8.37B | 2.86B | 84.53% | 87.10% | 57.24M | 2.21% |
| b21.v | rx-oop (OOP Engine) | 1.32 | 7.48B | 9.84B | 7.31B | 92.84% | 75.25% | 129.54M | 7.98% |
| b21.v | Icarus Verilog | 2.70 | 8.99B | 24.27B | 12.00B | 95.56% | 70.16% | 158.84M | 1.02% |
| b20.v | rx-prop | 1.91 | 6.50B | 12.43B | 4.83B | 89.85% | 87.81% | 59.93M | 6.03% |
| b20.v | rx-sweep (Linear) | 2.42 | 3.87B | 9.35B | 3.33B | 85.15% | 87.16% | 63.65M | 2.77% |
| b20.v | rx-oop (OOP Engine) | 1.26 | 8.40B | 10.57B | 8.00B | 92.92% | 73.56% | 150.27M | 8.61% |
| b20.v | Icarus Verilog | 2.62 | 10.26B | 26.86B | 13.44B | 95.55% | 70.60% | 175.68M | 1.10% |
| b22.v | rx-prop | 1.67 | 11.89B | 19.83B | 8.02B | 89.90% | 78.87% | 171.14M | 7.18% |
| b22.v | rx-sweep (Linear) | 2.07 | 7.03B | 14.57B | 5.46B | 86.48% | 84.51% | 114.22M | 3.73% |
| b22.v | rx-oop (OOP Engine) | 1.15 | 16.14B | 18.54B | 14.64B | 93.33% | 68.55% | 307.10M | 9.97% |
| b22.v | Icarus Verilog | 2.29 | 19.60B | 44.97B | 24.31B | 95.58% | 56.46% | 467.85M | 1.22% |
| b17.v | rx-prop | 3.01 | 5.15B | 15.49B | 5.21B | 87.75% | 80.50% | 124.63M | 0.95% |
| b17.v | rx-sweep (Linear) | 3.62 | 5.09B | 18.40B | 5.92B | 82.72% | 92.25% | 79.63M | 0.89% |
| b17.v | rx-oop (OOP Engine) | 1.82 | 8.13B | 14.76B | 9.15B | 90.60% | 60.72% | 337.82M | 2.22% |
| b17.v | Icarus Verilog | 2.46 | 15.35B | 37.78B | 17.58B | 94.50% | 56.66% | 419.67M | 0.72% |
| b18.v | rx-prop | 2.12 | 20.49B | 43.52B | 16.17B | 89.16% | 70.59% | 515.43M | 3.58% |
| b18.v | rx-sweep (Linear) | 3.17 | 14.23B | 45.06B | 14.83B | 83.32% | 87.40% | 311.56M | 1.26% |
| b18.v | rx-oop (OOP Engine) | 1.43 | 29.25B | 41.93B | 28.87B | 91.80% | 54.53% | 1.08B | 5.08% |
| b18.v | Icarus Verilog | 1.96 | 20.31B | 39.81B | 18.75B | 94.84% | 77.08% | 221.92M | 1.44% |
| b19.v | rx-prop | 2.34 | 32.03B | 74.92B | 26.35B | 88.31% | 64.38% | 1.10B | 2.18% |
| b19.v | rx-sweep (Linear) | 3.41 | 25.45B | 86.82B | 27.85B | 82.62% | 87.39% | 610.53M | 0.86% |
| b19.v | rx-oop (OOP Engine) | 1.62 | 44.66B | 72.16B | 45.18B | 91.32% | 52.32% | 1.87B | 2.99% |
| b19.v | Icarus Verilog | 1.73 | 37.53B | 64.94B | 28.83B | 94.41% | 76.14% | 383.87M | 1.39% |

---

# master_test/master_test_report_20260918_200731.md

# Master Test Unified Benchmark Report: tests/IWLS2005/opencores

**Execution Parameters:**
- **Target Suite / Path:** `tests/IWLS2005/opencores`
- **Circuits Benchmarked:** 21
- **Simulation Vectors (Phase 3):** 10,000 (Warmup: 10)
- **Verification Vectors (Phase 2):** 100
- **Hardware Profiler:** Linux `perf` kernel PMU counters

---

## 1. Zero-Testbench Memory Footprint (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | 184 | 2.45 MB (33.9 MB peak) | N/A | 0.58 MB (8.4 MB peak) | 0.70 MB (4.4 MB peak) |
| steppermotordrive.v | 258 | 1.02 MB (32.3 MB peak) | N/A | 0.95 MB (8.8 MB peak) | 0.82 MB (4.4 MB peak) |
| ss_pcm.v | 648 | 4.28 MB (35.7 MB peak) | N/A | 2.18 MB (9.9 MB peak) | 0.73 MB (4.4 MB peak) |
| usb_phy.v | 715 | 2.55 MB (33.9 MB peak) | N/A | 2.61 MB (10.5 MB peak) | 0.77 MB (4.4 MB peak) |
| sasc.v | 1,125 | 5.18 MB (36.5 MB peak) | N/A | 2.64 MB (10.5 MB peak) | 0.77 MB (4.5 MB peak) |
| simple_spi.v | 1,489 | 3.73 MB (35.1 MB peak) | N/A | 4.04 MB (11.8 MB peak) | 0.79 MB (4.5 MB peak) |
| pci_spoci_ctrl.v | 1,696 | 2.91 MB (34.3 MB peak) | N/A | 5.09 MB (13.0 MB peak) | 0.75 MB (4.4 MB peak) |
| i2c.v | 1,496 | 3.68 MB (35.1 MB peak) | N/A | 5.29 MB (13.1 MB peak) | 0.75 MB (4.4 MB peak) |
| systemcdes.v | 4,326 | 7.05 MB (38.5 MB peak) | N/A | 13.72 MB (21.5 MB peak) | 0.82 MB (4.5 MB peak) |
| spi.v | 4,531 | 9.09 MB (40.5 MB peak) | N/A | 14.93 MB (22.8 MB peak) | 0.81 MB (4.5 MB peak) |
| wb_dma.v | 5,720 | 18.05 MB (49.4 MB peak) | N/A | 16.05 MB (23.9 MB peak) | 0.95 MB (4.6 MB peak) |
| des_area.v | 6,445 | 8.18 MB (39.6 MB peak) | N/A | 18.87 MB (26.7 MB peak) | 1.04 MB (4.7 MB peak) |
| tv80.v | 10,607 | 17.14 MB (48.5 MB peak) | N/A | 31.18 MB (39.0 MB peak) | N/A |
| systemcaes.v | 14,071 | 23.59 MB (55.8 MB peak) | N/A | 40.91 MB (48.8 MB peak) | 1.14 MB (4.8 MB peak) |
| mem_ctrl.v | 16,796 | 32.54 MB (65.5 MB peak) | N/A | 54.08 MB (61.9 MB peak) | 1.18 MB (4.9 MB peak) |
| ac97_ctrl.v | 19,069 | 52.64 MB (85.3 MB peak) | N/A | 65.54 MB (73.4 MB peak) | 1.43 MB (5.1 MB peak) |
| usb_funct.v | 18,282 | 46.75 MB (79.7 MB peak) | N/A | 59.35 MB (67.2 MB peak) | 1.22 MB (4.9 MB peak) |
| aes_core.v | 25,565 | 30.35 MB (64.7 MB peak) | N/A | 78.83 MB (86.7 MB peak) | 1.29 MB (5.0 MB peak) |
| wb_conmax.v | 49,326 | 47.74 MB (84.0 MB peak) | N/A | 144.19 MB (152.0 MB peak) | 1.30 MB (5.0 MB peak) |
| des_perf.v | 111,781 | 206.16 MB (244.6 MB peak) | N/A | 440.63 MB (448.4 MB peak) | 2.76 MB (6.4 MB peak) |
| vga_lcd.v | 187,445 | 380.36 MB (420.8 MB peak) | N/A | 592.71 MB (600.5 MB peak) | 3.27 MB (7.0 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | 184 | 0.60 ms (0.014 ms opt) | N/A | 5.31 ms | 2.56 s |
| steppermotordrive.v | 258 | 8.37 ms (0.060 ms opt) | N/A | 7.35 ms | 2.60 s |
| ss_pcm.v | 648 | 9.42 ms (0.146 ms opt) | N/A | 11.30 ms | 2.62 s |
| usb_phy.v | 715 | 1.90 ms (0.167 ms opt) | N/A | 13.74 ms | 2.64 s |
| sasc.v | 1,125 | 9.95 ms (0.210 ms opt) | N/A | 13.10 ms | 2.74 s |
| simple_spi.v | 1,489 | 10.45 ms (0.274 ms opt) | N/A | 20.22 ms | 2.84 s |
| pci_spoci_ctrl.v | 1,696 | 9.90 ms (0.239 ms opt) | N/A | 23.94 ms | 2.75 s |
| i2c.v | 1,496 | 10.32 ms (0.272 ms opt) | N/A | 25.23 ms | 2.96 s |
| systemcdes.v | 4,326 | 13.36 ms (0.660 ms opt) | N/A | 64.91 ms | 3.60 s |
| spi.v | 4,531 | 13.74 ms (0.640 ms opt) | N/A | 66.70 ms | 3.87 s |
| wb_dma.v | 5,720 | 18.91 ms (0.996 ms opt) | N/A | 73.50 ms | 5.17 s |
| des_area.v | 6,445 | 14.25 ms (0.755 ms opt) | N/A | 90.51 ms | 4.41 s |
| tv80.v | 10,607 | 20.10 ms (1.434 ms opt) | N/A | 149.91 ms | N/A |
| systemcaes.v | 14,071 | 25.39 ms (2.249 ms opt) | N/A | 199.42 ms | 9.80 s |
| mem_ctrl.v | 16,796 | 35.13 ms (5.467 ms opt) | N/A | 292.83 ms | 15.82 s |
| ac97_ctrl.v | 19,069 | 46.92 ms (7.607 ms opt) | N/A | 319.86 ms | 12.47 s |
| usb_funct.v | 18,282 | 41.45 ms (6.537 ms opt) | N/A | 358.03 ms | 11.50 s |
| aes_core.v | 25,565 | 35.06 ms (4.654 ms opt) | N/A | 441.36 ms | 9.45 s |
| wb_conmax.v | 49,326 | 60.93 ms (13.410 ms opt) | N/A | 859.35 ms | 18.55 s |
| des_perf.v | 111,781 | 337.84 ms (63.315 ms opt) | N/A | 2.42 s | 74.39 s |
| vga_lcd.v | 187,445 | 643.45 ms (138.852 ms opt) | N/A | 3.34 s | 151.83 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | 5.03 ms | 6.35 ms | 7.34 ms | N/A | 180.57 ms | 0.32 ms |
| steppermotordrive.v | 11.96 ms | 13.48 ms | 16.83 ms | N/A | 21.45 ms | 3.67 ms |
| ss_pcm.v | 59.16 ms | 66.25 ms | 77.10 ms | N/A | 123.41 ms | 9.02 ms |
| usb_phy.v | 64.80 ms | 60.91 ms | 82.88 ms | N/A | 85.79 ms | 10.90 ms |
| sasc.v | 77.97 ms | 75.61 ms | 104.14 ms | N/A | 106.62 ms | 12.61 ms |
| simple_spi.v | 70.83 ms | 67.22 ms | 87.74 ms | N/A | 126.52 ms | 18.58 ms |
| pci_spoci_ctrl.v | 52.38 ms | 49.26 ms | 93.24 ms | N/A | 171.45 ms | 12.28 ms |
| i2c.v | 96.18 ms | 79.47 ms | 120.17 ms | N/A | 226.18 ms | 23.53 ms |
| systemcdes.v | 816.13 ms | 530.07 ms | 1295.42 ms | N/A | 3179.68 ms | 46.70 ms |
| spi.v | 143.02 ms | 143.57 ms | 168.18 ms | N/A | 489.56 ms | 43.57 ms |
| wb_dma.v | 349.63 ms | 350.49 ms | 485.56 ms | N/A | 1206.33 ms | 77.39 ms |
| des_area.v | 895.00 ms | 573.58 ms | 1306.32 ms | N/A | 10.19 s | 59.83 ms |
| tv80.v | 209.33 ms | 264.98 ms | 277.29 ms | N/A | 208.71 ms | 82.08 ms |
| systemcaes.v | 658.76 ms | 631.72 ms | 969.68 ms | N/A | 4173.41 ms | 146.11 ms |
| mem_ctrl.v | 612.66 ms | 656.78 ms | 898.09 ms | N/A | 1496.81 ms | 199.35 ms |
| ac97_ctrl.v | 1120.11 ms | 1033.17 ms | 1515.31 ms | N/A | 999.37 ms | 248.41 ms |
| usb_funct.v | 456.33 ms | 601.67 ms | 591.35 ms | N/A | 1665.47 ms | 259.23 ms |
| aes_core.v | 3245.75 ms | 3217.45 ms | 4599.22 ms | N/A | 5823.49 ms | 192.41 ms |
| wb_conmax.v | 1108.65 ms | 1295.52 ms | 1410.60 ms | N/A | 21.22 s | 341.78 ms |
| des_perf.v | 36.13 s | 28.56 s | 60.74 s | N/A | 120.99 s | 6434.68 ms |
| vga_lcd.v | 12.42 s | 10.18 s | 14.82 s | N/A | 12.68 s | 10.39 s |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | 35.87x | 28.42x | 24.61x | N/A | 1.00x | 564.84x |
| steppermotordrive.v | 1.79x | 1.59x | 1.27x | N/A | 1.00x | 5.85x |
| ss_pcm.v | 2.09x | 1.86x | 1.60x | N/A | 1.00x | 13.68x |
| usb_phy.v | 1.32x | 1.41x | 1.04x | N/A | 1.00x | 7.87x |
| sasc.v | 1.37x | 1.41x | 1.02x | N/A | 1.00x | 8.46x |
| simple_spi.v | 1.79x | 1.88x | 1.44x | N/A | 1.00x | 6.81x |
| pci_spoci_ctrl.v | 3.27x | 3.48x | 1.84x | N/A | 1.00x | 13.97x |
| i2c.v | 2.35x | 2.85x | 1.88x | N/A | 1.00x | 9.61x |
| systemcdes.v | 3.90x | 6.00x | 2.45x | N/A | 1.00x | 68.09x |
| spi.v | 3.42x | 3.41x | 2.91x | N/A | 1.00x | 11.24x |
| wb_dma.v | 3.45x | 3.44x | 2.48x | N/A | 1.00x | 15.59x |
| des_area.v | 11.39x | 17.77x | 7.80x | N/A | 1.00x | 170.41x |
| tv80.v | 1.00x | 0.79x | 0.75x | N/A | 1.00x | 2.54x |
| systemcaes.v | 6.34x | 6.61x | 4.30x | N/A | 1.00x | 28.56x |
| mem_ctrl.v | 2.44x | 2.28x | 1.67x | N/A | 1.00x | 7.51x |
| ac97_ctrl.v | 0.89x | 0.97x | 0.66x | N/A | 1.00x | 4.02x |
| usb_funct.v | 3.65x | 2.77x | 2.82x | N/A | 1.00x | 6.42x |
| aes_core.v | 1.79x | 1.81x | 1.27x | N/A | 1.00x | 30.27x |
| wb_conmax.v | 19.14x | 16.38x | 15.04x | N/A | 1.00x | 62.09x |
| des_perf.v | 3.35x | 4.24x | 1.99x | N/A | 1.00x | 18.80x |
| vga_lcd.v | 1.02x | 1.25x | 0.86x | N/A | 1.00x | 1.22x |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `3.00x`
- **rx-sweep (Linear Compiled):** `3.09x`
- **rx-oop (OOP Graph):** `2.17x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `14.73x`

### Cross-Engine Comparisons

- **Reactor Sweep vs Propagate Ratio:** `1.03x` (sweep faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | IPC | Cycles | Instructions | L1 Loads | L1 Hit% | L2 Hit% | LLC Misses | Brn Miss% |
|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | rx-prop | 3.83 | 20.38M | 78.03M | 27.68M | 99.10% | 93.46% | 16.24K | 3.17% |
| pci_conf_cyc_addr_dec.v | rx-sweep (Linear) | 2.89 | 14.05M | 40.62M | 14.48M | 99.84% | 99.38% | 141 | 4.92% |
| pci_conf_cyc_addr_dec.v | rx-oop (OOP Engine) | 4.54 | 9.20M | 41.77M | 11.47M | 99.36% | 97.99% | 4.30K | 6.16% |
| pci_conf_cyc_addr_dec.v | Icarus Verilog | 3.83 | 751.94M | 2.88B | 1.09B | 99.42% | 99.83% | 10.68K | 0.52% |
| steppermotordrive.v | rx-prop | 5.02 | 31.77M | 159.63M | 59.10M | 99.78% | 95.09% | 6.40K | 0.35% |
| steppermotordrive.v | rx-sweep (Linear) | 5.13 | 44.93M | 230.63M | 60.36M | 99.34% | 99.68% | 2.13K | 0.56% |
| steppermotordrive.v | rx-oop (OOP Engine) | 3.49 | 47.03M | 164.11M | 70.73M | 99.38% | 99.58% | 1.85K | 0.72% |
| steppermotordrive.v | Icarus Verilog | 3.78 | 99.52M | 376.60M | 150.72M | 99.61% | 97.18% | 16.60K | 0.78% |
| ss_pcm.v | rx-prop | 3.41 | 241.83M | 823.97M | 269.65M | 90.24% | 99.91% | 21.14K | 1.02% |
| ss_pcm.v | rx-sweep (Linear) | 3.21 | 257.64M | 826.49M | 264.70M | 86.54% | 99.95% | 15.20K | 1.30% |
| ss_pcm.v | rx-oop (OOP Engine) | 2.52 | 306.61M | 771.49M | 420.04M | 91.31% | 99.97% | 20.42K | 1.84% |
| ss_pcm.v | Icarus Verilog | 3.44 | 549.99M | 1.89B | 858.56M | 97.98% | 99.54% | 78.32K | 0.98% |
| usb_phy.v | rx-prop | 3.33 | 253.25M | 844.52M | 285.95M | 89.82% | 99.90% | 34.23K | 1.04% |
| usb_phy.v | rx-sweep (Linear) | 3.76 | 237.35M | 891.62M | 281.61M | 86.69% | 99.98% | 9.20K | 0.95% |
| usb_phy.v | rx-oop (OOP Engine) | 2.41 | 323.32M | 779.12M | 449.93M | 91.10% | 99.93% | 26.91K | 1.93% |
| usb_phy.v | Icarus Verilog | 3.34 | 420.86M | 1.41B | 621.76M | 97.96% | 99.31% | 86.93K | 0.95% |
| sasc.v | rx-prop | 3.49 | 296.95M | 1.04B | 331.39M | 88.41% | 99.98% | 8.63K | 1.02% |
| sasc.v | rx-sweep (Linear) | 3.71 | 295.12M | 1.10B | 347.66M | 85.46% | 99.99% | 8.51K | 1.09% |
| sasc.v | rx-oop (OOP Engine) | 2.66 | 407.43M | 1.09B | 590.92M | 90.96% | 99.97% | 23.87K | 1.91% |
| sasc.v | Icarus Verilog | 3.50 | 507.46M | 1.78B | 767.26M | 97.78% | 99.48% | 88.81K | 0.84% |
| simple_spi.v | rx-prop | 3.71 | 276.71M | 1.03B | 324.47M | 86.77% | 99.95% | 23.68K | 0.39% |
| simple_spi.v | rx-sweep (Linear) | 4.36 | 261.60M | 1.14B | 344.61M | 83.32% | 99.97% | 16.29K | 0.52% |
| simple_spi.v | rx-oop (OOP Engine) | 2.87 | 353.31M | 1.01B | 546.78M | 89.33% | 99.95% | 23.81K | 0.78% |
| simple_spi.v | Icarus Verilog | 3.55 | 614.53M | 2.18B | 964.86M | 97.22% | 99.26% | 205.65K | 0.75% |
| pci_spoci_ctrl.v | rx-prop | 3.91 | 204.44M | 798.62M | 259.75M | 94.21% | 99.95% | 7.02K | 0.75% |
| pci_spoci_ctrl.v | rx-sweep (Linear) | 4.10 | 195.35M | 800.53M | 244.96M | 85.27% | 99.92% | 26.76K | 0.67% |
| pci_spoci_ctrl.v | rx-oop (OOP Engine) | 2.05 | 387.37M | 795.35M | 509.60M | 93.46% | 99.87% | 44.09K | 3.74% |
| pci_spoci_ctrl.v | Icarus Verilog | 3.34 | 829.51M | 2.77B | 1.25B | 97.10% | 99.31% | 269.90K | 0.99% |
| i2c.v | rx-prop | 3.26 | 386.16M | 1.26B | 412.86M | 89.53% | 99.89% | 42.02K | 0.61% |
| i2c.v | rx-sweep (Linear) | 4.11 | 320.10M | 1.31B | 403.22M | 84.86% | 99.98% | 11.19K | 0.60% |
| i2c.v | rx-oop (OOP Engine) | 2.52 | 481.67M | 1.21B | 691.07M | 89.50% | 99.88% | 75.10K | 1.90% |
| i2c.v | Icarus Verilog | 3.75 | 1.05B | 3.93B | 1.74B | 95.84% | 97.43% | 1.86M | 0.60% |
| systemcdes.v | rx-prop | 2.04 | 3.33B | 6.80B | 2.71B | 91.61% | 99.67% | 698.01K | 6.48% |
| systemcdes.v | rx-sweep (Linear) | 1.99 | 2.17B | 4.32B | 1.71B | 89.97% | 99.65% | 619.61K | 5.47% |
| systemcdes.v | rx-oop (OOP Engine) | 1.34 | 5.22B | 7.01B | 5.29B | 93.49% | 98.30% | 5.85M | 9.50% |
| systemcdes.v | Icarus Verilog | 2.68 | 13.24B | 35.50B | 18.88B | 96.46% | 79.39% | 138.21M | 1.33% |
| spi.v | rx-prop | 3.60 | 585.39M | 2.10B | 681.92M | 87.58% | 99.82% | 154.53K | 0.42% |
| spi.v | rx-sweep (Linear) | 4.12 | 581.94M | 2.40B | 763.79M | 82.99% | 99.88% | 151.81K | 0.67% |
| spi.v | rx-oop (OOP Engine) | 2.90 | 688.05M | 1.99B | 1.07B | 89.15% | 99.59% | 479.40K | 0.90% |
| spi.v | Icarus Verilog | 3.58 | 2.34B | 8.37B | 3.75B | 96.01% | 81.57% | 27.78M | 0.55% |
| wb_dma.v | rx-prop | 3.68 | 1.46B | 5.36B | 1.82B | 86.58% | 99.03% | 2.37M | 0.61% |
| wb_dma.v | rx-sweep (Linear) | 3.85 | 1.46B | 5.62B | 1.83B | 85.71% | 97.45% | 6.67M | 0.96% |
| wb_dma.v | rx-oop (OOP Engine) | 2.59 | 1.99B | 5.17B | 2.86B | 89.08% | 93.35% | 20.80M | 1.05% |
| wb_dma.v | Icarus Verilog | 3.80 | 5.40B | 20.56B | 8.91B | 98.40% | 79.89% | 28.75M | 0.46% |
| des_area.v | rx-prop | 1.95 | 3.67B | 7.14B | 2.90B | 92.21% | 98.30% | 3.84M | 6.71% |
| des_area.v | rx-sweep (Linear) | 1.87 | 2.37B | 4.44B | 1.82B | 91.00% | 97.03% | 4.89M | 5.78% |
| des_area.v | rx-oop (OOP Engine) | 1.31 | 5.28B | 6.93B | 5.22B | 93.44% | 97.45% | 8.68M | 9.30% |
| des_area.v | Icarus Verilog | 3.16 | 41.58B | 131.57B | 51.36B | 97.50% | 81.31% | 239.52M | 0.59% |
| tv80.v | rx-prop | 3.54 | 838.53M | 2.96B | 987.60M | 86.64% | 99.39% | 803.31K | 0.67% |
| tv80.v | rx-sweep (Linear) | 3.83 | 1.07B | 4.09B | 1.27B | 82.28% | 95.61% | 9.95M | 0.82% |
| tv80.v | rx-oop (OOP Engine) | 2.58 | 1.10B | 2.86B | 1.60B | 89.44% | 97.49% | 4.23M | 1.38% |
| tv80.v | Icarus Verilog | 2.80 | 1.64B | 4.59B | 2.01B | 96.10% | 90.94% | 6.99M | 1.08% |
| systemcaes.v | rx-prop | 3.05 | 2.69B | 8.21B | 2.81B | 88.99% | 90.12% | 30.59M | 1.26% |
| systemcaes.v | rx-sweep (Linear) | 3.41 | 2.54B | 8.64B | 2.81B | 85.37% | 88.39% | 48.49M | 1.29% |
| systemcaes.v | rx-oop (OOP Engine) | 1.99 | 3.94B | 7.83B | 4.77B | 91.11% | 76.43% | 100.23M | 2.39% |
| systemcaes.v | Icarus Verilog | 3.97 | 17.94B | 71.16B | 31.70B | 96.77% | 74.37% | 262.57M | 0.35% |
| mem_ctrl.v | rx-prop | 3.33 | 2.48B | 8.25B | 2.77B | 87.08% | 87.95% | 43.09M | 0.60% |
| mem_ctrl.v | rx-sweep (Linear) | 3.65 | 2.63B | 9.62B | 3.05B | 84.37% | 88.78% | 53.29M | 0.91% |
| mem_ctrl.v | rx-oop (OOP Engine) | 2.21 | 3.60B | 7.95B | 4.53B | 89.48% | 72.81% | 129.66M | 1.12% |
| mem_ctrl.v | Icarus Verilog | 3.37 | 7.50B | 25.30B | 11.17B | 97.17% | 60.26% | 126.13M | 0.48% |
| ac97_ctrl.v | rx-prop | 3.23 | 4.49B | 14.50B | 4.76B | 86.29% | 80.67% | 126.23M | 0.15% |
| ac97_ctrl.v | rx-sweep (Linear) | 4.04 | 4.14B | 16.73B | 5.19B | 84.21% | 87.76% | 100.25M | 0.49% |
| ac97_ctrl.v | rx-oop (OOP Engine) | 2.28 | 6.08B | 13.88B | 7.39B | 88.45% | 55.18% | 382.77M | 0.26% |
| ac97_ctrl.v | Icarus Verilog | 3.21 | 5.68B | 18.23B | 7.42B | 96.28% | 60.46% | 109.30M | 0.42% |
| usb_funct.v | rx-prop | 2.82 | 1.86B | 5.26B | 1.76B | 87.52% | 74.76% | 55.45M | 0.50% |
| usb_funct.v | rx-sweep (Linear) | 3.43 | 2.42B | 8.31B | 2.69B | 81.40% | 86.67% | 66.56M | 0.89% |
| usb_funct.v | rx-oop (OOP Engine) | 2.12 | 2.36B | 5.01B | 2.78B | 89.11% | 62.25% | 113.95M | 0.92% |
| usb_funct.v | Icarus Verilog | 3.49 | 8.26B | 28.84B | 12.49B | 96.60% | 73.31% | 113.61M | 0.46% |
| aes_core.v | rx-prop | 1.54 | 13.10B | 20.13B | 8.88B | 90.37% | 80.46% | 167.33M | 7.83% |
| aes_core.v | rx-sweep (Linear) | 1.54 | 12.99B | 20.06B | 8.84B | 90.05% | 81.27% | 164.84M | 6.82% |
| aes_core.v | rx-oop (OOP Engine) | 1.06 | 18.49B | 19.56B | 16.54B | 93.65% | 70.16% | 313.22M | 10.37% |
| aes_core.v | Icarus Verilog | 2.59 | 25.59B | 66.19B | 34.71B | 97.28% | 50.71% | 464.24M | 1.16% |
| wb_conmax.v | rx-prop | 2.62 | 4.78B | 12.51B | 4.48B | 88.74% | 66.90% | 167.20M | 0.84% |
| wb_conmax.v | rx-sweep (Linear) | 2.95 | 5.51B | 16.24B | 5.80B | 84.32% | 83.69% | 148.33M | 1.35% |
| wb_conmax.v | rx-oop (OOP Engine) | 1.92 | 6.05B | 11.64B | 6.88B | 90.59% | 57.32% | 277.09M | 1.45% |
| wb_conmax.v | Icarus Verilog | 3.69 | 89.96B | 331.83B | 147.39B | 93.81% | 84.40% | 1.42B | 0.24% |
| des_perf.v | rx-prop | 1.28 | 144.84B | 184.88B | 77.06B | 89.34% | 34.91% | 5.35B | 6.38% |
| des_perf.v | rx-sweep (Linear) | 1.49 | 114.93B | 170.96B | 75.55B | 90.76% | 63.60% | 2.54B | 6.35% |
| des_perf.v | rx-oop (OOP Engine) | 0.74 | 243.89B | 180.81B | 153.23B | 93.36% | 24.18% | 7.70B | 8.52% |
| des_perf.v | Icarus Verilog | 1.12 | 59.79B | 66.96B | 38.01B | 95.98% | 36.11% | 975.95M | 1.46% |
| vga_lcd.v | rx-prop | 2.45 | 50.04B | 122.73B | 41.00B | 85.95% | 56.65% | 2.50B | 0.12% |
| vga_lcd.v | rx-sweep (Linear) | 3.48 | 40.68B | 141.76B | 43.71B | 83.24% | 78.63% | 1.57B | 0.62% |
| vga_lcd.v | rx-oop (OOP Engine) | 1.99 | 59.33B | 118.20B | 63.73B | 88.99% | 57.66% | 2.97B | 0.14% |
| vga_lcd.v | Icarus Verilog | 2.07 | 21.07B | 43.51B | 17.63B | 94.76% | 78.26% | 201.51M | 1.05% |

---

# master_test/master_test_report_20260918_200840.md

# Master Test Unified Benchmark Report: tests/IWLS2005/faraday

**Execution Parameters:**
- **Target Suite / Path:** `tests/IWLS2005/faraday`
- **Circuits Benchmarked:** 1
- **Simulation Vectors (Phase 3):** 10,000 (Warmup: 10)
- **Verification Vectors (Phase 2):** 100
- **Hardware Profiler:** Linux `perf` kernel PMU counters

---

## 1. Zero-Testbench Memory Footprint (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| DMA.v | 31,920 | 57.82 MB (89.1 MB peak) | N/A | 103.22 MB (111.0 MB peak) | 1.50 MB (5.2 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| DMA.v | 31,920 | 56.20 ms (13.844 ms opt) | N/A | 518.00 ms | 21.50 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| DMA.v | 1532.54 ms | 1401.96 ms | 2057.07 ms | N/A | 5758.52 ms | 698.87 ms |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| DMA.v | 3.76x | 4.11x | 2.80x | N/A | 1.00x | 8.24x |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `3.76x`
- **rx-sweep (Linear Compiled):** `4.11x`
- **rx-oop (OOP Graph):** `2.80x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `8.24x`

### Cross-Engine Comparisons

- **Reactor Sweep vs Propagate Ratio:** `1.09x` (sweep faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | IPC | Cycles | Instructions | L1 Loads | L1 Hit% | L2 Hit% | LLC Misses | Brn Miss% |
|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| DMA.v | rx-prop | 2.92 | 6.34B | 18.53B | 6.34B | 88.06% | 72.45% | 208.53M | 0.54% |
| DMA.v | rx-sweep (Linear) | 3.70 | 5.84B | 21.63B | 7.04B | 84.68% | 86.57% | 144.80M | 0.67% |
| DMA.v | rx-oop (OOP Engine) | 2.06 | 8.50B | 17.53B | 10.13B | 89.85% | 54.58% | 466.83M | 0.97% |
| DMA.v | Icarus Verilog | 3.38 | 26.26B | 88.73B | 40.33B | 97.16% | 49.00% | 582.43M | 0.37% |

---

# master_test/master_test_report_20260918_231307.md

# Master Test Unified Benchmark Report: tests/EPFL_mammoth_parsed

**Execution Parameters:**
- **Target Suite / Path:** `tests/EPFL_mammoth_parsed`
- **Circuits Benchmarked:** 1
- **Simulation Vectors (Phase 3):** 500 (Warmup: 10)
- **Verification Vectors (Phase 2):** 100
- **Hardware Profiler:** Linux `perf` kernel PMU counters

---

## 1. Zero-Testbench Memory Footprint (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| hyp.v | 420,896 | 399.13 MB (430.5 MB peak) | N/A | N/A | 3.53 MB (7.2 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| hyp.v | 420,896 | 648.57 ms (91.086 ms opt) | N/A | N/A | 124.40 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| hyp.v | N/A | 1026.11 ms | N/A | N/A | N/A | 251.29 ms |

### Speedup Analysis (vs Baseline: rx-prop = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| hyp.v | N/A | N/A | N/A | N/A | N/A | N/A |

### Geo-Mean Speedup Highlights (Baseline: rx-prop = 1.00x)

- **rx-prop (Wavefront BFS):** `1.00x (Baseline)`

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | IPC | Cycles | Instructions | L1 Loads | L1 Hit% | L2 Hit% | LLC Misses | Brn Miss% |
|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| hyp.v | rx-sweep (Linear) | 1.49 | 4.12B | 6.12B | 2.55B | 91.84% | 79.03% | 43.61M | 4.18% |
| hyp.v | Verilator C++ | 0.31 | 979.18M | 302.55M | 188.43M | 95.63% | 0.00% | 23.06M | 2.95% |

---

# perf/cache_perf_chaotic_20260918_190208.md

# Cache Fragmentation Profile (CHAOTIC)

Isolated purely via hardware `perf` boundaries tightly hugging the core `batch_toggle` simulation logic.

## 1. Core Performance (IPC & Branches)
| Size | OOP IPC | OOP Branch | Unopt IPC | Unopt Branch | Opt IPC | Opt Branch | Sweep IPC | Sweep Branch |
|---|---|---|---|---|---|---|---|---|
| 100 | 3.75 | 879.79M | 5.27 | 1.16B | 6.09 | 1.16B | 4.81 | 1.22B |
| 135 | 3.67 | 818.50M | 5.48 | 1.09B | 6.03 | 1.09B | 4.75 | 1.15B |
| 182 | 3.60 | 850.52M | 5.55 | 1.14B | 6.13 | 1.14B | 4.72 | 1.21B |
| 245 | 3.49 | 836.71M | 5.72 | 1.12B | 6.20 | 1.12B | 4.82 | 1.20B |
| 330 | 3.19 | 863.69M | 5.87 | 1.16B | 6.20 | 1.16B | 4.79 | 1.25B |
| 445 | 3.06 | 905.45M | 4.81 | 1.22B | 5.71 | 1.22B | 4.74 | 1.31B |
| 600 | 3.02 | 892.59M | 4.37 | 1.21B | 5.49 | 1.21B | 4.62 | 1.30B |
| 810 | 2.99 | 839.91M | 4.16 | 1.14B | 5.64 | 1.14B | 4.64 | 1.23B |
| 1,093 | 2.57 | 859.98M | 4.11 | 1.17B | 5.64 | 1.17B | 4.65 | 1.26B |
| 1,475 | 2.09 | 819.27M | 4.06 | 1.11B | 5.74 | 1.11B | 4.69 | 1.20B |
| 1,991 | 1.93 | 842.04M | 4.08 | 1.14B | 5.94 | 1.14B | 4.74 | 1.24B |
| 2,687 | 1.85 | 812.03M | 4.15 | 1.10B | 6.10 | 1.10B | 4.78 | 1.19B |
| 3,627 | 1.79 | 802.82M | 4.13 | 1.09B | 6.15 | 1.09B | 4.80 | 1.18B |
| 4,896 | 1.76 | 806.77M | 4.10 | 1.10B | 5.84 | 1.10B | 4.80 | 1.19B |
| 6,609 | 1.71 | 772.85M | 4.01 | 1.05B | 5.76 | 1.05B | 4.80 | 1.14B |
| 8,922 | 1.66 | 772.18M | 3.68 | 1.05B | 5.52 | 1.05B | 4.80 | 1.14B |
| 12,044 | 1.59 | 742.07M | 3.15 | 1.01B | 4.72 | 1.01B | 4.77 | 1.09B |
| 16,259 | 1.42 | 679.40M | 2.70 | 925.12M | 4.26 | 924.35M | 4.69 | 999.61M |
| 21,949 | 1.26 | 636.57M | 2.07 | 866.21M | 3.69 | 865.79M | 4.12 | 936.27M |
| 29,631 | 1.16 | 632.28M | 1.63 | 860.39M | 3.51 | 860.60M | 3.53 | 930.81M |
| 40,001 | 1.18 | 626.63M | 1.48 | 852.95M | 3.16 | 852.87M | 3.05 | 922.00M |
| 54,001 | 1.12 | 544.53M | 1.44 | 741.03M | 3.04 | 741.04M | 2.81 | 801.27M |
| 72,901 | 1.14 | 387.18M | 1.34 | 527.00M | 3.09 | 526.88M | 2.75 | 570.04M |
| 98,416 | 1.13 | 310.06M | 1.31 | 422.08M | 3.04 | 421.92M | 2.71 | 456.36M |
| 132,861 | 1.13 | 143.55M | 1.30 | 195.32M | 2.99 | 195.29M | 2.63 | 211.16M |
| 179,362 | 1.08 | 154.94M | 1.30 | 210.95M | 2.85 | 210.79M | 2.62 | 228.22M |
| 242,138 | 0.98 | 143.87M | 1.24 | 195.75M | 2.83 | 195.81M | 2.61 | 211.62M |
| 326,886 | 0.85 | 176.65M | 1.29 | 240.26M | 2.83 | 240.16M | 2.64 | 259.95M |
| 441,296 | 0.51 | 238.37M | 1.25 | 324.41M | 2.91 | 324.21M | 2.66 | 350.71M |
| 595,749 | 0.32 | 321.74M | 1.13 | 438.01M | 2.78 | 438.07M | 2.64 | 473.06M |
| 804,261 | 0.25 | 434.33M | 0.55 | 591.05M | 2.78 | 591.02M | 2.64 | 639.35M |

## 2. L1 Cache Performance
| Size | OOP L1 Load | OOP L1 Hit% | Unopt L1 Load | Unopt L1 Hit% | Opt L1 Load | Opt L1 Hit% | Sweep L1 Load | Sweep L1 Hit% |
|---|---|---|---|---|---|---|---|---|
| 100 | 4.28B | 100.00% | 2.93B | 100.00% | 2.89B | 100.00% | 1.81B | 99.97% |
| 135 | 4.04B | 99.83% | 2.69B | 100.00% | 2.68B | 100.00% | 1.70B | 99.98% |
| 182 | 4.22B | 99.50% | 2.82B | 100.00% | 2.80B | 99.98% | 1.78B | 99.98% |
| 245 | 4.20B | 98.92% | 2.77B | 99.93% | 2.76B | 99.97% | 1.75B | 99.80% |
| 330 | 4.35B | 96.62% | 2.86B | 99.85% | 2.86B | 99.99% | 1.81B | 99.84% |
| 445 | 4.58B | 95.36% | 3.02B | 96.83% | 3.02B | 96.73% | 1.90B | 96.68% |
| 600 | 4.53B | 94.79% | 2.98B | 94.70% | 2.97B | 94.52% | 1.88B | 90.92% |
| 810 | 4.28B | 94.86% | 2.80B | 93.62% | 2.80B | 94.38% | 1.78B | 91.05% |
| 1,093 | 5.11B | 95.72% | 2.87B | 93.40% | 2.86B | 94.45% | 1.82B | 91.32% |
| 1,475 | 5.99B | 96.98% | 2.73B | 93.08% | 2.73B | 94.63% | 1.73B | 91.64% |
| 1,991 | 6.73B | 97.27% | 2.82B | 92.88% | 2.81B | 95.37% | 1.78B | 92.65% |
| 2,687 | 6.77B | 97.38% | 2.71B | 92.86% | 2.71B | 95.98% | 1.71B | 93.71% |
| 3,627 | 6.80B | 97.40% | 2.69B | 92.99% | 2.68B | 96.18% | 1.69B | 93.98% |
| 4,896 | 6.94B | 97.42% | 2.73B | 93.23% | 2.71B | 96.22% | 1.70B | 94.01% |
| 6,609 | 6.75B | 97.29% | 2.66B | 93.49% | 2.64B | 96.31% | 1.63B | 94.05% |
| 8,922 | 6.85B | 97.34% | 2.77B | 93.86% | 2.66B | 96.35% | 1.63B | 94.05% |
| 12,044 | 6.68B | 97.36% | 2.84B | 94.26% | 2.71B | 96.56% | 1.57B | 94.08% |
| 16,259 | 6.27B | 97.67% | 2.72B | 94.54% | 2.55B | 96.66% | 1.45B | 94.14% |
| 21,949 | 6.04B | 97.72% | 2.76B | 94.99% | 2.54B | 96.85% | 1.42B | 94.37% |
| 29,631 | 6.13B | 97.67% | 2.94B | 95.32% | 2.59B | 96.94% | 1.52B | 94.78% |
| 40,001 | 6.07B | 97.62% | 3.02B | 95.46% | 2.65B | 97.03% | 1.58B | 95.03% |
| 54,001 | 5.32B | 97.68% | 2.70B | 95.60% | 2.34B | 97.08% | 1.41B | 95.16% |
| 72,901 | 3.76B | 97.53% | 1.96B | 95.69% | 1.68B | 97.10% | 1.02B | 95.23% |
| 98,416 | 3.03B | 97.53% | 1.59B | 95.73% | 1.35B | 97.13% | 821.31M | 95.27% |
| 132,861 | 1.40B | 97.65% | 739.86M | 95.79% | 631.00M | 97.15% | 380.48M | 95.28% |
| 179,362 | 1.52B | 97.68% | 807.89M | 95.83% | 680.82M | 97.15% | 411.33M | 95.28% |
| 242,138 | 1.41B | 97.63% | 752.16M | 95.83% | 634.53M | 97.15% | 382.35M | 95.28% |
| 326,886 | 1.75B | 97.57% | 926.05M | 95.86% | 782.47M | 97.17% | 469.38M | 95.29% |
| 441,296 | 2.44B | 97.80% | 1.25B | 95.88% | 1.06B | 97.17% | 634.76M | 95.29% |
| 595,749 | 3.44B | 97.83% | 1.69B | 95.90% | 1.43B | 97.17% | 857.28M | 95.28% |
| 804,261 | 4.66B | 97.84% | 2.29B | 95.90% | 1.93B | 97.19% | 1.15B | 95.26% |

## 3. L2, L3 & RAM Performance
| Size | OOP L2 Load | OOP L2 Hit% | OOP L3 Load | OOP L3 Hit% | OOP RAM (L3 Miss) | Unopt L2 Load | Unopt L2 Hit% | Unopt L3 Load | Unopt L3 Hit% | Unopt RAM (L3 Miss) | Opt L2 Load | Opt L2 Hit% | Opt L3 Load | Opt L3 Hit% | Opt RAM (L3 Miss) | Sweep L2 Load | Sweep L2 Hit% | Sweep L3 Load | Sweep L3 Hit% | Sweep RAM (L3 Miss) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 | 63.60K | 74.29% | 16.35K | -25.78% | 20.57K | 34.89K | 70.25% | 10.38K | -0.57% | 10.44K | 27.43K | 64.66% | 9.70K | -100.28% | 19.42K | 590.49K | 88.97% | 65.16K | -1.42% | 66.08K |
| 135 | 6.90M | 99.84% | 10.74K | -5.44% | 11.32K | 44.01K | 80.36% | 8.64K | 2.49% | 8.43K | 42.64K | 82.90% | 7.29K | -4.06% | 7.59K | 369.14K | 86.56% | 49.59K | 12.53% | 43.38K |
| 182 | 21.33M | 99.88% | 24.67K | -0.34% | 24.75K | 94.57K | 92.11% | 7.47K | 36.85% | 4.71K | 556.21K | 98.36% | 9.14K | -0.30% | 9.16K | 400.04K | 87.06% | 51.77K | -0.31% | 51.93K |
| 245 | 45.15M | 99.95% | 20.92K | 20.15% | 16.71K | 1.86M | 98.93% | 19.79K | 0.62% | 19.67K | 831.90K | 98.92% | 8.98K | -55.10% | 13.93K | 3.47M | 99.05% | 33.14K | 11.12% | 29.45K |
| 330 | 147.14M | 99.99% | 14.78K | -31.75% | 19.47K | 4.19M | 99.61% | 16.22K | 43.89% | 9.10K | 236.00K | 92.35% | 18.04K | -0.23% | 18.09K | 2.98M | 98.66% | 40.01K | 15.58% | 33.77K |
| 445 | 212.63M | 99.99% | 22.38K | 8.11% | 20.56K | 95.88M | 99.98% | 20.54K | 33.84% | 13.59K | 98.54M | 100.00% | 3.21K | -100.09% | 6.42K | 63.09M | 99.94% | 34.85K | -20.59% | 42.03K |
| 600 | 236.22M | 100.00% | 11.37K | 0.04% | 11.37K | 157.99M | 100.00% | 3.20K | -142.54% | 7.75K | 162.90M | 99.99% | 10.70K | -3.74% | 11.10K | 170.97M | 99.99% | 24.37K | 9.58% | 22.04K |
| 810 | 219.95M | 99.99% | 29.38K | -1.38% | 29.78K | 178.70M | 99.99% | 17.37K | -0.71% | 17.49K | 157.27M | 99.99% | 11.13K | 8.78% | 10.16K | 159.22M | 99.99% | 23.25K | -25.40% | 29.15K |
| 1,093 | 218.95M | 99.98% | 33.80K | 1.65% | 33.24K | 189.36M | 99.99% | 27.07K | 44.73% | 14.96K | 158.83M | 99.99% | 15.30K | -5.96% | 16.21K | 157.77M | 99.99% | 12.33K | -110.77% | 25.98K |
| 1,475 | 181.28M | 99.99% | 24.76K | -0.11% | 24.79K | 189.32M | 99.99% | 10.47K | -37.22% | 14.37K | 146.80M | 99.99% | 12.39K | -61.52% | 20.02K | 144.75M | 99.98% | 23.78K | -18.84% | 28.26K |
| 1,991 | 183.76M | 99.98% | 34.20K | 10.02% | 30.78K | 200.51M | 100.00% | 9.78K | 41.92% | 5.68K | 130.02M | 99.99% | 10.31K | -30.66% | 13.47K | 130.49M | 99.98% | 27.15K | 0.94% | 26.89K |
| 2,687 | 177.01M | 99.98% | 29.71K | 1.28% | 29.33K | 193.51M | 99.98% | 41.71K | 1.20% | 41.20K | 109.04M | 99.99% | 10.96K | -12.83% | 12.37K | 107.88M | 99.98% | 22.73K | 16.20% | 19.05K |
| 3,627 | 177.11M | 99.98% | 43.23K | 12.99% | 37.62K | 188.75M | 99.98% | 45.30K | 12.68% | 39.55K | 102.52M | 99.99% | 15.33K | 10.51% | 13.72K | 101.92M | 99.97% | 31.54K | 20.06% | 25.22K |
| 4,896 | 179.07M | 99.97% | 57.18K | 0.16% | 57.09K | 184.62M | 99.99% | 24.43K | -7.38% | 26.23K | 102.45M | 99.99% | 13.52K | 4.43% | 12.93K | 101.98M | 99.97% | 29.43K | -2.43% | 30.15K |
| 6,609 | 182.87M | 98.88% | 2.05M | 1.20% | 2.03M | 173.24M | 99.66% | 592.32K | -6.36% | 630.01K | 97.47M | 99.97% | 32.49K | 15.20% | 27.55K | 97.14M | 99.95% | 50.32K | 12.89% | 43.83K |
| 8,922 | 182.10M | 96.59% | 6.21M | 0.19% | 6.20M | 170.11M | 99.12% | 1.49M | -0.36% | 1.49M | 97.23M | 97.76% | 2.18M | -0.14% | 2.18M | 97.03M | 99.96% | 35.50K | 17.18% | 29.40K |
| 12,044 | 176.16M | 91.16% | 15.58M | 0.39% | 15.52M | 162.78M | 97.47% | 4.12M | -0.19% | 4.13M | 93.28M | 99.19% | 752.91K | -1.66% | 765.40K | 93.06M | 99.16% | 778.60K | -0.15% | 779.79K |
| 16,259 | 146.28M | 76.87% | 33.83M | 0.05% | 33.81M | 148.14M | 93.10% | 10.23M | -0.08% | 10.23M | 85.31M | 97.42% | 2.20M | 0.36% | 2.19M | 85.14M | 97.71% | 1.95M | 0.26% | 1.94M |
| 21,949 | 137.64M | 59.30% | 56.02M | 0.04% | 56.00M | 138.11M | 80.84% | 26.47M | 0.08% | 26.45M | 79.84M | 97.64% | 1.89M | 0.59% | 1.87M | 79.89M | 97.76% | 1.79M | 0.67% | 1.78M |
| 29,631 | 142.70M | 41.05% | 84.13M | -0.01% | 84.14M | 137.69M | 66.01% | 46.80M | 0.03% | 46.79M | 79.27M | 97.84% | 1.71M | 0.37% | 1.71M | 79.23M | 97.83% | 1.72M | -0.37% | 1.73M |
| 40,001 | 144.64M | 40.17% | 86.53M | -0.01% | 86.54M | 136.76M | 54.31% | 62.48M | -0.01% | 62.49M | 78.58M | 98.55% | 1.14M | -0.49% | 1.15M | 78.51M | 98.39% | 1.27M | 0.63% | 1.26M |
| 54,001 | 123.44M | 39.00% | 75.30M | -0.00% | 75.30M | 118.56M | 45.84% | 64.21M | 0.01% | 64.21M | 68.20M | 98.95% | 718.95K | -0.78% | 724.58K | 68.14M | 98.79% | 825.83K | 0.78% | 819.36K |
| 72,901 | 92.80M | 33.55% | 61.67M | -0.01% | 61.68M | 84.55M | 40.87% | 50.00M | -0.01% | 50.00M | 48.55M | 99.14% | 418.32K | -1.76% | 425.67K | 48.42M | 99.52% | 231.07K | 2.55% | 225.18K |
| 98,416 | 74.64M | 31.45% | 51.17M | -0.02% | 51.18M | 67.78M | 37.28% | 42.51M | 0.02% | 42.50M | 38.84M | 99.52% | 186.48K | 1.88% | 182.97K | 38.82M | 99.42% | 225.94K | 5.95% | 212.49K |
| 132,861 | 32.90M | 30.75% | 22.78M | 0.04% | 22.77M | 31.12M | 32.08% | 21.14M | -0.05% | 21.15M | 17.98M | 99.51% | 87.86K | -7.69% | 94.61K | 17.97M | 99.46% | 96.81K | -7.71% | 104.27K |
| 179,362 | 35.39M | 30.08% | 24.74M | 0.05% | 24.73M | 33.69M | 30.71% | 23.34M | -0.01% | 23.35M | 19.41M | 99.51% | 95.00K | 3.92% | 91.28K | 19.41M | 99.54% | 89.59K | -0.56% | 90.09K |
| 242,138 | 33.56M | 28.84% | 23.88M | -0.01% | 23.88M | 31.33M | 29.45% | 22.10M | -0.00% | 22.10M | 18.06M | 99.53% | 85.70K | -10.54% | 94.72K | 18.06M | 99.51% | 89.23K | 6.45% | 83.48K |
| 326,886 | 42.50M | 26.60% | 31.20M | -0.02% | 31.20M | 38.32M | 28.84% | 27.27M | 0.02% | 27.26M | 22.15M | 99.53% | 105.06K | -0.81% | 105.91K | 22.11M | 99.62% | 83.17K | 0.77% | 82.53K |
| 441,296 | 53.69M | 27.67% | 38.83M | -0.01% | 38.83M | 51.60M | 28.06% | 37.12M | -0.03% | 37.13M | 29.92M | 99.54% | 137.44K | -2.18% | 140.44K | 29.89M | 99.47% | 156.99K | -1.35% | 159.11K |
| 595,749 | 74.74M | 25.52% | 55.66M | -0.02% | 55.67M | 69.42M | 27.55% | 50.30M | 0.06% | 50.27M | 40.44M | 99.34% | 268.29K | -2.45% | 274.88K | 40.48M | 99.24% | 309.19K | 1.14% | 305.67K |
| 804,261 | 100.65M | 23.95% | 76.54M | 0.01% | 76.53M | 93.93M | 27.21% | 68.36M | 0.01% | 68.36M | 54.35M | 99.65% | 189.08K | -3.99% | 196.63K | 54.35M | 99.77% | 125.48K | -7.62% | 135.03K |

## 4. Execution Time & Throughput (per Iteration)
| Size | OOP Eval | OOP Time (ms) | OOP MEval/s | Unopt Eval | Unopt Time (ms) | Unopt MEval/s | Opt Eval | Opt Time (ms) | Opt MEval/s | Sweep Eval | Sweep Time (ms) | Sweep MEval/s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 | 198 | 0.0009 | 211.54 | 198 | 0.0007 | 301.43 | 198 | 0.0006 | 349.50 | 198 | 0.0006 | 353.63 |
| 135 | 268 | 0.0013 | 211.73 | 268 | 0.0008 | 318.71 | 268 | 0.0008 | 350.87 | 268 | 0.0008 | 354.69 |
| 182 | 362 | 0.0017 | 210.01 | 362 | 0.0011 | 327.85 | 362 | 0.0010 | 362.43 | 362 | 0.0010 | 361.11 |
| 245 | 488 | 0.0024 | 206.25 | 488 | 0.0014 | 341.63 | 488 | 0.0013 | 371.22 | 488 | 0.0013 | 366.51 |
| 330 | 658 | 0.0035 | 189.36 | 658 | 0.0019 | 354.21 | 658 | 0.0018 | 373.39 | 658 | 0.0018 | 366.31 |
| 445 | 888 | 0.0049 | 182.95 | 888 | 0.0030 | 291.92 | 888 | 0.0026 | 346.07 | 888 | 0.0024 | 366.06 |
| 600 | 1,198 | 0.0066 | 181.54 | 1,198 | 0.0045 | 266.91 | 1,198 | 0.0036 | 334.70 | 1,198 | 0.0034 | 357.35 |
| 810 | 1,618 | 0.0090 | 180.41 | 1,618 | 0.0064 | 254.23 | 1,618 | 0.0047 | 344.90 | 1,618 | 0.0045 | 360.10 |
| 1,093 | 2,184 | 0.0141 | 155.44 | 2,184 | 0.0087 | 251.93 | 2,184 | 0.0063 | 345.28 | 2,184 | 0.0061 | 360.80 |
| 1,475 | 2,948 | 0.0233 | 126.51 | 2,948 | 0.0118 | 249.01 | 2,948 | 0.0084 | 353.03 | 2,948 | 0.0081 | 364.73 |
| 1,991 | 3,980 | 0.0338 | 117.68 | 3,980 | 0.0159 | 250.42 | 3,980 | 0.0109 | 365.39 | 3,980 | 0.0108 | 367.60 |
| 2,687 | 5,372 | 0.0478 | 112.38 | 5,372 | 0.0210 | 255.31 | 5,372 | 0.0143 | 374.84 | 5,372 | 0.0145 | 371.46 |
| 3,627 | 7,252 | 0.0667 | 108.65 | 7,252 | 0.0285 | 254.75 | 7,252 | 0.0191 | 379.65 | 7,252 | 0.0194 | 373.08 |
| 4,896 | 9,790 | 0.0917 | 106.77 | 9,790 | 0.0387 | 253.23 | 9,790 | 0.0271 | 361.15 | 9,790 | 0.0262 | 373.21 |
| 6,609 | 13,216 | 0.1268 | 104.21 | 13,216 | 0.0527 | 250.96 | 13,216 | 0.0368 | 359.16 | 13,216 | 0.0354 | 373.61 |
| 8,922 | 17,842 | 0.1766 | 101.01 | 17,842 | 0.0777 | 229.53 | 17,842 | 0.0517 | 344.81 | 17,842 | 0.0477 | 373.72 |
| 12,044 | 24,086 | 0.2491 | 96.68 | 24,086 | 0.1219 | 197.61 | 24,086 | 0.0811 | 297.03 | 24,086 | 0.0648 | 371.48 |
| 16,259 | 32,516 | 0.3746 | 86.80 | 32,516 | 0.1920 | 169.31 | 32,516 | 0.1205 | 269.91 | 32,516 | 0.0884 | 367.69 |
| 21,949 | 43,896 | 0.5597 | 78.42 | 43,896 | 0.3391 | 129.43 | 43,896 | 0.1892 | 232.05 | 43,896 | 0.1347 | 325.88 |
| 29,631 | 59,260 | 0.8345 | 71.02 | 59,260 | 0.5863 | 101.07 | 59,260 | 0.2714 | 218.33 | 59,260 | 0.2103 | 281.73 |
| 40,001 | 80,000 | 1.1122 | 71.93 | 80,000 | 0.8768 | 91.24 | 80,000 | 0.4061 | 197.00 | 80,000 | 0.3349 | 238.85 |
| 54,001 | 108,000 | 1.5798 | 68.36 | 108,000 | 1.2112 | 89.17 | 108,000 | 0.5772 | 187.10 | 108,000 | 0.4901 | 220.38 |
| 72,901 | 145,800 | 2.0779 | 70.17 | 145,800 | 1.7414 | 83.73 | 145,800 | 0.7633 | 191.01 | 145,800 | 0.6802 | 214.34 |
| 98,416 | 196,830 | 2.8389 | 69.33 | 196,830 | 2.4394 | 80.69 | 196,830 | 1.0484 | 187.75 | 196,830 | 0.9307 | 211.48 |
| 132,861 | 265,720 | 3.8807 | 68.47 | 265,720 | 3.3037 | 80.43 | 265,720 | 1.4405 | 184.46 | 265,720 | 1.2971 | 204.86 |
| 179,362 | 358,722 | 5.4853 | 65.40 | 358,722 | 4.4694 | 80.26 | 358,722 | 2.0396 | 175.88 | 358,722 | 1.7486 | 205.15 |
| 242,138 | 484,274 | 7.9314 | 61.06 | 484,274 | 6.3020 | 76.84 | 484,274 | 2.7752 | 174.50 | 484,274 | 2.3852 | 203.04 |
| 326,886 | 653,770 | 12.5622 | 52.04 | 653,770 | 8.1950 | 79.78 | 653,770 | 3.7477 | 174.44 | 653,770 | 3.1626 | 206.72 |
| 441,296 | 882,590 | 26.9277 | 32.78 | 882,590 | 11.3730 | 77.60 | 882,590 | 4.9040 | 179.97 | 882,590 | 4.2454 | 207.89 |
| 595,749 | 1,191,496 | 60.4753 | 19.70 | 1,191,496 | 16.7389 | 71.18 | 1,191,496 | 6.9301 | 171.93 | 1,191,496 | 5.7818 | 206.08 |
| 804,261 | 1,608,520 | 103.6435 | 15.52 | 1,608,520 | 45.0952 | 35.67 | 1,608,520 | 9.3806 | 171.47 | 1,608,520 | 7.7733 | 206.93 |

---
