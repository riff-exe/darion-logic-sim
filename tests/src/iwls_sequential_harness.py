"""
iwls_sequential_harness.py
===========================
Icarus Verilog and Verilator simulation harness for IWLS 2005 benchmark circuits.

Handles:
  - Synthesis standard cell library injection (GSCLib_3.0.v)
  - Multi-bit bus ports (e.g. input [7:0] I; output [3:0] O;)
  - Escaped identifiers and bitwise vector indexing
  - Clock-aware vector pairs (setup @ CLK=0, trigger @ CLK=1)
  - 50-cycle warmup (inputs=0, alternating clock) to flush DFF states
  - VPI inner-loop timer ($start_timer / $stop_timer via vpi_timer.vpi) for Icarus
  - Cycle-accurate C++ simulation loop with nanosecond chrono timing for Verilator
"""

import os
import re
import sys
import time
import random
import shutil
import subprocess
from pathlib import Path

_SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
_TESTS_DIR    = os.path.dirname(_SCRIPT_DIR)
_PROJECT_ROOT = os.path.dirname(_TESTS_DIR)

sys.path.insert(0, _SCRIPT_DIR)
sys.path.insert(0, _TESTS_DIR)
sys.path.insert(0, _PROJECT_ROOT)

# VPI timer paths
_VPI_DIR = (
    os.path.join(_PROJECT_ROOT, "harness_build")
    if os.path.exists(os.path.join(_PROJECT_ROOT, "harness_build"))
    else os.path.join(_SCRIPT_DIR, "harness_build")
)
_VPI_TIMER_C   = os.path.join(_VPI_DIR, "vpi_timer.c")
_VPI_TIMER_VPI = os.path.join(_VPI_DIR, "vpi_timer.vpi")


# ---------------------------------------------------------------------------
# Helpers & Library Locator
# ---------------------------------------------------------------------------

def find_gsclib_path(start_path: str = "") -> str:
    """Locate GSCLib_3.0.v in the repository."""
    candidates = [
        os.path.join(_TESTS_DIR, "IWLS2005", "library", "GSCLib_3.0.v"),
        os.path.join(_SCRIPT_DIR, "IWLS2005", "library", "GSCLib_3.0.v"),
        os.path.join(_PROJECT_ROOT, "tests", "IWLS2005", "library", "GSCLib_3.0.v"),
        os.path.join(_PROJECT_ROOT, "IWLS2005", "library", "GSCLib_3.0.v"),
    ]
    if start_path:
        d = os.path.dirname(os.path.abspath(start_path))
        while len(d) > 3:
            cand = os.path.join(d, "library", "GSCLib_3.0.v")
            if os.path.exists(cand):
                return cand
            cand_sub = os.path.join(d, "IWLS2005", "library", "GSCLib_3.0.v")
            if os.path.exists(cand_sub):
                return cand_sub
            parent = os.path.dirname(d)
            if parent == d:
                break
            d = parent

    for c in candidates:
        if os.path.exists(c):
            return os.path.abspath(c)
    return ""


def build_vpi_timer() -> bool:
    """Compile vpi_timer.c -> vpi_timer.vpi using iverilog-vpi if not already built."""
    if os.path.exists(_VPI_TIMER_VPI):
        return True
    if not os.path.exists(_VPI_TIMER_C):
        return False
    if not shutil.which("iverilog-vpi"):
        return False
    try:
        res = subprocess.run(
            ["iverilog-vpi", "vpi_timer.c"],
            cwd=_VPI_DIR,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        return res.returncode == 0 and os.path.exists(_VPI_TIMER_VPI)
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Verilog Port & Bus Parser
# ---------------------------------------------------------------------------

def parse_iwls_ports(v_file: str):
    """
    Extract module name, port declarations (including multi-bit buses),
    flattened bit-level port lists, and clock port info.

    Returns:
        module_name (str): name of the top-level module
        port_decls (dict): {'inputs': [(name, msb, lsb), ...], 'outputs': [(name, msb, lsb), ...]}
        flat_inputs (list): list of all bit-level input names (e.g. 'I[0]', 'CLOCK', ...)
        flat_outputs (list): list of all bit-level output names
        clock_idx (int): index in flat_inputs corresponding to clock (or -1)
        clock_port_name (str): top-level port name for the clock
    """
    with open(v_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Strip comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    content = re.sub(r'//.*', '', content)

    module_name = "circuit"
    module_body = content

    # Match module definition
    for m in re.finditer(r'\bmodule\s+([a-zA-Z0-9_]+)\s*\((.*?)\);', content, flags=re.DOTALL):
        m_name = m.group(1).strip()
        if m_name.lower() not in ('dff', 'dffsrx1', 'dffx1', 'sdffsrx1', 'invx1', 'bufx1'):
            module_name = m_name
            # Extract body up to endmodule
            idx_start = m.start()
            end_m = re.search(r'\bendmodule\b', content[idx_start:], flags=re.DOTALL)
            if end_m:
                module_body = content[idx_start : idx_start + end_m.end()]
            else:
                module_body = content[idx_start:]
            break

    statements = [s.strip() for s in module_body.split(';') if s.strip()]

    input_decls = []
    output_decls = []
    flat_inputs = []
    flat_outputs = []

    for stmt in statements:
        m_in = re.match(r'^input\s+(.*)', stmt, re.DOTALL)
        if m_in:
            decl = m_in.group(1).strip()
            m_rng = re.match(r'^\[\s*(\d+)\s*:\s*(\d+)\s*\]\s*(.*)', decl, re.DOTALL)
            if m_rng:
                msb, lsb = int(m_rng.group(1)), int(m_rng.group(2))
                names = [n.strip() for n in m_rng.group(3).split(',') if n.strip()]
                for name in names:
                    input_decls.append((name, msb, lsb))
                    step = 1 if msb <= lsb else -1
                    for bit in range(msb, lsb + step, step):
                        flat_inputs.append(f"{name}[{bit}]")
            else:
                names = [n.strip() for n in decl.split(',') if n.strip()]
                for name in names:
                    input_decls.append((name, None, None))
                    flat_inputs.append(name)
            continue

        m_out = re.match(r'^output\s+(.*)', stmt, re.DOTALL)
        if m_out:
            decl = m_out.group(1).strip()
            m_rng = re.match(r'^\[\s*(\d+)\s*:\s*(\d+)\s*\]\s*(.*)', decl, re.DOTALL)
            if m_rng:
                msb, lsb = int(m_rng.group(1)), int(m_rng.group(2))
                names = [n.strip() for n in m_rng.group(3).split(',') if n.strip()]
                for name in names:
                    output_decls.append((name, msb, lsb))
                    step = 1 if msb <= lsb else -1
                    for bit in range(msb, lsb + step, step):
                        flat_outputs.append(f"{name}[{bit}]")
            else:
                names = [n.strip() for n in decl.split(',') if n.strip()]
                for name in names:
                    output_decls.append((name, None, None))
                    flat_outputs.append(name)
            continue

    # Find clock port
    candidates = []
    for idx, name in enumerate(flat_inputs):
        base = name.split('[')[0].strip().lower()
        if base in ('ck', 'clk', 'clock', 'g0') or 'clk' in base or 'clock' in base:
            candidates.append((idx, name.split('[')[0].strip()))

    clock_idx = -1
    clock_port_name = ""
    if len(candidates) == 1:
        clock_idx, clock_port_name = candidates[0]
    elif len(candidates) > 1:
        # Count flip-flops clocked by each candidate to pick the dominant clock
        best_cnt = -1
        best_cand = candidates[0]
        for idx, name in candidates:
            pat = rf'\.(?:CK|CLK)\s*\(\s*{re.escape(name)}\s*\)'
            cnt = len(re.findall(pat, module_body))
            if cnt > best_cnt:
                best_cnt = cnt
                best_cand = (idx, name)
        clock_idx, clock_port_name = best_cand

    port_decls = {'inputs': input_decls, 'outputs': output_decls}
    return module_name, port_decls, flat_inputs, flat_outputs, clock_idx, clock_port_name


def find_reset_port(flat_inputs: list):
    """
    Identify reset port index, port name, and whether it is active-low.
    Returns (reset_idx, reset_port_name, is_active_low).
    """
    for idx, name in enumerate(flat_inputs):
        base = name.split('[')[0].strip().lower()
        if base in ('reset', 'rst', 'reset_n', 'rst_n', 'rn', 'rstb', 'clear', 'clr'):
            is_active_low = base.endswith('_n') or base.endswith('b') or base == 'rn'
            return idx, name.split('[')[0].strip(), is_active_low
    for idx, name in enumerate(flat_inputs):
        base = name.split('[')[0].strip().lower()
        if 'reset' in base or 'rst' in base:
            is_active_low = base.endswith('_n') or base.endswith('b') or base == 'rn'
            return idx, name.split('[')[0].strip(), is_active_low
    return -1, "", False


# ---------------------------------------------------------------------------
# 1. Icarus Verilog Testbench Generator & Runner
# ---------------------------------------------------------------------------

def generate_icarus_tb_iwls(v_file: str, tb_file: str, measured: int, vector_file: str,
                             use_vpi_timer: bool = True):
    module_name, port_decls, flat_inputs, flat_outputs, clock_idx, clock_port_name = parse_iwls_ports(v_file)

    tb = []
    tb.append("`timescale 1ns/1ps\n")
    tb.append(f"module tb_{module_name};\n")

    # Declare inputs as reg
    for name, msb, lsb in port_decls['inputs']:
        if msb is not None and lsb is not None:
            tb.append(f"    reg [{msb}:{lsb}] {name};\n")
        else:
            tb.append(f"    reg {name};\n")

    # Declare outputs as wire
    for name, msb, lsb in port_decls['outputs']:
        if msb is not None and lsb is not None:
            tb.append(f"    wire [{msb}:{lsb}] {name};\n")
        else:
            tb.append(f"    wire {name};\n")

    total_inputs = len(flat_inputs)
    tb.append(f"    reg [{total_inputs-1}:0] test_vectors [0:{measured-1}];\n")
    tb.append("    integer i;\n\n")

    # Instantiate DUT
    tb.append(f"    {module_name} uut (\n")
    all_ports = [p[0] for p in port_decls['inputs'] + port_decls['outputs']]
    conn = [f"        .{p}({p})" for p in all_ports]
    tb.append(",\n".join(conn))
    tb.append("\n    );\n\n")

    v_path_str = str(vector_file).replace("\\", "/")

    tb.append("    initial begin\n")
    # Initialise all regs to 0
    for name, msb, lsb in port_decls['inputs']:
        tb.append(f"        {name} = 0;\n")

    # 50-cycle warmup: flush DFF state
    tb.append("        // 50-cycle warmup: flush DFF state\n")
    tb.append("        repeat (50) begin\n")
    if clock_port_name:
        tb.append(f"            {clock_port_name} = 0; #1;\n")
        tb.append(f"            {clock_port_name} = 1; #1;\n")
    else:
        tb.append("            #1;\n")
    tb.append("        end\n\n")

    # Load vectors
    tb.append(f'        $readmemb("{v_path_str}", test_vectors);\n')

    # Timer start
    if use_vpi_timer:
        tb.append("        $start_timer();\n")

    tb.append(f"        for (i = 0; i < {measured}; i = i + 1) begin\n")
    for idx, bit_name in enumerate(flat_inputs):
        tb.append(f"            {bit_name} = test_vectors[i][{idx}];\n")
    tb.append("            #1;\n")
    tb.append("        end\n")

    # Timer stop
    if use_vpi_timer:
        tb.append("        $stop_timer();\n")

    tb.append("        $finish;\n")
    tb.append("    end\n")
    tb.append("endmodule\n")

    with open(tb_file, 'w', encoding='utf-8') as f:
        f.write("".join(tb))


def run_icarus_harness_iwls(v_file: str, vectors: int, warmup: int,
                            use_perf: bool = False, perf_events: str = "") -> dict:
    filename    = os.path.basename(v_file)
    base_path   = os.path.splitext(v_file)[0]
    tb_file     = base_path + "_iwls_icarus_tb.v"
    vvp_file    = base_path + "_iwls_icarus.vvp"
    vector_file = base_path + "_iwls_icarus_vectors.txt"

    gsclib_path = find_gsclib_path(v_file)
    if not gsclib_path:
        return {"engine": "Icarus", "file": filename, "error": "GSCLib_3.0.v library file not found"}

    if not shutil.which("iverilog") or not shutil.which("vvp"):
        return {"engine": "Icarus", "file": filename, "error": "iverilog or vvp not found in PATH"}

    use_vpi = build_vpi_timer()

    try:
        module_name, port_decls, flat_inputs, flat_outputs, clock_idx, clock_port_name = parse_iwls_ports(v_file)
        logical_count = max(vectors - warmup, 1)
        file_size_kb = os.path.getsize(v_file) / 1024.0
        if file_size_kb > 4000:
            logical_count = min(logical_count, 1000)

        rng = random.Random(42)
        physical_vectors = []
        for _ in range(logical_count):
            base_vec = [rng.randint(0, 1) for _ in range(len(flat_inputs))]
            if clock_idx != -1:
                setup = list(base_vec)
                setup[clock_idx] = 0
                trigger = list(base_vec)
                trigger[clock_idx] = 1
                physical_vectors.append(setup)
                physical_vectors.append(trigger)
            else:
                physical_vectors.append(base_vec)

        measured = len(physical_vectors)

        with open(vector_file, 'w', encoding='utf-8') as f:
            for vec in physical_vectors:
                f.write("".join(str(v) for v in vec) + "\n")

        generate_icarus_tb_iwls(v_file, tb_file, measured, vector_file, use_vpi_timer=use_vpi)

        # Compile with iverilog
        t_comp_start = time.perf_counter_ns()
        compile_cmd = ["iverilog", "-o", vvp_file, gsclib_path, v_file, tb_file]
        comp_res = subprocess.run(compile_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        t_comp_end = time.perf_counter_ns()
        compile_ms = (t_comp_end - t_comp_start) / 1_000_000.0

        if comp_res.returncode != 0:
            return {"engine": "Icarus", "file": filename, "error": f"Compilation failure: {comp_res.stderr.strip()}"}

        # Run with vvp
        run_cmd = ["vvp"]
        if use_vpi and os.path.exists(_VPI_TIMER_VPI):
            run_cmd.extend(["-M", _VPI_DIR, "-m", "vpi_timer"])
        run_cmd.append(vvp_file)
        original_run_cmd = list(run_cmd)

        perf_data = f"perf_icarus_{filename}.data"
        perf_txt  = f"perf_icarus_{filename}.txt"
        if use_perf:
            cmd = ["perf", "record", "-m", "32", "-o", perf_data]
            if perf_events:
                cmd.extend(["-e", perf_events])
            cmd.extend(run_cmd)
            run_cmd = cmd

        t_run_start = time.perf_counter_ns()
        run_res = subprocess.run(run_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        t_run_end = time.perf_counter_ns()
        run_ms = (t_run_end - t_run_start) / 1_000_000.0

        if use_perf and run_res.returncode != 0:
            # Fallback to run without perf if perf record failed
            t_run_start = time.perf_counter_ns()
            run_res = subprocess.run(original_run_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            t_run_end = time.perf_counter_ns()
            run_ms = (t_run_end - t_run_start) / 1_000_000.0
        elif use_perf and os.path.exists(perf_data):
            rep = subprocess.run(["perf", "report", "-i", perf_data, "--stdio"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            with open(perf_txt, 'w', encoding='utf-8') as f:
                f.write(rep.stdout)
            for p in (perf_data, perf_data + ".old"):
                if os.path.exists(p):
                    try: os.remove(p)
                    except Exception: pass

        if run_res.returncode != 0:
            return {"engine": "Icarus", "file": filename, "error": f"Run failure: {run_res.stderr.strip()}"}

        sim_ms = None
        if use_vpi:
            for line in run_res.stdout.splitlines():
                if line.startswith("$ELAPSED_NS:"):
                    try:
                        elapsed_ns = int(line.split(":", 1)[1].strip())
                        sim_ms = elapsed_ns / 1_000_000.0
                    except ValueError:
                        pass
                    break

        result = {
            "engine": "Icarus",
            "file": filename,
            "compile_ms": compile_ms,
            "run_ms": run_ms,
            "total_ms": compile_ms + run_ms,
            "vpi_timer": use_vpi,
            "logical_vectors": logical_count,
            "physical_vectors": measured,
            "time_ms": sim_ms if sim_ms is not None else run_ms,
            "load_ms": compile_ms,
        }
        return result

    except Exception as e:
        return {"engine": "Icarus", "file": filename, "error": str(e)}
    finally:
        for p in (tb_file, vvp_file, vector_file):
            if p and os.path.exists(p):
                try: os.remove(p)
                except OSError: pass


# ---------------------------------------------------------------------------
# 2. Verilator Testbench Generator & Runner
# ---------------------------------------------------------------------------

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


def generate_verilator_tb_iwls(v_file: str, tb_file: str, module_name: str, port_decls: dict,
                               flat_inputs: list, clock_port_name: str, use_perf: bool = False):
    tb = [
        f'#include "V{module_name}.h"',
        '#include "verilated.h"',
        '#include <iostream>',
        '#include <fstream>',
        '#include <vector>',
        '#include <string>',
        '#include <chrono>',
        '#include <cstdint>',
        '#include <cstring>',
    ]
    if use_perf:
        tb.extend(['#include <fcntl.h>', '#include <unistd.h>'])

    tb.extend([
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
    ])

    tb.append('int main(int argc, char** argv) {')
    tb.append('    Verilated::commandArgs(argc, argv);')
    tb.append(f'    V{module_name}* top = new V{module_name};')
    tb.append('    std::ifstream infile(argv[1]);')
    tb.append('    std::string line;')
    tb.append('    std::vector<std::string> vectors;')
    tb.append('    while(std::getline(infile, line)) {')
    tb.append("        while (!line.empty() && (line.back() == '\\r' || line.back() == ' ')) line.pop_back();")
    tb.append('        if (!line.empty()) vectors.push_back(line);')
    tb.append('    }')
    tb.append('    // Warmup 50 cycles (inputs = 0, alternating clock)')
    for name, msb, lsb in port_decls['inputs']:
        c_name = cpp_ident(name)
        tb.append(f'    vl_clear(top->{c_name});')

    c_clock_name = cpp_ident(clock_port_name) if clock_port_name else ""
    tb.append('    for (int w = 0; w < 50; ++w) {')
    if clock_port_name:
        tb.append(f'        top->{c_clock_name} = 0;')
        tb.append('        top->eval();')
        tb.append(f'        top->{c_clock_name} = 1;')
        tb.append('        top->eval();')
    else:
        tb.append('        top->eval();')
    tb.append('    }')
    if clock_port_name:
        tb.append(f'    top->{c_clock_name} = 0;')
        tb.append('    top->eval();')

    if use_perf:
        tb.append('    int fd = open("/tmp/rx_perf_ctrl", O_WRONLY | O_NONBLOCK);')
        tb.append('    if (fd >= 0) { write(fd, "enable\\n", 7); close(fd); }')

    tb.append('    auto start = std::chrono::high_resolution_clock::now();')
    tb.append('    for (size_t i = 0; i < vectors.size(); ++i) {')
    tb.append('        const std::string& vec = vectors[i];')

    # Assign inputs from vec
    flat_idx = 0
    for name, msb, lsb in port_decls['inputs']:
        c_name = cpp_ident(name)
        if msb is not None and lsb is not None:
            base_shift = min(msb, lsb)
            tb.append(f'        vl_clear(top->{c_name});')
            step = 1 if msb <= lsb else -1
            for bit in range(msb, lsb + step, step):
                tb.append(f"        if (vec[{flat_idx}] == '1') vl_set_bit(top->{c_name}, {bit - base_shift});")
                flat_idx += 1
        else:
            tb.append(f"        top->{c_name} = vec[{flat_idx}] - '0';")
            flat_idx += 1

    tb.append('        top->eval();')
    tb.append('    }')
    tb.append('    auto end = std::chrono::high_resolution_clock::now();')

    if use_perf:
        tb.append('    fd = open("/tmp/rx_perf_ctrl", O_WRONLY | O_NONBLOCK);')
        tb.append('    if (fd >= 0) { write(fd, "disable\\n", 8); close(fd); }')

    tb.append('    auto elapsed = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start).count();')
    tb.append('    std::cout << "$ELAPSED_NS:" << elapsed << std::endl;')
    tb.append('    delete top;')
    tb.append('    return 0;')
    tb.append('}')

    with open(tb_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(tb) + '\n')


def run_verilator_harness_iwls(v_file: str, vectors: int, warmup: int,
                              use_perf: bool = False, perf_events: str = "") -> dict:
    filename    = os.path.basename(v_file)
    base_path   = os.path.splitext(v_file)[0]
    tb_file     = base_path + "_iwls_verilator_main.cpp"
    vector_file = base_path + "_iwls_verilator_vectors.txt"
    obj_dir     = base_path + "_iwls_verilator_obj_dir"

    gsclib_path = find_gsclib_path(v_file)
    if not gsclib_path:
        return {"engine": "Verilator", "file": filename, "error": "GSCLib_3.0.v library file not found"}

    if not shutil.which("verilator") or not shutil.which("make"):
        return {"engine": "Verilator", "file": filename, "error": "verilator or make not found in PATH"}

    try:
        module_name, port_decls, flat_inputs, flat_outputs, clock_idx, clock_port_name = parse_iwls_ports(v_file)
        logical_count = max(vectors - warmup, 1)

        rng = random.Random(42)
        physical_vectors = []
        for _ in range(logical_count):
            base_vec = [rng.randint(0, 1) for _ in range(len(flat_inputs))]
            if clock_idx != -1:
                setup = list(base_vec)
                setup[clock_idx] = 0
                trigger = list(base_vec)
                trigger[clock_idx] = 1
                physical_vectors.append(setup)
                physical_vectors.append(trigger)
            else:
                physical_vectors.append(base_vec)

        measured = len(physical_vectors)

        with open(vector_file, 'w', encoding='utf-8') as f:
            for vec in physical_vectors:
                f.write("".join(str(v) for v in vec) + "\n")

        generate_verilator_tb_iwls(v_file, tb_file, module_name, port_decls, flat_inputs, clock_port_name, use_perf=use_perf)

        t_comp_start = time.perf_counter_ns()
        comp_cmd = [
            "verilator", "-O3", "-Wno-fatal", "--default-language", "1364-2001", "--cc",
            gsclib_path, v_file,
            "--exe", tb_file,
            "--top-module", module_name,
            "--Mdir", obj_dir
        ]
        comp_res = subprocess.run(comp_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if comp_res.returncode != 0:
            return {"engine": "Verilator", "file": filename, "error": f"Verilator compilation failure: {comp_res.stderr.strip()}"}

        build_cmd = ["make", "-j", str(os.cpu_count() or 4), "-C", obj_dir, "-f", f"V{module_name}.mk", f"V{module_name}"]
        build_res = subprocess.run(build_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        t_comp_end = time.perf_counter_ns()
        compile_ms = (t_comp_end - t_comp_start) / 1_000_000.0

        if build_res.returncode != 0:
            return {"engine": "Verilator", "file": filename, "error": f"Make build failure: {build_res.stderr.strip()}"}

        exe_path = os.path.join(obj_dir, f"V{module_name}")
        run_cmd = [exe_path, vector_file]
        original_run_cmd = list(run_cmd)

        perf_data = f"perf_verilator_{filename}.data"
        perf_txt  = f"perf_verilator_{filename}.txt"
        if use_perf:
            cmd = ["perf", "record", "-m", "32", "-o", perf_data]
            if perf_events:
                cmd.extend(["-e", perf_events])
            cmd.extend(run_cmd)
            run_cmd = cmd

        t_run_start = time.perf_counter_ns()
        run_res = subprocess.run(run_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        t_run_end = time.perf_counter_ns()
        run_ms = (t_run_end - t_run_start) / 1_000_000.0

        if use_perf and run_res.returncode != 0:
            # Fallback to run without perf if perf record failed
            t_run_start = time.perf_counter_ns()
            run_res = subprocess.run(original_run_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            t_run_end = time.perf_counter_ns()
            run_ms = (t_run_end - t_run_start) / 1_000_000.0
        elif use_perf and os.path.exists(perf_data):
            rep = subprocess.run(["perf", "report", "-i", perf_data, "--stdio"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            with open(perf_txt, 'w', encoding='utf-8') as f:
                f.write(rep.stdout)
            for p in (perf_data, perf_data + ".old"):
                if os.path.exists(p):
                    try: os.remove(p)
                    except Exception: pass

        if run_res.returncode != 0:
            return {"engine": "Verilator", "file": filename, "error": f"Run failure: {run_res.stderr.strip()}"}

        sim_ms = None
        for line in run_res.stdout.splitlines():
            if line.startswith("$ELAPSED_NS:"):
                try:
                    elapsed_ns = int(line.split(":", 1)[1].strip())
                    sim_ms = elapsed_ns / 1_000_000.0
                except ValueError:
                    pass
                break

        result = {
            "engine": "Verilator",
            "file": filename,
            "compile_ms": compile_ms,
            "run_ms": run_ms,
            "total_ms": compile_ms + run_ms,
            "logical_vectors": logical_count,
            "physical_vectors": measured,
            "time_ms": sim_ms if sim_ms is not None else run_ms,
            "load_ms": compile_ms,
        }
        return result

    except Exception as e:
        return {"engine": "Verilator", "file": filename, "error": str(e)}
    finally:
        for p in (tb_file, vector_file):
            if p and os.path.exists(p):
                try: os.remove(p)
                except OSError: pass
        if obj_dir and os.path.exists(obj_dir):
            try: shutil.rmtree(obj_dir)
            except OSError: pass
