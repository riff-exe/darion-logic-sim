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
| DMA.v | 31,920 | 55.50 MB (83.4 MB peak) | N/A | 103.19 MB (111.0 MB peak) | 1.50 MB (5.2 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| DMA.v | 31,920 | 50.66 ms (12.507 ms opt) | N/A | 521.34 ms | 21.72 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| DMA.v | 6666.32 ms | 6926.44 ms | N/A | N/A | 29.21 s | 3431.22 ms |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| DMA.v | 4.38x | 4.22x | N/A | N/A | 1.00x | 8.51x |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `4.38x`
- **rx-sweep (Linear Compiled):** `4.22x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `8.51x`

### Cross-Engine Comparisons

- **Reactor Sweep vs Propagate Ratio:** `0.96x` (propagate faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | Instructions | Cycles | IPC | L1 Loads | L1 Misses | L2 Loads | L2 Misses | L3 Loads | DRAM Loads | Branches | Branch Misses |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| DMA.v | rx-prop | 70.25B | 24.61B | 2.85 | 27.09B | 2.67B | 2.67B | 546.41M | 1.78B | 68.87M | 7.21B | 35.82M |
| DMA.v | rx-sweep (Linear) | 86.38B | 25.59B | 3.38 | 26.98B | 4.30B | 4.30B | 485.78M | 3.37B | 68.67M | 18.01B | 130.41M |
| DMA.v | Icarus Verilog | 373.63B | 108.53B | 3.44 | 170.93B | 4.62B | 4.62B | 2.60B | 4.51B | 49.00M | 71.19B | 248.62M |
| DMA.v | Verilator C++ | 19.38B | 12.08B | 1.60 | 9.17B | 11.52M | 11.52M | 780.06M | 782.98M | 200.03K | 1.27B | 10.03M |
