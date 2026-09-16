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
| DMA.v | 31,920 | 56.88 MB (88.1 MB peak) | N/A | 103.14 MB (111.0 MB peak) | 1.36 MB (5.1 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| DMA.v | 31,920 | 52.77 ms (12.931 ms opt) | N/A | 518.45 ms | 21.68 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| DMA.v | 1575.91 ms | 1840.29 ms | 2069.06 ms | N/A | 5631.21 ms | 717.35 ms |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| DMA.v | 3.57x | 3.06x | 2.72x | N/A | 1.00x | 7.85x |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `3.57x`
- **rx-sweep (Linear Compiled):** `3.06x`
- **rx-oop (OOP Graph):** `2.72x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `7.85x`

### Cross-Engine Comparisons

- **Reactor Sweep vs Propagate Ratio:** `0.86x` (propagate faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | IPC | Cycles | Instructions | L1 Loads | L1 Hit% | L2 Hit% | LLC Misses | Brn Miss% |
|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| DMA.v | rx-prop | 2.82 | 6.51B | 18.37B | 6.10B | 87.62% | 73.04% | 203.58M | 0.54% |
| DMA.v | rx-sweep (Linear) | 3.51 | 7.61B | 26.74B | 8.32B | 87.09% | 88.70% | 121.37M | 0.84% |
| DMA.v | rx-oop (OOP Engine) | 2.05 | 8.50B | 17.41B | 9.98B | 89.87% | 53.50% | 470.04M | 0.88% |
| DMA.v | Icarus Verilog | 3.43 | 25.88B | 88.81B | 40.46B | 97.21% | 47.06% | 597.52M | 0.38% |
