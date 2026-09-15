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
| DMA.v | 31,920 | 57.31 MB (88.6 MB peak) | N/A | 103.36 MB (111.1 MB peak) | 1.50 MB (5.2 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| DMA.v | 31,920 | 73.06 ms (16.143 ms opt) | N/A | 647.87 ms | 26.01 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| DMA.v | 2334.55 ms | 2749.08 ms | 2989.62 ms | N/A | 8663.64 ms | 1087.78 ms |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| DMA.v | 3.71x | 3.15x | 2.90x | N/A | 1.00x | 7.96x |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `3.71x`
- **rx-sweep (Linear Compiled):** `3.15x`
- **rx-oop (OOP Graph):** `2.90x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `7.96x`

### Cross-Engine Comparisons

- **Reactor Sweep vs Propagate Ratio:** `0.85x` (propagate faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | IPC | Cycles | Instructions | L1 Loads | L1 Hit% | L2 Hit% | LLC Misses | Brn Miss% |
|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| DMA.v | rx-prop | 2.81 | 6.52B | 18.33B | 6.07B | 87.55% | 73.17% | 202.89M | 0.54% |
| DMA.v | rx-sweep (Linear) | 3.48 | 7.69B | 26.76B | 8.31B | 87.08% | 88.06% | 128.28M | 0.85% |
| DMA.v | rx-oop (OOP Engine) | 2.15 | 8.36B | 17.99B | 6.14B | 84.93% | 49.38% | 468.14M | 0.58% |
| DMA.v | Icarus Verilog | 3.30 | 26.92B | 88.78B | 41.15B | 97.24% | 48.65% | 581.44M | 0.37% |
