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
        
        self.VERILOG_GATE_MAP = {
            'and': self.const.AND_ID, 'nand': self.const.NAND_ID, 'or': self.const.OR_ID,
            'nor': self.const.NOR_ID, 'xor': self.const.XOR_ID, 'xnor': self.const.XNOR_ID,
            'not': self.const.NOT_ID, 'buf': self.const.BUFFER_ID
        }
        
        self.randomize_gates = randomize_gates
        self._parse_verilog(v_file_path)

    def _parse_verilog(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        content = re.sub(r'//.*', '', content)
        statements = [s.strip() for s in content.split(';') if s.strip()]
        connections = []

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
            if stmt.startswith('input '):
                ports = stmt.replace('input', '').strip().split(',')
                for p in ports:
                    p = p.strip()
                    if p:
                        var_node = self.circuit.getcomponent(self.const.VARIABLE_ID)
                        var_node.rename(f"IN_{p}")
                        self.nodes[p] = var_node
                        self.input_vars.append(var_node)
            elif stmt.startswith('output '):
                ports = stmt.replace('output', '').strip().split(',')
                for p in ports:
                    p = p.strip()
                    if p:
                        out_node = self.circuit.getcomponent(self.const.IC_OUTPUT_PIN_ID)
                        out_node.rename(f"OUT_{p}")
                        self.nodes[p + "_OUTPIN"] = out_node
                        self.outputs.append(p)
                        connections.append((p + "_OUTPIN", [p]))
            elif stmt.startswith(('wire ', 'module ', 'endmodule', 'reg ')):
                continue
            else:
                match = re.match(r'^([a-zA-Z_]\w*)\s+([a-zA-Z_0-9]+)?\s*\((.*)\)$', stmt)
                if match:
                    gate_statements.append(match)

        # If --random is specified, shuffle the gate creation order
        if self.randomize_gates:
            random.shuffle(gate_statements)

        # Second pass: create gates in potentially random order
        for match in gate_statements:
            gate_type = match.group(1).lower()
            ports_str = match.group(3)
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
                    
        self.circuit.simulate(self.const.COMPILE)

def process_iscas_file(in_path, out_path, randomize):
    print(f"Parsing {in_path} to {out_path} {'(RANDOMIZED)' if randomize else ''}...")
    try:
        runner = ISCASVerilogRunner(in_path, Circuit.Circuit, Const, randomize_gates=randomize)
        # runner.circuit.optimize()
        runner.circuit.writetojson(out_path)
    except Exception as e:
        print(f"Failed to dump {out_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Parse ISCAS85 verilog files to JSON format")
    parser.add_argument('--random', action='store_true', help="Randomize the creation order of gates in the JSON output")
    args = parser.parse_args()

    source_dir = os.path.join(_PROJECT_ROOT, 'tests', 'ISCAS85')
    target_dir = source_dir
        
    if os.path.exists(source_dir):
        os.makedirs(target_dir, exist_ok=True)
        files = glob.glob(os.path.join(source_dir, '*.v'))
        for f in files:
            out_name = os.path.basename(f).replace('.v', '.json')
            out_path = os.path.join(target_dir, out_name)
            process_iscas_file(f, out_path, args.random)
            
    print(f"Done parsing and dumping ISCAS85 benchmarks to {target_dir}.")

if __name__ == '__main__':
    main()
