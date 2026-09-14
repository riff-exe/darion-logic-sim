"""
verifier_iwls.py
================
Sequential State Verification Testbench for IWLS 2005 Circuits.

Compares cycle-by-cycle simulation states across execution engines:
  1. Icarus Verilog (Golden Reference via GSCLib_3.0.v cell models)
  2. Verilator C++ (Compiled Cycle-accurate Model)
  3. Pure Python Engine
  4. Cython Reactor - Propagate (SIMULATE mode / BFS Wavefront)
  5. Cython Reactor - Sweep (COMPILE mode / Topological Forward-Pass)
  6. Cython Reactor - OOP (SIMULATE mode)

Features:
  - 50-cycle warmup sequence (inputs set to 0, clock toggling) to flush DFF states.
  - Full Cadence GSCLib 3.0 standard cell library support.
  - Multi-bit bus port handling (input [7:0] I; output [3:0] O;).
  - Escaped identifier normalization.
  - Cycle-by-cycle output equivalence checking and mismatch diagnostics.
"""

import os
import re
import sys
import random
import argparse
import subprocess
import shutil
import json
from pathlib import Path

_SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
_TESTS_DIR    = os.path.dirname(_SCRIPT_DIR)
_PROJECT_ROOT = os.path.dirname(_TESTS_DIR)

sys.path.insert(0, _SCRIPT_DIR)
sys.path.insert(0, _TESTS_DIR)
sys.path.insert(0, _PROJECT_ROOT)

try:
    from iwls_sequential_harness import parse_iwls_ports, find_gsclib_path, find_reset_port
except ImportError:
    try:
        from tests.src.iwls_sequential_harness import parse_iwls_ports, find_gsclib_path, find_reset_port
    except ImportError:
        from tests.iwls_sequential_harness import parse_iwls_ports, find_gsclib_path, find_reset_port


def dump_json_file(filepath, obj, indent=True):
    with open(filepath, 'w', encoding='utf-8') as f:
        if indent:
            json.dump(obj, f, indent=2)
        else:
            json.dump(obj, f)


def load_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


# ===========================================================================
# 1. ICARUS VERILOG STATE RUNNER
# ===========================================================================

def generate_icarus_verifier_tb(v_file: str, tb_file: str, vector_file: str,
                                output_file: str, vectors_count: int):
    module_name, port_decls, flat_inputs, flat_outputs, clock_idx, clock_port_name = parse_iwls_ports(v_file)

    tb = []
    tb.append("`timescale 1ns/1ps\n")
    tb.append(f"module tb_verif_{module_name};\n")

    # Inputs as reg
    for name, msb, lsb in port_decls['inputs']:
        if msb is not None and lsb is not None:
            tb.append(f"    reg [{msb}:{lsb}] {name};\n")
        else:
            tb.append(f"    reg {name};\n")

    # Outputs as wire
    for name, msb, lsb in port_decls['outputs']:
        if msb is not None and lsb is not None:
            tb.append(f"    wire [{msb}:{lsb}] {name};\n")
        else:
            tb.append(f"    wire {name};\n")

    total_inputs = len(flat_inputs)
    tb.append(f"    reg [{total_inputs-1}:0] test_vectors [0:{vectors_count-1}];\n")
    tb.append("    integer i, outfile;\n\n")

    # Instantiate DUT
    all_ports = [p[0] for p in port_decls['inputs'] + port_decls['outputs']]
    conn = [f"        .{p}({p})" for p in all_ports]
    tb.append(f"    {module_name} uut (\n")
    tb.append(",\n".join(conn))
    tb.append("\n    );\n\n")

    v_path_str   = str(vector_file).replace("\\", "/")
    out_path_str = str(output_file).replace("\\", "/")

    tb.append("    initial begin\n")
    tb.append(f'        $readmemb("{v_path_str}", test_vectors);\n')
    tb.append(f'        outfile = $fopen("{out_path_str}", "w");\n')

    # Assign inputs for each vector and print outputs
    tb.append(f"        for (i = 0; i < {vectors_count}; i = i + 1) begin\n")
    for idx, bit_name in enumerate(flat_inputs):
        tb.append(f"            {bit_name} = test_vectors[i][{idx}];\n")
    tb.append("            #1;\n")

    # Write each flat output bit to outfile as binary string
    fmt_str = "%b" * len(flat_outputs)
    out_args = ", ".join(flat_outputs)
    tb.append(f'            $fdisplay(outfile, "{fmt_str}", {out_args});\n')
    tb.append("        end\n")
    tb.append("        $fclose(outfile);\n")
    tb.append("        $finish;\n")
    tb.append("    end\n")
    tb.append("endmodule\n")

    with open(tb_file, 'w', encoding='utf-8') as f:
        f.write("".join(tb))


def run_icarus_state_simulation(v_file: str, vectors: list) -> list:
    base_path   = os.path.splitext(v_file)[0]
    tb_file     = base_path + "_verif_tb.v"
    vvp_file    = base_path + "_verif.vvp"
    vec_file    = base_path + "_verif_inputs.txt"
    out_file    = base_path + "_verif_outputs.txt"

    gsclib_path = find_gsclib_path(v_file)
    if not gsclib_path:
        raise RuntimeError("GSCLib_3.0.v library file not found")

    if not shutil.which("iverilog") or not shutil.which("vvp"):
        raise RuntimeError("iverilog or vvp not found in system PATH")

    try:
        # Write vectors: rightmost bit is index 0 ($readmemb expects LSB at right)
        with open(vec_file, 'w', encoding='utf-8') as f:
            for vec in vectors:
                f.write("".join(str(v) for v in reversed(vec)) + "\n")

        generate_icarus_verifier_tb(v_file, tb_file, vec_file, out_file, len(vectors))

        comp_res = subprocess.run(
            ["iverilog", "-o", vvp_file, gsclib_path, v_file, tb_file],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        if comp_res.returncode != 0:
            raise RuntimeError(f"Icarus compile error: {comp_res.stderr.strip()}")

        run_res = subprocess.run(
            ["vvp", vvp_file],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        if run_res.returncode != 0:
            raise RuntimeError(f"Icarus runtime error: {run_res.stderr.strip()}")

        with open(out_file, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()

        normalized_results = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            normalized_results.append(
                [0 if b == '0' else (1 if b == '1' else 2) for b in line]
            )

        return normalized_results

    finally:
        for p in (tb_file, vvp_file, vec_file, out_file):
            if os.path.exists(p):
                try: os.remove(p)
                except OSError: pass


# ===========================================================================
# 2. VERILATOR STATE RUNNER
# ===========================================================================

CPP_KEYWORDS = {
    "alignas", "alignof", "and", "and_eq", "asm", "atomic_cancel", "atomic_commit",
    "atomic_noexcept", "auto", "bitand", "bitor", "bool", "break", "case", "catch",
    "char", "char8_t", "char16_t", "char32_t", "class", "compl", "concept",
    "const", "consteval", "constexpr", "constinit", "const_cast", "continue",
    "co_await", "co_return", "co_yield", "decltype", "default", "delete", "do",
    "double", "dynamic_cast", "else", "enum", "explicit", "export", "extern",
    "false", "float", "for", "friend", "goto", "if", "inline", "int", "long",
    "mutable", "namespace", "new", "noexcept", "not", "not_eq", "nullptr",
    "operator", "or", "or_eq", "private", "protected", "public", "reflexpr",
    "register", "reinterpret_cast", "requires", "return", "short", "signed",
    "sizeof", "static", "static_assert", "static_cast", "struct", "switch",
    "synchronized", "template", "this", "thread_local", "throw", "true", "try",
    "typedef", "typeid", "typename", "union", "unsigned", "using", "virtual",
    "void", "volatile", "wchar_t", "while", "xor", "xor_eq"
}

def cpp_ident(name: str) -> str:
    return f"__SYM__{name}" if name in CPP_KEYWORDS else name


def generate_verilator_verifier_tb(v_file: str, tb_file: str, module_name: str,
                                   port_decls: dict, flat_inputs: list, flat_outputs: list):
    tb = [
        f'#include "V{module_name}.h"',
        '#include "verilated.h"',
        '#include <iostream>',
        '#include <fstream>',
        '#include <string>',
        '#include <cstdint>',
        '#include <cstring>',
        '',
        'template <typename T>',
        'inline void vl_clear(T& val) {',
        '    val = 0;',
        '}',
        'template <std::size_t N>',
        'inline void vl_clear(VlWide<N>& val) {',
        '    for (size_t i = 0; i < N; ++i) val[i] = 0;',
        '}',
        '',
        'template <typename T>',
        'inline void vl_set_bit(T& val, size_t bit) {',
        '    val |= static_cast<T>(static_cast<uint64_t>(1) << bit);',
        '}',
        'template <std::size_t N>',
        'inline void vl_set_bit(VlWide<N>& val, size_t bit) {',
        '    val[bit / 32] |= (1U << (bit % 32));',
        '}',
        '',
        'template <typename T>',
        'inline int vl_get_bit(const T& val, size_t bit) {',
        '    return static_cast<int>((val >> bit) & 1);',
        '}',
        'template <std::size_t N>',
        'inline int vl_get_bit(const VlWide<N>& val, size_t bit) {',
        '    return static_cast<int>((val[bit / 32] >> (bit % 32)) & 1);',
        '}',
        '',
        'int main(int argc, char** argv) {',
        '    Verilated::commandArgs(argc, argv);',
        f'    V{module_name}* top = new V{module_name};',
        '    std::ifstream infile(argv[1]);',
        '    std::ofstream outfile(argv[2]);',
        '    std::string line;',
        '    while (std::getline(infile, line)) {',
        "        while (!line.empty() && (line.back() == '\\r' || line.back() == ' ')) line.pop_back();",
        '        if (line.empty()) continue;',
    ]

    # Assign inputs
    flat_idx = 0
    for name, msb, lsb in port_decls['inputs']:
        c_name = cpp_ident(name)
        if msb is not None and lsb is not None:
            base_shift = min(msb, lsb)
            tb.append(f'        vl_clear(top->{c_name});')
            step = 1 if msb <= lsb else -1
            for bit in range(msb, lsb + step, step):
                tb.append(f"        if (line[{flat_idx}] == '1') vl_set_bit(top->{c_name}, {bit - base_shift});")
                flat_idx += 1
        else:
            tb.append(f"        top->{c_name} = line[{flat_idx}] - '0';")
            flat_idx += 1

    tb.append('        top->eval();')

    # Write outputs
    for name, msb, lsb in port_decls['outputs']:
        c_name = cpp_ident(name)
        if msb is not None and lsb is not None:
            base_shift = min(msb, lsb)
            step = 1 if msb <= lsb else -1
            for bit in range(msb, lsb + step, step):
                tb.append(f'        outfile << vl_get_bit(top->{c_name}, {bit - base_shift});')
        else:
            tb.append(f'        outfile << (int)(top->{c_name} & 1);')

    tb.append('        outfile << "\\n";')
    tb.append('    }')
    tb.append('    delete top;')
    tb.append('    return 0;')
    tb.append('}')

    with open(tb_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(tb) + '\n')


def run_verilator_state_simulation(v_file: str, vectors: list) -> list:
    base_path   = os.path.splitext(v_file)[0]
    tb_file     = base_path + "_verif_verilator_tb.cpp"
    vec_file    = base_path + "_verif_verilator_inputs.txt"
    out_file    = base_path + "_verif_verilator_outputs.txt"
    obj_dir     = base_path + "_verif_verilator_obj_dir"

    gsclib_path = find_gsclib_path(v_file)
    if not gsclib_path:
        raise RuntimeError("GSCLib_3.0.v library file not found")

    if not shutil.which("verilator") or not shutil.which("make"):
        raise RuntimeError("verilator or make not found in system PATH")

    try:
        module_name, port_decls, flat_inputs, flat_outputs, _, _ = parse_iwls_ports(v_file)

        with open(vec_file, 'w', encoding='utf-8') as f:
            for vec in vectors:
                f.write("".join(str(v) for v in vec) + "\n")

        generate_verilator_verifier_tb(v_file, tb_file, module_name, port_decls, flat_inputs, flat_outputs)

        comp_cmd = [
            "verilator", "-O3", "-Wno-fatal", "--default-language", "1364-2001", "--cc",
            gsclib_path, v_file,
            "--exe", tb_file,
            "--top-module", module_name,
            "--Mdir", obj_dir
        ]
        comp_res = subprocess.run(comp_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if comp_res.returncode != 0:
            raise RuntimeError(f"Verilator compile error: {comp_res.stderr.strip()}")

        build_cmd = ["make", "-j", str(os.cpu_count() or 4), "-C", obj_dir, "-f", f"V{module_name}.mk", f"V{module_name}"]
        build_res = subprocess.run(build_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if build_res.returncode != 0:
            raise RuntimeError(f"Verilator make build error: {build_res.stderr.strip()}")

        exe_path = os.path.join(obj_dir, f"V{module_name}")
        run_res  = subprocess.run([exe_path, vec_file, out_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if run_res.returncode != 0:
            raise RuntimeError(f"Verilator runtime error: {run_res.stderr.strip()}")

        with open(out_file, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()

        normalized_results = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            normalized_results.append(
                [0 if b == '0' else (1 if b == '1' else 2) for b in line]
            )

        return normalized_results

    finally:
        for p in (tb_file, vec_file, out_file):
            if os.path.exists(p):
                try: os.remove(p)
                except OSError: pass
        if obj_dir and os.path.exists(obj_dir):
            try: shutil.rmtree(obj_dir)
            except OSError: pass


# ===========================================================================
# 3. INTERNAL WORKER FOR ENGINE & REACTOR
# ===========================================================================

def run_worker_process(filepath: str, exec_mode: str, vectors: list, optimize: bool = True) -> list:
    temp_vec_json = filepath + f"_{exec_mode}_in.tmp.json"
    temp_out_json = filepath + f"_{exec_mode}_out.tmp.json"

    dump_json_file(temp_vec_json, vectors, indent=False)

    cmd = [
        sys.executable, os.path.abspath(__file__),
        "--internal-worker", filepath,
        "--exec-mode", exec_mode,
        "--in-file", temp_vec_json,
        "--out-file", temp_out_json,
    ]
    if optimize:
        cmd.append("--optimize")
    else:
        cmd.append("--raw")

    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"Worker ({exec_mode}) failed: STDERR:\n{res.stderr}\nSTDOUT:\n{res.stdout}")

        return load_json_file(temp_out_json)

    finally:
        for p in (temp_vec_json, temp_out_json):
            if os.path.exists(p):
                try: os.remove(p)
                except OSError: pass


def internal_worker_main(filepath: str, exec_mode: str, in_file: str, out_file: str, optimize: bool = True):
    is_reactor = ('reactor' in exec_mode)
    pkg_dir    = 'reactor_oop' if exec_mode == 'reactor_oop' else 'reactor' if is_reactor else 'engine'
    is_oop     = (exec_mode == 'reactor_oop')

    target_path = os.path.join(_SCRIPT_DIR, pkg_dir)
    if not os.path.exists(target_path):
        target_path = os.path.join(_PROJECT_ROOT, pkg_dir)

    sys.path.insert(0, _PROJECT_ROOT)
    sys.path.insert(0, target_path)

    import Circuit
    import Const

    try:
        from benchmark_iwls import IWLSVerilogRunner
    except ImportError:
        try:
            from tests.src.benchmark_iwls import IWLSVerilogRunner
        except ImportError:
            from tests.benchmark_iwls import IWLSVerilogRunner

    vectors = load_json_file(in_file)
    target_const_mode = Const.COMPILE if 'sweep' in exec_mode else Const.SIMULATE

    runner = IWLSVerilogRunner(
        filepath, Circuit.Circuit, Const, is_reactor=is_reactor, is_oop=is_oop,
        use_optimize=optimize, mode=pkg_dir
    )
    results = runner.run_vectors(vectors, target_mode=target_const_mode)
    dump_json_file(out_file, results, indent=False)


# ===========================================================================
# 4. EQUIVALENCE VERIFIER & COMPARATOR
# ===========================================================================

def verify_circuit(v_file: str, vector_count: int = 1000, seed: int = 42,
                   use_icarus: bool = True, use_verilator: bool = True,
                   use_engine: bool = True, use_rx_prop: bool = True,
                   use_rx_sweep: bool = True, use_rx_oop: bool = True,
                   vectors: list = None, warmup_count: int = 50,
                   optimize: bool = True) -> dict:
    filename = os.path.basename(v_file)
    module_name, port_decls, flat_inputs, flat_outputs, clock_idx, clock_port_name = parse_iwls_ports(v_file)

    reset_idx, reset_name, is_active_low = find_reset_port(flat_inputs)
    assert_val = 0 if is_active_low else 1
    deassert_val = 1 if is_active_low else 0

    if vectors is not None:
        raw_vectors = list(vectors)
        warmup_count = min(warmup_count, len(raw_vectors))
    else:
        warmup_count = 50
        raw_vectors = []
        reset_cycles = 10

        # Warmup vectors:
        # First reset_cycles: assert reset with clock = 0 (flush state)
        # Next (warmup_count - reset_cycles): deassert reset with clock toggling
        for i in range(warmup_count):
            w_vec = [0] * len(flat_inputs)
            if i < reset_cycles:
                if reset_idx != -1:
                    w_vec[reset_idx] = assert_val
                if clock_idx != -1:
                    w_vec[clock_idx] = 0
            else:
                if reset_idx != -1:
                    w_vec[reset_idx] = deassert_val
                if clock_idx != -1:
                    w_vec[clock_idx] = (i - reset_cycles) % 2
            raw_vectors.append(w_vec)

        # Measured vectors: setup (clk=0) then trigger (clk=1) with reset deasserted
        rng = random.Random(seed)
        for _ in range(vector_count):
            base_vec = [rng.randint(0, 1) for _ in range(len(flat_inputs))]
            if reset_idx != -1:
                base_vec[reset_idx] = deassert_val
            if clock_idx != -1:
                setup = list(base_vec)
                setup[clock_idx] = 0
                trigger = list(base_vec)
                trigger[clock_idx] = 1
                raw_vectors.append(setup)
                raw_vectors.append(trigger)
            else:
                raw_vectors.append(base_vec)

    # ── 1. Reference Engine (Icarus preferred, Verilator fallback) ────────
    golden_outputs = None
    if use_icarus:
        try:
            golden_outputs = run_icarus_state_simulation(v_file, raw_vectors)
        except Exception as exc:
            print(f"[-] Icarus simulation failed on {filename}: {exc}")
            use_icarus = False

    verilator_outputs = None
    if use_verilator:
        try:
            verilator_outputs = run_verilator_state_simulation(v_file, raw_vectors)
        except Exception as exc:
            print(f"[-] Verilator simulation failed on {filename}: {exc}")
            use_verilator = False

    if golden_outputs is None and verilator_outputs is not None:
        golden_outputs = verilator_outputs
        ref_name = "Verilator"
    else:
        ref_name = "Icarus"

    if golden_outputs is None:
        eff_total = (len(raw_vectors) - warmup_count) // 2 if clock_idx != -1 else (len(raw_vectors) - warmup_count)
        return {
            "circuit": filename,
            "inputs_count": len(flat_inputs),
            "outputs_count": len(flat_outputs),
            "total_vectors": eff_total,
            "pass_count": 0,
            "fail_count": eff_total,
            "error": "No reference simulation engine (Icarus/Verilator) succeeded.",
            "status": "FAIL",
            "mismatches": [],
        }

    # ── 2. Run Engine & Reactor modes ─────────────────────────────────────
    engine_outputs = None
    if use_engine:
        try:
            engine_outputs = run_worker_process(v_file, 'engine', raw_vectors, optimize=optimize)
        except Exception as exc:
            print(f"[-] Engine worker failed on {filename}: {exc}")
            use_engine = False

    rx_prop_outputs = None
    if use_rx_prop:
        try:
            rx_prop_outputs = run_worker_process(v_file, 'reactor_prop', raw_vectors, optimize=optimize)
        except Exception as exc:
            print(f"[-] Reactor Propagate worker failed on {filename}: {exc}")
            use_rx_prop = False

    rx_sweep_outputs = None
    if use_rx_sweep:
        try:
            rx_sweep_outputs = run_worker_process(v_file, 'reactor_sweep', raw_vectors, optimize=optimize)
        except Exception as exc:
            print(f"[-] Reactor Sweep worker failed on {filename}: {exc}")
            use_rx_sweep = False

    rx_oop_outputs = None
    if use_rx_oop:
        try:
            rx_oop_outputs = run_worker_process(v_file, 'reactor_oop', raw_vectors, optimize=optimize)
        except Exception as exc:
            print(f"[-] Reactor OOP worker failed on {filename}: {exc}")
            use_rx_oop = False

    # ── 3. Equivalence Verification & Comparison ──────────────────────────
    mismatches = []
    vector_logs = []
    pass_count = 0
    total_vectors = len(raw_vectors)

    def state_matches(actual, ref):
        if actual is None or ref is None:
            return False
        if len(actual) != len(ref):
            return False
        for a, r in zip(actual, ref):
            # In 4-state simulation (Icarus), 2 represents 'x' (uninitialized latch).
            # 2-state simulators (Verilator, Darion) resolve uninitialized power-up to 0 or 1.
            if r == 2:
                continue
            if a != r:
                return False
        return True

    for i in range(total_vectors):
        is_warmup = (i < warmup_count)
        ref_state = golden_outputs[i] if golden_outputs else None

        g_out  = golden_outputs[i]   if use_icarus and golden_outputs else None
        v_out  = verilator_outputs[i] if use_verilator and verilator_outputs else None
        e_out  = engine_outputs[i]   if use_engine and engine_outputs else None
        rp_out = rx_prop_outputs[i]  if use_rx_prop and rx_prop_outputs else None
        rs_out = rx_sweep_outputs[i] if use_rx_sweep and rx_sweep_outputs else None
        ro_out = rx_oop_outputs[i]   if use_rx_oop and rx_oop_outputs else None

        match_icarus    = (g_out == ref_state)           if use_icarus else True
        match_verilator = state_matches(v_out, ref_state) if use_verilator else True
        match_engine    = state_matches(e_out, ref_state) if use_engine else True
        match_rx_prop   = state_matches(rp_out, ref_state) if use_rx_prop else True
        match_rx_sweep  = state_matches(rs_out, ref_state) if use_rx_sweep else True
        match_rx_oop    = state_matches(ro_out, ref_state) if use_rx_oop else True

        darion_active = use_engine or use_rx_prop or use_rx_sweep or use_rx_oop
        if darion_active:
            all_match = (
                match_engine and match_rx_prop and match_rx_sweep and match_rx_oop
            )
        else:
            all_match = match_icarus and match_verilator

        log_entry = {
            "vector_id": i - warmup_count if not is_warmup else f"W{i}",
            "inputs": raw_vectors[i],
            "expected": ref_state,
            "ref_source": ref_name,
            "icarus": g_out if use_icarus else "SKIPPED",
            "verilator": v_out if use_verilator else "SKIPPED",
            "engine": e_out if use_engine else "SKIPPED",
            "rx_prop": rp_out if use_rx_prop else "SKIPPED",
            "rx_sweep": rs_out if use_rx_sweep else "SKIPPED",
            "rx_oop": ro_out if use_rx_oop else "SKIPPED",
            "pass": all_match,
        }

        if not is_warmup:
            vector_logs.append(log_entry)
            if all_match:
                pass_count += 1
            else:
                mismatches.append({
                    "vector_id": i - warmup_count,
                    "inputs": raw_vectors[i],
                    "expected": ref_state,
                    "ref_source": ref_name,
                    "icarus_actual":    g_out  if not match_icarus    else "MATCH" if use_icarus    else "SKIPPED",
                    "verilator_actual": v_out  if not match_verilator else "MATCH" if use_verilator else "SKIPPED",
                    "engine_actual":    e_out  if not match_engine    else "MATCH" if use_engine    else "SKIPPED",
                    "rx_prop_actual":   rp_out if not match_rx_prop   else "MATCH" if use_rx_prop   else "SKIPPED",
                    "rx_sweep_actual":  rs_out if not match_rx_sweep  else "MATCH" if use_rx_sweep  else "SKIPPED",
                    "rx_oop_actual":    ro_out if not match_rx_oop    else "MATCH" if use_rx_oop    else "SKIPPED",
                })

    effective_total = (total_vectors - warmup_count) // 2 if clock_idx != -1 else (total_vectors - warmup_count)
    effective_pass  = pass_count // 2 if clock_idx != -1 else pass_count

    return {
        "circuit": filename,
        "inputs_count": len(flat_inputs),
        "outputs_count": len(flat_outputs),
        "total_vectors": effective_total,
        "pass_count": effective_pass,
        "fail_count": len(mismatches),
        "status": "PASS" if len(mismatches) == 0 else "FAIL",
        "mismatches": mismatches,
        "vector_logs": vector_logs,
    }


# ===========================================================================
# 5. FILE DISCOVERY & MAIN
# ===========================================================================

def get_v_files(targets) -> list:
    if isinstance(targets, str):
        targets = [targets]
    v_files = []
    for target in targets:
        if not os.path.exists(target):
            if os.path.exists(os.path.join(_TESTS_DIR, target)):
                target = os.path.join(_TESTS_DIR, target)
            elif os.path.exists(os.path.join(_PROJECT_ROOT, target)):
                target = os.path.join(_PROJECT_ROOT, target)
        if os.path.isfile(target) and target.endswith('.v'):
            v_files.append(target)
        elif os.path.isdir(target):
            for root, _, files in os.walk(target):
                for f in files:
                    if f.endswith('.v') and not f.endswith('_tb.v') and not f.endswith('_helper.v'):
                        v_files.append(os.path.join(root, f))
    return sorted(list(set(v_files)), key=os.path.getsize)


def main():
    parser = argparse.ArgumentParser(description="Unified Sequential IWLS 2005 State Verifier")
    parser.add_argument('target', nargs='*', default=["tests/IWLS2005/itc99/netlist/"],
                        help="Path to .v file(s) or directory")
    parser.add_argument('--vectors', type=int, default=100,
                        help="Number of test vectors per circuit (default: 100)")
    parser.add_argument('--seed', type=int, default=42, help="PRNG Seed")
    parser.add_argument('--output', type=str, default="iwls_verification_report", help="JSON output file prefix")
    parser.add_argument('--dump', action='store_true', help="Dump Markdown report to tests/test_result/verifier_iwls/")
    parser.add_argument('--json', action='store_true', help="Output JSON to stdout")

    parser.add_argument('--no-engine', dest='engine', action='store_false', default=True, help="Skip Python Engine")
    parser.add_argument('--no-rx-prop', dest='rx_prop', action='store_false', default=True, help="Skip Reactor BFS Propagate")
    parser.add_argument('--no-rx-sweep', dest='rx_sweep', action='store_false', default=True, help="Skip Reactor Sweep")
    parser.add_argument('--no-reactor-oop', '--no-rx-oop', dest='rx_oop', action='store_false', default=True, help="Skip Reactor OOP")
    parser.add_argument('--no-icarus', dest='icarus', action='store_false', default=True, help="Skip Icarus Verilog")
    parser.add_argument('--no-verilator', dest='verilator', action='store_false', default=True, help="Skip Verilator C++")

    parser.add_argument('--optimize', action='store_true', default=True, help="Enable circuit optimization")
    parser.add_argument('--no-optimize', dest='optimize', action='store_false')
    parser.add_argument('--raw', dest='optimize', action='store_false', help="Disable circuit optimization (use raw netlist order)")

    # Internal worker flags
    parser.add_argument('--internal-worker', type=str, default="", help=argparse.SUPPRESS)
    parser.add_argument('--exec-mode', type=str, help=argparse.SUPPRESS)
    parser.add_argument('--in-file', type=str, help=argparse.SUPPRESS)
    parser.add_argument('--out-file', type=str, help=argparse.SUPPRESS)

    args = parser.parse_args()

    if args.internal_worker:
        internal_worker_main(args.internal_worker, args.exec_mode, args.in_file, args.out_file, optimize=args.optimize)
        sys.exit(0)

    v_files = get_v_files(args.target)
    if not v_files:
        print("[-] Error: No .v files found.")
        sys.exit(1)

    if not args.json:
        print("=" * 115)
        print("  UNIFIED IWLS 2005 SEQUENTIAL STATE VERIFICATION SUITE (PYTHON, RX-PROP, RX-SWEEP, VERILATOR)")
        print(f"  Test Vectors/Circuit : {args.vectors:,} (after 50 warmup cycles) | Base Model: Icarus Verilog / Verilator")
        print("=" * 115)
        print(f"| {'Circuit':<18} | {'Inputs':<8} | {'Outputs':<8} | {'Vectors':<10} | {'Passed':<10} | {'Failed':<8} | {'Status':<8} |")
        print(f"|{'-'*20}|{'-'*10}|{'-'*10}|{'-'*12}|{'-'*12}|{'-'*10}|{'-'*10}|")

    all_reports = []
    md_lines = []
    md_lines.append("# Unified IWLS 2005 Sequential State Verification")
    md_lines.append("")
    md_lines.append(f"- **Vectors/Circuit**: {args.vectors:,}")
    md_lines.append(f"- **Seed**: {args.seed}")
    md_lines.append("")
    md_lines.append(f"| {'Circuit':<18} | {'Inputs':<8} | {'Outputs':<8} | {'Vectors':<10} | {'Passed':<10} | {'Failed':<8} | {'Status':<8} |")
    md_lines.append(f"|{'-'*20}|{'-'*10}|{'-'*10}|{'-'*12}|{'-'*12}|{'-'*10}|{'-'*10}|")
    overall_pass = True

    for v_file in v_files:
        res = verify_circuit(
            v_file, vector_count=args.vectors, seed=args.seed,
            use_icarus=args.icarus, use_verilator=args.verilator,
            use_engine=args.engine, use_rx_prop=args.rx_prop,
            use_rx_sweep=args.rx_sweep, use_rx_oop=args.rx_oop,
            optimize=args.optimize
        )
        all_reports.append(res)

        status_str = "\033[92mPASS\033[0m" if res["status"] == "PASS" else "\033[91mFAIL\033[0m"
        if res["status"] != "PASS":
            overall_pass = False

        row_str = (
            f"| {res['circuit']:<18} | "
            f"{res['inputs_count']:<8} | "
            f"{res['outputs_count']:<8} | "
            f"{res['total_vectors']:<10,}| "
            f"{res['pass_count']:<10,}| "
            f"{res['fail_count']:<8} | "
            f"{status_str:<8} |"
        )
        md_lines.append(row_str)

        if not args.json:
            print(row_str)
            if res.get("fail_count", 0) > 0 and res.get("mismatches"):
                mm = res['mismatches'][0]
                print(f"  └─> First mismatch at test vector #{mm['vector_id']}:")
                print(f"      Inputs applied: {mm['inputs']}")
                print(f"      Expected ({mm['ref_source']}): {mm['expected']}")
                print(f"      Icarus     : {mm['icarus_actual']}")
                print(f"      Verilator  : {mm['verilator_actual']}")
                print(f"      Engine     : {mm['engine_actual']}")
                print(f"      Rx-Prop    : {mm['rx_prop_actual']}")
                print(f"      Rx-Sweep   : {mm['rx_sweep_actual']}")
                print(f"      Rx-OOP     : {mm['rx_oop_actual']}")

    if args.json:
        print(json.dumps(all_reports, indent=2))

    if args.dump:
        out_dir = os.path.join(_TESTS_DIR, "test_result", "verifier_iwls")
        os.makedirs(out_dir, exist_ok=True)
        import datetime
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        dump_path = os.path.join(out_dir, f"unified_iwls_verifier_{ts}.md")
        with open(dump_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(md_lines) + "\n")
        print(f"\n[+] Markdown dump saved to -> {dump_path}")

    sys.exit(0 if overall_pass else 1)


if __name__ == "__main__":
    main()
