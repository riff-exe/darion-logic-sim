import sys
import os
import json
import time

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("reactor"))
import Circuit
import engine.Const as Const

# Load topology and ground truth from Digital
with open("tools/conway_topology.json") as f:
    topology = json.load(f)

with open("tools/digital_conway_states.json") as f:
    digital_states = json.load(f)

N = len(topology)
print(f"Loaded topology with {N} cells.")

c = Circuit.Circuit()
c.simulate(Const.DESIGN)
dff_ic = c.get_ic("tests/src/DFF.json")

clk = c.getcomponent(Const.VARIABLE_ID)
sel_init = c.getcomponent(Const.VARIABLE_ID)
const_0 = c.getcomponent(Const.VARIABLE_ID)

# NOT sel_init
not_sel = c.getcomponent(Const.NOT_ID)
c.setlimits(not_sel, 1)
c.connect(not_sel, sel_init.location, 0)

# Create 1200 DFFs
dffs = []
for i in range(N):
    inst = c.load_ic(dff_ic)
    c.connect(inst.inputs[0], clk.location, 0)
    dffs.append(inst)

def half_adder(a, b):
    s = c.getcomponent(Const.XOR_ID)
    c.setlimits(s, 2)
    c.connect(s, a.location, 0)
    c.connect(s, b.location, 1)
    co = c.getcomponent(Const.AND_ID)
    c.setlimits(co, 2)
    c.connect(co, a.location, 0)
    c.connect(co, b.location, 1)
    return s, co

def full_adder(a, b, cin):
    s1 = c.getcomponent(Const.XOR_ID)
    c.setlimits(s1, 2)
    c.connect(s1, a.location, 0)
    c.connect(s1, b.location, 1)
    s = c.getcomponent(Const.XOR_ID)
    c.setlimits(s, 2)
    c.connect(s, s1.location, 0)
    c.connect(s, cin.location, 1)
    ab = c.getcomponent(Const.AND_ID)
    c.setlimits(ab, 2)
    c.connect(ab, a.location, 0)
    c.connect(ab, b.location, 1)
    cs = c.getcomponent(Const.AND_ID)
    c.setlimits(cs, 2)
    c.connect(cs, cin.location, 0)
    c.connect(cs, s1.location, 1)
    co = c.getcomponent(Const.OR_ID)
    c.setlimits(co, 2)
    c.connect(co, ab.location, 0)
    c.connect(co, cs.location, 1)
    return s, co

print("Building exact cell gate trees from Digital topology...")
init_cycle_1 = digital_states["cycle_1"]

for i in range(N):
    nbr_indices = topology[i]
    nbr_nodes = [dffs[ni].outputs[0] for ni in nbr_indices]
    while len(nbr_nodes) < 8:
        nbr_nodes.append(const_0)
    
    # 8-bit adder tree
    s0, c0 = half_adder(nbr_nodes[0], nbr_nodes[1])
    s1, c1 = half_adder(nbr_nodes[2], nbr_nodes[3])
    s2, c2 = half_adder(nbr_nodes[4], nbr_nodes[5])
    s3, c3 = half_adder(nbr_nodes[6], nbr_nodes[7])
    
    bit0_a, c_bit0_a = half_adder(s0, s1)
    bit1_a, bit2_a = full_adder(c0, c1, c_bit0_a)
    
    bit0_b, c_bit0_b = half_adder(s2, s3)
    bit1_b, bit2_b = full_adder(c2, c3, c_bit0_b)
    
    b0, c_b0 = half_adder(bit0_a, bit0_b)
    b1, c_b1 = full_adder(bit1_a, bit1_b, c_b0)
    b2, b3 = full_adder(bit2_a, bit2_b, c_b1)
    
    not_b3 = c.getcomponent(Const.NOT_ID)
    c.setlimits(not_b3, 1)
    c.connect(not_b3, b3.location, 0)
    
    not_b2 = c.getcomponent(Const.NOT_ID)
    c.setlimits(not_b2, 1)
    c.connect(not_b2, b2.location, 0)
    
    b0_or_q = c.getcomponent(Const.OR_ID)
    c.setlimits(b0_or_q, 2)
    c.connect(b0_or_q, b0.location, 0)
    c.connect(b0_or_q, dffs[i].outputs[0].location, 1)
    
    next_d = c.getcomponent(Const.AND_ID)
    c.setlimits(next_d, 4)
    c.connect(next_d, not_b3.location, 0)
    c.connect(next_d, not_b2.location, 1)
    c.connect(next_d, b1.location, 2)
    c.connect(next_d, b0_or_q.location, 3)
    
    # Gating with not_sel: normal_d = next_d & ~sel_init
    normal_d = c.getcomponent(Const.AND_ID)
    c.setlimits(normal_d, 2)
    c.connect(normal_d, next_d.location, 0)
    c.connect(normal_d, not_sel.location, 1)
    
    if init_cycle_1[i] == 1:
        # Seed cell: d_in = normal_d | sel_init
        final_d = c.getcomponent(Const.OR_ID)
        c.setlimits(final_d, 2)
        c.connect(final_d, normal_d.location, 0)
        c.connect(final_d, sel_init.location, 1)
    else:
        # Non-seed cell: d_in = normal_d
        final_d = normal_d
        
    c.connect(dffs[i].inputs[1], final_d.location, 0)

num_comps = len(c.get_components() if hasattr(c, "get_components") else c.components)
print(f"Darion circuit constructed with {num_comps:,} gate components.")

c.optimize()
c.simulate(Const.SIMULATE)

print("Phase 1: Setting sel_init = 1 to load Digital's 36-cell seed into D inputs...")
c.toggle(sel_init.location, 1)
c.toggle(const_0.location, 0)
c.toggle(clk.location, 0)

print("Phase 2: Clock cycle 1 (0 -> 1 -> 0) to latch the seed...")
c.toggle(clk.location, 1)
c.toggle(clk.location, 0)

# Check cycle 1 state
cyc1_darion = [dffs[i].outputs[0].output for i in range(N)]
cyc1_digital = digital_states["cycle_1"]
cyc1_matches = sum(1 for d, g in zip(cyc1_darion, cyc1_digital) if d == g)
print(f"Cycle 1 (Seed Latch): Digital Active = {sum(cyc1_digital)}, Darion Active = {sum(cyc1_darion)}, Match = {cyc1_matches}/{N} ({cyc1_matches/N*100:.2f}%)")

print("Phase 3: Switching sel_init = 0 for autonomous Conway Game of Life evolution...")
c.toggle(sel_init.location, 0)

print("\n" + "="*70)
print(f"{'Cycle':<8} | {'Digital Active':<15} | {'Darion Active':<15} | {'Match Rate':<15} | {'Status':<8}")
print("-" * 70)

all_passed = (cyc1_matches == N)
print(f"Cycle 1  | {sum(cyc1_digital):<15} | {sum(cyc1_darion):<15} | {cyc1_matches/N*100:6.2f}% ({cyc1_matches}/{N}) | {'PASS' if cyc1_matches == N else 'FAIL'}")

for cyc in range(2, 26):
    c.toggle(clk.location, 1)
    c.toggle(clk.location, 0)
    
    darion_state = [dffs[i].outputs[0].output for i in range(N)]
    digital_state = digital_states[f"cycle_{cyc}"]
    
    matches = sum(1 for d, g in zip(darion_state, digital_state) if d == g)
    match_pct = (matches / N) * 100.0
    status = "PASS" if matches == N else "FAIL"
    if matches != N:
        all_passed = False
    
    print(f"Cycle {cyc:<2} | {sum(digital_state):<15} | {sum(darion_state):<15} | {match_pct:6.2f}% ({matches}/{N}) | {status}")

print("="*70)
if all_passed:
    print(">> 100.0% BIT-FOR-BIT VERIFICATION PASSED ACROSS ALL 1,200 CELLS AND ALL CYCLES! <<")
else:
    print(">> VERIFICATION FAILED: Mismatches detected. <<")
