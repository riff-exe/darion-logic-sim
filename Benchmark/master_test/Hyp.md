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
| hyp.v | 420,896 | 392.25 MB (419.8 MB peak) | N/A | 280.49 MB (288.4 MB peak) | 3.54 MB (7.2 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| hyp.v | 420,896 | 613.74 ms (100.939 ms opt) | N/A | 2.62 s | 116.02 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| hyp.v | 180.48 s | 851.64 ms | 301.93 s | N/A | 1496.10 s | 245.20 ms |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| hyp.v | 8.29x | 1756.72x | 4.96x | N/A | 1.00x | 6101.61x |

### Total Gate Evaluations

| Circuit | Gates | rx-prop Evals | rx-sweep Evals | rx-oop Evals | Pure Python Evals |
|:---|---:|---:|---:|---:|---:|
| hyp.v | 420,896 | 25,609,842,152 | 129,253,082 | 26,040,243,146 | N/A |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `8.29x`
- **rx-sweep (Linear Compiled):** `1756.72x`
- **rx-oop (OOP Graph):** `4.96x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `6101.61x`

### Gate Evaluation Highlights

- **Reactor Sweep vs Propagate Total Evaluations Ratio:** `0.01x` (propagate performed more evaluations)

### Cross-Engine Comparisons

- **Reactor Sweep vs Propagate Ratio:** `211.92x` (sweep faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | Instructions | Cycles | IPC | L1 Loads | L1 Misses | L2 Loads | L2 Misses | L3 Loads | DRAM Loads | Branches | Branch Misses |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| hyp.v | rx-prop | 850.36B | 647.66B | 1.31 | 327.92B | 43.64B | 43.64B | 28.19B | 46.49B | 110.24M | 80.07B | 3.93B |
| hyp.v | rx-sweep (Linear) | 4.52B | 3.02B | 1.50 | 2.10B | 152.09M | 152.09M | 38.85M | 149.72M | 15.30M | 840.87M | 44.86M |
| hyp.v | rx-oop (OOP Engine) | 963.99B | 1083.53B | 0.89 | 819.76B | 56.64B | 56.64B | 44.56B | 65.35B | 342.92M | 116.21B | 9.32B |
| hyp.v | Icarus Verilog | 6743.95B | 5369.88B | 1.26 | 4341.59B | 176.92B | 176.92B | 151.12B | 211.83B | 18.03B | 1352.22B | 19.39B |
| hyp.v | Verilator C++ | 268.15M | 866.95M | 0.31 | 168.78M | 7.39M | 7.39M | 20.65M | 21.20M | 6.03K | 40.72M | 1.18M |
