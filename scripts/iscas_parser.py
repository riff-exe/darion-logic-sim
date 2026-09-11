import os
import glob
import re
import sys
import argparse
import random

# Add the project root to sys.path so we can import engine/reactor dependencies
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_SCRIPT_DIR)
sys.path.insert(0, _PROJECT_ROOT)
sys.path.insert(0, os.path.join(_PROJECT_ROOT, 'reactor')) # Force reactor mode
import Circuit
import Const

class ISCASVerilogRunner:
    def __init__(self, v_file_path, circuit_cls, const_mod, randomize_gates=False):
        self.Circuit = circuit_cls
        self.const = const_mod
        self.circuit = self.Circuit()
        self.circuit.simulate(self.const.DESIGN)
        self.nodes = {}
        self.outputs = []
        self.input_vars = []
        self.dff_connections = []
        self.dff_crct = None
        self.is_sequential = False
        
        self.VERILOG_GATE_MAP = {
            'and': self.const.AND_ID, 'nand': self.const.NAND_ID, 'or': self.const.OR_ID,
            'nor': self.const.NOR_ID, 'xor': self.const.XOR_ID, 'xnor': self.const.XNOR_ID,
            'not': self.const.NOT_ID, 'buf': self.const.BUFFER_ID
        }
        
        # Load DFF.json from common locations
        for p in [
            os.path.join(_SCRIPT_DIR, "DFF.json"),
            os.path.join(_PROJECT_ROOT, "DFF.json"),
            os.path.join(_PROJECT_ROOT, "tests", "DFF.json"),
            "DFF.json",
        ]:
            if os.path.exists(p):
                try:
                    self.dff_crct = self.circuit.get_ic(p)
                    break
                except Exception:
                    pass

        self.randomize_gates = randomize_gates
        self._parse_verilog(v_file_path)
        self.output_objects = [self.nodes[p] for p in self.outputs if p in self.nodes]

    def _parse_verilog(self, filepath):
        if filepath.endswith('.json'):
            self.circuit.readfromjson(filepath)
            for gate in (self.circuit.get_components() if hasattr(self.circuit, 'get_components') else self.circuit.components):
                name_str = getattr(gate, 'custom_name', None) or getattr(gate, 'codename', None) or str(gate)
                if isinstance(name_str, bytes):
                    name_str = name_str.decode('utf-8')
                if 'dff' in name_str.lower() or 'DFF' in name_str:
                    self.is_sequential = True
            return

        with open(filepath, 'r', encoding='utf-8') as f:
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

        self.const_1_node = None
        self.const_0_node = None

        def get_const_node(val_str):
            if val_str == "1'b1":
                if not getattr(self, 'const_1_node', None):
                    self.const_1_node = self.circuit.getcomponent(getattr(self.const, 'VARIABLE_ID', 6))
                    self.const_1_node.rename("CONST_1")
                    self.nodes["1'b1"] = self.const_1_node
                return self.const_1_node
            elif val_str == "1'b0":
                if not getattr(self, 'const_0_node', None):
                    self.const_0_node = self.circuit.getcomponent(getattr(self.const, 'VARIABLE_ID', 6))
                    self.const_0_node.rename("CONST_0")
                    self.nodes["1'b0"] = self.const_0_node
                return self.const_0_node
            return None

        gate_statements = []

        # First pass: identify inputs, outputs, and gather gate statements
        for stmt in statements:
            if stmt.startswith('input ') or stmt.startswith('input\n') or stmt.startswith('input\t'):
                ports = re.sub(r'^\s*input\s+', '', stmt).split(',')
                for p in ports:
                    p = p.strip()
                    if p:
                        var_node = self.circuit.getcomponent(self.const.VARIABLE_ID)
                        var_node.rename(f"IN_{p}")
                        self.nodes[p] = var_node
                        self.input_vars.append(var_node)
            elif stmt.startswith('output ') or stmt.startswith('output\n') or stmt.startswith('output\t'):
                ports = re.sub(r'^\s*output\s+', '', stmt).split(',')
                for p in ports:
                    p = p.strip()
                    if p:
                        out_node = self.circuit.getcomponent(self.const.IC_OUTPUT_PIN_ID)
                        out_node.rename(f"OUT_{p}")
                        self.nodes[p + "_OUTPIN"] = out_node
                        self.outputs.append(p)
                        connections.append((p + "_OUTPIN", [p]))
            elif stmt.startswith(('wire ', 'wire\n', 'wire\t', 'module ', 'module\n', 'module\t', 'endmodule', 'reg ', 'reg\n', 'reg\t')):
                continue
            else:
                match = re.match(r'^([a-zA-Z_]\w*)\s+([a-zA-Z_0-9]+)?\s*\((.*)\)$', stmt, flags=re.DOTALL)
                if match:
                    gate_statements.append(match)

        # If --random is specified, shuffle the gate creation order
        if self.randomize_gates:
            random.shuffle(gate_statements)

        # Second pass: create gates in potentially random order
        for match in gate_statements:
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

                for w in in_wires:
                    get_const_node(w)

                if gate_id < getattr(self.const, 'VARIABLE_ID', 99) and hasattr(self.circuit, 'setlimits'):
                    self.circuit.setlimits(gate, len(in_wires))

                self.nodes[out_wire] = gate
                connections.append((out_wire, in_wires))

        # Final pass: establish connections
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

        self.dff_connections = dff_connections
        self.circuit.simulate(self.const.COMPILE)

def process_iscas_file(in_path, out_path, randomize):
    print(f"Parsing {in_path} to {out_path} {'(RANDOMIZED)' if randomize else ''}...")
    try:
        runner = ISCASVerilogRunner(in_path, Circuit.Circuit, Const, randomize_gates=randomize)
        # runner.circuit.optimize()
        runner.circuit.writetojson(out_path)
        circuit_type = "ISCAS89 Sequential" if runner.is_sequential else "ISCAS85 Combinational"
        print(f"Successfully dumped {out_path} ({circuit_type})")
    except Exception as e:
        print(f"Failed to dump {out_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Parse ISCAS85 and ISCAS89 verilog files to JSON format")
    parser.add_argument('path', nargs='?', default=None, help="Optional path to a .v file or directory containing .v files")
    parser.add_argument('--random', action='store_true', help="Randomize the creation order of gates in the JSON output")
    args = parser.parse_args()

    if args.path:
        if os.path.isfile(args.path):
            out_path = args.path.replace('.v', '.json')
            process_iscas_file(args.path, out_path, args.random)
        elif os.path.isdir(args.path):
            files = sorted(glob.glob(os.path.join(args.path, '*.v')))
            for f in files:
                out_name = os.path.basename(f).replace('.v', '.json')
                out_path = os.path.join(args.path, out_name)
                process_iscas_file(f, out_path, args.random)
            print(f"Done parsing and dumping benchmarks in {args.path}.")
        else:
            print(f"Error: Path {args.path} not found.")
            sys.exit(1)
        return

    dirs_to_process = [
        os.path.join(_PROJECT_ROOT, 'tests', 'ISCAS85'),
        os.path.join(_PROJECT_ROOT, 'tests', 'ISCAS89')
    ]

    for source_dir in dirs_to_process:
        if os.path.exists(source_dir):
            files = sorted(glob.glob(os.path.join(source_dir, '*.v')))
            for f in files:
                out_name = os.path.basename(f).replace('.v', '.json')
                out_path = os.path.join(source_dir, out_name)
                process_iscas_file(f, out_path, args.random)
            print(f"Done parsing and dumping benchmarks in {source_dir}.")

if __name__ == '__main__':
    main()
