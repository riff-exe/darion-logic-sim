import sys
import os
import random
import time

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("reactor"))
sys.path.insert(0, os.path.abspath("tests/src"))

import Circuit
import engine.Const as Const
from benchmark import VerilogRunner
try:
    from benchmark_89 import SequentialVerilogRunner
except ImportError:
    SequentialVerilogRunner = None

# Selected diverse circuits from across ISCAS85, EPFL, and ISCAS89
CIRCUIT_SUITE = [
    # ISCAS85 Combinational
    {"category": "ISCAS85", "name": "c17",    "path": "tests/ISCAS85/c17.v",    "type": "comb", "vectors": 200},
    {"category": "ISCAS85", "name": "c432",   "path": "tests/ISCAS85/c432.v",   "type": "comb", "vectors": 200},
    {"category": "ISCAS85", "name": "c499",   "path": "tests/ISCAS85/c499.v",   "type": "comb", "vectors": 200},
    {"category": "ISCAS85", "name": "c1355",  "path": "tests/ISCAS85/c1355.v",  "type": "comb", "vectors": 200},
    {"category": "ISCAS85", "name": "c1908",  "path": "tests/ISCAS85/c1908.v",  "type": "comb", "vectors": 200},
    {"category": "ISCAS85", "name": "c6288",  "path": "tests/ISCAS85/c6288.v",  "type": "comb", "vectors": 50}, # 16x16 multiplier, deep paths
    # EPFL Benchmarks
    {"category": "EPFL",    "name": "ctrl",   "path": "tests/EPFL/ctrl.v",       "type": "comb", "vectors": 200},
    {"category": "EPFL",    "name": "dec",    "path": "tests/EPFL/dec.v",        "type": "comb", "vectors": 200},
    {"category": "EPFL",    "name": "int2float", "path": "tests/EPFL/int2float.v", "type": "comb", "vectors": 200},
    {"category": "EPFL",    "name": "adder",  "path": "tests/EPFL/adder.v",      "type": "comb", "vectors": 200},
    # ISCAS89 Sequential
    {"category": "ISCAS89", "name": "s27",    "path": "tests/ISCAS89/s27.v",    "type": "seq",  "vectors": 200},
    {"category": "ISCAS89", "name": "s382",   "path": "tests/ISCAS89/s382.v",   "type": "seq",  "vectors": 100},
    {"category": "ISCAS89", "name": "s641",   "path": "tests/ISCAS89/s641.v",   "type": "seq",  "vectors": 100},
]

def verify_and_benchmark():
    print("=" * 115)
    print("  MULTI-SUITE VERIFICATION & PERFORMANCE BENCHMARK: SYNCHRONOUS TIMED PRIORITY QUEUE")
    print("=" * 115)
    header = f"| {'Suite':<8} | {'Circuit':<10} | {'Type':<5} | {'Gates':<7} | {'Vecs':<5} | {'Match Rate':<12} | {'Timed ms':<9} | {'Zero ms':<8} | {'Slowdown':<9} | {'Tasks':<10} | {'Status':<6} |"
    print(header)
    print(f"|{'-'*10}|{'-'*12}|{'-'*7}|{'-'*9}|{'-'*7}|{'-'*14}|{'-'*11}|{'-'*10}|{'-'*11}|{'-'*12}|{'-'*8}|")

    all_passed = True
    total_evals_timed = 0
    total_tasks_timed = 0
    total_time_timed = 0.0
    total_time_zero = 0.0

    summary_rows = []

    for item in CIRCUIT_SUITE:
        cat = item["category"]
        name = item["name"]
        path = item["path"]
        c_type = item["type"]
        v_count = item["vectors"]

        if not os.path.exists(path):
            print(f"Skipping {path} (not found)")
            continue

        if c_type == "comb":
            # Combinational Runner
            runner_ref = VerilogRunner(path, Circuit.Circuit, Const, is_reactor=True)
            runner_timed = VerilogRunner(path, Circuit.Circuit, Const, is_reactor=True)
            inputs = runner_ref.input_vars
            num_inputs = len(inputs)
            gate_count = runner_ref.circuit.infolist_size

            # Generate random test vectors
            rng = random.Random(42)
            raw_vectors = [[rng.randint(0, 1) for _ in range(num_inputs)] for _ in range(v_count)]

            # 1. Zero-delay Reference Run (rx-prop)
            t0_zero = time.perf_counter()
            ref_results = runner_ref.run_vectors(raw_vectors)
            t1_zero = time.perf_counter()
            zero_ms = (t1_zero - t0_zero) * 1000.0

            # 2. Timed Simulation Run (Pure Priority Queue)
            batches = runner_timed.build_batches(raw_vectors)
            runner_timed.circuit.simulate(Const.SIMULATE)
            runner_timed.circuit.eval_count = 0

            timed_results = []
            tasks_count = 0
            t0_timed = time.perf_counter()
            for b in batches:
                tasks_count += runner_timed.circuit.batch_toggle_timed(b)
                timed_results.append([int(g.output) for g in runner_timed.output_objects])
            t1_timed = time.perf_counter()
            timed_ms = (t1_timed - t0_timed) * 1000.0

            total_evals_timed += runner_timed.circuit.eval_count
            total_tasks_timed += tasks_count
            total_time_timed += (t1_timed - t0_timed)
            total_time_zero += (t1_zero - t0_zero)

        else:
            # Sequential Runner (ISCAS89)
            runner_ref = SequentialVerilogRunner(path, Circuit.Circuit, Const, is_reactor=True)
            runner_timed = SequentialVerilogRunner(path, Circuit.Circuit, Const, is_reactor=True)
            inputs = runner_ref.input_vars
            num_inputs = len(inputs)
            gate_count = runner_ref.circuit.infolist_size

            rng = random.Random(42)
            logical_vectors = [[rng.randint(0, 1) for _ in range(num_inputs)] for _ in range(v_count)]

            # Build physical vectors (setup clk=0, trigger clk=1)
            clock_idx = -1
            clock_var = runner_ref._find_clock_var()
            if clock_var is not None:
                for idx, v in enumerate(runner_ref.input_vars):
                    if v is clock_var:
                        clock_idx = idx
                        break

            physical_vectors = []
            if clock_idx != -1:
                for base in logical_vectors:
                    s_vec = list(base); s_vec[clock_idx] = 0; physical_vectors.append(s_vec)
                    t_vec = list(base); t_vec[clock_idx] = 1; physical_vectors.append(t_vec)
            else:
                physical_vectors = logical_vectors

            # 1. Warmup both runners identically with 50 reset flush cycles
            warmup_batches = runner_ref.build_reset_batches(50)
            runner_ref.circuit.simulate(Const.SIMULATE)
            runner_timed.circuit.simulate(Const.SIMULATE)
            for wb in warmup_batches:
                runner_ref.circuit.batch_toggle(wb)
                runner_timed.circuit.batch_toggle_timed(wb)

            batches_ref = runner_ref.build_physical_batches(physical_vectors)
            batches_timed = runner_timed.build_physical_batches(physical_vectors)
            batch_size = len(inputs) + (1 if getattr(runner_ref, 'const_1_node', None) else 0) + (1 if getattr(runner_ref, 'const_0_node', None) else 0)

            # 2. Zero-delay Reference Run
            t0_zero = time.perf_counter()
            ref_results = []
            for b in batches_ref:
                runner_ref.circuit.batch_toggle(b, batch_size)
                ref_results.append([int(g.output) for g in runner_ref.output_objects])
            t1_zero = time.perf_counter()
            zero_ms = (t1_zero - t0_zero) * 1000.0

            # 3. Timed Simulation Run
            runner_timed.circuit.eval_count = 0
            timed_results = []
            tasks_count = 0

            t0_timed = time.perf_counter()
            for b in batches_timed:
                tasks_count += runner_timed.circuit.batch_toggle_timed(b)
                timed_results.append([int(g.output) for g in runner_timed.output_objects])
            t1_timed = time.perf_counter()
            timed_ms = (t1_timed - t0_timed) * 1000.0

            total_evals_timed += runner_timed.circuit.eval_count
            total_tasks_timed += tasks_count
            total_time_timed += (t1_timed - t0_timed)
            total_time_zero += (t1_zero - t0_zero)

        # Verification comparison
        matches = sum(1 for r, t in zip(ref_results, timed_results) if r == t)
        match_pct = (matches / len(ref_results)) * 100.0
        status = "PASS" if matches == len(ref_results) else "FAIL"
        if matches != len(ref_results):
            all_passed = False

        slowdown = (timed_ms / zero_ms) if zero_ms > 0 else 0.0

        row = f"| {cat:<8} | {name:<10} | {c_type:<5} | {gate_count:<7,} | {v_count:<5} | {match_pct:6.2f}% ({matches}/{len(ref_results)}) | {timed_ms:7.2f} ms | {zero_ms:6.2f} ms | {slowdown:6.2f}x    | {tasks_count:<10,} | {status:<6} |"
        print(row)
        summary_rows.append({
            "cat": cat, "name": name, "type": c_type, "gates": gate_count, "vectors": len(ref_results),
            "matches": matches, "match_pct": match_pct, "timed_ms": timed_ms, "zero_ms": zero_ms,
            "slowdown": slowdown, "tasks": tasks_count, "status": status
        })

    print("=" * 115)
    if all_passed:
        print(">> 100.0% BIT-FOR-BIT VERIFICATION PASSED ACROSS ALL CIRCUITS & TEST VECTORS! <<")
    else:
        print(">> SOME CIRCUITS FAILED VERIFICATION <<")

    print("\n" + "=" * 60)
    print("  OVERALL TIMING SIMULATION STATS ACROSS ALL SUITES")
    print("=" * 60)
    print(f"Total Priority Queue Tasks : {total_tasks_timed:,} tasks")
    print(f"Total Gate Evaluations     : {total_evals_timed:,} evaluations")
    print(f"Total Timed Wall Time      : {total_time_timed*1000:.2f} ms ({total_time_timed:.4f} s)")
    print(f"Total Zero-Delay Wall Time : {total_time_zero*1000:.2f} ms ({total_time_zero:.4f} s)")
    overall_slowdown = total_time_timed / total_time_zero if total_time_zero > 0 else 0.0
    print(f"Average Slowdown vs Zero   : {overall_slowdown:.2f}x")
    task_rate = total_tasks_timed / total_time_timed if total_time_timed > 0 else 0.0
    eval_rate = (total_evals_timed / total_time_timed) / 1e6 if total_time_timed > 0 else 0.0
    print(f"Priority Queue Throughput  : {task_rate/1e6:.2f} Million Tasks/sec")
    print(f"Gate Evaluation Throughput : {eval_rate:.2f} MEval/sec")
    print("=" * 60)

if __name__ == "__main__":
    verify_and_benchmark()
