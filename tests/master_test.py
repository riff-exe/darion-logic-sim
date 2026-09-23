"""
master_test.py
==============
Master Unified 3-in-1 Benchmark Harness for Darion Logic Sim.

Integrates three comprehensive testing dimensions into a single unified pipeline:
  Phase 1: Zero-Testbench Load & Memory Benchmark (Timeline & RAM Footprint)
           - Measures pure circuit parsing/load time (ms) and topological optimization time (ms).
           - Measures baseline process RSS (MB), net circuit RAM (MB), and peak process memory (VmHWM).
  Phase 2: Correctness & Bit-Exact Verification
           - Executes cross-engine simulation against golden reference model (Icarus / Verilator).
           - Verifies 100% bit-exact equivalence of output signals across test vectors.
           - Emits PASS / FAIL diagnostic summary with pinpoint mismatch tracking.
  Phase 3: High-Performance Simulation & Hardware PMU Profiling
           - Executes timed simulation loops to record runtime (ms), vectors/sec, and Mega-Evals/sec (MEPS).
           - Simultaneously traces hardware performance counters via Linux perf kernel PMU:
             * Instructions per cycle (IPC)
             * CPU cycles and retired instructions
             * L1 data cache loads & L1 cache misses
             * L2 cache loads & L2 cache misses
             * L3 / LLC cache misses (DRAM access)
             * Branch instructions & branch mispredictions
           - Quantifies speedup and hardware metrics of topologically optimized layout vs. OOP graph engines.

Supported Benchmark Datasets:
  - IWLS 2005: itc99, opencores, faraday
  - ISCAS-85: Combinational circuits
  - ISCAS-89: Sequential circuits with DFF feedback
  - EPFL: Standard, Large, Mammoth combinational benchmarks
"""

import os
import sys
import re
import glob
import time
import json
import datetime
import argparse
import math
import subprocess
import shutil
import atexit

_FILE_REALPATH = os.path.realpath(os.path.abspath(__file__))
_SCRIPT_DIR   = os.path.dirname(_FILE_REALPATH)
_SRC_DIR      = os.path.join(_SCRIPT_DIR, "src")
_PROJECT_ROOT = os.path.dirname(_SCRIPT_DIR)
_TESTS_DIR    = _SCRIPT_DIR

sys.path.insert(0, _SCRIPT_DIR)
sys.path.insert(0, _SRC_DIR)
sys.path.insert(0, _PROJECT_ROOT)

from pmu_harness import pmu_harness, PmuStats

def _find_script(name: str) -> str:
    for d in (_SRC_DIR, _SCRIPT_DIR):
        p = os.path.join(d, name)
        if os.path.exists(p):
            return p
    return os.path.join(_SRC_DIR, name)

SUITE_ALIASES = {
    "iwls": os.path.join(_SCRIPT_DIR, "IWLS2005", "itc99"),
    "itc99": os.path.join(_SCRIPT_DIR, "IWLS2005", "itc99"),
    "opencores": os.path.join(_SCRIPT_DIR, "IWLS2005", "opencores"),
    "faraday": os.path.join(_SCRIPT_DIR, "IWLS2005", "faraday"),
    "iscas85": os.path.join(_SCRIPT_DIR, "ISCAS85"),
    "iscas89": os.path.join(_SCRIPT_DIR, "ISCAS89"),
    "epfl": os.path.join(_SCRIPT_DIR, "EPFL_parsed"),
    "epfl_large": os.path.join(_SCRIPT_DIR, "EPFL_large_parsed"),
    "epfl_mammoth": os.path.join(_SCRIPT_DIR, "EPFL_mammoth_parsed"),
}

EVENTS = pmu_harness.get_event_string()

def fmt_num(n):
    if n is None or (isinstance(n, float) and math.isnan(n)): return "N/A"
    if n >= 1e9: return f"{n/1e9:.2f}B"
    if n >= 1e6: return f"{n/1e6:.2f}M"
    if n >= 1e3: return f"{n/1e3:.2f}K"
    if isinstance(n, float): return f"{n:.2f}"
    return str(n)

def fmt_pct(pct):
    if pct is None or (isinstance(pct, float) and math.isnan(pct)): return "N/A"
    sign = "+" if pct > 0 else ""
    return f"{sign}{pct:.1f}%"

def geo_mean(values):
    valid = [v for v in values if v is not None and v > 0 and not math.isnan(v)]
    if not valid: return 0.0
    return math.exp(sum(math.log(v) for v in valid) / len(valid))

def classify_circuit(path: str) -> str:
    """Returns 'iwls', 'iscas89', or 'combinational'."""
    p_lower = path.lower()
    if "iwls" in p_lower or "gsclib" in p_lower or "/itc99" in p_lower or "/opencores" in p_lower or "/faraday" in p_lower:
        return "iwls"
    if "iscas89" in p_lower or re.search(r'/s\d+\.v$', path):
        return "iscas89"
    # Content inspection
    if os.path.isfile(path):
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(8192)
            if re.search(r'\b(AND2X1|INVX1|BUFX1|DFFSRX1|DFFX1|NOR2X1|NAND2X1|AOI21X1|OAI21X1|MX2X1|XOR2X1|TLATX1)\b', content):
                return "iwls"
            if re.search(r'\b(dff|DFF)\b', content):
                return "iscas89"
        except Exception:
            pass
    return "combinational"

def discover_circuits(target_arg: str, filter_str: str = "", limit: int = None):
    raw_target = SUITE_ALIASES.get(target_arg.lower().strip(), target_arg)
    if not os.path.exists(raw_target):
        if os.path.exists(os.path.join(_TESTS_DIR, raw_target)):
            raw_target = os.path.join(_TESTS_DIR, raw_target)
        elif os.path.exists(os.path.join(_PROJECT_ROOT, raw_target)):
            raw_target = os.path.join(_PROJECT_ROOT, raw_target)

    if os.path.isfile(raw_target):
        files = [os.path.abspath(raw_target)]
    elif os.path.isdir(raw_target):
        files = sorted(
            [
                os.path.abspath(f) for f in glob.glob(os.path.join(raw_target, "*.v"))
                if not f.endswith("_tb.v") and not f.endswith("_helper.v") and "GSCLib" not in f
            ],
            key=lambda x: os.path.getsize(x)
        )
        if not files:
            files = sorted(
                [
                    os.path.abspath(f) for f in glob.glob(os.path.join(raw_target, "**", "*.v"), recursive=True)
                    if not f.endswith("_tb.v") and not f.endswith("_helper.v") and "GSCLib" not in f
                ],
                key=lambda x: os.path.getsize(x)
            )
    else:
        files = sorted(
            [
                os.path.abspath(f) for f in glob.glob(raw_target)
                if not f.endswith("_tb.v") and not f.endswith("_helper.v") and "GSCLib" not in f
            ],
            key=lambda x: os.path.getsize(x)
        )
    
    # Exclude c17 upfront
    circuits = [c for c in files if "c17" not in os.path.basename(c)]
    if filter_str:
        circuits = [c for c in circuits if filter_str in os.path.basename(c)]
    if limit is not None:
        circuits = circuits[:limit]
    return circuits


# ===========================================================================
# ARTIFACT CLEANUP AND PURGE UTILITIES
# ===========================================================================
_KEEP_ARTIFACTS = False

def cleanup_circuit_artifacts(c_path: str):
    """
    Cleans all temporary simulation, compilation, and hardware profiling artifacts
    associated with a specific circuit file across circuit directories and root.
    """
    if not c_path:
        return
    c_dir = os.path.dirname(os.path.abspath(c_path))
    c_file = os.path.basename(c_path)
    c_base, _ = os.path.splitext(c_file)

    # 1. Circuit directory temporary files and folders
    circuit_dir_patterns = [
        os.path.join(c_dir, f"{c_base}*_obj_dir"),
        os.path.join(c_dir, f"{c_base}*_main.cpp"),
        os.path.join(c_dir, f"{c_base}*_vectors.txt"),
        os.path.join(c_dir, f"{c_base}*_tb.v"),
        os.path.join(c_dir, f"{c_base}*.vvp"),
        os.path.join(c_dir, f"{c_base}*.tmp.json"),
        os.path.join(c_dir, f"{c_file}*.tmp.json"),
    ]
    for pat in circuit_dir_patterns:
        for item in glob.glob(pat):
            # Guard against deleting real source netlists or JSON files
            if item.endswith(".v") and not (item.endswith("_tb.v") or item.endswith("_helper.v")):
                continue
            if item.endswith(".json") and not item.endswith(".tmp.json"):
                continue
            try:
                if os.path.isdir(item):
                    shutil.rmtree(item, ignore_errors=True)
                else:
                    os.remove(item)
            except Exception:
                pass

    # 2. CWD / Project root hardware perf profiling artifacts
    for root_dir in (_PROJECT_ROOT, os.getcwd()):
        perf_patterns = [
            os.path.join(root_dir, f"perf_*{c_file}*"),
            os.path.join(root_dir, f"perf_*{c_base}*"),
        ]
        for pat in perf_patterns:
            for item in glob.glob(pat):
                try:
                    if os.path.isdir(item):
                        shutil.rmtree(item, ignore_errors=True)
                    else:
                        os.remove(item)
                except Exception:
                    pass


def cleanup_global_artifacts():
    """
    Performs a full sweep across the project root and benchmark directories
    to remove any orphaned hardware profiler files, FIFOs, and compile artifacts.
    """
    # 1. Remove orphaned perf data and text files in project root & CWD
    for root_dir in (_PROJECT_ROOT, os.getcwd()):
        for pat in ["perf_*.data*", "perf_*.txt"]:
            for item in glob.glob(os.path.join(root_dir, pat)):
                try:
                    if os.path.isfile(item):
                        os.remove(item)
                except Exception:
                    pass

    # 2. Remove FIFO if leftover
    fifo = "/tmp/rx_perf_ctrl"
    if os.path.exists(fifo):
        try: os.remove(fifo)
        except Exception: pass

    # 3. Sweep circuit suite directories for leftover compile/harness artifacts
    suite_dirs = [
        os.path.join(_TESTS_DIR, "IWLS2005"),
        os.path.join(_TESTS_DIR, "ISCAS85"),
        os.path.join(_TESTS_DIR, "ISCAS89"),
        os.path.join(_TESTS_DIR, "EPFL_parsed"),
        os.path.join(_TESTS_DIR, "EPFL_large_parsed"),
        os.path.join(_TESTS_DIR, "EPFL_mammoth_parsed"),
    ]
    for sdir in suite_dirs:
        if not os.path.exists(sdir):
            continue
        for pat in ("**/*_obj_dir", "**/*_main.cpp", "**/*_vectors.txt", "**/*_tb.v", "**/*.vvp", "**/*.tmp.json"):
            for item in glob.glob(os.path.join(sdir, pat), recursive=True):
                if item.endswith(".v") and not (item.endswith("_tb.v") or item.endswith("_helper.v")):
                    continue
                if item.endswith(".json") and not item.endswith(".tmp.json"):
                    continue
                try:
                    if os.path.isdir(item):
                        shutil.rmtree(item, ignore_errors=True)
                    else:
                        os.remove(item)
                except Exception:
                    pass


def _atexit_cleanup():
    global _KEEP_ARTIFACTS
    if not _KEEP_ARTIFACTS:
        cleanup_global_artifacts()

atexit.register(_atexit_cleanup)


# ===========================================================================
# PHASE 1: ZERO-TESTBENCH LOAD & MEMORY BENCHMARK
# ===========================================================================
def run_phase1_load(c_path: str, engine: bool = True, rx_prop: bool = True, rx_sweep: bool = True,
                    icarus: bool = True, verilator: bool = True) -> dict:
    load_script = _find_script("load.py")
    cmd = [sys.executable, load_script, c_path, "--json"]
    if not engine:
        cmd.append("--no-engine")
    if not rx_prop:
        cmd.append("--no-rx-prop")
    if not rx_sweep:
        cmd.append("--no-rx-sweep")
    if not icarus:
        cmd.append("--no-icarus")
    if not verilator:
        cmd.append("--no-verilator")

    try:
        res = subprocess.run(cmd, capture_output=True, text=True)
        out = res.stdout.strip()
        # Find JSON block
        json_start = out.find("[")
        if json_start != -1:
            data = json.loads(out[json_start:])
            if data and isinstance(data, list):
                return data[0]
        # Fallback if dictionary
        json_start = out.find("{")
        if json_start != -1:
            return json.loads(out[json_start:])
    except Exception as e:
        return {"error": str(e)}
    return {"error": "Failed to parse load.py output"}


# ===========================================================================
# PHASE 2: CORRECTNESS & STATE VERIFICATION
# ===========================================================================
def run_phase2_verification(c_path: str, c_type: str, verify_vectors: int,
                            engine: bool = True, rx_prop: bool = True, rx_sweep: bool = True,
                            rx_oop: bool = True, icarus: bool = True, verilator: bool = True,
                            raw: bool = False) -> dict:
    if c_type == "iwls":
        script = _find_script("verifier_iwls.py")
    elif c_type == "iscas89":
        script = _find_script("verifier_89.py")
    else:
        script = _find_script("verifier.py")

    cmd = [sys.executable, script, c_path, "--vectors", str(verify_vectors), "--json"]
    if raw:
        cmd.append("--raw")
    if not engine:
        cmd.append("--no-engine")
    if not rx_prop:
        cmd.append("--no-rx-prop")
    if not rx_sweep:
        cmd.append("--no-rx-sweep")
    if not rx_oop:
        cmd.append("--no-rx-oop")
    if not icarus:
        cmd.append("--no-icarus")
    if not verilator:
        cmd.append("--no-verilator")

    try:
        res = subprocess.run(cmd, capture_output=True, text=True)
        out = res.stdout.strip()
        json_start = out.find("[")
        if json_start != -1:
            data = json.loads(out[json_start:])
            if data and isinstance(data, list):
                item = data[0]
                if "status" in item:
                    is_pass = (item.get("status") == "PASS")
                    total_vecs = item.get("total_vectors", verify_vectors)
                    mismatches = item.get("fail_count", 0)
                    engines = item.get("engines", {})
                    ref_src = item.get("ref_source", "Icarus/Golden")
                elif "summary" in item:
                    summary = item["summary"]
                    is_pass = bool(summary.get("pass", False))
                    total_vecs = summary.get("total_vectors", summary.get("total_cycles", verify_vectors))
                    mismatches = summary.get("mismatches", 0)
                    engines = summary.get("engines", {})
                    ref_src = summary.get("ref_source", "Golden")
                else:
                    is_pass = bool(item.get("pass", False))
                    total_vecs = item.get("total_vectors", verify_vectors)
                    mismatches = item.get("mismatches", 0)
                    engines = item.get("engines", {})
                    ref_src = "Golden"

                return {
                    "pass": is_pass,
                    "total_vectors": total_vecs,
                    "mismatches": mismatches,
                    "engines": engines,
                    "ref_source": ref_src
                }
    except Exception as e:
        return {"pass": False, "error": str(e)}
    return {"pass": False, "error": "Failed to parse verifier output"}


# ===========================================================================
# PHASE 3: SIMULATION & HARDWARE PMU PROFILING
# ===========================================================================
def run_phase3_simulation_and_perf(c_path: str, c_type: str, vectors: int, warmup: int,
                                   engine: bool = True, rx_prop: bool = True, rx_sweep: bool = True,
                                   rx_oop: bool = True, icarus: bool = True, verilator: bool = True,
                                   skip_perf: bool = False, raw: bool = False) -> dict:
    c_name = os.path.basename(c_path)
    if c_type == "iwls":
        bench_script = _find_script("benchmark_iwls.py")
    elif c_type == "iscas89":
        bench_script = _find_script("benchmark_89.py")
    else:
        bench_script = _find_script("benchmark.py")

    # Prepare Linux perf FIFO
    if not skip_perf and sys.platform == "linux":
        fifo_path = "/tmp/rx_perf_ctrl"
        if os.path.exists(fifo_path):
            try: os.remove(fifo_path)
            except Exception: pass
        try:
            os.mkfifo(fifo_path)
        except Exception:
            pass

    cmd_record = [
        sys.executable, bench_script, c_path,
        "--vectors", str(vectors), "--warmup", str(warmup),
        "--json"
    ]
    if raw:
        cmd_record.append("--raw")
    else:
        cmd_record.append("--optimize")
    if not skip_perf and sys.platform == "linux":
        cmd_record.extend(["--perf", "--perf-events", EVENTS])
    if not engine:
        cmd_record.append("--no-engine")
    if not rx_prop:
        cmd_record.append("--no-rx-prop")
    if not rx_sweep:
        cmd_record.append("--no-rx-sweep")
    if not rx_oop:
        cmd_record.append("--no-rx-oop")
    if not icarus:
        cmd_record.append("--no-icarus")
    if not verilator:
        cmd_record.append("--no-verilator")

    sim_raw = {}
    try:
        res = subprocess.run(cmd_record, capture_output=True, text=True)
        out = res.stdout.strip()
        
        json_start_dict = out.find("{")
        json_start_list = out.find("[")
        json_start = -1
        if json_start_dict != -1 and json_start_list != -1:
            json_start = min(json_start_dict, json_start_list)
        elif json_start_dict != -1:
            json_start = json_start_dict
        elif json_start_list != -1:
            json_start = json_start_list

        if json_start != -1:
            payload = json.loads(out[json_start:])
            if isinstance(payload, dict) and "circuits" in payload:
                sim_raw = payload["circuits"][0] if payload["circuits"] else {}
            elif isinstance(payload, list) and len(payload) > 0:
                sim_raw = payload[0]
            elif isinstance(payload, dict):
                sim_raw = payload
        else:
            sim_raw = {"error": res.stderr.strip() or f"Benchmark worker failed with exit code {res.returncode}"}
    except Exception as e:
        sim_raw = {"error": str(e)}

    # Parse hardware perf counter reports
    perf_metrics = {}
    if not skip_perf and sys.platform == "linux":
        report_files = {
            "prop": f"perf_reactor_prop_{c_name}.txt",
            "oop": f"perf_reactor_oop_prop_{c_name}.txt",
            "sweep": f"perf_reactor_sweep_{c_name}.txt",
            "engine": f"perf_engine_prop_{c_name}.txt",
            "icarus": f"perf_icarus_{c_name}.txt",
            "verilator": f"perf_verilator_{c_name}.txt"
        }
        if not os.path.exists(report_files["prop"]) and os.path.exists(f"perf_reactor_prop_opt_{c_name}.txt"):
            report_files["prop"] = f"perf_reactor_prop_opt_{c_name}.txt"
        for eng, rep_file in report_files.items():
            if os.path.exists(rep_file):
                st = pmu_harness.parse_report_file(rep_file)
                try: os.remove(rep_file)
                except Exception: pass

                if st.instructions > 0 or st.cycles > 0:
                    perf_metrics[eng] = st

    return {"sim": sim_raw, "perf": perf_metrics}


# ===========================================================================
# MAIN ORCHESTRATOR & REPORT GENERATOR
# ===========================================================================
def main():
    parser = argparse.ArgumentParser(
        description="Master Unified 3-in-1 Benchmark Harness (Load, Verification & Hardware Profiling)"
    )
    parser.add_argument("target", nargs="?", default="tests/IWLS2005/itc99",
                        help="Suite alias (iwls, iscas85, iscas89, epfl, etc.), file, or directory")
    parser.add_argument("--vectors", type=int, default=50000,
                        help="Test vectors for simulation benchmarking (default: 10000)")
    parser.add_argument("--verify-vectors", type=int, default=100,
                        help="Vectors for correctness verification (default: 100)")
    parser.add_argument("--warmup", type=int, default=10,
                        help="Untimed warmup cycles (default: 10)")
    parser.add_argument("--filter", type=str, default="",
                        help="Filter circuits by substring")
    parser.add_argument("--limit", type=int, default=None,
                        help="Maximum circuits to benchmark")
    parser.add_argument("--all-engines", action="store_true", default=True,
                        help="Benchmark all engines (default: True)")
    parser.add_argument("--no-engine", dest="engine", action="store_false", default=True,
                        help="Disable Pure Python Engine benchmark")
    parser.add_argument("--no-rx-prop", dest="rx_prop", action="store_false", default=True,
                        help="Disable Reactor BFS propagate benchmark")
    parser.add_argument("--no-rx-sweep", dest="rx_sweep", action="store_false", default=True,
                        help="Disable Reactor linear sweep benchmark")
    parser.add_argument("--no-rx-oop", "--no-reactor-oop", dest="rx_oop", action="store_false", default=True,
                        help="Disable Reactor OOP benchmark")
    parser.add_argument("--no-icarus", dest="icarus", action="store_false", default=True,
                        help="Disable Icarus Verilog benchmark")
    parser.add_argument("--no-verilator", dest="verilator", action="store_false", default=True,
                        help="Disable Verilator C++ benchmark")
    parser.add_argument("--skip-load", action="store_true",
                        help="Skip Phase 1 load & memory benchmark")
    parser.add_argument("--skip-verify", action="store_true",
                        help="Skip Phase 2 state verification")
    parser.add_argument("--skip-perf", action="store_true",
                        help="Run Phase 3 simulation without Linux perf counters")
    parser.add_argument("--raw", action="store_true",
                        help="Disable topological optimization (use raw netlist order)")
    parser.add_argument("--no-dump", action="store_true",
                        help="Do not write Markdown/JSON reports to disk")
    parser.add_argument("--json", action="store_true",
                        help="Output final results as raw JSON to stdout")
    parser.add_argument("--dump-json", action="store_true",
                        help="Save raw JSON results to disk (default: False)")
    parser.add_argument("--keep-artifacts", action="store_true", default=False,
                        help="Retain intermediate compilation and profiling artifacts on disk (default: False)")

    args = parser.parse_args()

    global _KEEP_ARTIFACTS
    _KEEP_ARTIFACTS = args.keep_artifacts

    if not args.keep_artifacts:
        cleanup_global_artifacts()

    circuits = discover_circuits(args.target, args.filter, args.limit)
    if not circuits:
        print(f"[-] Error: No netlists found matching target '{args.target}'")
        sys.exit(1)

    suite_name = args.target if not os.path.isfile(args.target) else os.path.basename(args.target)
    if not args.json:
        print("=" * 120)
        print("  DARION LOGIC SIM — MASTER UNIFIED 3-IN-1 BENCHMARK HARNESS")
        print(f"  Target Suite   : {suite_name} ({len(circuits)} circuits discovered)")
        print(f"  Vectors        : {args.vectors:,} (Sim Benchmarking) | {args.verify_vectors:,} (Verification)")
        print(f"  Linux perf PMU : {'Enabled' if not args.skip_perf and sys.platform == 'linux' else 'Disabled/Skipped'}")
        print("=" * 120)

    # Master results repository: circuit -> data
    results = {}

    for idx, c_path in enumerate(circuits, 1):
        c_name = os.path.basename(c_path)
        c_type = classify_circuit(c_path)
        c_size_kb = os.path.getsize(c_path) / 1024.0

        if not args.json:
            print(f"\n[{idx}/{len(circuits)}] Running Unified Benchmark for {c_name} ({c_size_kb:.1f} KB, type: {c_type})...")

        if not args.keep_artifacts:
            cleanup_circuit_artifacts(c_path)

        c_data = {
            "circuit": c_name,
            "path": c_path,
            "type": c_type,
            "size_kb": c_size_kb,
            "phase1_load": None,
            "phase2_verify": None,
            "phase3_sim_perf": None
        }

        try:
            # --- PHASE 1 ---
            if not args.skip_load:
                if not args.json:
                    print("  -> Phase 1: Zero-Testbench Load & Memory Benchmark...", end="", flush=True)
                t0 = time.perf_counter()
                p1 = run_phase1_load(
                    c_path,
                    engine=args.engine,
                    rx_prop=args.rx_prop,
                    rx_sweep=args.rx_sweep,
                    icarus=args.icarus,
                    verilator=args.verilator
                )
                t_el = (time.perf_counter() - t0) * 1000
                c_data["phase1_load"] = p1
                if not args.json:
                    rx = p1.get("reactor", {})
                    circ_mb = rx.get("circ_mb", 0.0)
                    peak_mb = rx.get("peak_mb", 0.0)
                    load_ms = rx.get("load_ms", 0.0)
                    opt_ms = rx.get("opt_ms", 0.0)
                    gates = p1.get("gates", rx.get("gates", "N/A"))
                    print(f" Done ({t_el:.1f}ms) | Gates: {gates} | RAM: {circ_mb:.2f}MB (Peak: {peak_mb:.1f}MB) | Load: {load_ms:.2f}ms | Opt: {opt_ms:.2f}ms")

            # --- PHASE 2 ---
            if not args.skip_verify:
                if not args.json:
                    print("  -> Phase 2: Functional Correctness & Bit-Exact Verification...", end="", flush=True)
                t0 = time.perf_counter()
                p2 = run_phase2_verification(
                    c_path, c_type, args.verify_vectors,
                    engine=args.engine,
                    rx_prop=args.rx_prop,
                    rx_sweep=args.rx_sweep,
                    rx_oop=args.rx_oop,
                    icarus=args.icarus,
                    verilator=args.verilator,
                    raw=args.raw
                )
                t_el = (time.perf_counter() - t0) * 1000
                c_data["phase2_verify"] = p2
                if not args.json:
                    status_str = "PASS" if p2.get("pass") else "FAIL"
                    vecs = p2.get("total_vectors", args.verify_vectors)
                    mism = p2.get("mismatches", 0)
                    print(f" Done ({t_el:.1f}ms) | Status: {status_str} (Mismatches: {mism} / {vecs} vectors)")

            # --- PHASE 3 ---
            if not args.json:
                print("  -> Phase 3: High-Performance Simulation & Hardware Profiling...", end="", flush=True)
            t0 = time.perf_counter()
            p3 = run_phase3_simulation_and_perf(
                c_path, c_type, args.vectors, args.warmup,
                engine=args.engine,
                rx_prop=args.rx_prop,
                rx_sweep=args.rx_sweep,
                rx_oop=args.rx_oop,
                icarus=args.icarus,
                verilator=args.verilator,
                skip_perf=args.skip_perf,
                raw=args.raw
            )
            t_el = (time.perf_counter() - t0) * 1000
            c_data["phase3_sim_perf"] = p3
            if not args.json:
                perf = p3.get("perf", {})
                rx_p = perf.get("prop", perf.get("prop_opt", perf.get("sweep", perf.get("oop", perf.get("engine", {})))))
                ipc = rx_p.get("ipc", 0.0)
                l1_ld = rx_p.get("l1_loads", rx_p.get("l1_load", 0))
                l1_ms = rx_p.get("l1_misses", rx_p.get("l1_miss", 0))
                cyc = rx_p.get("cyc", 0)
                print(f" Done ({t_el:.1f}ms) | IPC: {ipc:.2f} | Cycles: {fmt_num(cyc)} | L1 Load: {fmt_num(l1_ld)} | L1 Miss: {fmt_num(l1_ms)}")

            results[c_name] = c_data
        finally:
            if not args.keep_artifacts:
                cleanup_circuit_artifacts(c_path)

    # --- REPORT GENERATION ---
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = os.path.join(_TESTS_DIR, "test_result", "master_test")
    os.makedirs(out_dir, exist_ok=True)
    md_file = os.path.join(out_dir, f"master_test_report_{ts}.md")
    json_file = os.path.join(out_dir, f"master_test_report_{ts}.json")

    # Build Markdown document
    md = []
    md.append(f"# Master Test Unified Benchmark Report: {suite_name}\n")
    md.append(f"**Execution Parameters:**")
    md.append(f"- **Target Suite / Path:** `{args.target}`")
    md.append(f"- **Circuits Benchmarked:** {len(circuits)}")
    md.append(f"- **Simulation Vectors (Phase 3):** {args.vectors:,} (Warmup: {args.warmup})")
    md.append(f"- **Verification Vectors (Phase 2):** {args.verify_vectors:,}")
    md.append(f"- **Hardware Profiler:** Linux `perf` kernel PMU counters\n")
    md.append("---\n")

    # TABLE 1: Zero-Testbench Memory Footprint (Phase 1)
    if not args.skip_load:
        md.append("## 1. Zero-Testbench Memory Footprint (Phase 1)\n")
        md.append("| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |")
        md.append("|:---|---:|---:|---:|---:|---:|")
        for c_name, data in results.items():
            p1 = data.get("phase1_load")
            if not p1 or "error" in p1:
                md.append(f"| {c_name} | N/A | N/A | N/A | N/A | N/A |")
                continue
            raw_gates = p1.get("gates", "N/A")
            gates_str = f"{raw_gates:,}" if isinstance(raw_gates, int) else str(raw_gates)

            def fmt_mem_cell(d, is_enabled=True):
                if not is_enabled or (d and d.get("error") == "disabled"):
                    return "N/A"
                if not d or "error" in d:
                    return "N/A"
                circ = d.get("circ_mb", 0.0)
                peak = d.get("peak_mb", 0.0)
                if peak > 0:
                    return f"{circ:.2f} MB ({peak:.1f} MB peak)"
                return f"{circ:.2f} MB"

            rx_str = fmt_mem_cell(p1.get("reactor"), args.rx_prop or args.rx_sweep)
            py_str = fmt_mem_cell(p1.get("engine"), args.engine)
            ic_str = fmt_mem_cell(p1.get("icarus"), args.icarus)
            vr_str = fmt_mem_cell(p1.get("verilator"), args.verilator)
            md.append(f"| {c_name} | {gates_str} | {rx_str} | {py_str} | {ic_str} | {vr_str} |")
        md.append("\n---\n")

    # TABLE 2: Zero-Testbench Load & Compilation Times (Phase 1)
    if not args.skip_load:
        md.append("## 2. Zero-Testbench Load & Compilation Times (Phase 1)\n")
        md.append("| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |")
        md.append("|:---|---:|---:|---:|---:|---:|")
        for c_name, data in results.items():
            p1 = data.get("phase1_load")
            if not p1 or "error" in p1:
                md.append(f"| {c_name} | N/A | N/A | N/A | N/A | N/A |")
                continue
            raw_gates = p1.get("gates", "N/A")
            gates_str = f"{raw_gates:,}" if isinstance(raw_gates, int) else str(raw_gates)

            def fmt_load_cell(d, is_enabled=True, is_reactor=False):
                if not is_enabled or (d and d.get("error") == "disabled"):
                    return "N/A"
                if not d or "error" in d:
                    return "N/A"
                l_ms = d.get("load_ms", 0.0)
                if is_reactor:
                    opt_ms = d.get("opt_ms", 0.0)
                    if opt_ms > 0:
                        return f"{l_ms:.2f} ms ({opt_ms:.3f} ms opt)"
                    return f"{l_ms:.2f} ms"
                if l_ms >= 1000.0:
                    return f"{l_ms / 1000.0:.2f} s"
                return f"{l_ms:.2f} ms"

            rx_load = fmt_load_cell(p1.get("reactor"), args.rx_prop or args.rx_sweep, is_reactor=True)
            py_load = fmt_load_cell(p1.get("engine"), args.engine)
            ic_load = fmt_load_cell(p1.get("icarus"), args.icarus)
            vr_load = fmt_load_cell(p1.get("verilator"), args.verilator)
            md.append(f"| {c_name} | {gates_str} | {rx_load} | {py_load} | {ic_load} | {vr_load} |")
        md.append("\n---\n")

    # OPTIONAL: Functional State Verification (Phase 2)
    if not args.skip_verify:
        md.append("## Functional State Verification (Phase 2)\n")
        md.append("| Circuit | Verification Status | Checked Vectors | Mismatches | Reference Golden Model |")
        md.append("|:---|:---:|---:|---:|:---|")
        for c_name, data in results.items():
            p2 = data.get("phase2_verify")
            if not p2:
                md.append(f"| {c_name} | SKIPPED | - | - | - |")
                continue
            status_md = "**PASS**" if p2.get("pass") else "<span style='color:red;'>FAIL</span>"
            vecs = p2.get("total_vectors", args.verify_vectors)
            mism = p2.get("mismatches", 0)
            ref = p2.get("ref_source", "Golden")
            md.append(f"| {c_name} | {status_md} | {vecs:,} | {mism} | {ref} |")
        md.append("\n---\n")

    # TABLE 3: High-Throughput Simulation Performance (Phase 3)
    md.append("## 3. High-Throughput Simulation Performance (Phase 3)\n")
    md.append("### Simulation Wall-Clock Time (ms)\n")
    md.append("| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |")
    md.append("|:---|---:|---:|---:|---:|---:|---:|")

    speedup_rows = []
    geo_prop_spds = []
    geo_sweep_spds = []
    geo_oop_spds = []
    geo_eng_spds = []
    geo_ver_spds = []
    rx_vs_py_spds = []
    sw_vs_py_spds = []
    sw_vs_prop_spds = []
    suite_has_icarus = False

    for c_name, data in results.items():
        p3 = data.get("phase3_sim_perf", {})
        sim = p3.get("sim", {})
        
        r_prop = sim.get("r_res", sim.get("reactor", sim.get("r_opt_res", sim.get("reactor_opt", {}))))
        ro = sim.get("ro_res", sim.get("reactor_oop", {}))
        eng = sim.get("e_res", sim.get("engine", {}))
        ic = sim.get("i_res", sim.get("icarus", {}))
        ver = sim.get("v_res", sim.get("verilator", {}))

        target_vecs = max(args.vectors - args.warmup, 1)

        def get_norm_time(res, is_enabled=True, key="time_ms"):
            if not is_enabled or not res or "error" in res or (key == "sweep_ms" and "sweep_error" in res):
                return 0.0
            t_ms = res.get(key, res.get("propagate_ms", 0.0) if key == "time_ms" else 0.0)
            if t_ms <= 0:
                return 0.0
            m_vecs = res.get("logical_vectors", res.get("logical_count", res.get("measured_vectors", 0)))
            p_vecs = res.get("physical_vectors", 0)
            if p_vecs > 0 and m_vecs == p_vecs and p_vecs == 2 * target_vecs:
                m_vecs = target_vecs
            if m_vecs > 0 and target_vecs > 0 and m_vecs != target_vecs:
                return (t_ms / m_vecs) * target_vecs
            return t_ms

        p_ms  = get_norm_time(r_prop, args.rx_prop)
        sw_ms = get_norm_time(r_prop, args.rx_sweep, key="sweep_ms")
        ro_ms = get_norm_time(ro, args.rx_oop)
        e_ms  = get_norm_time(eng, args.engine)
        i_ms  = get_norm_time(ic, args.icarus)
        v_ms  = get_norm_time(ver, args.verilator)

        if i_ms > 0:
            suite_has_icarus = True

        def fmt_sim_time(ms):
            if ms <= 0: return "N/A"
            if ms >= 10000.0:
                return f"{ms / 1000.0:.2f} s"
            return f"{ms:.2f} ms"

        md.append(f"| {c_name} | {fmt_sim_time(p_ms)} | {fmt_sim_time(sw_ms)} | {fmt_sim_time(ro_ms)} | {fmt_sim_time(e_ms)} | {fmt_sim_time(i_ms)} | {fmt_sim_time(v_ms)} |")

        # Baseline: Icarus if available, else rx-prop
        base_ms = i_ms if i_ms > 0 else p_ms
        base_name = "Icarus" if i_ms > 0 else "rx-prop"

        def get_spd(target_ms):
            if base_ms > 0 and target_ms > 0:
                return base_ms / target_ms
            return None

        p_spd = get_spd(p_ms)
        sw_spd = get_spd(sw_ms)
        ro_spd = get_spd(ro_ms)
        e_spd = get_spd(e_ms)
        v_spd = get_spd(v_ms)

        if p_spd and base_name != "rx-prop": geo_prop_spds.append(p_spd)
        if sw_spd: geo_sweep_spds.append(sw_spd)
        if ro_spd: geo_oop_spds.append(ro_spd)
        if e_spd: geo_eng_spds.append(e_spd)
        if v_spd: geo_ver_spds.append(v_spd)

        if p_ms > 0 and e_ms > 0: rx_vs_py_spds.append(e_ms / p_ms)
        if sw_ms > 0 and e_ms > 0: sw_vs_py_spds.append(e_ms / sw_ms)
        if p_ms > 0 and sw_ms > 0: sw_vs_prop_spds.append(p_ms / sw_ms)

        def fmt_spd(s):
            if s is not None: return f"{s:.2f}x"
            return "N/A"

        ic_spd_str = "1.00x" if (base_name == "Icarus" and i_ms > 0) else (fmt_spd(get_spd(i_ms)) if i_ms > 0 else "N/A")
        prop_spd_str = "1.00x" if (base_name == "rx-prop" and p_ms > 0) else fmt_spd(p_spd)

        speedup_rows.append((
            c_name,
            prop_spd_str,
            fmt_spd(sw_spd),
            fmt_spd(ro_spd),
            fmt_spd(e_spd),
            ic_spd_str,
            fmt_spd(v_spd)
        ))

    base_label = "Icarus" if suite_has_icarus else "rx-prop"
    md.append(f"\n### Speedup Analysis (vs Baseline: {base_label} = 1.00x)\n")
    md.append("| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |")
    md.append("|:---|---:|---:|---:|---:|---:|---:|")
    for r in speedup_rows:
        md.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[6]} |")

    # Geo-mean Speedup Highlights
    md.append(f"\n### Geo-Mean Speedup Highlights (Baseline: {base_label} = 1.00x)\n")
    if geo_prop_spds and base_label != "rx-prop":
        md.append(f"- **rx-prop (Wavefront BFS):** `{geo_mean(geo_prop_spds):.2f}x`")
    elif base_label == "rx-prop":
        md.append(f"- **rx-prop (Wavefront BFS):** `1.00x (Baseline)`")
    if geo_sweep_spds:
        md.append(f"- **rx-sweep (Linear Compiled):** `{geo_mean(geo_sweep_spds):.2f}x`")
    if geo_oop_spds:
        md.append(f"- **rx-oop (OOP Graph):** `{geo_mean(geo_oop_spds):.2f}x`")
    if geo_eng_spds:
        md.append(f"- **Pure Python Engine:** `{geo_mean(geo_eng_spds):.2f}x`")
    if suite_has_icarus:
        md.append(f"- **Icarus Verilog:** `1.00x (Baseline)`")
    if geo_ver_spds:
        md.append(f"- **Verilator C++:** `{geo_mean(geo_ver_spds):.2f}x`")

    cross_lines = []
    if rx_vs_py_spds:
        cross_lines.append(f"- **Cython Reactor (`rx-prop`) vs Pure Python:** `{geo_mean(rx_vs_py_spds):.2f}x` faster")
    if sw_vs_py_spds:
        cross_lines.append(f"- **Cython Reactor (`rx-sweep`) vs Pure Python:** `{geo_mean(sw_vs_py_spds):.2f}x` faster")
    if sw_vs_prop_spds:
        r_sw_prop = geo_mean(sw_vs_prop_spds)
        cross_lines.append(f"- **Reactor Sweep vs Propagate Ratio:** `{r_sw_prop:.2f}x` ({'sweep faster' if r_sw_prop > 1 else 'propagate faster'})")

    if cross_lines:
        md.append("\n### Cross-Engine Comparisons\n")
        md.extend(cross_lines)

    md.append("\n---\n")

    # TABLE 4: Hardware PMU & Cache Hierarchy Profiling (Phase 3)
    md.append("## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)\n")
    pmu_hdr, pmu_sep = PmuStats.get_table_header(["Circuit", "Engine Variant"])
    md.append(pmu_hdr)
    md.append(pmu_sep)
    for c_name, data in results.items():
        p3 = data.get("phase3_sim_perf", {})
        perf = p3.get("perf", {})
        if not perf:
            continue
        order = [
            ("rx-prop", "prop"),
            ("rx-sweep (Linear)", "sweep"),
            ("rx-oop (OOP Engine)", "oop"),
            ("Pure Python Engine", "engine"),
            ("Icarus Verilog", "icarus"),
            ("Verilator C++", "verilator"),
        ]
        for label, k in order:
            s = perf.get(k)
            if not s and k == "prop":
                s = perf.get("prop_opt")
            if s:
                if isinstance(s, PmuStats):
                    md.append(s.format_row([c_name, label], fmt_num))
                else:
                    inst_val = s.get("instructions", s.get("inst", 0))
                    cyc_val = s.get("cycles", s.get("cyc", 0))
                    ipc_val = s.get("ipc", 0.0)
                    l1_load_val = s.get("l1_loads", s.get("l1_load", 0))
                    l1_miss_val = s.get("l1_misses", s.get("l1_miss", 0))
                    l2_load_val = s.get("l2_loads", s.get("l2_load", 0))
                    l2_miss_val = s.get("l2_misses", s.get("l2_miss", 0))
                    l3_load_val = s.get("l3_loads", s.get("l3_load", 0))
                    dram_val = s.get("dram_loads", s.get("l3_miss", 0))
                    brn_val = s.get("branches", s.get("brn", 0))
                    brn_miss_val = s.get("branch_misses", s.get("brn_miss", 0))

                    md.append(
                        f"| {c_name} | {label} | {fmt_num(inst_val)} | {fmt_num(cyc_val)} | {ipc_val:.2f} | "
                        f"{fmt_num(l1_load_val)} | {fmt_num(l1_miss_val)} | {fmt_num(l2_load_val)} | {fmt_num(l2_miss_val)} | "
                        f"{fmt_num(l3_load_val)} | {fmt_num(dram_val)} | "
                        f"{fmt_num(brn_val)} | {fmt_num(brn_miss_val)} |"
                    )

    # Save Markdown (and JSON only if requested)
    if not args.no_dump:
        with open(md_file, "w", encoding="utf-8") as f:
            f.write("\n".join(md) + "\n")
        if args.dump_json or args.json:
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, default=lambda o: o.to_dict() if hasattr(o, "to_dict") else o.__dict__)

    if args.json:
        print(json.dumps(results, indent=2, default=lambda o: o.to_dict() if hasattr(o, "to_dict") else o.__dict__))
    else:
        print("\n" + "\n".join(md))
        if not args.no_dump:
            print(f"\n[+] Master test markdown report written to: {md_file}")
            if args.dump_json or args.json:
                print(f"[+] Master test raw JSON data written to: {json_file}")

    if not args.keep_artifacts:
        cleanup_global_artifacts()


if __name__ == "__main__":
    main()
