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
| ctrl.v | 340 | 0.75 MB (28.4 MB peak) | 0.50 MB (33.5 MB peak) | 0.17 MB (8.1 MB peak) | 0.73 MB (4.4 MB peak) |
| int2float.v | 461 | 0.87 MB (28.3 MB peak) | 0.64 MB (33.6 MB peak) | 0.21 MB (8.1 MB peak) | 0.71 MB (4.4 MB peak) |
| dec.v | 576 | 0.98 MB (28.6 MB peak) | 0.78 MB (33.8 MB peak) | 0.21 MB (8.1 MB peak) | 0.61 MB (4.3 MB peak) |
| router.v | 576 | 0.92 MB (30.5 MB peak) | 0.73 MB (33.8 MB peak) | 0.23 MB (8.1 MB peak) | 0.68 MB (4.4 MB peak) |
| cavlc.v | 1,300 | 1.66 MB (31.2 MB peak) | 1.71 MB (34.8 MB peak) | 0.65 MB (8.5 MB peak) | 0.71 MB (4.4 MB peak) |
| priority.v | 2,043 | 2.24 MB (29.8 MB peak) | 2.49 MB (35.6 MB peak) | 0.96 MB (8.8 MB peak) | 0.77 MB (4.4 MB peak) |
| adder.v | 2,547 | 2.60 MB (30.1 MB peak) | 3.00 MB (36.0 MB peak) | 1.19 MB (9.0 MB peak) | 0.78 MB (4.4 MB peak) |
| i2c.v | 2,480 | 2.63 MB (30.2 MB peak) | 2.99 MB (36.0 MB peak) | 1.15 MB (9.0 MB peak) | 0.77 MB (4.4 MB peak) |
| bar.v | 5,526 | 5.69 MB (33.3 MB peak) | 6.88 MB (39.9 MB peak) | 3.16 MB (11.0 MB peak) | 0.90 MB (4.5 MB peak) |
| max.v | 6,025 | 5.97 MB (33.5 MB peak) | 7.27 MB (40.2 MB peak) | 3.47 MB (11.3 MB peak) | 0.85 MB (4.5 MB peak) |
| arbiter.v | 23,618 | 23.43 MB (51.0 MB peak) | 29.20 MB (62.2 MB peak) | 15.23 MB (23.1 MB peak) | 0.89 MB (4.6 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| ctrl.v | 340 | 0.87 ms (0.032 ms opt) | 2.61 ms | 3.59 ms | 2.50 s |
| int2float.v | 461 | 1.09 ms (0.041 ms opt) | 10.86 ms | 3.64 ms | 2.50 s |
| dec.v | 576 | 1.11 ms (0.034 ms opt) | 3.05 ms | 3.82 ms | 2.51 s |
| router.v | 576 | 1.23 ms (0.043 ms opt) | 11.22 ms | 4.44 ms | 2.52 s |
| cavlc.v | 1,300 | 2.62 ms (0.116 ms opt) | 13.08 ms | 7.21 ms | 2.54 s |
| priority.v | 2,043 | 3.75 ms (0.130 ms opt) | 6.67 ms | 9.67 ms | 2.57 s |
| adder.v | 2,547 | 4.40 ms (0.128 ms opt) | 14.92 ms | 10.91 ms | 2.63 s |
| i2c.v | 2,480 | 4.49 ms (0.187 ms opt) | 15.18 ms | 13.36 ms | 2.62 s |
| bar.v | 5,526 | 10.60 ms (0.358 ms opt) | 16.62 ms | 25.93 ms | 3.22 s |
| max.v | 6,025 | 10.99 ms (0.364 ms opt) | 17.43 ms | 28.10 ms | 2.89 s |
| arbiter.v | 23,618 | 55.19 ms (3.184 ms opt) | 75.53 ms | 133.77 ms | 8.45 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| ctrl.v | 47.77 ms | 49.52 ms | N/A | N/A | 413.04 ms | 3.21 ms |
| int2float.v | 48.48 ms | 88.75 ms | N/A | N/A | 498.14 ms | 4.62 ms |
| dec.v | 16.86 ms | 25.50 ms | N/A | N/A | 171.30 ms | 3.73 ms |
| router.v | 66.41 ms | 66.97 ms | N/A | N/A | 732.35 ms | 7.03 ms |
| cavlc.v | 154.44 ms | 250.48 ms | N/A | N/A | 1411.60 ms | 8.36 ms |
| priority.v | 250.55 ms | 245.55 ms | N/A | N/A | 13.42 s | 44.54 ms |
| adder.v | 404.14 ms | 358.48 ms | N/A | N/A | 3747.80 ms | 69.09 ms |
| i2c.v | 280.74 ms | 489.80 ms | N/A | N/A | 2853.99 ms | 27.15 ms |
| bar.v | 727.51 ms | 856.17 ms | N/A | N/A | 7083.19 ms | 59.48 ms |
| max.v | 1040.80 ms | 1279.32 ms | N/A | N/A | 12.57 s | 86.34 ms |
| arbiter.v | 2165.67 ms | 1927.86 ms | N/A | N/A | 17.91 s | 172.31 ms |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| ctrl.v | 8.65x | 8.34x | N/A | N/A | 1.00x | 128.70x |
| int2float.v | 10.27x | 5.61x | N/A | N/A | 1.00x | 107.73x |
| dec.v | 10.16x | 6.72x | N/A | N/A | 1.00x | 45.94x |
| router.v | 11.03x | 10.93x | N/A | N/A | 1.00x | 104.24x |
| cavlc.v | 9.14x | 5.64x | N/A | N/A | 1.00x | 168.80x |
| priority.v | 53.57x | 54.66x | N/A | N/A | 1.00x | 301.38x |
| adder.v | 9.27x | 10.45x | N/A | N/A | 1.00x | 54.25x |
| i2c.v | 10.17x | 5.83x | N/A | N/A | 1.00x | 105.11x |
| bar.v | 9.74x | 8.27x | N/A | N/A | 1.00x | 119.08x |
| max.v | 12.08x | 9.83x | N/A | N/A | 1.00x | 145.59x |
| arbiter.v | 8.27x | 9.29x | N/A | N/A | 1.00x | 103.92x |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `11.46x`
- **rx-sweep (Linear Compiled):** `9.37x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `111.98x`

### Cross-Engine Comparisons

- **Reactor Sweep vs Propagate Ratio:** `0.82x` (propagate faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | Instructions | Cycles | IPC | L1 Loads | L1 Misses | L2 Loads | L2 Misses | L3 Loads | DRAM Loads | Branches | Branch Misses |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| ctrl.v | rx-prop | 575.59M | 170.16M | 3.38 | 234.92M | 523.74K | 523.74K | 4.82K | 22.23K | 6.57K | 58.57M | 1.87M |
| ctrl.v | rx-sweep (Linear) | 369.88M | 170.75M | 2.17 | 167.94M | 575.16K | 575.16K | 3.58K | 24.38K | 14.70K | 72.45M | 3.48M |
| ctrl.v | Icarus Verilog | 5.10B | 1.47B | 3.47 | 2.46B | 40.16M | 40.16M | 4.50K | 16.90K | 885.00 | 1.02B | 11.31M |
| ctrl.v | Verilator C++ | 5.98M | 10.12M | 0.59 | 19.11M | 41.00K | 41.00K | 2.79K | 23.35K | 0.00 | 5.21M | 50.76K |
| int2float.v | rx-prop | 578.06M | 169.46M | 3.41 | 239.49M | 2.26M | 2.26M | 7.06K | 38.48K | 12.06K | 58.78M | 1.69M |
| int2float.v | rx-sweep (Linear) | 487.58M | 305.06M | 1.60 | 257.37M | 2.03M | 2.03M | 3.54K | 31.65K | 9.41K | 93.91M | 6.94M |
| int2float.v | Icarus Verilog | 5.71B | 1.79B | 3.18 | 2.82B | 61.15M | 61.15M | 3.71K | 14.04K | 7.11K | 1.15B | 15.24M |
| int2float.v | Verilator C++ | 4.38M | 9.49M | 0.46 | 27.95M | 30.78K | 30.78K | 2.58K | 26.19K | 3.65K | 4.14M | 147.61K |
| dec.v | rx-prop | 179.06M | 51.97M | 3.45 | 80.25M | 360.01K | 360.01K | 2.48K | 25.44K | 5.25K | 16.80M | 209.77K |
| dec.v | rx-sweep (Linear) | 195.53M | 81.37M | 2.40 | 96.69M | 584.85K | 584.85K | 2.73K | 21.18K | 3.01K | 51.34M | 1.19M |
| dec.v | Icarus Verilog | 2.46B | 612.73M | 4.01 | 1.06B | 22.97M | 22.97M | 2.36K | 11.96K | 1.29K | 495.15M | 3.85M |
| dec.v | Verilator C++ | 5.40M | 10.42M | 0.52 | 32.14M | 38.93K | 38.93K | 717.00 | 35.48K | 336.00 | 4.49M | 49.23K |
| router.v | rx-prop | 747.79M | 268.52M | 2.78 | 363.83M | 5.27M | 5.27M | 107.65K | 2.31M | 2.27M | 103.36M | 4.28M |
| router.v | rx-sweep (Linear) | 668.35M | 272.48M | 2.45 | 321.90M | 5.06M | 5.06M | 102.78K | 2.30M | 2.26M | 142.30M | 4.03M |
| router.v | Icarus Verilog | 9.40B | 2.64B | 3.56 | 4.44B | 79.17M | 79.17M | 8.25K | 17.72K | 3.05K | 1.86B | 18.95M |
| router.v | Verilator C++ | 23.47M | 10.41M | 2.26 | 37.59M | 131.82K | 131.82K | 3.67K | 121.33K | 199.00 | 2.82M | 27.53K |
| cavlc.v | rx-prop | 1.72B | 545.91M | 3.15 | 685.55M | 40.20M | 40.20M | 2.96K | 33.12K | 18.22K | 169.62M | 4.94M |
| cavlc.v | rx-sweep (Linear) | 1.38B | 892.94M | 1.54 | 670.55M | 48.48M | 48.48M | 2.18K | 33.68K | 6.61K | 255.06M | 19.41M |
| cavlc.v | Icarus Verilog | 15.29B | 5.07B | 3.01 | 7.86B | 298.72M | 298.72M | 97.77K | 120.40K | 8.87K | 3.08B | 39.68M |
| cavlc.v | Verilator C++ | 49.09M | 22.53M | 2.18 | 26.73M | 15.23K | 15.23K | 139.00 | 27.89K | 5.94K | 4.31M | 108.86K |
| priority.v | rx-prop | 2.96B | 977.38M | 3.03 | 1.30B | 73.72M | 73.72M | 232.21K | 5.36M | 5.12M | 362.12M | 8.19M |
| priority.v | rx-sweep (Linear) | 2.35B | 959.11M | 2.45 | 1.04B | 77.44M | 77.44M | 251.30K | 5.30M | 5.15M | 482.59M | 13.51M |
| priority.v | Icarus Verilog | 182.25B | 48.39B | 3.77 | 88.09B | 2.32B | 2.32B | 1.61M | 2.57M | 40.34K | 36.43B | 257.34M |
| priority.v | Verilator C++ | 185.33M | 155.43M | 1.19 | 132.86M | 141.81K | 141.81K | 1.34K | 93.53K | 8.17K | 16.74M | 750.10K |
| adder.v | rx-prop | 4.52B | 1.64B | 2.76 | 2.02B | 122.97M | 122.97M | 592.82K | 13.29M | 12.60M | 592.10M | 17.67M |
| adder.v | rx-sweep (Linear) | 3.87B | 1.48B | 2.61 | 1.72B | 127.44M | 127.44M | 550.20K | 12.92M | 12.32M | 793.87M | 18.20M |
| adder.v | Icarus Verilog | 50.67B | 13.50B | 3.75 | 24.01B | 723.93M | 723.93M | 2.44M | 3.45M | 74.66K | 9.96B | 68.00M |
| adder.v | Verilator C++ | 235.62M | 240.62M | 0.98 | 185.45M | 221.71K | 221.71K | 6.33K | 178.00K | 78.05K | 14.03M | 1.35M |
| i2c.v | rx-prop | 3.14B | 1.12B | 2.80 | 1.35B | 102.63M | 102.63M | 443.84K | 7.82M | 7.42M | 377.38M | 12.51M |
| i2c.v | rx-sweep (Linear) | 2.93B | 1.87B | 1.56 | 1.46B | 112.18M | 112.18M | 399.24K | 6.82M | 6.58M | 599.95M | 39.30M |
| i2c.v | Icarus Verilog | 35.11B | 10.24B | 3.43 | 16.90B | 548.87M | 548.87M | 2.13M | 2.97M | 53.89K | 6.98B | 63.61M |
| i2c.v | Verilator C++ | 227.13M | 98.12M | 2.31 | 113.96M | 180.78K | 180.78K | 2.47K | 101.81K | 8.97K | 14.67M | 1.14M |
| bar.v | rx-prop | 9.43B | 2.65B | 3.57 | 3.66B | 367.27M | 367.27M | 143.53K | 5.07M | 4.70M | 974.40M | 4.73M |
| bar.v | rx-sweep (Linear) | 6.26B | 3.13B | 2.00 | 2.87B | 229.81M | 229.81M | 150.99K | 5.12M | 4.89M | 1.19B | 60.93M |
| bar.v | Icarus Verilog | 93.94B | 25.30B | 3.71 | 43.44B | 2.37B | 2.37B | 381.33M | 511.14M | 123.64K | 18.86B | 65.31M |
| bar.v | Verilator C++ | 337.23M | 194.68M | 1.73 | 213.61M | 185.08K | 185.08K | 3.08K | 184.76K | 75.61K | 21.53M | 1.45M |
| max.v | rx-prop | 12.54B | 4.16B | 3.01 | 5.24B | 496.99M | 496.99M | 1.43M | 28.10M | 26.82M | 1.50B | 26.97M |
| max.v | rx-sweep (Linear) | 8.89B | 5.00B | 1.78 | 4.42B | 346.15M | 346.15M | 1.44M | 28.19M | 26.92M | 1.79B | 97.22M |
| max.v | Icarus Verilog | 146.34B | 44.97B | 3.25 | 73.17B | 2.68B | 2.68B | 446.51M | 644.85M | 291.72K | 28.85B | 233.91M |
| max.v | Verilator C++ | 747.59M | 298.25M | 2.51 | 380.09M | 405.16K | 405.16K | 12.14K | 357.91K | 328.64K | 50.32M | 774.13K |
| arbiter.v | rx-prop | 23.45B | 7.94B | 2.95 | 8.98B | 792.75M | 792.75M | 47.51M | 273.72M | 12.36M | 2.36B | 22.10M |
| arbiter.v | rx-sweep (Linear) | 22.08B | 7.02B | 3.15 | 7.65B | 840.82M | 840.82M | 30.84M | 371.68M | 12.37M | 4.26B | 63.97M |
| arbiter.v | Icarus Verilog | 205.65B | 63.82B | 3.22 | 96.92B | 5.85B | 5.85B | 3.00B | 5.60B | 418.16K | 41.16B | 97.99M |
| arbiter.v | Verilator C++ | 725.31M | 621.25M | 1.17 | 539.53M | 208.92K | 208.92K | 4.73K | 169.17K | 159.57K | 27.68M | 3.80M |
