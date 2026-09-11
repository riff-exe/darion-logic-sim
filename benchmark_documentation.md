# Darion Logic Sim — Benchmark & Test Documentation

> **Audience:** You know Python, but know nothing about digital logic circuits.  
> This document tells you *exactly* what every benchmark and test builds, wire by wire, and what it is measuring.  
> Every file listed here actually exists in the `tests/` directory and runs as-is.

---

## Table of Contents

1. [Installation, Dependencies & Backend Compilation](#0-installation-dependencies--backend-compilation)
   - [0.1 Python Environment & Libraries](#01-python-environment--libraries)
   - [0.2 System Toolchain & Hardware Profilers (perf, Icarus, Verilator)](#02-system-toolchain--hardware-profilers-perf-icarus-verilator)
   - [0.3 Compiling the Cython Backends (`scripts/build.sh` / `build.bat`)](#03-compiling-the-cython-backends-scriptsbuildsh--buildbat)
2. [Shared Concepts & Multi-Engine Architecture](#1-shared-concepts--multi-engine-architecture)
   - [1.1 What is a "Gate"?](#11-what-is-a-gate)
   - [1.2 What Does `connect(gate, source, slot)` Do?](#12-what-does-connectgate-source-slot-do)
   - [1.3 The Six Simulation Backends & Modes](#13-the-six-simulation-backends--modes)
   - [1.4 The Book Algorithm & $O(1)$ Gate Evaluation](#14-the-book-algorithm--o1-gate-evaluation)
   - [1.5 Topological Compilation & Memory Defragmentation (`circuit.optimize()`)](#15-topological-compilation--memory-defragmentation-circuitoptimize)
   - [1.6 Sequential Circuits & DFF Modeling](#16-sequential-circuits--dff-modeling)
   - [1.7 Benchmark Datasets](#17-benchmark-datasets)
3. [benchmark.py — Combinational Multi-Engine Benchmark](#2-benchmarkpy--combinational-multi-engine-benchmark)
4. [benchmark_89.py — Sequential Multi-Engine Benchmark](#3-benchmark_89py--sequential-multi-engine-benchmark)
5. [load.py — Universal RAM & Memory Footprint Benchmark](#4-loadpy--universal-ram--memory-footprint-benchmark)
6. [geometry.py — Circuit Geometry & Topological Locality Analyzer](#5-geometrypy--circuit-geometry--topological-locality-analyzer)
7. [verifier.py — Combinational State & Equivalence Verifier](#6-verifierpy--combinational-state--equivalence-verifier)
8. [verifier_89.py — Sequential State & Equivalence Verifier](#7-verifier_89py--sequential-state--equivalence-verifier)
9. [cache_test.py — High-Integrity Cache & Optimization Profiler](#8-cache_testpy--high-integrity-cache--optimization-profiler)
10. [cache_perf.py — Hardware Cache Profiler (Linux `perf`)](#9-cache_perfpy--hardware-cache-profiler-linux-perf)
11. [perf.py — Multi-Engine Hardware Event Profiler](#10-perfpy--multi-engine-hardware-event-profiler)
12. [ic_circuit_benchmark.py — IC Packaging & Serialization Benchmark](#11-ic_circuit_benchmarkpy--ic-packaging--serialization-benchmark)
13. [integrity_test.py — Master Integrity & Stress Test Suite](#12-integrity_testpy--master-integrity--stress-test-suite)
14. [iscas89_sequential_harness.py — Sequential Verilog Harness Engine](#13-iscas89_sequential_harnesspy--sequential-verilog-harness-engine)
15. [bash_test.sh — Automated Pipeline Runner](#14-bash_testsh--automated-pipeline-runner)
16. [Summary Table & Cheat Sheet](#15-summary-table--cheat-sheet)

---

## 0. Installation, Dependencies & Backend Compilation

Before running benchmarks or simulation tests, ensure all Python packages, system compilers, and simulation backends are installed and compiled.

### 0.1 Python Environment & Libraries

Create and activate a virtual environment, then install the core Python packages:

```bash
# 1. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate       # On Windows: .venv\Scripts\activate

# 2. Upgrade pip and build tools
pip install --upgrade pip setuptools wheel

# 3. Install all required dependencies
pip install pyside6 setuptools cython orjson matplotlib psutil numpy aioconsole
```

| Package | Purpose in Darion Logic Sim |
|---------|-----------------------------|
| **`pyside6`** | Qt6 GUI framework powering the interactive desktop visual circuit editor ([`main.py`](file:///home/farhan/Github/darion-logic-sim/main.py)). |
| **`setuptools`** | Python build system required to compile C/C++ extensions via `setup.py`. |
| **`cython`** | Optimizing static compiler translating Cython (`.pyx`) code into native C++ extensions. |
| **`orjson`** | Ultra-fast JSON library for parsing and dumping large verification reports and benchmark results. |
| **`matplotlib`** | Plotting engine for generating cache cliff curves, scaling charts, and memory locality histograms (`--plot`). |
| **`psutil`** | Cross-platform system and process monitoring library used for tracking peak RAM usage (RSS in MB) in [`load.py`](file:///home/farhan/Github/darion-logic-sim/tests/load.py) and [`cache_test.py`](file:///home/farhan/Github/darion-logic-sim/tests/cache_test.py). |
| **`numpy`** | Vectorized array processing for calculating jump distances, percentiles, and cache locality metrics in [`geometry.py`](file:///home/farhan/Github/darion-logic-sim/tests/geometry.py). |
| **`aioconsole`** | Non-blocking asynchronous console I/O for interactive terminal menus in [`tests/CLI.py`](file:///home/farhan/Github/darion-logic-sim/tests/CLI.py) and [`integrity_test.py`](file:///home/farhan/Github/darion-logic-sim/tests/integrity_test.py). |

---

### 0.2 System Toolchain & Hardware Profilers (perf, Icarus, Verilator)

Certain benchmarks interface directly with Linux hardware performance counters or third-party HDL simulators:

#### 1. C++ Build Toolchain (Required for Cython compilation)
- **Linux (Ubuntu / Debian):**
  ```bash
  sudo apt update && sudo apt install build-essential g++
  ```
- **Linux (Fedora / RHEL):**
  ```bash
  sudo dnf groupinstall "Development Tools"
  ```
- **macOS:**
  ```bash
  xcode-select --install
  ```
- **Windows:**
  Install Visual Studio (2019 or later) with the **"Desktop development with C++"** workload, or install MinGW-w64 (GCC) and ensure `g++` is in your `PATH`.

#### 2. Linux Hardware Profiler (`perf`)
[`cache_perf.py`](file:///home/farhan/Github/darion-logic-sim/tests/cache_perf.py) and [`perf.py`](file:///home/farhan/Github/darion-logic-sim/tests/perf.py) use the Linux kernel PMU to measure L1/L2/L3 cache misses, branch mispredictions, and IPC without simulation overhead.
```bash
sudo apt install linux-tools-common linux-tools-generic linux-tools-$(uname -r)
```
*Configuring Non-Root Access:* By default, Linux restricts PMU hardware events for security. Allow non-root users to monitor hardware counters:
```bash
sudo sysctl -w kernel.perf_event_paranoid=1
# For permanent configuration, add to /etc/sysctl.d/local.conf:
# kernel.perf_event_paranoid = 1
```

#### 3. HDL Baseline Simulators (`iverilog` & `verilator`)
The benchmark harness runs verification and performance comparisons against industry standard open-source tools:
- **Icarus Verilog (`iverilog` & `iverilog-vpi`):**
  ```bash
  sudo apt install iverilog
  ```
- **Verilator (Cycle-accurate C++ compiler):**
  ```bash
  sudo apt install verilator
  ```

---

### 0.3 Compiling the Cython Backends (`scripts/build.sh` / `build.bat`)

Darion contains two distinct Cython-accelerated simulation backends located in [`reactor/`](file:///home/farhan/Github/darion-logic-sim/reactor/) and [`reactor_oop/`](file:///home/farhan/Github/darion-logic-sim/reactor_oop/). You can compile them easily using the provided build scripts.

#### On Linux / macOS ([`scripts/build.sh`](file:///home/farhan/Github/darion-logic-sim/scripts/build.sh)):

The build script compiles with maximum optimization (`-O3 -g -fno-omit-frame-pointer`) using your system's detected C++ compiler (`g++` or `clang++`):

```bash
# 1. Compile the default high-performance Data-Oriented Design (AOS) Reactor:
bash scripts/build.sh --reactor

# 2. Compile the Object-Oriented Cython Reactor (ReactorOOP):
bash scripts/build.sh --reactor-oop
```

> [!NOTE]
> Running `bash scripts/build.sh` without arguments defaults to `--reactor`.  
> Both `--reactor-oop` and `--reactor_oop` are accepted interchangeably.

#### On Windows ([`scripts/build.bat`](file:///home/farhan/Github/darion-logic-sim/scripts/build.bat)):

The Windows batch script automatically locates your MSVC compiler (via `vswhere.exe` or `cl.exe` on `PATH`) or falls back to MinGW-w64 (`gcc.exe`):

```cmd
:: Compile standard Reactor (.pyd files into reactor\)
scripts\build.bat --reactor

:: Compile ReactorOOP (.pyd files into reactor_oop\)
scripts\build.bat --reactor-oop
```

#### What `build.sh` Does Under the Hood:
1. Automatically resolves your active virtual environment (`.venv/bin/python` or system `python3`).
2. Cleans out previous build artifacts (`rm -rf build/ *.so *.pyd`).
3. Executes `python setup.py build_ext --inplace --compiler=unix --source-dir <target>`.
4. Outputs compiled native binary shared libraries directly into the target directory (`reactor/Circuit.*.so` and `reactor/Const.*.so`).

---

## 1. Shared Concepts & Multi-Engine Architecture

Before reading anything else, you need these fundamental mental models.

### 1.1 What is a "Gate"?

Think of a gate as a fast hardware computational node that reads one or more *input* voltage states (`HIGH=1` or `LOW=0`) and immediately computes an *output* state. The primary components used throughout these files are:

| Name | Symbol | Truth Rule |
|------|--------|------------|
| **VARIABLE** | `V` | A primary input variable — driven by software via `toggle()`. Has an output only. |
| **NOT** | `¬` | Inverter: `HIGH → LOW`, `LOW → HIGH`. |
| **AND** | `&` | Output = `HIGH` only when **all** inputs are `HIGH`. |
| **OR** | `\|` | Output = `HIGH` when **any** input is `HIGH`. |
| **XOR** | `^` | Output = `HIGH` when an **odd number** of inputs are `HIGH`. |
| **NAND** | `¬&` | NOT(AND): Output = `HIGH` unless all inputs are `HIGH`. |
| **NOR** | `¬\|` | NOT(OR): Output = `HIGH` only when all inputs are `LOW`. |
| **XNOR** | `≡` | NOT(XOR): Output = `HIGH` when an **even number** of inputs are `HIGH`. |
| **BUFFER** | `B` | Identity gate: mirrors input directly (`HIGH → HIGH`, `LOW → LOW`). |
| **PROBE** | `P` | Non-intrusive tap: observes signal state without loading downstream gates. |
| **INPUT_PIN / OUTPUT_PIN** | `IN`/`OUT` | Boundary pins used when packaging sub-circuits into Integrated Circuits (ICs). |
| **DFF** | `DFF` | D Flip-Flop: clocked storage element capturing state `D` at rising clock edge `CLK` and outputting `Q`. |

### 1.2 What Does `connect(gate, source, slot)` Do?

It routes the output of `source` into input pin `slot` of `gate`. When `source` toggles its output, the downstream `gate` receives an event and updates its internal state.

### 1.3 The Six Simulation Backends & Modes

Darion Logic Sim implements and benchmarks six distinct execution engines and modes:

| Backend / Mode | Language | Location | Evaluation Strategy |
|----------------|----------|----------|---------------------|
| **1. Python Engine** | Pure Python | `engine/` | Dynamic OOP graph traversal. Serves as pure-Python reference. |
| **2. Cython Reactor (Propagate)** | Cython / C++ | `reactor/` (`SIMULATE`) | Breadth-First Search (BFS) double-buffered wavefront event-driven scheduler. Only visits changed gates. |
| **3. Cython Reactor (Sweep)** | Cython / C++ | `reactor/` (`COMPILE`) | Single forward linear traversal through topologically sorted C++ array of structures. Requires `optimize()`. |
| **4. Cython Reactor OOP** | Cython / C++ | `reactor_oop/` | Object-oriented Cython implementation (separate heap gate objects). |
| **5. Icarus Verilog** | Compiled C/C++ | `iverilog` / `vvp` | Standard open-source discrete-event simulator with custom VPI timing. Baseline comparison (1.0x). |
| **6. Verilator** | Compiled Native C++ | `verilator -O3` | Cycle-accurate native C++ compiled simulation binary. |

### 1.4 The Book Algorithm & $O(1)$ Gate Evaluation

Rather than re-reading all input sources whenever any single wire toggles, each gate maintains a compact fixed-size array called `book` that counts how many of its inputs are currently `HIGH`, `LOW`, or `UNKNOWN`.

- When an upstream wire flips from `LOW` to `HIGH`, the gate decrements `book[LOW]` and increments `book[HIGH]`.
- Output evaluation is computed purely from these counts in $O(1)$ time regardless of fan-in:
  - **AND**: Output is `HIGH` if and only if `book[HIGH] == total_inputs`.
  - **OR**: Output is `HIGH` if and only if `book[HIGH] > 0`.
  - **XOR**: Output is `HIGH` if and only if `book[HIGH] % 2 == 1`.
- Gates like `NOT` and `BUFFER` bypass the book array completely and mirror or invert their sole input directly.

### 1.5 Topological Compilation & Memory Defragmentation (`circuit.optimize()`)

When circuits are loaded from disk or built interactively, gate structures are allocated across arbitrary heap addresses, degrading CPU cache utilization.

Calling `circuit.optimize()` performs a full topological sort using a modified Kahn's algorithm and packs all gate data into a contiguous **Array of Structures (AOS)** in C++ (`reactor/Profile.h`):
1. **Cache Locality:** Related gates reside adjacent in memory, minimizing L1/L2/L3 cache misses.
2. **Linear Sweep Capability:** Once topologically sorted, the entire circuit can be evaluated with a single linear memory pass (`sweep()`), completely avoiding queue management overhead.
3. **Array Index IDs:** Every gate is addressed by its linear index integer, eliminating pointer chasing.

### 1.6 Sequential Circuits & DFF Modeling

Sequential circuits (e.g., ISCAS89) contain internal state and feedback loops governed by Flip-Flops:
- DFF components are loaded from [`DFF.json`](file:///home/farhan/Github/darion-logic-sim/DFF.json), exposing `CLK`, `D`, and `Q` pins.
- Simulation drives 2-phase clock cycles:
  1. **Setup Phase (`CLK = 0`):** Inputs stabilize combinational gates feeding the DFF inputs.
  2. **Trigger Phase (`CLK = 1`):** Rising clock edge clocks the state into `Q`, triggering downstream logic.
- A 50-cycle warmup sequence flushes unknown reset states before measurements begin.
- Async event loop tasks (`task_manager`) are settled between clock cycles to guarantee complete feedback convergence.

### 1.7 Benchmark Datasets

The repository includes standard benchmark suites located in `tests/`:

- **ISCAS-85 (`tests/ISCAS85/`):** 11 classic combinational netlists (`c17` to `c7552`), available in both `.v` (Verilog) and `.json` formats.
- **ISCAS-89 (`tests/ISCAS89/`):** 30 sequential netlists with DFF elements (`s27` to `s38584`), available in both `.v` and `.json` formats.
- **EPFL Combinational (`tests/EPFL_parsed/`):** Standard arithmetic and control circuits (`adder`, `arbiter`, `cavlc`, `ctrl`, `dec`, `i2c`, `int2float`, `priority`, `router`, etc.).
- **EPFL Large (`tests/EPFL_large_parsed/`):** Heavyweight benchmarks (`div`, `log2`, `mem_ctrl`, `multiplier`, `sin`, `sqrt`, `square`, `voter`).
- **EPFL Mammoth (`tests/EPFL_mammoth_parsed/`):** Giant combinational netlists with 1,000,000+ gates (`hyp`).

---

## 2. `benchmark.py` — Combinational Multi-Engine Benchmark

### 2.1 Purpose & Methodology
**File:** [`tests/benchmark.py`](file:///home/farhan/Github/darion-logic-sim/tests/benchmark.py)  
**Purpose:** Head-to-head simulation throughput benchmark comparing up to 6 execution backends on combinational netlists (ISCAS-85, EPFL standard, large, and mammoth).

**Methodology:**
- **Deterministic PRNG:** All engines receive an identical pseudorandom toggle sequence generated with `random.seed(42)`.
- **Symmetric Warmup:** Untimed warmup vectors run first through `batch_toggle()` to prime internal states and CPU caches.
- **Garbage Collection:** Python GC is explicitly disabled (`gc.disable()`) during timed windows.
- **VPI Timer Isolation:** Icarus Verilog compiles a custom C VPI extension ([`harness_build/vpi_timer.c`](file:///home/farhan/Github/darion-logic-sim/harness_build/vpi_timer.c)) exposing `$start_timer()` and `$stop_timer()`. The timer starts *after* `$readmemb` finishes loading vector tables into memory and stops *before* simulation teardown, measuring pure simulation throughput excluding disk I/O.
- **Metrics Reported:** Elapsed simulation time (ms), total gate evaluations, Mega-Evaluations Per Second (ME/s), and geometric-mean speedup relative to Icarus baseline (1.00x).

### 2.2 Command-Line Options
```text
usage: benchmark.py [-h] [--vectors VECTORS] [--warmup WARMUP] [--optimize]
                    [--output OUTPUT] [--dump] [--json] [--plot] [--perf]
                    [--perf-events PERF_EVENTS] [--no-engine] [--no-rx-prop]
                    [--no-rx-sweep] [--no-rx-oop] [--no-icarus]
                    [--no-verilator]
                    [target]
```

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `target` | Positional | `None` | Path to `.v` file or folder containing `.v` files. |
| `--vectors` | Integer | `50000` | Total vectors to simulate (warmup + measured). |
| `--warmup` | Integer | `5000` | Untimed warmup vector count. |
| `--optimize` | Flag | `False` | Apply `circuit.optimize()` (topological sort) before simulation. |
| `--dump` | Flag | `False` | Save human-readable Markdown summary report to `test_result/benchmark/`. |
| `--json` | Flag | `False` | Output structured machine-readable JSON results to stdout. |
| `--plot` | Flag | `False` | Generate graphical comparison plots in `test_result/`. |
| `--perf` | Flag | `False` | Attach Linux `perf` profiler and capture hardware counters. |
| `--perf-events` | String | `""` | Comma-separated list of hardware events to trace. |
| `--no-engine` | Flag | `False` | Skip Pure Python Engine (useful for large circuits where Python is too slow). |
| `--no-rx-prop` | Flag | `False` | Skip Reactor BFS wavefront mode (`SIMULATE`). |
| `--no-rx-sweep` | Flag | `False` | Skip Reactor linear sweep mode (`COMPILE`). |
| `--no-rx-oop` | Flag | `False` | Skip Reactor OOP backend. |
| `--no-icarus` | Flag | `False` | Skip Icarus Verilog baseline harness. |
| `--no-verilator` | Flag | `False` | Skip Verilator native C++ harness. |

### 2.3 Execution Examples
```bash
# Full combinational benchmark on ISCAS85 (50K vectors, with topological optimization)
python tests/benchmark.py tests/ISCAS85 --optimize --vectors 50000 --warmup 10 --dump

# EPFL standard benchmark
python tests/benchmark.py tests/EPFL_parsed --optimize --vectors 50000 --warmup 10 --dump

# EPFL large benchmark (disable slow Python engine)
python tests/benchmark.py tests/EPFL_large_parsed --optimize --vectors 500 --warmup 10 --no-engine --dump

# EPFL mammoth benchmark (1M+ gates)
python tests/benchmark.py tests/EPFL_mammoth_parsed --optimize --vectors 50 --warmup 10 --no-engine --dump
```

---

## 3. `benchmark_89.py` — Sequential Multi-Engine Benchmark

### 3.1 Purpose & Methodology
**File:** [`tests/benchmark_89.py`](file:///home/farhan/Github/darion-logic-sim/tests/benchmark_89.py)  
**Purpose:** Multi-engine simulation benchmark on ISCAS-89 sequential circuits containing flip-flops (DFF).

**Methodology:**
- **DFF IC Integration:** Automatically loads [`DFF.json`](file:///home/farhan/Github/darion-logic-sim/DFF.json) and wires clock, data, and output pins.
- **Two-Phase Physical Clocking:** Each logical test vector drives two discrete phases:
  1. *Setup:* Data inputs randomized, `CLK = 0`. Combinational logic settles.
  2. *Trigger:* Same data inputs, `CLK = 1`. Rising clock edge latches DFF states.
- **50-Cycle Warmup Flush:** 50 alternating clock cycles with zeroed data inputs flush initial uninitialized states before vector measurement begins.
- **Async Queue Draining:** Drains the event loop queue (`task_manager`) between cycles to properly resolve cyclic sequential dependencies during sweep passes.

### 3.2 Command-Line Options
```text
usage: benchmark_89.py [-h] [--vectors VECTORS] [--warmup WARMUP] [--optimize]
                       [--output OUTPUT] [--dump] [--json] [--plot]
                       [--no-engine] [--no-rx-prop] [--no-rx-sweep]
                       [--no-reactor-oop] [--no-icarus] [--no-verilator]
                       [--perf] [--perf-events PERF_EVENTS]
                       [target]
```

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `target` | Positional | `None` | Path to `.v` file or folder containing ISCAS89 `.v` netlists. |
| `--vectors` | Integer | `50000` | Total logical vectors (warmup + measured). |
| `--warmup` | Integer | `5000` | Untimed warmup logical vectors. |
| `--optimize` | Flag | `False` | Apply topological sort and contiguous AOS memory packing. |
| `--dump` | Flag | `False` | Save Markdown dump to `test_result/benchmark_89/`. |
| `--json` | Flag | `False` | Output JSON summary to stdout. |
| `--no-engine` | Flag | `False` | Skip Pure Python Engine. |
| `--no-rx-prop` | Flag | `False` | Skip Reactor BFS wavefront propagate. |
| `--no-rx-sweep` | Flag | `False` | Skip Reactor linear sweep mode. |
| `--no-reactor-oop` | Flag | `False` | Skip Reactor OOP mode. |
| `--no-icarus` | Flag | `False` | Skip Icarus Verilog sequential harness. |
| `--no-verilator` | Flag | `False` | Skip Verilator C++ sequential harness. |

### 3.3 Execution Examples
```bash
# Run sequential benchmark across all ISCAS89 circuits
python tests/benchmark_89.py tests/ISCAS89 --optimize --vectors 50000 --warmup 10 --dump

# Benchmark a single sequential circuit
python tests/benchmark_89.py tests/ISCAS89/s38584.v --optimize --vectors 10000 --warmup 50
```

---

## 4. `load.py` — Universal RAM & Memory Footprint Benchmark

### 4.1 Purpose & Methodology
**File:** [`tests/load.py`](file:///home/farhan/Github/darion-logic-sim/tests/load.py)  
**Purpose:** Measures the true Resident Set Size (RSS RAM) footprint in megabytes (MB) of loading any circuit (combinational or sequential) across simulation engines.

**Methodology:**
- Uses `psutil.Process().memory_info().rss` in isolated subprocesses to record true baseline vs. post-load memory consumption.
- Supports both Verilog netlists (`.v`) and native JSON definitions (`.json`).
- Automatically instantiates DFF components when parsing sequential circuits.
- Isolates memory allocation costs from simulation runtime state.

### 4.2 Command-Line Options
```text
usage: load.py [-h] [--no-engine] [--no-rx-prop] [--no-rx-sweep] [--no-icarus]
               [--no-verilator] [--dump] [--json]
               [target]
```

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `target` | Positional | `None` | Path to `.v`/`.json` file or directory. |
| `--dump` | Flag | `False` | Save timestamped Markdown summary to `test_result/load/`. |
| `--json` | Flag | `False` | Output results in JSON format. |
| `--no-engine` | Flag | `False` | Skip Python Engine memory measurement. |
| `--no-rx-prop` | Flag | `False` | Skip Reactor Propagate memory measurement. |
| `--no-rx-sweep` | Flag | `False` | Skip Reactor Sweep memory measurement. |
| `--no-icarus` | Flag | `False` | Skip Icarus Verilog memory measurement. |
| `--no-verilator` | Flag | `False` | Skip Verilator memory measurement. |

### 4.3 Execution Examples
```bash
# Measure RAM usage across all benchmark suites
python tests/load.py tests/ISCAS85 --dump
python tests/load.py tests/ISCAS89 --dump
python tests/load.py tests/EPFL_parsed --dump
python tests/load.py tests/EPFL_large_parsed --dump
python tests/load.py tests/EPFL_mammoth_parsed --dump
```

---

## 5. `geometry.py` — Circuit Geometry & Topological Locality Analyzer

### 5.1 Purpose & Methodology
**File:** [`tests/geometry.py`](file:///home/farhan/Github/darion-logic-sim/tests/geometry.py)  
**Purpose:** Inspects circuit graph topology and quantifies CPU cache locality by calculating memory jump distances between interconnected gates.

**The Geometry Metric:**
In an Array of Structures (AOS), every gate occupies an index in a contiguous array. When gate $A$ at index $i$ drives gate $B$ at index $j$, the CPU must fetch index $j$. The *jump distance* is $|j - i|$.
- **Adjacent (`Adj`):** Jump $= 1$ index. Perfect cache line reuse; subsequent gate already prefetched into L1 cache.
- **Near (`Near`):** Jump $\le 8$ indices. High probability of staying in L1 cache (64-byte cache line holds multiple gates).
- **Medium (`Med`):** Jump $\le 64$ indices. Likely hits L2/L3 cache.
- **Far (`Far`):** Jump $> 64$ indices. High risk of L3 cache miss and DRAM latency stall.

`geometry.py` extracts these jump distributions before and after calling `circuit.optimize()`, quantitatively proving why topologically compiled circuits exhibit massive speedups. It also outputs graph depth, width, edge counts, and component counts, and auto-detects sequential circuits containing DFFs.

### 5.2 Command-Line Options
```text
usage: geometry.py [-h] [--dump] [--plot] [target]
```

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `target` | Positional | `None` | Path to `.v` or `.json` file, or directory. |
| `--dump` | Flag | `False` | Save report to `test_result/geometry/datas/geometry_<timestamp>.txt`. |
| `--plot` | Flag | `False` | Generate logarithmic histogram images in `test_result/geometry/plots/`. |

### 5.3 Execution Examples
```bash
# Analyze locality across all suites
python tests/geometry.py tests/ISCAS85 --dump
python tests/geometry.py tests/ISCAS89 --dump
python tests/geometry.py tests/EPFL_parsed --dump
python tests/geometry.py tests/EPFL_large_parsed --dump
python tests/geometry.py tests/EPFL_mammoth_parsed --dump

# Generate cache locality histogram plots
python tests/geometry.py tests/ISCAS85/c7552.v --plot
```

---

## 6. `verifier.py` — Combinational State & Equivalence Verifier

### 6.1 Purpose & Methodology
**File:** [`tests/verifier.py`](file:///home/farhan/Github/darion-logic-sim/tests/verifier.py)  
**Purpose:** Formally verifies 100% bit-exact correctness between all simulation backends on combinational netlists (ISCAS-85 / EPFL).

**Engines Compared:**
1. Icarus Verilog (Golden Reference via Verilog file I/O)
2. Verilator C++ (Compiled cycle-accurate binary)
3. Pure Python Engine
4. Cython Reactor Propagate (`SIMULATE` BFS wavefront)
5. Cython Reactor Sweep (`COMPILE` linear forward pass)
6. Cython Reactor OOP

**Outputs:**
- Terminal summary table printing matching vectors, mismatch count, and pass/fail indicators.
- Structured JSON verification report with vector mismatch details down to the individual pin name.

### 6.2 Command-Line Options
```text
usage: verifier.py [-h] [--vectors VECTORS] [--seed SEED] [--output OUTPUT]
                   [--dump] [--json] [--no-engine] [--no-rx-prop]
                   [--no-rx-sweep] [--no-icarus] [--no-verilator]
                   [--no-reactor-oop]
                   [target]
```

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `target` | Positional | `None` | Path to `.v` file or folder. |
| `--vectors` | Integer | `1000` | Number of test vectors per circuit. |
| `--seed` | Integer | `42` | Pseudorandom number generator seed. |
| `--output` | String | `"verification_report"` | Output file prefix for JSON reports. |
| `--dump` | Flag | `False` | Print full report to stdout. |
| `--json` | Flag | `False` | Emit pure JSON report to stdout. |
| `--no-engine` | Flag | `False` | Skip Python Engine. |
| `--no-rx-prop` | Flag | `False` | Skip Reactor Propagate. |
| `--no-rx-sweep` | Flag | `False` | Skip Reactor Sweep. |
| `--no-reactor-oop`| Flag | `False` | Skip Reactor OOP. |
| `--no-icarus` | Flag | `False` | Skip Icarus Verilog reference. |
| `--no-verilator` | Flag | `False` | Skip Verilator reference. |

### 6.3 Execution Examples
```bash
# Verify 1,000 vectors on all ISCAS-85 circuits
python tests/verifier.py tests/ISCAS85 --vectors 1000 --dump

# Quick sanity check on single circuit
python tests/verifier.py tests/ISCAS85/c880.v --vectors 500
```

---

## 7. `verifier_89.py` — Sequential State & Equivalence Verifier

### 7.1 Purpose & Methodology
**File:** [`tests/verifier_89.py`](file:///home/farhan/Github/darion-logic-sim/tests/verifier_89.py)  
**Purpose:** Bit-exact state verification across all engines on sequential ISCAS-89 circuits with internal state registers (DFFs).

**Methodology:**
- Synchronizes flip-flop initial states using a 50-cycle alternating clock warmup.
- Awaits `task_manager` queue draining to guarantee cyclic stability across evaluation modes.
- Compares sequential state transitions across Icarus, Verilator, Python Engine, Reactor Propagate, Sweep, and OOP.

### 7.2 Command-Line Options
```text
usage: verifier_89.py [-h] [--vectors VECTORS] [--seed SEED] [--output OUTPUT]
                      [--dump] [--json] [--no-engine] [--no-rx-prop]
                      [--no-rx-sweep] [--no-reactor-oop] [--no-icarus]
                      [--no-verilator]
                      [target]
```

### 7.3 Execution Examples
```bash
# Verify all ISCAS-89 sequential circuits
python tests/verifier_89.py tests/ISCAS89 --vectors 500 --dump

# Verify single sequential circuit
python tests/verifier_89.py tests/ISCAS89/s27.v --vectors 200
```

---

## 8. `cache_test.py` — High-Integrity Cache & Optimization Profiler

### 8.1 Purpose & Methodology
**File:** [`tests/cache_test.py`](file:///home/farhan/Github/darion-logic-sim/tests/cache_test.py)  
**Purpose:** Identifies exact circuit size thresholds where circuit memory exceeds CPU hardware cache sizes (L1 $\approx 32\text{--}48\text{ KB}$, L2 $\approx 512\text{ KB}\text{--}1\text{ MB}$, L3 $\approx 16\text{--}32\text{ MB}$), causing steep performance cliffs.

**Fragmentation Modes:**
- **Chaotic:** Random 100% heap shuffle prior to wiring (worst-case pathological cache misses).
- **Realistic:** Allocated in 64-gate modular chunks and shuffled (mirrors human sub-circuit design).
- **Linear:** Allocated strictly in signal dependency order.
- **Homogeneous:** Long chains of identical gates (`AND`, `NAND`, `OR`, `NOR`, `XOR`, `XNOR`, `NOT`).

Tests scale geometrically from 100 to 2,000,000+ gates, profiling unoptimized fragmented memory vs. topologically sorted memory in a single execution.

### 8.2 Command-Line Options
```text
usage: cache_test.py [-h] [--engine] [--reactor_oop] [--chaotic] [--realistic]
                     [--mixed] [--and] [--nand] [--or] [--nor] [--xor]
                     [--xnor] [--not] [--dump] [--plot]
                     [--perf-size PERF_SIZE]
                     [--perf-pass {unopt,opt,sweep,oop}]
                     [--perf-fifo PERF_FIFO]
```

| Flag | Description |
|------|-------------|
| `--engine` | Use Python Engine backend instead of Cython Reactor. |
| `--reactor_oop` | Use Cython OOP backend. |
| `--chaotic` | Run worst-case chaotic shuffled memory test. |
| `--realistic` | Run realistic modular chunk shuffled test. |
| `--mixed` | Run both chaotic and realistic tests. |
| `--and`, `--or`, `--not`, ... | Run homogeneous gate chain tests. |
| `--dump` | Dump output to timestamped file in `test_result/`. |
| `--plot` | Generate performance scaling plots. |
| `--perf-size`, `--perf-pass`, `--perf-fifo` | Synchronize with hardware `perf` profiler via named pipe FIFO. |

### 8.3 Execution Examples
```bash
# Run chaotic fragmentation cache cliff test
python tests/cache_test.py --chaotic --dump

# Run realistic layout test with plots
python tests/cache_test.py --realistic --plot

# Test homogeneous XOR gate chain
python tests/cache_test.py --xor --dump
```

---

## 9. `cache_perf.py` — Hardware Cache Profiler (Linux `perf`)

### 9.1 Purpose & Methodology
**File:** [`tests/cache_perf.py`](file:///home/farhan/Github/darion-logic-sim/tests/cache_perf.py)  
**Platform:** Linux only (requires `perf` and FIFO support).  
**Purpose:** Instruments the CPU hardware performance monitoring unit (PMU) during cache tests to measure exact hardware metrics across circuit sizes from 100 to 1,000,000 gates.

**Hardware Events Monitored:**
- `L1-dcache-loads` & `L1-dcache-load-misses` (L1 data cache miss rate)
- `l2_cache_req_stat.ic_dc_miss_in_l2` (L2 cache misses)
- `cache-misses` (Last Level L3/LLC cache misses)
- `ex_ret_brn` & `ex_ret_brn_misp` (Branch instructions & mispredictions)
- `instructions` & `cycles` (Instructions Per Cycle — IPC)

Profiles four distinct execution paths: OOP, Unoptimized Propagate, Optimized Propagate, and Linear Sweep.

### 9.2 Execution Examples
```bash
# Profile chaotic layout hardware counters
python tests/cache_perf.py --chaotic

# Profile homogeneous AND chains with plots
python tests/cache_perf.py --and --plot
```

---

## 10. `perf.py` — Multi-Engine Hardware Event Profiler

### 10.1 Purpose & Methodology
**File:** [`tests/perf.py`](file:///home/farhan/Github/darion-logic-sim/tests/perf.py)  
**Platform:** Linux only.  
**Purpose:** Multi-engine hardware PMU profiler comparing Engine, Reactor Propagate, Reactor Sweep, Reactor OOP, Icarus Verilog, and Verilator on ISCAS-85 circuits.

Generates comprehensive Markdown tables detailing IPC, branch mispredictions, L1/L2 hit rates, and RAM traffic per circuit.

### 10.2 Execution Examples
```bash
# Profile all ISCAS-85 circuits (5,000 vectors each)
python tests/perf.py --vectors 5000

# Profile specific circuit
python tests/perf.py --vectors 5000 --filter c7552
```

---

## 11. `ic_circuit_benchmark.py` — IC Packaging & Serialization Benchmark

### 11.1 Purpose & Methodology
**File:** [`tests/ic_circuit_benchmark.py`](file:///home/farhan/Github/darion-logic-sim/tests/ic_circuit_benchmark.py)  
**Purpose:** Tests the Integrated Circuit (IC) modular packaging subsystem, JSON serialization, and deep nesting stability across both Python Engine and Cython Reactor backends.

**Test Phases:**
1. **Complex IC Benchmark:** Measures creation, JSON save, JSON load, and simulation performance across sizes from 10 to 150,000 gates.
2. **Complex Circuit Benchmark:** Evaluates raw circuits combining mixed subcircuits (NOT chains, AND pyramids, XOR parity trees).
3. **Nested IC Stress Test:** Packages circuits up to 10 IC hierarchy levels deep to verify boundary pin resolution and memory stability under deep nesting.

### 11.2 Execution Example
```bash
python tests/ic_circuit_benchmark.py
```

---

## 12. `integrity_test.py` — Master Integrity & Stress Test Suite

### 12.1 Purpose & Methodology
**File:** [`tests/integrity_test.py`](file:///home/farhan/Github/darion-logic-sim/tests/integrity_test.py)  
**Purpose:** The master unit and system testing suite (~5,100 lines). Exercises every engine feature across thousands of rigorous assertions.

**Test Categories:**
1. **Unit Tests:** Individual gate primitives, truth tables, and boundary pin states.
2. **Truth Table Exhaustion:** Exhaustive $2^N$ input combinations for multi-input subcircuits.
3. **Deep Chains & Fan-Outs:** Pathological chain propagation and massive fan-out stress tests.
4. **Event Manager:** Full Undo/Redo command stack verification.
5. **IC Packaging:** I/O pin mapping, nested components, and serialization integrity.
6. **Topological Optimization:** Validates that `optimize()` preserves exact functional semantics.
7. **Real-World Complex Systems:** 4-bit ALUs, Ripple Carry Adders, Ring Oscillators, and Glitch Counters.

### 12.2 Command-Line Options
```text
usage: integrity_test.py [-h] [--engine] [--optimize]
```

| Flag | Description |
|------|-------------|
| `--engine` | Test pure Python Engine (default is Cython Reactor). |
| `--optimize` | Run all test circuits through `circuit.optimize()` prior to asserting correctness. |

### 12.3 Execution Example
```bash
# Run master integrity suite on Reactor backend
python tests/integrity_test.py

# Run with topological optimization enabled
python tests/integrity_test.py --optimize

# Run on Python Engine backend
python tests/integrity_test.py --engine
```

---

## 13. `iscas89_sequential_harness.py` — Sequential Verilog Harness Engine

### 13.1 Purpose & Architecture
**File:** [`tests/iscas89_sequential_harness.py`](file:///home/farhan/Github/darion-logic-sim/tests/iscas89_sequential_harness.py)  
**Purpose:** Reusable harness module for generating timing-instrumented Icarus Verilog testbenches and Verilator C++ wrappers for sequential circuits.

**Features:**
- Injects a standard DFF model (`always @(posedge clk) Q <= D;`) if the netlist does not define one.
- Drives two-phase clock sequences (`setup @ CLK=0`, `trigger @ CLK=1`).
- Integrates the custom C VPI timer (`vpi_timer.vpi`) to bypass file I/O overhead.
- Generates Verilator C++ testbench harnesses and builds native cycle-accurate simulation binaries.

Can be imported programmatically or run as a standalone timing tool:
```python
from iscas89_sequential_harness import run_icarus_harness_89, run_verilator_harness_89
result_i = run_icarus_harness_89('tests/ISCAS89/s27.v', vectors=5000, warmup=500)
result_v = run_verilator_harness_89('tests/ISCAS89/s27.v', vectors=5000, warmup=500)
```

---

## 14. `bash_test.sh` — Automated Pipeline Runner

### 14.1 Purpose & Execution
**File:** [`bash_test.sh`](file:///home/farhan/Github/darion-logic-sim/bash_test.sh)  
**Purpose:** Top-level batch script executing the full end-to-end benchmark and profiling pipeline across all combinational and sequential benchmark suites.

**Contents & Pipeline Workflow:**
```bash
# 1. RAM Footprint Tests
python tests/load.py tests/ISCAS85 --dump 
python tests/load.py tests/EPFL_parsed --dump
python tests/load.py tests/EPFL_large_parsed --dump
python tests/load.py tests/EPFL_mammoth_parsed --dump

# 2. Combinational Simulation Benchmarks
python tests/benchmark.py tests/ISCAS85 --optimize --vector 50000 --warmup 10 --dump 
python tests/benchmark.py tests/EPFL_parsed --optimize --vector 50000 --warmup 10 --dump 
python tests/benchmark.py tests/EPFL_large_parsed --optimize --vector 500 --warmup 10 --no-engine --dump 
python tests/benchmark.py tests/EPFL_mammoth_parsed --optimize --vector 50 --warmup 10 --no-engine --dump 

# 3. Sequential Simulation Benchmarks
python tests/benchmark_89.py tests/ISCAS89 --optimize --vector 50000 --warmup 10 --dump 

# 4. Topological Geometry Analysis
python tests/geometry.py tests/ISCAS85 --dump
python tests/geometry.py tests/ISCAS89 --dump
python tests/geometry.py tests/EPFL_parsed --dump
python tests/geometry.py tests/EPFL_large_parsed --dump
python tests/geometry.py tests/EPFL_mammoth_parsed --dump
```

To run the full suite:
```bash
bash bash_test.sh
```

---

## 15. Summary Table & Cheat Sheet

| Script | Primary Question / Goal | Backends Evaluated | Datasets Supported | Key Flags |
|---|---|---|---|---|
| [`benchmark.py`](file:///home/farhan/Github/darion-logic-sim/tests/benchmark.py) | How fast is raw combinational simulation vs. Icarus & Verilator? | Engine, Rx-Prop, Rx-Sweep, Rx-OOP, Icarus, Verilator | ISCAS-85, EPFL (std/large/mammoth) | `--optimize`, `--vectors`, `--warmup`, `--dump`, `--no-engine` |
| [`benchmark_89.py`](file:///home/farhan/Github/darion-logic-sim/tests/benchmark_89.py) | How fast is clocked sequential simulation with DFF feedback? | Engine, Rx-Prop, Rx-Sweep, Rx-OOP, Icarus, Verilator | ISCAS-89 (`.v`, `.json`) | `--optimize`, `--vectors`, `--warmup`, `--dump` |
| [`load.py`](file:///home/farhan/Github/darion-logic-sim/tests/load.py) | What is the true RAM footprint (RSS in MB) of loading circuits? | Engine, Reactor, Icarus, Verilator | Any `.v` or `.json` (Comb & Seq) | `--dump`, `--json`, `--no-engine` |
| [`geometry.py`](file:///home/farhan/Github/darion-logic-sim/tests/geometry.py) | What are the physical memory hop distances & cache locality profiles? | Cython Reactor | Any `.v` or `.json` (Comb & Seq) | `--dump`, `--plot` |
| [`verifier.py`](file:///home/farhan/Github/darion-logic-sim/tests/verifier.py) | Do combinational outputs match bit-for-bit across all engines? | 6 backends | ISCAS-85, EPFL (`.v`) | `--vectors`, `--seed`, `--output`, `--dump` |
| [`verifier_89.py`](file:///home/farhan/Github/darion-logic-sim/tests/verifier_89.py) | Do sequential DFF outputs match bit-for-bit across all engines? | 6 backends | ISCAS-89 (`.v`, `.json`) | `--vectors`, `--seed`, `--output`, `--dump` |
| [`cache_test.py`](file:///home/farhan/Github/darion-logic-sim/tests/cache_test.py) | Where are the CPU cache cliffs (L1/L2/L3), and how much does `optimize()` help? | Reactor, Engine, Rx-OOP | Synthetic chains (100–2M gates) | `--chaotic`, `--realistic`, `--and`, `--plot`, `--dump` |
| [`cache_perf.py`](file:///home/farhan/Github/darion-logic-sim/tests/cache_perf.py) | What are the hardware PMU cache miss rates & IPC across circuit scales? | OOP, Unopt, Opt, Sweep | Synthetic chains | `--chaotic`, `--realistic`, `--plot` (Linux only) |
| [`perf.py`](file:///home/farhan/Github/darion-logic-sim/tests/perf.py) | What are the hardware PMU cache miss rates & IPC on real circuits? | 6 backends | ISCAS-85 | `--vectors`, `--filter`, `--limit` (Linux only) |
| [`ic_circuit_benchmark.py`](file:///home/farhan/Github/darion-logic-sim/tests/ic_circuit_benchmark.py) | Does IC packaging and JSON serialization scale to deep hierarchies? | Engine, Reactor | Synthetic ICs & nested chains | Standalone script |
| [`integrity_test.py`](file:///home/farhan/Github/darion-logic-sim/tests/integrity_test.py) | Is every single engine feature, gate, undo/redo, and truth table 100% correct? | Engine, Reactor | Full unit/functional test suite | `--engine`, `--optimize` |
| [`bash_test.sh`](file:///home/farhan/Github/darion-logic-sim/bash_test.sh) | How do I run all RAM, simulation, and geometry benchmarks in batch? | Orchestrator | All benchmark suites | Standalone shell script |
