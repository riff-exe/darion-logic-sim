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
        
        # Load DFF.json or DFFSR.json from common locations
        for p in [
            os.path.join(_SCRIPT_DIR, "DFF.json"),
            os.path.join(_PROJECT_ROOT, "tests", "src", "DFF.json"),
            os.path.join(_PROJECT_ROOT, "DFF.json"),
            os.path.join(_PROJECT_ROOT, "tests", "DFF.json"),
            "DFF.json",
            os.path.join(_SCRIPT_DIR, "DFFSR.json"),
            os.path.join(_PROJECT_ROOT, "tests", "src", "DFFSR.json"),
            os.path.join(_PROJECT_ROOT, "tests", "DFFSR.json"),
            "DFFSR.json",
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
            if len(dff_inst.inputs) > 2:
                c1_gate = get_const_node("1'b1")
                self.circuit.connect(dff_inst.inputs[2], c1_gate, 0)
            if len(dff_inst.inputs) > 3:
                c1_gate = get_const_node("1'b1")
                self.circuit.connect(dff_inst.inputs[3], c1_gate, 0)

        self.dff_connections = dff_connections
        self.circuit.simulate(self.const.COMPILE)


# ---------------------------------------------------------------------------------------------------------------
# Export of structural gate-primitive netlists (ISCAS85 / EPFL_parsed .v) to other simulators' formats, for a
# gate-for-gate comparison. No Darion engine is involved. Every Verilog gate becomes ONE native gate of the target
# tool (no LUTs, no macros); `buf` has no Digital gate and is merged into its input net (a wire), which is
# recorded in the printed summary. Nets are connected by name through Tunnels placed directly on the pins, so no
# wire routing is needed. Verified by running the generated circuit against vectors from an independent evaluator.
#   python scripts/iscas_parser.py tests/ISCAS85/c432.v --export dig|circ --out <dir> [--vectors 1000]
#   dig : check with  java -cp Digital.jar CLI test -circ c432.dig -tests c432_tests.dig  (expects "passed")
#   circ: Logisim-evolution 5.0.0's `-w` test-vector mode fails headless, so write constant-input variants and run each
#         with  java -Djava.awt.headless=true -jar logisim-evolution.jar --tty table c432_v0.circ  against c432_expected.txt
# ---------------------------------------------------------------------------------------------------------------
_GATE_RE = re.compile(r'^\s*(and|nand|or|nor|xor|xnor|not|buf)\s+\w+\s*\(([^)]*)\)\s*;', re.M)
_PY_EVAL = {
    'and': lambda v: int(all(v)), 'nand': lambda v: int(not all(v)), 'or': lambda v: int(any(v)),
    'nor': lambda v: int(not any(v)), 'xor': lambda v: sum(v) & 1, 'xnor': lambda v: 1 - (sum(v) & 1),
    'not': lambda v: 1 - v[0], 'buf': lambda v: v[0],
}

def parse_gate_netlist(path):
    text = re.sub(r'//.*', '', open(path).read())
    if re.search(r"\bassign\b|1'b", text):
        raise ValueError(f"{path}: assign statements or constants are not supported by the exporter")
    def names(kw):
        out = []
        for m in re.finditer(r'^\s*' + kw + r'\s+([^;]*);', text, re.M):
            out += [x.strip() for x in m.group(1).replace('\n', ' ').split(',') if x.strip()]
        return out
    gates = []
    for m in _GATE_RE.finditer(text):
        pins = [x.strip() for x in m.group(2).split(',')]
        gates.append((m.group(1), pins[0], pins[1:]))
    return names('input'), names('output'), gates

def _resolve_buffers(inputs, outputs, gates):
    """Merge every buf into its input net. Returns (real gates with resolved nets, net->canonical net, #buffers)."""
    alias = {}
    for t, o, ins in gates:
        if t == 'buf':
            alias[o] = ins[0]
    def canon(n):
        while n in alias:
            n = alias[n]
        return n
    real = [(t, canon(o), [canon(i) for i in ins]) for t, o, ins in gates if t != 'buf']
    return real, canon, len(alias)

def _dig_pins(n):
    """Input pin y offsets (multiples of 20) and output y offset of a Digital gate with n inputs: odd n is a contiguous
    column, even n leaves the middle slot free."""
    if n % 2:
        return [20 * i for i in range(n)], 10 * (n - 1)
    h = n // 2
    return [20 * i for i in range(h)] + [20 * (i + 1) for i in range(h, n)], 10 * n

def write_dig(path, inputs, outputs, gates, columns=40):
    real, canon, nbuf = _resolve_buffers(inputs, outputs, gates)
    dig_name = {'and': 'And', 'nand': 'NAnd', 'or': 'Or', 'nor': 'NOr', 'xor': 'XOr', 'xnor': 'XNOr', 'not': 'Not'}
    L = ['<?xml version="1.0" encoding="utf-8"?>', '<circuit>', '  <version>1</version>', '  <attributes/>', '  <visualElements>']
    def element(name, x, y, attrs=''):
        L.append(f'    <visualElement><elementName>{name}</elementName><elementAttributes>{attrs}</elementAttributes><pos x="{x}" y="{y}"/></visualElement>')
    def entry(k, kind, v):
        return f'<entry><string>{k}</string><{kind}>{v}</{kind}></entry>'
    def tunnel(x, y, net):
        element('Tunnel', x, y, entry('NetName', 'string', net))
    x0 = 100
    for i, name in enumerate(inputs):                     # primary inputs down the left edge, each with a tunnel
        element('In', x0, 20 * i * 2, entry('Label', 'string', name)); tunnel(x0, 20 * i * 2, canon(name))
    for i, name in enumerate(outputs):                    # primary outputs
        element('Out', x0 + 200, 20 * i * 2, entry('Label', 'string', name)); tunnel(x0 + 200, 20 * i * 2, canon(name))
    base_x = x0 + 600
    row_h = 20 * 22
    for gi, (t, o, ins) in enumerate(real):
        gx = base_x + (gi % columns) * 200
        gy = (gi // columns) * row_h
        n = len(ins)
        attrs = ''
        if t == 'not':
            attrs = entry('wideShape', 'boolean', 'true'); offs, oy = [0], 0
        else:
            attrs = entry('Inputs', 'int', n) if n != 2 else ''
            offs, oy = _dig_pins(n)
        element(dig_name[t], gx, gy, attrs)
        for off, net in zip(offs, ins):
            tunnel(gx, gy + off, net)
        tunnel(gx + (80 if t in ('nand', 'nor', 'xnor') else 60), gy + oy, o)   # inverting gates are 20 wider (probed)
    L += ['  </visualElements>', '  <wires/>', '</circuit>']
    open(path, 'w').write('\n'.join(L) + '\n')
    return {'gates': len(real), 'buffers_merged': nbuf, 'inputs': len(inputs), 'outputs': len(outputs)}

def write_dig_tests(path, inputs, outputs, gates, n, seed=42):
    """Digital test-case file (header of signal names, one row per vector) with expected outputs from a plain-Python
    evaluator of the original Verilog netlist, which is independent of every simulator under test."""
    rng = random.Random(seed)
    order = []
    # topological evaluation of the gates (the netlists are combinational DAGs)
    drivers = {o: (t, ins) for t, o, ins in gates}
    def value(net, val, memo):
        if net in val: return val[net]
        if net in memo: return memo[net]
        t, ins = drivers[net]
        r = _PY_EVAL[t]([value(i, val, memo) for i in ins]); memo[net] = r; return r
    sys.setrecursionlimit(100000)
    rows = [' '.join(inputs + outputs)]
    for _ in range(n):
        val = {nm: rng.randint(0, 1) for nm in inputs}; memo = {}
        rows.append(' '.join(str(val[nm]) for nm in inputs) + ' ' + ' '.join(str(value(nm, val, memo)) for nm in outputs))
    # Digital reads a test file as a circuit file holding a Testcase element
    open(path, 'w').write('<?xml version="1.0" encoding="utf-8"?>\n<circuit><version>1</version><attributes/><visualElements>'
                          '<visualElement><elementName>Testcase</elementName><elementAttributes><entry><string>Testdata</string>'
                          '<testData><dataString>' + '\n'.join(rows) + '</dataString></testData></entry></elementAttributes>'
                          '<pos x="0" y="0"/></visualElement></visualElements><wires/></circuit>\n')

_CIRC_HDR = ('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<project source="5.0.0" version="1.0">\n'
             '  <lib desc="#Wiring" name="0"/>\n  <lib desc="#Gates" name="1"/>\n  <main name="main"/>\n'
             '  <circuit name="main">\n    <a name="appearance" val="logisim_evolution"/>\n    <a name="circuit" val="main"/>\n')

def _circ_pins(n):
    """y offsets of the inputs of a size-30 Logisim gate: multiples of 10 centred on the output, middle slot skipped for even n."""
    if n % 2:
        return [10 * (i - (n - 1) // 2) for i in range(n)]
    h = n // 2
    return [10 * (i - h) for i in range(h)] + [10 * (i - h + 1) for i in range(h, n)]

def write_circ(path, inputs, outputs, gates, input_values=None, columns=40):
    """Logisim-evolution circuit. Same construction as write_dig (one native gate per Verilog gate, nets joined by
    Tunnels on the pins). Logisim IGNORES an unconnected gate input instead of reporting an error, so a wrong pin
    offset silently changes the logic: always verify against vectors. With input_values (net -> 0/1) the primary
    inputs are Constants instead of Pins, so one vector can be evaluated headless with `--tty table`."""
    real, canon, nbuf = _resolve_buffers(inputs, outputs, gates)
    lg_name = {'and': 'AND Gate', 'nand': 'NAND Gate', 'or': 'OR Gate', 'nor': 'NOR Gate', 'xor': 'XOR Gate',
               'xnor': 'XNOR Gate', 'not': 'NOT Gate'}
    in_dx = {'and': 30, 'or': 30, 'nand': 40, 'nor': 40, 'xor': 40, 'xnor': 50, 'not': 30}   # input pin distance left of the output (probed)
    L = [_CIRC_HDR]
    def comp(lib, x, y, name, **a):
        L.append(f'    <comp lib="{lib}" loc="({x},{y})" name="{name}">' + ''.join(f'<a name="{k}" val="{v}"/>' for k, v in a.items()) + '</comp>\n')
    def tunnel(x, y, net):
        comp(0, x, y, 'Tunnel', label=net)
    x0 = 200
    for i, name in enumerate(inputs):
        y = 40 * i + 40
        if input_values is None:
            comp(0, x0, y, 'Pin', label=name, appearance='NewPins')
        else:
            comp(0, x0, y, 'Constant', value=hex(input_values[name]), width='1')
        tunnel(x0, y, canon(name))
    for i, name in enumerate(outputs):
        y = 40 * i + 40
        comp(0, x0 + 300, y, 'Pin', label=name, output='true')
        tunnel(x0 + 300, y, canon(name))
    base_x = x0 + 800
    row_h = 10 * 24
    for gi, (t, o, ins) in enumerate(real):
        gx = base_x + (gi % columns) * 200
        gy = (gi // columns) * row_h + 60
        n = len(ins)
        if t == 'not':
            comp(1, gx, gy, lg_name[t], size='30'); offs = [0]
        else:
            comp(1, gx, gy, lg_name[t], size='30', inputs=str(n)); offs = _circ_pins(n)
        for off, net in zip(offs, ins):
            tunnel(gx - in_dx[t], gy + off, net)
        tunnel(gx, gy, o)
    L.append('  </circuit>\n</project>\n')
    open(path, 'w').write(''.join(L))
    return {'gates': len(real), 'buffers_merged': nbuf, 'inputs': len(inputs), 'outputs': len(outputs)}

def write_circ_vectors(base, inputs, outputs, gates, n, seed=42):
    """n constant-input variants base_v<k>.circ plus base_expected.txt (one line per variant: the output bits from the
    independent Python evaluator). Run each with:  java -Djava.awt.headless=true -jar logisim.jar --tty table <file>"""
    rng = random.Random(seed)
    drivers = {o: (t, ins) for t, o, ins in gates}
    def value(net, val, memo):
        if net in val: return val[net]
        if net in memo: return memo[net]
        t, ins = drivers[net]
        r = _PY_EVAL[t]([value(i, val, memo) for i in ins]); memo[net] = r; return r
    sys.setrecursionlimit(100000)
    with open(base + '_expected.txt', 'w') as f:
        for k in range(n):
            val = {nm: rng.randint(0, 1) for nm in inputs}
            write_circ(f'{base}_v{k}.circ', inputs, outputs, gates, input_values=val)
            f.write(' '.join(str(value(nm, val, {})) for nm in outputs) + '\n')

def flatten_darion_json(path):
    """Gate-for-gate netlist of what Darion simulates, from its own JSON (sequential circuits included: the DFF/DFFSR
    ICs are expanded into their gates, so a flip-flop is built from the same NAND/NOT gates in the other tool).
    Returns (inputs, outputs, gates, names): inputs/outputs are net labels ("I<loc>" / "O<loc>"), gates are
    (type, out_net, [in_nets]) with pass-through pins as 'buf', names maps label -> Darion component name."""
    import json
    tmap = {0: 'and', 1: 'nand', 2: 'or', 3: 'nor', 4: 'xor', 5: 'xnor', 6: 'buf', 7: 'not', 8: 'buf', 10: 'buf'}
    flat = {}
    def walk(entries, top):
        for e in entries:
            if e[1] == 11:
                walk(e[4], False)
            else:
                flat[e[2]] = (e[0], e[1], e[4], top)
    walk(json.load(open(path)), True)
    net = lambda loc: ('I%d' % loc) if flat[loc][1] == 9 else ('n%d' % loc)
    inputs, outputs, gates, names = [], [], [], {}
    for loc, (name, t, src, top) in sorted(flat.items()):
        if t == 9:
            inputs.append('I%d' % loc); names['I%d' % loc] = name
        elif top and t == 10 and name.startswith('OUT_'):
            outputs.append('O%d' % loc); names['O%d' % loc] = name
            gates.append(('buf', 'O%d' % loc, [net(src[0])]))
        else:
            if any(x == -1 for x in src):
                raise ValueError(f"{path}: gate {name} at {loc} has an unconnected input")
            gates.append((tmap[t], 'n%d' % loc, [net(x) for x in src]))
    return inputs, outputs, gates, names

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
    parser.add_argument('--export', choices=('dig', 'circ'), help="Export a gate-primitive .v file to another simulator's format instead of JSON (needs a file path)")
    parser.add_argument('--out', default='.', help="--export: output directory")
    parser.add_argument('--vectors', type=int, default=1000, help="--export: number of random test vectors (with expected outputs) to write")
    args = parser.parse_args()

    if args.export:
        inputs, outputs, gates = parse_gate_netlist(args.path)
        os.makedirs(args.out, exist_ok=True)
        base = os.path.join(args.out, os.path.basename(args.path)[:-2])
        if args.export == 'dig':
            info = write_dig(base + '.dig', inputs, outputs, gates)
            write_dig_tests(base + '_tests.dig', inputs, outputs, gates, args.vectors)
            print(f"wrote {base}.dig and {base}_tests.dig: {info}")
        else:
            info = write_circ(base + '.circ', inputs, outputs, gates)
            write_circ_vectors(base, inputs, outputs, gates, min(args.vectors, 20))
            print(f"wrote {base}.circ and {min(args.vectors, 20)} constant-input variants {base}_v*.circ + {base}_expected.txt: {info}")
        return

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
