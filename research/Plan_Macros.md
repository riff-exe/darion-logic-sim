# Plan: macros (P2)

Status: design for discussion (2026-10-22). Nothing implemented. Engine change, the author implements; this document is the working plan and the list of open issues. Line numbers refer to the tree as of 2026-10-22. Companion plan: `Plan_Packed_Hitlists.md` (P1); section 9 lists where the two touch.

## 1. Goal and scope

A macro is a native block (C++ behaviour, one object) that stands in for a gate-level subcircuit: a flip-flop, a register, a RAM, a ROM, a bus multiplexer. It exists for three reasons:

1. **Size.** A gate-level DFF is 10 gates (`DFFSR.json`, 2 NOT + 8 NAND, master-slave); a 1 KiB RAM is not feasible at gate level. Course circuits (registers, counters, RAM, ROM, simple CPUs) need memory.
2. **Glitches and repeated work.** A gate-level block re-evaluates on every input flip in every wave. A macro evaluates once per trigger and can be deferred until its inputs have settled.
3. **Observability.** Darion's point is that you can read any gate. A macro keeps that: its state (a register value, a RAM word) is readable and writable through the API.

Build order (agreed): DFF first, then RAM/ROM, then bus. The OOP engine (`reactor_oop/`) and the Python engine (`engine/`) get no macros; the Claim 13 benchmarks keep running on circuits without macros.

Not in scope: high-impedance (Z) states (the bus macro is a multiplexer, no tri-state), native flop evaluation inside the gate loop (the removed flop-cut experiment), macro behaviour written in Python (decided against, 2026-10-22: no GIL in the loop, no deferred Python evaluation).

## 2. Engine facts the design rests on

From reading `reactor/` (2026-10-22):

* **Eager target evaluation.** All three loops (`propagate` [Circuit.pyx:1475](../reactor/Circuit.pyx#L1475), `sweep` [1545](../reactor/Circuit.pyx#L1545), `complete_task` [1409](../reactor/Circuit.pyx#L1409)) evaluate each target inside the source's edge loop (`target.evaluate()`) and queue it only if its output changed and it is not already `FLAG_MARK`ed. A gate that flips twice in one wave is queued once and pops with its final value.
* **The pop.** `propagate` pops a gate, clears `MARK`, pushes it to the visual queue, walks its hitlist (lines 1494-1520). `sweep` does the same in Phase 1 (1567) and Phase 2 (1605). `complete_task` drops stale tasks (`task.time < gate_clocks[origin]`, 1427), handles clocks (`VARIABLE` with `inputlimit == INFINITE`, 1433), then walks the hitlist. These are the three dispatch points for macros.
* **Quiescence.** `propagate` ends when a wave produces no changed gate (`while end_point > 0`, 1494); after `wave_limit` waves it moves the remaining gates to the timed queue (oscillation fallback, 1527-1540). `sweep` ends after Phase 2 and hands back edges to `propagate` (1640).
* **Seeding.** `simulate()` ([1335](../reactor/Circuit.pyx#L1335)) seeds the queue with every `VARIABLE` only. `reset()` ([1386](../reactor/Circuit.pyx#L1386)) resets gates and ICs through Python objects.
* **Sort.** `_topological_sort` ([823](../reactor/Circuit.pyx#L823)) follows hitlist edges; `FLAG_BOUNDARY` (bit 7) targets are skipped for in-degree (lines 856-956), which is how flop outputs break cycles today (set in `IC.pyx:90,158` by an IC-name heuristic: dff, flip, latch, tlat).
* **Types.** `AND 0 .. IC 11`, `TOTAL 12`, `DEAD 255` ([Const.pxd:24-40](../reactor/Const.pxd#L24-L40)); delay arrays are sized `[12]` ([Circuit.pyx:45-58](../reactor/Circuit.pyx#L45-L58)); `Store.namelist` and `retype`'s bound (`>= IC_ID`) also depend on the count.
* **Free bits.** Flags bits 4-6 are unused; `hitlist.data` is unused when `size = capacity = 0`.
* **Gate vector moves.** `Store.get` ([Store.pyx:44-64](../reactor/Store.pyx#L44-L64)) doubles `gate_infolist` past the 500k reservation and fixes every `profile.target` and `Gate.info` by `diff`. Any other `CPP_Gate*` held elsewhere (for example by a macro) would dangle.

## 3. Design

### 3.1 Pieces

| Piece | What it is | Where it lives |
|---|---|---|
| macro gate | `MacroGate(Gate)`, type `MACRO_GATE_ID` (XOR seed 1, mask 1): a gate whose evaluation is done by its core; fields `kind`, `params`, `outs` | the gate array; `hitlist.data = MacroCore*`, `size = capacity = 0` |
| inputs | the macro gate's ordinary sources, in pin order, each with a real edge (any input change queues it; `eval` returns early when nothing relevant changed) | sources' hitlists |
| output gates | type `MACRO_OUT_ID`: no source, `inputlimit = 0` (`logic` stays 0, so `compute()` returns the flag bit), written only by the core | the gate array; ordinary hitlists to their fan-out |
| `MacroCore` | C++ base class (`Macro.h`): input/output locations, memory, virtual `eval` overridden per kind | heap, owned by `Circuit`, never moves |
| packaging | `make_macro(kind, params)` wraps macro gate and output gates in an ordinary IC (pins) so the UI draws a block; packaging only, flattening keeps the macro gate and output gates | `objlist[IC_ID]` |

### 3.2 `MacroCore`: C++ base class with a virtual `eval` (decided 2026-10-22)

All macros share the same data; the only thing that differs per kind is `eval`. Written in C++ in a new `reactor/Macro.h` next to `Profile.h`, declared to Cython as `extern` (as `CPP_Gate` is):

```cpp
struct EvalCtx { CPP_Gate** write_queue; Py_ssize_t* size; /* commit/dirty lists */ };

struct MacroCore {
  uint8_t   sequential;        // commit rule (3.6), sort rule (3.9)
  uint16_t  n_in, n_out;
  int*      inputs;            // source locations (the macro gate's _sources), pin order
  int*      outputs;           // output gate locations (outs)
  uint32_t  n_mem;
  uint8_t*  memory;            // [0, n_in): previous value of each input (0/1/X)
                               // [n_in, n_in + n_out): staged outputs
                               // [n_in + n_out, n_mem): extra storage, only if the kind asks (RAM words, ROM image)

  MacroCore(uint16_t n_in, uint16_t n_out, uint32_t n_extra, uint8_t sequential);
  virtual ~MacroCore();                                     // frees inputs, outputs, memory
  virtual void eval(CPP_Gate* G, EvalCtx& c) noexcept = 0;  // the one per-kind difference
  void reset() noexcept;                                    // generic (below)
  void commit(CPP_Gate* G, EvalCtx& c) noexcept;            // staged -> output gates, queue the changed ones
};

// each kind: struct DFF : MacroCore { void eval(CPP_Gate*, EvalCtx&) noexcept override; };  (added per kind, not part of the infrastructure)
```

* The loop calls `(<MacroCore*>info.hitlist.data).eval(gate_infolist, ctx)`; Cython calls virtual methods of `extern` C++ classes nogil.
* **Memory is the previous state (author, 2026-10-22).** By default it is one byte per input, holding that input's value from the last evaluation, so every input gets edge detection for free (`memory[i] = 0` and current `1` is a posedge on input `i`). A flop's own state needs no memory: it is the value of its output gates. Only kinds that hold more than that (RAM, ROM) ask for extra storage.
* **Sizes come from the pins.** `n_in` and `n_out` are fixed at creation; many kinds derive their width from them (RAM: data width `= n_out`, address width `= n_in - 2 - n_out`; adder: width `= n_out - 1`), so `params` shrinks to the extra-memory size where it is needed at all.
* `reset` is generic: the previous-input and staged areas to X; extra storage kept for ROM, cleared or kept for RAM (issue 6). Output gates go to X through `Gate.reset`, which is the flop's reset state.
* Freed with `delete` (virtual destructor) in `clearcircuit` and `__dealloc__`.
* **Kind table** (read once at creation): `kind -> pin names, sequential, extra memory size, constructor` (a small C++ factory `MacroCore* make_core(kind, ...)` or a Cython dict of constructors). Adding a kind = one subclass + one table entry.

**Locations, not pointers, inside the macro.** The pointer-versus-index measurement (`Index_vs_pointer.md`) is about the per-edge inner loop; a macro is visited once per trigger and does far more work per visit, so a base-plus-index load is noise. Locations survive the gate-vector growth in `Store.get` with no fix-up loop; after `optimize()` `sync_core` refills them from the macro gate's `_sources` and `outs`. The one pointer that stays is `MacroCore*` in the macro gate, and cores never move.

The indirect call is the dispatch the paper argues against for gates, but it runs once per macro trigger, not once per edge, so it costs nothing measurable; say so in the paper if macros are mentioned.

### 3.3 The macro gate

* Type `MACRO_GATE_ID` (decided 2026-10-22): its own gate type with XOR's seed and mask (`seed = 1`, `mask = 1`, set in `Store.get` before the `choice >= BUFFER_ID` branch, which would otherwise catch it). Every trigger change flips the macro gate's output, so the existing loops queue it exactly like a gate whose output changed. If two triggers change in one wave the macro gate is still queued once (MARK), and the macro reads the real pin values on pop, so the macro gate's own output value is never used.
* How it enters the queue, step by step: a trigger source pops, walks its hitlist, reaches the macro gate's `Profile`, updates `macro gate.logic` and calls `macro gate.evaluate()` (the existing inner loop, no change). XOR parity flips on any single input change, so `target_output != target.output` holds and the macro gate is appended to `write_queue` and `MARK`ed. It is in the next `read_queue`. The macro gate's output value means nothing and nothing reads it (it has no fan-out); it is only a change detector that reuses the queueing rule. UNKNOWN works the same way (known -> UNKNOWN and back are both changes).
* Own type rather than XOR plus a flag: no flag bit spent, dispatch tests the type byte, and the timed-mode delay is simply `Global_delay[MACRO_GATE_ID] = 0` with no special case. Costs: `TOTAL` grows to 13 (delay arrays, `namelist`), `retype` must refuse it (its bound is `>= IC_ID`, so it already does).
* `inputlimit = 0` once all inputs are connected; an unconnected input keeps `inputlimit > 0`, the macro gate reads UNKNOWN and never fires, like any gate with a floating input.
* `hitlist`: `data = MacroCore*`, `size = capacity = 0`. `begin() == end()`, so the loops never walk it. `connect` must refuse a macro gate as a source; P1's `pack_gate` carries `data` for empty lists.
* `Profile.index` is `uint8_t`, so a macro gate has at most 256 inputs (a RAM with 8-bit address and data: 18; a 32-bit ALU: about 70).

### 3.4 Dispatch (one type test per pop, not per edge)

Decided (author, 2026-10-22): the macro runs during the read-queue wave, at the point where the macro gate would walk its edges. The macro gate's edge walk is replaced by the macro call; the macro gets the current `write_queue` and `size`, writes its output gates and appends the changed ones, so their fan-out runs in the next wave like any gate's. No separate macro queue.

In each pop site, right after `flags &= ~FLAG_MARK`:

```cython
if unlikely(self_info.type == MACRO_GATE_ID):
    m = <MacroCore*>self_info.hitlist.data
    m.eval(m, gate_infolist, &ctx)
    continue
```

Sites: the `propagate` pop (around line 1497), `sweep` Phase 1 (1569) and Phase 2 (1606), `complete_task` (after the stale-task check, 1427), and the oscillation fallback (1527) which only reschedules and needs no change. Cost for circuits without macros: one predictable, never-taken branch per popped gate. This must be measured (7.3) because Claim 13 numbers come from the same loops.

### 3.5 Output gates

* Type `MACRO_OUT_ID` (not `IC_OUTPUT_PIN`, which `build_ic` removes): no source and `inputlimit = 0`, so `logic` stays 0 and `compute()` returns the flag bit; `eval` writes `output` directly (0/1/X) and queues the gate if it changed. `Gate.reset` leaves `inputlimit` and `mask` alone (checked, [Gates.pyx:266](../reactor/Gates.pyx#L266)), so the setup survives `reset()`.
* Nothing may drive them but the macro: `Gate.connect` must refuse them as targets (as it returns early for `VARIABLE` targets, [Gates.pyx:235](../reactor/Gates.pyx#L235)).
* They are ordinary sources: their fan-out is a normal hitlist, packed by P1, walked by the hot loops with no change.
* **Zero connectivity.** Seen from the gate graph an output pin has no inputs. Anything that walks the graph backwards (sort roots, geometry, the UI's "driven by") asks the owning macro gate (`outs`).

### 3.6 Nonblocking commit (the shift-register race)

**Problem.** Two DFF macros in a shift register, both clocked by the same edge. The clock pops, both macro gates are queued in the next wave. Stub A pops first, samples D, writes Q_A. Stub B pops later in the same wave and samples D_B = Q_A, which is already new. B captures the wrong value. Gate-level flops do not have this problem in the same way because their master-slave structure is real logic; macros must supply the semantics themselves. Verilog solves it with the nonblocking-assignment region: all flops sample before any of them updates.

**Within the dispatch of 3.4** the race sits in one place: the macro writing an output gate's `output` during the read-queue wave, while a later macro gate in the same `read_queue` reads it as data. Options, cheapest first:

* **(i) stage, publish at the end of the wave.** The macro writes the new value to the staged area of `memory` only (not `FLAG_VALUE`, which cannot hold X, 3.10) and records the macro; after the `for index in range(end_point)` loop, before the buffer swap, one pass copies `staged` to the output pins and appends the changed ones to `write_queue`. Fixes flops clocked in the same wave. Does not fix clock skew: a flop whose clock arrives one wave later (a deeper buffer chain) sees the new Q.
* **(ii) commit at quiescence** (below). Fixes skew too; costs a commit list and an outer loop in `propagate`.

**Proposed rule (ii).** Sequential macros sample at pop and write to `staged`, setting `MF_STAGED` and appending themselves to a per-circuit `commit_list`. Staged values become visible only when the active work has drained:

| Mode | When `commit_list` is applied |
|---|---|
| propagate | when a wave produces nothing (`end_point == 0`): for every staged macro, write `staged` to its output gates, queue the changed ones, clear the list, continue `propagate`; stop when both are empty |
| sweep | after Phase 2 and its back-edge `propagate` (1640), the same commit loop, then `propagate` for whatever changed |
| timed | outputs scheduled at `t + D` (D >= 1, from the macro's delay entry) as `Task`s on the output gates; `gate_clocks` gives inertial replacement if the macro re-fires before `t + D` |

In propagate and sweep this means: clock trees settle, every triggered flop samples, then all Q values change together. That matches the reference simulators' semantics for the cell library's `udp_dff` (which `verify_state.py` already runs nonblocking for Verilator), so the DFF macro can be checked against Icarus flop by flop.

`wave_limit` counts waves including those after a commit, so a ring of flops through combinational logic cannot loop forever without being caught by the existing oscillation fallback.

### 3.7 Combinational macros (mux, adder, ROM read, RAM read port)

Two policies:

* **(a) gate-like:** evaluate on pop, write outputs immediately. Same glitch behaviour as gates; no special path.
* **(b) deferred:** on pop, set `MF_DIRTY` and append to a `dirty_list`; evaluate dirty macros when the active wave front is empty, before the sequential commit. Inputs settled, one evaluation, no glitches (the full-adder/multiplier concern raised in discussion).

Recommended: (b) for propagate, with the per-settle order **active waves -> dirty combinational macros -> active waves -> ... -> sequential commit -> active waves**. In sweep the topological order already evaluates each macro gate after its inputs, so (b) reduces to (a) there except for back edges. In timed mode, combinational macros schedule their outputs at `t + D` like gates; deferral has no meaning when delays are explicit.

Caveat: (b) changes zero-delay ordering relative to gate-level logic (macro outputs appear after all gate-level activity of the settle). Results at quiescence are the same; intermediate waves differ. A combinational loop through a deferred macro is still caught by `wave_limit`.

### 3.8 Timed mode

* Stub delay is 0 (`Global_delay[MACRO_GATE_ID] = 0`, its own type, no special case), so the macro gate's task runs at the trigger time `t`, after the triggering task. The macro samples its inputs at `t`.
* Output delay `D` lives in the macro (per kind, editable like gate delays); outputs are tasks at `t + D` on the output gates (`complete_task` treats them like a source: stale-task check, then the hitlist walk).
* `D >= 1` for sequential macros keeps same-time readers from seeing the new value (the timed equivalent of 3.6).
* Inertial filtering on the macro gate (a second trigger inside the window replacing the first) does not apply because the macro gate's delay is 0. Inertial filtering on outputs uses the output gates' `gate_clocks`, as for gates.
* The timing system is finished; this adds a type to its tables and changes nothing else in it.

### 3.9 Sort and sweep order

* Sequential macros are breakpoints: their output gates are roots (in-degree 0, like `FLAG_BOUNDARY` targets), placed early. Inputs are normal edges into the macro gate, so it is placed after its inputs.
* Combinational macros need one dependency the gate graph does not have: macro gate -> each output gate. The sort adds it from `MacroCore.out[]` (a temporary adjacency, not a hitlist entry).
* After the sort, `sync_core` refills `inp[]`, `out[]` and `hitlist.data`, and `pack_gate` (P1) carries `MacroCore*` across.
* In sweep, a sequential macro's outputs sit before its macro gate, so their changes after the commit are back edges handled by `propagate`. That is the current behaviour of gate-level flop outputs too.

### 3.10 UNKNOWN

Gates go UNKNOWN when any input is UNKNOWN or unconnected. A macro reads its pins as 0/1/2 (UNKNOWN = 2) and decides per kind. Proposed rules (issue 6), modelled on the cell library's `udp_dff` table so the DFF can be verified against Icarus:

* **Storage:** previous inputs and staged outputs are one byte each (0/1/2) in `memory` (3.2); flop state is the output gates' value. RAM words in the extra area are two bitplanes, `value` and `xmask` (bit set = X), so a word costs 2x its width.
* **Output writes:** `FLAG_VALUE` holds only 0/1, so outputs are written as `output = v` (0/1/2) directly, and any staged value lives in the staged area of `memory`, not in `FLAG_VALUE`.
* **DFF clock edge**, from the previous input value in `memory` to current: 0->1 is an edge (Q = D, which may be X); 0->X and X->1 are "maybe edges": Q unchanged if D == Q, else Q = X; 1->0, 1->X, X->0 and steady: hold.
* **DFF async set/reset:** active (known) forces Q; X: Q unchanged if Q already equals the forced value, else Q = X; both active: whatever the library table says (check `DFFSRX1`).
* **DFF outputs:** QN = !Q, with X -> X.
* **Combinational macros (author's rule):** compute only when every input is known; otherwise drive every output X (never hold the old value, which would look valid). No counter is needed: the macro reads all its pins at each evaluation anyway, so one scan decides. More pessimistic than the gate-level equivalent (a gate-level adder with X high bits still produces correct low bits), so macro-vs-gate equivalence checks compare only vectors where all macro inputs are known. Count evaluations that saw X (`MacroCore.x_evals`) and expose them in the API, because an X that survives initialization points at a floating pin or a missing reset.
* **RAM read:** X address -> data out X. **RAM write:** X write-enable or X address while writing -> no word written; count it in a debug counter (marking the whole RAM X is the other choice, issue 6).
* **Unconnected inputs:** the macro gate stays UNKNOWN and never fires, as a gate with a floating input never settles.
* **Initial / after `reset()`:** flop state X (as gate-level flops start); RAM X on creation, not cleared by `reset()` (open); ROM keeps its image.

### 3.11 Python side

* **A macro is a gate, an IC only packages it (decided 2026-10-22).** `MacroGate(Gate)` is a Cython subclass like `Variable`/`NOT` ([Gates.pyx:516](../reactor/Gates.pyx#L516)). Overrides: `full_data`/`partial_data` add `kind`, `params`, the output gates' locations and optional state; `clone` remaps `outs` through `pseudo` and builds the core; `reset` also resets the core. Saving, loading, connect/disconnect and copy/paste of its inputs are the existing `Gate` code, because the inputs are ordinary sources.
* **`make_macro(kind, params)`:** kind table lookup, create the macro gate and its output gates, allocate the core and set `eval`, then package them in an IC (input pins connected to the macro gate, output pins driven by the output gates) for the UI.
* **After `optimize()`:** `sync_core` refills `core.inp` from the macro gate's `_sources` (already updated by `optimize()`), `core.out` from `outs`, and re-sets `hitlist.data`.
* **Flattening (`build_ic`):** the macro gate and its output gates are ordinary gates, so packaging a circuit that contains macros into an IC keeps them; `build_ic` must stop dropping gates with `id >= IC_INPUT_PIN_ID` that are macro types, and should stop wiping inner output pins (TODO P2, first item).
* `simulate()` must seed every macro (evaluate once, commit outputs) as it seeds variables; otherwise output pins sit at their initial value until the first trigger.
* `reset()`: reset macro state (issue 6) and clear `commit_list` / `dirty_list`.
* Serialization (`full_data`, `partial_data`, `clone`, JSON): a macro entry with kind, parameters, pin connections, optional state (ROM contents, RAM initial image). Darion's own JSON format is the input; keep it backward compatible (old files have no macros).
* IC creation from a circuit that contains macros: `IC.implement`/`configure` copy internal gates; they must also clone the macro objects and remap their locations. This is the largest unknown on the Python side (issue 9).
* UI: hide macro gates; draw macros as blocks with pins; show output gates as pins. The UI is the friend's code; keep the engine-side interface small (component with pins and a `kind`).

## 4. File-by-file changes (estimate)

| File | Change |
|---|---|
| `reactor/Const.pxd` | `MACRO_GATE_ID = 12`, `MACRO_OUT_ID = 13`, `TOTAL = 14` |
| new `reactor/Macro.h` | `MacroCore` base class (data, constructor/destructor, `reset`, `commit`, pure virtual `eval`); kind subclasses added separately |
| `reactor/Gates.pxd` | `extern` declaration of `MacroCore` |
| `reactor/Gates.pyx/.pxd` (`MacroGate`) | subclass with `kind`, `params`, `outs`, core; overrides of save/load/reset; refuse as source, refuse `MACRO_OUT` as target |
| `reactor/Circuit.pxd/.pyx` | macro list, `commit_list`, `dirty_list`; delay arrays `[TOTAL]`; dispatch in 4 sites; commit/dirty loops in `propagate` and `sweep`; output tasks in `complete_task`; seeding in `simulate`; `reset`; sort additions (3.9); remap after sort; free macros in `clearcircuit` / `__dealloc__` |
| `reactor/Circuit.pyx` (`build_ic`) | keep macro types and inner output pins when flattening |
| `reactor/Store.pyx` | `MACRO_GATE_ID` and `MACRO_OUT_ID` branches before `choice >= BUFFER_ID` |
| `tests/src/` loaders | test tooling only: map library flops (DFFX1, DFFSRX1, ...) to DFF macros instead of `DFFSR.json` (with the planned `--rtl` flag) |
| `tests/integrity_test.py`, `tests/test_timing.py` | macro cases (extend, do not add scripts) |

Rough size: engine 500-800 lines, Python component and serialization 300-500, tests 200-400. The DFF milestone alone is roughly half of the engine work, because it builds the infrastructure.

## 5. Milestones

1. **M0, infrastructure + DFF.** `build_ic` fix, `MACRO_GATE_ID`/`MACRO_OUT_ID`, `MacroGate`, `make_macro`, dispatch, output pin setup, commit list, seeding, reset, sort, remap, a DFF with async set/reset matching `DFFSRX1`. No UI. Validation 7.1-7.3.
2. **M1, register / counter** (width parameter, same kernel). Mostly free after M0.
3. **M2, RAM and ROM.** Combinational read (deferred, 3.7), synchronous write; state API; ROM contents in JSON.
4. **M3, bus multiplexer** (select lines, no Z).
5. **M4, UI and IC creation** with macros inside ICs.

## 6. Edge cases

* Macro with no trigger connected: never fires; outputs keep their seeded value.
* Trigger and data from the same source (a DFF whose D is its own clock): sampled after the triggering wave; defined by the rule in 3.6, verify against Icarus.
* An output pin feeding the same macro (counter feedback through logic): sequential, fine through the commit; combinational, a loop caught by `wave_limit`.
* Gate-vector growth: locations, so nothing to fix (3.2).
* Deleting a macro: deletion rebuilds the circuit from stored connections, so the macro's connections must be in that store.
* `hitlist_mem_layout()` and `geometry()`: skip macro gates (their `data` is not a profile array).
* `visual_queue`: the macro gate would be pushed on pop; skip it (the `continue` in 3.4 sits before the push, or the UI ignores the type).
* `eval_count`: macro evaluations are not edge evaluations; count them separately so benchmark evaluation counts stay comparable.
* Oscillation fallback to the timed queue while `commit_list` is non-empty: commit first, or move staged outputs into tasks at the current time + D.

## 7. Validation and measurement

1. **Correctness, DFF macro vs reference.** Load ITC99 and OpenCores designs with library flops mapped to DFF macros; `tests/verify_state.py` against Icarus (every flop and output, long runs, `--all-clocks` for multi-clock designs) and against Verilator with the nonblocking `udp_dff`. Expected: 0 mismatches, as with gate-level flops.
2. **Equivalence, macro vs gate-level DFF.** Same circuit with `DFFSR.json` flops and with DFF macros: identical outputs at every vector in propagate, sweep and timed modes (timed with a delay matching the gate-level flop's clock-to-Q).
3. **No regression without macros.** Current build versus macro build on circuits with no macros: rx-prop and rx-sweep on b15, b17, b18, b19, vga_lcd, des_perf, pinned, interleaved, 7-9 repeats, median and spread. The dispatch branch should cost nothing; if it does, Claim 13 numbers must be re-run on the macro build or the branch moved.
4. **Performance, macro vs gate-level flops** (new data, not a claim yet): ITC99/OpenCores with flops as macros vs as 10-gate DFFs; gate count, memory, load time, wall clock. This is also the natural "RTL-level flop" mode for the planned `--rtl`/`--gls` flags in the test scripts.
5. **Timing:** `tests/test_timing.py` suites unchanged; new cases for macro output delay and inertial replacement.
6. **Integrity:** `tests/integrity_test.py` unchanged, plus macro cases (connect/disconnect pins, optimize with macros, clear, reset, save/load, IC with macro inside).
7. **ASan build** once over the integrity tests (macro gate `data` must never be freed or walked).

## 8. Paper framing

Macros are future work in the current paper (CLAUDE.md: "Macros are the planned future direction"). If any macro result is reported, the OOP comparison stays on macro-free circuits, the macro's `switch` dispatch is stated as per-block not per-edge, and macro-versus-gate-level flop numbers are reported as a modelling choice (RTL-style flops), not as engine speed.

## 9. Interaction with P1 (packed hitlists)

* `pack_gate` copies `data` for empty lists, so `MacroCore*` in the macro gate survives `optimize()` (today's copy assignment would lose it).
* Stub `capacity == 0` means "never free, never grow", which is exactly the P1 rule for borrowed data.
* `connect` refusing a macro gate as source guarantees the macro gate never grows.
* P1 can land first and independently. M0 does not strictly depend on it: without P1, today's copy assignment drops `data` of empty lists in `optimize()`, but `sync_core` runs after every `optimize()` and can re-set `macro gate.hitlist.data = core`. The `HitList` free rule (never free when `capacity == 0`) is still needed so a destructor never frees the core.

## 10. Open issues for discussion

1. **Flag bit or type?** Decided: own type `MACRO_GATE_ID` (XOR seed and mask), no flag.
2. **Nonblocking rule (3.6).** With dispatch in the read-queue wave (decided): (i) stage in `FLAG_VALUE` and publish at the end of the wave (cheap, fixes same-wave races, not clock skew), or (ii) commit at quiescence (Verilog-like, fixes skew, needs a commit list). Timed mode uses `t + D` either way.
3. **Combinational policy (3.7).** Deferred evaluation (b) in propagate, or gate-like (a)? (b) answers the glitch concern; (a) is simpler and matches gate-level ordering.
4. **Input pins.** Decided: inputs are the macro gate's ordinary sources, all with edges (a sequential macro also wakes on data changes and returns early); IC pins exist only in the packaging.
5. **Delay model for macros.** Per-kind output delay D only, or per-pin (clock-to-Q, address-to-data)? Setup/hold checks (no, probably)?
6. **UNKNOWN and reset semantics** (3.10): flop state after reset X or 0; RAM kept or cleared on reset; X address on write.
7. **Combinational trigger limit.** 256 trigger inputs per macro gate (`Profile.index` uint8). Enough for an ALU/RAM; anything wider would need several macro gates or a wider index.
8. **State API.** What the API exposes: `macro.read(addr)`, `macro.write(addr, value)`, a whole-state dump? Writes during simulation: apply immediately and re-evaluate outputs, or only in DESIGN mode?
9. **ICs containing macros.** Solved by the gate model: flattening keeps the macro gate and output gates as gates; needs the `build_ic` change (TODO P2, first item).
10. **Serialization format** of a macro in Darion's JSON (kind, params, pin map, state image) and backward compatibility.
11. **Kinds list for M0-M3** and their exact pin sets (DFF with or without enable, async set/reset polarity as `DFFSRX1`, RAM single or dual port).
12. **User-defined macros from equations** (author's idea, 2026-10-22): the user writes characteristic equations (`dff: on posedge clk: q = d`; `sr: q = s | (q & ~r)`). C++ never parses text: Python parses the equation once (the `ast` module with a whitelist of `~ & | ^` and names, never `eval`) and compiles it to one of two forms the C++ side runs:
    * **3-valued truth table** (the Verilog UDP idea): evaluate the equation over {0, 1, X} for every combination of inputs plus current state, store `3^n` entries; C++ does `index = sum(pin_i * 3^i)`, one load. Exact X semantics for free. Practical up to about 10 inputs including state (59k entries); SR has 3 (27 entries), a DFF with async set/reset 5.
    * **Bytecode** for anything wider (word-level adders, buses): a postfix program (`LOAD s, LOAD q, LOAD r, NOT, AND, OR, STORE q`) run by a small C++ interpreter, with the "any X input -> X outputs" rule. Slower than a table, still once per trigger.
    **`if` statements** compile to multiplexers, so they never reach C++ as branches: each assigned variable becomes a nested mux over the conditions, and a branch that does not assign a variable holds it (`q = q`), which is how state is expressed. `if r: q = 0 / elif s: q = 1 / elif posedge(clk): q = d` becomes `q = mux(r, 0, mux(s, 1, mux(edge_clk, d, q)))`, a 5-variable table (243 entries). `posedge(clk)`/`negedge(clk)` are pseudo-inputs the macro computes from `prev` (X for a maybe-edge). X in a condition: the mux gives the common value if both arms agree, else X (UDP-like; Verilog behavioural `if (x)` takes the else branch, so say which one Darion follows). No loops, except `for` over a constant range, unrolled.
    **Decided (2026-10-22): no user-defined macros for now.** ICs already are user-defined blocks; a user-defined macro would only make a small IC faster or glitch-free, which does not justify a compiler. Macros are built-in native kinds only (DFF, RAM/ROM, word-level arithmetic, mux, register, counter). The table design below stays on file in case a need appears.
    **Decided (author, 2026-10-22): no Python backend.** Macro behaviour never runs Python, neither in the loop (GIL ruled out) nor deferred between settles (too slow if misused). Backends: native C++ kinds through the registry; optionally the truth-table and row-program modes, which run in C++ with no GIL. Equations may still be parsed by Python at load time to build the table or row program; that is load-time work only.
    **Recommendation (2026-10-22):** built-in, parameterised, word-level C++ kinds first (registry, 3.2); user-defined blocks are what ICs already are. Of the equation language, only the truth-table mode is worth building soon (small, exact X, covers JK/T/SR and custom latches); the row/bytecode interpreter only if a concrete need appears, because it grows into an HDL and Verilog already exists.
    The spec names inputs, state, outputs, the trigger (`posedge clk`, `any`) and async overrides; it is stored in the circuit JSON. Built-in kinds (DFF, RAM) stay hand-written C++.
