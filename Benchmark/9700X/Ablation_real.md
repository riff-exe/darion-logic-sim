# Zen 5 (Ryzen 7 9700X): ablation harness on 25 real netlists (2026-10-22)

`tests/ablation_layout.cpp` built with `g++ -O3 -march=native -std=c++20`; netlists exported from the production engine with `tests/ablation_eval.py --export reactor <suite/>circuit out.net` (optimized layout, benchmark vectors); each run pinned to core 2, 9 repeats, variants abcdge, once with topological placement and once shuffled with `--frag 192`. Machine idle. Times are median ns per edge evaluation; ratios are of medians. Variants: a heap objects + virtual call (40 B), b same objects in an arena, c flat 24 B + `switch`, d flat 24 B + SIMA, e SIMA at 32 B, g SIMA at 40 B. Stored so the Zen 5 harness numbers in `research/Claims.md` (Claim 13) have data behind them; they were previously only in the claims doc.




| Configuration | a heap+virtual | b arena | c switch | d SIMA | e 32 B | g 40 B | a/d | b/a | c/a | d/c | branch miss/eval a / d | max spread | fingerprints |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| b14 topological | 7.47 | 7.34 | 5.81 | 3.14 | 3.29 | 3.32 | **2.38** | 0.98 | 0.78 | 0.54 | 0.565 / 0.243 | 1% | identical |
| b14 shuffled-frag | 8.62 | 8.03 | 6.16 | 3.53 | 3.65 | 3.75 | **2.44** | 0.93 | 0.71 | 0.57 | 0.573 / 0.242 | 6% | identical |
| b15 topological | 4.14 | 4.03 | 3.29 | 2.27 | 2.38 | 2.47 | **1.82** | 0.97 | 0.79 | 0.69 | 0.142 / 0.026 | 8% | identical |
| b15 shuffled-frag | 5.12 | 4.82 | 3.94 | 2.93 | 3.02 | 3.14 | **1.75** | 0.94 | 0.77 | 0.74 | 0.143 / 0.026 | 4% | identical |
| b17 topological | 4.81 | 4.63 | 3.72 | 2.73 | 2.95 | 3.12 | **1.76** | 0.96 | 0.77 | 0.73 | 0.135 / 0.023 | 2% | identical |
| b17 shuffled-frag | 6.51 | 5.72 | 5.21 | 4.23 | 4.36 | 4.55 | **1.54** | 0.88 | 0.80 | 0.81 | 0.136 / 0.023 | 2% | identical |
| b18 topological | 6.39 | 6.09 | 4.95 | 3.30 | 3.61 | 3.73 | **1.94** | 0.95 | 0.77 | 0.67 | 0.294 / 0.109 | 7% | identical |
| b18 shuffled-frag | 9.27 | 7.49 | 6.83 | 5.12 | 5.02 | 5.02 | **1.81** | 0.81 | 0.74 | 0.75 | 0.298 / 0.109 | 2% | identical |
| b19 topological | 5.78 | 5.56 | 4.62 | 3.45 | 3.57 | 3.85 | **1.68** | 0.96 | 0.80 | 0.75 | 0.179 / 0.064 | 5% | identical |
| b19 shuffled-frag | 10.07 | 7.34 | 6.89 | 5.69 | 5.49 | 5.63 | **1.77** | 0.73 | 0.68 | 0.83 | 0.181 / 0.064 | 2% | identical |
| c1908 topological | 6.39 | 6.37 | 5.62 | 3.00 | 3.05 | 3.04 | **2.13** | 1.00 | 0.88 | 0.53 | 0.496 / 0.258 | 2% | identical |
| c1908 shuffled-frag | 6.71 | 6.47 | 5.63 | 3.00 | 3.06 | 3.07 | **2.24** | 0.96 | 0.84 | 0.53 | 0.501 / 0.258 | 1% | identical |
| c3540 topological | 7.78 | 7.70 | 6.38 | 3.30 | 3.34 | 3.34 | **2.36** | 0.99 | 0.82 | 0.52 | 0.654 / 0.296 | 3% | identical |
| c3540 shuffled-frag | 8.10 | 7.93 | 6.43 | 3.35 | 3.39 | 3.42 | **2.42** | 0.98 | 0.79 | 0.52 | 0.657 / 0.296 | 27% | identical |
| c5315 topological | 7.70 | 7.63 | 6.22 | 3.39 | 3.49 | 3.51 | **2.27** | 0.99 | 0.81 | 0.55 | 0.617 / 0.296 | 1% | identical |
| c5315 shuffled-frag | 8.25 | 7.88 | 6.34 | 3.54 | 3.60 | 3.61 | **2.33** | 0.96 | 0.77 | 0.56 | 0.616 / 0.296 | 1% | identical |
| c6288 topological | 5.16 | 5.12 | 4.06 | 3.54 | 3.65 | 3.66 | **1.46** | 0.99 | 0.79 | 0.87 | 0.347 / 0.321 | 5% | identical |
| c6288 shuffled-frag | 5.49 | 5.23 | 4.21 | 3.69 | 3.75 | 3.76 | **1.49** | 0.95 | 0.77 | 0.88 | 0.347 / 0.321 | 1% | identical |
| c7552 topological | 7.86 | 7.78 | 6.39 | 3.57 | 3.67 | 3.68 | **2.20** | 0.99 | 0.81 | 0.56 | 0.597 / 0.303 | 1% | identical |
| c7552 shuffled-frag | 8.65 | 8.04 | 6.52 | 3.73 | 3.79 | 3.80 | **2.32** | 0.93 | 0.75 | 0.57 | 0.608 / 0.302 | 2% | identical |
| adder topological | 7.91 | 7.83 | 5.21 | 3.93 | 3.95 | 4.03 | **2.01** | 0.99 | 0.66 | 0.75 | 0.567 / 0.276 | 0% | identical |
| adder shuffled-frag | 8.57 | 8.08 | 5.32 | 4.06 | 4.07 | 4.15 | **2.11** | 0.94 | 0.62 | 0.76 | 0.571 / 0.277 | 0% | identical |
| bar topological | 3.44 | 3.37 | 2.86 | 2.40 | 2.53 | 2.58 | **1.43** | 0.98 | 0.83 | 0.84 | 0.042 / 0.024 | 1% | identical |
| bar shuffled-frag | 4.16 | 3.65 | 3.20 | 2.79 | 2.82 | 2.87 | **1.49** | 0.88 | 0.77 | 0.87 | 0.042 / 0.024 | 1% | identical |
| max topological | 6.34 | 6.25 | 3.85 | 3.16 | 3.26 | 3.30 | **2.01** | 0.99 | 0.61 | 0.82 | 0.363 / 0.134 | 1% | identical |
| max shuffled-frag | 7.24 | 6.55 | 4.12 | 3.46 | 3.52 | 3.55 | **2.09** | 0.90 | 0.57 | 0.84 | 0.365 / 0.135 | 1% | identical |
| arbiter topological | 4.34 | 4.27 | 3.41 | 2.99 | 3.21 | 3.28 | **1.45** | 0.98 | 0.79 | 0.88 | 0.091 / 0.049 | 0% | identical |
| arbiter shuffled-frag | 6.00 | 5.26 | 3.97 | 3.53 | 3.79 | 4.13 | **1.70** | 0.88 | 0.66 | 0.89 | 0.092 / 0.049 | 1% | identical |
| cavlc topological | 6.90 | 6.83 | 3.23 | 2.72 | 2.80 | 2.85 | **2.54** | 0.99 | 0.47 | 0.84 | 0.481 / 0.146 | 1% | identical |
| cavlc shuffled-frag | 7.05 | 6.89 | 3.25 | 2.75 | 2.81 | 2.87 | **2.56** | 0.98 | 0.46 | 0.85 | 0.482 / 0.146 | 1% | identical |
| des_area topological | 7.99 | 7.94 | 6.28 | 3.46 | 3.55 | 3.58 | **2.31** | 0.99 | 0.79 | 0.55 | 0.649 / 0.294 | 1% | identical |
| des_area shuffled-frag | 9.22 | 8.41 | 6.49 | 3.70 | 3.76 | 3.84 | **2.49** | 0.91 | 0.70 | 0.57 | 0.656 / 0.294 | 1% | identical |
| systemcaes topological | 4.35 | 4.25 | 3.49 | 2.50 | 2.59 | 2.73 | **1.74** | 0.98 | 0.80 | 0.72 | 0.143 / 0.051 | 2% | identical |
| systemcaes shuffled-frag | 5.79 | 5.20 | 4.15 | 3.23 | 3.39 | 3.63 | **1.79** | 0.90 | 0.72 | 0.78 | 0.144 / 0.051 | 2% | identical |
| tv80 topological | 3.62 | 3.55 | 3.04 | 2.31 | 2.40 | 2.45 | **1.57** | 0.98 | 0.84 | 0.76 | 0.077 / 0.021 | 5% | identical |
| tv80 shuffled-frag | 4.50 | 4.21 | 3.49 | 2.84 | 2.97 | 3.07 | **1.58** | 0.94 | 0.78 | 0.81 | 0.078 / 0.021 | 5% | identical |
| ac97_ctrl topological | 3.78 | 3.64 | 3.04 | 2.71 | 2.78 | 3.09 | **1.39** | 0.96 | 0.80 | 0.89 | 0.015 / 0.007 | 7% | identical |
| ac97_ctrl shuffled-frag | 6.09 | 5.63 | 5.10 | 4.31 | 4.46 | 4.84 | **1.41** | 0.92 | 0.84 | 0.85 | 0.015 / 0.007 | 1% | identical |
| mem_ctrl topological | 3.77 | 3.63 | 3.04 | 2.39 | 2.57 | 2.67 | **1.58** | 0.96 | 0.81 | 0.79 | 0.065 / 0.026 | 1% | identical |
| mem_ctrl shuffled-frag | 5.36 | 4.89 | 4.12 | 3.41 | 3.57 | 3.90 | **1.57** | 0.91 | 0.77 | 0.83 | 0.065 / 0.026 | 2% | identical |
| aes_core topological | 9.79 | 9.66 | 7.40 | 4.01 | 4.18 | 4.30 | **2.44** | 0.99 | 0.76 | 0.54 | 0.689 / 0.231 | 2% | identical |
| aes_core shuffled-frag | 11.14 | 10.78 | 8.24 | 4.79 | 5.00 | 5.13 | **2.33** | 0.97 | 0.74 | 0.58 | 0.690 / 0.231 | 1% | identical |
| des_perf topological | 10.70 | 9.89 | 7.91 | 5.31 | 5.65 | 5.89 | **2.02** | 0.92 | 0.74 | 0.67 | 0.534 / 0.209 | 3% | identical |
| des_perf shuffled-frag | 19.77 | 11.70 | 9.83 | 7.46 | 7.46 | 7.44 | **2.65** | 0.59 | 0.50 | 0.76 | 0.538 / 0.209 | 5% | identical |
| usb_funct topological | 4.24 | 4.11 | 3.45 | 2.82 | 3.01 | 3.18 | **1.50** | 0.97 | 0.81 | 0.82 | 0.063 / 0.026 | 1% | identical |
| usb_funct shuffled-frag | 5.94 | 5.51 | 4.64 | 4.04 | 4.25 | 4.49 | **1.47** | 0.93 | 0.78 | 0.87 | 0.064 / 0.026 | 2% | identical |
| wb_conmax topological | 4.72 | 4.60 | 3.80 | 3.12 | 3.38 | 3.56 | **1.51** | 0.97 | 0.81 | 0.82 | 0.103 / 0.047 | 2% | identical |
| wb_conmax shuffled-frag | 6.25 | 5.39 | 5.16 | 4.59 | 4.61 | 4.85 | **1.36** | 0.86 | 0.83 | 0.89 | 0.103 / 0.046 | 2% | identical |
| vga_lcd topological | 4.26 | 3.94 | 3.68 | 3.10 | 3.35 | 3.48 | **1.37** | 0.92 | 0.86 | 0.84 | 0.007 / 0.003 | 5% | identical |
| vga_lcd shuffled-frag | 10.35 | 6.43 | 6.38 | 5.93 | 6.16 | 6.00 | **1.75** | 0.62 | 0.62 | 0.93 | 0.007 / 0.003 | 3% | identical |

**Fingerprints:** identical in all 50 configurations.

**Agreement with the stored Claim 13 values:** topological a/d b15 1.82 (stored 1.81), b17 1.76 (1.76), b18 1.94 (1.92), b19 1.68 (1.70), c1908 2.13 (2.14), c3540 2.36 (2.38), c5315 2.27 (2.27), c6288 1.46 (1.46); the rest within about 0.06.

**Harness against the full engine (24 circuits with engine repeats, `PMU_repeats.md`):** Pearson r = 0.89 between the topological harness a/d and the engine OOP/prop cycle ratio; the engine ratio is on average 0.23 higher; it falls inside the harness's [topological, shuffled+fragmented] bracket for 6 of 24 circuits (c5315, c6288, c7552, adder, des_area, des_perf). Harness a/d median 1.79, range 1.37-2.54. All as stored (r = 0.89, about 0.25, 6 of 24).
