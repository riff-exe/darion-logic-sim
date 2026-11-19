"""
cache_perf.py: cache and branch behaviour of the engines on synthetic chains and trees, with Linux `perf`.

    python tests/cache_perf.py --chaotic [--tree] [--plot]       profile (runs tests/cache_test.py per size and pass)
    python tests/cache_perf.py --from-json [FILE] [--scale both]  plot an existing result (latest in tests/test_result/perf)

Writes tests/test_result/perf/cache_perf_<mode>_<time>.{json,md} and, with --plot, the hierarchy, throughput and
branch-miss plots. Set REACTOR_DIR to profile a scratch engine build.
"""
import os
import sys
import subprocess
import argparse
import datetime
import json
import glob
import re
from typing import Dict, Any, List, Tuple, Optional

_TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_TESTS_DIR, "src"))     # pmu_harness lives next to the benchmark runners

from pmu_harness import pmu_harness, PmuStats


# ── plotting ─────────────────────────────────────────────────────────────────────────────────────────────────
def smooth_curve(y, window_size: int = 3):
    """Moving average convolution with edge padding to avoid border distortion."""
    import numpy as np
    y_arr = np.asarray(y, dtype=float)
    if len(y_arr) < window_size or window_size <= 1:
        return y_arr
    box = np.ones(window_size) / window_size
    pad_left = window_size // 2
    pad_right = window_size - 1 - pad_left
    padded = np.pad(y_arr, (pad_left, pad_right), mode='edge')
    return np.convolve(padded, box, mode='valid')


def parse_numeric(s: str) -> float:
    """Parses suffixed metrics (e.g. 7.09B, 67.08K, 1.28M) into raw floats."""
    s = s.strip().replace(",", "").replace("%", "")
    if not s or s == "N/A":
        return 0.0
    mult = 1.0
    if s.endswith("B"):
        mult = 1e9
        s = s[:-1]
    elif s.endswith("M"):
        mult = 1e6
        s = s[:-1]
    elif s.endswith("K"):
        mult = 1e3
        s = s[:-1]
    try:
        return float(s) * mult
    except ValueError:
        return 0.0


def load_from_json(json_path: str) -> Tuple[Dict[str, Any], Dict[str, List[PmuStats]]]:
    """Loads benchmark metadata and PmuStats dictionaries from a JSON file."""
    with open(json_path, "r", encoding="utf-8") as f:
        doc = json.load(f)

    metadata = doc.get("metadata", {})
    raw_data = doc.get("data", {})
    
    data: Dict[str, List[PmuStats]] = {}
    for engine_key, stats_list in raw_data.items():
        data[engine_key] = [PmuStats.from_dict(item) for item in stats_list]

    return metadata, data


def parse_md_fallback(md_path: str) -> Tuple[Dict[str, Any], Dict[str, List[PmuStats]]]:
    """
    Fallback parser for existing legacy markdown benchmark reports.
    Extracts sizes, engines, PMU metrics, time, and evals.
    """
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    metadata: Dict[str, Any] = {
        "mode": "chaotic",
        "cpu_model": "Unknown CPU",
        "pmu_events": "",
        "sizes": [],
        "engines": ["oop", "unopt", "opt", "sweep"],
        "source_file": md_path
    }

    m_mode = re.search(r"# Cache Fragmentation Profile \(([^)]+)\)", content)
    if m_mode:
        metadata["mode"] = m_mode.group(1).lower()

    m_cpu = re.search(r"CPU:\s*([^|]+)\|\s*PMU Events:\s*`([^`]+)`", content)
    if m_cpu:
        metadata["cpu_model"] = m_cpu.group(1).strip()
        metadata["pmu_events"] = m_cpu.group(2).strip()

    data: Dict[str, List[PmuStats]] = {
        "oop": [],
        "unopt": [],
        "opt": [],
        "sweep": []
    }

    engine_name_to_key = {
        "OOP": "oop",
        "Unopt BFS": "unopt",
        "Opt BFS": "opt",
        "Linear Sweep": "sweep",
        "Fragmented (OOP)": "oop",
        "Unoptimized (BFS)": "unopt",
        "Sorted (BFS)": "opt",
        "Linear (Sweep)": "sweep",
    }

    # Parse Table 1 (Overview table)
    t1_match = re.search(r"## 1\. Hardware PMU & Cache Hierarchy Overview.*?\n\|(.*?)\n\|[-:| ]+\n(.*?)(?=\n##|\Z)", content, re.DOTALL)
    sizes_set = []
    
    if t1_match:
        rows = t1_match.group(2).strip().split("\n")
        for row in rows:
            cols = [c.strip() for c in row.strip("|").split("|")]
            if len(cols) < 9:
                continue
            try:
                size_val = int(cols[0].replace(",", ""))
            except ValueError:
                continue
            if size_val not in sizes_set:
                sizes_set.append(size_val)
            
            eng_str = cols[1]
            eng_key = engine_name_to_key.get(eng_str)
            if not eng_key:
                continue

            inst = parse_numeric(cols[2])
            cyc = parse_numeric(cols[3])
            l1_loads = parse_numeric(cols[5])
            l2_loads = parse_numeric(cols[6])
            l3_loads = parse_numeric(cols[7])
            dram_loads = parse_numeric(cols[8])
            brn = parse_numeric(cols[12]) if len(cols) > 12 else 0.0
            brn_miss = parse_numeric(cols[13]) if len(cols) > 13 else 0.0

            st = PmuStats(
                instructions=inst,
                cycles=cyc,
                l1_loads=l1_loads,
                l1_misses=l2_loads,
                l2_loads=l2_loads,
                l2_misses=l3_loads,
                l3_loads=l3_loads,
                dram_loads=dram_loads,
                branches=brn,
                branch_misses=brn_miss
            )
            data[eng_key].append(st)

    # Parse Phase 2 table if Table 1 was not found
    if not sizes_set:
        p2_match = re.search(r"## Phase 2: Memory Hierarchy.*?\n\|(.*?)\n\|[-:| ]+\n(.*?)(?=\n##|\Z)", content, re.DOTALL)
        if p2_match:
            rows = p2_match.group(2).strip().split("\n")
            for row in rows:
                cols = [c.strip() for c in row.strip("|").split("|")]
                if len(cols) < 8:
                    continue
                try:
                    size_val = int(cols[0].replace(",", ""))
                except ValueError:
                    continue
                if size_val not in sizes_set:
                    sizes_set.append(size_val)
                eng_str = cols[1]
                eng_key = engine_name_to_key.get(eng_str)
                if not eng_key:
                    continue
                l1_loads = parse_numeric(cols[2])
                l1_miss = parse_numeric(cols[3])
                l2_loads = parse_numeric(cols[4])
                l2_miss = parse_numeric(cols[5])
                l3_loads = parse_numeric(cols[6])
                dram_loads = parse_numeric(cols[7])
                st = PmuStats(
                    l1_loads=l1_loads,
                    l1_misses=l1_miss,
                    l2_loads=l2_loads,
                    l2_misses=l2_miss,
                    l3_loads=l3_loads,
                    dram_loads=dram_loads
                )
                data[eng_key].append(st)

    metadata["sizes"] = sorted(sizes_set)

    # Parse Phase 4 or Table 7 for time_ms, evals, iterations
    p4_match = re.search(r"## Phase 4: Execution Time & Throughput.*?\n\|(.*?)\n\|[-:| ]+\n(.*?)(?=\n##|\Z)", content, re.DOTALL)
    if p4_match:
        rows = p4_match.group(2).strip().split("\n")
        idx_map = {k: 0 for k in data}
        for row in rows:
            cols = [c.strip() for c in row.strip("|").split("|")]
            if len(cols) < 5:
                continue
            eng_str = cols[1]
            eng_key = engine_name_to_key.get(eng_str)
            if not eng_key:
                continue
            time_ms = parse_numeric(cols[2])
            evals = parse_numeric(cols[3])
            idx = idx_map[eng_key]
            if idx < len(data[eng_key]):
                st = data[eng_key][idx]
                st.time_ms = time_ms
                st.evals = evals
                st.iterations = 1.0
                idx_map[eng_key] += 1

    return metadata, data


def find_latest_benchmark_file(directory: str = "tests/test_result/perf") -> Optional[str]:
    """Finds the most recent .json (or .md) benchmark file in the target directory."""
    json_files = glob.glob(os.path.join(directory, "cache_perf_*.json"))
    if json_files:
        return max(json_files, key=os.path.getmtime)
    md_files = glob.glob(os.path.join(directory, "cache_perf_*.md"))
    if md_files:
        return max(md_files, key=os.path.getmtime)
    return None


def plot_cache_perf_scaling(
    metadata: Dict[str, Any],
    data: Dict[str, List[PmuStats]],
    output_path: Optional[str] = None,
    dpi: int = 300
) -> str:
    """
    Renders the unified 5-subplot Cache Performance Scaling figure:
      1. L1 Cache Loads
      2. L1 Cache Misses / L2 Loads
      3. L2 Cache Misses / L3 Loads
      4. L3 Cache Misses / RAM Loads
      5. Simulation Throughput (MEPS)
    Values are plotted AS IS without iteration normalization,
    using distinct shape markers for each engine curve.
    """
    import matplotlib.pyplot as plt

    sizes = metadata.get("sizes", [])
    if not sizes and "oop" in data and len(data["oop"]) > 0:
        sizes = list(range(100, 100 + len(data["oop"]) * 100, 100))

    mode_name = metadata.get("mode", "Benchmark").upper()

    def raw(pass_name: str, attr: str):
        res = []
        for i, s in enumerate(sizes):
            if pass_name not in data or i >= len(data[pass_name]):
                res.append(1.0)
                continue
            st = data[pass_name][i]
            val = float(getattr(st, attr, 0.0) if hasattr(st, attr) else st.get(attr, 0.0))
            if attr == "l1_misses" and val == 0.0:
                val = float(getattr(st, "l2_loads", 0.0) if hasattr(st, "l2_loads") else st.get("l2_loads", 0.0))
            elif attr == "l2_misses" and val == 0.0:
                val = float(getattr(st, "l3_loads", 0.0) if hasattr(st, "l3_loads") else st.get("l3_loads", 0.0))
            elif attr == "dram_loads" and val == 0.0:
                val = float(getattr(st, "l3_misses", 0.0) if hasattr(st, "l3_misses") else st.get("l3_misses", 0.0))
            iters = float(getattr(st, 'iterations', 1.0) if hasattr(st, 'iterations') else st.get('iterations', 1.0))
            if iters > 0:
                val = val / iters
            res.append(max(0.1, val))
        return res

    def meps(pass_name: str):
        res = []
        for i, s in enumerate(sizes):
            if pass_name not in data or i >= len(data[pass_name]):
                res.append(0.0)
                continue
            st = data[pass_name][i]
            time_ms = float(getattr(st, "time_ms", 0.0) if hasattr(st, "time_ms") else st.get("time_ms", 0.0))
            evals = float(getattr(st, "evals", 0.0) if hasattr(st, "evals") else st.get("evals", 0.0))
            time_s = time_ms / 1000.0 if time_ms > 0 else 1e-9
            res.append((evals / time_s) / 1_000_000.0)
        return res

    def add_cliffs(ax):
        if sizes and min(sizes) <= 1000 <= max(sizes):
            ax.axvline(x=1000, color='gray', linestyle='--', alpha=0.7)
            ax.text(1000 * 1.2, 0.5, "L1 Capacity Spill", color='gray', rotation=90, verticalalignment='center', transform=ax.get_xaxis_transform())
        if sizes and min(sizes) <= 10000 <= max(sizes):
            ax.axvline(x=10000, color='black', linestyle='--', alpha=0.7)
            ax.text(10000 * 1.2, 0.5, "L2 Saturation / RAM Wall", color='black', rotation=90, verticalalignment='center', transform=ax.get_xaxis_transform())

    fig = plt.figure(figsize=(14, 25))

    # Subplot 1: L1 Loads
    ax1 = plt.subplot(5, 1, 1)
    plt.title(f"L1 Cache Loads per Iteration ({mode_name})", fontsize=13, fontweight='bold')
    plt.plot(sizes, raw("oop", "l1_loads"), label="Reactor OOP", color="purple", linewidth=2.5)
    plt.plot(sizes, raw("unopt", "l1_loads"), label="Unoptimized (BFS)", color="red", linewidth=2.5)
    plt.plot(sizes, raw("opt", "l1_loads"), label="Optimized (BFS)", color="blue", linewidth=2.5)
    plt.plot(sizes, raw("sweep", "l1_loads"), label="Optimized (Sweep)", color="green", linewidth=2.5)
    plt.xscale("log")
    plt.yscale("log")
    plt.ylabel("L1 Loads / Iter", fontsize=11, fontweight='bold')
    add_cliffs(ax1)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=11)

    # Subplot 2: L1 Misses / L2 Loads
    ax2 = plt.subplot(5, 1, 2)
    plt.title(f"L1 Cache Misses / L2 Loads per Iteration ({mode_name})", fontsize=13, fontweight='bold')
    plt.plot(sizes, raw("oop", "l1_misses"), color="purple", linewidth=2.5)
    plt.plot(sizes, raw("unopt", "l1_misses"), color="red", linewidth=2.5)
    plt.plot(sizes, raw("opt", "l1_misses"), color="blue", linewidth=2.5)
    plt.plot(sizes, raw("sweep", "l1_misses"), color="green", linewidth=2.5)
    plt.xscale("log")
    plt.yscale("log")
    plt.ylabel("L1 Misses / L2 Loads / Iter", fontsize=11, fontweight='bold')
    add_cliffs(ax2)
    plt.grid(True, alpha=0.3)

    # Subplot 3: L2 Misses / L3 Loads
    ax3 = plt.subplot(5, 1, 3)
    plt.title(f"L2 Cache Misses / L3 Loads per Iteration ({mode_name})", fontsize=13, fontweight='bold')
    plt.plot(sizes, raw("oop", "l2_misses"), color="purple", linewidth=2.5)
    plt.plot(sizes, raw("unopt", "l2_misses"), color="red", linewidth=2.5)
    plt.plot(sizes, raw("opt", "l2_misses"), color="blue", linewidth=2.5)
    plt.plot(sizes, raw("sweep", "l2_misses"), color="green", linewidth=2.5)
    plt.xscale("log")
    plt.yscale("log")
    plt.ylabel("L2 Misses / L3 Loads / Iter", fontsize=11, fontweight='bold')
    add_cliffs(ax3)
    plt.grid(True, alpha=0.3)

    # Subplot 4: L3 Misses / RAM Loads
    ax4 = plt.subplot(5, 1, 4)
    plt.title(f"L3 Cache Misses / RAM Loads per Iteration ({mode_name})", fontsize=13, fontweight='bold')
    plt.plot(sizes, raw("oop", "dram_loads"), color="purple", linewidth=2.5)
    plt.plot(sizes, raw("unopt", "dram_loads"), color="red", linewidth=2.5)
    plt.plot(sizes, raw("opt", "dram_loads"), color="blue", linewidth=2.5)
    plt.plot(sizes, raw("sweep", "dram_loads"), color="green", linewidth=2.5)
    plt.xscale("log")
    plt.yscale("log")
    plt.ylabel("L3 Misses / RAM Loads / Iter", fontsize=11, fontweight='bold')
    add_cliffs(ax4)
    plt.grid(True, alpha=0.3)

    # Subplot 5: MEPS
    ax5 = plt.subplot(5, 1, 5)
    plt.title(f"Throughput (Mega-Evaluations Per Second) ({mode_name})", fontsize=13, fontweight='bold')
    plt.plot(sizes, meps("oop"), label="Reactor OOP", color="purple", linewidth=2.5)
    plt.plot(sizes, meps("unopt"), label="Unoptimized (BFS)", color="red", linewidth=2.5)
    plt.plot(sizes, meps("opt"), label="Optimized (BFS)", color="blue", linewidth=2.5)
    plt.plot(sizes, meps("sweep"), label="Optimized (Sweep)", color="green", linewidth=2.5)
    plt.xscale("log")
    plt.yscale("linear")
    plt.ylabel("MEPS", fontsize=11, fontweight='bold')
    plt.xlabel("Circuit Size (Gates)", fontsize=12, fontweight='bold')
    add_cliffs(ax5)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=11)

    plt.tight_layout()

    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        fig.savefig(output_path, bbox_inches='tight', dpi=dpi)
        print(f"5-Subplot Cache Performance Scaling plot saved to -> {output_path}")

    plt.close(fig)
    return output_path or ""


def plot_memory_hierarchy(
    metadata: Dict[str, Any],
    data: Dict[str, List[PmuStats]],
    scale: str = 'linear',
    smoothing: int = 3,
    output_path: Optional[str] = None,
    dpi: int = 300
) -> str:
    """
    Renders the 4-Stage Memory Hierarchy Decomposition across 4 subplots
    (L1, L2, L3, DRAM) using loads normalized per iteration with continuous curves.
    """
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker

    sizes = metadata.get("sizes", [])
    if not sizes and "oop" in data and len(data["oop"]) > 0:
        sizes = list(range(100, 100 + len(data["oop"]) * 100, 100))

    mode_name = metadata.get("mode", "Benchmark").upper()
    scale_title = "LINEAR" if scale == 'linear' else "LOG-LOG"

    fig, axes = plt.subplots(4, 1, figsize=(14, 16), sharex=True)
    fig.suptitle(
        f"Memory Hierarchy Decomposition: Loads per Iteration ({mode_name} — {scale_title})",
        fontsize=16, fontweight='bold', y=0.985
    )

    engine_styles = {
        'sweep': {'col': '#2E7D32', 'ls': '-', 'lw': 2.5, 'label': 'Linear Sweep'},   # Green
        'opt':   {'col': '#1565C0', 'ls': '-', 'lw': 2.5, 'label': 'Optimized BFS'},   # Blue
        'unopt': {'col': '#D32F2F', 'ls': '-', 'lw': 2.5, 'label': 'Unoptimized BFS'}, # Red
        'oop':   {'col': '#7B1FA2', 'ls': '-', 'lw': 2.5, 'label': 'Reactor OOP'},     # Purple
    }

    subplots_config = [
        (axes[0], 'Stage 1: L1 Data Cache (Loads)', 'l1_loads'),
        (axes[1], 'Stage 2: L2 Cache (L1 Misses)', 'l2_loads'),
        (axes[2], 'Stage 3: L3 Cache (L2 Misses)', 'l3_loads'),
        (axes[3], 'Stage 4: DRAM / Main Memory (Spill)', 'dram_loads')
    ]

    # Helper to calculate loads normalized per iteration
    def get_raw_vals(pass_name: str, attr: str):
        vals = []
        for i, s in enumerate(sizes):
            if pass_name not in data or i >= len(data[pass_name]):
                vals.append(1.0 if scale == 'log' else 0.0)
                continue
            st = data[pass_name][i]
            val = float(getattr(st, attr, 0.0) if hasattr(st, attr) else st.get(attr, 0.0))
            iters = float(getattr(st, 'iterations', 1.0) if hasattr(st, 'iterations') else st.get('iterations', 1.0))
            if iters > 0:
                val = val / iters
            if scale == 'log':
                val = max(0.1, val)
            vals.append(val)
        if smoothing > 1:
            if scale == 'log':
                import numpy as np
                log_vals = np.log10(np.maximum(1e-3, vals))
                smoothed_log = smooth_curve(log_vals, window_size=smoothing)
                return np.power(10.0, smoothed_log)
            return smooth_curve(vals, window_size=smoothing)
        return vals

    for ax, title, attr in subplots_config:
        ax.set_title(title, fontsize=13, fontweight='bold', pad=8)
        
        for eng_key in ['oop', 'unopt', 'opt', 'sweep']:
            cfg = engine_styles[eng_key]
            y_vals = get_raw_vals(eng_key, attr)
            ax.plot(sizes, y_vals, color=cfg['col'], linestyle=cfg['ls'], linewidth=cfg['lw'],
                    label=cfg['label'])

        ax.set_xscale(scale)
        ax.set_yscale(scale)
        ax.set_ylabel('Loads / Iter', fontsize=11, fontweight='bold')
        ax.grid(True, alpha=0.3, which='both' if scale == 'log' else 'major', linestyle='--')

        if scale == 'linear':
            ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{int(x):,}"))
            def format_y(val, pos):
                if val >= 1e9: return f"{val/1e9:.1f}B" if (val % 1e9) != 0 else f"{int(val/1e9)}B"
                elif val >= 1e6: return f"{val/1e6:.1f}M" if (val % 1e6) != 0 else f"{int(val/1e6)}M"
                elif val >= 1e3: return f"{val/1e3:.1f}K" if (val % 1e3) != 0 else f"{int(val/1e3)}K"
                elif val >= 1: return f"{val:.1f}" if (val % 1) != 0 else f"{int(val)}"
                else: return f"{val:.2f}"
            ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_y))

    # Set bottom subplot X-axis label
    axes[3].set_xlabel('Circuit Size (Gates)', fontsize=12, fontweight='bold')

    # Single unified legend at the bottom
    engine_handles = [
        plt.Line2D([0], [0], color=engine_styles['sweep']['col'], lw=engine_styles['sweep']['lw'], linestyle=engine_styles['sweep']['ls'], label=engine_styles['sweep']['label']),
        plt.Line2D([0], [0], color=engine_styles['opt']['col'], lw=engine_styles['opt']['lw'], linestyle=engine_styles['opt']['ls'], label=engine_styles['opt']['label']),
        plt.Line2D([0], [0], color=engine_styles['unopt']['col'], lw=engine_styles['unopt']['lw'], linestyle=engine_styles['unopt']['ls'], label=engine_styles['unopt']['label']),
        plt.Line2D([0], [0], color=engine_styles['oop']['col'], lw=engine_styles['oop']['lw'], linestyle=engine_styles['oop']['ls'], label=engine_styles['oop']['label'])
    ]

    fig.legend(
        handles=engine_handles, title="Engine Traversal",
        loc='lower center', bbox_to_anchor=(0.5, 0.008),
        ncol=4, frameon=True, fontsize=11, title_fontsize=12
    )

    plt.tight_layout(rect=[0, 0.035, 1, 0.975])

    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        fig.savefig(output_path, bbox_inches='tight', dpi=dpi)
        print(f"[{scale_title}] 4-Subplot Memory Hierarchy plot saved to -> {output_path}")

    plt.close(fig)
    return output_path or ""


def plot_simulation_throughput(
    metadata: Dict[str, Any],
    data: Dict[str, List[PmuStats]],
    smoothing: int = 3,
    output_path: Optional[str] = None,
    dpi: int = 300
) -> str:
    """Renders the Simulation Throughput (MEval/sec) plot with continuous curves."""
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker

    sizes = metadata.get("sizes", [])
    if not sizes and "oop" in data and len(data["oop"]) > 0:
        sizes = list(range(100, 100 + len(data["oop"]) * 100, 100))

    mode_name = metadata.get("mode", "Benchmark").upper()

    fig, ax = plt.subplots(figsize=(11, 6.8))
    ax.set_title(
        f"Simulation Throughput: Mega-Evaluations per Second ({mode_name})",
        fontsize=14, fontweight='bold', pad=15
    )

    def get_meps(pass_name: str):
        vals = []
        for i, s in enumerate(sizes):
            if pass_name not in data or i >= len(data[pass_name]):
                vals.append(0.0)
                continue
            st = data[pass_name][i]
            time_ms = float(getattr(st, "time_ms", 0.0) if hasattr(st, "time_ms") else st.get("time_ms", 0.0))
            evals = float(getattr(st, "evals", 0.0) if hasattr(st, "evals") else st.get("evals", 0.0))
            time_s = time_ms / 1000.0 if time_ms > 0 else 1e-9
            vals.append((evals / time_s) / 1_000_000.0)
        if smoothing > 1:
            return smooth_curve(vals, window_size=smoothing)
        return vals

    # Continuous curves with consistent engine colors (no markers/dots)
    ax.plot(sizes, get_meps("sweep"), label="Linear Sweep", color="#2E7D32", linestyle='-', linewidth=2.5)
    ax.plot(sizes, get_meps("opt"), label="Optimized BFS", color="#1565C0", linestyle='-', linewidth=2.5)
    ax.plot(sizes, get_meps("unopt"), label="Unoptimized BFS", color="#D32F2F", linestyle='-', linewidth=2.5)
    ax.plot(sizes, get_meps("oop"), label="Reactor OOP", color="#7B1FA2", linestyle='-', linewidth=2.5)

    ax.set_xscale("linear")
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{int(x):,}"))
    ax.set_xlabel("Circuit Size (Gates)", fontsize=12, fontweight='bold')
    ax.set_ylabel("Throughput (MEval / sec)", fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3, linestyle='--')

    ax.legend(
        loc='upper center',
        bbox_to_anchor=(0.5, -0.14),
        ncol=4,
        frameon=True,
        fontsize=11
    )
    plt.tight_layout()

    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        fig.savefig(output_path, bbox_inches='tight', dpi=dpi)
        print(f"Throughput plot saved to -> {output_path}")

    plt.close(fig)
    return output_path or ""


def plot_branch_misses(
    metadata: Dict[str, Any],
    data: Dict[str, List[PmuStats]],
    smoothing: int = 3,
    output_path: Optional[str] = None,
    dpi: int = 300
) -> str:
    """Renders the Branch Misprediction Rate (%) plot with continuous curves."""
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker

    sizes = metadata.get("sizes", [])
    if not sizes and "oop" in data and len(data["oop"]) > 0:
        sizes = list(range(100, 100 + len(data["oop"]) * 100, 100))

    mode_name = metadata.get("mode", "Benchmark").upper()

    fig, ax = plt.subplots(figsize=(11, 6.8))
    ax.set_title(
        f"Branch Misprediction Rate: Branch Miss % ({mode_name})",
        fontsize=14, fontweight='bold', pad=15
    )

    def get_miss_pct(pass_name: str):
        vals = []
        for i, s in enumerate(sizes):
            if pass_name not in data or i >= len(data[pass_name]):
                vals.append(0.0)
                continue
            st = data[pass_name][i]
            branches = float(getattr(st, "branches", 0.0) if hasattr(st, "branches") else st.get("branches", 0.0))
            misses = float(getattr(st, "branch_misses", 0.0) if hasattr(st, "branch_misses") else st.get("branch_misses", 0.0))
            pct = (misses / branches * 100.0) if branches > 0 else 0.0
            vals.append(pct)
        if smoothing > 1:
            return smooth_curve(vals, window_size=smoothing)
        return vals

    # Continuous curves with consistent engine colors (no markers/dots)
    ax.plot(sizes, get_miss_pct("sweep"), label="Linear Sweep", color="#2E7D32", linestyle='-', linewidth=2.5)
    ax.plot(sizes, get_miss_pct("opt"), label="Optimized BFS", color="#1565C0", linestyle='-', linewidth=2.5)
    ax.plot(sizes, get_miss_pct("unopt"), label="Unoptimized BFS", color="#D32F2F", linestyle='-', linewidth=2.5)
    ax.plot(sizes, get_miss_pct("oop"), label="Reactor OOP", color="#7B1FA2", linestyle='-', linewidth=2.5)

    ax.set_xscale("linear")
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{int(x):,}"))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, p: f"{y:.1f}%"))
    ax.set_xlabel("Circuit Size (Gates)", fontsize=12, fontweight='bold')
    ax.set_ylabel("Branch Misprediction Rate (%)", fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3, linestyle='--')

    ax.legend(
        loc='upper center',
        bbox_to_anchor=(0.5, -0.14),
        ncol=4,
        frameon=True,
        fontsize=11
    )
    plt.tight_layout()

    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        fig.savefig(output_path, bbox_inches='tight', dpi=dpi)
        print(f"Branch misprediction plot saved to -> {output_path}")

    plt.close(fig)
    return output_path or ""


def plot_existing(args):
    """Plot a stored result (JSON, or the legacy markdown) without profiling."""
    input_file = args.from_json if args.from_json not in (None, "latest") else args.from_md
    if not input_file:
        input_file = find_latest_benchmark_file()
        if not input_file:
            print("Error: No benchmark data found in 'tests/test_result/perf'. Run 'python tests/cache_perf.py' first.")
            sys.exit(1)
        print(f"Auto-selected latest benchmark data: {input_file}")
    if input_file.endswith(".json"):
        metadata, data = load_from_json(input_file)
    elif input_file.endswith(".md"):
        print(f"Parsing legacy markdown file: {input_file}")
        metadata, data = parse_md_fallback(input_file)
    else:
        print(f"Error: Unsupported file format '{input_file}'. Expected .json or .md.")
        sys.exit(1)

    out_dir = args.output_dir or os.path.dirname(os.path.abspath(input_file))
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    base_name = re.sub(r"_(hierarchy_linear|hierarchy_log|throughput|funnel|branch_misses)$", "", base_name)
    print(f"\nGenerating plots for {metadata.get('mode', 'benchmark').upper()} (Sizes: {len(metadata.get('sizes', []))} points)...")

    if args.scaling:
        plot_cache_perf_scaling(metadata, data, output_path=os.path.join(out_dir, f"{base_name}.png"), dpi=args.dpi)
    if args.scale in ['linear', 'both']:
        plot_memory_hierarchy(metadata, data, scale='linear', smoothing=args.smoothing, dpi=args.dpi,
                              output_path=os.path.join(out_dir, f"{base_name}_hierarchy_linear.png"))
    if args.scale in ['log', 'both']:
        plot_memory_hierarchy(metadata, data, scale='log', smoothing=args.smoothing, dpi=args.dpi,
                              output_path=os.path.join(out_dir, f"{base_name}_hierarchy_log.png"))
    if not args.no_throughput:
        plot_simulation_throughput(metadata, data, smoothing=args.smoothing, dpi=args.dpi,
                                   output_path=os.path.join(out_dir, f"{base_name}_throughput.png"))
    if not args.no_branch:
        plot_branch_misses(metadata, data, smoothing=args.smoothing, dpi=args.dpi,
                           output_path=os.path.join(out_dir, f"{base_name}_branch_misses.png"))
    print("All requested plots successfully generated.\n")


def main():
    parser = argparse.ArgumentParser(description="Cache Performance Scaling Profiler")
    parser.add_argument('--chaotic', action='store_true', help='Run mixed chaotic test')
    parser.add_argument('--realistic', action='store_true', help='Run mixed realistic test')
    parser.add_argument('--and', dest='gate_and', action='store_true', help='Run homogeneous AND test')
    parser.add_argument('--nand', dest='gate_nand', action='store_true', help='Run homogeneous NAND test')
    parser.add_argument('--or', dest='gate_or', action='store_true', help='Run homogeneous OR test')
    parser.add_argument('--nor', dest='gate_nor', action='store_true', help='Run homogeneous NOR test')
    parser.add_argument('--xor', dest='gate_xor', action='store_true', help='Run homogeneous XOR test')
    parser.add_argument('--xnor', dest='gate_xnor', action='store_true', help='Run homogeneous XNOR test')
    parser.add_argument('--buffer', '--buf', dest='gate_buffer', action='store_true', help='Run homogeneous BUFFER test')
    parser.add_argument('--not', dest='gate_not', action='store_true', help='Run homogeneous NOT test')
    parser.add_argument('--tree', '--binary-tree', dest='tree', action='store_true', help='Wire circuit as a complete binary tree (MST) instead of a linear chain')
    parser.add_argument('--plot', action='store_true', help='Generate both logarithmic and linear plots')
    parser.add_argument('--plot-log', action='store_true', help='Generate logarithmic plot')
    parser.add_argument('--plot-linear', action='store_true', help='Generate linear plot')
    parser.add_argument('--smoothing', type=int, default=3, help='Moving average smoothing window (default: 3)')
    parser.add_argument('--min-size', type=int, default=100, help='Minimum circuit size (default: 100)')
    parser.add_argument('--max-size', type=int, default=1e6, help='Maximum circuit size (default: 50000)')
    parser.add_argument('--step', type=float, default=0.15, help='Circuit size step increment (default: 200)')
    
    parser.add_argument('--from-json', nargs='?', const='latest', default=None, metavar='FILE', help='Skip profiling: plot an existing result (default: the latest JSON)')
    parser.add_argument('--from-md', default=None, metavar='FILE', help='Skip profiling: plot a legacy markdown result')
    parser.add_argument('--scale', choices=['linear', 'log', 'both'], default='linear', help='With --from-json: scale of the memory hierarchy plot')
    parser.add_argument('--scaling', action='store_true', help='With --from-json: also the unified 5-subplot scaling plot')
    parser.add_argument('--no-throughput', action='store_true', help='With --from-json: skip the throughput plot')
    parser.add_argument('--no-branch', action='store_true', help='With --from-json: skip the branch misprediction plot')
    parser.add_argument('--output-dir', default=None, help='With --from-json: output directory (default: next to the input)')
    parser.add_argument('--dpi', type=int, default=300, help='With --from-json: plot resolution')

    args, unknown = parser.parse_known_args()
    if args.from_json is not None or args.from_md is not None:
        return plot_existing(args)
    if sys.platform != "linux":
        print("Error: Profiling tools ('perf' and FIFOs) are Linux-exclusive. Aborting.")
        sys.exit(0)
    
    test_args = []
    mode_name = "chaotic"
    if args.realistic: 
        test_args.append('--realistic')
        mode_name = "realistic"
    elif args.gate_and:
        test_args.append('--and')
        mode_name = "homogeneous_and"
    elif args.gate_nand:
        test_args.append('--nand')
        mode_name = "homogeneous_nand"
    elif args.gate_or:
        test_args.append('--or')
        mode_name = "homogeneous_or"
    elif args.gate_nor:
        test_args.append('--nor')
        mode_name = "homogeneous_nor"
    elif args.gate_xor:
        test_args.append('--xor')
        mode_name = "homogeneous_xor"
    elif args.gate_xnor:
        test_args.append('--xnor')
        mode_name = "homogeneous_xnor"
    elif args.gate_buffer:
        test_args.append('--buffer')
        mode_name = "homogeneous_buffer"
    elif args.gate_not:
        test_args.append('--not')
        mode_name = "homogeneous_not"
    else:
        test_args.append('--chaotic')

    if args.tree:
        test_args.append('--tree')
        mode_name += "_tree"

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
        current_size += int(current_size * args.step)
        
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
            "topology": "binary_tree" if args.tree else "chain",
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
        topology_desc = "Complete Binary Tree (MST)" if args.tree else "Linear Chain"
        f.write(f"# Cache Fragmentation Profile ({mode_name.upper()})\n\n")
        f.write(f"Topology: {topology_desc}. Isolated purely via hardware `perf` boundaries tightly hugging the core `batch_toggle` simulation logic.\n")
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

        # Phase 1: Core Performance (Instructions, Cycles, IPC — per Iteration)
        f.write("## Phase 1: Core Performance (Instructions, Cycles, IPC — per Iteration)\n")
        f.write("| Size | Engine Variant | Instructions | Cycles | IPC |\n")
        f.write("| :--- | :--- | ---: | ---: | ---: |\n")
        for i, s in enumerate(sizes):
            for eng_disp, eng_key in engine_map:
                st: PmuStats = data[eng_key][i]
                iters = st.iterations if st.iterations > 0 else 1.0
                f.write(f"| {s:,} | {eng_disp} | {fmt(st.instructions / iters)} | {fmt(st.cycles / iters)} | {st.ipc:.2f} |\n")
        f.write("\n")

        # Phase 2: Memory Hierarchy (L1, L2, L3, DRAM — per Iteration)
        f.write("## Phase 2: Memory Hierarchy (L1, L2, L3, DRAM — per Iteration)\n")
        f.write("| Size | Engine Variant | L1 Loads | L1 Misses | L2 Loads | L2 Misses | L3 Loads | DRAM Loads |\n")
        f.write("| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: |\n")
        for i, s in enumerate(sizes):
            for eng_disp, eng_key in engine_map:
                st: PmuStats = data[eng_key][i]
                iters = st.iterations if st.iterations > 0 else 1.0
                f.write(f"| {s:,} | {eng_disp} | {fmt(st.l1_loads / iters)} | {fmt(st.l1_misses / iters)} | {fmt(st.l2_loads / iters)} | {fmt(st.l2_misses / iters)} | {fmt(st.l3_loads / iters)} | {fmt(st.dram_loads / iters)} |\n")
        f.write("\n")

        # Phase 3: Branch Profiling (Branches, Branch Misses — per Iteration)
        f.write("## Phase 3: Branch Profiling (Branches, Branch Misses — per Iteration)\n")
        f.write("| Size | Engine Variant | Branches | Branch Misses |\n")
        f.write("| :--- | :--- | ---: | ---: |\n")
        for i, s in enumerate(sizes):
            for eng_disp, eng_key in engine_map:
                st: PmuStats = data[eng_key][i]
                iters = st.iterations if st.iterations > 0 else 1.0
                f.write(f"| {s:,} | {eng_disp} | {fmt(st.branches / iters)} | {fmt(st.branch_misses / iters)} |\n")
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
            f.write(f"![Memory Hierarchy (Linear)](cache_perf_{mode_name}_{ts}_hierarchy_linear.png)\n\n")
            if args.plot_log or (args.plot and not args.plot_linear):
                f.write("### Logarithmic Memory Hierarchy (Log-Log)\n\n")
                f.write(f"![Memory Hierarchy (Log-Log)](cache_perf_{mode_name}_{ts}_hierarchy_log.png)\n\n")
            f.write("### Simulation Throughput (MEval/sec)\n\n")
            f.write(f"![Simulation Throughput: Mega-Evaluations per Second](cache_perf_{mode_name}_{ts}_throughput.png)\n\n")
            f.write("### Branch Misprediction Rate (%)\n\n")
            f.write(f"![Branch Misprediction Rate](cache_perf_{mode_name}_{ts}_branch_misses.png)\n\n")

    print(f"Streamlined 4-phase report saved to {report_file}")

    # 3. Dedicated Plot Generation
    do_plot = args.plot or args.plot_log or args.plot_linear
    if do_plot:
        try:
            # Linear Memory Hierarchy (primary, loads normalized per iteration)
            plot_file_linear = f"tests/test_result/perf/cache_perf_{mode_name}_{ts}_hierarchy_linear.png"
            plot_memory_hierarchy(json_doc["metadata"], data, scale='linear', smoothing=args.smoothing, output_path=plot_file_linear)

            # Optional Logarithmic Memory Hierarchy (loads normalized per iteration)
            if args.plot_log or (args.plot and not args.plot_linear):
                plot_file_log = f"tests/test_result/perf/cache_perf_{mode_name}_{ts}_hierarchy_log.png"
                plot_memory_hierarchy(json_doc["metadata"], data, scale='log', smoothing=args.smoothing, output_path=plot_file_log)

            # Throughput
            plot_file_throughput = f"tests/test_result/perf/cache_perf_{mode_name}_{ts}_throughput.png"
            plot_simulation_throughput(json_doc["metadata"], data, smoothing=args.smoothing, output_path=plot_file_throughput)

            # Branch Misprediction Rate
            plot_file_branch = f"tests/test_result/perf/cache_perf_{mode_name}_{ts}_branch_misses.png"
            plot_branch_misses(json_doc["metadata"], data, smoothing=args.smoothing, output_path=plot_file_branch)
        except Exception as e:
            print(f"Plotting failed: {e}")

    print("\nTip: plot this result again anytime without re-profiling:")
    print(f"  python tests/cache_perf.py --from-json {json_file} --scale both\n")


if __name__ == '__main__':
    main()
