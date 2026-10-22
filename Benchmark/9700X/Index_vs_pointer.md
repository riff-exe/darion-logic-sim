# Zen 5 (Ryzen 7 9700X): pointer versus index edges, and CSR, in the ablation harness (2026-10-22)

`tests/ablation_layout.cpp` (variants added 2026-10-22: `i` index edges with the 24-byte gate, `j` index edges with the gate padded to 32 bytes, `k` CSR with index edges and a 16-byte gate, `p` CSR with pointer edges and a 16-byte gate), built with `g++ -O3 -march=native -std=c++20`; the 25 real netlists re-exported with `tests/ablation_eval.py --export reactor <suite/>circuit out.net`; each run pinned to core 2, 9 interleaved repeats, machine idle. Times are median ns per edge evaluation. Every run reproduced the evaluation counts, changed-gate counts and final-state fingerprint of variant `d` (the current engine layout: 24-byte gate, 16-byte pointer edges in per-gate lists). Harness numbers, not the full engine.

Motivation: macros need side tables keyed by gate location, and indices would also simplify `Store`; the question was what indices cost in the hot loop.

## Index cost, separated from stride (topological placement)

| circuit | gates | d ptr 24 B | e ptr 32 B | i idx 24 B | j idx 32 B | k CSR idx 16 B | i/d | j/e | k/d |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| c1908 | 938 | 2.96 | 3.00 | 3.25 | 3.36 | 3.26 | 1.098 | 1.120 | 1.101 |
| cavlc | 1,300 | 2.71 | 2.78 | 3.00 | 3.14 | 2.80 | 1.107 | 1.129 | 1.033 |
| c3540 | 1,741 | 3.25 | 3.28 | 3.57 | 3.68 | 3.49 | 1.098 | 1.122 | 1.074 |
| c6288 | 2,480 | 3.52 | 3.60 | 3.78 | 3.87 | 3.58 | 1.074 | 1.075 | 1.017 |
| adder | 2,547 | 3.91 | 3.95 | 4.31 | 4.36 | 4.14 | 1.102 | 1.104 | 1.059 |
| c5315 | 2,608 | 3.36 | 3.42 | 3.68 | 3.79 | 3.57 | 1.095 | 1.108 | 1.062 |
| c7552 | 3,828 | 3.55 | 3.60 | 3.87 | 3.99 | 3.72 | 1.090 | 1.108 | 1.048 |
| bar | 5,526 | 2.43 | 2.53 | 2.70 | 2.84 | 2.47 | 1.111 | 1.123 | 1.016 |
| max | 6,025 | 3.20 | 3.26 | 3.53 | 3.65 | 3.33 | 1.103 | 1.120 | 1.041 |
| des_area | 8,365 | 3.46 | 3.53 | 3.76 | 3.86 | 3.56 | 1.087 | 1.093 | 1.029 |
| b14 | 14,299 | 3.13 | 3.21 | 3.37 | 3.54 | 3.17 | 1.077 | 1.103 | 1.013 |
| tv80 | 15,992 | 2.34 | 2.39 | 2.75 | 2.82 | 2.40 | 1.175 | 1.180 | 1.026 |
| arbiter | 23,618 | 3.01 | 3.21 | 3.15 | 3.35 | 2.76 | 1.047 | 1.044 | 0.917 |
| systemcaes | 24,121 | 2.52 | 2.69 | 2.82 | 3.06 | 2.47 | 1.119 | 1.138 | 0.980 |
| b15 | 24,329 | 2.28 | 2.37 | 2.59 | 2.75 | 2.30 | 1.136 | 1.160 | 1.009 |
| mem_ctrl | 33,041 | 2.46 | 2.53 | 2.79 | 3.09 | 2.39 | 1.134 | 1.221 | 0.972 |
| aes_core | 33,515 | 4.10 | 4.21 | 4.41 | 4.61 | 3.70 | 1.076 | 1.095 | 0.902 |
| usb_funct | 44,472 | 2.80 | 2.95 | 3.29 | 3.50 | 2.53 | 1.175 | 1.186 | 0.904 |
| ac97_ctrl | 52,054 | 2.75 | 2.92 | 3.32 | 3.47 | 2.33 | 1.207 | 1.188 | 0.847 |
| wb_conmax | 60,876 | 3.15 | 3.37 | 3.48 | 3.77 | 2.76 | 1.105 | 1.119 | 0.876 |
| b17 | 73,475 | 2.66 | 2.87 | 3.23 | 3.54 | 2.44 | 1.214 | 1.233 | 0.917 |
| b18 | 182,380 | 3.26 | 3.46 | 3.90 | 4.14 | 2.98 | 1.196 | 1.197 | 0.914 |
| des_perf | 243,901 | 5.55 | 5.77 | 5.96 | 6.31 | 4.54 | 1.074 | 1.094 | 0.818 |
| b19 | 356,399 | 3.40 | 3.61 | 4.24 | 4.50 | 2.95 | 1.247 | 1.247 | 0.868 |
| vga_lcd | 443,630 | 3.00 | 3.35 | 3.91 | 4.16 | 2.57 | 1.303 | 1.242 | 0.857 |
- i/d: geomean 1.128 [1.047, 1.303], designs of 100k gates or more 1.202
- j/e: geomean 1.141 [1.044, 1.247], designs of 100k gates or more 1.193
- k/d: geomean 0.969 [0.818, 1.101], designs of 100k gates or more 0.863

## CSR with pointers versus CSR with indices (both placements)

| circuit | placement | gates | d ptr 24 B | k CSR idx | p CSR ptr | k/d | p/d | k/p |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| c1908 | shuffled | 938 | 3.00 | 3.24 | 2.99 | 1.080 | 0.997 | 1.084 |
| c1908 | topological | 938 | 2.98 | 3.25 | 2.98 | 1.091 | 1.000 | 1.091 |
| cavlc | shuffled | 1,300 | 2.74 | 2.78 | 2.60 | 1.015 | 0.949 | 1.069 |
| cavlc | topological | 1,300 | 2.72 | 2.77 | 2.58 | 1.018 | 0.949 | 1.074 |
| c3540 | shuffled | 1,741 | 3.34 | 3.51 | 3.36 | 1.051 | 1.006 | 1.045 |
| c3540 | topological | 1,741 | 3.27 | 3.46 | 3.26 | 1.058 | 0.997 | 1.061 |
| c6288 | shuffled | 2,480 | 3.68 | 3.75 | 3.65 | 1.019 | 0.992 | 1.027 |
| c6288 | topological | 2,480 | 3.54 | 3.56 | 3.40 | 1.006 | 0.960 | 1.047 |
| adder | shuffled | 2,547 | 4.07 | 4.32 | 4.10 | 1.061 | 1.007 | 1.054 |
| adder | topological | 2,547 | 3.93 | 4.13 | 3.88 | 1.051 | 0.987 | 1.064 |
| c5315 | shuffled | 2,608 | 3.53 | 3.70 | 3.56 | 1.048 | 1.008 | 1.039 |
| c5315 | topological | 2,608 | 3.39 | 3.54 | 3.35 | 1.044 | 0.988 | 1.057 |
| c7552 | shuffled | 3,828 | 3.72 | 3.95 | 3.79 | 1.062 | 1.019 | 1.042 |
| c7552 | topological | 3,828 | 3.55 | 3.67 | 3.52 | 1.034 | 0.992 | 1.043 |
| bar | shuffled | 5,526 | 2.79 | 3.13 | 2.93 | 1.122 | 1.050 | 1.068 |
| bar | topological | 5,526 | 2.40 | 2.48 | 2.26 | 1.033 | 0.942 | 1.097 |
| max | shuffled | 6,025 | 3.48 | 3.87 | 3.61 | 1.112 | 1.037 | 1.072 |
| max | topological | 6,025 | 3.17 | 3.33 | 3.10 | 1.050 | 0.978 | 1.074 |
| des_area | shuffled | 8,365 | 3.72 | 3.98 | 3.79 | 1.070 | 1.019 | 1.050 |
| des_area | topological | 8,365 | 3.45 | 3.53 | 3.36 | 1.023 | 0.974 | 1.051 |
| b14 | shuffled | 14,299 | 3.48 | 3.69 | 3.61 | 1.060 | 1.037 | 1.022 |
| b14 | topological | 14,299 | 3.13 | 3.13 | 3.02 | 1.000 | 0.965 | 1.036 |
| tv80 | shuffled | 15,992 | 2.84 | 3.36 | 3.17 | 1.183 | 1.116 | 1.060 |
| tv80 | topological | 15,992 | 2.32 | 2.42 | 2.20 | 1.043 | 0.948 | 1.100 |
| arbiter | shuffled | 23,618 | 3.60 | 3.90 | 3.75 | 1.083 | 1.042 | 1.040 |
| arbiter | topological | 23,618 | 3.00 | 2.75 | 2.62 | 0.917 | 0.873 | 1.050 |
| systemcaes | shuffled | 24,121 | 3.22 | 3.63 | 3.47 | 1.127 | 1.078 | 1.046 |
| systemcaes | topological | 24,121 | 2.50 | 2.46 | 2.30 | 0.984 | 0.920 | 1.070 |
| b15 | shuffled | 24,329 | 2.91 | 3.37 | 3.21 | 1.158 | 1.103 | 1.050 |
| b15 | topological | 24,329 | 2.25 | 2.29 | 2.13 | 1.018 | 0.947 | 1.075 |
| mem_ctrl | shuffled | 33,041 | 3.43 | 3.82 | 3.75 | 1.114 | 1.093 | 1.019 |
| mem_ctrl | topological | 33,041 | 2.43 | 2.41 | 2.21 | 0.992 | 0.909 | 1.090 |
| aes_core | shuffled | 33,515 | 4.75 | 4.61 | 4.69 | 0.971 | 0.987 | 0.983 |
| aes_core | topological | 33,515 | 4.01 | 3.66 | 3.55 | 0.913 | 0.885 | 1.031 |
| usb_funct | shuffled | 44,472 | 4.03 | 4.20 | 4.27 | 1.042 | 1.060 | 0.984 |
| usb_funct | topological | 44,472 | 2.91 | 2.53 | 2.43 | 0.869 | 0.835 | 1.041 |
| ac97_ctrl | shuffled | 52,054 | 4.53 | 4.65 | 4.89 | 1.026 | 1.079 | 0.951 |
| ac97_ctrl | topological | 52,054 | 2.68 | 2.32 | 2.20 | 0.866 | 0.821 | 1.055 |
| wb_conmax | shuffled | 60,876 | 4.42 | 4.68 | 4.79 | 1.059 | 1.084 | 0.977 |
| wb_conmax | topological | 60,876 | 3.15 | 2.75 | 2.63 | 0.873 | 0.835 | 1.046 |
| b17 | shuffled | 73,475 | 4.17 | 4.78 | 4.70 | 1.146 | 1.127 | 1.017 |
| b17 | topological | 73,475 | 2.66 | 2.42 | 2.30 | 0.910 | 0.865 | 1.052 |
| b18 | shuffled | 182,380 | 4.96 | 5.89 | 5.77 | 1.188 | 1.163 | 1.021 |
| b18 | topological | 182,380 | 3.29 | 2.93 | 2.83 | 0.891 | 0.860 | 1.035 |
| des_perf | shuffled | 243,901 | 7.23 | 7.87 | 7.26 | 1.089 | 1.004 | 1.084 |
| des_perf | topological | 243,901 | 5.34 | 4.44 | 4.49 | 0.831 | 0.841 | 0.989 |
| b19 | shuffled | 356,399 | 5.39 | 6.49 | 6.22 | 1.204 | 1.154 | 1.043 |
| b19 | topological | 356,399 | 3.17 | 2.83 | 2.73 | 0.893 | 0.861 | 1.037 |
| vga_lcd | shuffled | 443,630 | 5.96 | 7.33 | 7.00 | 1.230 | 1.174 | 1.047 |
| vga_lcd | topological | 443,630 | 2.94 | 2.56 | 2.46 | 0.871 | 0.837 | 1.041 |
- topological, k/d: geomean 0.968 [0.831, 1.091], below 1 on 12/25; under 10k gates 1.041; 100k or more 0.871
- topological, p/d: geomean 0.917 [0.821, 1.000], below 1 on 24/25; under 10k gates 0.976; 100k or more 0.850
- topological, k/p: geomean 1.056 [0.989, 1.100], below 1 on 1/25; under 10k gates 1.066; 100k or more 1.025
- shuffled, k/d: geomean 1.091 [0.971, 1.230], below 1 on 1/25; under 10k gates 1.063; 100k or more 1.176
- shuffled, p/d: geomean 1.054 [0.949, 1.174], below 1 on 4/25; under 10k gates 1.008; 100k or more 1.122
- shuffled, k/p: geomean 1.035 [0.951, 1.084], below 1 on 4/25; under 10k gates 1.055; 100k or more 1.049

## Reading

- Index edges are slower than pointer edges in every layout: 13% (24-byte gate) and 14% (32-byte gate, so not the non-power-of-two stride) with per-gate lists, about 5% inside CSR. The loop is latency-bound (edge load, then target gate load, then evaluation); an index adds an address computation to that chain on every edge.
- The gain is CSR (one contiguous edge array, 16-byte gate): with pointer edges it is 8% faster than the current layout overall and 15% faster on the designs of 100k gates or more, faster on 24 of 25 circuits, in the topological placement that `optimize()` produces. With a shuffled placement CSR loses (p/d 1.05), so it must be built after reordering.
- Implication (not implemented): indices for the editable DESIGN form (stable under growth and reordering, the saved form, simple macro side tables); a CSR with pointers built by `optimize()` for SIMULATE mode, in fixed arrays that do not reallocate during simulation. Only measured on this machine and in the harness; the full engine needs its own measurement after a change.

## Packed hitlists (variant q, topological placement)

Variant q is variant d (24-byte gate, the same per-gate pointer lists and the same loop) with every list's data copied into one block in placement order after wiring, as `optimize()` could do after reordering; nothing else changes. Same method as above, 9 repeats, all 25 fingerprints identical.

| circuit | gates | d now | q packed | p CSR 16 B | q/d | p/d | L1 miss/edge d / q / p |
|---|---:|---:|---:|---:|---:|---:|---:|
| c1908 | 938 | 2.98 | 2.87 | 3.05 | 0.963 | 1.023 | 0.46 / 0.06 / 0.02 |
| cavlc | 1,300 | 2.74 | 2.56 | 2.62 | 0.934 | 0.956 | 0.98 / 0.57 / 0.24 |
| c3540 | 1,741 | 3.28 | 3.16 | 3.34 | 0.963 | 1.018 | 0.82 / 0.55 / 0.41 |
| c6288 | 2,480 | 3.55 | 3.44 | 3.53 | 0.969 | 0.994 | 1.16 / 0.88 / 0.61 |
| adder | 2,547 | 3.91 | 3.79 | 3.93 | 0.969 | 1.005 | 1.74 / 1.41 / 1.00 |
| c5315 | 2,608 | 3.40 | 3.29 | 3.43 | 0.968 | 1.009 | 1.19 / 0.85 / 0.63 |
| c7552 | 3,828 | 3.56 | 3.45 | 3.58 | 0.969 | 1.006 | 1.61 / 1.33 / 1.05 |
| bar | 5,526 | 2.44 | 2.23 | 2.29 | 0.914 | 0.939 | 1.91 / 1.36 / 0.99 |
| max | 6,025 | 3.20 | 3.04 | 3.17 | 0.950 | 0.991 | 2.23 / 1.92 / 1.55 |
| des_area | 8,365 | 3.47 | 3.34 | 3.45 | 0.963 | 0.994 | 1.70 / 1.41 / 1.07 |
| b14 | 14,299 | 3.18 | 3.00 | 3.08 | 0.943 | 0.969 | 1.85 / 1.59 / 1.32 |
| tv80 | 15,992 | 2.36 | 2.15 | 2.23 | 0.911 | 0.945 | 2.04 / 1.73 / 1.46 |
| arbiter | 23,618 | 3.06 | 2.75 | 2.67 | 0.899 | 0.873 | 1.77 / 1.41 / 1.34 |
| systemcaes | 24,121 | 2.53 | 2.28 | 2.31 | 0.901 | 0.913 | 1.85 / 1.57 / 1.29 |
| b15 | 24,329 | 2.28 | 2.10 | 2.16 | 0.921 | 0.947 | 1.83 / 1.56 / 1.32 |
| mem_ctrl | 33,041 | 2.45 | 2.17 | 2.23 | 0.886 | 0.910 | 2.01 / 1.74 / 1.47 |
| aes_core | 33,515 | 4.12 | 3.66 | 3.66 | 0.888 | 0.888 | 2.36 / 2.22 / 1.92 |
| usb_funct | 44,472 | 2.83 | 2.45 | 2.43 | 0.866 | 0.859 | 2.13 / 1.81 / 1.58 |
| ac97_ctrl | 52,054 | 2.62 | 2.21 | 2.22 | 0.844 | 0.847 | 1.99 / 1.74 / 1.48 |
| wb_conmax | 60,876 | 3.19 | 2.80 | 2.70 | 0.878 | 0.846 | 2.08 / 1.88 / 1.60 |
| b17 | 73,475 | 2.69 | 2.39 | 2.33 | 0.888 | 0.866 | 1.86 / 1.71 / 1.44 |
| b18 | 182,380 | 3.29 | 2.89 | 2.95 | 0.878 | 0.897 | 1.86 / 1.68 / 1.42 |
| des_perf | 243,901 | 5.75 | 4.81 | 4.60 | 0.837 | 0.800 | 2.43 / 2.29 / 2.08 |
| b19 | 356,399 | 3.39 | 2.91 | 2.87 | 0.858 | 0.847 | 1.86 / 1.70 / 1.44 |
| vga_lcd | 443,630 | 3.05 | 2.57 | 2.63 | 0.843 | 0.862 | 2.08 / 1.77 / 1.52 |
- q/d: geomean 0.911 [0.837, 0.969], below 1 on 25/25; under 10k gates 0.956; 10k-100k 0.893; 100k or more 0.854
- p/d: geomean 0.926 [0.800, 1.023], below 1 on 20/25; under 10k gates 0.993; 10k-100k 0.896; 100k or more 0.851

Reading: packing alone captures all of the CSR gain (median 103% of p's gain on the circuits of 10k gates or more) and is faster than the current layout on all 25 circuits, so the gain is contiguous edges in visit order, not the smaller gate or flattening. It needs no change to the gate struct, the hot loop or editing: `optimize()` packs the lists into one block after reordering, `HitList` marks block-owned data and copies out instead of `realloc` on growth and skips `free` for it; connect and disconnect stay O(1) amortized and the next `optimize()` repacks. This supersedes the 'Implication' bullet above (indices plus a CSR build). Harness only; the full engine needs its own measurement after a change.

## Correction: how the harness's d relates to the real engine (measured later on 2026-10-22)

`Circuit.hitlist_mem_layout()` on b15 and b19 (JSON load, as the app loads circuits) shows where the engine's lists actually sit. Before `optimize()` they are scattered (18% of consecutive gates' lists adjacent, 34% going backwards), which is what variant d models. After `optimize()` on a clean heap they are already in gate order (98% adjacent, separated only by 16-byte malloc headers), because `optimize()` copies every list into a fresh allocation in the new order. On a heap fragmented with list-sized holes (24-64 B blocks freed in a scattered pattern, as in a long interactive session) the same `optimize()` leaves only 52% adjacent and 24% going backwards. So the q/d gain above is the gain over an unordered layout; the real engine after `optimize()` is close to q on a clean heap (the remaining gain is removing the headers) and in between on a fragmented one. Packing's value is guaranteeing the ordered layout regardless of heap state; its real-engine gain has to be measured on a scratch build (clean and fragmented heap).
