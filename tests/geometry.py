import os
import sys
import glob
import numpy as np
import matplotlib.pyplot as plt

# --- PATH RESOLUTION ---
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.insert(0, os.path.join(root_dir, 'reactor'))
sys.path.insert(0, current_dir)

import Circuit
import Const

class JSONCircuitLoader:
    def __init__(self, filepath, circuit_cls, const_mod):
        self.filepath = filepath
        self.Circuit = circuit_cls
        self.const = const_mod
        self.circuit = self.Circuit()
        self.circuit.simulate(self.const.DESIGN)
        
        self.is_sequential = False
        self._load()
        
    def _load(self):
        if not self.filepath.endswith('.json'):
            raise ValueError(
                f"Geometry analysis is permanently JSON-based. Cannot load '{self.filepath}'. "
                "Only .json circuit files are supported."
            )
        self.circuit.readfromjson(self.filepath)
        for gate in (self.circuit.get_components() if hasattr(self.circuit, 'get_components') else self.circuit.components):
            name_str = getattr(gate, 'custom_name', None) or getattr(gate, 'codename', None) or str(gate)
            if isinstance(name_str, bytes):
                name_str = name_str.decode('utf-8')
            if 'dff' in name_str.lower() or 'DFF' in name_str:
                self.is_sequential = True
                break

# Backwards compatibility alias
HybridParser = JSONCircuitLoader


def _process_jumps(jumps, filename, ctype, label, output_dir):
    if not jumps:
        return None
        
    jumps_arr = np.array(jumps)
    total_edges = len(jumps_arr)
    if total_edges == 0:
        return None
        
    mean_jump = np.mean(jumps_arr)
    max_jump = np.max(jumps_arr)
    
    adj_edges = np.sum(jumps_arr == 1)
    l1_edges = np.sum((jumps_arr > 1) & (jumps_arr <= 8))
    l2_edges = np.sum((jumps_arr > 8) & (jumps_arr <= 64))
    far_edges = np.sum(jumps_arr > 64)
    
    pct_adj = (adj_edges / total_edges) * 100
    pct_near = (l1_edges / total_edges) * 100
    pct_med = (l2_edges / total_edges) * 100
    pct_far = (far_edges / total_edges) * 100
    
    # 2. Generate Histogram Plot
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6))

    bins = np.logspace(0, np.log10(max_jump) if max_jump > 0 else 1, 100)
    
    ax.hist(jumps_arr, bins=bins, color='cyan', alpha=0.7, edgecolor='black')
    
    ax.axvline(1, color='green', linestyle=':', alpha=0.8, label='Adjacent')
    ax.axvline(8, color='yellow', linestyle='--', alpha=0.8, label='Near Bound (8)')
    ax.axvline(64, color='red', linestyle='--', alpha=0.8, label='Med Bound (64)')

    ax.set_xscale('log')
    ax.set_yscale('log')
    
    ax.set_title(f"Memory Locality Profile: {filename} ({label})\n{ctype}", fontsize=14, pad=15)
    ax.set_xlabel("Jump Distance (Indices)", fontsize=12)
    ax.set_ylabel("Frequency (Number of Edges)", fontsize=12)
    
    ax.grid(True, alpha=0.15)
    ax.legend()
    
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        save_path = os.path.join(output_dir, f"{filename}_{label}_geometry.png")
        plt.tight_layout()
        plt.savefig(save_path, dpi=150)
    plt.close()

    return {
        'circuit': f"{filename} ({label})",
        'type': 'Seq' if 'Sequential' in ctype else 'Comb',
        'edges': total_edges,
        'adj': pct_adj,
        'near': pct_near,
        'med': pct_med,
        'far': pct_far
    }


def _heap_stats(layout):
    """Compute physical hitlist buffer address stats from hitlist_mem_layout() output."""
    if not layout:
        return None
    addrs = np.array([a for _, a, _, _ in layout], dtype=np.int64)
    sizes = np.array([s for _, _, s, _ in layout], dtype=np.int64)
    deltas = np.diff(addrs)
    MB = 1024 * 1024
    if len(deltas) == 0:
        return None
    return {
        'n_buffers':   len(addrs),
        'total_edges': int(sizes.sum()),
        'span_mb':     float((addrs.max() - addrs.min()) / MB),
        'mean_delta':  float(np.mean(np.abs(deltas))),
        'median_delta':float(np.median(np.abs(deltas))),
        'fwd_pct':     float(np.sum(deltas > 0) / len(deltas) * 100),
        'max_fanout':  int(sizes.max()),
        'mean_fanout': float(sizes.mean()),
    }


def analyze_file(filepath, output_dir):
    filename = os.path.basename(filepath)

    try:
        loader = JSONCircuitLoader(filepath, Circuit.Circuit, Const)
        ctype = "Sequential" if loader.is_sequential else "Combinational"

        jumps_unopt = loader.circuit.geometry()
        unopt_res = _process_jumps(jumps_unopt, filename, ctype, "Unopt", output_dir)

        # Heap layout BEFORE optimize — switch to SIMULATE so hitlists are populated
        unopt_heap = None
        if hasattr(loader.circuit, 'hitlist_mem_layout'):
            try:
                loader.circuit.simulate(Const.SIMULATE)
                vars_ = loader.circuit.get_variables()
                if vars_:
                    for v in vars_[:min(4, len(vars_))]:
                        loader.circuit.toggle(v, Const.HIGH)
                        loader.circuit.toggle(v, Const.LOW)
                unopt_heap = _heap_stats(loader.circuit.hitlist_mem_layout())
                loader.circuit.simulate(Const.DESIGN)   # restore design mode
            except Exception:
                pass

        if hasattr(loader.circuit, 'optimize'):
            loader.circuit.optimize()
        jumps_opt = loader.circuit.geometry()
        opt_res = _process_jumps(jumps_opt, filename, ctype, "Opt", output_dir)

        # Heap layout AFTER optimize
        opt_heap = None
        if hasattr(loader.circuit, 'hitlist_mem_layout'):
            try:
                loader.circuit.simulate(Const.SIMULATE)
                vars_ = loader.circuit.get_variables()
                if vars_:
                    for v in vars_[:min(4, len(vars_))]:
                        loader.circuit.toggle(v, Const.HIGH)
                        loader.circuit.toggle(v, Const.LOW)
                opt_heap = _heap_stats(loader.circuit.hitlist_mem_layout())
                loader.circuit.simulate(Const.DESIGN)
            except Exception:
                pass

    except Exception as e:
        print(f"Error processing {filename}: {e}")
        return None

    results = []
    if unopt_res:
        if unopt_heap:
            unopt_res['heap'] = unopt_heap
        results.append(unopt_res)
    if opt_res:
        if opt_heap:
            opt_res['heap'] = opt_heap
        results.append(opt_res)

    return results

def print_batch_summary(results):
    if not results:
        return
    print("\n" + "="*100)
    print(" BATCH GEOMETRY ANALYSIS SUMMARY REPORT — LOGICAL JUMP DISTANCES")
    print("="*100)
    print(" Jump Distance Zones:")
    print("   Adj (Adjacent) : Jump of 1 index (Ideal locality)")
    print("   Near           : Jump of 2-8 indices")
    print("   Med (Medium)   : Jump of 9-64 indices")
    print("   Far            : Jump > 64 indices (High cache miss risk)")
    print("-" * 100)
    print(f"{'Circuit':<25} | {'Type':<4} | {'Edges':>10} | {'Adj %':>7} | {'Near %':>7} | {'Med %':>7} | {'Far %':>7}")
    print("-" * 100)

    for r in results:
        print(f"{r['circuit']:<25} | {r['type']:<4} | {r['edges']:10,} | {r['adj']:6.1f}% | {r['near']:6.1f}% | {r['med']:6.1f}% | {r['far']:6.1f}%")

    print("="*100 + "\n")


def print_heap_summary(results):
    """Print physical hitlist buffer heap locality before vs after optimize()."""
    # Only show rows that have heap data and come in (Unopt, Opt) pairs
    heap_rows = [(r['circuit'].replace(' (Unopt)', '').replace(' (Opt)', ''), r)
                 for r in results if 'heap' in r]
    if not heap_rows:
        return

    # Group by base circuit name
    seen = {}
    for name, r in heap_rows:
        seen.setdefault(name, {})
        stage = 'unopt' if 'Unopt' in r['circuit'] else 'opt'
        seen[name][stage] = r['heap']

    W = 130
    print("\n" + "="*W)
    print(" HITLIST PHYSICAL HEAP LOCALITY REPORT")
    print("="*W)
    print(" Measures actual C++ hitlist.data() buffer addresses (via hitlist_mem_layout()).")
    print(" Median|Δ|: median byte distance between consecutive hitlist buffers in traversal order.")
    print(" FwdAddr%:  % of consecutive buffer pairs where next_addr > prev_addr (100% = fully linear alloc).")
    print(" Defrag ratio = Before_median / After_median  (higher = more dramatic compaction from optimize()).")
    print("-"*W)
    hdr = (f"{'Circuit':<22} | {'Buffers':>7} | "
           f"{'Before Median|Δ|(B)':>20} | {'Before Fwd%':>11} | "
           f"{'After Median|Δ|(B)':>19} | {'After Fwd%':>10} | "
           f"{'Defrag Ratio':>12} | {'Max Fanout':>10}")
    print(hdr)
    print("-"*W)

    for name, stages in sorted(seen.items()):
        u = stages.get('unopt')
        o = stages.get('opt')
        if not u or not o:
            continue
        ratio = u['median_delta'] / o['median_delta'] if o['median_delta'] > 0 else float('inf')
        short = name.split('(')[0].strip()[:22]
        print(f"{short:<22} | {u['n_buffers']:>7,} | "
              f"{u['median_delta']:>20,.0f} | {u['fwd_pct']:>10.1f}% | "
              f"{o['median_delta']:>19,.0f} | {o['fwd_pct']:>9.1f}% | "
              f"{ratio:>11,.0f}x | {o['max_fanout']:>10,}")

    print("="*W + "\n")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Circuit Geometry Analyzer (JSON-based)')
    parser.add_argument('target', nargs='?', type=str, help='Path to a .json file or directory containing .json files')
    parser.add_argument('--dump', action='store_true', help='Dump output to time-stamped txt in test_result')
    parser.add_argument('--plot', action='store_true', help='Generate plots in test_result')
    args = parser.parse_args()

    target = args.target
    if not target:
        target = input("Enter path to .json file or directory: ").strip()

    target = os.path.abspath(target)
    if not os.path.exists(target):
        print(f"Error: Target path '{target}' does not exist.")
        sys.exit(1)

    circuit_files = []
    if os.path.isdir(target):
        circuit_files = glob.glob(os.path.join(target, "*.json"))
        if not circuit_files:
            circuit_files = glob.glob(os.path.join(target, "**", "*.json"), recursive=True)
        if not circuit_files:
            print(f"No .json files found in directory '{target}'.")
            sys.exit(1)
        circuit_files = sorted(list(set(circuit_files)))
    elif os.path.isfile(target):
        if target.endswith('.v'):
            json_alt = target[:-2] + '.json'
            if os.path.exists(json_alt):
                print(f"[Note] Geometry is permanently JSON-based. Automatically using '{os.path.basename(json_alt)}' instead.")
                circuit_files = [json_alt]
            else:
                print(f"Error: Geometry is permanently JSON-based (.v files are not supported). No matching '{json_alt}' found.")
                sys.exit(1)
        elif target.endswith('.json'):
            circuit_files = [target]
        else:
            print(f"Error: Target file '{target}' must be a .json file.")
            sys.exit(1)
    else:
        print(f"Invalid target: '{target}'")
        sys.exit(1)

    if getattr(args, 'plot', False):
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        plots_dir = os.path.join(current_dir, 'test_result', 'geometry', 'plots', timestamp)
    else:
        plots_dir = None

    results = []
    
    class _Tee:
        def __init__(self, *streams):
            self.streams = streams
        def write(self, data):
            for s in self.streams:
                s.write(data)
        def flush(self):
            for s in self.streams:
                s.flush()

    _orig = sys.stdout
    if getattr(args, 'dump', False):
        import datetime
        dump_dir = os.path.join(current_dir, 'test_result', 'geometry', 'datas')
        os.makedirs(dump_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        _LOG = os.path.join(dump_dir, f"geometry_{timestamp}.txt")
        _lf = open(_LOG, "a", encoding="utf-8")
        sys.stdout = _Tee(_orig, _lf)
    else:
        _lf = None

    try:
        for filepath in circuit_files:
            res_list = analyze_file(filepath, plots_dir)
            if res_list:
                results.extend(res_list)
                
        if len(results) > 0:
            print_batch_summary(results)
            print_heap_summary(results)
        
        if plots_dir:
            print(f"Saved plots to: {plots_dir}")
    finally:
        sys.stdout = _orig
        if _lf:
            _lf.close()