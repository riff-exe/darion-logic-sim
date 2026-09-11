import os
import sys
import glob
import re
import numpy as np
import matplotlib.pyplot as plt

# --- PATH RESOLUTION ---
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.insert(0, os.path.join(root_dir, 'reactor'))
sys.path.insert(0, current_dir)

import Circuit
import Const

class HybridParser:
    def __init__(self, filepath, circuit_cls, const_mod):
        self.filepath = filepath
        self.Circuit = circuit_cls
        self.const = const_mod
        self.circuit = self.Circuit()
        self.circuit.simulate(self.const.DESIGN)
        
        self.is_sequential = False
        self.nodes = {}
        
        self.VERILOG_GATE_MAP = {
            'and':  self.const.AND_ID,
            'nand': self.const.NAND_ID,
            'or':   self.const.OR_ID,
            'nor':  self.const.NOR_ID,
            'xor':  self.const.XOR_ID,
            'xnor': self.const.XNOR_ID,
            'not':  self.const.NOT_ID,
            'buf':  self.const.BUFFER_ID,
        }
        
        self.dff_crct = None
        for p in [os.path.join(current_dir, "DFF.json"), os.path.join(root_dir, "DFF.json")]:
            if os.path.exists(p):
                try:
                    self.dff_crct = self.circuit.get_ic(p)
                    break
                except:
                    pass
        
        self._parse()
        
    def _parse(self):
        if self.filepath.endswith('.json'):
            self.circuit.readfromjson(self.filepath)
            for gate in (self.circuit.get_components() if hasattr(self.circuit, 'get_components') else self.circuit.components):
                name_str = getattr(gate, 'custom_name', None) or getattr(gate, 'codename', None) or str(gate)
                if isinstance(name_str, bytes):
                    name_str = name_str.decode('utf-8')
                if 'dff' in name_str.lower() or 'DFF' in name_str:
                    self.is_sequential = True
            return

        with open(self.filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        content = re.sub(r'//.*', '', content)
        
        module_body = content
        for m in re.finditer(r'\bmodule\s+([a-zA-Z0-9_]+)(.*?)\bendmodule\b', content, flags=re.DOTALL):
            if m.group(1).lower() != 'dff':
                module_body = m.group(0)
                break
                
        statements = [s.strip() for s in module_body.split(';') if s.strip()]
        connections = []
        dff_connections = []
        
        for stmt in statements:
            if stmt.startswith('input '):
                ports = stmt.replace('input', '').strip().split(',')
                for p in ports:
                    p = p.strip()
                    if p:
                        var_node = self.circuit.getcomponent(self.const.VARIABLE_ID)
                        var_node.rename(f"IN_{p}")
                        self.nodes[p] = var_node
            elif stmt.startswith('output '):
                ports = stmt.replace('output', '').strip().split(',')
                for p in ports:
                    p = p.strip()
                    if p:
                        out_node = self.circuit.getcomponent(self.const.IC_OUTPUT_PIN_ID)
                        out_node.rename(f"OUT_{p}")
                        self.nodes[p + "_OUTPIN"] = out_node
                        connections.append((p + "_OUTPIN", [p]))
            elif stmt.startswith(('wire ', 'module ', 'endmodule', 'reg ')):
                continue
            else:
                match = re.match(r'^([a-zA-Z_]\w*)\s+([a-zA-Z_0-9]+)?\s*\((.*)\)$', stmt, flags=re.DOTALL)
                if not match:
                    continue
                gate_type = match.group(1).lower()
                ports_str = match.group(3)
                
                if gate_type.startswith('dff'):
                    self.is_sequential = True
                    if not self.dff_crct:
                        raise RuntimeError("DFF.json is required for sequential circuits but was not found.")
                        
                    wires = {}
                    if '.' in ports_str:
                        for pm in re.finditer(r'\.\s*([a-zA-Z0-9_]+)\s*\(\s*([a-zA-Z0-9_]+)\s*\)', ports_str):
                            wires[pm.group(1).upper()] = pm.group(2)
                        d_wire = wires.get('D')
                        clk_wire = wires.get('CK', wires.get('CLK', wires.get('C')))
                        q_wire = wires.get('Q')
                    else:
                        pts = [p.strip() for p in ports_str.split(',')]
                        clk_wire = pts[0] if len(pts) > 0 else None
                        q_wire = pts[1] if len(pts) > 1 else None
                        d_wire = pts[2] if len(pts) > 2 else None
                        
                    dff_inst = self.circuit.load_ic(self.dff_crct)
                    inst_name = match.group(2) or f"inst_{len(dff_connections)}"
                    if hasattr(dff_inst, 'rename'):
                        dff_inst.rename(f"DFF_{inst_name}")
                    else:
                        dff_inst.custom_name = f"DFF_{inst_name}"
                        
                    if q_wire:
                        self.nodes[q_wire] = dff_inst.outputs[0]
                        
                    dff_connections.append((dff_inst, d_wire, clk_wire))
                    continue

                if gate_type in self.VERILOG_GATE_MAP:
                    ports = [p.strip() for p in ports_str.split(',')]
                    out_wire = ports[0]
                    in_wires = ports[1:]
                    gate_id = self.VERILOG_GATE_MAP[gate_type]
                    gate = self.circuit.getcomponent(gate_id)
                    gate.rename(f"G_{out_wire}")
                    if gate_id < self.const.VARIABLE_ID and hasattr(self.circuit, 'setlimits'):
                        self.circuit.setlimits(gate, len(in_wires))
                    self.nodes[out_wire] = gate
                    
                    for w in in_wires:
                        if w == "1'b1":
                            if "1'b1" not in self.nodes:
                                const_1 = self.circuit.getcomponent(self.const.VARIABLE_ID)
                                const_1.rename("CONST_1")
                                self.nodes["1'b1"] = const_1
                        elif w == "1'b0":
                            if "1'b0" not in self.nodes:
                                const_0 = self.circuit.getcomponent(self.const.VARIABLE_ID)
                                const_0.rename("CONST_0")
                                self.nodes["1'b0"] = const_0
                    
                    connections.append((out_wire, in_wires))

        for target_id, source_ids in connections:
            target_gate = self.nodes.get(target_id)
            if not target_gate: continue
            for pin_index, source_id in enumerate(source_ids):
                source_gate = self.nodes.get(source_id)
                if source_gate:
                    self.circuit.connect(target_gate, source_gate, pin_index)
                    
        for dff_inst, d_wire, clk_wire in dff_connections:
            if clk_wire:
                clk_gate = self.nodes.get(clk_wire)
                if clk_gate and len(dff_inst.inputs) > 0:
                    self.circuit.connect(dff_inst.inputs[0], clk_gate, 0)
            if d_wire:
                d_gate = self.nodes.get(d_wire)
                if d_gate and len(dff_inst.inputs) > 1:
                    self.circuit.connect(dff_inst.inputs[1], d_gate, 0)
        
        pass


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


def analyze_file(filepath, output_dir):
    filename = os.path.basename(filepath)
    
    try:
        parser = HybridParser(filepath, Circuit.Circuit, Const)
        ctype = "ISCAS89 (Sequential)" if parser.is_sequential else "ISCAS85 (Combinational)"
        
        jumps_unopt = parser.circuit.geometry()
        unopt_res = _process_jumps(jumps_unopt, filename, ctype, "Unopt", output_dir)
        
        if hasattr(parser.circuit, 'optimize'):
            parser.circuit.optimize()
        jumps_opt = parser.circuit.geometry()
        opt_res = _process_jumps(jumps_opt, filename, ctype, "Opt", output_dir)
        
    except Exception as e:
        print(f"Error processing {filename}: {e}")
        return None
    
    results = []
    if unopt_res:
        results.append(unopt_res)
    if opt_res:
        results.append(opt_res)
        
    return results

def print_batch_summary(results):
    if not results:
        return
    print("\n" + "="*100)
    print(" BATCH GEOMETRY ANALYSIS SUMMARY REPORT")
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

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Circuit Geometry Analyzer')
    parser.add_argument('target', nargs='?', type=str, help='Path to a .v/.json file or directory containing them')
    parser.add_argument('--dump', action='store_true', help='Dump output to time-stamped txt in test_result')
    parser.add_argument('--plot', action='store_true', help='Generate plots in test_result')
    args = parser.parse_args()

    target = args.target
    if not target:
        target = input("Enter path to .v or .json file or directory: ").strip()

    target = os.path.abspath(target)
    if not os.path.exists(target):
        print(f"Error: Target path '{target}' does not exist.")
        sys.exit(1)

    circuit_files = []
    if os.path.isdir(target):
        for ext in ("*.v", "*.json"):
            circuit_files.extend(glob.glob(os.path.join(target, ext)))
        if not circuit_files:
            for ext in ("*.v", "*.json"):
                circuit_files.extend(glob.glob(os.path.join(target, "**", ext), recursive=True))
        if not circuit_files:
            print(f"No .v or .json files found in directory '{target}'.")
            sys.exit(1)
        circuit_files = sorted(list(set(circuit_files)))
    elif os.path.isfile(target):
        circuit_files = [target]
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
        
        if plots_dir:
            print(f"Saved plots to: {plots_dir}")
    finally:
        sys.stdout = _orig
        if _lf:
            _lf.close()