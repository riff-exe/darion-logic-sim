# Darion Logic Sim: Comprehensive Timing Verification & Delay Architecture Report

Empirical stress-testing, delay-model analysis, and failure mode differentiation for the Reactor Priority Queue simulation engine.

---

## Executive Summary

The Reactor simulation engine was subjected to a comprehensive 22-topology timing verification and delay stress-testing suite in `tests/test_timing.py --suite topologies`. The suite validates propagation delays, reconvergent fan-out hazards, inertial pulse rejection, setup and hold timing margins, dynamic capacitive loading, and industrial benchmark netlists up to 2,480 gates. A second, independently-checked suite (`tests/test_timing.py --suite extended`, Section 6) establishes how exact the model is, where it deviates from a reference simulator, and where its scope ends.

```
=======================================================================================================================================
EXECUTIVE VERDICT SUMMARY:
  - Timing Failure Modes Reproduced (qualitative)                       : 6
  - Engine Defects Detected by These 22 Topologies (see extended suite) : 0
  - Circuits Passing Functional Spec under Timing Limits                 : 15
  - Analog Physical Boundaries Isolated (SPICE Required)                : 1
  Total Circuits / Topologies Evaluated                                  : 22
  Total Execution Time                                                   : 0.02 seconds
=======================================================================================================================================
```

### Simulator Timing & Verification Rating

| Evaluation Dimension | Result | Technical Assessment |
| :--- | :--- | :--- |
| **Delay Model** | **Exact for its model** | Linear load-dependent delay: intrinsic delay + fan-in port load (`reserved`) + fan-out load (`hitlist.size`). Measured delays equal the formula on all 156 gate/fan-in/fan-out combinations (extended suite A1). Not calibrated to a real cell library; no rise/fall, pin-arc or slew dependence. |
| **Timing-Failure Reproduction** | **Qualitative, at predicted thresholds** | Reproduces 6 canonical timing-failure modes (glitch-clocked DFF, setup/hold overclocking, wave collision, ripple decoder spikes, clock skew race-through, ring oscillator lockup). Thresholds follow from component measurements (for example the T-flip-flop minimum period and the skew race boundary). Not validated against silicon or SPICE. |
| **Benchmark Agreement** | **100% on settled values; event-for-event vs Icarus** | Settled values equal a zero-delay reference on 7 ISCAS-85 circuits up to 2,480 gates (c6288), and the extended suite matches Icarus Verilog gate-level inertial simulation event for event on all nets outside same-tick tie cones. |
| **Inertial Delay Glitch Absorption** | **Verified ($O(1)$)** | Pulses shorter than a gate's delay are discarded in-place via $O(1)$ timestamp invalidation. Rejection threshold swept in extended suite B1. |
| **Test Harness Timing Mechanics** | **Exact at tick resolution** | Clock pulses and input waveforms land on exact integer ticks. Time has no stated physical unit and no sub-tick resolution. |

---

## 1. Circuit Failure vs. Simulator Defect

In Electronic Design Automation (EDA), confusing a **circuit timing failure** with a **simulator software bug** is a fundamental error. Differentiating them is critical:

| Dimension | Circuit Timing Failure (`HARDWARE FAIL` in the test output) | Simulator Defect (`ACTUAL FAIL`) |
| :--- | :--- | :--- |
| **What Broke?** | **The circuit under test** violates a timing constraint. | **The simulator software** broke in C++/Cython code. |
| **Simulator Role** | Models propagation delays, setup/hold constraints and race conditions, and shows the resulting misbehaviour. | **Software Defect**: Violated discrete-event semantics, corrupted event queues, or mismanaged state. |
| **Zero-Delay Simulators** | Pass these circuits, because they ignore delays. | Would hang, crash or give wrong results. |
| **Hardware Expectation** | A fabricated chip would be expected to misbehave in a similar way (qualitative; not validated against silicon). | A flaw in the simulator code that misrepresents the model. |
| **Fix Required** | Fix the circuit schematic (add pipeline registers, balance clock trees, filter glitches). | Fix the engine code in `reactor/Circuit.pyx` or `reactor/Profile.h`. |

### Why Reproducing Timing Failures Matters

If an engineer designs a sequential circuit with 6 buffers of clock skew, or clocks a feedback loop whose minimum clock period is 39 ticks with a 20-tick ring oscillator:
1. **In a zero-delay simulator:** The circuit reports `PASS`, which hides the problem until the circuit is built.
2. **In Reactor (timed priority queue):** The simulator models load-dependent propagation delays, exposes the hold-time violation, and corrupts the register state.

Reproducing these failures shows that the delay model captures hazards and timing violations that zero-delay simulation cannot see. It is not a substitute for silicon measurement, SPICE, or sign-off timing analysis.

---

## 2. Dynamic Electrical Loading: Fan-In & Fan-Out Degradation

Rather than a fixed delay per gate, Reactor implements a **load-dependent delay model** (intrinsic delay plus fan-in and fan-out terms) directly in Cython.

### Engine Implementation (`reactor/Circuit.pyx`)

From `reactor/Circuit.pyx`:
```python
# Gate delay parameters:
# Index:      0(AND), 1(NAND), 2(OR), 3(NOR), 4(XOR), 5(XNOR), 6(BUF), 7(NOT), 8(PIN_IN), 9(VAR), 10(PIN_OUT), 11(IC)
g_delay[:] =  [3,     2,       3,     2,      4,      4,       2,      1,      0,         0,      0,           0]
fi_delay[:] = [1,     1,       2,     2,      2,      2,       0,      0,      0,         0,      0,           0]
fo_delay[:] = [1,     1,       1,     1,      2,      2,       1,      1,      1,         0,      1,           0]
```

Event calculation in `reactor/Circuit.pyx`:
```python
calc_time = self.Global_Clock + self.Global_delay[target.type] + (self.FanIn_delay[target.type] * target.reserved) + (self.FanOut_delay[target.type] * target.hitlist.size)
```

The dynamic delay equation executed on every gate is:
```
total_delay = Global_delay[type] + (FanIn_delay[type] * fan_in) + (FanOut_delay[type] * fan_out)
```

This has the same linear form as the simplest load-dependent cell-delay models:
```
t_delay = t_intrinsic + (k_in * FanIn) + (k_out * FanOut)
```

Commercial Liberty libraries (NLDM/CCS) additionally index delay by input slew and output load and distinguish rise/fall and pin-to-pin arcs. This model does not: delay is purely structural (extended suite H6), and the coefficients are not calibrated to a real library.

### Empirical Proof

* **NOT Gate with Fan-Out = 1:**
  `delay = 1 (intrinsic) + 0 (fan-in) + 1 * 1 (fan-out) = 2 ticks`
  Sinks toggle at `t = 2`.
* **NOT Gate with Fan-Out = 8:**
  `delay = 1 (intrinsic) + 0 (fan-in) + 1 * 8 (fan-out) = 9 ticks`
  Sinks toggle at `t = 11` (9 ticks for gate + 2 ticks for buffers).

The gate driving 8 loads is **7 ticks slower** purely due to fan-out loading in the delay model.

---

## 3. Physical Driver Model: Waves as Physical Transients & State Supersession

In physical hardware (silicon, PCB traces, transistor drains):
1. **A Wire Has Only One Active Potential: "Now" (`V(t_now)`)**:
   A physical wire cannot hold future commitments. You cannot tell a physical wire at `t = 0`: *"Be 1 at t = 10, and be 0 at t = 20."*
   A function generator or driver transistor actively applies voltage at `t = 10`, and pulls it to ground at `t = 20`.
2. **Superseding Old Transient States**:
   Before the next wave, all intermediate logic levels across the circuit are transient. If an input driver transitions again while a previous disturbance is in flight, the active physical driver potential **supersedes** prior transient states. The latest driver state takes physical precedence.
3. **Waves Are Transient Electrical Responses**:
   When an input transitions, electrons charge and discharge downstream gate capacitances. That ripple through logic gates is a transient wavefront in flight.
4. **UI Synchronization at Wave Boundaries**:
   Darion Logic Sim's interactive canvas renders the settled state at the end of each wave. Intermediate logic levels are transient; downstream circuits evaluate and settle before the UI updates the display frame. Sequential pulse sequences (e.g. clock signals) naturally execute as a sequence of waves (as implemented in `run_clock_timed`).

---

## 4. Detailed Breakdown of the 22 Evaluated Topologies

### Category 1: Timing Failure Modes Reproduced

1. **Dynamic Hazard Clock Trigger (Test 7):**
   * *Topology:* Reconvergent fan-out (5 inverters on slow path) driving an AND gate connected to a DFF clock input.
   * *Timing Defect:* Reconvergent delay creates a 10-tick dynamic hazard pulse (3 inverters give 6 ticks, which is filtered).
   * *Resulting Behaviour:* The pulse exceeds the flip-flop's 7-tick minimum clock pulse width. The clock fires spuriously, corrupting stored memory `Q` from 0 to 1.
2. **Setup/Hold Overclocking Violation (Test 8):**
   * *Topology:* T-Flip-Flop (DFF + XOR feedback), minimum working clock period = 39 ticks.
   * *Timing Defect:* Driven with an overclocked clock period of 16 or 24 ticks.
   * *Resulting Behaviour:* Feedback data arrives after the clock edge (setup violation). Counter suffers lost/corrupted toggles (`[1, 1, 1, 1, 0, 0]`) instead of `[1, 0, 1, 0, 1, 0]`.
3. **Unregistered Combinational Wave Collision (Test 10):**
   * *Topology:* ISCAS-85 `c432` (203 gates, longest structural path = 151 ticks).
   * *Timing Defect:* Vector 1 injected at `t = 50` ticks without pipeline registers while Vector 0 is still in flight.
   * *Resulting Behaviour:* Fast paths of Vector 1 overtake slow paths of Vector 0. Output sampled at `t = 150` yields `[1, 1, 1, 1, 1, 1, 1]` instead of `[1, 0, 1, 1, 0, 0, 0]`.
4. **Asynchronous Ripple Counter Decoded Bus Glitch (Test 12):**
   * *Topology:* 2-bit asynchronous ripple counter driving a 2-to-4 decoder.
   * *Timing Defect:* When counting 1 -> 2, Q0 falls before Q1 rises due to flip-flop propagation delay.
   * *Resulting Behaviour:* A transient false state `(0, 0)` persists for 9 ticks. Channel Y0 emits a false pulse on the bus, momentarily double-selecting bus lines `[0, 1, 0, 1]`.
5. **Pipeline Clock Skew Race-Through (Test 13):**
   * *Topology:* 2-stage shift register with 6 buffers of clock skew on DFF2's clock line.
   * *Timing Defect:* Clock edge arrives at DFF2 after DFF1 has already latched and presented its new output.
   * *Resulting Behaviour:* Hold time violation causes data to race through two pipeline stages in a single clock cycle (`Q1 = 1, Q2 = 1`).
6. **Ring Oscillator Natural Overclocking Lockup (Test 16):**
   * *Topology:* 3-gate ring oscillator (natural period = 20 ticks) driving a T-Flip-Flop (minimum working clock period = 39 ticks).
   * *Timing Defect:* The ring oscillator's frequency exceeds the sequential feedback bandwidth.
   * *Resulting Behaviour:* Counter skips edges and outputs `[0, 0, 0, 1]` instead of `[1, 0, 1, 0]`.

---

### Category 2: Functional & Timing Specification Met (Settled Values Match the Zero-Delay Reference)

1. **Inverter Chain Propagation Delay (Test 1):** 4-stage NOT chain propagates sequentially in 11 ticks (accounting for capacitive fan-out loading from attached probe buffers: 3 ticks for intermediate stages + 2 ticks for the final stage); probes confirm discrete step delays.
2. **4-Bit Ripple Carry Adder (Test 2):** Full carry-chain ripple latency verified; sums settle to `[0, 0, 0, 0]` with Cout = 1.
3. **Dynamic Hazard Glitch Detection (Test 3):** Reconvergent AND gate captures transient 6-tick pulse, cleanly settling to static 0.
4. **Static-1 Hazard MUX 0-Dip (Test 4):** 2-to-1 MUX captures transient 8-tick 0-dip during select line transition, settling to static 1.
5. **SR NOR Latch Pulse Filtering (Test 5):** Rejects sub-threshold pulses (< 8 ticks); sets cleanly on valid pulses (>= 8 ticks).
6. **Master-Slave DFF Clock Width (Test 6):** Sub-threshold clock pulses (< 7 ticks) are rejected; valid pulses (>= 7 ticks) latch data.
7. **ISCAS-85 Benchmark Suite (Test 9):**
   * `c17` (13 gates): Max latency 17 ticks — 100% bit-exact match across 20 vectors.
   * `c432` (203 gates): Max latency 105 ticks — 100% bit-exact match across 10 vectors.
   * `c499` (275 gates): Max latency 127 ticks — 100% bit-exact match across 10 vectors.
   * `c880` (469 gates): Max latency 113 ticks — 100% bit-exact match across 10 vectors.
   * `c1355` (619 gates): Max latency 141 ticks — 100% bit-exact match across 10 vectors.
   * `c1908` (938 gates): Max latency 132 ticks — 100% bit-exact match across 10 vectors.
   * `c6288` (2,480 gates, 16-bit multiplier): Max latency 670 ticks — 100% bit-exact match across 5 vectors.
8. **Wave-Synchronized Multi-Pulse Transitions (Test 11):** Sequential wave pulses propagate and settle bit-exact before UI frame boundaries. Because intermediate states within a wave are transient, new driver states supersede older transient states, and each wave settles completely before the next wave begins.
9. **Latch Simultaneous-Release Tie-Break (Test 14):** There is no metastability model. A symmetric latch released at one tick is resolved deterministically by gate allocation order (`gate_loc`), so the winner depends on creation order. A reference simulator with equal delays (Icarus) oscillates instead (extended suite H3).

---

### Category 3: Analog Physical Boundaries (SPICE Required)

1. **Capacitive RC Charge Integration (Test 15):**
   * *Discrete-Event Model:* Memoryless inertial delay drops sub-threshold pulses independently, providing clean digital noise filtering.
   * *Analog SPICE Domain:* A high-frequency pulse train continuously injects charge into load capacitance (`Q = C * V`), gradually crossing the switching threshold voltage (`V_th`). Continuous RC differential equations are outside discrete-event simulation scope.

---

## 5. Verification Execution Instructions

To execute the complete 22-topology timing verification suite:

```bash
python tests/test_timing.py --suite topologies
```

### Verified Runtime Metrics
* **Total Execution Time:** 0.02 seconds (20 milliseconds).
* **Memory Footprint:** Priority queue memory stays bounded (including synchronous draining of clock variables, which pops expired `time_limit` entries; no growth over 6×10⁶ clock toggles in `tests/test_timing.py --suite extended`, case H5).
* **Exit Code:** 0 (Clean exit, zero unhandled exceptions).

---

## 6. Extended Verification (`tests/test_timing.py --suite extended`)

```bash
python tests/test_timing.py --suite extended          # about 5 seconds; add -k E to run one tier
```

44 cases in tiers A to H. Every expectation is derived independently of the engine: the documented delay formula, a pure-Python reference simulator, Icarus Verilog gate primitives with the same per-gate delays, and structural path sums or static timing analysis. Four deliberately broken engine builds (inertial rejection off, fan-out term dropped, same-tick order reversed, the old `inputlimit` fan-in term) are each caught by the suite.

### What is established

* **Delay formula:** exact on 156 gate-type x fan-in x fan-out combinations, rise and fall.
* **Structures:** ripple-adder latency equals the structural path sum and is exactly linear in width (4 to 64 bits); ring-oscillator period is exactly linear in stage count and load; Kogge-Stone scales logarithmically.
* **Benchmarks:** about 95,000 committed events on ISCAS-85 equal the reference simulator exactly; 28,679 were also compared event for event with Icarus on nets outside same-tick tie cones. ISCAS-89 s27, s382 and s1423 match the zero-delay reference above sharp minimum clock half-periods of 60, 40 and 120 ticks.
* **Flip-flop timing:** one sharp capture boundary per polarity (setup 4 and 6 ticks for D rising and falling); clock-to-Q is flat and then rises one tick per tick of D lateness near the boundary (time borrowing).
* **Composition:** the toggle flip-flop minimum period (29 ticks) equals `(cq_r + cq_f + 2*d_loop + K_r + K_f) / 2` from separate component measurements, and the clock-skew race boundary matches its prediction at all 15 skew values.
* **Glitch activity:** committed transitions per functional transition are about 11x on c6288 versus about 1.0 to 2.1x on the other ISCAS-85 circuits.
* **Memory:** the synchronous drain no longer grows the `time_limit` queue (fixed; verified by case H5).

### Known deviations and limits

* **Same-tick tie-break:** when two different nets change in one tick, the engine applies them in `gate_loc` order, a deterministic stand-in for physical skew. An evaluate-once-per-tick reference (and Icarus) can differ: 4 of 1,440 random ISCAS vectors on c1908, c2670 and c3540, and 1 of 68 tie-free random circuits. Settled values are always correct. A pulse exactly as wide as a gate's delay is likewise accepted or rejected by allocation order.
* **Duplicate pins (known defect B8):** a net driving two pins of one gate is updated pin by pin, which can retime a pending output event. It is rare and has no effect on settled values.
* **Linear load model:** no rise/fall, pin-to-pin or slew dependence, and coefficients not calibrated to a cell library.
* **No analog behaviour:** no metastability, no RC charge integration (Test 15), no wire delay.
* **Capacity:** gates support up to 255 inputs (enforced by the engine: `Gate.setlimits` rejects larger sizes and the JSON loader raises; test H1); simulated time is 32-bit and wraps after 2^32 ticks; a clock with both phases 0 does not advance simulated time.
* **Hierarchy:** an IC's pin gates add delay (the IC form of the D-FF has a clock-to-Q 4 ticks slower than the same flop built from plain gates).

### Claim boundary

Supported: an exact, deterministic, load-dependent discrete-event delay simulator that agrees with Icarus gate-level inertial simulation, and reproduces hazards, setup windows, minimum clock periods and clock-skew races at their predicted values.

Not claimed: agreement with real silicon or SPICE, calibration to a cell library, sign-off-quality timing, or analog and metastability behaviour.
