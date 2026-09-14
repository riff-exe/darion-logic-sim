import os
import sys
import subprocess
import glob
import re
import datetime
import argparse
import math

if sys.platform != "linux":
    print("Error: Hardware profiling ('perf' and FIFOs) is Linux-exclusive. Aborting.")
    sys.exit(0)

_SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
_TESTS_DIR    = os.path.dirname(_SCRIPT_DIR)
_PROJECT_ROOT = os.path.dirname(_TESTS_DIR)

parser = argparse.ArgumentParser(description="Multi-engine hardware profiling")
parser.add_argument("target", nargs="?", default="iwls", help="Circuit file, directory or suite name (default: iwls)")
parser.add_argument("--vectors", type=int, default=5000, help="Number of test vectors (default: 5000)")
parser.add_argument("--filter", type=str, default="", help="Filter circuits by name (e.g., 'b01', 'c432')")
parser.add_argument("--limit", type=int, default=None, help="Limit number of circuits tested")
parser.add_argument("--raw", action="store_true", help="Disable topological optimization (use raw netlist order)")
parser.add_argument("--all-engines", action="store_true", default=True, help="Profile all engines (default: True)")
parser.add_argument("--no-engine", dest="engine", action="store_false", default=True, help="Disable Engine")
parser.add_argument("--no-rx-prop", dest="rx_prop", action="store_false", default=True, help="Disable Rx-prop")
parser.add_argument("--no-rx-sweep", dest="rx_sweep", action="store_false", default=True, help="Disable Rx-sweep")
parser.add_argument("--no-rx-oop", "--no-reactor-oop", dest="rx_oop", action="store_false", default=True, help="Disable Rx-oop")
parser.add_argument("--no-icarus", dest="icarus", action="store_false", default=True, help="Disable Icarus")
parser.add_argument("--no-verilator", dest="verilator", action="store_false", default=True, help="Disable Verilator")
args = parser.parse_args()

SUITE_ALIASES = {
    "iwls": os.path.join(_TESTS_DIR, "IWLS2005", "itc99"),
    "itc99": os.path.join(_TESTS_DIR, "IWLS2005", "itc99"),
    "opencores": os.path.join(_TESTS_DIR, "IWLS2005", "opencores"),
    "faraday": os.path.join(_TESTS_DIR, "IWLS2005", "faraday"),
    "iscas85": os.path.join(_TESTS_DIR, "ISCAS85"),
    "iscas89": os.path.join(_TESTS_DIR, "ISCAS89"),
    "epfl": os.path.join(_TESTS_DIR, "EPFL_parsed"),
    "epfl_large": os.path.join(_TESTS_DIR, "EPFL_large_parsed"),
    "epfl_mammoth": os.path.join(_TESTS_DIR, "EPFL_mammoth_parsed"),
}
target_arg = SUITE_ALIASES.get(args.target.lower().strip(), args.target)
if not os.path.exists(target_arg):
    if os.path.exists(os.path.join(_TESTS_DIR, target_arg)):
        target_arg = os.path.join(_TESTS_DIR, target_arg)
    elif os.path.exists(os.path.join(_PROJECT_ROOT, target_arg)):
        target_arg = os.path.join(_PROJECT_ROOT, target_arg)

if os.path.isfile(target_arg):
    all_circuits = [target_arg]
elif os.path.isdir(target_arg):
    all_circuits = sorted(
        [
            f for f in glob.glob(os.path.join(target_arg, "*.v"))
            if not f.endswith("_tb.v") and not f.endswith("_helper.v") and "GSCLib" not in f
        ],
        key=lambda x: os.path.getsize(x)
    )
    if not all_circuits:
        all_circuits = sorted(
            [
                f for f in glob.glob(os.path.join(target_arg, "**", "*.v"), recursive=True)
                if not f.endswith("_tb.v") and not f.endswith("_helper.v") and "GSCLib" not in f
            ],
            key=lambda x: os.path.getsize(x)
        )
else:
    all_circuits = sorted(
        [
            f for f in glob.glob(target_arg)
            if not f.endswith("_tb.v") and not f.endswith("_helper.v") and "GSCLib" not in f
        ],
        key=lambda x: os.path.getsize(x)
    )

# Exclude c17 upfront because it has negligible runtime and is not a valid benchmark
CIRCUITS = [c for c in all_circuits if "c17" not in os.path.basename(c)]
if args.filter:
    CIRCUITS = [c for c in CIRCUITS if args.filter in os.path.basename(c)]
if args.limit is not None:
    CIRCUITS = CIRCUITS[:args.limit]

EVENTS = "L1-dcache-loads:u,L1-dcache-load-misses:u,l2_cache_req_stat.ic_dc_miss_in_l2:u,cache-misses:u,ex_ret_brn:u,ex_ret_brn_misp:u,instructions:u,cycles:u"
VECTORS = args.vectors

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
perf_dir = os.path.join(_TESTS_DIR, "test_result", "perf")
os.makedirs(perf_dir, exist_ok=True)
REPORT_FILE = os.path.join(perf_dir, f"perf_report_{ts}.md")

def fmt(n):
    if n >= 1e9: return f"{n/1e9:.2f}B"
    if n >= 1e6: return f"{n/1e6:.2f}M"
    if n >= 1e3: return f"{n/1e3:.2f}K"
    return str(n)

def fmt_diff(pct):
    sign = "+" if pct > 0 else ""
    return f"{sign}{pct:.1f}%"

def geo_mean(values):
    valid = [v for v in values if v > 0]
    if not valid: return 0.0
    return math.exp(sum(math.log(v) for v in valid) / len(valid))

suite_desc = target_arg if not os.path.isfile(target_arg) else os.path.basename(target_arg)
print(f"Collecting hardware profiling for {len(CIRCUITS)} circuits ({VECTORS:,} vectors) from {suite_desc}...\n")

# Raw metrics per circuit: circuit -> engine -> metric_dict
circuit_metrics = {}

for c_path in CIRCUITS:
    c_name = os.path.basename(c_path)
    print(f"Profiling {c_name}...")
    circuit_metrics[c_name] = {}
    
    fifo_path = "/tmp/rx_perf_ctrl"
    if os.path.exists(fifo_path):
        try: os.remove(fifo_path)
        except: pass
    os.mkfifo(fifo_path)
    
    # Determine appropriate benchmark runner script
    if "IWLS" in c_path or "GSCLib" in c_path or "/itc99" in c_path or "/opencores" in c_path or "/faraday" in c_path:
        bench_script = os.path.join(_SCRIPT_DIR, "benchmark_iwls.py")
    elif "ISCAS89" in c_path or re.search(r'/s\d+\.v$', c_path):
        bench_script = os.path.join(_SCRIPT_DIR, "benchmark_89.py")
    else:
        bench_script = os.path.join(_SCRIPT_DIR, "benchmark.py")

    cmd_record = [
        "taskset", "-c", "2",
        sys.executable, bench_script, c_path,
        "--vectors", str(VECTORS), "--warmup", "10", "--json",
        "--perf", "--perf-events", EVENTS
    ]
    if args.raw:
        cmd_record.append("--raw")
    if not args.engine:
        cmd_record.append("--no-engine")
    if not args.rx_prop:
        cmd_record.append("--no-rx-prop")
    if not args.rx_sweep:
        cmd_record.append("--no-rx-sweep")
    if not args.rx_oop:
        cmd_record.append("--no-rx-oop")
    if not args.icarus:
        cmd_record.append("--no-icarus")
    if not args.verilator:
        cmd_record.append("--no-verilator")

    subprocess.run(cmd_record, capture_output=True)
    
    # Parse individual reports
    report_files = {
        "prop": f"perf_reactor_prop_{c_name}.txt",
        "oop": f"perf_reactor_oop_prop_{c_name}.txt",
        "sweep": f"perf_reactor_sweep_{c_name}.txt",
        "engine": f"perf_engine_prop_{c_name}.txt",
        "icarus": f"perf_icarus_{c_name}.txt",
        "verilator": f"perf_verilator_{c_name}.txt"
    }

    raw_stats = {}
    for eng, rep_file in report_files.items():
        raw_stats[eng] = {}
        if os.path.exists(rep_file):
            with open(rep_file, "r", encoding="utf-8") as f:
                current_event = None
                for line in f:
                    m_event = re.search(r"# Samples: .* of event '(.*?)'", line)
                    if m_event:
                        current_event = m_event.group(1)
                        continue
                    m_total = re.search(r"# Event count \(approx\.\):\s+(\d+)", line)
                    if m_total and current_event:
                        raw_stats[eng][current_event] = int(m_total.group(1))
            for p in (rep_file, rep_file.replace(".txt", ".data"), rep_file.replace(".txt", ".data.old")):
                if os.path.exists(p):
                    try: os.remove(p)
                    except Exception: pass

    for eng, stats in raw_stats.items():
        if not stats:
            continue
        def get_count(evt):
            return stats.get(evt, 0)

        l1_load = get_count("L1-dcache-loads:u") or get_count("L1-dcache-loads")
        l1_miss = get_count("L1-dcache-load-misses:u") or get_count("L1-dcache-load-misses")
        l2_miss = get_count("l2_cache_req_stat.ic_dc_miss_in_l2:u") or get_count("l2_cache_req_stat.ic_dc_miss_in_l2")
        l3_miss = get_count("cache-misses:u") or get_count("cache-misses")
        brn = get_count("ex_ret_brn:u")
        brn_miss = get_count("ex_ret_brn_misp:u")
        inst = get_count("instructions:u") or get_count("instructions")
        cyc = get_count("cycles:u") or get_count("cycles")

        l1_hit = max(0, l1_load - l1_miss)
        l2_hit = max(0, l1_miss - l2_miss)
        l3_hit = max(0, l2_miss - l3_miss)

        ipc = (inst / cyc) if cyc > 0 else 0.0
        brn_hr = ((brn - brn_miss) / brn * 100) if brn > 0 else 0.0
        l1_hr = (l1_hit / l1_load * 100) if l1_load > 0 else 0.0
        l2_hr = (l2_hit / l1_miss * 100) if l1_miss > 0 else 0.0
        l3_hr = (l3_hit / l2_miss * 100) if l2_miss > 0 else 0.0

        circuit_metrics[c_name][eng] = {
            "ipc": ipc,
            "inst": inst,
            "cyc": cyc,
            "l1_load": l1_load,
            "l1_miss": l1_miss,
            "l1_hr": l1_hr,
            "l2_miss": l2_miss,
            "l2_hr": l2_hr,
            "l3_miss": l3_miss,
            "l3_hr": l3_hr,
            "brn": brn,
            "brn_miss": brn_miss,
            "brn_hr": brn_hr
        }

# --- GENERATE COMPARISON REPORT ---
engine_display_names = {
    "prop":       "rx-prop",
    "oop":        "rx-oop (OOP Engine)",
    "sweep":      "rx-sweep (Linear)",
    "engine":     "Pure Python Engine",
    "icarus":     "Icarus Verilog",
    "verilator":  "Verilator C++"
}

# Tables formatting
c_w = max(10, max((len(c) for c in circuit_metrics.keys()), default=10))

side_header = f"| {'Circuit':<{c_w}} | {'Variant':<22} | {'IPC':>5} | {'Cycles':>9} | {'Instructions':>13} | {'L1 Loads':>10} | {'L1 Hit%':>8} | {'Brn Miss%':>10} |"
side_div    = f"|{'-'*(c_w+2)}|{'-'*24}|{'-'*7}|{'-'*11}|{'-'*15}|{'-'*12}|{'-'*10}|{'-'*12}|"

delta_header = f"| {'Circuit':<{c_w}} | {'Cycles rx-prop vs OOP':<22} | {'Inst rx-prop vs OOP':<20} | {'L1 Load Delta':<14} | {'IPC vs OOP':<11} |"
delta_div    = f"|{'-'*(c_w+2)}|{'-'*24}|{'-'*22}|{'-'*16}|{'-'*13}|"

side_rows = []
delta_rows = []

opt_oop_speedups = []
inst_reductions = []
l1_reductions = []

for c_name, engs in circuit_metrics.items():
    has_prop = "prop" in engs
    has_oop = "oop" in engs

    first_eng = True
    for eng_key in ["prop", "sweep", "oop", "engine", "icarus"]:
        if eng_key in engs:
            m = engs[eng_key]
            disp = engine_display_names[eng_key]
            circ_label = c_name if first_eng else ""
            first_eng = False
            brn_misp_pct = (100.0 - m["brn_hr"]) if m["brn"] > 0 else 0.0
            side_rows.append(
                f"| {circ_label:<{c_w}} | {disp:<22} | {m['ipc']:>5.2f} | {fmt(m['cyc']):>9} | {fmt(m['inst']):>13} | {fmt(m['l1_load']):>10} | {m['l1_hr']:>7.2f}% | {brn_misp_pct:>9.2f}% |"
            )

    if has_prop and has_oop:
        p = engs["prop"]
        oop = engs["oop"]
        cyc_prop = p["cyc"]
        cyc_oop = oop["cyc"]
        oop_spd = (cyc_oop / cyc_prop) if cyc_prop > 0 else 1.0
        oop_cyc_diff = ((cyc_prop - cyc_oop) / cyc_oop * 100) if cyc_oop > 0 else 0.0
        opt_oop_speedups.append(oop_spd)

        inst_p = p["inst"]
        inst_oop = oop["inst"]
        inst_diff = ((inst_p - inst_oop) / inst_oop * 100) if inst_oop > 0 else 0.0
        inst_reductions.append(-inst_diff)

        l1_p = p["l1_load"]
        l1_oop = oop["l1_load"]
        l1_diff = ((l1_p - l1_oop) / l1_oop * 100) if l1_oop > 0 else 0.0
        l1_reductions.append(-l1_diff)

        ipc_oop = oop["ipc"]
        ipc_p = p["ipc"]
        ipc_diff = ((ipc_p - ipc_oop) / ipc_oop * 100) if ipc_oop > 0 else 0.0

        c_oop_str = f"{fmt_diff(oop_cyc_diff)} ({oop_spd:.2f}x spd)"
        delta_rows.append(
            f"| {c_name:<{c_w}} | {c_oop_str:<22} | {fmt_diff(inst_diff):<20} | {fmt_diff(l1_diff):<14} | {fmt_diff(ipc_diff):<11} |"
        )

# Print Summary to Terminal
print("\n" + "="*80)
print(f"  HARDWARE PERFORMANCE PROFILING: rx-prop vs rx-oop ({suite_desc})")
print("="*80)
print(side_header)
print(side_div)
for r in side_rows:
    print(r)
print("\n" + "="*80)
print("  HARDWARE DELTAS & SPEEDUPS (Cycles, Instructions, Cache)")
print("="*80)
print(delta_header)
print(delta_div)
for r in delta_rows:
    print(r)

if opt_oop_speedups:
    print("\n" + "-"*80)
    print(f"  Geo-Mean CPU Cycle Speedup (rx-prop vs rx-oop): {geo_mean(opt_oop_speedups):.2f}x")
    if inst_reductions:
        print(f"  Average Instruction Reduction vs OOP:      {sum(inst_reductions)/len(inst_reductions):.1f}%")
    if l1_reductions:
        print(f"  Average L1 Data Cache Load Delta vs OOP:   {sum(l1_reductions)/len(l1_reductions):.1f}%")
    print("-"*80 + "\n")

# Write Markdown Report
suite_title = target_arg if not os.path.isfile(target_arg) else os.path.basename(target_arg)
with open(REPORT_FILE, "w") as f:
    f.write(f"# Hardware Profiling: `rx-prop` vs `rx-oop` ({suite_title})\n\n")
    f.write(f"**Test Parameters:**\n- **Target Suite:** `{suite_title}`\n- **Vectors simulated:** {VECTORS:,}\n- **Hardware Profiler:** Linux `perf` via kernel performance counters\n\n")
    f.write("Profiling isolates the computational core of simulation engines (excluding Python bytecode compilation and harness setup).\n\n")

    f.write("## 1. Side-by-Side Hardware Counter Comparison\n\n")
    f.write(side_header + "\n")
    f.write(side_div + "\n")
    for r in side_rows:
        f.write(r + "\n")
    f.write("\n")

    f.write("## 2. Hardware Improvement & Delta Analysis\n\n")
    f.write(delta_header + "\n")
    f.write(delta_div + "\n")
    for r in delta_rows:
        f.write(r + "\n")
    f.write("\n")

    if opt_oop_speedups:
        f.write("### Aggregate Hardware Highlights\n\n")
        f.write(f"- **Geo-Mean CPU Cycle Speedup (`rx-prop` vs `rx-oop`):** `{geo_mean(opt_oop_speedups):.2f}x`\n")
        if inst_reductions:
            f.write(f"- **Average Instruction Reduction vs OOP:** `{sum(inst_reductions)/len(inst_reductions):.1f}%` fewer instructions executed\n")
        if l1_reductions:
            f.write(f"- **Average L1 Cache Load Delta vs OOP:** `{sum(l1_reductions)/len(l1_reductions):.1f}%` L1 data cache memory references\n")
        f.write("\n")

    # Detailed tables for engines that have data
    f.write("## 3. Detailed Cache Hierarchy & Branch Profiling\n\n")
    det_header = f"| {'Circuit':<{c_w}} | {'IPC':>5} | {'Branch':>9} | {'Brn Miss':>9} | {'L1 Load':>10} | {'L1 Hit%':>8} | {'L2 Load':>9} | {'L2 Hit%':>8} | {'L3/RAM Load':>12} |"
    det_div    = f"|{'-'*(c_w+2)}|{'-'*7}|{'-'*11}|{'-'*11}|{'-'*12}|{'-'*10}|{'-'*11}|{'-'*10}|{'-'*14}|"

    engines_to_detail = [
        ("prop",       "Reactor: `rx-prop` (Wavefront BFS)"),
        ("oop",        "Reactor OOP: `rx-oop` (Object Graph)"),
        ("sweep",      "Reactor: `rx-sweep` (Linear Compiled)"),
        ("engine",     "Pure Python Engine"),
        ("icarus",     "Icarus Verilog (`vvp`)")
    ]

    for eng_key, title in engines_to_detail:
        has_any = any(eng_key in circuit_metrics[c] for c in circuit_metrics)
        if not has_any:
            continue
        f.write(f"### {title}\n\n")
        f.write(det_header + "\n")
        f.write(det_div + "\n")
        for c_name, engs in circuit_metrics.items():
            if eng_key in engs:
                m = engs[eng_key]
                row = f"| {c_name:<{c_w}} | {m['ipc']:>5.2f} | {fmt(m['brn']):>9} | {fmt(m['brn_miss']):>9} | {fmt(m['l1_load']):>10} | {m['l1_hr']:>7.2f}% | {fmt(m['l1_miss']):>9} | {m['l2_hr']:>7.2f}% | {fmt(m['l2_miss']):>12} |"
                f.write(row + "\n")
        f.write("\n")

print(f"[+] Multi-engine report generated and saved to {REPORT_FILE}")

