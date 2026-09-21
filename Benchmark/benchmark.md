# master_test/master_test_report_20260921_105733.md

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
| c432.v | 203 | 0.49 MB (31.8 MB peak) | N/A | 0.10 MB (7.9 MB peak) | 0.67 MB (4.4 MB peak) |
| c499.v | 275 | 0.57 MB (32.0 MB peak) | N/A | 0.10 MB (8.0 MB peak) | 0.80 MB (4.4 MB peak) |
| c880.v | 469 | 0.75 MB (32.1 MB peak) | N/A | 0.22 MB (8.0 MB peak) | 0.71 MB (4.4 MB peak) |
| c1355.v | 619 | 0.94 MB (32.3 MB peak) | N/A | 0.38 MB (8.2 MB peak) | 0.72 MB (4.4 MB peak) |
| c1908.v | 938 | 1.25 MB (32.6 MB peak) | N/A | 0.50 MB (8.3 MB peak) | 0.72 MB (4.4 MB peak) |
| c2670.v | 1,642 | 1.86 MB (33.2 MB peak) | N/A | 0.71 MB (8.6 MB peak) | 0.64 MB (4.3 MB peak) |
| c3540.v | 1,741 | 1.96 MB (33.3 MB peak) | N/A | 0.81 MB (8.6 MB peak) | 0.71 MB (4.4 MB peak) |
| c5315.v | 2,608 | 2.83 MB (34.2 MB peak) | N/A | 1.28 MB (9.1 MB peak) | 0.76 MB (4.3 MB peak) |
| c6288.v | 2,480 | 4.70 MB (36.0 MB peak) | N/A | 1.25 MB (9.1 MB peak) | 0.80 MB (4.5 MB peak) |
| c7552.v | 3,828 | 3.92 MB (35.3 MB peak) | N/A | 1.82 MB (9.7 MB peak) | 0.76 MB (4.5 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| c432.v | 203 | 0.42 ms (0.019 ms opt) | N/A | 2.93 ms | 2.51 s |
| c499.v | 275 | 0.41 ms (0.020 ms opt) | N/A | 2.77 ms | 2.55 s |
| c880.v | 469 | 0.60 ms (0.048 ms opt) | N/A | 4.21 ms | 2.53 s |
| c1355.v | 619 | 0.64 ms (0.046 ms opt) | N/A | 4.04 ms | 2.53 s |
| c1908.v | 938 | 1.10 ms (0.077 ms opt) | N/A | 6.21 ms | 2.53 s |
| c2670.v | 1,642 | 1.30 ms (0.113 ms opt) | N/A | 7.68 ms | 2.57 s |
| c3540.v | 1,741 | 1.43 ms (0.158 ms opt) | N/A | 9.07 ms | 2.61 s |
| c5315.v | 2,608 | 2.08 ms (0.204 ms opt) | N/A | 12.61 ms | 2.60 s |
| c6288.v | 2,480 | 2.01 ms (0.176 ms opt) | N/A | 11.55 ms | 2.69 s |
| c7552.v | 3,828 | 2.87 ms (0.304 ms opt) | N/A | 17.01 ms | 2.88 s |

---

## Functional State Verification (Phase 2)

| Circuit | Verification Status | Checked Vectors | Mismatches | Reference Golden Model |
|:---|:---:|---:|---:|:---|
| c432.v | **PASS** | 100 | 0 | Icarus/Golden |
| c499.v | **PASS** | 100 | 0 | Icarus/Golden |
| c880.v | **PASS** | 100 | 0 | Icarus/Golden |
| c1355.v | **PASS** | 100 | 0 | Icarus/Golden |
| c1908.v | **PASS** | 100 | 0 | Icarus/Golden |
| c2670.v | **PASS** | 100 | 0 | Icarus/Golden |
| c3540.v | **PASS** | 100 | 0 | Icarus/Golden |
| c5315.v | **PASS** | 100 | 0 | Icarus/Golden |
| c6288.v | **PASS** | 100 | 0 | Icarus/Golden |
| c7552.v | **PASS** | 100 | 0 | Icarus/Golden |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| c432.v | 45.35 ms | 53.39 ms | 65.56 ms | N/A | 406.81 ms | 5.15 ms |
| c499.v | 53.74 ms | 55.45 ms | 71.80 ms | N/A | 512.79 ms | 4.97 ms |
| c880.v | 99.92 ms | 109.21 ms | 177.58 ms | N/A | 806.70 ms | 9.28 ms |
| c1355.v | 141.71 ms | 120.47 ms | 217.48 ms | N/A | 1130.03 ms | 9.22 ms |
| c1908.v | 257.99 ms | 165.09 ms | 507.73 ms | N/A | 1911.11 ms | 10.16 ms |
| c2670.v | 401.76 ms | 348.86 ms | 751.85 ms | N/A | 3548.57 ms | 35.83 ms |
| c3540.v | 505.96 ms | 363.43 ms | 906.87 ms | N/A | 3321.68 ms | 20.11 ms |
| c5315.v | 879.28 ms | 689.52 ms | 1680.16 ms | N/A | 6699.73 ms | 31.85 ms |
| c6288.v | 4701.06 ms | 450.72 ms | 6948.11 ms | N/A | 33.70 s | 44.20 ms |
| c7552.v | 1281.13 ms | 871.11 ms | 2466.38 ms | N/A | 9854.39 ms | 46.41 ms |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| c432.v | 8.97x | 7.62x | 6.20x | N/A | 1.00x | 79.05x |
| c499.v | 9.54x | 9.25x | 7.14x | N/A | 1.00x | 103.21x |
| c880.v | 8.07x | 7.39x | 4.54x | N/A | 1.00x | 86.89x |
| c1355.v | 7.97x | 9.38x | 5.20x | N/A | 1.00x | 122.60x |
| c1908.v | 7.41x | 11.58x | 3.76x | N/A | 1.00x | 188.10x |
| c2670.v | 8.83x | 10.17x | 4.72x | N/A | 1.00x | 99.03x |
| c3540.v | 6.57x | 9.14x | 3.66x | N/A | 1.00x | 165.21x |
| c5315.v | 7.62x | 9.72x | 3.99x | N/A | 1.00x | 210.33x |
| c6288.v | 7.17x | 74.77x | 4.85x | N/A | 1.00x | 762.44x |
| c7552.v | 7.69x | 11.31x | 4.00x | N/A | 1.00x | 212.32x |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `7.94x`
- **rx-sweep (Linear Compiled):** `11.58x`
- **rx-oop (OOP Graph):** `4.70x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `157.02x`

### Cross-Engine Comparisons

- **Reactor Sweep vs Propagate Ratio:** `1.46x` (sweep faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | IPC | Cycles | Instructions | L1 Loads | L1 Hit% | L2 Hit% | LLC Misses | Brn Miss% |
|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| c432.v | rx-prop | 2.47 | 182.91M | 451.70M | 183.49M | 99.25% | 97.90% | 27.98K | 3.93% |
| c432.v | rx-sweep (Linear) | 1.82 | 225.71M | 411.37M | 169.79M | 99.47% | 97.29% | 30.21K | 5.10% |
| c432.v | rx-oop (OOP Engine) | 1.76 | 266.48M | 470.25M | 326.94M | 99.43% | 97.99% | 55.78K | 5.99% |
| c432.v | Icarus Verilog | 3.68 | 1.64B | 6.05B | 2.74B | 99.08% | 99.99% | 2.77K | 1.02% |
| c432.v | Verilator C++ | 3.96 | 13.28M | 52.64M | 24.05M | 99.63% | 98.43% | 1.41K | 1.45% |
| c499.v | rx-prop | 3.15 | 238.25M | 749.75M | 282.25M | 99.48% | 97.35% | 37.16K | 2.26% |
| c499.v | rx-sweep (Linear) | 2.48 | 243.95M | 604.77M | 233.54M | 99.40% | 97.38% | 34.18K | 2.96% |
| c499.v | rx-oop (OOP Engine) | 2.51 | 305.04M | 765.12M | 443.96M | 99.06% | 98.62% | 57.94K | 3.24% |
| c499.v | Icarus Verilog | 3.64 | 2.07B | 7.51B | 3.40B | 98.64% | 99.99% | 2.57K | 1.05% |
| c499.v | Verilator C++ | 5.02 | 8.05M | 40.42M | 12.49M | 99.80% | 98.19% | 5.27K | 0.26% |
| c880.v | rx-prop | 2.26 | 429.96M | 973.45M | 429.53M | 98.80% | 98.77% | 64.66K | 4.72% |
| c880.v | rx-sweep (Linear) | 1.72 | 464.53M | 800.91M | 369.34M | 98.14% | 98.97% | 68.87K | 5.10% |
| c880.v | rx-oop (OOP Engine) | 1.39 | 744.54M | 1.03B | 809.82M | 97.82% | 99.51% | 87.74K | 8.76% |
| c880.v | Icarus Verilog | 3.51 | 3.25B | 11.39B | 5.29B | 98.17% | 99.99% | 14.55K | 1.12% |
| c880.v | Verilator C++ | 2.48 | 29.30M | 72.67M | 33.32M | 99.66% | 97.50% | 2.79K | 3.56% |
| c1355.v | rx-prop | 2.78 | 589.36M | 1.64B | 616.91M | 97.11% | 99.68% | 56.27K | 3.42% |
| c1355.v | rx-sweep (Linear) | 2.09 | 503.43M | 1.05B | 421.27M | 95.34% | 99.73% | 58.08K | 3.18% |
| c1355.v | rx-oop (OOP Engine) | 2.03 | 891.03M | 1.81B | 1.12B | 97.10% | 99.80% | 65.90K | 5.92% |
| c1355.v | Icarus Verilog | 3.66 | 4.54B | 16.63B | 7.54B | 98.13% | 99.96% | 59.86K | 1.01% |
| c1355.v | Verilator C++ | 1.83 | 31.93M | 58.56M | 35.25M | 99.71% | 94.71% | 5.47K | 4.90% |
| c1908.v | rx-prop | 2.64 | 1.06B | 2.79B | 1.05B | 96.14% | 99.80% | 81.77K | 3.40% |
| c1908.v | rx-sweep (Linear) | 2.17 | 676.65M | 1.47B | 534.76M | 91.41% | 99.85% | 67.78K | 2.67% |
| c1908.v | rx-oop (OOP Engine) | 1.74 | 2.04B | 3.56B | 2.43B | 97.45% | 99.93% | 52.10K | 7.22% |
| c1908.v | Icarus Verilog | 3.30 | 7.75B | 25.57B | 12.35B | 97.34% | 100.00% | 11.62K | 1.20% |
| c1908.v | Verilator C++ | 2.14 | 31.77M | 68.02M | 45.93M | 99.77% | 94.24% | 6.09K | 3.65% |
| c2670.v | rx-prop | 2.23 | 1.79B | 3.98B | 1.71B | 94.82% | 99.44% | 507.52K | 4.00% |
| c2670.v | rx-sweep (Linear) | 1.94 | 1.58B | 3.07B | 1.34B | 92.54% | 99.57% | 425.99K | 3.95% |
| c2670.v | rx-oop (OOP Engine) | 1.47 | 3.19B | 4.69B | 3.52B | 96.26% | 99.66% | 445.98K | 7.73% |
| c2670.v | Icarus Verilog | 3.52 | 14.39B | 50.73B | 24.23B | 97.74% | 99.98% | 87.85K | 0.99% |
| c2670.v | Verilator C++ | 1.91 | 131.29M | 250.13M | 118.04M | 99.83% | 97.94% | 3.50K | 15.04% |
| c3540.v | rx-prop | 2.15 | 2.08B | 4.47B | 1.80B | 95.50% | 99.78% | 181.09K | 5.09% |
| c3540.v | rx-sweep (Linear) | 1.66 | 1.49B | 2.48B | 999.44M | 90.77% | 99.74% | 236.03K | 5.47% |
| c3540.v | rx-oop (OOP Engine) | 1.46 | 3.69B | 5.40B | 4.04B | 96.97% | 99.91% | 114.75K | 9.90% |
| c3540.v | Icarus Verilog | 2.93 | 13.45B | 39.41B | 20.16B | 96.66% | 99.95% | 320.01K | 1.55% |
| c3540.v | Verilator C++ | 1.85 | 68.31M | 126.12M | 74.29M | 99.93% | 89.43% | 6.03K | 2.49% |
| c5315.v | rx-prop | 2.16 | 3.68B | 7.97B | 3.26B | 92.62% | 99.85% | 354.27K | 4.47% |
| c5315.v | rx-sweep (Linear) | 1.65 | 2.89B | 4.78B | 2.09B | 91.96% | 99.79% | 352.55K | 5.64% |
| c5315.v | rx-oop (OOP Engine) | 1.42 | 6.84B | 9.73B | 7.24B | 95.70% | 99.89% | 353.08K | 8.97% |
| c5315.v | Icarus Verilog | 3.05 | 27.07B | 82.63B | 41.17B | 96.64% | 97.14% | 39.71M | 1.35% |
| c5315.v | Verilator C++ | 2.60 | 118.26M | 307.65M | 131.95M | 99.91% | 95.77% | 6.08K | 5.87% |
| c6288.v | rx-prop | 2.30 | 19.07B | 43.90B | 16.20B | 91.23% | 99.96% | 611.47K | 5.37% |
| c6288.v | rx-sweep (Linear) | 2.38 | 1.83B | 4.35B | 1.68B | 91.52% | 99.88% | 196.75K | 2.82% |
| c6288.v | rx-oop (OOP Engine) | 2.02 | 28.12B | 56.84B | 33.61B | 93.69% | 99.97% | 659.93K | 6.08% |
| c6288.v | Icarus Verilog | 3.58 | 136.36B | 488.57B | 216.34B | 95.63% | 99.67% | 31.00M | 0.81% |
| c6288.v | Verilator C++ | 1.65 | 165.98M | 274.07M | 144.65M | 99.97% | 92.32% | 2.75K | 9.41% |
| c7552.v | rx-prop | 2.17 | 5.32B | 11.55B | 4.56B | 90.38% | 99.87% | 584.25K | 4.13% |
| c7552.v | rx-sweep (Linear) | 1.82 | 3.66B | 6.67B | 2.73B | 91.61% | 99.69% | 723.08K | 4.73% |
| c7552.v | rx-oop (OOP Engine) | 1.48 | 10.08B | 14.89B | 10.82B | 94.66% | 99.85% | 876.36K | 8.32% |
| c7552.v | Icarus Verilog | 2.92 | 39.49B | 115.29B | 58.40B | 96.32% | 91.64% | 179.90M | 1.36% |
| c7552.v | Verilator C++ | 2.04 | 178.10M | 362.76M | 176.14M | 99.88% | 84.84% | 14.06K | 8.16% |

---

# master_test/master_test_report_20260921_110248.md

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
| ctrl.v | 340 | 0.67 MB (32.0 MB peak) | 0.50 MB (33.4 MB peak) | 0.18 MB (8.0 MB peak) | 0.70 MB (4.4 MB peak) |
| int2float.v | 461 | 0.76 MB (32.2 MB peak) | 0.61 MB (33.7 MB peak) | 0.17 MB (8.1 MB peak) | 0.72 MB (4.4 MB peak) |
| dec.v | 576 | 0.91 MB (32.3 MB peak) | 0.78 MB (33.8 MB peak) | 0.18 MB (8.0 MB peak) | 0.74 MB (4.4 MB peak) |
| router.v | 576 | 0.88 MB (32.2 MB peak) | 0.72 MB (33.8 MB peak) | 0.30 MB (8.1 MB peak) | 0.71 MB (4.4 MB peak) |
| cavlc.v | 1,300 | 1.56 MB (32.9 MB peak) | 1.70 MB (34.7 MB peak) | 0.67 MB (8.5 MB peak) | 0.61 MB (4.3 MB peak) |
| priority.v | 2,043 | 4.16 MB (35.5 MB peak) | 2.52 MB (35.6 MB peak) | 0.93 MB (8.8 MB peak) | 0.71 MB (4.4 MB peak) |
| adder.v | 2,547 | 2.59 MB (33.9 MB peak) | 3.03 MB (36.1 MB peak) | 1.20 MB (9.0 MB peak) | 0.77 MB (4.5 MB peak) |
| i2c.v | 2,480 | 2.61 MB (34.0 MB peak) | 2.98 MB (35.9 MB peak) | 1.12 MB (9.0 MB peak) | 0.75 MB (4.4 MB peak) |
| bar.v | 5,526 | 5.77 MB (37.0 MB peak) | 6.88 MB (39.9 MB peak) | 3.16 MB (11.0 MB peak) | 0.86 MB (4.5 MB peak) |
| max.v | 6,025 | 6.08 MB (37.4 MB peak) | 7.26 MB (40.4 MB peak) | 3.39 MB (11.2 MB peak) | 0.78 MB (4.5 MB peak) |
| arbiter.v | 23,618 | 24.58 MB (55.9 MB peak) | 29.15 MB (62.1 MB peak) | 15.26 MB (23.1 MB peak) | 0.84 MB (4.5 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| ctrl.v | 340 | 1.32 ms (0.028 ms opt) | 2.57 ms | 3.33 ms | 2.55 s |
| int2float.v | 461 | 1.30 ms (0.039 ms opt) | 2.84 ms | 3.62 ms | 2.55 s |
| dec.v | 576 | 1.33 ms (0.035 ms opt) | 3.49 ms | 3.32 ms | 2.52 s |
| router.v | 576 | 1.48 ms (0.043 ms opt) | 3.20 ms | 4.06 ms | 2.54 s |
| cavlc.v | 1,300 | 2.96 ms (0.112 ms opt) | 5.01 ms | 7.14 ms | 2.61 s |
| priority.v | 2,043 | 4.24 ms (0.118 ms opt) | 6.68 ms | 9.69 ms | 2.62 s |
| adder.v | 2,547 | 5.22 ms (0.143 ms opt) | 7.05 ms | 13.04 ms | 2.60 s |
| i2c.v | 2,480 | 4.81 ms (0.179 ms opt) | 7.19 ms | 11.92 ms | 2.59 s |
| bar.v | 5,526 | 10.78 ms (0.334 ms opt) | 16.35 ms | 25.51 ms | 3.15 s |
| max.v | 6,025 | 11.14 ms (0.340 ms opt) | 16.74 ms | 26.45 ms | 2.90 s |
| arbiter.v | 23,618 | 45.22 ms (1.243 ms opt) | 61.50 ms | 118.29 ms | 8.54 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| ctrl.v | 62.53 ms | 51.31 ms | 108.80 ms | 2882.81 ms | 413.08 ms | 3.19 ms |
| int2float.v | 77.69 ms | 93.04 ms | 119.66 ms | 3312.73 ms | 500.94 ms | 4.35 ms |
| dec.v | 16.34 ms | 26.64 ms | 20.51 ms | 1399.20 ms | 171.34 ms | 3.65 ms |
| router.v | 90.42 ms | 68.55 ms | 138.50 ms | 3848.84 ms | 739.58 ms | 7.07 ms |
| cavlc.v | 245.96 ms | 263.04 ms | 371.51 ms | 9631.01 ms | 1407.33 ms | 9.00 ms |
| priority.v | 280.35 ms | 241.29 ms | 408.43 ms | 14.57 s | 13.50 s | 43.05 ms |
| adder.v | 594.54 ms | 344.24 ms | 804.40 ms | 27.17 s | 3771.13 ms | 64.02 ms |
| i2c.v | 387.79 ms | 499.75 ms | 574.62 ms | 15.66 s | 2846.28 ms | 27.06 ms |
| bar.v | 866.52 ms | 861.04 ms | 1100.17 ms | 64.10 s | 7098.68 ms | 61.72 ms |
| max.v | 1642.56 ms | 1327.57 ms | 2131.24 ms | 70.85 s | 12.46 s | 86.93 ms |
| arbiter.v | 2795.33 ms | 2180.64 ms | 4048.85 ms | 173.11 s | 17.51 s | 171.43 ms |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| ctrl.v | 6.61x | 8.05x | 3.80x | 0.14x | 1.00x | 129.38x |
| int2float.v | 6.45x | 5.38x | 4.19x | 0.15x | 1.00x | 115.23x |
| dec.v | 10.49x | 6.43x | 8.36x | 0.12x | 1.00x | 47.00x |
| router.v | 8.18x | 10.79x | 5.34x | 0.19x | 1.00x | 104.67x |
| cavlc.v | 5.72x | 5.35x | 3.79x | 0.15x | 1.00x | 156.38x |
| priority.v | 48.16x | 55.96x | 33.06x | 0.93x | 1.00x | 313.66x |
| adder.v | 6.34x | 10.95x | 4.69x | 0.14x | 1.00x | 58.90x |
| i2c.v | 7.34x | 5.70x | 4.95x | 0.18x | 1.00x | 105.17x |
| bar.v | 8.19x | 8.24x | 6.45x | 0.11x | 1.00x | 115.02x |
| max.v | 7.59x | 9.39x | 5.85x | 0.18x | 1.00x | 143.34x |
| arbiter.v | 6.26x | 8.03x | 4.32x | 0.10x | 1.00x | 102.14x |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `8.57x`
- **rx-sweep (Linear Compiled):** `9.09x`
- **rx-oop (OOP Graph):** `5.96x`
- **Pure Python Engine:** `0.17x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `112.78x`

### Cross-Engine Comparisons

- **Cython Reactor (`rx-prop`) vs Pure Python:** `50.39x` faster
- **Cython Reactor (`rx-sweep`) vs Pure Python:** `53.45x` faster
- **Reactor Sweep vs Propagate Ratio:** `1.06x` (sweep faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | IPC | Cycles | Instructions | L1 Loads | L1 Hit% | L2 Hit% | LLC Misses | Brn Miss% |
|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| ctrl.v | rx-prop | 2.77 | 241.04M | 668.44M | 255.82M | 99.65% | 99.59% | 7.12K | 3.86% |
| ctrl.v | rx-sweep (Linear) | 2.34 | 194.06M | 453.33M | 170.65M | 99.47% | 99.62% | 4.21K | 3.93% |
| ctrl.v | rx-oop (OOP Engine) | 1.75 | 439.82M | 767.62M | 539.74M | 99.08% | 99.41% | 29.06K | 7.18% |
| ctrl.v | Pure Python Engine | 4.79 | 95.89M | 459.38M | 212.90M | 99.64% | 99.07% | 7.37K | 0.24% |
| ctrl.v | Icarus Verilog | 3.51 | 1.65B | 5.80B | 2.74B | 98.34% | 99.98% | 7.40K | 1.10% |
| ctrl.v | Verilator C++ | 0.00 | 0 | 22.72M | 4.75M | 99.22% | 92.89% | 2.65K | 0.92% |
| int2float.v | rx-prop | 2.33 | 300.49M | 700.78M | 281.45M | 99.16% | 99.67% | 7.52K | 5.51% |
| int2float.v | rx-sweep (Linear) | 1.68 | 351.12M | 589.72M | 250.45M | 98.44% | 99.83% | 7.67K | 6.40% |
| int2float.v | rx-oop (OOP Engine) | 1.65 | 475.73M | 785.71M | 574.48M | 98.37% | 99.74% | 25.72K | 7.77% |
| int2float.v | Pure Python Engine | 4.90 | 116.59M | 571.31M | 240.46M | 99.62% | 99.58% | 3.88K | 0.23% |
| int2float.v | Icarus Verilog | 3.19 | 2.01B | 6.42B | 3.16B | 97.80% | 99.94% | 40.37K | 1.32% |
| int2float.v | Verilator C++ | 4.97 | 7.77M | 38.64M | 10.98M | 99.91% | 86.50% | 4.21K | 2.51% |
| dec.v | rx-prop | 3.93 | 60.26M | 237.04M | 81.38M | 99.12% | 99.66% | 2.13K | 1.14% |
| dec.v | rx-sweep (Linear) | 2.87 | 96.25M | 275.95M | 89.12M | 98.75% | 99.47% | 5.33K | 1.95% |
| dec.v | rx-oop (OOP Engine) | 3.43 | 70.52M | 241.93M | 127.57M | 99.01% | 99.66% | 17.51K | 1.56% |
| dec.v | Pure Python Engine | 5.84 | 31.67M | 185.09M | 76.52M | 99.55% | 97.83% | 7.66K | 0.10% |
| dec.v | Icarus Verilog | 4.06 | 691.04M | 2.81B | 1.20B | 97.86% | 99.98% | 6.08K | 0.76% |
| dec.v | Verilator C++ | 27.73 | 1.47M | 40.72M | 7.77M | 99.62% | 84.63% | 4.57K | 0.75% |
| router.v | rx-prop | 2.15 | 406.34M | 873.98M | 387.23M | 98.70% | 97.67% | 133.64K | 5.00% |
| router.v | rx-sweep (Linear) | 2.60 | 305.00M | 792.33M | 311.88M | 98.32% | 97.75% | 128.04K | 2.44% |
| router.v | rx-oop (OOP Engine) | 1.56 | 585.26M | 911.47M | 651.85M | 97.75% | 99.38% | 90.88K | 7.16% |
| router.v | Pure Python Engine | 4.70 | 132.72M | 623.18M | 274.73M | 99.66% | 99.68% | 3.82K | 0.47% |
| router.v | Icarus Verilog | 3.58 | 2.95B | 10.57B | 4.95B | 98.21% | 99.98% | 17.29K | 0.99% |
| router.v | Verilator C++ | 3.51 | 25.99M | 91.34M | 39.65M | 99.68% | 95.42% | 6.08K | 0.73% |
| cavlc.v | rx-prop | 2.10 | 965.37M | 2.03B | 872.15M | 95.36% | 99.93% | 33.04K | 5.46% |
| cavlc.v | rx-sweep (Linear) | 1.55 | 1.06B | 1.65B | 711.60M | 91.17% | 99.99% | 8.22K | 6.53% |
| cavlc.v | rx-oop (OOP Engine) | 1.55 | 1.49B | 2.32B | 1.68B | 96.35% | 99.88% | 78.87K | 7.47% |
| cavlc.v | Pure Python Engine | 4.79 | 365.14M | 1.75B | 770.56M | 99.54% | 96.88% | 113.90K | 0.18% |
| cavlc.v | Icarus Verilog | 3.03 | 5.71B | 17.30B | 8.80B | 96.17% | 99.99% | 41.75K | 1.29% |
| cavlc.v | Verilator C++ | 2.16 | 30.75M | 66.31M | 38.52M | 99.93% | 94.24% | 1.63K | 2.88% |
| priority.v | rx-prop | 2.76 | 1.22B | 3.38B | 1.36B | 94.25% | 99.69% | 245.94K | 2.41% |
| priority.v | rx-sweep (Linear) | 2.62 | 1.07B | 2.82B | 1.07B | 91.08% | 99.70% | 290.62K | 2.32% |
| priority.v | rx-oop (OOP Engine) | 2.18 | 1.72B | 3.75B | 2.28B | 94.60% | 99.83% | 207.92K | 3.37% |
| priority.v | Pure Python Engine | 4.64 | 558.41M | 2.59B | 1.17B | 99.63% | 86.83% | 551.80K | 0.23% |
| priority.v | Icarus Verilog | 3.74 | 54.79B | 204.91B | 97.73B | 97.31% | 99.95% | 1.28M | 0.71% |
| priority.v | Verilator C++ | 1.31 | 164.58M | 215.88M | 143.43M | 99.87% | 94.60% | 850 | 4.91% |
| adder.v | rx-prop | 1.94 | 2.61B | 5.07B | 2.35B | 93.86% | 99.69% | 443.34K | 4.66% |
| adder.v | rx-sweep (Linear) | 2.78 | 1.60B | 4.44B | 1.76B | 91.14% | 99.72% | 444.49K | 1.96% |
| adder.v | rx-oop (OOP Engine) | 1.61 | 3.38B | 5.44B | 3.94B | 94.87% | 99.83% | 347.09K | 6.22% |
| adder.v | Pure Python Engine | 4.56 | 1.06B | 4.85B | 2.22B | 99.62% | 75.00% | 2.10M | 0.26% |
| adder.v | Icarus Verilog | 3.77 | 15.12B | 57.01B | 26.71B | 96.97% | 98.66% | 10.74M | 0.67% |
| adder.v | Verilator C++ | 1.17 | 247.45M | 290.35M | 185.55M | 99.87% | 97.90% | 5.37K | 9.38% |
| i2c.v | rx-prop | 2.11 | 1.68B | 3.54B | 1.58B | 91.96% | 99.74% | 333.75K | 4.34% |
| i2c.v | rx-sweep (Linear) | 1.60 | 2.14B | 3.44B | 1.51B | 90.86% | 99.75% | 344.55K | 5.96% |
| i2c.v | rx-oop (OOP Engine) | 1.59 | 2.41B | 3.83B | 2.76B | 94.63% | 99.85% | 214.99K | 6.65% |
| i2c.v | Pure Python Engine | 4.51 | 604.17M | 2.73B | 1.23B | 99.58% | 81.41% | 966.72K | 0.34% |
| i2c.v | Icarus Verilog | 3.43 | 11.51B | 39.51B | 19.03B | 96.74% | 98.68% | 8.18M | 0.91% |
| i2c.v | Verilator C++ | 2.45 | 95.97M | 235.60M | 121.40M | 99.82% | 92.21% | 17.60K | 7.51% |
| bar.v | rx-prop | 3.32 | 3.54B | 11.76B | 4.19B | 87.27% | 99.90% | 544.77K | 0.39% |
| bar.v | rx-sweep (Linear) | 2.10 | 3.53B | 7.40B | 3.01B | 90.33% | 99.93% | 237.33K | 4.22% |
| bar.v | rx-oop (OOP Engine) | 2.71 | 4.47B | 12.12B | 6.52B | 91.80% | 99.14% | 4.59M | 0.76% |
| bar.v | Pure Python Engine | 4.33 | 483.04M | 2.09B | 951.98M | 99.46% | 56.18% | 2.22M | 0.18% |
| bar.v | Icarus Verilog | 3.71 | 28.46B | 105.67B | 48.62B | 94.49% | 83.91% | 430.61M | 0.35% |
| bar.v | Verilator C++ | 1.73 | 243.08M | 419.52M | 231.63M | 99.92% | 96.14% | 3.41K | 6.69% |
| max.v | rx-prop | 2.15 | 7.10B | 15.24B | 6.66B | 89.92% | 99.70% | 1.99M | 3.42% |
| max.v | rx-sweep (Linear) | 1.78 | 5.81B | 10.32B | 4.55B | 90.84% | 99.65% | 1.45M | 4.98% |
| max.v | rx-oop (OOP Engine) | 1.72 | 9.01B | 15.44B | 10.75B | 92.97% | 99.61% | 2.97M | 4.97% |
| max.v | Pure Python Engine | 4.49 | 523.32M | 2.35B | 1.05B | 99.54% | 57.07% | 2.13M | 0.21% |
| max.v | Icarus Verilog | 3.30 | 49.99B | 164.82B | 82.24B | 96.32% | 83.41% | 502.53M | 0.81% |
| max.v | Verilator C++ | 2.54 | 350.32M | 891.53M | 406.47M | 99.88% | 97.62% | 11.84K | 1.39% |
| arbiter.v | rx-prop | 2.33 | 11.44B | 26.64B | 9.76B | 85.33% | 81.11% | 270.52M | 0.92% |
| arbiter.v | rx-sweep (Linear) | 2.91 | 8.96B | 26.04B | 8.40B | 87.54% | 88.73% | 117.94M | 1.34% |
| arbiter.v | rx-oop (OOP Engine) | 1.83 | 16.49B | 30.18B | 17.29B | 91.33% | 60.19% | 596.29M | 1.64% |
| arbiter.v | Pure Python Engine | 3.96 | 612.15M | 2.43B | 1.08B | 99.34% | 44.13% | 4.00M | 0.09% |
| arbiter.v | Icarus Verilog | 3.29 | 70.39B | 231.35B | 109.19B | 94.16% | 50.68% | 3.15B | 0.24% |
| arbiter.v | Verilator C++ | 1.20 | 689.56M | 826.03M | 597.17M | 99.97% | 96.08% | 16.59K | 13.77% |

---

# master_test/master_test_report_20260921_111014.md

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
| sin.v | 8,947 | 10.61 MB (42.0 MB peak) | N/A | 5.32 MB (13.1 MB peak) | 0.80 MB (4.5 MB peak) |
| voter.v | 27,720 | 29.71 MB (61.1 MB peak) | N/A | 17.83 MB (25.7 MB peak) | 0.98 MB (4.7 MB peak) |
| square.v | 35,687 | 35.47 MB (66.8 MB peak) | N/A | 22.66 MB (30.5 MB peak) | 1.27 MB (5.0 MB peak) |
| sqrt.v | 41,234 | 41.54 MB (72.9 MB peak) | N/A | 27.12 MB (34.9 MB peak) | 1.16 MB (4.8 MB peak) |
| multiplier.v | 50,760 | 48.96 MB (80.3 MB peak) | N/A | 32.97 MB (40.8 MB peak) | 1.30 MB (4.9 MB peak) |
| log2.v | 54,531 | 52.23 MB (83.6 MB peak) | N/A | 35.54 MB (43.3 MB peak) | 0.97 MB (4.7 MB peak) |
| mem_ctrl.v | 84,974 | 80.29 MB (111.7 MB peak) | N/A | 55.28 MB (63.2 MB peak) | 1.46 MB (5.2 MB peak) |
| div.v | 101,859 | 97.36 MB (128.7 MB peak) | N/A | 67.38 MB (75.2 MB peak) | 1.60 MB (5.3 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| sin.v | 8,947 | 6.86 ms (0.663 ms opt) | N/A | 42.52 ms | 2.95 s |
| voter.v | 27,720 | 20.19 ms (1.907 ms opt) | N/A | 137.33 ms | 4.59 s |
| square.v | 35,687 | 26.64 ms (4.166 ms opt) | N/A | 187.62 ms | 5.66 s |
| sqrt.v | 41,234 | 30.45 ms (4.230 ms opt) | N/A | 220.53 ms | 5.82 s |
| multiplier.v | 50,760 | 40.81 ms (7.155 ms opt) | N/A | 285.98 ms | 7.15 s |
| log2.v | 54,531 | 44.08 ms (7.850 ms opt) | N/A | 310.42 ms | 7.70 s |
| mem_ctrl.v | 84,974 | 73.78 ms (16.438 ms opt) | N/A | 933.51 ms | 13.21 s |
| div.v | 101,859 | 110.77 ms (15.548 ms opt) | N/A | 640.08 ms | 21.48 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| sin.v | 305.45 ms | 15.35 ms | 496.97 ms | N/A | 1583.97 ms | 1.02 ms |
| voter.v | 255.82 ms | 44.91 ms | 409.11 ms | N/A | 1433.64 ms | 2.81 ms |
| square.v | 230.73 ms | 64.04 ms | 333.64 ms | N/A | 1075.84 ms | 5.13 ms |
| sqrt.v | 26.82 s | 74.70 ms | 35.63 s | N/A | 131.49 s | 3.34 ms |
| multiplier.v | 1753.99 ms | 85.38 ms | 2914.64 ms | N/A | 9326.97 ms | 3.43 ms |
| log2.v | 7716.89 ms | 93.02 ms | 12.80 s | N/A | 43.65 s | 5.48 ms |
| mem_ctrl.v | 240.77 ms | 174.96 ms | 421.64 ms | N/A | 2264.82 ms | 25.62 ms |
| div.v | 436.92 ms | 121.77 ms | 638.65 ms | N/A | 2942.89 ms | 44.85 ms |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| sin.v | 5.19x | 103.22x | 3.19x | N/A | 1.00x | 1555.48x |
| voter.v | 5.60x | 31.92x | 3.50x | N/A | 1.00x | 510.15x |
| square.v | 4.66x | 16.80x | 3.22x | N/A | 1.00x | 209.63x |
| sqrt.v | 4.90x | 1760.25x | 3.69x | N/A | 1.00x | 39323.50x |
| multiplier.v | 5.32x | 109.24x | 3.20x | N/A | 1.00x | 2715.97x |
| log2.v | 5.66x | 469.26x | 3.41x | N/A | 1.00x | 7959.33x |
| mem_ctrl.v | 9.41x | 12.95x | 5.37x | N/A | 1.00x | 88.40x |
| div.v | 6.74x | 24.17x | 4.61x | N/A | 1.00x | 65.61x |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `5.79x`
- **rx-sweep (Linear Compiled):** `79.29x`
- **rx-oop (OOP Graph):** `3.71x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `975.52x`

### Cross-Engine Comparisons

- **Reactor Sweep vs Propagate Ratio:** `13.69x` (sweep faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | IPC | Cycles | Instructions | L1 Loads | L1 Hit% | L2 Hit% | LLC Misses | Brn Miss% |
|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| sin.v | rx-prop | 1.59 | 1.21B | 1.92B | 856.12M | 90.66% | 99.71% | 230.95K | 8.06% |
| sin.v | rx-sweep (Linear) | 1.96 | 47.36M | 93.00M | 30.64M | 90.06% | 96.87% | 105.68K | 5.73% |
| sin.v | rx-oop (OOP Engine) | 1.25 | 2.00B | 2.49B | 1.93B | 94.17% | 98.83% | 1.29M | 11.25% |
| sin.v | Icarus Verilog | 2.52 | 6.35B | 16.03B | 8.94B | 95.64% | 87.98% | 46.33M | 1.61% |
| sin.v | Verilator C++ | 0.00 | 0 | 29 | 6.42K | 95.20% | 0.00% | 1.65K | 2.89% |
| voter.v | rx-prop | 1.48 | 1.03B | 1.52B | 690.75M | 90.64% | 88.26% | 7.61M | 8.33% |
| voter.v | rx-sweep (Linear) | 2.04 | 181.08M | 369.53M | 136.73M | 90.21% | 86.71% | 1.82M | 4.06% |
| voter.v | rx-oop (OOP Engine) | 1.21 | 1.64B | 1.99B | 1.56B | 94.45% | 84.73% | 13.27M | 11.10% |
| voter.v | Icarus Verilog | 2.40 | 5.72B | 13.73B | 7.87B | 96.48% | 63.10% | 102.52M | 1.60% |
| voter.v | Verilator C++ | 8.59 | 1.45M | 12.44M | 766.01K | 99.89% | 0.00% | 3.54K | 5.83% |
| square.v | rx-prop | 1.37 | 904.87M | 1.24B | 575.77M | 89.92% | 86.28% | 7.96M | 7.87% |
| square.v | rx-sweep (Linear) | 1.73 | 249.22M | 431.34M | 171.04M | 89.99% | 83.15% | 2.88M | 5.29% |
| square.v | rx-oop (OOP Engine) | 1.12 | 1.33B | 1.49B | 1.23B | 94.33% | 81.12% | 13.06M | 10.93% |
| square.v | Icarus Verilog | 2.16 | 4.31B | 9.31B | 5.66B | 95.90% | 57.00% | 100.33M | 1.57% |
| square.v | Verilator C++ | 3.05 | 7.79M | 23.76M | 8.93M | 99.99% | 0.00% | 1.95K | 2.51% |
| sqrt.v | rx-prop | 1.23 | 108.17B | 132.61B | 60.67B | 88.88% | 48.99% | 3.44B | 6.55% |
| sqrt.v | rx-sweep (Linear) | 1.99 | 285.17M | 568.42M | 233.26M | 91.36% | 78.48% | 4.34M | 3.75% |
| sqrt.v | rx-oop (OOP Engine) | 1.02 | 142.76B | 145.35B | 116.52B | 94.01% | 34.89% | 4.55B | 9.04% |
| sqrt.v | Icarus Verilog | 1.83 | 526.57B | 962.89B | 617.49B | 95.71% | 21.89% | 20.69B | 1.50% |
| sqrt.v | Verilator C++ | 0.00 | 0 | 2.79M | 2.68M | 99.97% | 0.00% | 4.31K | 7.17% |
| multiplier.v | rx-prop | 1.33 | 7.04B | 9.39B | 4.45B | 89.94% | 79.75% | 91.38M | 8.06% |
| multiplier.v | rx-sweep (Linear) | 1.99 | 326.36M | 650.01M | 247.82M | 89.68% | 78.99% | 5.40M | 3.76% |
| multiplier.v | rx-oop (OOP Engine) | 1.03 | 11.64B | 12.04B | 9.99B | 94.14% | 63.16% | 215.34M | 11.01% |
| multiplier.v | Icarus Verilog | 1.87 | 37.23B | 69.54B | 44.54B | 96.22% | 28.40% | 1.21B | 1.60% |
| multiplier.v | Verilator C++ | 0.00 | 0 | 1.41M | 4.61M | 99.98% | 0.00% | 4.86K | 0.60% |
| log2.v | rx-prop | 1.31 | 31.08B | 40.85B | 19.17B | 89.49% | 63.72% | 733.56M | 7.19% |
| log2.v | rx-sweep (Linear) | 1.81 | 355.15M | 644.21M | 256.78M | 90.41% | 82.32% | 4.35M | 4.81% |
| log2.v | rx-oop (OOP Engine) | 1.00 | 51.44B | 51.40B | 43.02B | 94.33% | 45.31% | 1.34B | 10.42% |
| log2.v | Icarus Verilog | 1.83 | 174.83B | 320.46B | 204.01B | 96.07% | 22.05% | 6.25B | 1.50% |
| log2.v | Verilator C++ | 1.57 | 7.88M | 12.34M | 6.82M | 99.99% | 0.00% | 3.44K | 3.58% |
| mem_ctrl.v | rx-prop | 1.36 | 952.36M | 1.29B | 584.79M | 88.56% | 47.92% | 34.87M | 5.15% |
| mem_ctrl.v | rx-sweep (Linear) | 1.50 | 703.75M | 1.06B | 442.60M | 89.95% | 74.84% | 11.22M | 5.94% |
| mem_ctrl.v | rx-oop (OOP Engine) | 1.10 | 1.65B | 1.83B | 1.42B | 93.63% | 37.59% | 56.38M | 7.33% |
| mem_ctrl.v | Icarus Verilog | 1.62 | 9.10B | 14.73B | 8.59B | 95.97% | 19.90% | 276.12M | 0.99% |
| mem_ctrl.v | Verilator C++ | 1.18 | 94.43M | 111.90M | 45.97M | 99.64% | 0.00% | 6.90M | 1.84% |
| div.v | rx-prop | 1.47 | 1.74B | 2.57B | 1.10B | 89.04% | 55.35% | 53.63M | 4.44% |
| div.v | rx-sweep (Linear) | 2.79 | 468.08M | 1.30B | 435.00M | 89.41% | 81.42% | 8.51M | 2.04% |
| div.v | rx-oop (OOP Engine) | 1.17 | 2.55B | 2.97B | 2.09B | 93.16% | 48.74% | 73.39M | 5.64% |
| div.v | Icarus Verilog | 1.81 | 11.86B | 21.40B | 11.52B | 95.30% | 40.04% | 324.62M | 0.79% |
| div.v | Verilator C++ | 0.42 | 167.74M | 70.78M | 41.42M | 99.92% | 0.00% | 1.25M | 0.16% |

---

# master_test/master_test_report_20260921_111558.md

# Master Test Unified Benchmark Report: tests/ISCAS89

**Execution Parameters:**
- **Target Suite / Path:** `tests/ISCAS89`
- **Circuits Benchmarked:** 15
- **Simulation Vectors (Phase 3):** 50,000 (Warmup: 10)
- **Verification Vectors (Phase 2):** 100
- **Hardware Profiler:** Linux `perf` kernel PMU counters

---

## 1. Zero-Testbench Memory Footprint (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| s27.v | 19 | 0.43 MB (31.8 MB peak) | 0.16 MB (33.2 MB peak) | 0.06 MB (7.9 MB peak) | 0.58 MB (4.3 MB peak) |
| s420.v | 254 | 0.84 MB (32.2 MB peak) | 0.64 MB (33.6 MB peak) | 0.11 MB (8.0 MB peak) | 0.73 MB (4.4 MB peak) |
| s382.v | 189 | 2.81 MB (34.1 MB peak) | 0.62 MB (33.7 MB peak) | 0.10 MB (8.0 MB peak) | 0.81 MB (4.4 MB peak) |
| s641.v | 458 | 1.04 MB (32.4 MB peak) | 0.94 MB (34.0 MB peak) | 0.36 MB (8.1 MB peak) | 0.70 MB (4.4 MB peak) |
| s713.v | 471 | 1.08 MB (32.3 MB peak) | 0.98 MB (33.9 MB peak) | 0.32 MB (8.1 MB peak) | 0.59 MB (4.3 MB peak) |
| s1238.v | 555 | 1.23 MB (34.6 MB peak) | 1.05 MB (34.1 MB peak) | 0.37 MB (8.2 MB peak) | 0.75 MB (4.4 MB peak) |
| s1423.v | 754 | 2.08 MB (33.4 MB peak) | 2.27 MB (35.3 MB peak) | 0.73 MB (8.5 MB peak) | 0.72 MB (4.4 MB peak) |
| s1488.v | 687 | 1.16 MB (32.6 MB peak) | 1.09 MB (34.2 MB peak) | 0.38 MB (8.3 MB peak) | 0.70 MB (4.4 MB peak) |
| s5378.v | 3,043 | 7.46 MB (38.8 MB peak) | 6.61 MB (39.6 MB peak) | 2.28 MB (10.1 MB peak) | 0.70 MB (4.4 MB peak) |
| s9234.v | 5,884 | 9.48 MB (40.8 MB peak) | 11.40 MB (44.5 MB peak) | 4.31 MB (12.2 MB peak) | 0.72 MB (4.4 MB peak) |
| s13207.v | 8,804 | 19.64 MB (51.0 MB peak) | 18.68 MB (51.8 MB peak) | 8.02 MB (15.9 MB peak) | 0.77 MB (4.5 MB peak) |
| s15850.v | 10,534 | 20.05 MB (51.4 MB peak) | 18.95 MB (52.0 MB peak) | 8.56 MB (16.4 MB peak) | 0.71 MB (4.4 MB peak) |
| s35932.v | 18,149 | 45.29 MB (76.7 MB peak) | 44.83 MB (77.9 MB peak) | 18.92 MB (26.7 MB peak) | 0.98 MB (4.6 MB peak) |
| s38584.v | 21,022 | 43.84 MB (75.2 MB peak) | 43.78 MB (76.9 MB peak) | 20.07 MB (28.0 MB peak) | 0.92 MB (4.6 MB peak) |
| s38417.v | 23,950 | 45.96 MB (77.3 MB peak) | 52.00 MB (85.1 MB peak) | 22.53 MB (30.4 MB peak) | 0.93 MB (4.6 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| s27.v | 19 | 0.33 ms (0.008 ms opt) | 0.59 ms | 2.17 ms | 2.60 s |
| s420.v | 254 | 0.57 ms (0.042 ms opt) | 10.06 ms | 3.62 ms | 2.51 s |
| s382.v | 189 | 0.66 ms (0.041 ms opt) | 10.24 ms | 2.84 ms | 2.61 s |
| s641.v | 458 | 0.71 ms (0.057 ms opt) | 10.37 ms | 3.85 ms | 2.57 s |
| s713.v | 471 | 0.71 ms (0.065 ms opt) | 10.22 ms | 4.11 ms | 2.60 s |
| s1238.v | 555 | 0.81 ms (0.098 ms opt) | 3.05 ms | 4.82 ms | 2.63 s |
| s1423.v | 754 | 1.35 ms (0.126 ms opt) | 12.29 ms | 5.60 ms | 2.59 s |
| s1488.v | 687 | 0.88 ms (0.085 ms opt) | 10.54 ms | 5.10 ms | 2.57 s |
| s5378.v | 3,043 | 3.60 ms (0.368 ms opt) | 10.66 ms | 16.82 ms | 2.61 s |
| s9234.v | 5,884 | 6.14 ms (0.663 ms opt) | 14.72 ms | 34.06 ms | 2.69 s |
| s13207.v | 8,804 | 12.16 ms (1.494 ms opt) | 26.30 ms | 57.57 ms | 2.80 s |
| s15850.v | 10,534 | 12.40 ms (1.364 ms opt) | 27.41 ms | 67.59 ms | 2.97 s |
| s35932.v | 18,149 | 29.68 ms (4.911 ms opt) | 89.53 ms | 112.90 ms | 3.96 s |
| s38584.v | 21,022 | 29.32 ms (5.087 ms opt) | 83.28 ms | 160.33 ms | 5.61 s |
| s38417.v | 23,950 | 31.79 ms (6.211 ms opt) | 97.14 ms | 164.34 ms | 4.57 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| s27.v | 11.29 ms | 9.44 ms | 13.79 ms | 63.44 s | 94.67 ms | 3.14 ms |
| s420.v | 44.65 ms | 51.80 ms | 73.86 ms | 302.13 s | 337.59 ms | 7.74 ms |
| s382.v | 48.66 ms | 48.50 ms | 78.04 ms | 336.84 s | 179.48 ms | 3.66 ms |
| s641.v | 89.14 ms | 95.64 ms | 150.25 ms | 508.57 s | 648.07 ms | 11.73 ms |
| s713.v | 91.17 ms | 98.44 ms | 164.13 ms | 500.99 s | 676.99 ms | 10.49 ms |
| s1238.v | 157.08 ms | 230.64 ms | 288.33 ms | 735.59 s | 838.18 ms | 19.31 ms |
| s1423.v | 270.60 ms | 278.92 ms | 423.64 ms | 1437.59 s | 837.40 ms | 16.05 ms |
| s1488.v | 62.53 ms | 77.25 ms | 128.12 ms | 388.84 s | 538.35 ms | 13.52 ms |
| s5378.v | 802.49 ms | 877.46 ms | 1147.71 ms | 21254.65 s | 2348.52 ms | 28.62 ms |
| s9234.v | 821.29 ms | 1002.44 ms | 1325.67 ms | 25674.34 s | 2914.81 ms | 21.40 ms |
| s13207.v | 1978.87 ms | 2621.85 ms | 3510.97 ms | 61041.99 s | 5135.87 ms | 59.13 ms |
| s15850.v | 1845.72 ms | 2272.45 ms | 3440.45 ms | 60911.65 s | 6842.98 ms | 70.99 ms |
| s35932.v | 7742.65 ms | 6810.94 ms | 10.85 s | 246608.85 s | 20.63 s | 194.19 ms |
| s38584.v | 8403.45 ms | 9851.87 ms | 13.79 s | 227075.56 s | 23.61 s | 173.26 ms |
| s38417.v | 5830.74 ms | 6264.81 ms | 9495.27 ms | 347305.65 s | 14.40 s | 169.20 ms |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| s27.v | 8.38x | 10.03x | 6.87x | 0.00x | 1.00x | 30.18x |
| s420.v | 7.56x | 6.52x | 4.57x | 0.00x | 1.00x | 43.61x |
| s382.v | 3.69x | 3.70x | 2.30x | 0.00x | 1.00x | 49.04x |
| s641.v | 7.27x | 6.78x | 4.31x | 0.00x | 1.00x | 55.27x |
| s713.v | 7.43x | 6.88x | 4.12x | 0.00x | 1.00x | 64.56x |
| s1238.v | 5.34x | 3.63x | 2.91x | 0.00x | 1.00x | 43.40x |
| s1423.v | 3.09x | 3.00x | 1.98x | 0.00x | 1.00x | 52.18x |
| s1488.v | 8.61x | 6.97x | 4.20x | 0.00x | 1.00x | 39.81x |
| s5378.v | 2.93x | 2.68x | 2.05x | 0.00x | 1.00x | 82.05x |
| s9234.v | 3.55x | 2.91x | 2.20x | 0.00x | 1.00x | 136.22x |
| s13207.v | 2.60x | 1.96x | 1.46x | 0.00x | 1.00x | 86.86x |
| s15850.v | 3.71x | 3.01x | 1.99x | 0.00x | 1.00x | 96.39x |
| s35932.v | 2.66x | 3.03x | 1.90x | 0.00x | 1.00x | 106.26x |
| s38584.v | 2.81x | 2.40x | 1.71x | 0.00x | 1.00x | 136.24x |
| s38417.v | 2.47x | 2.30x | 1.52x | 0.00x | 1.00x | 85.13x |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `4.31x`
- **rx-sweep (Linear Compiled):** `3.87x`
- **rx-oop (OOP Graph):** `2.63x`
- **Pure Python Engine:** `0.00x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `66.88x`

### Cross-Engine Comparisons

- **Cython Reactor (`rx-prop`) vs Pure Python:** `13064.81x` faster
- **Cython Reactor (`rx-sweep`) vs Pure Python:** `11727.98x` faster
- **Reactor Sweep vs Propagate Ratio:** `0.90x` (propagate faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | IPC | Cycles | Instructions | L1 Loads | L1 Hit% | L2 Hit% | LLC Misses | Brn Miss% |
|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| s27.v | rx-prop | 3.87 | 53.57M | 207.11M | 75.76M | 99.24% | 93.95% | 30.52K | 0.47% |
| s27.v | rx-sweep (Linear) | 4.94 | 37.99M | 187.57M | 55.89M | 99.35% | 98.02% | 12.17K | 0.34% |
| s27.v | rx-oop (OOP Engine) | 3.81 | 44.28M | 168.66M | 73.97M | 99.94% | 94.19% | 2.52K | 0.84% |
| s27.v | Pure Python Engine | 42.66 | 1.36M | 58.22M | 10.25M | 99.81% | 96.96% | 3.15K | 0.22% |
| s27.v | Icarus Verilog | 3.69 | 380.48M | 1.40B | 629.07M | 99.99% | 90.03% | 4.96K | 1.28% |
| s27.v | Verilator C++ | 10.68 | 1.48M | 15.82M | 4.46M | 99.94% | 0.00% | 4.05K | 0.28% |
| s420.v | rx-prop | 4.17 | 191.79M | 800.56M | 271.13M | 99.64% | 98.13% | 27.52K | 0.79% |
| s420.v | rx-sweep (Linear) | 4.28 | 201.02M | 859.99M | 263.36M | 99.57% | 97.19% | 43.70K | 0.88% |
| s420.v | rx-oop (OOP Engine) | 2.84 | 313.94M | 891.29M | 498.14M | 98.97% | 98.99% | 54.48K | 1.80% |
| s420.v | Pure Python Engine | 4.93 | 95.77M | 471.88M | 213.10M | 99.49% | 98.88% | 11.35K | 0.24% |
| s420.v | Icarus Verilog | 3.90 | 1.36B | 5.30B | 2.44B | 99.31% | 99.87% | 19.32K | 0.76% |
| s420.v | Verilator C++ | 2.69 | 30.94M | 83.23M | 41.32M | 99.75% | 99.66% | 352 | 0.17% |
| s382.v | rx-prop | 4.38 | 193.19M | 846.84M | 290.52M | 99.90% | 98.82% | 3.15K | 0.35% |
| s382.v | rx-sweep (Linear) | 4.70 | 191.29M | 899.84M | 272.99M | 99.81% | 97.74% | 11.47K | 0.45% |
| s382.v | rx-oop (OOP Engine) | 3.11 | 303.77M | 943.91M | 509.57M | 99.42% | 99.78% | 6.68K | 1.19% |
| s382.v | Pure Python Engine | 5.05 | 117.16M | 591.56M | 246.95M | 99.48% | 99.91% | 1.12K | 0.17% |
| s382.v | Icarus Verilog | 3.96 | 713.62M | 2.82B | 1.36B | 99.11% | 99.95% | 6.07K | 0.72% |
| s382.v | Verilator C++ | 11.65 | 1.19M | 13.82M | 6.98K | 82.69% | 0.08% | 1.20K | 0.18% |
| s641.v | rx-prop | 3.35 | 397.16M | 1.33B | 499.55M | 98.60% | 99.08% | 72.41K | 1.53% |
| s641.v | rx-sweep (Linear) | 3.33 | 421.65M | 1.41B | 478.32M | 97.47% | 99.46% | 64.74K | 1.17% |
| s641.v | rx-oop (OOP Engine) | 2.24 | 647.68M | 1.45B | 866.28M | 97.64% | 99.39% | 111.76K | 3.28% |
| s641.v | Pure Python Engine | 4.66 | 185.76M | 865.38M | 374.67M | 99.51% | 96.75% | 55.04K | 0.39% |
| s641.v | Icarus Verilog | 4.01 | 2.57B | 10.30B | 4.62B | 98.70% | 99.86% | 72.89K | 0.71% |
| s641.v | Verilator C++ | 2.76 | 40.38M | 111.64M | 48.88M | 99.88% | 96.42% | 3.63K | 1.17% |
| s713.v | rx-prop | 3.30 | 416.08M | 1.37B | 527.94M | 98.43% | 99.01% | 85.99K | 1.53% |
| s713.v | rx-sweep (Linear) | 3.35 | 436.94M | 1.46B | 483.46M | 96.98% | 99.47% | 75.19K | 1.12% |
| s713.v | rx-oop (OOP Engine) | 2.09 | 700.24M | 1.46B | 918.77M | 97.67% | 99.49% | 114.74K | 3.70% |
| s713.v | Pure Python Engine | 4.95 | 175.13M | 867.39M | 381.12M | 99.53% | 99.47% | 11.89K | 0.19% |
| s713.v | Icarus Verilog | 3.87 | 2.73B | 10.56B | 4.81B | 98.71% | 99.97% | 19.91K | 0.77% |
| s713.v | Verilator C++ | 3.50 | 25.96M | 90.81M | 46.64M | 99.87% | 94.21% | 3.31K | 1.65% |
| s1238.v | rx-prop | 2.58 | 647.74M | 1.67B | 627.72M | 96.35% | 99.81% | 42.28K | 3.37% |
| s1238.v | rx-sweep (Linear) | 1.82 | 931.86M | 1.70B | 628.03M | 93.82% | 99.84% | 63.28K | 4.57% |
| s1238.v | rx-oop (OOP Engine) | 1.52 | 1.17B | 1.79B | 1.28B | 96.89% | 99.87% | 57.52K | 7.76% |
| s1238.v | Pure Python Engine | 4.75 | 279.86M | 1.33B | 580.23M | 99.56% | 98.28% | 23.64K | 0.25% |
| s1238.v | Icarus Verilog | 3.06 | 3.39B | 10.38B | 5.06B | 97.21% | 99.99% | 11.34K | 1.47% |
| s1238.v | Verilator C++ | 1.79 | 67.00M | 120.00M | 73.22M | 99.98% | 69.38% | 4.96K | 2.10% |
| s1423.v | rx-prop | 3.19 | 1.11B | 3.53B | 1.23B | 91.82% | 99.97% | 46.54K | 1.02% |
| s1423.v | rx-sweep (Linear) | 3.34 | 1.14B | 3.80B | 1.17B | 86.69% | 99.98% | 48.55K | 1.06% |
| s1423.v | rx-oop (OOP Engine) | 2.29 | 1.73B | 3.97B | 2.35B | 92.65% | 99.96% | 69.14K | 2.70% |
| s1423.v | Pure Python Engine | 4.73 | 544.67M | 2.58B | 1.15B | 99.42% | 95.67% | 277.91K | 0.19% |
| s1423.v | Icarus Verilog | 3.80 | 3.35B | 12.73B | 6.09B | 97.53% | 99.91% | 138.54K | 0.74% |
| s1423.v | Verilator C++ | 1.73 | 64.60M | 111.79M | 74.22M | 99.84% | 96.70% | 3.96K | 1.42% |
| s1488.v | rx-prop | 3.37 | 256.95M | 867.05M | 319.50M | 97.27% | 99.87% | 11.29K | 1.49% |
| s1488.v | rx-sweep (Linear) | 3.30 | 308.03M | 1.02B | 315.97M | 96.08% | 99.91% | 9.78K | 1.44% |
| s1488.v | rx-oop (OOP Engine) | 1.86 | 514.93M | 956.28M | 657.63M | 97.48% | 99.67% | 51.43K | 5.19% |
| s1488.v | Pure Python Engine | 4.85 | 143.88M | 698.55M | 303.58M | 99.58% | 98.81% | 22.01K | 0.26% |
| s1488.v | Icarus Verilog | 3.31 | 2.15B | 7.13B | 3.36B | 97.48% | 99.90% | 111.88K | 1.20% |
| s1488.v | Verilator C++ | 2.32 | 49.57M | 115.17M | 57.74M | 99.96% | 89.89% | 1.22K | 0.95% |
| s5378.v | rx-prop | 2.86 | 3.29B | 9.43B | 3.36B | 88.85% | 99.95% | 205.54K | 1.69% |
| s5378.v | rx-sweep (Linear) | 3.02 | 3.60B | 10.87B | 3.34B | 84.60% | 99.95% | 251.80K | 1.48% |
| s5378.v | rx-oop (OOP Engine) | 2.23 | 4.64B | 10.32B | 6.17B | 91.68% | 99.84% | 946.89K | 3.37% |
| s5378.v | Pure Python Engine | 4.47 | 295.91M | 1.32B | 591.79M | 99.41% | 53.98% | 1.60M | 0.18% |
| s5378.v | Icarus Verilog | 3.48 | 9.43B | 32.78B | 16.20B | 97.01% | 98.23% | 8.52M | 0.85% |
| s5378.v | Verilator C++ | 2.13 | 109.90M | 234.02M | 135.34M | 99.91% | 98.16% | 2.12K | 1.39% |
| s9234.v | rx-prop | 3.06 | 3.36B | 10.29B | 3.62B | 87.99% | 99.85% | 665.11K | 1.15% |
| s9234.v | rx-sweep (Linear) | 3.19 | 4.09B | 13.08B | 3.78B | 82.04% | 99.73% | 1.88M | 1.05% |
| s9234.v | rx-oop (OOP Engine) | 2.17 | 5.38B | 11.70B | 7.14B | 91.49% | 99.02% | 6.00M | 3.14% |
| s9234.v | Pure Python Engine | 4.39 | 354.19M | 1.56B | 699.52M | 99.45% | 44.80% | 2.13M | 0.16% |
| s9234.v | Icarus Verilog | 3.31 | 11.75B | 38.91B | 19.99B | 96.87% | 88.79% | 70.24M | 0.77% |
| s9234.v | Verilator C++ | 2.13 | 79.49M | 169.31M | 112.53M | 99.89% | 99.48% | 2.88K | 2.66% |
| s13207.v | rx-prop | 3.21 | 8.03B | 25.81B | 8.92B | 85.85% | 98.90% | 13.86M | 0.85% |
| s13207.v | rx-sweep (Linear) | 3.01 | 10.62B | 31.93B | 9.81B | 84.29% | 94.52% | 84.55M | 1.33% |
| s13207.v | rx-oop (OOP Engine) | 2.06 | 14.08B | 29.00B | 17.55B | 90.35% | 85.29% | 249.14M | 2.45% |
| s13207.v | Pure Python Engine | 4.32 | 866.24M | 3.74B | 1.66B | 99.40% | 20.60% | 7.94M | 0.17% |
| s13207.v | Icarus Verilog | 3.22 | 20.72B | 66.72B | 35.14B | 96.86% | 75.06% | 275.38M | 0.60% |
| s13207.v | Verilator C++ | 1.59 | 236.40M | 374.92M | 277.07M | 99.97% | 98.94% | 1.54K | 3.64% |
| s15850.v | rx-prop | 3.19 | 7.52B | 24.00B | 8.37B | 86.59% | 98.42% | 17.74M | 0.90% |
| s15850.v | rx-sweep (Linear) | 3.19 | 9.25B | 29.50B | 8.66B | 83.13% | 94.47% | 80.82M | 1.03% |
| s15850.v | rx-oop (OOP Engine) | 2.01 | 13.86B | 27.91B | 17.27B | 91.65% | 84.31% | 226.58M | 2.73% |
| s15850.v | Pure Python Engine | 4.22 | 859.52M | 3.63B | 1.65B | 99.42% | 26.59% | 6.92M | 0.19% |
| s15850.v | Icarus Verilog | 3.08 | 27.37B | 84.30B | 44.44B | 96.73% | 66.33% | 489.84M | 0.64% |
| s15850.v | Verilator C++ | 1.60 | 287.09M | 458.94M | 337.42M | 99.92% | 97.58% | 3.13K | 6.70% |
| s35932.v | rx-prop | 2.89 | 31.14B | 89.85B | 30.53B | 84.01% | 81.82% | 887.37M | 0.16% |
| s35932.v | rx-sweep (Linear) | 3.64 | 27.26B | 99.29B | 29.42B | 83.84% | 88.46% | 548.52M | 0.23% |
| s35932.v | rx-oop (OOP Engine) | 2.37 | 43.63B | 103.22B | 55.65B | 88.54% | 67.61% | 2.07B | 0.34% |
| s35932.v | Pure Python Engine | 4.12 | 3.54B | 14.62B | 6.60B | 99.37% | 24.81% | 31.65M | 0.18% |
| s35932.v | Icarus Verilog | 3.93 | 82.86B | 325.82B | 153.49B | 94.53% | 71.21% | 2.42B | 0.11% |
| s35932.v | Verilator C++ | 0.86 | 776.72M | 665.22M | 719.56M | 99.98% | 96.41% | 2.06K | 0.44% |
| s38584.v | rx-prop | 2.26 | 33.55B | 75.72B | 27.67B | 85.70% | 79.38% | 816.19M | 1.73% |
| s38584.v | rx-sweep (Linear) | 2.24 | 39.51B | 88.34B | 30.42B | 86.15% | 84.97% | 633.23M | 2.32% |
| s38584.v | rx-oop (OOP Engine) | 1.56 | 55.47B | 86.78B | 56.66B | 91.10% | 54.21% | 2.31B | 3.59% |
| s38584.v | Pure Python Engine | 3.46 | 3.28B | 11.38B | 5.16B | 99.43% | 15.52% | 25.04M | 0.25% |
| s38584.v | Icarus Verilog | 2.43 | 94.71B | 229.87B | 130.44B | 95.80% | 49.82% | 2.75B | 0.98% |
| s38584.v | Verilator C++ | 1.43 | 700.54M | 1.00B | 800.74M | 99.98% | 96.92% | 2.31K | 5.54% |
| s38417.v | rx-prop | 2.78 | 23.45B | 65.13B | 22.58B | 84.44% | 83.81% | 569.40M | 0.59% |
| s38417.v | rx-sweep (Linear) | 3.20 | 25.23B | 80.75B | 23.64B | 83.27% | 88.64% | 449.51M | 0.75% |
| s38417.v | rx-oop (OOP Engine) | 2.00 | 38.13B | 76.38B | 44.32B | 89.92% | 60.05% | 1.78B | 1.31% |
| s38417.v | Pure Python Engine | 4.28 | 1.12B | 4.81B | 2.14B | 99.40% | 18.56% | 10.46M | 0.13% |
| s38417.v | Icarus Verilog | 3.27 | 57.87B | 189.44B | 98.32B | 96.17% | 64.99% | 1.32B | 0.38% |
| s38417.v | Verilator C++ | 1.38 | 681.82M | 944.13M | 656.93M | 99.97% | 95.85% | 3.88K | 0.97% |

---

# master_test/master_test_report_20260921_113748.md

# Master Test Unified Benchmark Report: tests/IWLS2005/itc99

**Execution Parameters:**
- **Target Suite / Path:** `tests/IWLS2005/itc99`
- **Circuits Benchmarked:** 21
- **Simulation Vectors (Phase 3):** 50,000 (Warmup: 10)
- **Verification Vectors (Phase 2):** 100
- **Hardware Profiler:** Linux `perf` kernel PMU counters

---

## 1. Zero-Testbench Memory Footprint (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| b02.v | 52 | 0.48 MB (31.9 MB peak) | N/A | 0.46 MB (8.2 MB peak) | 0.71 MB (4.4 MB peak) |
| b01.v | 101 | 0.55 MB (31.9 MB peak) | N/A | 0.51 MB (8.4 MB peak) | 0.69 MB (4.4 MB peak) |
| b06.v | 100 | 0.59 MB (32.0 MB peak) | N/A | 0.53 MB (8.4 MB peak) | 0.71 MB (4.4 MB peak) |
| b08.v | 309 | 1.00 MB (32.4 MB peak) | N/A | 1.22 MB (9.1 MB peak) | 0.71 MB (4.4 MB peak) |
| b09.v | 331 | 1.12 MB (32.5 MB peak) | N/A | 1.31 MB (9.1 MB peak) | 0.71 MB (4.4 MB peak) |
| b10.v | 417 | 2.95 MB (34.4 MB peak) | N/A | 1.39 MB (9.2 MB peak) | 0.72 MB (4.4 MB peak) |
| b03.v | 549 | 3.28 MB (34.6 MB peak) | N/A | 1.89 MB (9.7 MB peak) | 0.72 MB (4.4 MB peak) |
| b13.v | 540 | 1.75 MB (33.1 MB peak) | N/A | 2.18 MB (10.0 MB peak) | 0.73 MB (4.4 MB peak) |
| b07.v | 859 | 1.96 MB (33.3 MB peak) | N/A | 3.19 MB (11.0 MB peak) | 0.78 MB (4.4 MB peak) |
| b11.v | 1,046 | 1.91 MB (33.1 MB peak) | N/A | 3.14 MB (11.0 MB peak) | 0.75 MB (4.4 MB peak) |
| b04.v | 1,259 | 2.55 MB (33.9 MB peak) | N/A | 3.82 MB (11.6 MB peak) | 0.78 MB (4.4 MB peak) |
| b05.v | 1,292 | 2.09 MB (33.6 MB peak) | N/A | 3.93 MB (11.7 MB peak) | 0.74 MB (4.4 MB peak) |
| b12.v | 2,937 | 4.95 MB (36.3 MB peak) | N/A | 8.80 MB (16.7 MB peak) | 0.93 MB (4.5 MB peak) |
| b14.v | 10,624 | 15.21 MB (46.5 MB peak) | N/A | 36.74 MB (44.6 MB peak) | 1.16 MB (4.7 MB peak) |
| b15.v | 17,594 | 25.21 MB (58.2 MB peak) | N/A | 56.78 MB (64.7 MB peak) | 1.18 MB (4.9 MB peak) |
| b21.v | 23,092 | 28.96 MB (63.4 MB peak) | N/A | 78.64 MB (86.4 MB peak) | 1.28 MB (5.0 MB peak) |
| b20.v | 23,839 | 29.74 MB (64.7 MB peak) | N/A | 80.02 MB (87.8 MB peak) | 1.25 MB (4.9 MB peak) |
| b22.v | 34,903 | 40.77 MB (78.2 MB peak) | N/A | 119.07 MB (126.9 MB peak) | 1.19 MB (4.9 MB peak) |
| b17.v | 52,250 | 59.37 MB (94.9 MB peak) | N/A | 173.06 MB (180.9 MB peak) | 1.33 MB (5.0 MB peak) |
| b18.v | 132,940 | 139.50 MB (188.6 MB peak) | N/A | 429.03 MB (436.9 MB peak) | 2.23 MB (5.9 MB peak) |
| b19.v | 257,489 | 269.19 MB (337.4 MB peak) | N/A | 828.54 MB (836.3 MB peak) | 3.32 MB (7.0 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| b02.v | 52 | 0.36 ms (0.013 ms opt) | N/A | 3.87 ms | 2.50 s |
| b01.v | 101 | 0.45 ms (0.018 ms opt) | N/A | 4.93 ms | 2.59 s |
| b06.v | 100 | 0.64 ms (0.022 ms opt) | N/A | 5.32 ms | 2.58 s |
| b08.v | 309 | 0.85 ms (0.057 ms opt) | N/A | 7.23 ms | 2.56 s |
| b09.v | 331 | 1.02 ms (0.066 ms opt) | N/A | 7.91 ms | 2.58 s |
| b10.v | 417 | 0.82 ms (0.065 ms opt) | N/A | 9.00 ms | 2.59 s |
| b03.v | 549 | 1.16 ms (0.083 ms opt) | N/A | 9.65 ms | 2.62 s |
| b13.v | 540 | 1.38 ms (0.117 ms opt) | N/A | 10.49 ms | 2.62 s |
| b07.v | 859 | 1.59 ms (0.138 ms opt) | N/A | 16.09 ms | 2.68 s |
| b11.v | 1,046 | 1.81 ms (0.134 ms opt) | N/A | 15.82 ms | 2.70 s |
| b04.v | 1,259 | 2.34 ms (0.187 ms opt) | N/A | 18.57 ms | 2.69 s |
| b05.v | 1,292 | 1.74 ms (0.166 ms opt) | N/A | 21.54 ms | 2.66 s |
| b12.v | 2,937 | 3.83 ms (0.399 ms opt) | N/A | 46.31 ms | 3.16 s |
| b14.v | 10,624 | 11.30 ms (1.490 ms opt) | N/A | 179.01 ms | 6.21 s |
| b15.v | 17,594 | 19.07 ms (2.490 ms opt) | N/A | 289.09 ms | 8.66 s |
| b21.v | 23,092 | 31.15 ms (4.317 ms opt) | N/A | 405.39 ms | 10.75 s |
| b20.v | 23,839 | 31.82 ms (4.031 ms opt) | N/A | 413.87 ms | 11.12 s |
| b22.v | 34,903 | 38.11 ms (9.683 ms opt) | N/A | 640.55 ms | 16.59 s |
| b17.v | 52,250 | 65.19 ms (17.532 ms opt) | N/A | 945.01 ms | 23.13 s |
| b18.v | 132,940 | 275.19 ms (57.198 ms opt) | N/A | 2.42 s | 67.43 s |
| b19.v | 257,489 | 591.66 ms (123.638 ms opt) | N/A | 4.81 s | 162.86 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| b02.v | 22.07 ms | 14.43 ms | 26.99 ms | N/A | 156.23 ms | 4.23 ms |
| b01.v | 27.52 ms | 21.71 ms | 45.96 ms | N/A | 182.30 ms | 4.79 ms |
| b06.v | 37.19 ms | 29.78 ms | 61.63 ms | N/A | 160.85 ms | 11.32 ms |
| b08.v | 57.90 ms | 69.58 ms | 94.35 ms | N/A | 258.56 ms | 22.00 ms |
| b09.v | 67.00 ms | 69.90 ms | 99.04 ms | N/A | 252.27 ms | 18.50 ms |
| b10.v | 82.09 ms | 88.63 ms | 157.08 ms | N/A | 426.03 ms | 25.13 ms |
| b03.v | 111.19 ms | 124.44 ms | 192.27 ms | N/A | 274.69 ms | 22.87 ms |
| b13.v | 136.94 ms | 148.94 ms | 192.94 ms | N/A | 366.85 ms | 52.50 ms |
| b07.v | 128.49 ms | 146.10 ms | 191.64 ms | N/A | 296.04 ms | 35.12 ms |
| b11.v | 156.34 ms | 168.41 ms | 311.20 ms | N/A | 398.24 ms | 44.26 ms |
| b04.v | 357.45 ms | 397.53 ms | 566.98 ms | N/A | 1414.67 ms | 75.65 ms |
| b05.v | 92.24 ms | 142.77 ms | 147.06 ms | N/A | 190.56 ms | 52.99 ms |
| b12.v | 342.53 ms | 399.16 ms | 464.19 ms | N/A | 893.65 ms | 130.77 ms |
| b14.v | 4414.55 ms | 2787.98 ms | 7224.92 ms | N/A | 6677.90 ms | 443.73 ms |
| b15.v | 1739.79 ms | 2280.98 ms | 2886.97 ms | N/A | 5459.13 ms | 705.72 ms |
| b21.v | 5599.38 ms | 3940.06 ms | 9153.37 ms | N/A | 8556.27 ms | 1039.71 ms |
| b20.v | 7005.18 ms | 4733.54 ms | 10.30 s | N/A | 10.00 s | 1092.49 ms |
| b22.v | 12.85 s | 8534.45 ms | 20.14 s | N/A | 20.01 s | 2156.80 ms |
| b17.v | 6460.78 ms | 7209.14 ms | 10.03 s | N/A | 12.84 s | 5364.96 ms |
| b18.v | 23.61 s | 18.76 s | 34.36 s | N/A | 102.60 s | 28.08 s |
| b19.v | 37.86 s | 34.03 s | 54.01 s | N/A | 146.82 s | 63.92 s |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| b02.v | 7.08x | 10.83x | 5.79x | N/A | 1.00x | 36.97x |
| b01.v | 6.62x | 8.40x | 3.97x | N/A | 1.00x | 38.07x |
| b06.v | 4.33x | 5.40x | 2.61x | N/A | 1.00x | 14.21x |
| b08.v | 4.47x | 3.72x | 2.74x | N/A | 1.00x | 11.75x |
| b09.v | 3.77x | 3.61x | 2.55x | N/A | 1.00x | 13.63x |
| b10.v | 5.19x | 4.81x | 2.71x | N/A | 1.00x | 16.95x |
| b03.v | 2.47x | 2.21x | 1.43x | N/A | 1.00x | 12.01x |
| b13.v | 2.68x | 2.46x | 1.90x | N/A | 1.00x | 6.99x |
| b07.v | 2.30x | 2.03x | 1.54x | N/A | 1.00x | 8.43x |
| b11.v | 2.55x | 2.36x | 1.28x | N/A | 1.00x | 9.00x |
| b04.v | 3.96x | 3.56x | 2.50x | N/A | 1.00x | 18.70x |
| b05.v | 2.07x | 1.33x | 1.30x | N/A | 1.00x | 3.60x |
| b12.v | 2.61x | 2.24x | 1.93x | N/A | 1.00x | 6.83x |
| b14.v | 1.51x | 2.40x | 0.92x | N/A | 1.00x | 15.05x |
| b15.v | 3.14x | 2.39x | 1.89x | N/A | 1.00x | 7.74x |
| b21.v | 1.53x | 2.17x | 0.93x | N/A | 1.00x | 8.23x |
| b20.v | 1.43x | 2.11x | 0.97x | N/A | 1.00x | 9.16x |
| b22.v | 1.56x | 2.34x | 0.99x | N/A | 1.00x | 9.28x |
| b17.v | 1.99x | 1.78x | 1.28x | N/A | 1.00x | 2.39x |
| b18.v | 4.35x | 5.47x | 2.99x | N/A | 1.00x | 3.65x |
| b19.v | 3.88x | 4.32x | 2.72x | N/A | 1.00x | 2.30x |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `2.96x`
- **rx-sweep (Linear Compiled):** `3.11x`
- **rx-oop (OOP Graph):** `1.89x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `9.38x`

### Cross-Engine Comparisons

- **Reactor Sweep vs Propagate Ratio:** `1.05x` (sweep faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | IPC | Cycles | Instructions | L1 Loads | L1 Hit% | L2 Hit% | LLC Misses | Brn Miss% |
|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| b02.v | rx-prop | 5.65 | 60.78M | 343.27M | 88.16M | 99.89% | 95.90% | 3.90K | 0.23% |
| b02.v | rx-sweep (Linear) | 4.84 | 63.63M | 308.28M | 97.88M | 99.69% | 77.51% | 66.21K | 0.10% |
| b02.v | rx-oop (OOP Engine) | 3.55 | 111.65M | 396.25M | 212.65M | 99.36% | 96.05% | 54.12K | 0.33% |
| b02.v | Icarus Verilog | 3.82 | 631.99M | 2.41B | 1.06B | 99.80% | 97.68% | 50.27K | 0.90% |
| b02.v | Verilator C++ | 8.16 | 6.88M | 56.20M | 10.23M | 99.87% | 87.00% | 1.74K | 0.40% |
| b01.v | rx-prop | 4.75 | 101.91M | 483.76M | 157.68M | 99.97% | 91.96% | 4.02K | 0.26% |
| b01.v | rx-sweep (Linear) | 4.84 | 95.44M | 461.56M | 135.95M | 99.58% | 96.82% | 17.93K | 0.24% |
| b01.v | rx-oop (OOP Engine) | 3.06 | 184.78M | 566.31M | 308.45M | 99.87% | 97.59% | 10.03K | 1.61% |
| b01.v | Icarus Verilog | 3.82 | 772.97M | 2.96B | 1.34B | 99.49% | 99.69% | 20.55K | 0.87% |
| b01.v | Verilator C++ | 5.74 | 12.39M | 71.12M | 17.20M | 99.92% | 95.93% | 576 | 0.58% |
| b06.v | rx-prop | 4.70 | 153.05M | 718.64M | 236.08M | 99.90% | 95.80% | 9.79K | 0.27% |
| b06.v | rx-sweep (Linear) | 4.74 | 128.18M | 607.77M | 189.28M | 99.87% | 74.41% | 74.33K | 0.22% |
| b06.v | rx-oop (OOP Engine) | 3.16 | 257.56M | 814.43M | 449.29M | 99.67% | 97.58% | 37.08K | 1.10% |
| b06.v | Icarus Verilog | 4.16 | 683.72M | 2.85B | 1.24B | 99.71% | 99.02% | 36.43K | 0.69% |
| b06.v | Verilator C++ | 2.32 | 36.40M | 84.34M | 36.99M | 99.99% | 41.05% | 2.99K | 1.31% |
| b08.v | rx-prop | 4.24 | 239.26M | 1.01B | 346.99M | 99.33% | 98.83% | 27.43K | 0.51% |
| b08.v | rx-sweep (Linear) | 3.95 | 291.69M | 1.15B | 340.96M | 98.89% | 99.18% | 38.39K | 0.66% |
| b08.v | rx-oop (OOP Engine) | 2.92 | 373.03M | 1.09B | 595.25M | 98.51% | 99.48% | 50.18K | 1.41% |
| b08.v | Icarus Verilog | 3.92 | 1.12B | 4.37B | 1.92B | 98.30% | 99.87% | 38.29K | 0.81% |
| b08.v | Verilator C++ | 1.88 | 78.54M | 147.81M | 76.24M | 99.98% | 80.72% | 1.82K | 1.26% |
| b09.v | rx-prop | 4.23 | 260.74M | 1.10B | 371.69M | 99.44% | 99.55% | 9.62K | 0.27% |
| b09.v | rx-sweep (Linear) | 4.52 | 279.99M | 1.26B | 340.98M | 98.13% | 99.63% | 21.53K | 0.29% |
| b09.v | rx-oop (OOP Engine) | 3.18 | 382.98M | 1.22B | 629.19M | 98.27% | 99.87% | 15.92K | 0.44% |
| b09.v | Icarus Verilog | 4.14 | 1.06B | 4.37B | 1.95B | 96.66% | 99.82% | 122.71K | 0.47% |
| b09.v | Verilator C++ | 2.93 | 52.40M | 153.42M | 87.29M | 99.98% | 92.04% | 1.43K | 0.46% |
| b10.v | rx-prop | 3.72 | 337.59M | 1.26B | 434.83M | 98.73% | 99.46% | 38.38K | 1.07% |
| b10.v | rx-sweep (Linear) | 3.37 | 371.75M | 1.25B | 378.29M | 97.76% | 99.54% | 45.55K | 1.11% |
| b10.v | rx-oop (OOP Engine) | 2.17 | 618.33M | 1.34B | 840.61M | 98.09% | 99.57% | 87.67K | 3.87% |
| b10.v | Icarus Verilog | 3.92 | 1.79B | 7.03B | 3.11B | 97.00% | 99.90% | 104.27K | 0.74% |
| b10.v | Verilator C++ | 2.05 | 83.78M | 171.58M | 80.48M | 99.99% | 66.53% | 3.33K | 1.19% |
| b03.v | rx-prop | 3.84 | 450.64M | 1.73B | 596.71M | 97.25% | 99.91% | 12.25K | 0.50% |
| b03.v | rx-sweep (Linear) | 3.50 | 512.46M | 1.79B | 516.63M | 91.38% | 99.89% | 61.31K | 0.72% |
| b03.v | rx-oop (OOP Engine) | 2.42 | 777.93M | 1.89B | 1.15B | 96.51% | 99.91% | 31.20K | 2.77% |
| b03.v | Icarus Verilog | 3.84 | 1.19B | 4.56B | 2.06B | 96.75% | 99.87% | 99.10K | 0.69% |
| b03.v | Verilator C++ | 2.66 | 84.09M | 223.57M | 106.66M | 99.97% | 88.82% | 854 | 0.94% |
| b13.v | rx-prop | 3.73 | 561.39M | 2.09B | 710.33M | 95.26% | 99.92% | 34.13K | 0.30% |
| b13.v | rx-sweep (Linear) | 3.96 | 615.50M | 2.44B | 674.83M | 87.12% | 99.97% | 34.91K | 0.38% |
| b13.v | rx-oop (OOP Engine) | 2.92 | 783.64M | 2.29B | 1.22B | 93.19% | 99.95% | 58.20K | 0.53% |
| b13.v | Icarus Verilog | 3.94 | 1.58B | 6.25B | 2.78B | 96.63% | 99.73% | 277.12K | 0.68% |
| b13.v | Verilator C++ | 1.49 | 200.34M | 298.80M | 165.85M | 100.00% | 76.16% | 1.98K | 0.72% |
| b07.v | rx-prop | 4.16 | 501.72M | 2.09B | 683.08M | 95.91% | 99.96% | 11.29K | 0.16% |
| b07.v | rx-sweep (Linear) | 4.10 | 596.96M | 2.45B | 638.53M | 84.74% | 99.96% | 36.73K | 0.28% |
| b07.v | rx-oop (OOP Engine) | 2.97 | 769.67M | 2.29B | 1.22B | 92.25% | 99.95% | 52.06K | 0.70% |
| b07.v | Icarus Verilog | 4.17 | 1.28B | 5.36B | 2.37B | 95.95% | 99.80% | 185.25K | 0.46% |
| b07.v | Verilator C++ | 2.45 | 130.04M | 318.46M | 165.28M | 100.00% | 85.36% | 1.15K | 0.20% |
| b11.v | rx-prop | 3.33 | 638.11M | 2.12B | 741.82M | 95.53% | 99.93% | 24.61K | 1.21% |
| b11.v | rx-sweep (Linear) | 3.21 | 699.30M | 2.25B | 633.76M | 84.57% | 99.90% | 101.47K | 0.92% |
| b11.v | rx-oop (OOP Engine) | 1.97 | 1.24B | 2.44B | 1.58B | 95.61% | 99.91% | 77.15K | 4.85% |
| b11.v | Icarus Verilog | 3.57 | 1.71B | 6.10B | 2.82B | 97.10% | 99.64% | 320.88K | 0.94% |
| b11.v | Verilator C++ | 1.80 | 165.76M | 298.12M | 169.44M | 99.99% | 79.86% | 2.10K | 1.17% |
| b04.v | rx-prop | 2.75 | 1.45B | 3.98B | 1.44B | 91.52% | 99.94% | 68.46K | 2.22% |
| b04.v | rx-sweep (Linear) | 2.66 | 1.61B | 4.29B | 1.34B | 85.93% | 99.95% | 101.89K | 2.00% |
| b04.v | rx-oop (OOP Engine) | 1.93 | 2.29B | 4.41B | 2.84B | 92.10% | 99.94% | 136.05K | 5.11% |
| b04.v | Icarus Verilog | 3.28 | 5.85B | 19.21B | 9.45B | 96.91% | 99.41% | 1.69M | 1.12% |
| b04.v | Verilator C++ | 1.79 | 293.62M | 524.96M | 259.54M | 100.00% | 40.19% | 2.94K | 1.59% |
| b05.v | rx-prop | 4.33 | 361.53M | 1.57B | 523.42M | 98.01% | 99.92% | 4.87K | 0.21% |
| b05.v | rx-sweep (Linear) | 3.81 | 578.91M | 2.20B | 543.54M | 80.87% | 99.98% | 15.93K | 0.34% |
| b05.v | rx-oop (OOP Engine) | 2.94 | 601.86M | 1.77B | 985.19M | 95.52% | 99.79% | 88.67K | 1.27% |
| b05.v | Icarus Verilog | 4.14 | 881.90M | 3.65B | 1.59B | 96.19% | 99.80% | 109.76K | 0.46% |
| b05.v | Verilator C++ | 1.83 | 191.36M | 350.95M | 179.50M | 99.99% | 80.94% | 2.58K | 0.32% |
| b12.v | rx-prop | 3.44 | 1.38B | 4.74B | 1.61B | 87.20% | 99.97% | 50.01K | 0.28% |
| b12.v | rx-sweep (Linear) | 3.88 | 1.62B | 6.29B | 1.62B | 78.19% | 99.98% | 62.57K | 0.33% |
| b12.v | rx-oop (OOP Engine) | 2.79 | 1.86B | 5.18B | 2.89B | 89.27% | 99.97% | 102.57K | 1.25% |
| b12.v | Icarus Verilog | 3.83 | 3.81B | 14.58B | 6.70B | 95.69% | 97.84% | 6.18M | 0.62% |
| b12.v | Verilator C++ | 1.93 | 513.87M | 993.91M | 518.72M | 100.00% | 89.23% | 3.08K | 0.31% |
| b14.v | rx-prop | 2.00 | 17.69B | 35.44B | 13.69B | 88.84% | 96.17% | 58.51M | 4.55% |
| b14.v | rx-sweep (Linear) | 2.15 | 11.26B | 24.20B | 7.81B | 83.97% | 95.34% | 58.35M | 3.14% |
| b14.v | rx-oop (OOP Engine) | 1.29 | 28.95B | 37.21B | 28.38B | 93.54% | 87.78% | 224.07M | 9.47% |
| b14.v | Icarus Verilog | 2.81 | 27.85B | 78.33B | 41.07B | 95.61% | 76.28% | 427.56M | 1.11% |
| b14.v | Verilator C++ | 2.06 | 1.79B | 3.70B | 2.05B | 99.99% | 96.57% | 2.29K | 0.99% |
| b15.v | rx-prop | 3.24 | 7.04B | 22.83B | 7.86B | 86.56% | 96.84% | 33.42M | 0.58% |
| b15.v | rx-sweep (Linear) | 3.22 | 9.21B | 29.64B | 7.82B | 77.71% | 92.97% | 122.77M | 0.77% |
| b15.v | rx-oop (OOP Engine) | 2.19 | 11.65B | 25.50B | 15.54B | 90.91% | 89.70% | 145.76M | 2.40% |
| b15.v | Icarus Verilog | 3.34 | 23.66B | 78.92B | 36.43B | 95.76% | 61.06% | 601.30M | 0.45% |
| b15.v | Verilator C++ | 2.40 | 2.86B | 6.87B | 3.38B | 100.00% | 84.15% | 23.25K | 0.18% |
| b21.v | rx-prop | 2.02 | 22.57B | 45.60B | 17.44B | 88.33% | 88.62% | 232.10M | 3.90% |
| b21.v | rx-sweep (Linear) | 2.48 | 15.84B | 39.28B | 11.28B | 80.28% | 90.02% | 221.95M | 1.93% |
| b21.v | rx-oop (OOP Engine) | 1.34 | 36.81B | 49.38B | 36.47B | 92.77% | 75.68% | 641.79M | 7.91% |
| b21.v | Icarus Verilog | 2.83 | 36.62B | 103.62B | 52.68B | 95.55% | 66.15% | 793.69M | 0.93% |
| b21.v | Verilator C++ | 2.25 | 4.17B | 9.38B | 4.88B | 99.99% | 0.00% | 18.60M | 0.51% |
| b20.v | rx-prop | 1.90 | 28.27B | 53.68B | 20.87B | 88.17% | 87.71% | 304.12M | 4.48% |
| b20.v | rx-sweep (Linear) | 2.29 | 19.11B | 43.70B | 13.22B | 81.18% | 89.72% | 255.84M | 2.38% |
| b20.v | rx-oop (OOP Engine) | 1.27 | 41.48B | 52.53B | 39.93B | 93.02% | 73.95% | 726.03M | 8.60% |
| b20.v | Icarus Verilog | 2.71 | 42.43B | 115.07B | 59.36B | 95.58% | 66.31% | 884.51M | 1.01% |
| b20.v | Verilator C++ | 2.27 | 4.39B | 9.94B | 5.08B | 100.00% | 0.00% | 2.42M | 0.53% |
| b22.v | rx-prop | 1.66 | 51.53B | 85.47B | 34.25B | 88.09% | 78.88% | 861.91M | 5.26% |
| b22.v | rx-sweep (Linear) | 1.99 | 34.12B | 67.81B | 21.72B | 82.82% | 86.66% | 497.94M | 3.14% |
| b22.v | rx-oop (OOP Engine) | 1.14 | 81.19B | 92.73B | 73.57B | 93.12% | 68.71% | 1.58B | 10.01% |
| b22.v | Icarus Verilog | 2.34 | 83.84B | 196.38B | 109.92B | 95.63% | 51.52% | 2.33B | 1.18% |
| b22.v | Verilator C++ | 1.80 | 8.55B | 15.41B | 7.73B | 99.84% | 0.00% | 291.69M | 0.73% |
| b17.v | rx-prop | 2.59 | 26.02B | 67.44B | 23.29B | 86.37% | 76.57% | 744.56M | 0.69% |
| b17.v | rx-sweep (Linear) | 3.07 | 28.89B | 88.57B | 23.39B | 78.12% | 91.85% | 417.15M | 0.82% |
| b17.v | rx-oop (OOP Engine) | 1.84 | 40.06B | 73.83B | 45.77B | 90.79% | 59.29% | 1.72B | 2.20% |
| b17.v | Icarus Verilog | 2.59 | 56.71B | 146.65B | 72.06B | 94.39% | 48.67% | 2.07B | 0.49% |
| b17.v | Verilator C++ | 1.23 | 21.15B | 26.01B | 12.04B | 99.80% | 0.00% | 1.70B | 1.94% |
| b18.v | rx-prop | 1.97 | 95.10B | 187.68B | 71.29B | 87.72% | 71.13% | 2.53B | 2.82% |
| b18.v | rx-sweep (Linear) | 2.84 | 75.74B | 215.35B | 57.86B | 78.63% | 90.16% | 1.22B | 1.16% |
| b18.v | rx-oop (OOP Engine) | 1.52 | 138.08B | 209.43B | 140.04B | 91.91% | 56.07% | 4.97B | 5.00% |
| b18.v | Icarus Verilog | 1.94 | 20.56B | 39.82B | 18.76B | 94.76% | 77.03% | 226.47M | 1.45% |
| b18.v | Verilator C++ | 0.68 | 111.60B | 75.40B | 38.74B | 99.40% | 0.00% | 5.95B | 15.26% |
| b19.v | rx-prop | 2.14 | 151.91B | 325.18B | 118.00B | 86.91% | 64.32% | 5.51B | 1.74% |
| b19.v | rx-sweep (Linear) | 3.06 | 136.00B | 416.37B | 107.92B | 77.62% | 88.74% | 2.72B | 0.77% |
| b19.v | rx-oop (OOP Engine) | 1.67 | 216.42B | 361.45B | 225.81B | 91.49% | 51.61% | 9.30B | 2.99% |
| b19.v | Icarus Verilog | 1.78 | 36.40B | 64.87B | 28.74B | 94.35% | 76.23% | 384.56M | 1.38% |
| b19.v | Verilator C++ | 0.68 | 254.27B | 171.87B | 84.85B | 98.89% | 0.00% | 13.60B | 18.92% |

---

# master_test/master_test_report_20260921_121522.md

# Master Test Unified Benchmark Report: tests/IWLS2005/opencores

**Execution Parameters:**
- **Target Suite / Path:** `tests/IWLS2005/opencores`
- **Circuits Benchmarked:** 21
- **Simulation Vectors (Phase 3):** 50,000 (Warmup: 10)
- **Verification Vectors (Phase 2):** 100
- **Hardware Profiler:** Linux `perf` kernel PMU counters

---

## 1. Zero-Testbench Memory Footprint (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | 184 | 0.55 MB (31.7 MB peak) | N/A | 0.58 MB (8.4 MB peak) | 0.69 MB (4.4 MB peak) |
| steppermotordrive.v | 258 | 1.02 MB (32.4 MB peak) | N/A | 1.09 MB (8.9 MB peak) | 0.75 MB (4.4 MB peak) |
| ss_pcm.v | 648 | 2.35 MB (33.7 MB peak) | N/A | 2.12 MB (9.9 MB peak) | 0.62 MB (4.3 MB peak) |
| usb_phy.v | 715 | 2.57 MB (33.8 MB peak) | N/A | 2.58 MB (10.5 MB peak) | 0.77 MB (4.4 MB peak) |
| sasc.v | 1,125 | 3.18 MB (34.6 MB peak) | N/A | 2.57 MB (10.4 MB peak) | 0.75 MB (4.4 MB peak) |
| simple_spi.v | 1,489 | 3.73 MB (35.1 MB peak) | N/A | 4.00 MB (11.8 MB peak) | 0.78 MB (4.5 MB peak) |
| pci_spoci_ctrl.v | 1,696 | 2.89 MB (34.3 MB peak) | N/A | 5.26 MB (13.0 MB peak) | 0.65 MB (4.3 MB peak) |
| i2c.v | 1,496 | 3.69 MB (35.0 MB peak) | N/A | 5.30 MB (13.2 MB peak) | 0.80 MB (4.4 MB peak) |
| systemcdes.v | 4,326 | 8.88 MB (40.2 MB peak) | N/A | 13.72 MB (21.5 MB peak) | 0.86 MB (4.6 MB peak) |
| spi.v | 4,531 | 9.06 MB (40.4 MB peak) | N/A | 14.99 MB (22.9 MB peak) | 0.79 MB (4.5 MB peak) |
| wb_dma.v | 5,720 | 15.81 MB (47.3 MB peak) | N/A | 16.15 MB (24.0 MB peak) | 0.93 MB (4.6 MB peak) |
| des_area.v | 6,445 | 8.20 MB (39.6 MB peak) | N/A | 18.89 MB (26.8 MB peak) | 1.12 MB (4.7 MB peak) |
| tv80.v | 10,607 | 17.49 MB (48.9 MB peak) | N/A | 31.07 MB (39.0 MB peak) | N/A |
| systemcaes.v | 14,071 | 24.96 MB (57.2 MB peak) | N/A | 40.84 MB (48.7 MB peak) | 1.14 MB (4.8 MB peak) |
| mem_ctrl.v | 16,796 | 32.59 MB (65.4 MB peak) | N/A | 54.10 MB (61.9 MB peak) | 1.11 MB (4.8 MB peak) |
| ac97_ctrl.v | 19,069 | 53.59 MB (86.1 MB peak) | N/A | 65.55 MB (73.4 MB peak) | 1.44 MB (5.1 MB peak) |
| usb_funct.v | 18,282 | 43.93 MB (76.8 MB peak) | N/A | 59.40 MB (67.2 MB peak) | 1.34 MB (4.9 MB peak) |
| aes_core.v | 25,565 | 29.88 MB (64.3 MB peak) | N/A | 78.80 MB (86.7 MB peak) | 1.18 MB (4.9 MB peak) |
| wb_conmax.v | 49,326 | 48.34 MB (84.2 MB peak) | N/A | 144.15 MB (152.0 MB peak) | 1.32 MB (5.0 MB peak) |
| des_perf.v | 111,781 | 207.06 MB (245.7 MB peak) | N/A | 440.62 MB (448.4 MB peak) | 2.84 MB (6.5 MB peak) |
| vga_lcd.v | 187,445 | 380.25 MB (421.0 MB peak) | N/A | 592.68 MB (600.5 MB peak) | 3.30 MB (7.0 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | 184 | 0.38 ms (0.014 ms opt) | N/A | 5.19 ms | 2.53 s |
| steppermotordrive.v | 258 | 0.69 ms (0.058 ms opt) | N/A | 7.07 ms | 2.58 s |
| ss_pcm.v | 648 | 1.67 ms (0.135 ms opt) | N/A | 11.24 ms | 2.62 s |
| usb_phy.v | 715 | 1.64 ms (0.179 ms opt) | N/A | 13.18 ms | 2.63 s |
| sasc.v | 1,125 | 2.32 ms (0.203 ms opt) | N/A | 12.83 ms | 2.75 s |
| simple_spi.v | 1,489 | 2.55 ms (0.264 ms opt) | N/A | 19.04 ms | 2.78 s |
| pci_spoci_ctrl.v | 1,696 | 2.01 ms (0.228 ms opt) | N/A | 24.44 ms | 2.69 s |
| i2c.v | 1,496 | 2.41 ms (0.269 ms opt) | N/A | 25.15 ms | 2.88 s |
| systemcdes.v | 4,326 | 5.40 ms (0.595 ms opt) | N/A | 64.08 ms | 3.50 s |
| spi.v | 4,531 | 5.75 ms (0.652 ms opt) | N/A | 68.53 ms | 3.82 s |
| wb_dma.v | 5,720 | 10.20 ms (1.008 ms opt) | N/A | 71.10 ms | 5.04 s |
| des_area.v | 6,445 | 6.34 ms (0.766 ms opt) | N/A | 90.40 ms | 4.29 s |
| tv80.v | 10,607 | 11.85 ms (1.401 ms opt) | N/A | 149.35 ms | N/A |
| systemcaes.v | 14,071 | 17.35 ms (2.213 ms opt) | N/A | 195.64 ms | 9.56 s |
| mem_ctrl.v | 16,796 | 24.94 ms (3.764 ms opt) | N/A | 269.61 ms | 15.48 s |
| ac97_ctrl.v | 19,069 | 40.05 ms (7.240 ms opt) | N/A | 309.54 ms | 12.25 s |
| usb_funct.v | 18,282 | 32.96 ms (6.717 ms opt) | N/A | 308.53 ms | 11.17 s |
| aes_core.v | 25,565 | 28.63 ms (4.944 ms opt) | N/A | 438.86 ms | 9.24 s |
| wb_conmax.v | 49,326 | 52.53 ms (13.621 ms opt) | N/A | 845.33 ms | 18.26 s |
| des_perf.v | 111,781 | 321.70 ms (61.218 ms opt) | N/A | 2.41 s | 73.94 s |
| vga_lcd.v | 187,445 | 646.26 ms (132.711 ms opt) | N/A | 3.28 s | 150.91 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | 23.60 ms | 31.47 ms | 35.19 ms | N/A | 885.29 ms | 1.60 ms |
| steppermotordrive.v | 55.81 ms | 67.05 ms | 83.81 ms | N/A | 97.71 ms | 15.52 ms |
| ss_pcm.v | 269.78 ms | 301.79 ms | 383.56 ms | N/A | 572.31 ms | 48.60 ms |
| usb_phy.v | 289.48 ms | 297.26 ms | 407.83 ms | N/A | 419.07 ms | 53.24 ms |
| sasc.v | 355.59 ms | 386.39 ms | 517.36 ms | N/A | 513.82 ms | 81.53 ms |
| simple_spi.v | 330.11 ms | 351.10 ms | 426.67 ms | N/A | 611.27 ms | 97.91 ms |
| pci_spoci_ctrl.v | 235.01 ms | 252.40 ms | 469.49 ms | N/A | 810.63 ms | 62.07 ms |
| i2c.v | 402.55 ms | 406.97 ms | 585.61 ms | N/A | 1164.74 ms | 119.48 ms |
| systemcdes.v | 3186.06 ms | 2418.32 ms | 6397.52 ms | N/A | 15.62 s | 246.37 ms |
| spi.v | 670.22 ms | 785.59 ms | 820.85 ms | N/A | 2367.71 ms | 221.74 ms |
| wb_dma.v | 1640.03 ms | 1807.13 ms | 2425.49 ms | N/A | 5816.23 ms | 390.03 ms |
| des_area.v | 3753.33 ms | 2724.03 ms | 6325.54 ms | N/A | 50.85 s | 295.31 ms |
| tv80.v | 968.42 ms | 1423.57 ms | 1381.00 ms | N/A | 1005.50 ms | 418.35 ms |
| systemcaes.v | 3191.75 ms | 3265.69 ms | 4758.03 ms | N/A | 20.55 s | 740.10 ms |
| mem_ctrl.v | 2876.84 ms | 3334.67 ms | 4491.13 ms | N/A | 7422.09 ms | 956.36 ms |
| ac97_ctrl.v | 5672.90 ms | 5586.92 ms | 7877.40 ms | N/A | 4904.02 ms | 1233.62 ms |
| usb_funct.v | 2103.48 ms | 3330.60 ms | 2961.57 ms | N/A | 8095.28 ms | 1285.62 ms |
| aes_core.v | 13.08 s | 14.19 s | 22.78 s | N/A | 28.39 s | 964.55 ms |
| wb_conmax.v | 5324.83 ms | 6932.38 ms | 7135.19 ms | N/A | 102.39 s | 1670.85 ms |
| des_perf.v | 144.60 s | 128.98 s | 268.43 s | N/A | 583.66 s | 31.67 s |
| vga_lcd.v | 56.98 s | 54.96 s | 79.34 s | N/A | 62.87 s | 51.90 s |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | 37.52x | 28.13x | 25.16x | N/A | 1.00x | 553.23x |
| steppermotordrive.v | 1.75x | 1.46x | 1.17x | N/A | 1.00x | 6.29x |
| ss_pcm.v | 2.12x | 1.90x | 1.49x | N/A | 1.00x | 11.77x |
| usb_phy.v | 1.45x | 1.41x | 1.03x | N/A | 1.00x | 7.87x |
| sasc.v | 1.44x | 1.33x | 0.99x | N/A | 1.00x | 6.30x |
| simple_spi.v | 1.85x | 1.74x | 1.43x | N/A | 1.00x | 6.24x |
| pci_spoci_ctrl.v | 3.45x | 3.21x | 1.73x | N/A | 1.00x | 13.06x |
| i2c.v | 2.89x | 2.86x | 1.99x | N/A | 1.00x | 9.75x |
| systemcdes.v | 4.90x | 6.46x | 2.44x | N/A | 1.00x | 63.39x |
| spi.v | 3.53x | 3.01x | 2.88x | N/A | 1.00x | 10.68x |
| wb_dma.v | 3.55x | 3.22x | 2.40x | N/A | 1.00x | 14.91x |
| des_area.v | 13.55x | 18.67x | 8.04x | N/A | 1.00x | 172.19x |
| tv80.v | 1.04x | 0.71x | 0.73x | N/A | 1.00x | 2.40x |
| systemcaes.v | 6.44x | 6.29x | 4.32x | N/A | 1.00x | 27.77x |
| mem_ctrl.v | 2.58x | 2.23x | 1.65x | N/A | 1.00x | 7.76x |
| ac97_ctrl.v | 0.86x | 0.88x | 0.62x | N/A | 1.00x | 3.98x |
| usb_funct.v | 3.85x | 2.43x | 2.73x | N/A | 1.00x | 6.30x |
| aes_core.v | 2.17x | 2.00x | 1.25x | N/A | 1.00x | 29.44x |
| wb_conmax.v | 19.23x | 14.77x | 14.35x | N/A | 1.00x | 61.28x |
| des_perf.v | 4.04x | 4.53x | 2.17x | N/A | 1.00x | 18.43x |
| vga_lcd.v | 1.10x | 1.14x | 0.79x | N/A | 1.00x | 1.21x |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `3.23x`
- **rx-sweep (Linear Compiled):** `2.98x`
- **rx-oop (OOP Graph):** `2.13x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `14.15x`

### Cross-Engine Comparisons

- **Reactor Sweep vs Propagate Ratio:** `0.92x` (propagate faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | IPC | Cycles | Instructions | L1 Loads | L1 Hit% | L2 Hit% | LLC Misses | Brn Miss% |
|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | rx-prop | 3.01 | 103.88M | 312.64M | 127.30M | 99.41% | 96.66% | 36.48K | 2.30% |
| pci_conf_cyc_addr_dec.v | rx-sweep (Linear) | 2.38 | 139.23M | 331.53M | 133.12M | 99.34% | 97.42% | 30.80K | 2.98% |
| pci_conf_cyc_addr_dec.v | rx-oop (OOP Engine) | 2.19 | 147.55M | 323.72M | 195.43M | 99.40% | 98.35% | 32.89K | 4.11% |
| pci_conf_cyc_addr_dec.v | Icarus Verilog | 3.90 | 3.68B | 14.36B | 5.52B | 99.44% | 99.89% | 33.40K | 0.52% |
| pci_conf_cyc_addr_dec.v | Verilator C++ | 0.00 | 0 | 1.50M | 9.08K | 0.00% | 81.73% | 5.00K | 0.08% |
| steppermotordrive.v | rx-prop | 4.21 | 225.10M | 948.10M | 320.85M | 99.56% | 99.88% | 1.79K | 0.33% |
| steppermotordrive.v | rx-sweep (Linear) | 4.17 | 279.89M | 1.17B | 331.58M | 98.83% | 98.18% | 74.09K | 0.45% |
| steppermotordrive.v | rx-oop (OOP Engine) | 3.14 | 334.96M | 1.05B | 551.65M | 99.11% | 99.81% | 10.07K | 0.76% |
| steppermotordrive.v | Icarus Verilog | 4.05 | 436.31M | 1.77B | 716.96M | 99.83% | 97.64% | 30.93K | 0.72% |
| steppermotordrive.v | Verilator C++ | 2.41 | 55.17M | 133.10M | 62.69M | 99.98% | 85.90% | 2.02K | 1.54% |
| ss_pcm.v | rx-prop | 3.21 | 1.11B | 3.57B | 1.23B | 89.10% | 99.96% | 58.94K | 0.75% |
| ss_pcm.v | rx-sweep (Linear) | 3.24 | 1.25B | 4.06B | 1.24B | 85.10% | 99.94% | 109.14K | 1.12% |
| ss_pcm.v | rx-oop (OOP Engine) | 2.50 | 1.56B | 3.90B | 2.21B | 91.11% | 99.96% | 75.60K | 1.76% |
| ss_pcm.v | Icarus Verilog | 3.71 | 2.45B | 9.10B | 4.11B | 98.02% | 99.89% | 111.90K | 0.86% |
| ss_pcm.v | Verilator C++ | 1.93 | 194.19M | 375.29M | 221.01M | 99.95% | 97.73% | 2.52K | 1.87% |
| usb_phy.v | rx-prop | 3.17 | 1.18B | 3.74B | 1.28B | 88.28% | 99.95% | 81.89K | 0.79% |
| usb_phy.v | rx-sweep (Linear) | 3.58 | 1.19B | 4.27B | 1.23B | 84.21% | 99.98% | 52.29K | 0.79% |
| usb_phy.v | rx-oop (OOP Engine) | 2.47 | 1.66B | 4.10B | 2.29B | 91.03% | 99.96% | 80.22K | 1.84% |
| usb_phy.v | Icarus Verilog | 3.50 | 1.84B | 6.43B | 2.88B | 98.07% | 99.75% | 138.52K | 1.06% |
| usb_phy.v | Verilator C++ | 2.00 | 206.35M | 412.71M | 224.83M | 99.99% | 85.89% | 2.34K | 1.90% |
| sasc.v | rx-prop | 3.23 | 1.43B | 4.62B | 1.58B | 87.73% | 99.96% | 67.00K | 0.70% |
| sasc.v | rx-sweep (Linear) | 3.38 | 1.57B | 5.32B | 1.56B | 83.16% | 99.97% | 85.66K | 0.94% |
| sasc.v | rx-oop (OOP Engine) | 2.59 | 2.10B | 5.43B | 3.05B | 90.94% | 99.96% | 105.01K | 1.82% |
| sasc.v | Icarus Verilog | 3.63 | 2.22B | 8.06B | 3.65B | 97.81% | 99.83% | 158.87K | 0.88% |
| sasc.v | Verilator C++ | 1.85 | 324.53M | 600.72M | 333.90M | 99.97% | 96.24% | 3.40K | 1.66% |
| simple_spi.v | rx-prop | 3.35 | 1.34B | 4.49B | 1.53B | 85.75% | 99.97% | 86.23K | 0.29% |
| simple_spi.v | rx-sweep (Linear) | 3.86 | 1.46B | 5.62B | 1.54B | 80.50% | 99.94% | 199.65K | 0.46% |
| simple_spi.v | rx-oop (OOP Engine) | 2.94 | 1.73B | 5.10B | 2.74B | 89.10% | 99.96% | 129.89K | 0.72% |
| simple_spi.v | Icarus Verilog | 3.81 | 2.62B | 9.98B | 4.39B | 97.22% | 99.59% | 471.39K | 0.74% |
| simple_spi.v | Verilator C++ | 1.90 | 391.80M | 745.98M | 377.74M | 99.99% | 95.05% | 2.14K | 0.84% |
| pci_spoci_ctrl.v | rx-prop | 3.66 | 974.54M | 3.57B | 1.26B | 93.93% | 99.87% | 96.85K | 0.58% |
| pci_spoci_ctrl.v | rx-sweep (Linear) | 3.63 | 1.06B | 3.86B | 1.07B | 83.77% | 99.93% | 116.00K | 0.60% |
| pci_spoci_ctrl.v | rx-oop (OOP Engine) | 2.05 | 1.91B | 3.92B | 2.54B | 92.41% | 99.95% | 90.65K | 3.88% |
| pci_spoci_ctrl.v | Icarus Verilog | 3.56 | 3.51B | 12.51B | 5.77B | 97.08% | 99.09% | 1.54M | 0.89% |
| pci_spoci_ctrl.v | Verilator C++ | 2.30 | 245.65M | 564.27M | 281.14M | 99.96% | 98.97% | 1.02K | 0.79% |
| i2c.v | rx-prop | 3.39 | 1.63B | 5.54B | 1.88B | 88.27% | 99.96% | 88.24K | 0.37% |
| i2c.v | rx-sweep (Linear) | 3.83 | 1.65B | 6.33B | 1.75B | 82.17% | 99.96% | 120.33K | 0.55% |
| i2c.v | rx-oop (OOP Engine) | 2.58 | 2.39B | 6.18B | 3.53B | 89.83% | 99.97% | 116.53K | 1.82% |
| i2c.v | Icarus Verilog | 3.72 | 4.92B | 18.29B | 8.44B | 95.89% | 97.10% | 10.13M | 0.61% |
| i2c.v | Verilator C++ | 1.63 | 461.73M | 753.43M | 419.96M | 99.99% | 95.65% | 2.44K | 1.14% |
| systemcdes.v | rx-prop | 2.24 | 13.06B | 29.22B | 11.17B | 89.87% | 99.47% | 6.08M | 3.92% |
| systemcdes.v | rx-sweep (Linear) | 2.01 | 9.88B | 19.83B | 7.26B | 88.08% | 99.26% | 6.44M | 4.19% |
| systemcdes.v | rx-oop (OOP Engine) | 1.34 | 26.05B | 35.02B | 26.44B | 93.75% | 98.08% | 31.86M | 9.34% |
| systemcdes.v | Icarus Verilog | 2.75 | 63.33B | 174.01B | 92.81B | 96.42% | 79.41% | 683.47M | 1.31% |
| systemcdes.v | Verilator C++ | 1.83 | 996.75M | 1.83B | 890.19M | 99.98% | 97.73% | 1.48K | 5.24% |
| spi.v | rx-prop | 3.29 | 2.78B | 9.13B | 3.11B | 86.50% | 99.78% | 897.93K | 0.38% |
| spi.v | rx-sweep (Linear) | 3.62 | 3.25B | 11.76B | 3.17B | 79.37% | 99.73% | 1.76M | 0.61% |
| spi.v | rx-oop (OOP Engine) | 2.93 | 3.36B | 9.86B | 5.39B | 89.17% | 99.70% | 1.77M | 0.91% |
| spi.v | Icarus Verilog | 3.88 | 10.01B | 38.80B | 17.48B | 96.03% | 81.05% | 131.38M | 0.45% |
| spi.v | Verilator C++ | 1.89 | 890.37M | 1.68B | 810.37M | 99.98% | 97.35% | 3.41K | 0.55% |
| wb_dma.v | rx-prop | 3.42 | 6.91B | 23.63B | 8.26B | 85.16% | 98.95% | 12.92M | 0.48% |
| wb_dma.v | rx-sweep (Linear) | 3.50 | 7.64B | 26.75B | 8.04B | 83.47% | 97.65% | 31.21M | 0.93% |
| wb_dma.v | rx-oop (OOP Engine) | 2.59 | 9.98B | 25.89B | 14.39B | 89.33% | 92.92% | 108.71M | 1.03% |
| wb_dma.v | Icarus Verilog | 4.05 | 24.48B | 99.01B | 43.45B | 98.48% | 78.36% | 143.09M | 0.44% |
| wb_dma.v | Verilator C++ | 1.97 | 1.59B | 3.12B | 1.62B | 99.99% | 96.30% | 28.88K | 1.52% |
| des_area.v | rx-prop | 1.96 | 15.53B | 30.49B | 12.38B | 90.82% | 99.55% | 5.09M | 5.16% |
| des_area.v | rx-sweep (Linear) | 1.80 | 11.36B | 20.39B | 7.81B | 89.42% | 99.46% | 4.48M | 5.06% |
| des_area.v | rx-oop (OOP Engine) | 1.34 | 25.89B | 34.60B | 26.21B | 93.99% | 95.86% | 65.22M | 9.27% |
| des_area.v | Icarus Verilog | 3.18 | 206.22B | 656.05B | 256.79B | 97.50% | 80.83% | 1.23B | 0.58% |
| des_area.v | Verilator C++ | 2.37 | 1.19B | 2.82B | 1.39B | 99.99% | 98.18% | 1.73K | 8.74% |
| tv80.v | rx-prop | 3.32 | 3.93B | 13.04B | 4.47B | 85.23% | 99.44% | 3.68M | 0.53% |
| tv80.v | rx-sweep (Linear) | 3.38 | 5.72B | 19.31B | 4.98B | 77.35% | 94.82% | 58.63M | 0.80% |
| tv80.v | rx-oop (OOP Engine) | 2.61 | 5.54B | 14.46B | 8.09B | 89.08% | 97.53% | 21.82M | 1.40% |
| tv80.v | Icarus Verilog | 3.20 | 4.91B | 15.73B | 7.13B | 96.21% | 88.65% | 30.77M | 0.92% |
| tv80.v | Verilator C++ | 2.18 | 1.67B | 3.63B | 1.89B | 100.00% | 0.00% | 21.13K | 0.49% |
| systemcaes.v | rx-prop | 2.73 | 13.14B | 35.85B | 12.91B | 87.94% | 88.48% | 179.21M | 1.04% |
| systemcaes.v | rx-sweep (Linear) | 3.04 | 13.54B | 41.15B | 12.15B | 82.64% | 90.78% | 194.60M | 1.18% |
| systemcaes.v | rx-oop (OOP Engine) | 2.01 | 19.56B | 39.40B | 23.83B | 91.11% | 73.15% | 569.79M | 2.33% |
| systemcaes.v | Icarus Verilog | 4.10 | 84.60B | 347.07B | 154.71B | 96.83% | 73.49% | 1.30B | 0.31% |
| systemcaes.v | Verilator C++ | 2.39 | 2.96B | 7.07B | 3.06B | 100.00% | 23.56% | 81.97K | 0.32% |
| mem_ctrl.v | rx-prop | 3.06 | 11.77B | 36.05B | 12.42B | 85.51% | 89.83% | 182.73M | 0.45% |
| mem_ctrl.v | rx-sweep (Linear) | 3.36 | 13.62B | 45.74B | 12.68B | 80.99% | 91.58% | 202.96M | 0.83% |
| mem_ctrl.v | rx-oop (OOP Engine) | 2.19 | 18.23B | 39.97B | 22.86B | 89.39% | 71.64% | 687.87M | 1.11% |
| mem_ctrl.v | Icarus Verilog | 3.61 | 31.60B | 114.11B | 51.10B | 97.34% | 54.37% | 619.15M | 0.40% |
| mem_ctrl.v | Verilator C++ | 2.12 | 3.87B | 8.20B | 4.16B | 100.00% | 30.82% | 114.25K | 1.27% |
| ac97_ctrl.v | rx-prop | 2.75 | 22.93B | 63.04B | 21.46B | 84.69% | 80.74% | 633.13M | 0.13% |
| ac97_ctrl.v | rx-sweep (Linear) | 3.53 | 22.62B | 79.94B | 21.76B | 81.11% | 87.18% | 526.93M | 0.51% |
| ac97_ctrl.v | rx-oop (OOP Engine) | 2.20 | 31.55B | 69.52B | 38.65B | 89.04% | 55.13% | 1.90B | 0.31% |
| ac97_ctrl.v | Icarus Verilog | 3.49 | 21.70B | 75.81B | 31.24B | 96.36% | 52.71% | 536.86M | 0.28% |
| ac97_ctrl.v | Verilator C++ | 2.25 | 4.94B | 11.12B | 5.30B | 99.99% | 0.00% | 1.59M | 0.64% |
| usb_funct.v | rx-prop | 2.68 | 8.60B | 23.03B | 8.02B | 86.16% | 80.02% | 221.55M | 0.40% |
| usb_funct.v | rx-sweep (Linear) | 2.96 | 13.53B | 40.11B | 10.15B | 75.16% | 89.97% | 252.74M | 0.88% |
| usb_funct.v | rx-oop (OOP Engine) | 2.09 | 12.04B | 25.12B | 14.20B | 89.19% | 63.30% | 563.29M | 0.93% |
| usb_funct.v | Icarus Verilog | 3.78 | 34.55B | 130.69B | 57.41B | 96.70% | 70.53% | 558.02M | 0.33% |
| usb_funct.v | Verilator C++ | 2.17 | 5.14B | 11.14B | 5.35B | 99.99% | 0.00% | 1.63M | 0.61% |
| aes_core.v | rx-prop | 1.63 | 52.91B | 85.99B | 36.23B | 88.22% | 80.29% | 841.67M | 5.23% |
| aes_core.v | rx-sweep (Linear) | 1.57 | 57.53B | 90.11B | 36.05B | 87.72% | 82.11% | 792.31M | 5.26% |
| aes_core.v | rx-oop (OOP Engine) | 1.06 | 92.26B | 98.07B | 83.21B | 93.66% | 69.99% | 1.58B | 10.36% |
| aes_core.v | Icarus Verilog | 2.67 | 116.97B | 312.57B | 167.07B | 97.41% | 47.39% | 2.28B | 1.13% |
| aes_core.v | Verilator C++ | 1.57 | 3.88B | 6.10B | 3.40B | 99.99% | 53.50% | 103.87K | 7.21% |
| wb_conmax.v | rx-prop | 2.42 | 22.92B | 55.45B | 20.91B | 87.69% | 70.75% | 753.24M | 0.75% |
| wb_conmax.v | rx-sweep (Linear) | 2.65 | 29.49B | 78.03B | 23.18B | 80.27% | 85.95% | 643.76M | 1.28% |
| wb_conmax.v | rx-oop (OOP Engine) | 1.91 | 30.47B | 58.33B | 34.68B | 90.75% | 56.50% | 1.40B | 1.44% |
| wb_conmax.v | Icarus Verilog | 3.90 | 418.02B | 1629.18B | 728.51B | 93.88% | 84.11% | 7.08B | 0.21% |
| wb_conmax.v | Verilator C++ | 2.25 | 6.68B | 15.04B | 6.98B | 99.93% | 0.00% | 97.98M | 0.39% |
| des_perf.v | rx-prop | 1.37 | 579.11B | 792.15B | 313.26B | 87.03% | 35.74% | 26.11B | 4.33% |
| des_perf.v | rx-sweep (Linear) | 1.50 | 516.71B | 774.35B | 313.75B | 88.92% | 63.93% | 12.56B | 4.95% |
| des_perf.v | rx-oop (OOP Engine) | 0.84 | 1079.99B | 904.88B | 746.84B | 93.23% | 23.91% | 38.42B | 8.54% |
| des_perf.v | Icarus Verilog | 1.15 | 58.07B | 67.04B | 37.79B | 95.96% | 36.03% | 977.17M | 1.49% |
| des_perf.v | Verilator C++ | 0.45 | 126.67B | 57.27B | 41.20B | 99.60% | 0.00% | 4.10B | 41.83% |
| vga_lcd.v | rx-prop | 2.34 | 228.04B | 534.16B | 179.34B | 84.52% | 57.07% | 11.92B | 0.06% |
| vga_lcd.v | rx-sweep (Linear) | 3.09 | 219.65B | 678.62B | 187.20B | 80.25% | 77.28% | 8.40B | 0.67% |
| vga_lcd.v | rx-oop (OOP Engine) | 1.86 | 317.65B | 591.83B | 334.31B | 89.38% | 50.16% | 17.69B | 0.21% |
| vga_lcd.v | Icarus Verilog | 2.13 | 20.47B | 43.50B | 17.58B | 94.70% | 78.32% | 201.91M | 1.05% |
| vga_lcd.v | Verilator C++ | 0.39 | 206.50B | 80.44B | 64.11B | 99.35% | 0.00% | 6.25B | 50.45% |

---

# master_test/master_test_report_20260921_121758.md

# Master Test Unified Benchmark Report: tests/IWLS2005/faraday

**Execution Parameters:**
- **Target Suite / Path:** `tests/IWLS2005/faraday`
- **Circuits Benchmarked:** 1
- **Simulation Vectors (Phase 3):** 50,000 (Warmup: 10)
- **Verification Vectors (Phase 2):** 100
- **Hardware Profiler:** Linux `perf` kernel PMU counters

---

## 1. Zero-Testbench Memory Footprint (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| DMA.v | 31,920 | 57.52 MB (88.8 MB peak) | N/A | 103.11 MB (111.0 MB peak) | 1.41 MB (5.1 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| DMA.v | 31,920 | 53.22 ms (12.467 ms opt) | N/A | 506.31 ms | 21.22 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| DMA.v | 7703.84 ms | 7446.90 ms | 10.15 s | N/A | 28.23 s | 3439.17 ms |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| DMA.v | 3.66x | 3.79x | 2.78x | N/A | 1.00x | 8.21x |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `3.66x`
- **rx-sweep (Linear Compiled):** `3.79x`
- **rx-oop (OOP Graph):** `2.78x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `8.21x`

### Cross-Engine Comparisons

- **Reactor Sweep vs Propagate Ratio:** `1.03x` (sweep faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | IPC | Cycles | Instructions | L1 Loads | L1 Hit% | L2 Hit% | LLC Misses | Brn Miss% |
|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| DMA.v | rx-prop | 2.54 | 32.09B | 81.53B | 29.08B | 86.98% | 73.16% | 1.02B | 0.49% |
| DMA.v | rx-sweep (Linear) | 3.35 | 31.10B | 104.11B | 29.58B | 81.77% | 88.46% | 622.08M | 0.67% |
| DMA.v | rx-oop (OOP Engine) | 2.09 | 42.11B | 87.85B | 51.08B | 90.13% | 52.83% | 2.38B | 0.97% |
| DMA.v | Icarus Verilog | 3.53 | 119.12B | 420.54B | 193.71B | 97.29% | 43.86% | 2.95B | 0.33% |
| DMA.v | Verilator C++ | 1.58 | 13.82B | 21.79B | 10.31B | 99.79% | 0.00% | 872.59M | 0.76% |

---

# perf/cache_perf_chaotic_20260921_121949.md

# Cache Fragmentation Profile (CHAOTIC)

Isolated purely via hardware `perf` boundaries tightly hugging the core `batch_toggle` simulation logic.

## 1. Core Performance (IPC & Branches)
| Size | OOP IPC | OOP Branch | Unopt IPC | Unopt Branch | Opt IPC | Opt Branch | Sweep IPC | Sweep Branch |
|---|---|---|---|---|---|---|---|---|
| 100 | 3.71 | 819.04M | 4.89 | 1.02B | 5.20 | 1.02B | 4.62 | 1.15B |
| 135 | 3.65 | 917.81M | 4.62 | 1.15B | 5.39 | 1.15B | 4.52 | 1.31B |
| 182 | 3.61 | 929.97M | 4.74 | 1.17B | 5.37 | 1.17B | 4.64 | 1.34B |
| 245 | 3.64 | 835.57M | 4.98 | 1.05B | 5.45 | 1.05B | 4.59 | 1.22B |
| 330 | 3.30 | 675.65M | 4.76 | 854.91M | 5.36 | 855.21M | 4.68 | 993.39M |
| 445 | 3.01 | 871.82M | 4.37 | 1.11B | 5.07 | 1.11B | 4.64 | 1.29B |
| 600 | 2.99 | 900.61M | 3.70 | 1.14B | 4.85 | 1.14B | 4.58 | 1.33B |
| 810 | 3.01 | 847.42M | 3.56 | 1.08B | 4.92 | 1.08B | 4.59 | 1.26B |
| 1,093 | 2.51 | 786.66M | 3.54 | 1.00B | 5.01 | 1.00B | 4.63 | 1.17B |
| 1,475 | 2.11 | 812.40M | 3.49 | 1.04B | 5.09 | 1.04B | 4.61 | 1.21B |
| 1,991 | 1.96 | 828.82M | 3.49 | 1.06B | 5.28 | 1.06B | 4.62 | 1.24B |
| 2,687 | 1.86 | 824.17M | 3.48 | 1.05B | 5.45 | 1.05B | 4.64 | 1.23B |
| 3,627 | 1.81 | 819.53M | 3.53 | 1.05B | 5.52 | 1.05B | 4.64 | 1.23B |
| 4,896 | 1.68 | 753.71M | 3.58 | 962.30M | 5.51 | 962.27M | 4.65 | 1.13B |
| 6,609 | 1.73 | 802.63M | 3.57 | 1.02B | 5.51 | 1.03B | 4.65 | 1.20B |
| 8,922 | 1.60 | 767.07M | 3.63 | 979.68M | 5.51 | 979.90M | 4.65 | 1.15B |
| 12,044 | 1.60 | 703.10M | 3.50 | 898.21M | 5.51 | 898.07M | 4.64 | 1.05B |
| 16,259 | 1.35 | 654.69M | 2.69 | 835.97M | 5.48 | 835.33M | 4.60 | 981.05M |
| 21,949 | 1.29 | 687.84M | 2.11 | 878.88M | 5.19 | 878.55M | 4.05 | 1.03B |
| 29,631 | 1.19 | 637.82M | 1.65 | 814.78M | 3.60 | 814.42M | 3.40 | 956.10M |
| 40,001 | 1.18 | 637.40M | 1.21 | 814.50M | 3.05 | 814.25M | 2.87 | 955.86M |
| 54,001 | 1.15 | 597.92M | 1.26 | 763.99M | 2.85 | 763.78M | 2.59 | 896.64M |
| 72,901 | 1.15 | 452.86M | 1.16 | 578.69M | 2.75 | 578.34M | 2.46 | 678.99M |
| 98,416 | 1.07 | 301.25M | 1.07 | 384.89M | 2.70 | 384.94M | 2.39 | 451.83M |
| 132,861 | 1.13 | 165.07M | 1.13 | 210.89M | 2.69 | 210.79M | 2.39 | 247.47M |
| 179,362 | 1.12 | 155.00M | 1.12 | 198.07M | 2.67 | 197.92M | 2.41 | 232.31M |
| 242,138 | 0.82 | 143.72M | 1.11 | 183.75M | 2.64 | 183.79M | 2.38 | 215.72M |
| 326,886 | 0.70 | 176.54M | 1.07 | 225.52M | 2.66 | 225.60M | 2.37 | 264.90M |
| 441,296 | 0.50 | 238.36M | 1.04 | 304.50M | 2.65 | 304.36M | 2.37 | 357.08M |
| 595,749 | 0.32 | 321.76M | 1.01 | 411.20M | 2.65 | 411.10M | 2.37 | 482.24M |
| 804,261 | 0.24 | 434.32M | 0.48 | 555.00M | 2.67 | 555.23M | 2.36 | 651.33M |

## 2. L1 Cache Performance
| Size | OOP L1 Load | OOP L1 Hit% | Unopt L1 Load | Unopt L1 Hit% | Opt L1 Load | Opt L1 Hit% | Sweep L1 Load | Sweep L1 Hit% |
|---|---|---|---|---|---|---|---|---|
| 100 | 3.98B | 99.90% | 2.39B | 100.00% | 2.39B | 100.00% | 1.55B | 99.84% |
| 135 | 4.56B | 99.93% | 2.66B | 99.97% | 2.66B | 100.00% | 1.77B | 99.98% |
| 182 | 4.65B | 99.58% | 2.71B | 99.96% | 2.69B | 99.99% | 1.76B | 99.98% |
| 245 | 4.18B | 99.45% | 2.42B | 99.99% | 2.41B | 100.00% | 1.60B | 99.98% |
| 330 | 3.41B | 97.36% | 1.96B | 99.10% | 1.95B | 99.58% | 1.27B | 99.98% |
| 445 | 4.41B | 95.09% | 2.54B | 97.59% | 2.52B | 97.24% | 1.65B | 97.65% |
| 600 | 4.58B | 94.75% | 2.61B | 93.67% | 2.61B | 93.57% | 1.71B | 91.20% |
| 810 | 4.32B | 94.99% | 2.46B | 92.67% | 2.46B | 93.35% | 1.61B | 90.12% |
| 1,093 | 4.74B | 95.76% | 2.28B | 92.38% | 2.28B | 93.63% | 1.49B | 90.10% |
| 1,475 | 5.96B | 96.96% | 2.35B | 91.97% | 2.35B | 93.81% | 1.54B | 90.56% |
| 1,991 | 6.59B | 97.29% | 2.40B | 91.80% | 2.39B | 94.62% | 1.57B | 91.84% |
| 2,687 | 6.84B | 97.32% | 2.38B | 91.72% | 2.38B | 95.37% | 1.56B | 92.99% |
| 3,627 | 6.96B | 97.31% | 2.37B | 91.85% | 2.37B | 95.59% | 1.55B | 93.31% |
| 4,896 | 6.48B | 97.39% | 2.18B | 92.07% | 2.18B | 95.62% | 1.42B | 93.34% |
| 6,609 | 7.00B | 97.28% | 2.32B | 92.27% | 2.32B | 95.64% | 1.52B | 93.34% |
| 8,922 | 6.85B | 97.38% | 2.22B | 92.33% | 2.22B | 95.64% | 1.45B | 93.35% |
| 12,044 | 6.31B | 97.30% | 2.03B | 92.44% | 2.03B | 95.65% | 1.33B | 93.38% |
| 16,259 | 6.07B | 97.69% | 1.90B | 92.51% | 1.89B | 95.67% | 1.26B | 93.48% |
| 21,949 | 6.63B | 97.50% | 2.01B | 92.63% | 2.00B | 95.68% | 1.40B | 93.82% |
| 29,631 | 6.17B | 97.55% | 2.35B | 94.19% | 2.16B | 96.29% | 1.39B | 94.27% |
| 40,001 | 6.15B | 97.63% | 2.56B | 94.69% | 2.30B | 96.52% | 1.48B | 94.62% |
| 54,001 | 5.84B | 97.70% | 2.55B | 95.02% | 2.21B | 96.61% | 1.44B | 94.79% |
| 72,901 | 4.38B | 97.52% | 1.97B | 95.15% | 1.70B | 96.67% | 1.11B | 94.91% |
| 98,416 | 2.95B | 97.70% | 1.33B | 95.22% | 1.14B | 96.69% | 743.36M | 94.93% |
| 132,861 | 1.61B | 97.67% | 730.05M | 95.23% | 626.30M | 96.70% | 407.46M | 94.93% |
| 179,362 | 1.51B | 97.63% | 686.96M | 95.25% | 589.44M | 96.70% | 381.23M | 94.91% |
| 242,138 | 1.43B | 97.73% | 638.42M | 95.26% | 549.27M | 96.72% | 356.29M | 94.94% |
| 326,886 | 1.77B | 97.67% | 785.20M | 95.28% | 671.69M | 96.71% | 439.72M | 94.96% |
| 441,296 | 2.44B | 97.72% | 1.06B | 95.30% | 909.22M | 96.71% | 593.66M | 94.96% |
| 595,749 | 3.46B | 97.86% | 1.43B | 95.29% | 1.23B | 96.71% | 807.42M | 94.98% |
| 804,261 | 4.82B | 97.98% | 1.93B | 95.27% | 1.65B | 96.71% | 1.08B | 94.96% |

## 3. L2, L3 & RAM Performance
| Size | OOP L2 Load | OOP L2 Hit% | OOP L3 Load | OOP L3 Hit% | OOP RAM (L3 Miss) | Unopt L2 Load | Unopt L2 Hit% | Unopt L3 Load | Unopt L3 Hit% | Unopt RAM (L3 Miss) | Opt L2 Load | Opt L2 Hit% | Opt L3 Load | Opt L3 Hit% | Opt RAM (L3 Miss) | Sweep L2 Load | Sweep L2 Hit% | Sweep L3 Load | Sweep L3 Hit% | Sweep RAM (L3 Miss) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 | 3.78M | 99.61% | 14.74K | 17.57% | 12.15K | 54.66K | 94.59% | 2.96K | -35.06% | 3.99K | 20.31K | 47.06% | 10.75K | -0.55% | 10.81K | 2.53M | 97.69% | 58.45K | 15.11% | 49.62K |
| 135 | 3.11M | 99.15% | 26.39K | -21.36% | 32.03K | 850.10K | 96.94% | 26.03K | -28.32% | 33.40K | 60.99K | 37.72% | 37.98K | 1.57% | 37.39K | 433.79K | 88.73% | 48.89K | -22.40% | 59.84K |
| 182 | 19.65M | 99.94% | 11.99K | -0.31% | 12.03K | 1.13M | 99.53% | 5.34K | -87.66% | 10.02K | 210.53K | 93.09% | 14.56K | -5.91% | 15.42K | 428.45K | 90.32% | 41.48K | -6.94% | 44.35K |
| 245 | 22.90M | 99.93% | 15.78K | 36.58% | 10.01K | 254.34K | 95.91% | 10.41K | 0.40% | 10.37K | 99.92K | 85.32% | 14.67K | -1.58% | 14.90K | 281.27K | 87.49% | 35.19K | -17.42% | 41.32K |
| 330 | 89.95M | 99.96% | 36.99K | 60.12% | 14.75K | 17.55M | 99.93% | 12.87K | 0.70% | 12.78K | 8.17M | 99.80% | 16.39K | 16.95% | 13.61K | 305.91K | 90.40% | 29.37K | -0.11% | 29.40K |
| 445 | 216.33M | 100.00% | 8.16K | 20.76% | 6.47K | 61.16M | 100.00% | 2.58K | -104.11% | 5.27K | 69.56M | 99.99% | 6.95K | -96.62% | 13.66K | 38.70M | 99.96% | 15.06K | -106.45% | 31.09K |
| 600 | 240.63M | 99.99% | 20.04K | 30.09% | 14.01K | 164.98M | 99.99% | 16.13K | 5.39% | 15.26K | 168.21M | 99.99% | 15.03K | -26.56% | 19.03K | 150.87M | 99.98% | 25.55K | -3.45% | 26.43K |
| 810 | 216.44M | 99.99% | 17.69K | 40.54% | 10.52K | 179.99M | 99.99% | 11.12K | 12.14% | 9.77K | 163.43M | 99.99% | 13.38K | 28.91% | 9.51K | 158.61M | 99.98% | 30.70K | 9.32% | 27.84K |
| 1,093 | 201.11M | 99.98% | 36.34K | -25.00% | 45.43K | 173.71M | 99.99% | 19.66K | -22.88% | 24.15K | 145.08M | 99.99% | 9.67K | 50.06% | 4.83K | 147.03M | 99.99% | 16.15K | -1.50% | 16.39K |
| 1,475 | 181.23M | 99.98% | 27.72K | -0.23% | 27.78K | 188.76M | 99.99% | 22.22K | -5.38% | 23.41K | 145.35M | 99.99% | 15.34K | 4.20% | 14.70K | 145.31M | 99.99% | 20.17K | -20.14% | 24.23K |
| 1,991 | 178.82M | 99.97% | 47.25K | -0.57% | 47.52K | 196.63M | 99.99% | 24.45K | 9.79% | 22.06K | 128.82M | 99.99% | 7.75K | -6.09% | 8.22K | 128.03M | 99.99% | 11.78K | -5.77% | 12.45K |
| 2,687 | 183.10M | 99.98% | 27.79K | -0.53% | 27.94K | 197.33M | 99.99% | 27.45K | 20.58% | 21.80K | 110.33M | 99.99% | 7.08K | -51.05% | 10.69K | 109.23M | 99.99% | 10.53K | -29.27% | 13.62K |
| 3,627 | 187.27M | 99.99% | 19.03K | -77.83% | 33.84K | 193.12M | 99.99% | 16.73K | -8.98% | 18.23K | 104.49M | 99.99% | 15.37K | 56.10% | 6.75K | 103.80M | 99.98% | 18.37K | -9.04% | 20.03K |
| 4,896 | 169.07M | 99.95% | 84.72K | -18.04% | 100.00K | 172.69M | 99.81% | 326.57K | -0.07% | 326.79K | 95.52M | 99.98% | 21.62K | 3.75% | 20.81K | 94.93M | 99.99% | 12.71K | 13.24% | 11.03K |
| 6,609 | 190.66M | 99.42% | 1.10M | -1.12% | 1.11M | 179.34M | 99.86% | 257.98K | -6.08% | 273.66K | 101.22M | 99.95% | 52.83K | 24.65% | 39.80K | 101.04M | 99.97% | 33.19K | 0.61% | 32.99K |
| 8,922 | 179.32M | 92.14% | 14.09M | -0.42% | 14.15M | 170.22M | 99.14% | 1.47M | 0.42% | 1.46M | 96.65M | 99.95% | 48.45K | 19.46% | 39.02K | 96.46M | 99.80% | 193.93K | 1.28% | 191.44K |
| 12,044 | 170.12M | 92.41% | 12.91M | -0.30% | 12.95M | 153.88M | 95.26% | 7.29M | 0.15% | 7.28M | 88.38M | 99.05% | 838.86K | -1.33% | 849.99K | 88.24M | 98.98% | 895.69K | -2.72% | 920.03K |
| 16,259 | 140.23M | 75.91% | 33.78M | 0.03% | 33.77M | 141.88M | 90.83% | 13.02M | -0.20% | 13.04M | 82.05M | 97.20% | 2.30M | 0.10% | 2.29M | 82.01M | 98.11% | 1.55M | 0.18% | 1.55M |
| 21,949 | 165.79M | 56.74% | 71.71M | -0.01% | 71.72M | 148.37M | 79.25% | 30.78M | 0.02% | 30.78M | 86.54M | 97.21% | 2.41M | 0.66% | 2.40M | 86.30M | 97.42% | 2.22M | -0.11% | 2.23M |
| 29,631 | 150.90M | 46.14% | 81.28M | -0.00% | 81.28M | 136.49M | 67.71% | 44.08M | -0.01% | 44.08M | 79.98M | 97.56% | 1.95M | 0.12% | 1.95M | 79.88M | 97.69% | 1.84M | 0.05% | 1.84M |
| 40,001 | 145.91M | 41.59% | 85.22M | -0.02% | 85.24M | 135.81M | 48.46% | 70.00M | -0.01% | 70.01M | 79.95M | 98.23% | 1.42M | 0.17% | 1.42M | 79.92M | 98.38% | 1.29M | 0.64% | 1.28M |
| 54,001 | 134.40M | 36.54% | 85.29M | -0.03% | 85.31M | 127.04M | 46.47% | 68.01M | -0.09% | 68.07M | 74.95M | 98.69% | 982.64K | -0.01% | 982.70K | 74.93M | 98.85% | 858.10K | -0.19% | 859.70K |
| 72,901 | 108.56M | 33.46% | 72.24M | -0.00% | 72.24M | 95.68M | 37.40% | 59.89M | 0.02% | 59.88M | 56.73M | 99.28% | 406.58K | 0.28% | 405.42K | 56.67M | 99.34% | 375.33K | -1.36% | 380.42K |
| 98,416 | 67.82M | 34.08% | 44.70M | -0.01% | 44.71M | 63.42M | 34.99% | 41.23M | -0.01% | 41.23M | 37.76M | 99.37% | 239.22K | -1.66% | 243.19K | 37.72M | 99.42% | 220.50K | -2.12% | 225.17K |
| 132,861 | 37.47M | 29.97% | 26.24M | 0.01% | 26.24M | 34.84M | 33.63% | 23.12M | 0.02% | 23.12M | 20.68M | 99.50% | 102.96K | -0.78% | 103.77K | 20.68M | 99.44% | 116.11K | 1.40% | 114.48K |
| 179,362 | 35.73M | 28.64% | 25.49M | -0.03% | 25.50M | 32.63M | 31.45% | 22.37M | -0.03% | 22.37M | 19.44M | 99.58% | 81.55K | -9.80% | 89.54K | 19.41M | 99.51% | 94.20K | -1.03% | 95.16K |
| 242,138 | 32.42M | 27.64% | 23.46M | 0.15% | 23.42M | 30.25M | 30.38% | 21.06M | 0.01% | 21.06M | 18.04M | 99.51% | 88.54K | 6.68% | 82.62K | 18.03M | 99.47% | 96.27K | 8.11% | 88.46K |
| 326,886 | 41.14M | 26.90% | 30.07M | 0.06% | 30.05M | 37.09M | 29.76% | 26.05M | 0.05% | 26.04M | 22.10M | 99.68% | 71.02K | -9.04% | 77.45K | 22.14M | 99.54% | 102.12K | -0.63% | 102.76K |
| 441,296 | 55.62M | 26.34% | 40.97M | -0.08% | 41.00M | 49.96M | 29.19% | 35.38M | 0.02% | 35.37M | 29.92M | 99.51% | 145.34K | -3.09% | 149.83K | 29.92M | 99.39% | 181.99K | 4.84% | 173.18K |
| 595,749 | 73.80M | 25.95% | 54.65M | -0.00% | 54.65M | 67.52M | 28.56% | 48.23M | 0.02% | 48.22M | 40.35M | 99.46% | 219.61K | 0.18% | 219.22K | 40.51M | 99.13% | 351.29K | -3.03% | 361.94K |
| 804,261 | 97.07M | 26.04% | 71.79M | -0.00% | 71.80M | 91.07M | 28.37% | 65.23M | -0.00% | 65.23M | 54.38M | 99.64% | 197.36K | 0.11% | 197.13K | 54.30M | 99.78% | 120.72K | -1.30% | 122.28K |

## 4. Execution Time & Throughput (per Iteration)
| Size | OOP Eval | OOP Time (ms) | OOP MEval/s | Unopt Eval | Unopt Time (ms) | Unopt MEval/s | Opt Eval | Opt Time (ms) | Opt MEval/s | Sweep Eval | Sweep Time (ms) | Sweep MEval/s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 | 198 | 0.0009 | 209.70 | 198 | 0.0006 | 341.39 | 198 | 0.0006 | 356.46 | 198 | 0.0005 | 393.51 |
| 135 | 268 | 0.0013 | 213.79 | 268 | 0.0008 | 322.94 | 268 | 0.0007 | 376.81 | 268 | 0.0007 | 388.16 |
| 182 | 362 | 0.0017 | 210.68 | 362 | 0.0011 | 336.14 | 362 | 0.0010 | 379.32 | 362 | 0.0009 | 404.33 |
| 245 | 488 | 0.0023 | 214.98 | 488 | 0.0014 | 359.13 | 488 | 0.0012 | 390.73 | 488 | 0.0012 | 405.31 |
| 330 | 658 | 0.0033 | 196.94 | 658 | 0.0019 | 345.63 | 658 | 0.0017 | 390.96 | 658 | 0.0016 | 414.96 |
| 445 | 888 | 0.0049 | 180.45 | 888 | 0.0028 | 319.31 | 888 | 0.0024 | 371.96 | 888 | 0.0021 | 413.97 |
| 600 | 1,198 | 0.0067 | 180.00 | 1,198 | 0.0044 | 271.30 | 1,198 | 0.0034 | 355.35 | 1,198 | 0.0029 | 408.95 |
| 810 | 1,618 | 0.0089 | 181.35 | 1,618 | 0.0062 | 262.11 | 1,618 | 0.0045 | 361.88 | 1,618 | 0.0039 | 412.83 |
| 1,093 | 2,184 | 0.0143 | 152.25 | 2,184 | 0.0084 | 261.17 | 2,184 | 0.0059 | 370.22 | 2,184 | 0.0053 | 415.60 |
| 1,475 | 2,948 | 0.0230 | 128.00 | 2,948 | 0.0114 | 258.03 | 2,948 | 0.0078 | 377.29 | 2,948 | 0.0071 | 415.69 |
| 1,991 | 3,980 | 0.0336 | 118.57 | 3,980 | 0.0154 | 258.60 | 3,980 | 0.0102 | 391.19 | 3,980 | 0.0096 | 416.26 |
| 2,687 | 5,372 | 0.0475 | 113.15 | 5,372 | 0.0208 | 258.34 | 5,372 | 0.0133 | 404.14 | 5,372 | 0.0128 | 418.68 |
| 3,627 | 7,252 | 0.0658 | 110.24 | 7,252 | 0.0276 | 262.30 | 7,252 | 0.0177 | 410.31 | 7,252 | 0.0173 | 418.65 |
| 4,896 | 9,790 | 0.0958 | 102.18 | 9,790 | 0.0368 | 265.95 | 9,790 | 0.0239 | 409.59 | 9,790 | 0.0233 | 419.41 |
| 6,609 | 13,216 | 0.1253 | 105.49 | 13,216 | 0.0497 | 265.97 | 13,216 | 0.0322 | 410.05 | 13,216 | 0.0315 | 420.12 |
| 8,922 | 17,842 | 0.1836 | 97.16 | 17,842 | 0.0659 | 270.66 | 17,842 | 0.0435 | 410.07 | 17,842 | 0.0425 | 420.15 |
| 12,044 | 24,086 | 0.2479 | 97.15 | 24,086 | 0.0924 | 260.64 | 24,086 | 0.0588 | 409.74 | 24,086 | 0.0574 | 419.53 |
| 16,259 | 32,516 | 0.3973 | 81.84 | 32,516 | 0.1616 | 201.17 | 32,516 | 0.0796 | 408.24 | 32,516 | 0.0780 | 416.83 |
| 21,949 | 43,896 | 0.5609 | 78.26 | 43,896 | 0.2763 | 158.85 | 43,896 | 0.1121 | 391.56 | 43,896 | 0.1173 | 374.37 |
| 29,631 | 59,260 | 0.8192 | 72.34 | 59,260 | 0.4689 | 126.37 | 59,260 | 0.2111 | 280.70 | 59,260 | 0.1898 | 312.28 |
| 40,001 | 80,000 | 1.1099 | 72.08 | 80,000 | 0.8575 | 93.29 | 80,000 | 0.3476 | 230.17 | 80,000 | 0.3028 | 264.24 |
| 54,001 | 108,000 | 1.5380 | 70.22 | 108,000 | 1.1331 | 95.32 | 108,000 | 0.5049 | 213.90 | 108,000 | 0.4607 | 234.43 |
| 72,901 | 145,800 | 2.0787 | 70.14 | 145,800 | 1.6894 | 86.30 | 145,800 | 0.7113 | 204.97 | 145,800 | 0.6534 | 223.14 |
| 98,416 | 196,830 | 3.0218 | 65.14 | 196,830 | 2.4802 | 79.36 | 196,830 | 0.9774 | 201.38 | 196,830 | 0.9079 | 216.79 |
| 132,861 | 265,720 | 3.8629 | 68.79 | 265,720 | 3.1582 | 84.14 | 265,720 | 1.3268 | 200.27 | 265,720 | 1.2249 | 216.93 |
| 179,362 | 358,722 | 5.2927 | 67.78 | 358,722 | 4.3153 | 83.13 | 358,722 | 1.8025 | 199.02 | 358,722 | 1.6502 | 217.38 |
| 242,138 | 484,274 | 8.1648 | 59.31 | 484,274 | 5.8404 | 82.92 | 484,274 | 2.4614 | 196.75 | 484,274 | 2.2128 | 218.85 |
| 326,886 | 653,770 | 13.1560 | 49.69 | 653,770 | 8.2226 | 79.51 | 653,770 | 3.3030 | 197.93 | 653,770 | 3.0507 | 214.30 |
| 441,296 | 882,590 | 27.5511 | 32.03 | 882,590 | 11.3303 | 77.90 | 882,590 | 4.4736 | 197.29 | 882,590 | 4.1007 | 215.23 |
| 595,749 | 1,191,496 | 60.3796 | 19.73 | 1,191,496 | 15.5440 | 76.65 | 1,191,496 | 6.0213 | 197.88 | 1,191,496 | 5.5636 | 214.16 |
| 804,261 | 1,608,520 | 107.9959 | 14.89 | 1,608,520 | 44.9910 | 35.75 | 1,608,520 | 8.0971 | 198.65 | 1,608,520 | 7.5556 | 212.89 |

---
