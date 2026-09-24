import os
import sys
import subprocess
import argparse
import datetime
import json

if sys.platform != "linux":
    print("Error: Profiling tools ('perf' and FIFOs) are Linux-exclusive. Aborting.")
    sys.exit(0)

# Ensure tests/ directory is in path so pmu_harness is discoverable
_TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
if _TESTS_DIR not in sys.path:
    sys.path.insert(0, _TESTS_DIR)

from pmu_harness import pmu_harness, PmuStats

def main():
    parser = argparse.ArgumentParser(description="Cache Performance Scaling Profiler")
    parser.add_argument('--chaotic', action='store_true', help='Run mixed chaotic test')
    parser.add_argument('--realistic', action='store_true', help='Run mixed realistic test')
    parser.add_argument('--and', dest='gate_and', action='store_true', help='Run homogeneous AND test')
    parser.add_argument('--or', dest='gate_or', action='store_true', help='Run homogeneous OR test')
    parser.add_argument('--not', dest='gate_not', action='store_true', help='Run homogeneous NOT test')
    parser.add_argument('--plot', action='store_true', help='Generate both logarithmic and linear plots')
    parser.add_argument('--plot-log', action='store_true', help='Generate logarithmic plot')
    parser.add_argument('--plot-linear', action='store_true', help='Generate linear plot')
    parser.add_argument('--min-size', type=int, default=100, help='Minimum circuit size (default: 100)')
    parser.add_argument('--max-size', type=int, default=50000, help='Maximum circuit size (default: 50000)')
    parser.add_argument('--step', type=float, default=1.15, help='Circuit size step increment (default: 200)')
    
    args, unknown = parser.parse_known_args()
    
    test_args = []
    mode_name = "chaotic"
    if args.realistic: 
        test_args.append('--realistic')
        mode_name = "realistic"
    elif args.gate_and:
        test_args.append('--and')
        mode_name = "homogeneous_and"
    elif args.gate_or:
        test_args.append('--or')
        mode_name = "homogeneous_or"
    elif args.gate_not:
        test_args.append('--not')
        mode_name = "homogeneous_not"
    else:
        test_args.append('--chaotic')

    fifo_path = "/tmp/cache_perf_ctrl"
    if os.path.exists(fifo_path):
        try: os.remove(fifo_path)
        except: pass
    os.mkfifo(fifo_path)

    events = pmu_harness.get_event_string()

    sizes = []
    current_size = args.min_size
    while current_size <= args.max_size:
        sizes.append(current_size)
        current_size = int(current_size * args.step)
        
    data = {
        "oop": [],
        "unopt": [],
        "opt": [],
        "sweep": []
    }

    print(f"Starting cache performance profiling ({mode_name})... Microarchitecture: {pmu_harness.model_name}")
    print(f"Tracing PMU events: {events}")
    
    for s in sizes:
        print(f"Profiling size {s:<9,} ... ", end="", flush=True)
        shared_iters = None
        for pass_name in ["oop", "unopt", "opt", "sweep"]:
            pass_args = test_args + ["--reactor_oop"] if pass_name == "oop" else test_args
            extra_args = ["--perf-iters", str(int(shared_iters))] if shared_iters is not None else []
            cmd = [
                "perf", "stat", "-D", "-1", f"--control=fifo:{fifo_path}", "-e", events, "-x,",
                "--", sys.executable, "tests/cache_test.py", *pass_args, "--perf-size", str(s), "--perf-pass", pass_name, "--perf-fifo", fifo_path, *extra_args
            ]
            res = subprocess.run(cmd, capture_output=True, text=True)
            stats = pmu_harness.parse_stat_csv(res.stderr)
            
            for line in res.stderr.split("\n"):
                if line.startswith("ITERATIONS:"):
                    stats.iterations = float(line.split(":")[1].strip())
                    if shared_iters is None:
                        shared_iters = stats.iterations
                elif line.startswith("TIME_MS:"):
                    stats.time_ms = float(line.split(":")[1].strip())
                elif line.startswith("EVAL_COUNT:"):
                    stats.evals = float(line.split(":")[1].strip())

            if stats.instructions == 0:
                print(f"\nERROR: `perf stat` returned '<not counted>' for size {s} {pass_name}. This usually happens if another `perf` instance is running in parallel and monopolizing the hardware PMU counters. Please ensure no other profilers are running.")
                sys.exit(1)

            data[pass_name].append(stats)
        print("Done")

    if os.path.exists(fifo_path):
        os.remove(fifo_path)

    os.makedirs("tests/test_result/perf", exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    json_file = f"tests/test_result/perf/cache_perf_{mode_name}_{ts}.json"
    report_file = f"tests/test_result/perf/cache_perf_{mode_name}_{ts}.md"

    # 1. Export structured benchmark data to JSON
    json_doc = {
        "metadata": {
            "timestamp": ts,
            "mode": mode_name,
            "cpu_model": pmu_harness.model_name,
            "pmu_events": events,
            "sizes": sizes,
            "engines": ["oop", "unopt", "opt", "sweep"]
        },
        "data": {
            k: [st.to_dict() for st in v] for k, v in data.items()
        }
    }
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(json_doc, f, indent=2)
    print(f"\nRaw benchmark data saved to {json_file}")

    # 2. Generate Streamlined 4-Phase Markdown Report
    with open(report_file, "w") as f:
        f.write(f"# Cache Fragmentation Profile ({mode_name.upper()})\n\n")
        f.write("Isolated purely via hardware `perf` boundaries tightly hugging the core `batch_toggle` simulation logic.\n")
        f.write(f"CPU: {pmu_harness.model_name} | PMU Events: `{events}`\n\n")
        
        def fmt(n):
            if n is None: return "N/A"
            if n >= 1e9: return f"{n/1e9:.2f}B"
            if n >= 1e6: return f"{n/1e6:.2f}M"
            if n >= 1e3: return f"{n/1e3:.2f}K"
            return f"{n:.2f}" if isinstance(n, float) else str(n)

        engine_map = [
            ("OOP", "oop"),
            ("Unopt BFS", "unopt"),
            ("Opt BFS", "opt"),
            ("Linear Sweep", "sweep"),
        ]

        # Phase 1: Core Performance (Instructions, Cycles, IPC)
        f.write("## Phase 1: Core Performance (Instructions, Cycles, IPC)\n")
        f.write("| Size | Engine Variant | Instructions | Cycles | IPC |\n")
        f.write("| :--- | :--- | ---: | ---: | ---: |\n")
        for i, s in enumerate(sizes):
            for eng_disp, eng_key in engine_map:
                st: PmuStats = data[eng_key][i]
                f.write(f"| {s:,} | {eng_disp} | {fmt(st.instructions)} | {fmt(st.cycles)} | {st.ipc:.2f} |\n")
        f.write("\n")

        # Phase 2: Memory Hierarchy (L1, L2, L3, DRAM)
        f.write("## Phase 2: Memory Hierarchy (L1, L2, L3, DRAM)\n")
        f.write("| Size | Engine Variant | L1 Loads | L1 Misses | L2 Loads | L2 Misses | L3 Loads | DRAM Loads |\n")
        f.write("| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: |\n")
        for i, s in enumerate(sizes):
            for eng_disp, eng_key in engine_map:
                st: PmuStats = data[eng_key][i]
                f.write(f"| {s:,} | {eng_disp} | {fmt(st.l1_loads)} | {fmt(st.l1_misses)} | {fmt(st.l2_loads)} | {fmt(st.l2_misses)} | {fmt(st.l3_loads)} | {fmt(st.dram_loads)} |\n")
        f.write("\n")

        # Phase 3: Branch Profiling (Branches, Branch Misses)
        f.write("## Phase 3: Branch Profiling (Branches, Branch Misses)\n")
        f.write("| Size | Engine Variant | Branches | Branch Misses |\n")
        f.write("| :--- | :--- | ---: | ---: |\n")
        for i, s in enumerate(sizes):
            for eng_disp, eng_key in engine_map:
                st: PmuStats = data[eng_key][i]
                f.write(f"| {s:,} | {eng_disp} | {fmt(st.branches)} | {fmt(st.branch_misses)} |\n")
        f.write("\n")

        # Phase 4: Execution Time & Throughput
        f.write("## Phase 4: Execution Time & Throughput (per Iteration)\n")
        f.write("| Size | Engine Variant | Time (ms) | Evaluations | MEval/sec |\n")
        f.write("| :--- | :--- | ---: | ---: | ---: |\n")
        for i, s in enumerate(sizes):
            for eng_disp, eng_key in engine_map:
                st: PmuStats = data[eng_key][i]
                iters = st.iterations if st.iterations > 0 else 1.0
                t_str = f"{st.time_ms / iters:.4f}"
                e_str = f"{st.evals / iters:,.0f}"
                me_val = (st.evals / (st.time_ms / 1000.0)) / 1_000_000.0 if st.time_ms > 0 else 0.0
                f.write(f"| {s:,} | {eng_disp} | {t_str} | {e_str} | {me_val:.2f} |\n")
        f.write("\n")

        do_plot = args.plot or args.plot_log or args.plot_linear
        if do_plot:
            f.write("## Visualizations\n\n")
            f.write("### Linear Memory Hierarchy (4 Stages: L1, L2, L3, DRAM)\n\n")
            f.write(f"![Memory Hierarchy (Linear): Loads per Iteration](cache_perf_{mode_name}_{ts}_hierarchy_linear.png)\n\n")
            if args.plot_log or (args.plot and not args.plot_linear):
                f.write("### Logarithmic Memory Hierarchy (Log-Log)\n\n")
                f.write(f"![Memory Hierarchy (Log-Log): Loads per Iteration](cache_perf_{mode_name}_{ts}_hierarchy_log.png)\n\n")
            f.write("### Simulation Throughput (MEval/sec)\n\n")
            f.write(f"![Simulation Throughput: Mega-Evaluations per Second](cache_perf_{mode_name}_{ts}_throughput.png)\n\n")
            f.write("> *Curves smoothed using a 15-point moving average to isolate architectural scaling trends from localized PMU noise.*\n\n")

    print(f"Streamlined 4-phase report saved to {report_file}")

    # 3. Dedicated Plot Generation
    do_plot = args.plot or args.plot_log or args.plot_linear
    if do_plot:
        try:
            from plot_cache_perf import (
                plot_memory_hierarchy,
                plot_simulation_throughput,
                plot_branch_misses
            )
            
            # Linear Memory Hierarchy (primary)
            plot_file_linear = f"tests/test_result/perf/cache_perf_{mode_name}_{ts}_hierarchy_linear.png"
            plot_memory_hierarchy(json_doc["metadata"], data, scale='linear', output_path=plot_file_linear)

            # Optional Logarithmic Memory Hierarchy
            if args.plot_log or (args.plot and not args.plot_linear):
                plot_file_log = f"tests/test_result/perf/cache_perf_{mode_name}_{ts}_hierarchy_log.png"
                plot_memory_hierarchy(json_doc["metadata"], data, scale='log', output_path=plot_file_log)

            # Throughput
            plot_file_throughput = f"tests/test_result/perf/cache_perf_{mode_name}_{ts}_throughput.png"
            plot_simulation_throughput(json_doc["metadata"], data, output_path=plot_file_throughput)

            # Branch Misprediction Rate
            plot_file_branch = f"tests/test_result/perf/cache_perf_{mode_name}_{ts}_branch_misses.png"
            plot_branch_misses(json_doc["metadata"], data, output_path=plot_file_branch)
        except Exception as e:
            print(f"Plotting failed: {e}")

    print("\nTip: Run standalone plotter anytime without re-profiling:")
    print(f"  python tests/plot_cache_perf.py --json {json_file} --scale linear\n")


if __name__ == '__main__':
    main()
