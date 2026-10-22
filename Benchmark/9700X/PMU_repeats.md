# Zen 5 (Ryzen 7 9700X): full-engine PMU repeats, rx-prop vs rx-oop (2026-10-22)

Re-measurement of the Claim 13 repeat tables, stored here because the earlier Zen 5 repeats existed only as numbers in `research/Claims.md`. Machine idle (verification finished first), `perf.py` pins to core 2 itself, SMT sibling online, 5,000 vectors, one engine pair per call, circuits interleaved within each repeat. Commands:

```bash
for r in 1..9; do for c in b15 b17 b18 b19; do
  PYTHONPATH=editor/tools .venv/bin/python tests/src/perf.py itc99 --filter $c.v --no-engine --no-rx-sweep --no-icarus --no-verilator \
    | grep -E "\| rx-prop |\| rx-oop" ; done; done            # other circuits: perf.py <suite> --filter <circuit>.v, 7 repeats
```

Each ratio is OOP divided by prop for the same repeat; the table gives the median and [min, max] over repeats, the medians of the other ratios, and the spread of rx-prop cycles across repeats. Raw rows: session scratchpad (`pmu_itc99.log`, `pmu_other.log`).

## ITC99, 9 repeats

| Circuit | repeats | cycles OOP/prop, median [min, max] | instructions OOP/prop | L1 misses | L2 misses | branch misses | IPC prop / OOP | prop cycles spread |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| b15 | 9 | **2.03** [1.99, 2.09] | 1.18 | 1.59 | 7.0 | 5.6 | 3.53 / 2.03 | 4% |
| b17 | 9 | **2.02** [1.95, 2.06] | 1.16 | 1.60 | 3.1 | 6.0 | 3.13 / 1.81 | 6% |
| b18 | 9 | **2.16** [2.08, 2.24] | 1.16 | 1.58 | 2.5 | 2.5 | 2.65 / 1.43 | 4% |
| b19 | 9 | **1.89** [1.85, 1.97] | 1.16 | 1.60 | 2.2 | 2.4 | 2.65 / 1.63 | 1% |

Median of the per-circuit medians: 2.02 (range 1.89-2.16, 4 circuits).

## ISCAS85, EPFL and OpenCores, 7 repeats

| Circuit | repeats | cycles OOP/prop, median [min, max] | instructions OOP/prop | L1 misses | L2 misses | branch misses | IPC prop / OOP | prop cycles spread |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| c1908 | 7 | **2.33** [2.28, 2.47] | 1.39 | 1.89 | 3.2 | 1.9 | 2.53 / 1.51 | 9% |
| c3540 | 7 | **2.72** [2.44, 2.80] | 1.38 | 1.71 | 2.6 | 2.5 | 2.54 / 1.29 | 15% |
| c5315 | 7 | **2.28** [2.25, 2.42] | 1.18 | 1.61 | 2.6 | 2.1 | 2.47 / 1.27 | 7% |
| c6288 | 7 | **1.48** [1.47, 1.49] | 1.18 | 1.64 | 1.5 | 1.1 | 2.26 / 1.80 | 1% |
| c7552 | 7 | **2.24** [2.23, 2.31] | 1.28 | 1.47 | 1.5 | 2.0 | 2.34 / 1.33 | 3% |
| adder | 7 | **2.03** [1.94, 2.18] | 1.14 | 1.49 | 1.8 | 2.1 | 2.39 / 1.34 | 12% |
| bar | 7 | **1.77** [1.71, 1.84] | 1.24 | 1.57 | 4.5 | 1.9 | 3.66 / 2.54 | 6% |
| max | 7 | **1.99** [1.96, 2.00] | 1.11 | 1.35 | 3.6 | 2.7 | 2.92 / 1.64 | 2% |
| arbiter | 7 | **2.04** [2.02, 2.04] | 1.17 | 2.29 | 15.0 | 2.0 | 3.01 / 1.73 | 1% |
| cavlc | 7 | **3.18** [2.66, 3.61] | 1.56 | 2.18 | 1.8 | 4.4 | 2.78 / 1.39 | 23% |
| des_area | 7 | **2.35** [2.32, 2.38] | 1.18 | 1.61 | 16.6 | 2.0 | 2.41 / 1.21 | 1% |
| systemcaes | 7 | **1.99** [1.97, 2.02] | 1.15 | 1.62 | 5.7 | 2.8 | 3.36 / 1.93 | 2% |
| tv80 | 7 | **1.74** [1.71, 1.75] | 1.19 | 1.68 | 8.1 | 3.5 | 3.51 / 2.40 | 2% |
| ac97_ctrl | 7 | **1.72** [1.68, 1.74] | 1.15 | 1.78 | 3.5 | 2.4 | 3.21 / 2.16 | 2% |
| mem_ctrl | 7 | **1.91** [1.87, 1.93] | 1.16 | 1.77 | 9.3 | 2.5 | 3.49 / 2.12 | 2% |
| aes_core | 7 | **2.56** [2.55, 2.58] | 1.18 | 1.34 | 2.1 | 2.7 | 2.17 / 1.00 | 1% |
| des_perf | 7 | **2.27** [2.23, 2.36] | 1.16 | 1.34 | 1.7 | 2.3 | 1.75 / 0.89 | 2% |
| usb_funct | 7 | **1.76** [1.70, 1.77] | 1.15 | 1.70 | 4.4 | 2.2 | 3.11 / 2.05 | 2% |
| wb_conmax | 7 | **1.66** [1.62, 1.71] | 1.08 | 1.49 | 2.2 | 2.2 | 2.89 / 1.89 | 5% |
| vga_lcd | 7 | **1.79** [1.73, 1.83] | 1.16 | 1.77 | 2.4 | 3.5 | 3.05 / 1.97 | 1% |

Median of the per-circuit medians: 2.01 (range 1.48-3.18, 20 circuits).

## Agreement with the stored values (Claims.md, Claim 13)

ITC99: 2.03 / 2.02 / 2.16 / 1.89 here against 2.05 / 2.04 / 2.12 / 1.90 stored. Other circuits: every median within about 0.1 of the stored one except cavlc (3.18 here, 3.38 stored; its rx-prop cycles spread 23% across repeats) and vga_lcd (1.79 here, 1.67 stored). The stored text said "19 circuits"; its table, and this one, list 20.
