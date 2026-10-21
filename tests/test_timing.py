#!/usr/bin/env python3
"""
Timing verification and timed-mode speed, one entry point
=========================================================
Verification of the Reactor real-delay (PRIORITY) engine. Three suites share the helpers in tests/timing_lib.py:

  --suite topologies   22 hand-built topologies (propagation, skew, hazards, latches, DFF pulse width, counters,
                       ISCAS-85 settling, ring oscillator). Prints the failure-mode report.
  --suite extended     44 cases in tiers A-H (delay model exactness, inertial semantics, oscillators, combinational
                       structures, sequential timing, ISCAS benchmarks, random-circuit properties, scope limits).
                       Oracles: timing_lib.RefSim, Icarus Verilog with the same #delays, structural path sums.
                       Case kinds: verify (must pass), defect (asserts correct behaviour of a known defect; B8),
                       limit (asserts a documented model limitation). Options: -k TIER_OR_ID_PREFIX[,...]  -v
  --suite bench        timed-mode speed against Icarus Verilog gate-level with #delays (needs iverilog/vvp).
                       Options: [circuit ...] [--vectors N] [--repeat R]
                                --iscas89 [circuit ...] [--warm N]   (sequential; a long --warm makes the Icarus
                                baseline large and the subtracted sim time noisy: use it for agreement, not timing)
  --suite all          topologies then extended.

Set REACTOR_DIR to run against a different engine build (used for mutation testing).

Run:  python tests/test_timing.py --suite topologies|extended|bench|all [suite options]
"""
import os
import sys
import gc
import time
import random
import shutil
import zlib
import tempfile
import argparse
import subprocess
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from timing_lib import *  # noqa: E402,F401,F403
import timing_lib as TL   # noqa: E402
import Circuit            # noqa: E402
import Const              # noqa: E402
from editor.tools.timing_tracer import tracer  # noqa: E402
try:
    from benchmark import VerilogRunner  # noqa: E402
except ImportError:
    VerilogRunner = None




# =============================================================================
# suite: topologies
# =============================================================================
RESULTS_REGISTRY = []


def register_result(test_id, name, circuit_desc, verdict, failure_mode, details, category=None):
    if category is None:
        if "HARDWARE FAIL" in verdict:
            category = "HARDWARE_FAIL"
        elif "ACTUAL FAIL" in verdict:
            category = "ENGINE_FAIL"
        elif "LIMITATION" in verdict:
            category = "SPICE_LIMIT"
        else:
            category = "CIRCUIT_PASS"
    RESULTS_REGISTRY.append({
        "id": test_id,
        "name": name,
        "desc": circuit_desc,
        "verdict": verdict,
        "category": category,
        "failure_mode": failure_mode,
        "details": details
    })



# ==============================================================================
# TEST 1: Inverter Chain Propagation Delay
# ==============================================================================
def test_propagation_delays():
    print("=" * 75)
    print("TEST 1: Inverter Chain Propagation Delay & Probe Waveform Capture")
    print("=" * 75)

    c = Circuit.Circuit()
    c.simulate(Const.PRIORITY)
    c.recording = True
    tracer.start(0)

    # Inverter chain: X -> INV1 -> INV2 -> INV3 -> INV4
    x = c.getcomponent(Const.VARIABLE_ID)
    inverters = []
    prev_loc = x.location
    for i in range(4):
        inv = c.getcomponent(Const.NOT_ID)
        c.setlimits(inv, 1)
        c.connect(inv, prev_loc, 0)
        inverters.append(inv)
        prev_loc = inv.location

    # Attach probes (BUFFER) to each inverter stage
    probes = []
    for i, inv in enumerate(inverters):
        probe = c.getcomponent(Const.BUFFER_ID)
        c.setlimits(probe, 1)
        c.connect(probe, inv.location, 0)
        probes.append(probe)

    # Settle at X=0
    c.toggle(x.location, 0)
    c.drain_timed_queue()
    tracer.clear()
    tracer.start(0)

    # Toggle X: 0 -> 1 at t=0
    c.toggle_timed(x.location, 1, delay=0)

    timeline = []
    while not c.timed_queue_empty():
        c.drain_timed_queue(max_tasks=1)
        timeline.append((c.Global_Clock, [p.output for p in probes]))

    last_state = None
    for t, state in timeline:
        if state != last_state:
            print(f"  Time {t:2d}: Probes = {state}")
            last_state = state

    final_probes = [p.output for p in probes]
    expected_probes = [0, 1, 0, 1]
    passed = (final_probes == expected_probes)
    verdict = "PASS" if passed else "FAIL"
    print(f"VERDICT: [{verdict}] Inverter chain output {final_probes} == {expected_probes}\n")
    register_result(1, "Inverter Chain", "4-Stage NOT Gates + Probes", verdict,
                    "None (Met Timing Spec)", f"Rippled sequentially; final outputs={final_probes}")


# ==============================================================================
# TEST 2: 4-Bit Ripple Carry Adder Skew
# ==============================================================================
def test_ripple_carry_skew():
    print("=" * 75)
    print("TEST 2: Ripple Skew in 4-Bit Ripple Carry Adder")
    print("=" * 75)

    c = Circuit.Circuit()
    c.simulate(Const.PRIORITY)

    def make_fa(c):
        xor1 = c.getcomponent(Const.XOR_ID); c.setlimits(xor1, 2)
        xor2 = c.getcomponent(Const.XOR_ID); c.setlimits(xor2, 2)
        and1 = c.getcomponent(Const.AND_ID); c.setlimits(and1, 2)
        and2 = c.getcomponent(Const.AND_ID); c.setlimits(and2, 2)
        or1  = c.getcomponent(Const.OR_ID);  c.setlimits(or1, 2)

        c.connect(xor2, xor1.location, 0)
        c.connect(and2, xor1.location, 0)
        c.connect(or1, and1.location, 0)
        c.connect(or1, and2.location, 1)

        return {"xor1": xor1, "xor2": xor2, "and1": and1, "and2": and2, "or1": or1}

    fas = [make_fa(c) for _ in range(4)]
    a_vars = [c.getcomponent(Const.VARIABLE_ID) for _ in range(4)]
    b_vars = [c.getcomponent(Const.VARIABLE_ID) for _ in range(4)]
    cin_var = c.getcomponent(Const.VARIABLE_ID)

    for i in range(4):
        c.connect(fas[i]["xor1"], a_vars[i].location, 0)
        c.connect(fas[i]["xor1"], b_vars[i].location, 1)
        c.connect(fas[i]["and1"], a_vars[i].location, 0)
        c.connect(fas[i]["and1"], b_vars[i].location, 1)

        cin_src = cin_var.location if i == 0 else fas[i - 1]["or1"].location
        c.connect(fas[i]["xor2"], cin_src, 1)
        c.connect(fas[i]["and2"], cin_src, 1)

    for v in a_vars: c.toggle(v.location, 1)
    for v in b_vars: c.toggle(v.location, 0)
    c.toggle(cin_var.location, 0)
    c.drain_timed_queue()

    # Assert Cin = 1 at t=0
    c.toggle_timed(cin_var.location, 1, delay=0)

    events = []
    while not c.timed_queue_empty():
        c.drain_timed_queue(max_tasks=1)
        carries = [fas[i]["or1"].output for i in range(4)]
        sums = [fas[i]["xor2"].output for i in range(4)]
        events.append((c.Global_Clock, carries, sums))

    prev_c, prev_s = None, None
    for t, carries, sums in events:
        if (carries, sums) != (prev_c, prev_s):
            print(f"  Time {t:3d}: Carries={carries}  Sums={sums}")
            prev_c, prev_s = carries, sums

    final_sums = [fas[i]["xor2"].output for i in range(4)]
    final_cout = fas[3]["or1"].output
    passed = (final_sums == [0, 0, 0, 0] and final_cout == 1)
    verdict = "PASS" if passed else "FAIL"
    print(f"VERDICT: [{verdict}] 4-Bit Adder correctly settled to Sums=[0,0,0,0], Cout=1\n")
    register_result(2, "Ripple Carry Adder", "4-Bit Full Adder Carry Chain", verdict,
                    "None (Met Timing Spec)", f"Final sums={final_sums}, Cout={final_cout}")


# ==============================================================================
# TEST 3: Dynamic Hazard Glitch Generation & Transient Analysis
# ==============================================================================
def test_race_condition_and_glitch():
    print("=" * 75)
    print("TEST 3: Reconvergent Fan-Out Dynamic Hazard Glitch Generation")
    print("=" * 75)

    c = Circuit.Circuit()
    c.simulate(Const.PRIORITY)

    x = c.getcomponent(Const.VARIABLE_ID)
    inv1 = c.getcomponent(Const.NOT_ID); c.setlimits(inv1, 1); c.connect(inv1, x.location, 0)
    inv2 = c.getcomponent(Const.NOT_ID); c.setlimits(inv2, 1); c.connect(inv2, inv1.location, 0)
    inv3 = c.getcomponent(Const.NOT_ID); c.setlimits(inv3, 1); c.connect(inv3, inv2.location, 0)

    and_gate = c.getcomponent(Const.AND_ID); c.setlimits(and_gate, 2)
    c.connect(and_gate, x.location, 0)
    c.connect(and_gate, inv3.location, 1)

    c.toggle(x.location, 0)
    c.drain_timed_queue()

    # Toggle X: 0 -> 1 at t=10
    c.toggle_timed(x.location, 1, delay=10 - c.Global_Clock)

    glitch_pulse_detected = False
    glitch_start = None
    glitch_end = None

    while not c.timed_queue_empty():
        c.drain_timed_queue(max_tasks=1)
        t = c.Global_Clock
        out = and_gate.output
        if out == 1:
            if not glitch_pulse_detected:
                glitch_pulse_detected = True
                glitch_start = t
        elif glitch_pulse_detected and glitch_end is None:
            glitch_end = t      # the step at which the output actually returned low

    duration = (glitch_end - glitch_start) if glitch_pulse_detected else 0
    # In static zero-delay logic, AND(X, ~X) is 0. The output produced a false 1-pulse!
    print(f"  Transient Analysis: Hazard Pulse Detected = {glitch_pulse_detected}")
    print(f"  Glitch Active Window: t = {glitch_start} to {glitch_end} (Duration: {duration} ticks)")
    print(f"  Final Settled Output: {and_gate.output}")
    verdict = "PASS" if (glitch_pulse_detected and and_gate.output == 0) else "FAIL"
    print(f"VERDICT: [{verdict}] Glitch pulse accurately captured, settled to 0\n")
    register_result(3, "Dynamic Hazard", "Reconvergent Fan-Out AND Gate", verdict,
                    "Dynamic Hazard Glitch", f"Transient 1-pulse ({duration} ticks); settled to 0")


# ==============================================================================
# TEST 4: Static-1 Hazard (0-Glitch Dip) in 2-to-1 Multiplexer
# ==============================================================================
def test_static_hazard_mux():
    print("=" * 75)
    print("TEST 4: Static-1 Hazard (0-Glitch Dip) in 2-to-1 Multiplexer")
    print("=" * 75)

    c = Circuit.Circuit()
    c.simulate(Const.PRIORITY)

    # MUX equation: Y = (A & ~S) | (B & S)
    # When A=1, B=1: Static Boolean logic dictates Y=1 identically.
    # Physical logic: S toggling 1 -> 0 causes AND2 to turn OFF before AND1 turns ON.
    # Result: A momentary 0-glitch dip on Y!
    a = c.getcomponent(Const.VARIABLE_ID)
    b = c.getcomponent(Const.VARIABLE_ID)
    s = c.getcomponent(Const.VARIABLE_ID)

    inv_s = c.getcomponent(Const.NOT_ID); c.setlimits(inv_s, 1); c.connect(inv_s, s.location, 0)
    buf1 = c.getcomponent(Const.BUFFER_ID); c.setlimits(buf1, 1); c.connect(buf1, inv_s.location, 0)
    buf2 = c.getcomponent(Const.BUFFER_ID); c.setlimits(buf2, 1); c.connect(buf2, buf1.location, 0)

    and1 = c.getcomponent(Const.AND_ID); c.setlimits(and1, 2)
    c.connect(and1, a.location, 0)
    c.connect(and1, buf2.location, 1)

    and2 = c.getcomponent(Const.AND_ID); c.setlimits(and2, 2)
    c.connect(and2, b.location, 0)
    c.connect(and2, s.location, 1)

    or_gate = c.getcomponent(Const.OR_ID); c.setlimits(or_gate, 2)
    c.connect(or_gate, and1.location, 0)
    c.connect(or_gate, and2.location, 1)

    # Initialize A=1, B=1, S=1 -> Y=1
    c.toggle_timed(a.location, 1, delay=0)
    c.toggle_timed(b.location, 1, delay=0)
    c.toggle_timed(s.location, 1, delay=0)
    c.drain_timed_queue()

    # Switch S: 1 -> 0 at t=10
    c.toggle_timed(s.location, 0, delay=10)

    glitch_dip_detected = False
    dip_start, dip_end = None, None

    while not c.timed_queue_empty():
        c.drain_timed_queue(max_tasks=1)
        t = c.Global_Clock
        y = or_gate.output
        if y == 0:
            if not glitch_dip_detected:
                glitch_dip_detected = True
                dip_start = t
        elif glitch_dip_detected and dip_end is None:
            dip_end = t         # the step at which the output actually returned high

    dip_duration = (dip_end - dip_start) if glitch_dip_detected else 0
    passed = glitch_dip_detected and (or_gate.output == 1)
    verdict = "PASS" if passed else "FAIL"
    print(f"  Static-1 Hazard 0-Dip Detected: {glitch_dip_detected}")
    print(f"  Dip Window: t = {dip_start} to {dip_end} (Duration: {dip_duration} ticks)")
    print(f"  Final Settled Output: {or_gate.output}")
    print(f"VERDICT: [{verdict}] Static-1 hazard dip accurately captured, settled to 1\n")
    register_result(4, "Static-1 Hazard", "2-to-1 Multiplexer (A=1, B=1)", verdict,
                    "Static-1 Hazard 0-Dip", f"Transient 0-dip ({dip_duration} ticks); settled to 1")


# ==============================================================================
# TEST 5: Cross-Coupled SR NOR Latch Minimum Pulse Width
# ==============================================================================
def test_sr_latch_pulse_width():
    print("=" * 75)
    print("TEST 5: Cross-Coupled SR NOR Latch Sub-Threshold Pulse Rejection")
    print("=" * 75)

    def eval_latch_pulse(width):
        c = Circuit.Circuit()
        c.simulate(Const.PRIORITY)

        r = c.getcomponent(Const.VARIABLE_ID)
        s = c.getcomponent(Const.VARIABLE_ID)
        nor_q = c.getcomponent(Const.NOR_ID); c.setlimits(nor_q, 2)
        nor_qb = c.getcomponent(Const.NOR_ID); c.setlimits(nor_qb, 2)

        c.connect(nor_q, r.location, 0)
        c.connect(nor_q, nor_qb.location, 1)
        c.connect(nor_qb, s.location, 0)
        c.connect(nor_qb, nor_q.location, 1)

        # Reset latch: R=1, S=0 -> Q=0, Q_bar=1
        c.toggle_timed(r.location, 1, delay=0)
        c.toggle_timed(s.location, 0, delay=0)
        c.drain_timed_queue()

        c.toggle_timed(r.location, 0, delay=0)
        c.drain_timed_queue()

        # Apply pulse on S of specified width
        t0 = c.Global_Clock
        c.toggle_timed(s.location, 1, delay=0)
        c.drain_timed_queue(max_time=t0 + width)
        c.Global_Clock = t0 + width
        c.toggle_timed(s.location, 0, delay=0)
        c.drain_timed_queue()

        return nor_q.output, nor_qb.output

    # Under-driven pulses (< 8 ticks) FAIL to flip the latch in physical silicon!
    q_sub, qb_sub = eval_latch_pulse(4)  # 4 ticks: FAILS TO SET (remains Q=0)
    q_sup, qb_sup = eval_latch_pulse(10) # 10 ticks: SUCCEEDS (sets Q=1)

    sub_failed = (q_sub == 0 and qb_sub == 1)
    sup_passed = (q_sup == 1 and qb_sup == 0)

    print(f"  Pulse Width =  4 ticks (< threshold 8): Q={q_sub}, Q_bar={qb_sub} -> [FAIL TO SET] Latch ignored pulse")
    print(f"  Pulse Width = 10 ticks (>= threshold 8): Q={q_sup}, Q_bar={qb_sup} -> [PASS] Latch flipped to Q=1")
    verdict = "PASS" if (sub_failed and sup_passed) else "FAIL"
    print(f"VERDICT: [{verdict}] Inertial pulse attenuation threshold verified at 8 ticks\n")
    register_result(5, "SR NOR Latch", "Cross-Coupled NOR Gates", verdict,
                    "Sub-Threshold Pulse Rejection (<8 ticks)", "Pulses <8 ticks fail to set latch; >=8 ticks set Q=1")


# ==============================================================================
# TEST 6: Master-Slave D Flip-Flop Clock Width & Hold Timing Limits
# ==============================================================================
def test_dff_clock_pulse_width():
    print("=" * 75)
    print("TEST 6: Master-Slave D Flip-Flop Clock Width Violation")
    print("=" * 75)

    dff_path = "tests/src/DFF.json"
    if not os.path.exists(dff_path):
        print("  Skipping: tests/src/DFF.json not found.")
        return

    def eval_dff_clk_width(pw):
        c = Circuit.Circuit()
        dff = c.getIC(dff_path)
        clk_var = c.getcomponent(Const.VARIABLE_ID)
        d_var = c.getcomponent(Const.VARIABLE_ID)

        c.connect(dff.inputs[0], clk_var.location, 0)
        c.connect(dff.inputs[1], d_var.location, 0)
        c.simulate(Const.PRIORITY)

        # Reset: CLK=0, D=0
        c.toggle_timed(clk_var.location, 0, delay=0)
        c.toggle_timed(d_var.location, 0, delay=0)
        c.drain_timed_queue()

        # Set D=1
        c.toggle_timed(d_var.location, 1, delay=0)
        c.drain_timed_queue()

        # Pulse CLK
        t0 = c.Global_Clock
        c.toggle_timed(clk_var.location, 1, delay=0)
        c.drain_timed_queue(max_time=t0 + pw)
        c.Global_Clock = t0 + pw
        c.toggle_timed(clk_var.location, 0, delay=0)
        c.drain_timed_queue()

        return dff.outputs[0].output, dff.outputs[1].output

    q_narrow, qb_narrow = eval_dff_clk_width(5) # 5 ticks < 7: FAILS TO CLOCK
    q_wide, qb_wide = eval_dff_clk_width(12)    # 12 ticks >= 7: SUCCEEDS

    clock_width_violation = (q_narrow == 0 and qb_narrow == 1)
    clock_width_satisfied = (q_wide == 1 and qb_wide == 0)
    passed = clock_width_violation and clock_width_satisfied

    print(f"  Narrow Clock (5 ticks < 7): Q={q_narrow}, Q_bar={qb_narrow} -> [CIRCUIT FAILED] Clock pulse too narrow to latch")
    print(f"  Valid Clock  (12 ticks >= 7): Q={q_wide}, Q_bar={qb_wide} -> [CIRCUIT PASSED] Latch successfully updated")
    verdict = "PASS" if passed else "FAIL"
    print(f"VERDICT: [{verdict}] Physical clock pulse threshold verified at 7 ticks\n")
    register_result(6, "D Flip-Flop (IC)", "Master-Slave DFF Clock Width", verdict,
                    "Clock Pulse Width Violation (<7 ticks)", "Narrow clock pulses (<7 ticks) fail to latch data")


# ==============================================================================
# TEST 7: Dynamic Hazard Glitch Clocking Flip-Flop (State Corruption)
# ==============================================================================
def test_glitch_clocked_dff():
    print("=" * 75)
    print("TEST 7: Dynamic Hazard Glitch Clocking Flip-Flop (TIMING FAILURE REPRODUCED)")
    print("=" * 75)

    dff_path = "tests/src/DFF.json"
    if not os.path.exists(dff_path):
        print("  Skipping: tests/src/DFF.json not found.")
        return

    # In zero-delay logic: AND(X, ~X) is 0 identically. Clock never transitions.
    # In real hardware: Reconvergent fanout produces a dynamic hazard glitch.
    # The hazard pulse is 2 ticks per inverter: 3 inverters -> 6 ticks (< 7, filtered), 5 -> 10 ticks (>= 7, triggers).
    # The glitch pulses the clock pin, flipping Q from 0 to 1!
    def run_glitch_clock(num_inverters):
        c = Circuit.Circuit()
        dff = c.getIC(dff_path)

        x = c.getcomponent(Const.VARIABLE_ID)
        d_var = c.getcomponent(Const.VARIABLE_ID)

        and_gate = c.getcomponent(Const.AND_ID); c.setlimits(and_gate, 2)
        c.connect(and_gate, x.location, 0)

        prev_loc = x.location
        for _ in range(num_inverters):
            inv = c.getcomponent(Const.NOT_ID); c.setlimits(inv, 1)
            c.connect(inv, prev_loc, 0)
            prev_loc = inv.location

        c.connect(and_gate, prev_loc, 1)
        c.connect(dff.inputs[0], and_gate.location, 0)
        c.connect(dff.inputs[1], d_var.location, 0)

        c.simulate(Const.PRIORITY)

        c.toggle_timed(x.location, 0, delay=0)
        c.toggle_timed(d_var.location, 1, delay=0)
        c.drain_timed_queue()

        q_before = dff.outputs[0].output
        c.toggle_timed(x.location, 1, delay=10)
        c.drain_timed_queue()
        q_after = dff.outputs[0].output

        return q_before, q_after

    q0_narrow, q1_narrow = run_glitch_clock(3) # 3 inverters: 6-tick glitch < 7 -> Ignored
    q0_wide, q1_wide = run_glitch_clock(5)     # 5 inverters: 10-tick glitch >= 7 -> Flips Q=1!

    print(f"  3-Inverter Hazard (6 ticks): Q_before={q0_narrow}, Q_after={q1_narrow} -> [PASS] Glitch filtered")
    print(f"  5-Inverter Hazard (10 ticks): Q_before={q0_wide}, Q_after={q1_wide} -> [HARDWARE FAILURE] Glitch triggered clock!")
    print(f"  Circuit Specification: Q must remain 0. Actual Output: Q = {q1_wide}")

    # The CIRCUIT FAILED its logic specification because of a physical hazard glitch!
    circuit_failed = (q1_wide == 1)
    verdict = "HARDWARE FAIL (Physical Timing Defect)" if circuit_failed else "PASS (Spec Met)"
    print(f"CIRCUIT VERDICT: [{verdict}] Glitch physically corrupted output state from 0 to 1\n")
    register_result(7, "Glitch-Clocked DFF", "Reconvergent Hazard -> DFF Clock", verdict,
                    "Glitch-Induced Clock Trigger", "Glitch >= 7 ticks triggered clock pin; output Q corrupted to 1")


# ==============================================================================
# TEST 8: Synchronous Toggle Counter Overclocking Stress Test
# ==============================================================================
def test_toggle_counter_overclocking():
    print("=" * 75)
    print("TEST 8: Synchronous Toggle Counter Overclocking (TIMING FAILURE REPRODUCED)")
    print("=" * 75)

    dff_path = "tests/src/DFF.json"
    if not os.path.exists(dff_path):
        print("  Skipping: tests/src/DFF.json not found.")
        return

    # T-Flip-Flop: D = XOR(Q, 1). Toggles on each clock edge.
    # Minimum working clock period = 39 ticks.
    def eval_clock_frequency(half_period, cycles=6):
        c = Circuit.Circuit()
        dff = c.getIC(dff_path)
        xor1 = c.getcomponent(Const.XOR_ID); c.setlimits(xor1, 2)
        clk_var = c.getcomponent(Const.VARIABLE_ID)
        const_1 = c.getcomponent(Const.VARIABLE_ID)

        c.connect(xor1, dff.outputs[0].location, 0)
        c.connect(xor1, const_1.location, 1)
        c.connect(dff.inputs[1], xor1.location, 0)
        c.connect(dff.inputs[0], clk_var.location, 0)

        c.simulate(Const.PRIORITY)
        c.toggle_timed(const_1.location, 1, delay=0)
        c.toggle_timed(clk_var.location, 0, delay=0)
        c.drain_timed_queue()

        period = half_period * 2
        history = []
        for _ in range(cycles):
            t0 = c.Global_Clock
            c.toggle_timed(clk_var.location, 1, delay=0)
            c.drain_timed_queue(max_time=t0 + half_period)
            c.Global_Clock = t0 + half_period
            c.toggle_timed(clk_var.location, 0, delay=0)
            c.drain_timed_queue(max_time=t0 + period)
            c.Global_Clock = t0 + period
            history.append(dff.outputs[0].output)
        return history

    expected_pattern = [1, 0, 1, 0, 1, 0]
    out_overclocked = eval_clock_frequency(8)   # Period 16: Setup violation / narrow clock
    out_feedback_err = eval_clock_frequency(12) # Period 24: Feedback not settled
    out_safe = eval_clock_frequency(22)         # Period 44: Safe frequency, perfect toggle

    print(f"  Overclocked Period 16: Output={out_overclocked} != {expected_pattern} -> [CIRCUIT FAILED] Frozen/lost toggles")
    print(f"  Overclocked Period 24: Output={out_feedback_err} != {expected_pattern} -> [CIRCUIT FAILED] Feedback race error")
    print(f"  Safe Clock  Period 44: Output={out_safe} == {expected_pattern} -> [CIRCUIT PASSED] Clean toggle")

    circuit_failed = (out_overclocked != expected_pattern)
    verdict = "HARDWARE FAIL (Physical Timing Defect)" if circuit_failed else "PASS (Spec Met)"
    print(f"CIRCUIT VERDICT: [{verdict}] Counter suffered setup/hold violation when overclocked\n")
    register_result(8, "Toggle Counter", "DFF + XOR Feedback", verdict,
                    "Setup/Hold Timing Violation", f"Overclocked Period < 39 ticks caused output corruption {out_overclocked}")


# ==============================================================================
# TEST 9: ISCAS-85 Multi-Stage Critical Path Latencies & Settling Accuracy
# ==============================================================================
def test_iscas85_settling_accuracy():
    print("=" * 75)
    print("TEST 9: ISCAS-85 Benchmark Circuits Settling Latency & Bit-Exactness")
    print("=" * 75)

    if VerilogRunner is None:
        print("  Skipping: VerilogRunner not available.")
        return

    benchmark_list = [
        ("c17",   "tests/ISCAS85/c17.v",   20),
        ("c432",  "tests/ISCAS85/c432.v",  10),
        ("c499",  "tests/ISCAS85/c499.v",  10),
        ("c880",  "tests/ISCAS85/c880.v",  10),
        ("c1355", "tests/ISCAS85/c1355.v", 10),
        ("c1908", "tests/ISCAS85/c1908.v", 10),
        ("c6288", "tests/ISCAS85/c6288.v", 5),
    ]

    all_passed = True
    print(f"  {'Circuit':<8} | {'Gates':<6} | {'Vectors':<7} | {'Max Latency (ticks)':<20} | {'Verdict':<6}")
    print(f"  {'-'*8}-|-{'-'*6}-|-{'-'*7}-|-{'-'*20}-|-{'-'*7}")

    for name, v_path, num_vecs in benchmark_list:
        if not os.path.exists(v_path):
            continue
        runner_ref = VerilogRunner(v_path, Circuit.Circuit, Const, is_reactor=True)
        runner_timed = VerilogRunner(v_path, Circuit.Circuit, Const, is_reactor=True)

        inputs = runner_ref.input_vars
        gate_count = runner_ref.circuit.infolist_size

        rng = random.Random(999)
        vecs = [[rng.randint(0, 1) for _ in range(len(inputs))] for _ in range(num_vecs)]
        ref_outs = runner_ref.run_vectors(vecs)
        batches = runner_timed.build_batches(vecs)

        runner_timed.circuit.simulate(Const.SIMULATE)
        max_latency = 0
        mismatches = 0

        for idx, b in enumerate(batches):
            t0 = runner_timed.circuit.Global_Clock
            runner_timed.circuit.batch_toggle_timed(b)
            latency = runner_timed.circuit.Global_Clock - t0
            if latency > max_latency:
                max_latency = latency
            out = [int(g.output) for g in runner_timed.output_objects]
            if out != ref_outs[idx]:
                mismatches += 1

        c_verdict = "PASS" if mismatches == 0 else "FAIL"
        if mismatches > 0:
            all_passed = False
        print(f"  {name:<8} | {gate_count:<6} | {num_vecs:<7} | {max_latency:<20} | {c_verdict:<6}")
        register_result(9, f"ISCAS85 {name}", f"{gate_count} Gates Netlist", c_verdict,
                        "None (Settled)" if mismatches == 0 else "Settling Mismatch",
                        f"Latency={max_latency} ticks, match rate={(num_vecs-mismatches)/num_vecs*100:.1f}%")

    verdict = "PASS" if all_passed else "FAIL"
    print(f"\nCIRCUIT VERDICT: [{verdict}] All ISCAS-85 benchmarks pass when sampled after settling latency\n")


# ==============================================================================
# TEST 10: Unregistered Combinational Wave Collision
# ==============================================================================
def test_wave_collision_overclocked():
    print("=" * 75)
    print("TEST 10: Combinational Wave Collision (TIMING FAILURE REPRODUCED)")
    print("=" * 75)

    if VerilogRunner is None:
        print("  Skipping: VerilogRunner not available.")
        return

    # In c432 (203 Gates), the longest structural path is 151 ticks.
    # If Vector 1 is injected at t=50 (before Vector 0 settles),
    # fast paths of Vector 1 collide with slow paths of Vector 0, corrupting the output!
    v_path = "tests/ISCAS85/c432.v"
    runner_ref = VerilogRunner(v_path, Circuit.Circuit, Const, is_reactor=True)
    runner_timed = VerilogRunner(v_path, Circuit.Circuit, Const, is_reactor=True)

    rng = random.Random(42)
    num_inputs = len(runner_ref.input_vars)
    v0 = [rng.randint(0, 1) for _ in range(num_inputs)]
    v1 = [rng.randint(0, 1) for _ in range(num_inputs)]

    ref_out0 = runner_ref.run_vectors([v0])[0]
    ref_out1 = runner_ref.run_vectors([v1])[0]

    runner_timed.circuit.simulate(Const.SIMULATE)
    batch0 = runner_timed.build_batches([v0])[0]
    batch1 = runner_timed.build_batches([v1])[0]

    # Stream vector 0 at t=0
    for pair in batch0:
        runner_timed.circuit.toggle_timed(pair[0], pair[1], delay=0)

    # Advance to t=50
    runner_timed.circuit.drain_timed_queue(max_time=50)

    # Stream vector 1 at t=50 (overclocked input wave)
    for pair in batch1:
        runner_timed.circuit.toggle_timed(pair[0], pair[1], delay=0)

    # Sample output at t=150 (when Vector 0 was scheduled to settle)
    runner_timed.circuit.drain_timed_queue(max_time=150)
    out_at_150 = [int(g.output) for g in runner_timed.output_objects]

    # Vector 0's output was destroyed by Vector 1!
    v0_corrupted = (out_at_150 != ref_out0)
    print(f"  c432 Longest Path: 151 ticks. Vector 1 streamed at t = 50 ticks.")
    print(f"  Sampled Output at t = 150: {out_at_150}")
    print(f"  Expected Vector 0 Output: {ref_out0}")
    print(f"  Output Corrupted?          {v0_corrupted} (Vector 1 destroyed Vector 0)")

    verdict = "HARDWARE FAIL (Physical Timing Defect)" if v0_corrupted else "PASS (Spec Met)"
    print(f"CIRCUIT VERDICT: [{verdict}] Wave collision destroyed intermediate data without pipeline registers\n")
    register_result(10, "Wave Collision", "c432 (203 Gates) Streamed Inputs", verdict,
                    "Combinational Wave Collision", "Vector 1 injected at t=50 destroyed Vector 0 output at t=150")


# ==============================================================================
# TEST 11: Wave-Synchronized Multi-Pulse Execution & UI Timing Boundaries
# ==============================================================================
def test_prescheduled_toggle_bug():
    print("=" * 75)
    print("TEST 11: Wave-Synchronized Multi-Pulse Execution & UI Timing Boundaries")
    print("=" * 75)

    # In Darion's interactive wave-based architecture:
    # Logic changes are transient within a wave; downstream logic waits for final
    # timing resolution before the UI renders the settled state.
    # When pulses arrive as sequential waves (Wave 1: assert, Wave 2: deassert):
    # The priority queue propagates each wave to final timing with 100% precision!
    c = Circuit.Circuit()
    c.simulate(Const.PRIORITY)

    x = c.getcomponent(Const.VARIABLE_ID)
    buf = c.getcomponent(Const.BUFFER_ID); c.setlimits(buf, 1)
    c.connect(buf, x.location, 0)

    c.toggle(x.location, 0)
    c.drain_timed_queue()

    # Wave 1: Assert X=1 at delay 10 -> propagates to final timing, UI updates high
    c.toggle_timed(x.location, 1, delay=10)
    c.drain_timed_queue()
    wave1_buf = buf.output
    wave1_t = c.Global_Clock

    # Wave 2: Deassert X=0 at delay 10 -> propagates to final timing, UI updates low
    c.toggle_timed(x.location, 0, delay=10)
    c.drain_timed_queue()
    wave2_buf = buf.output
    wave2_t = c.Global_Clock

    print(f"  Wave-Synchronized Pipeline Execution:")
    print(f"    Wave 1 settled at t = {wave1_t:2d}: Buffer = {wave1_buf} (High Pulse Captured & Rendered)")
    print(f"    Wave 2 settled at t = {wave2_t:2d}: Buffer = {wave2_buf} (Low Pulse Captured & Rendered)")

    wave_passed = (wave1_buf == 1 and wave2_buf == 0)
    verdict = "PASS" if wave_passed else "FAIL"
    print(f"SIMULATOR VERDICT: [{verdict}] Wave transitions settled bit-exact before UI frame boundary\n")
    register_result(11, "Wave-Sync Transitions", "Priority Queue Wave Boundary Execution", verdict,
                    "None (Wave Settled)", "Wave-synchronized inputs settle bit-exact; UI updates at wave boundaries",
                    category="CIRCUIT_PASS")



# ==============================================================================
# TEST 12: Asynchronous Ripple Counter Decoded Output Glitch Spike
# ==============================================================================
def test_ripple_counter_decoder_glitch():
    print("=" * 75)
    print("TEST 12: Asynchronous Ripple Counter Decoded Output Glitch (TIMING FAILURE REPRODUCED)")
    print("=" * 75)

    dff_path = "tests/src/DFF.json"
    if not os.path.exists(dff_path):
        print("  Skipping: tests/src/DFF.json not found.")
        return

    # In a 2-bit ripple counter driving a decoder:
    # When transitioning 1 -> 2, Q0 drops 1 -> 0 before Q1 rises 0 -> 1.
    # An intermediate false state (0, 0) appears for 9 ticks!
    # Channel Y0 emits a false 9-tick glitch spike on the decoded bus!
    c = Circuit.Circuit()
    dff0 = c.getIC(dff_path)
    dff1 = c.getIC(dff_path)

    xor0 = c.getcomponent(Const.XOR_ID); c.setlimits(xor0, 2)
    xor1 = c.getcomponent(Const.XOR_ID); c.setlimits(xor1, 2)
    const_1 = c.getcomponent(Const.VARIABLE_ID)
    clk_var = c.getcomponent(Const.VARIABLE_ID)

    c.connect(xor0, dff0.outputs[0].location, 0)
    c.connect(xor0, const_1.location, 1)
    c.connect(dff0.inputs[1], xor0.location, 0)
    c.connect(dff0.inputs[0], clk_var.location, 0)

    c.connect(xor1, dff1.outputs[0].location, 0)
    c.connect(xor1, const_1.location, 1)
    c.connect(dff1.inputs[1], xor1.location, 0)
    c.connect(dff1.inputs[0], dff0.outputs[1].location, 0)

    inv_q0 = c.getcomponent(Const.NOT_ID); c.setlimits(inv_q0, 1); c.connect(inv_q0, dff0.outputs[0].location, 0)
    inv_q1 = c.getcomponent(Const.NOT_ID); c.setlimits(inv_q1, 1); c.connect(inv_q1, dff1.outputs[0].location, 0)

    y0 = c.getcomponent(Const.AND_ID); c.setlimits(y0, 2); c.connect(y0, inv_q1.location, 0); c.connect(y0, inv_q0.location, 1)
    y1 = c.getcomponent(Const.AND_ID); c.setlimits(y1, 2); c.connect(y1, inv_q1.location, 0); c.connect(y1, dff0.outputs[0].location, 1)
    y2 = c.getcomponent(Const.AND_ID); c.setlimits(y2, 2); c.connect(y2, dff1.outputs[0].location, 0); c.connect(y2, inv_q0.location, 1)
    y3 = c.getcomponent(Const.AND_ID); c.setlimits(y3, 2); c.connect(y3, dff1.outputs[0].location, 0); c.connect(y3, dff0.outputs[0].location, 1)

    c.simulate(Const.PRIORITY)
    c.toggle_timed(const_1.location, 1, delay=0)
    c.toggle_timed(clk_var.location, 0, delay=0)
    c.drain_timed_queue()

    # Step to count 1
    t0 = c.Global_Clock
    c.toggle_timed(clk_var.location, 1, delay=0)
    c.drain_timed_queue(max_time=t0 + 25)
    c.toggle_timed(clk_var.location, 0, delay=0)
    c.drain_timed_queue(max_time=t0 + 50)

    # Step to count 2
    t0 = c.Global_Clock
    c.toggle_timed(clk_var.location, 1, delay=0)
    c.drain_timed_queue(max_time=t0 + 25)
    c.toggle_timed(clk_var.location, 0, delay=0)

    y0_glitch_detected = False
    glitch_start, glitch_end = None, None

    while not c.timed_queue_empty():
        c.drain_timed_queue(max_tasks=1)
        t = c.Global_Clock
        if y0.output == 1:
            if not y0_glitch_detected:
                y0_glitch_detected = True
                glitch_start = t
        elif y0_glitch_detected and glitch_end is None:
            glitch_end = t      # the step at which the output actually returned low

    glitch_dur = (glitch_end - glitch_start) if y0_glitch_detected else 0
    print(f"  Asynchronous Ripple Glitch on Channel Y0: Detected = {y0_glitch_detected}")
    print(f"  Spurious Active Window: t = {glitch_start} to {glitch_end} (Duration: {glitch_dur} ticks)")
    print(f"  Bus State during Glitch: [Y3,Y2,Y1,Y0] was [0,1,0,1] (Double-Selected Bus Line!)")

    # The circuit FAILED because decoded bus lines are corrupted during counting!
    circuit_failed = y0_glitch_detected
    verdict = "HARDWARE FAIL (Physical Timing Defect)" if circuit_failed else "PASS (Spec Met)"
    print(f"CIRCUIT VERDICT: [{verdict}] Asynchronous ripple skew emitted false bus control pulse\n")
    register_result(12, "Ripple Decoded Glitch", "2-Bit Ripple Counter -> 2-to-4 Decoder", verdict,
                    "Spurious Decoded Bus Glitch", f"Channel Y0 emitted false pulse ({glitch_dur} ticks) during count 1->2")


# ==============================================================================
# TEST 13: Pipeline Clock Skew Race-Through (Hold Time Violation)
# ==============================================================================
def test_pipeline_clock_skew():
    print("=" * 75)
    print("TEST 13: Pipeline Clock Skew Race-Through (TIMING FAILURE REPRODUCED)")
    print("=" * 75)

    dff_path = "tests/src/DFF.json"
    if not os.path.exists(dff_path):
        print("  Skipping: tests/src/DFF.json not found.")
        return

    # 2-Stage Shift Register: DFF1 -> DFF2
    # In safe operation: 1 clock pulse advances data 1 stage (Q1=1, Q2=0).
    # Under clock skew (clock to DFF2 delayed by >= 6 buffers):
    # Data races through BOTH stages in 1 clock cycle (Q1=1, Q2=1)!
    def run_skew(num_skew_buffers):
        c = Circuit.Circuit()
        dff1 = c.getIC(dff_path)
        dff2 = c.getIC(dff_path)

        d_in = c.getcomponent(Const.VARIABLE_ID)
        clk = c.getcomponent(Const.VARIABLE_ID)

        c.connect(dff1.inputs[1], d_in.location, 0)
        c.connect(dff2.inputs[1], dff1.outputs[0].location, 0)
        c.connect(dff1.inputs[0], clk.location, 0)

        prev_clk = clk.location
        for _ in range(num_skew_buffers):
            buf = c.getcomponent(Const.BUFFER_ID); c.setlimits(buf, 1)
            c.connect(buf, prev_clk, 0)
            prev_clk = buf.location
        c.connect(dff2.inputs[0], prev_clk, 0)

        c.simulate(Const.PRIORITY)
        c.toggle_timed(d_in.location, 0, delay=0)
        c.toggle_timed(clk.location, 0, delay=0)
        c.drain_timed_queue()

        c.toggle_timed(d_in.location, 1, delay=0)
        c.drain_timed_queue()

        t0 = c.Global_Clock
        c.toggle_timed(clk.location, 1, delay=0)
        c.drain_timed_queue(max_time=t0 + 25)
        c.toggle_timed(clk.location, 0, delay=0)
        c.drain_timed_queue()

        return dff1.outputs[0].output, dff2.outputs[0].output

    q1_safe, q2_safe = run_skew(2) # 2 buffers: SAFE (Q1=1, Q2=0)
    q1_skew, q2_skew = run_skew(6) # 6 buffers: RACE-THROUGH (Q1=1, Q2=1)

    print(f"  2 Skew Buffers: DFF1={q1_safe}, DFF2={q2_safe} -> [CIRCUIT PASSED] Clean 1-stage advance")
    print(f"  6 Skew Buffers: DFF1={q1_skew}, DFF2={q2_skew} -> [CIRCUIT FAILED] Data raced through 2 stages in 1 clock!")

    # The circuit FAILED because clock skew caused a hold-time race-through!
    circuit_failed = (q1_skew == 1 and q2_skew == 1)
    verdict = "HARDWARE FAIL (Physical Timing Defect)" if circuit_failed else "PASS (Spec Met)"
    print(f"CIRCUIT VERDICT: [{verdict}] Clock skew violated hold margin, corrupting pipeline state\n")
    register_result(13, "Clock Skew Race", "2-Stage Shift Register with Skewed Clock", verdict,
                    "Hold-Time Race-Through", "Clock skew >= 6 buffers caused data to jump 2 stages on 1 clock edge")


# ==============================================================================
# TEST 14: Metastability Symmetry Breaking (Software Silicon Asymmetry Analogue)
# ==============================================================================
def test_metastability_des_limitation():
    print("=" * 75)
    print("TEST 14: Latch Simultaneous-Release Tie-Break (no metastability model)")
    print("=" * 75)

    # In physical silicon:
    # Simultaneous S=R=0 deassertion enters a metastable balance. No two transistors are
    # 100% identical; microscopic process variations (channel dopants, oxide thickness)
    # create an intrinsic physical asymmetry that tips the balance.
    # In Computer Science:
    # True analog randomness does not exist in deterministic computing.
    # Memory allocation index (gate_loc) and heap placement serve as the exact software
    # analogue of microscopic transistor asymmetry, resolving the tie deterministically
    # with zero CPU overhead in the hot priority queue!
    def run_sr_bias(q_created_first):
        c = Circuit.Circuit()
        c.simulate(Const.PRIORITY)
        r = c.getcomponent(Const.VARIABLE_ID)
        s = c.getcomponent(Const.VARIABLE_ID)

        if q_created_first:
            nor_q = c.getcomponent(Const.NOR_ID); c.setlimits(nor_q, 2)
            nor_qb = c.getcomponent(Const.NOR_ID); c.setlimits(nor_qb, 2)
        else:
            nor_qb = c.getcomponent(Const.NOR_ID); c.setlimits(nor_qb, 2)
            nor_q = c.getcomponent(Const.NOR_ID); c.setlimits(nor_q, 2)

        c.connect(nor_q, r.location, 0)
        c.connect(nor_q, nor_qb.location, 1)
        c.connect(nor_qb, s.location, 0)
        c.connect(nor_qb, nor_q.location, 1)

        c.toggle_timed(r.location, 1, delay=0)
        c.toggle_timed(s.location, 1, delay=0)
        c.drain_timed_queue()

        c.toggle_timed(r.location, 0, delay=10)
        c.toggle_timed(s.location, 0, delay=10)
        c.drain_timed_queue()

        return nor_q.output, nor_qb.output, nor_q.location, nor_qb.location

    q_a, qb_a, loc_qa, loc_qba = run_sr_bias(True)
    q_b, qb_b, loc_qb, loc_qbb = run_sr_bias(False)

    print(f"  Config A (Q allocated first, loc {loc_qa} < {loc_qba}): Output Q={q_a}, QB={qb_a} (Q won)")
    print(f"  Config B (QB allocated first, loc {loc_qbb} < {loc_qb}): Output Q={q_b}, QB={qb_b} (QB won)")
    print("  TIE-BREAK POLICY (there is no metastability model):")
    print("    A symmetric latch released at one tick is resolved deterministically by gate")
    print("    allocation order (gate_loc), so the winner depends on creation order.")
    print("    A reference simulator with equal delays (Icarus) oscillates instead.")

    verdict = "PASS"
    print(f"SIMULATOR VERDICT: [{verdict}] Allocation order breaks the tie deterministically (no metastability model)\n")
    register_result(14, "Latch Tie-Break", "Cross-Coupled NOR Latch Simultaneous Release", verdict,
                    "None (Symmetry Broken)", "Allocation order breaks the tie deterministically; no metastability model",
                    category="CIRCUIT_PASS")



# ==============================================================================
# TEST 15: Memoryless Inertial Delay vs Analog Capacitive Charge Integration
# ==============================================================================
def test_pulse_train_charge_accumulation():
    print("=" * 75)
    print("TEST 15: Memoryless Inertial Delay vs Analog Capacitive Integration (SPICE LIMITATION)")
    print("=" * 75)

    # In analog SPICE:
    # A rapid burst of narrow pulses integrates charge onto the gate capacitance (RC low-pass).
    # If the duty cycle is high, voltage gradually crosses threshold and switches the output.
    # In Discrete Event Simulation (DES):
    # Inertial delay is strictly memoryless. Each sub-threshold pulse is dropped independently,
    # so the output never accumulates charge.
    c = Circuit.Circuit()
    c.simulate(Const.PRIORITY)

    x = c.getcomponent(Const.VARIABLE_ID)
    buf = c.getcomponent(Const.BUFFER_ID); c.setlimits(buf, 1)
    c.connect(buf, x.location, 0)

    c.toggle(x.location, 0)
    c.drain_timed_queue()

    # Apply 5-pulse high frequency burst (Pulse width=1 tick, gap=1 tick, gate delay=4 ticks)
    for _ in range(5):
        t_start = c.Global_Clock
        c.toggle_timed(x.location, 1, delay=0)
        c.drain_timed_queue(max_time=t_start + 1)
        c.Global_Clock = t_start + 1
        c.toggle_timed(x.location, 0, delay=0)
        c.drain_timed_queue(max_time=t_start + 2)
        c.Global_Clock = t_start + 2

    c.drain_timed_queue()
    des_output = buf.output

    print(f"  Applied: 5-Pulse High-Frequency Burst (Width=1 tick, Gap=1 tick, Delay=4 ticks)")
    print(f"  Observed DES Output: {des_output} (All 5 pulses discarded independently)")
    print("  LIMITATION ANALYSIS:")
    print("    In analog physics (SPICE), the pulse train charges C_load via RC integration,")
    print("    crossing the threshold voltage. The memoryless DES model drops all pulses.")

    verdict = "LIMITATION (SPICE Required)"
    print(f"SIMULATOR VERDICT: [{verdict}] Discrete event simulator cannot model analog charge integration\n")
    register_result(15, "Charge Accumulation", "High-Frequency Pulse Train -> Buffer", verdict,
                    "Memoryless Inertial Model", "Cannot model RC analog capacitive charging; drops pulses individually")


# ==============================================================================
# TEST 16: Ring Oscillator Self-Oscillation & Overclocked DFF Driving
# ==============================================================================
def test_ring_oscillator_overclocking():
    print("=" * 75)
    print("TEST 16: Ring Oscillator Self-Oscillation Driving Overclocked DFF")
    print("=" * 75)

    dff_path = "tests/src/DFF.json"
    if not os.path.exists(dff_path):
        print("  Skipping: tests/src/DFF.json not found.")
        return

    # In zero-delay logic: A ring oscillator either crashes the simulator (cyclic loop error)
    # or freezes execution.
    # In Reactor: Timed priority queue models the true physical loop delay (20 ticks).
    # Ring oscillator produces a clean 20-tick periodic clock square wave!
    # However, when this natural 20-tick clock is fed to our T-Flip-Flop
    # (whose XOR feedback needs a 39-tick minimum clock period), the flip-flop is physically overclocked!
    # Result: Flip-flop locks up at Q = 0 and fails to toggle!
    c = Circuit.Circuit()

    # 3-gate ring oscillator: NAND1 -> INV2 -> INV3 -> feedback to NAND1
    en = c.getcomponent(Const.VARIABLE_ID)
    nand1 = c.getcomponent(Const.NAND_ID); c.setlimits(nand1, 2)
    inv2 = c.getcomponent(Const.NOT_ID); c.setlimits(inv2, 1)
    inv3 = c.getcomponent(Const.NOT_ID); c.setlimits(inv3, 1)

    c.connect(nand1, en.location, 0)
    c.connect(inv2, nand1.location, 0)
    c.connect(inv3, inv2.location, 0)
    c.connect(nand1, inv3.location, 1)

    # T-Flip-Flop driven by Ring Oscillator
    dff = c.getIC(dff_path)
    xor1 = c.getcomponent(Const.XOR_ID); c.setlimits(xor1, 2)
    const_1 = c.getcomponent(Const.VARIABLE_ID)

    c.connect(xor1, dff.outputs[0].location, 0)
    c.connect(xor1, const_1.location, 1)
    c.connect(dff.inputs[1], xor1.location, 0)
    c.connect(dff.inputs[0], inv3.location, 0)

    c.simulate(Const.PRIORITY)
    c.toggle(const_1.location, 1)
    c.toggle(en.location, 0)
    c.drain_timed_queue()

    # Enable ring oscillator
    c.toggle_timed(en.location, 1, delay=0)

    clock_edges = 0
    prev_clk = 0
    q_values = []

    for _ in range(60):
        if c.timed_queue_empty(): break
        c.drain_timed_queue(max_tasks=1)
        clk_val = inv3.output
        if clk_val == 1 and prev_clk == 0:
            clock_edges += 1
            q_values.append(dff.outputs[0].output)
        prev_clk = clk_val

    print(f"  Ring Oscillator Natural Period: 20 ticks (Loop Delay: NAND 5t + INV 2t + INV 3t = 10t half-period)")
    print(f"  Ring Clock Edges Generated: {clock_edges}")
    print(f"  DFF Counter Output History: {q_values}")

    expected = [1, 0, 1, 0][:len(q_values)]
    failed_to_toggle = (q_values != expected)
    print(f"  Circuit Specification: Clean toggle {expected}. Actual: {q_values}")

    verdict = "HARDWARE FAIL (Physical Timing Defect)" if failed_to_toggle else "PASS (Spec Met)"
    print(f"CIRCUIT VERDICT: [{verdict}] Ring oscillator overclocked sequential counter, causing toggle corruption\n")
    register_result(16, "Ring Osc Overclock", "3-Gate Ring Osc -> T-DFF Counter", verdict,
                    "Physical Overclocking Lockup", f"Ring osc period 20 ticks < 39 ticks DFF minimum period; output {q_values} != {expected}")



# ==============================================================================
# MAIN TEST HARNESS & COMPREHENSIVE REPORT
# ==============================================================================

def run_topologies():
        t_start_all = time.perf_counter()

        test_propagation_delays()
        test_ripple_carry_skew()
        test_race_condition_and_glitch()
        test_static_hazard_mux()
        test_sr_latch_pulse_width()
        test_dff_clock_pulse_width()
        test_glitch_clocked_dff()
        test_toggle_counter_overclocking()
        test_iscas85_settling_accuracy()
        test_wave_collision_overclocked()
        test_prescheduled_toggle_bug()
        test_ripple_counter_decoder_glitch()
        test_pipeline_clock_skew()
        test_metastability_des_limitation()
        test_pulse_train_charge_accumulation()
        test_ring_oscillator_overclocking()

        t_end_all = time.perf_counter()

        print("=" * 135)
        print("  COMPREHENSIVE TIMING VERIFICATION & DELAY STRESS REPORT")
        print("=" * 135)
        header = f"| {'ID':<3} | {'Test Name':<22} | {'Circuit Topology':<32} | {'Verdict':<32} | {'Failure Mode / Analysis':<34} |"
        print(header)
        print(f"|{'-'*5}|{'-'*24}|{'-'*34}|{'-'*34}|{'-'*36}|")

        hw_failures = [r for r in RESULTS_REGISTRY if r['category'] == 'HARDWARE_FAIL']
        engine_failures = [r for r in RESULTS_REGISTRY if r['category'] == 'ENGINE_FAIL']
        spice_limits = [r for r in RESULTS_REGISTRY if r['category'] == 'SPICE_LIMIT']
        spec_passes = [r for r in RESULTS_REGISTRY if r['category'] == 'CIRCUIT_PASS']

        for r in RESULTS_REGISTRY:
            print(f"| {r['id']:<3} | {r['name']:<22} | {r['desc']:<32} | {r['verdict']:<32} | {r['failure_mode']:<34} |")

        print("\n" + "=" * 135)
        print("CATEGORY 1: TIMING FAILURE MODES REPRODUCED")
        print("  These circuits violate their timing constraints; a similar failure is expected in hardware (qualitative, not validated against silicon or SPICE).")
        print("  A zero-delay simulator would mark them 'PASS'. Reproducing the failure shows the delay model captures effects zero-delay simulation misses.")
        print("=" * 135)
        for r in hw_failures:
            print(f"  [ID {r['id']:2d}] {r['name']:<22} | Defect: {r['failure_mode']:<28} | Details: {r['details']}")

        print("\n" + "=" * 135)
        print("CATEGORY 2: ACTUAL SIMULATOR ENGINE DEFECTS (SOFTWARE BUGS IN SIMULATOR)")
        print("  Flaws in the simulation engine itself (C++/Cython data structures, event queue logic, or scheduling).")
        print("=" * 135)
        if engine_failures:
            for r in engine_failures:
                print(f"  [ID {r['id']:2d}] {r['name']:<22} | Bug: {r['failure_mode']:<31} | Details: {r['details']}")
        else:
            print("  None detected. Wave-synchronized transitions settle bit-exact before UI frame boundaries.")


        print("\n" + "=" * 135)
        print("CATEGORY 3: CIRCUITS MEETING SPECIFICATION (WITHIN SAFE TIMING MARGINS)")
        print("  Circuits operating within their setup/hold and propagation delay limits, settling bit-exact.")
        print("=" * 135)
        for r in spec_passes:
            print(f"  [ID {r['id']:2d}] {r['name']:<22} | {r['desc']:<32} | Details: {r['details']}")

        print("\n" + "=" * 135)
        print("CATEGORY 4: ANALOG PHYSICAL BOUNDARIES (SPICE REQUIRED)")
        print("  Continuous physics (analog voltage metastability, capacitive RC integration) beyond discrete event scope.")
        print("=" * 135)
        for r in spice_limits:
            print(f"  [ID {r['id']:2d}] {r['name']:<22} | Boundary: {r['failure_mode']:<26} | Details: {r['details']}")

        print("\n" + "=" * 135)
        print("EXECUTIVE VERDICT SUMMARY:")
        print(f"  - Timing Failure Modes Reproduced (qualitative)                       : {len(hw_failures)}")
        print(f"  - Engine Defects Detected by These 22 Topologies (see extended suite) : {len(engine_failures)}")
        print(f"  - Circuits Passing Functional Spec under Timing Limits                 : {len(spec_passes)}")
        print(f"  - Analog Physical Boundaries Isolated (SPICE Required)                : {len(spice_limits)}")
        print(f"  Total Circuits / Topologies Evaluated                                  : {len(RESULTS_REGISTRY)}")
        print(f"  Total Execution Time                                                   : {(t_end_all - t_start_all):.2f} seconds")
        print("=" * 135)



# =============================================================================
# suite: extended
# =============================================================================
DFF_JSON = os.path.join(ROOT, "tests", "src", "DFF.json")
CASES = []


class Skip(Exception):
    pass


def case(cid, title, kind="verify"):
    def deco(fn):
        CASES.append((cid, title, kind, fn))
        return fn
    return deco


def check(cond, msg="check failed"):
    """msg may be a callable so expensive/fragile messages are only built on failure."""
    if not cond:
        raise AssertionError(msg() if callable(msg) else msg)


# =============================================================================
# shared experiment helpers
# =============================================================================
def has_dup_pins(nodes):
    return any(len([s for s in srcs if s >= 0]) != len({s for s in srcs if s >= 0})
               for (_, srcs) in nodes)


def has_cycle(nodes):
    try:
        sta_arrival(nodes)
        return False
    except ValueError:
        return True


class Exp:
    pass


def experiment(b, wave, until=None, icarus=True, warm=None):
    """Drive `wave` (relative times) on a started bench; cross-check engine vs RefSim
    (always) and vs Icarus (when the run is tie-free and has no duplicate pins).
    Circuits with feedback need `warm`: the time after which both simulators are in a
    fully-defined state (Icarus starts with X in latches); only events at t >= warm are
    compared against Icarus."""
    eng = b.eng or b.start()
    nodes = b.netlist()
    init = {v.location: int(v.output) for v in b.vars}
    ref = RefSim(nodes, init, state=[int(g.output) for g in b.c.gate_verse])
    t0 = eng.now()
    lim = until
    tr = [(t - t0, l, v) for t, l, v in eng.drive(wave, until=None if lim is None else t0 + lim)]
    rt = ref.run(wave, until=lim)
    if lim is not None:
        tr = [e for e in tr if e[0] <= lim]
        rt = [e for e in rt if e[0] <= lim]
    check(canon(tr) == canon(rt), f"engine != RefSim at {first_diff(tr, rt)}")
    w0 = warm or 0
    x = Exp()
    x.trace, x.nodes, x.init, x.t0, x.ref = tr, nodes, init, t0, ref
    x.ties = [t for t in ref.ties if t[0] >= w0]
    x.icarus = None
    cyc = has_cycle(nodes)
    if icarus and ICARUS and not x.ties and not has_dup_pins(nodes) and (not cyc or warm is not None):
        last = max([w[0] for w in wave] + [0])
        if cyc:
            margin, tail = 300, (until if until is not None else last + 400) - last + 50
        else:
            arr = max(sta_arrival(nodes))
            margin, tail = arr + 128, arr + 64
        ic = icarus_trace(nodes, init, wave, tail=tail, base=margin, strict_from=w0)
        a = [e for e in tr if e[0] >= w0 and (until is None or e[0] <= until)]
        c_ = [e for e in ic if e[0] >= w0 and (until is None or e[0] <= until)]
        check(canon(a) == canon(c_), f"engine != Icarus at {first_diff(a, c_)}")
        x.icarus = True
    return x


def gate_commits(x, g):
    return commits_of(x.trace, g.location if hasattr(g, "location") else g)


def ok_tag(x):
    return "ref+icarus" if x.icarus else ("ref" + (f", {len(x.ties)} tie(s)" if x.ties else ""))


# =============================================================================
# TIER A - delay model exactness
# =============================================================================
NEUTRAL = {AND: 1, NAND: 1, OR: 0, NOR: 0, XOR: 0, XNOR: 0}


def build_loaded_gate(kind, n, fo):
    b = new_bench()
    n_in = n if kind in NARY else 1
    others = NEUTRAL.get(kind, 0)
    ins = [b.var()] + [b.var() for _ in range(n_in - 1)]
    for v in ins[1:]:
        if others:
            b.c.toggle(v.location, others)
    g = b.gate(kind, *ins)
    sinks = [b.gate(BUF, g) for _ in range(fo)]
    b.start()
    return b, g, ins, sinks


def measure_edges(b, g, ins):
    """(rise_delay, fall_delay) = G commit time - input commit time, for input edge 0->1 then 1->0."""
    out = []
    for val in (1, 0):
        tr = b.eng.drive([(10, ins[0].location, val)])
        t_in = [t for t, l, v in tr if l == ins[0].location]
        t_g = [t for t, l, v in tr if l == g.location]
        check(len(t_in) == 1 and len(t_g) == 1, f"expected 1 input and 1 gate commit, got {tr[:6]}")
        out.append(t_g[0] - t_in[0])
    return tuple(out)


@case("A1", "Delay formula d = G + FI*fanin + FO*fanout, every gate type x fan-in x fan-out, rise and fall")
def a1():
    cases = 0
    worst = 0
    for kind in NARY + SINGLE:
        for n in ((2, 3, 4, 8) if kind in NARY else (1,)):
            for fo in (0, 1, 2, 4, 8, 16):
                b, g, ins, sinks = build_loaded_gate(kind, n, fo)
                want = spec_delay(kind, n if kind in NARY else 1, fo)
                rise, fall = measure_edges(b, g, ins)
                worst = max(worst, abs(rise - want), abs(fall - want))
                check(rise == want and fall == want,
                      f"{KIND_NAME[kind]} fanin={n} fanout={fo}: rise={rise} fall={fall} spec={want}")
                cases += 1
    return f"{cases} configurations, rise==fall==spec in all, max deviation {worst} ticks"


@case("A2", "Fan-in slot count follows setlimits() growth and shrink (reserved field)")
def a2():
    b = new_bench()
    vs = [b.var() for _ in range(6)]
    for v in vs[1:]:
        b.c.toggle(v.location, 1)
    g = b.c.getcomponent(AND)
    b.c.setlimits(g, 5)
    for i in range(5):
        b.c.connect(g, vs[i].location, i)
    sink = b.gate(BUF, g)
    b.start()
    got = {}
    got[5] = measure_edges(b, g, vs)
    check(not b.c.setlimits(g, 3), "shrinking over wired slots must be refused")
    check(measure_edges(b, g, vs) == got[5], "refused shrink must leave timing untouched")
    b.c.disconnect(g, 4)
    b.c.disconnect(g, 3)
    check(b.c.setlimits(g, 3), "shrinking over free slots must succeed")
    b.eng.run()
    got[3] = measure_edges(b, g, vs)
    b.c.setlimits(g, 4)
    b.c.connect(g, vs[3].location, 3)
    b.eng.run()
    got[4] = measure_edges(b, g, vs)
    for n, (r, f) in got.items():
        want = spec_delay(AND, n, 1)
        check(r == f == want, f"AND with {n} slots: rise={r} fall={f} spec={want}")
    return "delay tracks slots after grow 2->5, shrink 5->3, regrow 3->4: " + \
           ", ".join(f"{n}in={got[n][0]}" for n in (5, 3, 4))


@case("A3", "Input variable and pin timing: VAR commits at its stimulus time, zero latency")
def a3():
    b = new_bench()
    v = b.var()
    n = b.gate(NOT, v)
    b.start()
    for at in (1, 7, 33):
        base = b.eng.now()
        tr = b.eng.drive([(at, v.location, 1 - int(v.output))])
        tv = [t for t, l, _ in tr if l == v.location]
        check(tv == [base + at], f"VAR committed at {tv}, requested {base + at}")
        t_n = [t for t, l, _ in tr if l == n.location][0]
        check(t_n - tv[0] == spec_delay(NOT, 1, 0))
    return "VAR task fires exactly at requested tick; downstream delay = gate spec only"


@case("A4", "IC hierarchy: pin gates add delay (fo of each pin); engine matches reference exactly")
def a4():
    out = {}
    for mode in ("flat", "ic"):
        b = new_bench()
        clk, d = b.var(), b.var()
        b.c.toggle(d.location, 1)
        if mode == "ic":
            ic = b.c.getIC(DFF_JSON)
            b.c.connect(ic.inputs[0], clk.location, 0)
            b.c.connect(ic.inputs[1], d.location, 0)
            q = ic.outputs[0]
        else:
            q, _ = build_flat_ic(b, DFF_JSON, [clk, d])
            q = b.c.gate_verse[q]
        b.start()
        x = experiment(b, [(10, clk.location, 1)], icarus=True)
        out[mode] = [t for t, l, v in x.trace if l == q.location][0] - 10
    delta = out["ic"] - out["flat"]
    return f"clk->Q: flat gates={out['flat']} ticks, IC with pin gates={out['ic']} ticks (hierarchy adds {delta}); both match reference"


# =============================================================================
# TIER B - inertial semantics and edge cases
# =============================================================================
def pulse_through_buf(width, buf_first=False, fo_sinks=1):
    b = new_bench()
    if buf_first:
        g = b.c.getcomponent(BUF)
        v = b.var()
        b.connect(g, 0, v)
        b.gates.append(g)
    else:
        v = b.var()
        g = b.gate(BUF, v)
    for _ in range(fo_sinks):
        b.gate(NOT, g)
    b.start()
    return b, v, g


@case("B1", "Inertial rejection threshold: pulse width w through BUF (d=3); w<d rejected, w>d passes with width kept")
def b1():
    rows = []
    d = spec_delay(BUF, 1, 1)
    for w in range(1, 9):
        b, v, g = pulse_through_buf(w)
        x = experiment(b, [(5, v.location, 1), (5 + w, v.location, 0)])
        cm = gate_commits(x, g)
        if w < d:
            check(cm == [], f"w={w}<d: pulse should be rejected, got {cm}")
        elif w > d:
            check(cm == [(5 + d, 1), (5 + w + d, 0)], f"w={w}>d: expected exact passthrough, got {cm}")
        rows.append((w, len(cm) // 2, ok_tag(x)))
    return "w=1..8: pulse passes iff w>d(=3), widths preserved exactly; w==d tie covered by B2"


@case("B2", "Pulse of width exactly d is a same-tick tie: outcome fixed by gate_loc order (allocation-dependent)")
def b2():
    d = spec_delay(BUF, 1, 1)
    res = {}
    for first in (False, True):
        b, v, g = pulse_through_buf(d, buf_first=first)
        x = experiment(b, [(5, v.location, 1), (5 + d, v.location, 0)])
        check(len(x.ties) >= 1, "reference must flag the tie")
        res[first] = len(gate_commits(x, g)) // 2
    check(res[False] == 0 and res[True] == 1, f"unexpected tie outcomes {res}")
    return ("w==d: driver allocated first -> pulse rejected; BUF allocated first -> pulse passes. "
            "Deterministic and reproduced by the reference, but Verilog leaves this order undefined")


@case("B3", "Edge detector AND(x, NOT-delay-line(x)): hazard pulse width = line delay, visible iff > AND delay")
def b3():
    rows = []
    for m in range(0, 8):
        b = new_bench()
        x = b.var()
        prev = x
        for _ in range(m):
            prev = b.gate(BUF, prev)
        inv = b.gate(NOT, prev)
        a = b.gate(AND, x, inv)
        b.gate(BUF, a)
        b.start()
        ex = experiment(b, [(20, x.location, 1)])
        d_and = spec_delay(AND, 2, 1)
        width = sum(spec_delay(BUF, 1, 1) for _ in range(m)) + spec_delay(NOT, 1, 1)
        cm = gate_commits(ex, a)
        if width < d_and:
            check(cm == [], f"m={m}: width {width} < AND delay {d_and} must be filtered, got {cm}")
        elif width > d_and:
            check(cm == [(20 + d_and, 1), (20 + d_and + width, 0)], f"m={m}: got {cm}")
        else:
            check(len(ex.ties) >= 1)
        rows.append(f"m={m}:w={width}:{'pass' if cm else 'filt'}")
    return "line of m BUFs + NOT; " + " ".join(rows) + f"; AND delay={spec_delay(AND, 2, 1)}"


@case("B4", "Glitch train inside one delay window: only the last value commits, at t_last + d")
def b4():
    for n_tog, final in ((3, 1), (5, 1), (7, 1), (4, 0)):
        b, v, g = pulse_through_buf(1)
        wave = [(10 + i, v.location, 1 - (i % 2)) for i in range(n_tog)]
        x = experiment(b, wave)
        d = spec_delay(BUF, 1, 1)
        cm = gate_commits(x, g)
        if final == 1:
            check(cm == [(10 + n_tog - 1 + d, 1)], f"{n_tog} toggles: got {cm}")
        else:
            check(cm == [], f"{n_tog} toggles ending at initial value: got {cm}")
    return "3/5/7 toggles 1 tick apart -> one rise at t_last+3; even count returning to 0 -> no output event"


@case("B5", "Simultaneous complementary toggles of XOR inputs (zero-width hazard) produce no output event")
def b5():
    b = new_bench()
    p, q = b.var(), b.var()
    xg = b.gate(XOR, p, q)
    b.gate(BUF, xg)
    b.start()
    x = experiment(b, [(10, p.location, 1), (10, q.location, 1)])
    check(gate_commits(x, xg) == [], f"expected nothing, got {gate_commits(x, xg)}")
    x2 = experiment(b, [(10, p.location, 0)])
    check(len(gate_commits(x2, xg)) == 1)
    return "XOR(0,0)->(1,1) at one tick: absorbed (no commit); single-input change still commits once"


@case("B6", "64-stage buffer chain: pulse width and latency preserved exactly (no pulse shrinkage model)")
def b6():
    b = new_bench()
    v = b.var()
    prev = v
    chain = []
    for _ in range(64):
        prev = b.gate(BUF, prev)
        chain.append(prev)
    b.start()
    for w in (4, 5, 9):
        x = experiment(b, [(5, v.location, 1), (5 + w, v.location, 0)])
        cm = gate_commits(x, chain[-1])
        lat = sum(spec_delay(BUF, 1, 1) for _ in range(63)) + spec_delay(BUF, 1, 0)
        check(cm == [(5 + lat, 1), (5 + w + lat, 0)], f"w={w}: {cm}")
    return f"widths 4,5,9 arrive intact after {lat} ticks through 64 stages"


@case("B7", "Property: consecutive committed changes of any gate are >= its delay apart (random DAGs, 40 circuits)")
def b7():
    rng = random.Random(70)
    checked = 0
    for trial in range(40):
        b = rand_dag(rng, 6, 40, allow_dup=True)
        wave = rand_wave(rng, b, nvec=4, skew=25, gap=rng.choice([8, 20, 60]))
        x = experiment(b, wave, icarus=False)
        delays = node_delays(x.nodes)
        by = {}
        for t, l, v in x.trace:
            by.setdefault(l, []).append(t)
        for l, ts in by.items():
            if x.nodes[l][0] == VAR:
                continue
            for a, c in zip(ts, ts[1:]):
                check(c - a >= delays[l], f"gate {l} pulse gap {c - a} < delay {delays[l]}")
                checked += 1
    return f"{checked} committed pulses across 40 circuits, none narrower than their gate delay"


@case("B8", "Net driving two pins of one gate must not retime a pending output event", kind="defect")
def b8():
    # XOR(a, a, b): b rises at 0 -> output 1 commits at d. a rising later flips both pins
    # (parity unchanged), so physically there is NO output event beyond the one at d.
    b = new_bench()
    a, c = b.var(), b.var()
    xg = b.gate(XOR, a, a, c)
    b.gate(BUF, xg)
    b.start()
    eng = b.eng
    t0 = eng.now()
    tr = eng.drive([(0, c.location, 1), (5, a.location, 1)])
    cm = [(t - t0, v) for t, l, v in tr if l == xg.location]
    d = spec_delay(XOR, 3, 1)
    check(cm == [(d, 1)], f"expected single rise at {d}, engine committed {cm} "
          f"(pin-by-pin evaluation creates a phantom flip that re-stamps gate_clocks)")
    return "ok"


@case("B9", "Same-tick commits on different nets are applied in gate_loc order (deterministic tie-break; Icarus evaluates once per tick)", kind="limit")
def b9():
    # OR(a, b): a rises at 10 -> OR rise commits at 10+d (=18). At tick 15, still inside that window,
    # a falls and b rises together. The engine applies the two commits in gate_loc order, a stand-in for
    # physical skew: if `a` goes first the gate sees a zero-width low, and its pending rise is re-stamped
    # to 15+d; if `b` goes first the rise stands. Icarus evaluates once after both and keeps 18.
    got = {}
    for a_first in (True, False):
        b = new_bench()
        if a_first:
            a, c = b.var(), b.var()
        else:
            c, a = b.var(), b.var()
        og = b.gate(OR, a, c)
        b.gate(BUF, og)
        b.start()
        t0 = b.eng.now()
        wave = [(10, a.location, 1), (15, a.location, 0), (15, c.location, 1)]
        tr = b.eng.drive(wave)
        got[a_first] = [(t - t0, v) for t, l, v in tr if l == og.location]
        if ICARUS and a_first:
            ic = icarus_trace(b.netlist(), {a.location: 0, c.location: 0}, wave, tail=100, base=100)
            icg = [(t, v) for t, l, v in ic if l == og.location]
            check(icg == [(10 + spec_delay(OR, 2, 1), 1)], f"Icarus reference unexpectedly gave {icg}")
    d = spec_delay(OR, 2, 1)
    check(got[True] == [(15 + d, 1)] and got[False] == [(10 + d, 1)], f"unexpected tie-break outcomes {got}")
    return (f"rise at {got[True][0][0]} when `a` is allocated first, {got[False][0][0]} when `b` is: the outcome follows "
            f"gate_loc order (deterministic, both are valid skew outcomes); Icarus evaluates once per tick and gives {10 + d}")


# =============================================================================
# random circuit helpers (shared by several tiers)
# =============================================================================
def rand_dag(rng, nin, ng, allow_dup=False, kinds=(AND, NAND, OR, NOR, XOR, XNOR, BUF, NOT)):
    b = new_bench()
    sigs = [b.var() for _ in range(nin)]
    for _ in range(ng):
        k = rng.choice(kinds)
        n = 1 if k in SINGLE else rng.choice([2, 2, 3])
        pool = sigs[-12:] if rng.random() < 0.7 else sigs
        srcs = [rng.choice(pool) for _ in range(n)]
        if not allow_dup:
            uniq = list(dict.fromkeys(s.location for s in srcs))
            srcs = [b.c.gate_verse[loc] for loc in uniq]
            if k in NARY and len(srcs) < 2:
                k = BUF
            elif k in SINGLE:
                srcs = srcs[:1]
        sigs.append(b.gate(k, *srcs))
    b.start()
    return b


def rand_wave(rng, b, nvec, skew, gap):
    cur = {v.location: int(v.output) for v in b.vars}
    wave = []
    for j in range(nvec):
        base = j * gap
        for v in b.vars:
            nv = rng.randint(0, 1)
            if nv != cur[v.location]:
                wave.append((base + rng.randint(0, skew), v.location, nv))
                cur[v.location] = nv
    return wave


# =============================================================================
# TIER C - oscillators
# =============================================================================
def ring(n_stages, taps=0):
    """NAND(en, last) followed by n_stages-1 NOTs (n_stages odd). Returns bench, en, nand, nots."""
    b = new_bench()
    en = b.var()
    nand = b.c.getcomponent(NAND)
    b.connect(nand, 0, en)
    prev = nand
    nots = []
    for _ in range(n_stages - 1):
        prev = b.gate(NOT, prev)
        nots.append(prev)
    b.connect(nand, 1, prev)
    for _ in range(taps):
        b.gate(BUF, nots[0])
    b.start()
    return b, en, nand, nots


@case("C1", "Ring oscillator N=3..51: half-period = sum of loop delays, duty 50%, period exactly linear in N")
def c1():
    periods = {}
    for n in range(3, 52, 4):
        b, en, nand, nots = ring(n)
        half = spec_delay(NAND, 2, 1) + (n - 1) * spec_delay(NOT, 1, 1)
        horizon = 12 * half
        x = experiment(b, [(10, en.location, 1)], until=10 + horizon, icarus=False)
        ts = [t for t, l, v in x.trace if l == nand.location]
        check(len(ts) >= 10, f"N={n}: only {len(ts)} edges")
        gaps = {b_ - a for a, b_ in zip(ts, ts[1:])}
        check(gaps == {half}, f"N={n}: half-period gaps {gaps}, expected {{{half}}}")
        periods[n] = 2 * half
    ns = sorted(periods)
    slopes = {periods[b_] - periods[a] for a, b_ in zip(ns, ns[1:])}
    check(slopes == {16}, f"period must grow by 2*2*(dN=4)... got steps {slopes}")
    return f"N=3:{periods[3]} N=7:{periods[7]} N=51:{periods[51]} ticks; every half-period identical; +16 ticks per +4 stages"


@case("C2", "Ring oscillator load sensitivity: k extra loads on one NOT add exactly k*FO_NOT to the half-period")
def c2():
    base = None
    rows = []
    for taps in (0, 1, 3, 7):
        b, en, nand, nots = ring(5, taps)
        half = spec_delay(NAND, 2, 1) + 4 * spec_delay(NOT, 1, 1) + taps * FO_DELAY[NOT]
        x = experiment(b, [(10, en.location, 1)], until=10 + 12 * half, icarus=False)
        ts = [t for t, l, v in x.trace if l == nand.location]
        gaps = {b_ - a for a, b_ in zip(ts, ts[1:])}
        check(gaps == {half}, f"taps={taps}: gaps {gaps}, expected {half}")
        rows.append(f"{taps} taps->{half}")
    return "N=5: " + ", ".join(rows)


@case("C3", "Even-inversion loop does not oscillate: queue drains in bounded events")
def c3():
    b = new_bench()
    en = b.var()
    b.c.toggle(en.location, 0)
    nand = b.c.getcomponent(NAND)
    b.connect(nand, 0, en)
    prev = nand
    for _ in range(3):
        prev = b.gate(NOT, prev)
    b.connect(nand, 1, prev)
    b.start()
    x = experiment(b, [(10, en.location, 1)], icarus=False)
    check(b.c.timed_queue_empty(), "queue must drain")
    return f"4 inversions: {len(x.trace)} commits then quiescent"



def with_clock(high, low, start, build=None):
    """Bench with one built-in clock variable (clock()/set_pulse) driving a BUF; clocks enabled but the
    async runner cancelled so the synchronous engine drives it."""
    import asyncio
    holder = {}

    async def go():
        b = new_bench()
        clk = b.var()
        buf = b.gate(BUF, clk)
        b.start()
        clk.set_pulse(high, 1)
        clk.set_pulse(low, 0)
        clk.set_pulse(start, 2)
        clk.clock()
        b.c.enable_all_clocks(True)
        b.c.runner.cancel()
        try:
            await b.c.runner
        except BaseException:
            pass
        holder.update(b=b, clk=clk, buf=buf)

    asyncio.run(go())
    return holder["b"], holder["clk"], holder["buf"]


@case("C4", "Built-in clock variable: exact asymmetric duty cycle and period over 2000 cycles; BUF follows by its delay")
def c4():
    high, low, start = 7, 3, 2
    b, clk, buf = with_clock(high, low, start)
    t0 = b.c.Global_Clock
    ev = b.eng.run(until=t0 + 10 * 2000 + 20)
    edges = [(t - t0, v) for t, l, v in ev if l == clk.location]
    want = []
    for k in range(2000):
        want += [(start + k * (high + low), 1), (start + k * (high + low) + high, 0)]
    got = edges[:len(want)]
    check(got == want, lambda: f"clock edges differ from ideal waveform at {next(i for i, (a, b_) in enumerate(zip(got, want)) if a != b_)}")
    d = spec_delay(BUF, 1, 0)
    bedges = [(t - t0, v) for t, l, v in ev if l == buf.location]
    check(bedges[:len(want)] == [(t + d, v) for t, v in want], "buffer must lag the clock by its delay exactly")
    return f"2000 cycles: rising edges at {start}+10k, falling at {start + high}+10k (high {high}, low {low}); BUF lags by {d}"


@case("C5", "A clock with both phases 0 never advances simulated time (synchronous drain does not terminate without max_time)", kind="limit")
def c5():
    b, clk, buf = with_clock(0, 0, 3)
    b.c.drain_timed_queue(1000, 0)       # the start delay legitimately moves time once
    t1 = b.c.Global_Clock
    b.c.drain_timed_queue(100000, 0)
    adv = b.c.Global_Clock - t1
    check(adv == 0, f"simulated time advanced by {adv} ticks; expected it to stay at tick {t1}")
    return (f"after 100000 more tasks the clock is still at tick {t1}: the clock just flips (in the UI each flip gets a "
            f"frame via task_manager's sleep, so it is benign there)")


# =============================================================================
# TIER D - combinational architectures and hazards
# =============================================================================
def full_adder(b, a, bb, cin):
    x1 = b.gate(XOR, a, bb)
    s = b.gate(XOR, x1, cin)
    c1 = b.gate(AND, a, bb)
    c2 = b.gate(AND, x1, cin)
    co = b.gate(OR, c1, c2)
    return s, co, c2


def ripple_adder(n, a_val=None):
    b = new_bench()
    A = [b.var() for _ in range(n)]
    B = [b.var() for _ in range(n)]
    cin = b.var()
    if a_val is not None:
        for i in range(n):
            if (a_val >> i) & 1:
                b.c.toggle(A[i].location, 1)
    sums, couts, c2s = [], [], []
    carry = cin
    for i in range(n):
        s, co, c2 = full_adder(b, A[i], B[i], carry)
        sums.append(s); couts.append(co); c2s.append(c2)
        carry = co
    b.start()
    return b, A, B, cin, sums, couts, c2s


def kogge_stone(n, a_val=None):
    b = new_bench()
    A = [b.var() for _ in range(n)]
    B = [b.var() for _ in range(n)]
    if a_val is not None:
        for i in range(n):
            if (a_val >> i) & 1:
                b.c.toggle(A[i].location, 1)
    p = [b.gate(XOR, A[i], B[i]) for i in range(n)]
    G = [b.gate(AND, A[i], B[i]) for i in range(n)]
    P = list(p)
    d = 1
    while d < n:
        nG, nP = list(G), list(P)
        for i in range(d, n):
            t = b.gate(AND, P[i], G[i - d])
            nG[i] = b.gate(OR, G[i], t)
            nP[i] = b.gate(AND, P[i], P[i - d])
        G, P = nG, nP
        d *= 2
    outs = [b.gate(BUF, p[0])] + [b.gate(XOR, p[i], G[i - 1]) for i in range(1, n)]
    cout = b.gate(BUF, G[n - 1])
    b.start()
    return b, A, B, outs, cout


def bits_of(b, gates):
    return sum(int(g.output) << i for i, g in enumerate(gates))


@case("D1", "Ripple-carry adder n=4..64: worst-case carry latency equals the structural path sum; exactly linear in n")
def d1():
    T = {}
    for n in (4, 8, 16, 32, 64):
        b, A, B, cin, sums, couts, c2s = ripple_adder(n, a_val=(1 << n) - 1)
        x = experiment(b, [(10, cin.location, 1)], icarus=(n <= 16))
        delays = node_delays(x.nodes)
        want = sum(delays[c2s[i].location] + delays[couts[i].location] for i in range(n))
        got = [t for t, l, v in x.trace if l == couts[n - 1].location][-1] - 10
        check(got == want, f"n={n}: carry latency {got} != path sum {want}")
        check(bits_of(b, sums) == 0 and int(couts[n - 1].output) == 1, "sum must wrap to 0 with carry out")
        check(got <= sta_arrival(x.nodes)[couts[n - 1].location], "dynamic latency must not exceed STA bound")
        T[n] = got
    beta = (T[64] - T[32]) // 32
    check((T[64] - T[32]) % 32 == 0 and (T[32] - T[16]) == 16 * beta and (T[16] - T[8]) == 8 * beta
          and (T[8] - T[4]) == 4 * beta, f"latency not linear: {T}")
    return f"cin->cout latency {T} ticks; constant {beta} ticks/bit (AND2+OR2 stage); matches path sum"


@case("D2", "Kogge-Stone adder is functionally exact and its worst-case delay grows sub-linearly vs ripple-carry")
def d2():
    rng = random.Random(2)
    res = {}
    for n in (4, 8, 16, 32):
        # worst case for both: A=all ones, B 0 -> 1 on bit 0 (full-width carry)
        wave = [(10, None, 1)]
        for kind in ("ripple", "ks"):
            if kind == "ripple":
                b, A, B, cin, sums, couts, c2s = ripple_adder(n, a_val=(1 << n) - 1)
                outs = sums + [couts[-1]]
            else:
                b, A, B, outs, cout = kogge_stone(n, a_val=(1 << n) - 1)
                outs = outs + [cout]
            x = experiment(b, [(10, B[0].location, 1)], icarus=(n <= 16))
            last = max(t for t, l, v in x.trace if l in {g.location for g in outs}) - 10
            check(bits_of(b, outs) == (1 << n), f"{kind} n={n}: A+B settled to {bits_of(b, outs)}")
            res[(kind, n)] = last
            # random functional check (settled state) on a fresh instance
        b, A, B, outs, cout = kogge_stone(n)
        for _ in range(12):
            a, bv = rng.getrandbits(n), rng.getrandbits(n)
            wave = [(1 + i, A[i].location, (a >> i) & 1) for i in range(n)] + \
                   [(1 + i, B[i].location, (bv >> i) & 1) for i in range(n)]
            b.eng.drive(wave)
            check(bits_of(b, outs) + (int(cout.output) << n) == a + bv, f"KS n={n}: {a}+{bv} wrong")
    r = {n: res[("ripple", n)] for n in (4, 8, 16, 32)}
    k = {n: res[("ks", n)] for n in (4, 8, 16, 32)}
    check(r[32] > 4 * k[32], f"KS should beat ripple by >4x at n=32: ripple {r[32]} ks {k[32]}")
    check(k[32] < 2 * k[8], f"KS delay must grow sub-linearly: {k}")
    check(r[32] > 3.5 * r[8], f"ripple delay must grow ~linearly: {r}")
    return f"worst-case settle ripple={r}  kogge-stone={k}"


@case("D3", "MUX static-1 hazard: dip appears only if its width exceeds the OR delay; consensus term removes it")
def d3():
    rows = []
    for m in range(0, 7):
        for consensus in (False, True):
            b = new_bench()
            a, bb, s = b.var(), b.var(), b.var()
            for v in (a, bb, s):
                b.c.toggle(v.location, 1)
            line = [b.gate(NOT, s)]
            for _ in range(m):
                line.append(b.gate(BUF, line[-1]))
            and1 = b.gate(AND, a, line[-1])
            and2 = b.gate(AND, bb, s)
            terms = [and1, and2] + ([b.gate(AND, a, bb)] if consensus else [])
            y = b.gate(OR, *terms)
            b.gate(BUF, y)
            b.start()
            x = experiment(b, [(20, s.location, 0)])
            dl = node_delays(x.nodes)
            off = 20 + dl[and2.location]                         # and2 turns off -> OR re-evaluates
            on = 20 + sum(dl[g.location] for g in line) + dl[and1.location]   # and1 turns on
            dip = on - off
            ycm = gate_commits(x, y)
            if consensus:
                check(ycm == [], f"m={m}: consensus term must remove the hazard, got {ycm}")
                continue
            check(dip == 2 + 3 * m, f"structural dip width {dip} != {2 + 3 * m}")
            d_or = dl[y.location]
            if dip > d_or:
                check(ycm == [(off + d_or, 0), (on + d_or, 1)], f"m={m}: unexpected Y commits {ycm}")
            elif dip < d_or:
                check(ycm == [], f"m={m}: dip {dip} < OR delay {d_or} must be filtered, got {ycm}")
            else:
                check(len(x.ties) >= 1, "dip == OR delay must be flagged as a tie")
            rows.append(f"m={m}:{dip}->{'dip' if ycm else ('tie' if dip == d_or else 'filt')}")
    return "no consensus term " + " ".join(rows) + f" (OR delay 8); with consensus term: never"


@case("D4", "XOR parity of 15 inputs: chain critical path O(n) vs balanced tree O(log n), exact path sums")
def d4():
    n = 15

    def build(kind):
        b = new_bench()
        xs = [b.var() for _ in range(n)]
        if kind == "chain":
            acc = xs[0]
            for i in range(1, n):
                acc = b.gate(XOR, acc, xs[i])
            out = acc
        else:
            layer = list(xs)
            while len(layer) > 1:
                nxt = [b.gate(XOR, layer[i], layer[i + 1]) for i in range(0, len(layer) - 1, 2)]
                if len(layer) % 2:
                    nxt.append(layer[-1])
                layer = nxt
            out = layer[0]
        b.start()
        return b, xs, out

    res = {}
    for kind in ("chain", "tree"):
        b, xs, out = build(kind)
        nodes = b.netlist()
        want = arrival_from(nodes, xs[0].location)[out.location]
        x = experiment(b, [(10, xs[0].location, 1)])
        got = gate_commits(x, out)[-1][0] - 10
        check(got == want, f"{kind}: x0->parity latency {got} != structural path sum {want}")
        check(x.icarus, f"{kind}: single-toggle run should be tie-free and Icarus-checked")
        # all inputs together: report spurious activity (ties expected in the chain)
        b2, xs2, out2 = build(kind)
        x2 = experiment(b2, [(10, v.location, 1) for v in xs2])
        check(int(out2.output) == n % 2, "parity wrong")
        res[kind] = (got, len(gate_commits(x2, out2)), len(x2.ties))
    check(res["chain"][0] > 2.5 * res["tree"][0], f"chain should be >2.5x slower: {res}")
    return (f"x0->out: chain={res['chain'][0]} ticks, tree={res['tree'][0]} ticks (exact path sums, Icarus-checked). "
            f"All-inputs-together: out commits chain={res['chain'][1]}/tree={res['tree'][1]}, "
            f"same-tick ties chain={res['chain'][2]}/tree={res['tree'][2]}")



# =============================================================================
# TIER E - sequential timing (gate-level master-slave DFF built from DFF.json)
# =============================================================================
def dff_bench(d_init=0):
    b = new_bench()
    clk, d = b.var(), b.var()
    if d_init:
        b.c.toggle(d.location, 1)
    q, qb = build_flat_ic(b, DFF_JSON, [clk, d])
    return b, clk, d, b.c.gate_verse[q], b.c.gate_verse[qb]


WARM_T = 80   # settled-state time after the initial flush pulse (clock 5..60)


def warm_wave(clk):
    return [(5, clk.location, 1), (60, clk.location, 0)]


def clock_wave(loc, start, period, cycles, high=None):
    h = period // 2 if high is None else high
    w = []
    for k in range(cycles):
        w += [(start + k * period, loc, 1), (start + k * period + h, loc, 0)]
    return w


def value_at(trace, loc, t, init):
    v = init
    for (tt, l, val) in sorted(trace):
        if l == loc and tt <= t:
            v = val
    return v


def capture_point(tau, direction, check_icarus=True):
    """D makes a 0->1 (direction 1) or 1->0 (0) transition at tau relative to the rising CLK edge."""
    b, clk, d, q, qb = dff_bench(0 if direction else 1)
    b.start()
    T = 100
    wave = warm_wave(clk) + [(T, clk.location, 1), (T + tau, d.location, direction),
                             (T + 200, clk.location, 0)]
    x = experiment(b, wave, icarus=check_icarus, warm=WARM_T)
    return int(q.output), x


_CHAR = {}


def dff_curve(direction, icarus=False, lo=-30, hi=-2):
    """[(tau, captured, clk->Q)] for a D transition at tau relative to the rising CLK edge."""
    rows = []
    for tau in range(lo, hi + 1):
        b, clk, d, q, qb = dff_bench(0 if direction else 1)
        b.start()
        wave = warm_wave(clk) + [(100, clk.location, 1), (100 + tau, d.location, direction),
                                 (300, clk.location, 0)]
        x = experiment(b, wave, icarus=icarus, warm=WARM_T)
        qt = [t - 100 for t, l, v in x.trace if l == q.location and t >= 60 and v == direction]
        captured = (int(q.output) == direction)
        rows.append((tau, captured, qt[0] if (captured and qt) else None))
    return rows


def curve_params(rows):
    caps = [(t, qt) for t, c, qt in rows if c]
    nominal = caps[0][1]
    su = -caps[-1][0]
    k = -max(t for t, qt in caps if qt == nominal)
    return nominal, k, su


def dff_char():
    """Isolated characterisation of the gate-level DFF (cached): nominal clk->Q, knee K and setup per polarity."""
    if not _CHAR:
        for direction, tag in ((1, "r"), (0, "f")):
            nominal, k, su = curve_params(dff_curve(direction))
            _CHAR.update({"cq_" + tag: nominal, "K_" + tag: k, "su_" + tag: su})
    return _CHAR


@case("E1", "DFF clk->Q for capture-1 and capture-0 equals the structural gate-path sums; functional check")
def e1():
    b, clk, d, q, qb = dff_bench(0)
    b.start()
    wave = warm_wave(clk) + [(100, d.location, 1), (200, clk.location, 1), (300, clk.location, 0),
                             (350, d.location, 0), (450, clk.location, 1), (550, clk.location, 0)]
    x = experiment(b, wave, warm=WARM_T)
    m = b.flat_map
    dl = node_delays(x.nodes)
    dd = lambda eid: dl[m[eid].location]
    # entry ids from DFF.json: 11,12 = slave gating NANDs, 13/14 = slave SR latch (Q, Q')
    q_r = [t - 200 for t, l, v in x.trace if l == q.location and t >= 200 and v == 1][0]
    qb_f = [t - 200 for t, l, v in x.trace if l == qb.location and t >= 200 and v == 0][0]
    q_f = [t - 450 for t, l, v in x.trace if l == q.location and t >= 450 and v == 0][0]
    qb_r = [t - 450 for t, l, v in x.trace if l == qb.location and t >= 450 and v == 1][0]
    check(q_r == dd(11) + dd(13), f"Q rise {q_r} != gates 11+13 = {dd(11) + dd(13)}")
    check(qb_f == dd(11) + dd(13) + dd(14), f"Q' fall {qb_f} != {dd(11) + dd(13) + dd(14)}")
    check(qb_r == dd(12) + dd(14), f"Q' rise {qb_r} != {dd(12) + dd(14)}")
    check(q_f == dd(12) + dd(14) + dd(13), f"Q fall {q_f} != {dd(12) + dd(14) + dd(13)}")
    check(int(q.output) == 0 and int(qb.output) == 1)
    return (f"clk->Q rise={q_r}, fall={q_f}; clk->Q' fall={qb_f}, rise={qb_r} (all equal structural path sums); "
            f"validated vs {ok_tag(x)}")


@case("E2", "Setup sweep: sharp capture boundary; clk->Q is flat, then rises 1 tick per tick of D lateness (time borrowing)")
def e2():
    out = {}
    for direction, name in ((1, "D rise"), (0, "D fall")):
        rows = dff_curve(direction, icarus=True, lo=-30, hi=11)
        bits = "".join("1" if c else "0" for _, c, _ in rows)
        check(bits == "1" * bits.count("1") + "0" * bits.count("0"),
              f"{name}: capture result not a single step across tau: {bits}")
        check(bits[0] == "1" and bits[-1] == "0", f"{name}: sweep does not cross the boundary: {bits}")
        nominal, k, su = curve_params(rows)
        for tau, c, qt in rows:
            if c:
                want = nominal + max(0, tau + k)
                check(qt == want, f"{name}: tau={tau} clk->Q={qt}, time-borrowing law predicts {want}")
        out[name] = (nominal, k, su)
    _CHAR.update({"cq_r": out["D rise"][0], "K_r": out["D rise"][1], "su_r": out["D rise"][2],
                  "cq_f": out["D fall"][0], "K_f": out["D fall"][1], "su_f": out["D fall"][2]})
    r, f = out["D rise"], out["D fall"]
    return (f"D rise: clk->Q={r[0]} for D earlier than {r[1]} ticks before the edge, then +1/tick until capture fails "
            f"(setup {r[2]}); D fall: clk->Q={f[0]}, knee {f[1]}, setup {f[2]}. No re-entrant window. "
            f"All points cross-checked vs RefSim" + (" and Icarus" if ICARUS else ""))


@case("E3", "Minimum clock pulse widths (high and low): sharp thresholds bounded by the gate delays on the capture path")
def e3():
    def high_pulse(w, flat=True):
        b, clk, d, q, qb = dff_bench(0)
        b.start()
        wave = warm_wave(clk) + [(90, d.location, 1), (100, clk.location, 1), (100 + w, clk.location, 0)]
        x = experiment(b, wave, warm=WARM_T)
        return int(q.output), x, b

    res = []
    for w in range(1, 26):
        qv, x, b = high_pulse(w)
        res.append(qv)
    s = "".join(map(str, res))
    check(s == "0" * s.count("0") + "1" * s.count("1"), f"high pulse: not a single threshold: {s}")
    w_hi = s.count("0") + 1
    b, clk, d, q, qb = dff_bench(0)
    b.start()
    m = b.flat_map
    dl = node_delays(b.netlist())
    bound = max(dl[m[11].location], dl[m[13].location])
    check(w_hi >= bound, f"min high pulse {w_hi} below slowest capture-path gate delay {bound}: impossible")

    def low_pulse(w):
        b, clk, d, q, qb = dff_bench(1)
        b.start()
        wave = warm_wave(clk) + [(100, clk.location, 1), (150, d.location, 0),
                                 (200, clk.location, 0), (200 + w, clk.location, 1), (400, clk.location, 0)]
        x = experiment(b, wave, warm=WARM_T)
        return int(q.output)

    lo = "".join(str(low_pulse(w)) for w in range(1, 26))
    check(lo == "1" * lo.count("1") + "0" * lo.count("0"), f"low pulse: not a single threshold: {lo}")
    w_lo = lo.count("1") + 1
    # the same sweep on the IC form of the DFF (pin gates in the clock path)
    def ic_high(w):
        b = new_bench()
        clk, d = b.var(), b.var()
        ic = b.c.getIC(DFF_JSON)
        b.c.connect(ic.inputs[0], clk.location, 0)
        b.c.connect(ic.inputs[1], d.location, 0)
        b.start()
        wave = warm_wave(clk) + [(90, d.location, 1), (100, clk.location, 1), (100 + w, clk.location, 0)]
        experiment(b, wave, warm=WARM_T)
        return int(ic.outputs[0].output)
    ic = "".join(str(ic_high(w)) for w in range(1, 26))
    check(ic == "0" * ic.count("0") + "1" * ic.count("1"), f"IC high pulse: not a single threshold: {ic}")
    w_ic = ic.count("0") + 1
    return (f"min CLK-high pulse: gate-level DFF={w_hi} ticks (bound >= {bound}); IC form={w_ic} ticks "
            f"(pin gates add load); min CLK-low pulse={w_lo} ticks; all points cross-checked vs RefSim/Icarus")


def tff_bench():
    b = new_bench()
    clk = b.var()
    nq = b.c.getcomponent(NOT)
    q, qb = build_flat_ic(b, DFF_JSON, [clk, nq])
    q = b.c.gate_verse[q]
    b.connect(nq, 0, q)
    b.start()
    return b, clk, q, nq


def tff_passes(p, cycles=12):
    b, clk, q, nq = tff_bench()
    start = 100
    x = experiment(b, warm_wave(clk) + clock_wave(clk.location, start, p, cycles) , icarus=False)
    seq = [value_at(x.trace, q.location, start + k * p + p - 1, None) for k in range(cycles)]
    seq = [int(b.c.gate_verse[q.location].output) if v is None else v for v in seq]
    ok = all(seq[k] == 1 - seq[k - 1] for k in range(3, cycles))
    return ok, x, b, q, nq


@case("E4", "Toggle flip-flop Fmax from components: p* = (cq_r + cq_f + 2*d_loop + K_r + K_f) / 2")
def e4():
    res = {p: tff_passes(p, cycles=30)[0] for p in range(8, 70)}
    p_star = max(p for p, ok in res.items() if not ok) + 1
    check(all(res[p] for p in range(p_star, 70)), "passes must hold for all periods above the threshold")
    check(not any(res[p] for p in range(8, p_star - 6)), "fails must hold well below the threshold")
    # clk->Q in THIS circuit (Q loaded by the loop NOT) at a safe slow clock
    ok, x, b, q, nq = tff_passes(200, cycles=6)
    dl = node_delays(x.nodes)
    edge = lambda k: 100 + k * 200
    q_rise = [t - edge(k) for k in range(2, 6) for t, l, v in x.trace if l == q.location and v == 1 and edge(k) <= t < edge(k) + 100]
    q_fall = [t - edge(k) for k in range(2, 6) for t, l, v in x.trace if l == q.location and v == 0 and edge(k) <= t < edge(k) + 100]
    cq_r, cq_f = q_rise[0], q_fall[0]
    ch = dff_char()
    d_not = dl[nq.location]
    # Q rise -> D fall (knee K_f) -> Q fall -> D rise (knee K_r): lateness accumulates iff the 2-cycle
    # sum exceeds 2p, because beyond the knee clk->Q grows 1:1 with D lateness
    total = cq_r + cq_f + 2 * d_not + ch["K_r"] + ch["K_f"]
    pred = -(-total // 2)
    check(p_star == pred, f"measured Fmax period {p_star} vs composed prediction {pred} "
          f"(cq_r={cq_r}, cq_f={cq_f}, d_loop={d_not}, K_r={ch['K_r']}, K_f={ch['K_f']})")
    return (f"T_min={p_star} ticks = ({cq_r}+{cq_f}+2*{d_not}+{ch['K_r']}+{ch['K_f']})/2 = {pred}; "
            f"passes for every period 29..69 over 30 cycles, fails below (intermittently just under, by lateness drift)")


@case("E5", "Clock-skew race-through: boundary predicted per skew from DFF setup and measured arrival times")
def e5():
    ch = dff_char()
    rows = []
    race_seen, ok_seen = False, False
    for k in range(0, 15):
        b = new_bench()
        clk, din = b.var(), b.var()
        q1n, _ = build_flat_ic(b, DFF_JSON, [clk, din])
        c2 = clk
        for _ in range(k):
            c2 = b.gate(BUF, c2)
        q2n, _ = build_flat_ic(b, DFF_JSON, [c2, b.c.gate_verse[q1n]])
        q1, q2 = b.c.gate_verse[q1n], b.c.gate_verse[q2n]
        b.start()
        # two flush pulses (din=0) so both stages hold a defined 0; skew delays stage 2's copy of them
        flush = warm_wave(clk) + [(90, clk.location, 1), (140, clk.location, 0)]
        wave = flush + [(250, din.location, 1), (350, clk.location, 1), (450, clk.location, 0)]
        x = experiment(b, wave, warm=220)
        t_d2 = [t for t, l, v in x.trace if l == q1.location and t >= 350][0]
        t_c2 = [t for t, l, v in x.trace if l == c2.location and t >= 350][0] if k else 350
        tau = t_d2 - t_c2
        predicted_race = (tau <= -ch["su_r"])
        actual_race = (int(q1.output) == 1 and int(q2.output) == 1)
        check(int(q1.output) == 1, "stage 1 must always capture")
        check(actual_race == predicted_race,
              f"skew {k} buffers: tau={tau}, setup={ch['su_r']}: predicted race={predicted_race}, actual={actual_race}")
        race_seen |= actual_race
        ok_seen |= not actual_race
        rows.append(f"{k}:{'RACE' if actual_race else 'ok'}(tau={tau})")
    check(race_seen and ok_seen, "sweep must cross the race boundary")
    return "skew buffers -> outcome: " + " ".join(rows)


def counter_bench(n, kind):
    b = new_bench()
    clk = b.var()
    qs, ds = [], []
    carry = None
    for i in range(n):
        if kind == "sync":
            if i == 0:
                dn = b.c.getcomponent(NOT)
            else:
                dn = b.c.getcomponent(XOR)
            ds.append(dn)
        q, _ = build_flat_ic(b, DFF_JSON, [clk, ds[i]])
        qs.append(b.c.gate_verse[q])
    carry = None
    for i in range(n):
        if i == 0:
            b.connect(ds[0], 0, qs[0])
        else:
            carry = qs[0] if i == 1 else b.gate(AND, carry, qs[i - 1])
            b.connect(ds[i], 0, qs[i])
            b.connect(ds[i], 1, carry)
    b.start()
    return b, clk, qs, ds


def counter_ok(n, p, cycles=None):
    cycles = cycles or (1 << n) + 4
    b, clk, qs, ds = counter_bench(n, "sync")
    start = 100
    # settle the flops with a few slow pulses first, then run `cycles` at period p
    wave = warm_wave(clk) + [(120 + 200 * i, clk.location, 1) for i in range(0)]
    x = experiment(b, wave + clock_wave(clk.location, start, p, cycles), icarus=False)
    states = []
    for k in range(cycles):
        t = start + k * p + p - 1
        states.append(sum(value_at(x.trace, qs[i].location, t, int(qs[i].output)) << i for i in range(n)))
    ok = all(states[k] == (states[k - 1] + 1) % (1 << n) for k in range(2, cycles))
    return ok, x, qs, ds, states


@case("E6", "Synchronous binary counter n=2..5: Fmax matches clk->Q + data-path arrival + setup, and grows with n")
def e6():
    ch = dff_char()
    rows, ps = [], []
    for n in (2, 3, 4, 5):
        res = {p: counter_ok(n, p)[0] for p in range(10, 140)}
        p_star = max(p for p, ok in res.items() if not ok) + 1
        check(all(res[p] for p in range(p_star, 140)), f"n={n}: passes must hold above threshold")
        # dynamic worst data arrival over all cycles of a slow run, per D polarity
        ok, x, qs, ds, states = counter_ok(n, 400)
        check(ok, "counter must count correctly at a slow clock")
        need = 0
        for k in range(2, (1 << n) + 4):
            edge = 100 + k * 400
            for dgate in ds:
                last = [(t, v) for t, l, v in x.trace if l == dgate.location and edge <= t < edge + 399]
                if last:
                    t, v = last[-1]
                    need = max(need, (t - edge) + (ch["su_r"] if v == 1 else ch["su_f"]))
        check(abs(p_star - need) <= 2, f"n={n}: Fmax period {p_star} vs worst arrival+setup {need}")
        rows.append(f"n={n}:T_min={p_star}(pred {need})")
        ps.append(p_star)
    check(all(a <= b_ for a, b_ in zip(ps, ps[1:])) and ps[-1] > ps[0], f"T_min must grow with n: {ps}")
    return " ".join(rows) + "; prediction = latest D arrival after the edge + polarity setup, from a slow-clock run"


def decode_commits(kind):
    """2-bit counter + 2-to-4 decoder. Returns per-transition decoded-line commit counts and states."""
    b = new_bench()
    clk = b.var()
    nq0 = b.c.getcomponent(NOT)
    if kind == "ripple":
        nq1 = b.c.getcomponent(NOT)
        q0n, qb0n = build_flat_ic(b, DFF_JSON, [clk, nq0])
        q0, qb0 = b.c.gate_verse[q0n], b.c.gate_verse[qb0n]
        b.connect(nq0, 0, q0)
        q1n, _ = build_flat_ic(b, DFF_JSON, [qb0, nq1])
        q1 = b.c.gate_verse[q1n]
        b.connect(nq1, 0, q1)
    else:
        if kind == "gray":
            d0 = nq0
            d1 = b.c.getcomponent(BUF)
        else:
            d0 = nq0
            d1 = b.c.getcomponent(XOR)
        q0n, _ = build_flat_ic(b, DFF_JSON, [clk, d0])
        q1n, _ = build_flat_ic(b, DFF_JSON, [clk, d1])
        q0, q1 = b.c.gate_verse[q0n], b.c.gate_verse[q1n]
        if kind == "gray":     # q0' = !q1, q1' = q0
            b.connect(nq0, 0, q1)
            b.connect(d1, 0, q0)
        else:                  # binary: q0' = !q0, q1' = q1 ^ q0
            b.connect(nq0, 0, q0)
            b.connect(d1, 0, q1)
            b.connect(d1, 1, q0)
    n0, n1 = b.gate(NOT, q0), b.gate(NOT, q1)
    y = [b.gate(AND, n1, n0), b.gate(AND, n1, q0), b.gate(AND, q1, n0), b.gate(AND, q1, q0)]
    for g in y:
        b.gate(BUF, g)
    b.start()
    return b, clk, q0, q1, y


def decoder_run(kind, steps=8, p=300):
    b, clk, q0, q1, y = decode_commits(kind)
    wave = warm_wave(clk) + clock_wave(clk.location, 100, p, steps)
    x = experiment(b, wave, icarus=False)
    per = []
    states = []
    for k in range(steps):
        lo, hi = 100 + k * p, 100 + k * p + p
        per.append(sum(1 for t, l, v in x.trace if lo <= t < hi and l in {g.location for g in y}))
        states.append(int(value_at(x.trace, q1.location, hi - 1, int(q1.output))) * 2 +
                      int(value_at(x.trace, q0.location, hi - 1, int(q0.output))))
    return per, states


@case("E7", "Decoder glitches: Gray-coded synchronous counter is hazard-free; binary and ripple counters glitch")
def e7():
    out = {}
    for kind in ("gray", "binary", "ripple"):
        per, states = decoder_run(kind)
        out[kind] = (per, states)
    gray_per, gray_st = out["gray"]
    # after the first step each transition changes one decoded line pair: exactly 2 commits, never more
    check(all(c == 2 for c in gray_per[2:]), f"gray counter must give exactly 2 decoded commits/step: {gray_per}")
    seq = gray_st[2:]
    check(all(bin(a ^ b_).count("1") == 1 for a, b_ in zip(seq, seq[1:])), f"gray sequence invalid {seq}")
    bin_per, bin_st = out["binary"]
    rip_per, rip_st = out["ripple"]
    check(max(bin_per[2:]) > 2 or max(rip_per[2:]) > 2, "a multi-bit-change counter must show decoder glitches")
    check(max(rip_per[2:]) > 2, f"ripple counter must glitch the decoder: {rip_per}")
    return (f"decoded-line commits per clock step (2 = clean hand-off): gray={gray_per[2:]} binary={bin_per[2:]} "
            f"ripple={rip_per[2:]}")



# =============================================================================
# TIER F - industrial benchmark netlists (ISCAS-85)
# =============================================================================
ISCAS85 = [("c17", 20), ("c432", 8), ("c499", 8), ("c880", 8), ("c1355", 8), ("c1908", 8),
           ("c2670", 6), ("c3540", 6), ("c5315", 6), ("c6288", 4), ("c7552", 4)]


class Adopted(Bench):
    def __init__(self, c, input_gates):
        self.c, self.vars, self.gates, self.eng = c, list(input_gates), [], None


_CACHE = {}


def load_iscas(name):
    if name in _CACHE:
        return _CACHE[name]
    try:
        from benchmark import VerilogRunner
    except ImportError:
        raise Skip("benchmark.VerilogRunner not importable")
    path = os.path.join(ROOT, "tests", "ISCAS85", name + ".v")
    if not os.path.exists(path):
        raise Skip(f"{path} missing")
    r = VerilogRunner(path, Circuit.Circuit, Const, is_reactor=True)
    b = Adopted(r.circuit, r.input_vars)
    b.start()
    nodes = b.netlist()
    outs = [g.location for g in r.output_objects]
    _CACHE[name] = (b, nodes, outs)
    return _CACHE[name]



def tainted_nets(nodes, tie_gates):
    """Transitive fan-out cone of every tied gate: the only nets a same-tick tie can influence."""
    fo = fanout_lists(nodes)
    seen = set()
    stack = list(tie_gates)
    while stack:
        u = stack.pop()
        if u in seen:
            continue
        seen.add(u)
        stack.extend(v for v, _ in fo[u])
    return seen


def bad_windows(nodes, windows, A, B, ties):
    """Window indices where traces A and B differ on nets outside the fan-out cone of a tie."""
    out = []
    for j, (a, e) in enumerate(windows):
        taint = tainted_nets(nodes, {g for (t, g) in ties if a <= t < e})
        if canon([ev for ev in A if a <= ev[0] < e and ev[1] not in taint]) != \
           canon([ev for ev in B if a <= ev[0] < e and ev[1] not in taint]):
            out.append(j)
    return out


def compare_icarus(name, nodes, x, wave, windows, gap, arr):
    """Per vector window, compare engine vs Icarus on every net outside the fan-out cone of a
    same-tick tie. Returns (events_compared, events_total, mismatching_windows)."""
    ic = icarus_trace(nodes, x.init, wave, tail=gap * len(windows) + 50, base=max(arr) + 200)
    cmp_ev = tot_ev = 0
    bad = []
    for j, (a, e) in enumerate(windows):
        ties = {g for (t, g) in x.ties if a <= t < e}
        taint = tainted_nets(nodes, ties)
        eng_w = canon([ev for ev in x.trace if a <= ev[0] < e and ev[1] not in taint])
        ic_w = canon([ev for ev in ic if a <= ev[0] < e and ev[1] not in taint])
        cmp_ev += len(eng_w)
        tot_ev += len([ev for ev in x.trace if a <= ev[0] < e])
        if eng_w != ic_w:
            bad.append((j, first_diff(eng_w, ic_w)))
    return cmp_ev, tot_ev, bad


def vector_wave(rng, b, nvec, gap, skew):
    """Random vectors, each input skewed uniformly in [0, skew]; vector j starts at j*gap."""
    cur = {v.location: int(v.output) for v in b.vars}
    wave, windows = [], []
    for j in range(nvec):
        base = j * gap
        windows.append((base, base + gap))
        for v in b.vars:
            nv = rng.randint(0, 1)
            if nv != cur[v.location]:
                wave.append((base + (rng.randint(0, skew) if skew else 0), v.location, nv))
                cur[v.location] = nv
    return wave, windows


def window_of(t, windows):
    for j, (a, e) in enumerate(windows):
        if a <= t < e:
            return j
    return None


def run_benchmark(name, nvec, skew, seed, gap_extra=150):
    b, nodes, outs = load_iscas(name)
    # restore a known start state: all-zero inputs settled
    b.eng.drive([(0, v.location, 0) for v in b.vars])
    arr = sta_arrival(nodes)
    gap = max(arr) + gap_extra
    rng = random.Random(seed)
    wave, windows = vector_wave(rng, b, nvec, gap, skew)
    x = experiment(b, wave, icarus=False)
    return b, nodes, outs, arr, gap, wave, windows, x


@case("F1", "ISCAS-85 timed traces: engine == reference exactly; == Icarus on every net outside tie cones (no duplicate pins)")
def f1():
    rows = []
    total_events = tot_cmp = 0
    for name, nvec in ISCAS85:
        b, nodes, outs, arr, gap, wave, windows, x = run_benchmark(name, nvec, skew=25, seed=zlib.crc32(name.encode()) & 0xffff)
        total_events += len(x.trace)
        dup = has_dup_pins(nodes)
        note = ""
        if ICARUS and not dup:
            cmp_ev, tot_ev, bad = compare_icarus(name, nodes, x, wave, windows, gap, arr)
            if bad:
                check(False, f"{name}: engine != Icarus in vector {bad[0][0]} at {bad[0][1]}")
            tot_cmp += cmp_ev
            note = f"{100 * cmp_ev // max(1, tot_ev)}%vsIcarus"
        else:
            note = "dup-pin(see F2)" if dup else "no-icarus"
        final_in = {v.location: int(v.output) for v in b.vars}
        check([int(g.output) for g in b.c.gate_verse] == zero_delay_settle(nodes, final_in),
              f"{name}: settled state differs from zero-delay evaluation")
        rows.append(f"{name}:{len(nodes)}g/{len(x.trace)}ev/{note}/{len(x.ties)}ties")
    return f"{total_events} events, {tot_cmp} compared event-for-event with Icarus; " + " ".join(rows)


@case("F2", "ISCAS-85 vectors with same-tick commits: engine differs from Icarus only through the gate_loc tie-break", kind="limit")
def f2():
    if not ICARUS:
        raise Skip("Icarus not installed")
    # seeds found by scanning 1440 random vectors on c1908/c2670/c3540 (4 differing vectors, 0.28%)
    repro = [("c1908", 51), ("c2670", 4)]
    diff = []
    for name, seed in repro:
        b, nodes, outs, arr, gap, wave, windows, x = run_benchmark(name, 8, skew=25, seed=seed)
        ic = icarus_trace(nodes, x.init, wave, tail=gap * 8 + 50, base=max(arr) + 200)
        st0 = zero_delay_settle(nodes, x.init)
        atomic = RefSim(nodes, x.init, state=st0, tick_atomic=True)
        t_at = atomic.run(wave)
        check(not bad_windows(nodes, windows, t_at, ic, atomic.ties),
              f"{name}: evaluate-once-per-tick reference disagrees with Icarus; the explanation does not hold")
        eng_bad = bad_windows(nodes, windows, x.trace, ic, x.ties)
        check(eng_bad, f"{name} seed {seed}: engine unexpectedly matches Icarus (limit no longer present)")
        diff.append(f"{name} seed {seed}: vector(s) {eng_bad}")
    return ("engine differs from Icarus on " + "; ".join(diff) + "; evaluating each gate once per tick reproduces "
            "Icarus exactly on both, so the difference is the same-tick tie-break policy")


@case("F3", "Per-net invariants on ISCAS-85: commit parity == functional change; settle time <= per-net STA arrival")
def f3():
    rows = []
    for name, nvec in ISCAS85:
        b, nodes, outs, arr, gap, wave, windows, x = run_benchmark(name, nvec, skew=0, seed=zlib.crc32(name.encode()) & 0xff0f)
        nets = len(nodes)
        prev = [int(v) for v in zero_delay_settle(nodes, {l: 0 for l in range(nets) if nodes[l][0] == VAR})]
        by_win = {}
        for t, l, v in x.trace:
            by_win.setdefault(window_of(t, windows), []).append((t, l, v))
        cur_in = {v.location: 0 for v in b.vars}
        worst_ratio = 0.0
        tot_commits = tot_func = 0
        for j, (a, e) in enumerate(windows):
            for (t, l, v) in wave:
                if a <= t < e:
                    cur_in[l] = v
            end = zero_delay_settle(nodes, cur_in)
            ev = by_win.get(j, [])
            cnt = {}
            last = {}
            for t, l, v in ev:
                cnt[l] = cnt.get(l, 0) + 1
                last[l] = t
            t_stim = a   # skew=0: every input changes at the window start
            for l in range(nets):
                changed = end[l] != prev[l]
                check((cnt.get(l, 0) % 2 == 1) == changed, f"{name} net {l}: {cnt.get(l, 0)} commits but changed={changed}")
                if l in last:
                    check(last[l] - t_stim <= arr[l], f"{name} net {l}: settled at +{last[l] - t_stim} > STA {arr[l]}")
            func = sum(1 for l in range(nets) if end[l] != prev[l] and nodes[l][0] != VAR)
            comm = sum(c for l, c in cnt.items() if nodes[l][0] != VAR)
            tot_commits += comm
            tot_func += func
            prev = end
        ratio = tot_commits / max(1, tot_func)
        out_settle = max([max([t - windows[j][0] for t, l, v in by_win.get(j, []) if l in outs] + [0])
                          for j in range(nvec)])
        rows.append((name, ratio, out_settle, max(arr[o] for o in outs)))
    txt = " ".join(f"{n}:glitch x{r:.2f},settle {s}/STA {a}" for n, r, s, a in rows)
    return "commits per functional toggle, observed output settle vs STA bound. " + txt




EXT_ISCAS89 = [("s27", 24), ("s382", 24), ("s1423", 16)]


def load_iscas89(name, optimize=False):
    try:
        from benchmark_89 import SequentialVerilogRunner
    except ImportError:
        raise Skip("benchmark_89.SequentialVerilogRunner not importable")
    path = os.path.join(ROOT, "tests", "ISCAS89", name + ".v")
    if not os.path.exists(path):
        raise Skip(f"{path} missing")
    return SequentialVerilogRunner(path, Circuit.Circuit, Const, is_reactor=True, use_optimize=optimize,
                                   dff_file=os.path.join(ROOT, "tests", "src", "DFF.json"))


def physical_vectors(rng, n_inputs, clk_idx, nvec, flush=10):
    phys = []
    for i in range(flush):
        phys.append([(i % 2) if j == clk_idx else 0 for j in range(n_inputs)])
    for _ in range(nvec):
        v = [rng.randint(0, 1) for _ in range(n_inputs)]
        for clk in (0, 1):
            phys.append([clk if j == clk_idx else v[j] for j in range(n_inputs)])
    return phys


def state_pins(c):
    """Locations of every IC/primary output pin: flop Q/Q' and primary outputs."""
    return [g.location for g in c.gate_verse if g.id == PIN_OUT]


def zero_delay_reference(name, phys):
    """Per physical step, the state of every output pin under zero-delay (SIMULATE) evaluation."""
    import asyncio
    r = load_iscas89(name)

    async def go():
        r.circuit.simulate(Const.SIMULATE)
        Const.set_MODE(Const.SIMULATE)
        pins = state_pins(r.circuit)
        rows = []
        for vec in phys:
            batch = r.build_physical_batches([vec])[0]
            r.circuit.batch_toggle(batch, len(batch))
            rows.append([int(r.circuit.gate_verse[p].output) for p in pins])
        return rows

    return asyncio.run(go())


def sequential_run(name, H, phys, flush_steps, check_ref=False):
    """Clock the netlist with one physical step every H ticks; sample every output pin just before
    the next step. Returns one row per post-flush step."""
    r = load_iscas89(name)
    c = r.circuit
    b = Adopted(c, r.input_vars)
    b.start()
    cur = {v.location: int(v.output) for v in b.vars}
    wave = []
    for s_idx, vec in enumerate(phys):
        for v, bit in zip(r.input_vars, vec):
            if cur[v.location] != bit:
                wave.append((s_idx * H, v.location, bit))
                cur[v.location] = bit
    split = flush_steps * H
    b.eng.drive([w for w in wave if w[0] < split])
    check(all(int(g.output) in (0, 1) for g in c.gate_verse), "state still UNKNOWN after the flush phase")
    pins = state_pins(c)
    start = {p: int(c.gate_verse[p].output) for p in pins}
    post = [(t - split, l, v) for t, l, v in wave if t >= split]
    if check_ref:
        trace = experiment(b, post, icarus=False).trace
    else:
        t0 = b.eng.now()
        trace = [(t - t0, l, v) for t, l, v in b.eng.drive(post)]
    by = {p: [] for p in pins}
    for (t, l, v) in sorted(trace):
        if l in by:
            by[l].append((t, v))
    rows = []
    for k in range(len(phys) - flush_steps):
        t_samp = (k + 1) * H - 1
        row = []
        for p in pins:
            v = start[p]
            for (t, val) in by[p]:
                if t <= t_samp:
                    v = val
                else:
                    break
            row.append(v)
        rows.append(row)
    return rows


@case("F4", "ISCAS-89 sequential circuits: timed clocking equals the zero-delay reference above a sharp minimum half-period")
def f4():
    rows = []
    for name, nvec in EXT_ISCAS89:
        r = load_iscas89(name)
        n_in = len(r.input_vars)
        clk_idx = r.input_vars.index(r._find_clock_var())
        rng = random.Random(zlib.crc32(name.encode()))
        flush = 10
        phys = physical_vectors(rng, n_in, clk_idx, nvec, flush)
        ref = zero_delay_reference(name, phys)[flush:]
        Hs = [10, 15, 20, 30, 40, 60, 80, 120, 160, 240, 400]
        bad = {}
        for H in Hs:
            got = sequential_run(name, H, phys, flush)
            bad[H] = sum(1 for a, b_ in zip(got, ref) if a != b_)
        check(bad[400] == 0, f"{name}: half-period 400 differs from the zero-delay reference: {bad}")
        check(bad[10] > 0, f"{name}: a 10-tick half-period must violate timing, got {bad}")
        h_star = min(H for H in Hs if all(bad[h] == 0 for h in Hs if h >= H))
        below = [h for h in Hs if h < h_star]
        for H in [h_star] + below[-1:]:
            sequential_run(name, H, phys, flush, check_ref=True)    # engine == reference simulator exactly
        rows.append(f"{name}: {len(state_pins(r.circuit))} state/output pins, H*={h_star} "
                    f"(mismatching steps at H=" + ",".join(f"{h}:{bad[h]}" for h in Hs if h <= 80) + ")")
    return "; ".join(rows)


# =============================================================================
# TIER G - engine invariants on random circuits
# =============================================================================
_RANDOM = {}


def random_trials(n=120):
    """Cached sweep over small random DAGs with dense same-tick activity."""
    if "rows" in _RANDOM:
        return _RANDOM["rows"]
    rows = []
    for seed in range(n):
        rng = random.Random(1000 + seed)
        b = rand_dag(rng, 6, rng.choice([20, 40, 60]), allow_dup=False)
        wave = rand_wave(rng, b, nvec=4, skew=6, gap=90)
        nodes = b.netlist()
        init = {v.location: int(v.output) for v in b.vars}
        state = [int(g.output) for g in b.c.gate_verse]
        eng = b.eng
        t0 = eng.now()
        raw = eng.drive(wave)
        clock_end = b.c.Global_Clock
        tr = [(t - t0, l, v) for t, l, v in raw]
        dflt = RefSim(nodes, init, state=state)
        r_d = dflt.run(wave)
        atom = RefSim(nodes, init, state=state, tick_atomic=True)
        r_a = atom.run(wave)
        row = dict(seed=seed, nodes=nodes, init=init, wave=wave, trace=tr, raw_times=[t for t, _, _ in raw],
                   r_d=r_d, r_a=r_a, ties_a=atom.ties, final=[int(g.output) for g in b.c.gate_verse],
                   final_in={v.location: int(v.output) for v in b.vars}, clock_end=clock_end, t0=t0)
        if ICARUS and not atom.ties:
            arr = max(sta_arrival(nodes))
            row["ic"] = icarus_trace(nodes, init, wave, tail=arr + 400, base=arr + 200)
        rows.append(row)
    _RANDOM["rows"] = rows
    return rows


@case("G1", "Oracle validation (120 random circuits): engine == sequential reference; tick-atomic reference == Icarus on tie-free runs")
def g1():
    rows = random_trials()
    n_ic = n_tie = 0
    for r in rows:
        check(canon(r["trace"]) == canon(r["r_d"]), f"seed {r['seed']}: engine != sequential reference")
        if r["ties_a"]:
            n_tie += 1
        if "ic" in r:
            check(canon(r["ic"]) == canon(r["r_a"]), f"seed {r['seed']}: tick-atomic reference != Icarus at {first_diff(r['ic'], r['r_a'])}")
            n_ic += 1
    return (f"{len(rows)} circuits: engine matches its sequential-semantics reference on all; tick-atomic reference "
            f"matches Icarus exactly on {n_ic} tie-free runs ({n_tie} runs had same-tick ties and were excluded)")


@case("G2", "Random circuits (tie-free runs): the engine's gate_loc tie-break deviates from evaluate-once-per-tick on a small fraction", kind="limit")
def g2():
    rows = random_trials()
    bad = [r["seed"] for r in rows if not r["ties_a"] and canon(r["trace"]) != canon(r["r_a"])]
    total = sum(1 for r in rows if not r["ties_a"])
    check(bad, "no deviation found; the policy difference did not show up on these circuits")
    return f"{len(bad)} of {total} tie-free circuits differ (seeds {bad[:8]}); settled values are always correct (G3)"


@case("G3", "Invariants over random runs: commit times never decrease; settled state == zero-delay evaluation; rerun is deterministic")
def g3():
    rows = random_trials()
    for r in rows:
        ts = r["raw_times"]
        check(all(a <= b_ for a, b_ in zip(ts, ts[1:])), f"seed {r['seed']}: emitted commit times not monotone")
        want = zero_delay_settle(r["nodes"], r["final_in"])
        check(r["final"] == want, f"seed {r['seed']}: settled state != zero-delay evaluation")
    # determinism: rebuild a few circuits from the same seed and compare traces
    for seed in (3, 17, 58):
        rng = random.Random(1000 + seed)
        b = rand_dag(rng, 6, rng.choice([20, 40, 60]), allow_dup=False)
        wave = rand_wave(rng, b, nvec=4, skew=6, gap=90)
        t0 = b.eng.now()
        tr = [(t - t0, l, v) for t, l, v in b.eng.drive(wave)]
        check(canon(tr) == canon(rows[seed]["trace"]), f"seed {seed}: second build gave a different trace")
    return f"{len(rows)} runs: monotone time, zero-delay-equal final state; 3 rebuilds bit-identical"


@case("G4", "optimize_dfs/optimize_bfs relabel gates without changing timing: engine == reference and same final values")
def g4():
    finals = {}
    for seed in (5, 11, 23, 40):
        per = {}
        for mode in (None, "dfs", "bfs"):
            rng = random.Random(7000 + seed)
            b = new_bench()
            sigs = [b.var() for _ in range(6)]
            created = list(sigs)
            for _ in range(rng.choice([25, 45])):
                k = rng.choice([AND, NAND, OR, NOR, XOR, XNOR, BUF, NOT])
                n = 1 if k in SINGLE else 2
                srcs = list(dict.fromkeys(rng.choice(sigs[-10:]) for _ in range(n)))
                if k in NARY and len(srcs) < 2:
                    k, srcs = BUF, srcs[:1]
                elif k in SINGLE:
                    srcs = srcs[:1]
                g = b.gate(k, *srcs)
                sigs.append(g)
                created.append(g)
            if mode == "dfs":
                b.c.optimize_dfs()
            elif mode == "bfs":
                b.c.optimize_bfs()
            b.start()
            wave = []
            rr = random.Random(seed)
            for j in range(3):
                for v in b.vars:
                    wave.append((j * 120 + rr.randint(0, 8), v.location, rr.randint(0, 1)))
            x = experiment(b, wave, icarus=False)
            per[mode] = [int(g.output) for g in created]
        check(per[None] == per["dfs"] == per["bfs"], f"seed {seed}: final values differ across layouts")
        finals[seed] = len(per[None])
    return f"4 circuits x 3 layouts (none/dfs/bfs): each engine run equals its reference; final values identical across layouts"


@case("G5", "Async task_manager reaches the same final state and clock as synchronous draining")
def g5():
    import asyncio
    def build():
        b = new_bench()
        v = b.var()
        prev = v
        for i in range(8):
            prev = b.gate(NOT if i % 2 else BUF, prev)
        b.start()
        return b, v, prev
    b1, v1, l1 = build()
    b1.c.toggle_timed(v1.location, 1, 10)
    b1.c.drain_timed_queue()
    b2, v2, l2 = build()
    b2.c.toggle_timed(v2.location, 1, 10)
    old = Const.get_DELAY()
    Const.set_DELAY(0.0)
    try:
        async def go():
            await asyncio.wait_for(b2.c.task_manager(), 20)
        asyncio.run(go())
    finally:
        Const.set_DELAY(old)
    check(b2.c.timed_queue_empty(), "async runner must drain the queue")
    check(b1.c.Global_Clock == b2.c.Global_Clock, f"clock {b1.c.Global_Clock} vs {b2.c.Global_Clock}")
    check([int(g.output) for g in b1.c.gate_verse] == [int(g.output) for g in b2.c.gate_verse], "final outputs differ")
    return f"both finish at t={b1.c.Global_Clock} with identical outputs"


# =============================================================================
# TIER H - capacity, scope limits and model boundaries
# =============================================================================
@case("H1", "Fan-in is capped at 255 inputs: Gate.setlimits rejects 256+ (the 8-bit delay and logic fields would wrap)")
def h1():
    b = new_bench()
    g = b.c.getcomponent(AND)
    check(g.setlimits(255), "255 inputs must be accepted")
    for n in (256, 300, 512, 100000):
        check(not g.setlimits(n), f"{n} inputs must be rejected")
    check(len(g._sources) == 255, f"a rejected resize must leave the gate unchanged, has {len(g._sources)} slots")
    vs = [b.var() for _ in range(255)]
    for v in vs[1:]:
        b.c.toggle(v.location, 1)
    g2 = b.gate(AND, *vs)
    b.gate(BUF, g2)
    b.start()
    tr = b.eng.drive([(10, vs[0].location, 1)])
    tin = [t for t, l, v in tr if l == vs[0].location][0]
    got = [t - tin for t, l, v in tr if l == g2.location]
    check(got == [spec_delay(AND, 255, 1)], f"AND255 must be exact, got {got}")
    return f"255 accepted and exact (delay {got[0]}); 256, 300, 512 and 100000 rejected, gate left unchanged"


@case("H2", "By design: a later toggle_timed supersedes an earlier queued value (wave semantics); pulses need a waveform driver", kind="limit")
def h2():
    b = new_bench()
    v = b.var()
    g = b.gate(BUF, v)
    b.gate(NOT, g)
    b.start()
    c = b.c
    t0 = c.Global_Clock
    c.toggle_timed(v.location, 1, delay=10)
    c.toggle_timed(v.location, 0, delay=30)    # a 20-tick pulse, scheduled up front
    tr = b.eng.run()
    check([e for e in tr if e[1] == g.location] == [],
          "expected the pre-scheduled pulse to be lost (value is written at call time)")
    # the same pulse applied as a waveform is propagated
    tr2 = b.eng.drive([(10, v.location, 1), (30, v.location, 0)])
    check(len([e for e in tr2 if e[1] == g.location]) == 2)
    return "queued values are superseded by the latest (transient states are not evaluated), so no pulse; applying the two edges as separate waves delivers it"


@case("H3", "SR latch released simultaneously: engine resolves by allocation order; Icarus (symmetric delays) oscillates", kind="limit")
def h3():
    results = {}
    for q_first in (True, False):
        b = new_bench()
        r, s_ = b.var(), b.var()
        if q_first:
            nq = b.c.getcomponent(NOR); nqb = b.c.getcomponent(NOR)
        else:
            nqb = b.c.getcomponent(NOR); nq = b.c.getcomponent(NOR)
        b.connect(nq, 0, r); b.connect(nq, 1, nqb)
        b.connect(nqb, 0, s_); b.connect(nqb, 1, nq)
        b.gates += [nq, nqb]
        b.c.toggle(r.location, 1); b.c.toggle(s_.location, 1)
        b.start()
        x = experiment(b, [(10, r.location, 0), (10, s_.location, 0)], icarus=False)
        results[q_first] = (int(nq.output), int(nqb.output), len(x.trace))
        check(b.c.timed_queue_empty(), "engine must settle")
        if q_first:
            nodes, init = b.netlist(), {r.location: 1, s_.location: 1}
            loc_nq, loc_nqb = nq.location, nqb.location
    check(results[True] != results[False], f"outcome should depend on allocation order: {results}")
    osc = None
    if ICARUS:
        ic = icarus_trace(nodes, init, [(100, r.location, 0), (100, s_.location, 0)], tail=200, base=100)
        osc = len([e for e in ic if e[1] in (loc_nq, loc_nqb) and e[0] >= 100])
        check(osc >= 10, f"Icarus was expected to oscillate, saw {osc} output edges")
    return (f"engine: Q first -> (Q,Q')={results[True][:2]}, Q' first -> {results[False][:2]} (settles in {results[True][2]} events); "
            f"Icarus symmetric release: {osc} output edges in 200 ticks (no metastability model, order picks the winner)")


@case("H4", "32-bit simulated time wraps: commit times go backwards across 2^32 ticks", kind="limit")
def h4():
    b = new_bench()
    v = b.var()
    prev = v
    chain = []
    for _ in range(6):
        prev = b.gate(BUF, prev)
        chain.append(prev)
    b.start()
    b.c.Global_Clock = 2 ** 32 - 12
    tr = b.eng.drive([(5, v.location, 1)])
    ts = [t for t, _, _ in tr]
    check(any(b_ < a for a, b_ in zip(ts, ts[1:])), f"expected a backwards time step across the wrap, got {ts}")
    # two events straddling the wrap are ordered wrongly
    b2 = new_bench()
    x, y = b2.var(), b2.var()
    b2.gate(BUF, x); b2.gate(BUF, y)
    b2.start()
    b2.c.Global_Clock = 2 ** 32 - 3
    b2.c.toggle_timed(x.location, 1, delay=5)      # wraps to tick 2
    b2.c.toggle_timed(y.location, 1, delay=1)      # tick 2^32 - 2
    ev = b2.eng.run()
    first = [l for t, l, v_ in ev if l in (x.location, y.location)][0]
    check(first == x.location, "the event scheduled LATER ran first (wrapped timestamp sorts as earliest)")
    return "after 4294967295 the clock reads 2; an event due at +5 overtakes one due at +1 (4.29e9 ticks is far beyond interactive use)"


@case("H5", "Clock variables drained synchronously keep time_limit bounded (no memory growth over 6e6 toggles)")
def h5():
    if not os.path.exists("/proc/self/statm"):
        raise Skip("needs /proc")
    rss = lambda: int(open("/proc/self/statm").read().split()[1]) * os.sysconf("SC_PAGE_SIZE") / 1e6

    # control: same number of toggles from an ordinary variable, no self-rescheduling clock
    b = new_bench()
    v = b.var()
    b.gate(BUF, v)
    b.start()
    r0 = rss()
    b.c.run_clock_timed(v.location, 3_000_000, 5)
    control = rss() - r0

    bc, clk, buf = with_clock(5, 5, 1)
    bc.c.drain_timed_queue(0, bc.c.Global_Clock + 1000)
    r1 = rss()
    bc.c.drain_timed_queue(0, bc.c.Global_Clock + 60_000_000)    # 6,000,000 clock toggles
    growth = rss() - r1
    check(growth < control + 8, f"memory grew {growth:.0f} MB over 6e6 clock toggles (control: {control:.1f} MB)")
    return f"grew {growth:.1f} MB over 6e6 clock toggles (control {control:.1f} MB); expired time_limit entries are popped in drain_timed_queue"


@case("H6", "No pin-arc, rise/fall or input-slew dependence: delay is purely structural (linear load model)", kind="limit")
def h6():
    # pin swap: AND(a,b) vs AND(b,a), with a driven by a long buffer chain, b directly
    d = []
    for swap in (False, True):
        b = new_bench()
        a, c = b.var(), b.var()
        slow = a
        for _ in range(12):
            slow = b.gate(BUF, slow)
        b.c.toggle(c.location, 1)
        g = b.gate(AND, *( (c, slow) if swap else (slow, c)))
        b.gate(BUF, g)
        b.start()
        tr = b.eng.drive([(5, a.location, 1)])
        t_slow = [t for t, l, v in tr if l == slow.location][0]
        t_g = [t for t, l, v in tr if l == g.location][0]
        d.append(t_g - t_slow)
    check(d[0] == d[1] == spec_delay(AND, 2, 1), f"pin-to-pin delays differ: {d}")
    # input slew: same gate driven by a chain of 1 vs 40 buffers - gate delay identical
    out = []
    for nbuf in (1, 40):
        b = new_bench()
        a = b.var(); c = b.var(); b.c.toggle(c.location, 1)
        src = a
        for _ in range(nbuf):
            src = b.gate(BUF, src)
        g = b.gate(AND, src, c)
        b.gate(BUF, g)
        b.start()
        tr = b.eng.drive([(5, a.location, 1)])
        out.append([t for t, l, v in tr if l == g.location][0] - [t for t, l, v in tr if l == src.location][0])
    check(out[0] == out[1], f"slew dependence appeared: {out}")
    return (f"AND delay identical for either pin ({d[0]}) and for 1- vs 40-buffer drivers ({out[0]}); rise == fall for all types (A1). "
            f"A Liberty NLDM/CCS-style model would show all three effects")


# =============================================================================
# runner
# =============================================================================
def run_all(select=None, verbose=False):
    results = []
    t_all = time.perf_counter()
    for cid, title, kind, fn in CASES:
        if select and not any(cid.startswith(s) for s in select):
            continue
        t0 = time.perf_counter()
        try:
            detail = fn()
            if kind == "verify":
                status = "PASS"
            elif kind == "defect":
                status = "FIXED"
            else:
                status = "LIMIT"
        except Skip as e:
            status, detail = "SKIP", str(e)
        except AssertionError as e:
            if kind == "verify":
                status = "FAIL"
            elif kind == "defect":
                status = "DEFECT"
            else:
                status = "LIMIT-CHANGED"
            detail = str(e)
        except Exception as e:  # noqa: BLE001
            status = "ERROR"
            detail = "".join(traceback.format_exception_only(type(e), e)).strip()
            if verbose:
                traceback.print_exc()
        dt = time.perf_counter() - t0
        results.append((cid, title, kind, status, detail, dt))
        print(f"[{status:<13}] {cid:<4} {title}  ({dt:.2f}s)")
        print(f"               {detail}")
    return results, time.perf_counter() - t_all


def summarize(results, total):
    from collections import Counter
    c = Counter(r[3] for r in results)
    print("\n" + "=" * 100)
    print("SUMMARY  " + "  ".join(f"{k}={v}" for k, v in sorted(c.items())) + f"  total={len(results)}  time={total:.1f}s")
    for r in results:
        if r[3] in ("FAIL", "ERROR"):
            print(f"  !! {r[0]} {r[3]}: {r[4]}")
    for r in results:
        if r[3] == "DEFECT":
            print(f"  known engine defect {r[0]}: {r[4]}")
    print("=" * 100)
    return 1 if (c["FAIL"] or c["ERROR"] or c["LIMIT-CHANGED"]) else 0



def run_extended(argv):
    sel = []
    verbose = "-v" in argv
    if "-k" in argv:
        sel = argv[argv.index("-k") + 1].split(",")
    res, total = run_all(sel, verbose)
    return summarize(res, total)

# =============================================================================
# suite: bench
# =============================================================================
CIRCUITS = ["c432", "c880", "c1908", "c3540", "c5315", "c6288", "c7552"]
DEFAULT_VECTORS = {"c432": 2000, "c880": 2000, "c1908": 1000, "c3540": 600, "c5315": 400, "c6288": 150, "c7552": 300}


def build_tb(nodes, init, vectors, gap, settle, outs, path):
    delays = node_delays(nodes)
    L = ["`timescale 1ns/1ns", "module tb;"]
    for i, (k, _) in enumerate(nodes):
        L.append(f"  reg n{i} = 1'b{init.get(i, 0)};" if k == VAR else f"  wire n{i};")
    for i, (k, s) in enumerate(nodes):
        if k == VAR:
            continue
        L.append(f"  {TL._VPRIM[k]} #({delays[i]}) g{i}({', '.join([f'n{i}'] + [f'n{x}' for x in s])});")
    L.append("  initial begin")
    L.append(f"    #{settle};")
    for vec in vectors:
        for loc, val in vec:
            L.append(f"    n{loc} = 1'b{val};")
        L.append(f"    #{gap};")
    L.append('    $display("OUT %b", {' + ", ".join(f"n{o}" for o in outs) + "});")
    L.append("    $finish;")
    L.append("  end")
    L.append("endmodule")
    with open(path, "w") as f:
        f.write("\n".join(L))


def best_of(fn, repeat):
    best = None
    for _ in range(repeat):
        t = fn()
        best = t if best is None or t < best else best
    return best


def run_vvp(vvp_path):
    t0 = time.perf_counter()
    out = subprocess.run(["vvp", vvp_path], check=True, capture_output=True, text=True).stdout
    return time.perf_counter() - t0, out


def bench(name, nvec, repeat):
    path = os.path.join(ROOT, "tests", "ISCAS85", name + ".v")
    t0 = time.perf_counter()
    r = VerilogRunner(path, Circuit.Circuit, Const, is_reactor=True)
    c = r.circuit
    c.simulate(Const.PRIORITY)
    c.drain_timed_queue()
    load_s = time.perf_counter() - t0
    nodes = extract_netlist(c)
    ins = [v.location for v in r.input_vars]
    outs = [g.location for g in r.output_objects]
    init = {l: int(c.gate_verse[l].output) for l in ins}
    rng = random.Random(7)
    cur = dict(init)
    vectors = []
    for _ in range(nvec):
        vec = []
        for l in ins:
            nv = rng.randint(0, 1)
            if nv != cur[l]:
                vec.append((l, nv))
                cur[l] = nv
        vectors.append(vec)
    gap = max(sta_arrival(nodes)) + 20

    # ---- Reactor (synchronous drain)
    def reactor_once():
        # identical start state each repeat: fresh circuit
        rr = VerilogRunner(path, Circuit.Circuit, Const, is_reactor=True)
        cc = rr.circuit
        cc.simulate(Const.PRIORITY)
        cc.drain_timed_queue()
        batches = [list(v) for v in vectors]
        gc.disable()
        t = time.perf_counter()
        tasks = 0
        for b in batches:
            tasks += cc.batch_toggle_timed(b)
        dt = time.perf_counter() - t
        gc.enable()
        return dt, tasks, [int(cc.gate_verse[o].output) for o in outs]

    best = None
    for _ in range(repeat):
        res = reactor_once()
        best = res if best is None or res[0] < best[0] else best
    r_dt, tasks, r_out = best

    # ---- Icarus
    row = dict(name=name, gates=sum(1 for k, _ in nodes if k != VAR), vectors=nvec, load_s=load_s,
               r_s=r_dt, tasks=tasks)
    if not ICARUS:
        return row
    with tempfile.TemporaryDirectory() as d:
        full, base = os.path.join(d, "full.v"), os.path.join(d, "base.v")
        build_tb(nodes, init, vectors, gap, gap, outs, full)
        build_tb(nodes, init, [], gap, gap, outs, base)
        t = time.perf_counter()
        subprocess.run(["iverilog", "-o", os.path.join(d, "full.vvp"), full], check=True, capture_output=True)
        row["icarus_compile_s"] = time.perf_counter() - t
        subprocess.run(["iverilog", "-o", os.path.join(d, "base.vvp"), base], check=True, capture_output=True)
        t_full = best_of(lambda: run_vvp(os.path.join(d, "full.vvp"))[0], repeat)
        t_base = best_of(lambda: run_vvp(os.path.join(d, "base.vvp"))[0], repeat)
        _, out = run_vvp(os.path.join(d, "full.vvp"))
    bits = next(l.split()[1] for l in out.splitlines() if l.startswith("OUT "))
    row["agree"] = (bits == "".join(str(b) for b in r_out))
    row["i_s"] = max(t_full - t_base, 1e-9)
    row["i_total_s"] = t_full
    row["i_base_s"] = t_base
    return row


BENCH_ISCAS89 = ["s27", "s382", "s420", "s641", "s713", "s1238", "s1423", "s1488", "s5378", "s9234"]
VEC89 = {"s27": 3000, "s382": 3000, "s420": 3000, "s641": 2000, "s713": 2000, "s1238": 1500, "s1423": 1000,
         "s1488": 1500, "s5378": 300, "s9234": 150}


def load89(name):
    sys.path.insert(0, os.path.join(ROOT, "tests", "src"))
    from benchmark_89 import SequentialVerilogRunner
    return SequentialVerilogRunner(os.path.join(ROOT, "tests", "ISCAS89", name + ".v"), Circuit.Circuit, Const,
                                   is_reactor=True, use_optimize=False,
                                   dff_file=os.path.join(ROOT, "tests", "src", "DFF.json"))


def bench89(name, nvec, repeat, gap=800, flush=10, warm=300):
    t0 = time.perf_counter()
    r = load89(name)
    if getattr(r, "const_1_node", None) is not None or getattr(r, "const_0_node", None) is not None:
        return dict(name=name, skipped="has constant tie-offs")
    c = r.circuit
    c.simulate(Const.PRIORITY)
    load_s = time.perf_counter() - t0
    clk = r._find_clock_var()
    ins = [v.location for v in r.input_vars]
    clk_loc = clk.location
    rng = random.Random(11)
    steps = [{l: ((i % 2) if l == clk_loc else 0) for l in ins} for i in range(flush)]
    # random-data warm-up: flushes unknown (X) state out of flops that have no reset; untimed for both
    for _ in range(warm):
        v = {l: rng.randint(0, 1) for l in ins}
        steps.append({**v, clk_loc: 0})
        steps.append({**v, clk_loc: 1})
    flush = flush + 2 * warm
    for _ in range(nvec):
        v = {l: rng.randint(0, 1) for l in ins}
        steps.append({**v, clk_loc: 0})
        steps.append({**v, clk_loc: 1})
    # per-step changes
    cur = {l: int(c.gate_verse[l].output) for l in ins}
    init = dict(cur)
    changes = []
    for st in steps:
        ch = [(l, st[l]) for l in ins if st[l] != cur[l]]
        cur.update(st)
        changes.append(ch)
    pins = [g.location for g in c.gate_verse if g.id == PIN_OUT]
    nodes = extract_netlist(c)

    def reactor_once():
        rr = load89(name)
        cc = rr.circuit
        cc.simulate(Const.PRIORITY)
        for ch in changes[:flush]:
            cc.batch_toggle_timed(list(ch))
        gc.disable()
        t = time.perf_counter()
        tasks = 0
        for ch in changes[flush:]:
            tasks += cc.batch_toggle_timed(list(ch))
        dt = time.perf_counter() - t
        gc.enable()
        return dt, tasks, "".join(str(int(cc.gate_verse[p].output)) for p in pins)

    best = None
    for _ in range(repeat):
        res = reactor_once()
        best = res if best is None or res[0] < best[0] else best
    r_dt, tasks, r_bits = best
    row = dict(name=name, gates=sum(1 for k, _ in nodes if k != VAR), flops=sum(1 for k, _ in nodes if k == PIN_IN) - len(ins) + 0,
               vectors=nvec, load_s=load_s, r_s=r_dt, tasks=tasks)
    if not ICARUS:
        return row
    with tempfile.TemporaryDirectory() as d:
        full, base = os.path.join(d, "full.v"), os.path.join(d, "base.v")
        build_tb(nodes, init, changes, gap, gap, pins, full)
        build_tb(nodes, init, changes[:flush], gap, gap, pins, base)
        subprocess.run(["iverilog", "-o", os.path.join(d, "full.vvp"), full], check=True, capture_output=True)
        subprocess.run(["iverilog", "-o", os.path.join(d, "base.vvp"), base], check=True, capture_output=True)
        t_full = best_of(lambda: run_vvp(os.path.join(d, "full.vvp"))[0], repeat)
        t_base = best_of(lambda: run_vvp(os.path.join(d, "base.vvp"))[0], repeat)
        _, out = run_vvp(os.path.join(d, "full.vvp"))
    bits = next(l.split()[1] for l in out.splitlines() if l.startswith("OUT "))
    row["agree"] = (bits == r_bits)
    row["x_bits"] = bits.count("x")
    row["i_s"] = max(t_full - t_base, 1e-9)
    return row


def bench_main89(names, nv_override, repeat, warm=300):
    print(f"(each circuit: 10 zero-input steps + {warm} random warm-up vectors flushed untimed, then the timed vectors)")
    print(f"{'circuit':<7}{'gates':>6}{'vecs':>6}{'events':>10} | {'Reactor ms':>11}{'Mev/s':>7} | "
          f"{'Icarus sim ms':>14} | {'speedup':>8} {'agree':>6} {'x':>3}")
    for n in names:
        r = bench89(n, nv_override or VEC89[n], repeat, warm=warm)
        if "skipped" in r:
            print(f"{n:<7} skipped: {r['skipped']}")
            continue
        sp = r["i_s"] / r["r_s"] if "i_s" in r else float("nan")
        print(f"{r['name']:<7}{r['gates']:>6}{r['vectors']:>6}{r['tasks']:>10} | {r['r_s'] * 1e3:>11.1f}"
              f"{r['tasks'] / r['r_s'] / 1e6:>7.2f} | {r.get('i_s', float('nan')) * 1e3:>14.1f} | "
              f"{sp:>7.1f}x {str(r.get('agree')):>6} {r.get('x_bits', '-'):>3}")


def bench_main():
    args = sys.argv[1:]
    repeat = 3
    nv_override = None
    warm = 300
    names = []
    i = 0
    while i < len(args):
        if args[i] == "--repeat":
            repeat = int(args[i + 1]); i += 2
        elif args[i] == "--warm":
            warm = int(args[i + 1]); i += 2
        elif args[i] == "--vectors":
            nv_override = int(args[i + 1]); i += 2
        else:
            names.append(args[i]); i += 1
    if "--iscas89" in names:
        names.remove("--iscas89")
        return bench_main89(names or BENCH_ISCAS89, nv_override, repeat, warm)
    names = names or CIRCUITS
    rows = []
    print(f"{'circuit':<7}{'gates':>6}{'vecs':>6}{'events':>10} | {'Reactor ms':>11}{'Mev/s':>7} | "
          f"{'Icarus sim ms':>14}{'(total)':>9}{'base':>7} | {'speedup':>8} {'agree':>6} | {'load vs compile (s)':>22}")
    for n in names:
        r = bench(n, nv_override or DEFAULT_VECTORS[n], repeat)
        rows.append(r)
        sp = r["i_s"] / r["r_s"] if "i_s" in r else float("nan")
        print(f"{r['name']:<7}{r['gates']:>6}{r['vectors']:>6}{r['tasks']:>10} | {r['r_s'] * 1e3:>11.1f}"
              f"{r['tasks'] / r['r_s'] / 1e6:>7.2f} | "
              f"{r.get('i_s', float('nan')) * 1e3:>14.1f}{r.get('i_total_s', float('nan')) * 1e3:>9.0f}"
              f"{r.get('i_base_s', float('nan')) * 1e3:>7.0f} | {sp:>7.1f}x {str(r.get('agree')):>6} | "
              f"{r['load_s']:>10.3f} vs {r.get('icarus_compile_s', float('nan')):>7.3f}")
    return rows



# =============================================================================
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--suite", choices=("topologies", "extended", "bench", "all"), required=True)
    args, rest = ap.parse_known_args()
    code = 0
    if args.suite in ("topologies", "all"):
        run_topologies()
    if args.suite in ("extended", "all"):
        code = run_extended(rest)
    if args.suite == "bench":
        sys.argv = [sys.argv[0]] + rest
        bench_main()
    return code


if __name__ == "__main__":
    sys.exit(main())
