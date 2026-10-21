# Ablation harness on the laptop, real netlists and synthetic sweep

## Ablation harness on the real ITC99 netlists (9 repeats, topological placement)

Source: raw log `abl_real.log` (not kept) (converted from the raw harness output; columns as printed by `tests/ablation_layout.cpp`).

#### topology=netlist gates=14299 inputs=0 window=64 placement=topological frag=0 activity=0.10 iters=905 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 11.76 | 11.58 | 12.86 | 10.8% | 47.24 | 1.04 | 0.6355 | 2.4227 | x1.000 |
| b arena+virtual | 40 | 12.37 | 11.58 | 13.02 | 11.6% | 49.68 | 0.99 | 0.6637 | 2.3489 | x1.035 |
| c flat24+switch | 24 | 9.67 | 9.23 | 10.39 | 12.0% | 38.95 | 1.28 | 0.5158 | 1.9308 | x0.808 |
| d flat24+SIMA | 24 | 6.11 | 6.04 | 6.16 | 2.0% | 24.58 | 1.86 | 0.2353 | 1.9096 | x0.520 |
| g flat40+SIMA | 40 | 7.10 | 6.98 | 8.73 | 24.6% | 28.51 | 1.60 | 0.2344 | 2.2199 | x0.603 |
| e flat32+SIMA | 32 | 6.45 | 6.42 | 6.70 | 4.3% | 25.89 | 1.77 | 0.2333 | 2.0333 | x0.549 |

evals/rep=8282911 changed/rep=3894295 fingerprint-check=identical

#### topology=netlist gates=24329 inputs=0 window=64 placement=topological frag=0 activity=0.10 iters=1253 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 8.51 | 8.39 | 9.49 | 12.9% | 34.11 | 1.43 | 0.1869 | 2.4175 | x1.000 |
| b arena+virtual | 40 | 8.13 | 8.03 | 9.52 | 18.4% | 32.69 | 1.49 | 0.1850 | 2.4147 | x0.958 |
| c flat24+switch | 24 | 6.42 | 6.34 | 7.20 | 13.3% | 25.82 | 1.90 | 0.1246 | 1.9553 | x0.755 |
| d flat24+SIMA | 24 | 5.24 | 5.15 | 6.16 | 19.3% | 21.08 | 2.14 | 0.0300 | 1.9684 | x0.612 |
| g flat40+SIMA | 40 | 6.32 | 6.26 | 6.58 | 5.1% | 25.42 | 1.78 | 0.0302 | 2.3119 | x0.739 |
| e flat32+SIMA | 32 | 5.95 | 5.86 | 6.01 | 2.5% | 23.97 | 1.89 | 0.0289 | 2.1885 | x0.700 |

evals/rep=7632954 changed/rep=3397255 fingerprint-check=identical

#### topology=netlist gates=73475 inputs=0 window=64 placement=topological frag=0 activity=0.10 iters=401 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 9.05 | 9.00 | 9.15 | 1.7% | 36.27 | 1.34 | 0.1695 | 2.4865 | x1.000 |
| b arena+virtual | 40 | 9.34 | 9.11 | 9.78 | 7.2% | 37.50 | 1.30 | 0.1750 | 2.4242 | x1.030 |
| c flat24+switch | 24 | 7.38 | 7.26 | 9.01 | 23.7% | 29.70 | 1.65 | 0.1135 | 1.9846 | x0.815 |
| d flat24+SIMA | 24 | 6.11 | 6.08 | 6.16 | 1.3% | 24.59 | 1.83 | 0.0359 | 2.0032 | x0.674 |
| g flat40+SIMA | 40 | 6.89 | 6.76 | 8.84 | 30.2% | 27.71 | 1.63 | 0.0313 | 2.3426 | x0.759 |
| e flat32+SIMA | 32 | 6.84 | 6.77 | 6.88 | 1.6% | 27.51 | 1.64 | 0.0293 | 2.2048 | x0.753 |

evals/rep=7253246 changed/rep=3253798 fingerprint-check=identical

#### topology=netlist gates=182380 inputs=0 window=64 placement=topological frag=0 activity=0.10 iters=145 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 11.13 | 10.90 | 11.20 | 2.7% | 44.68 | 1.10 | 0.3336 | 2.5080 | x1.000 |
| b arena+virtual | 40 | 10.92 | 10.49 | 11.16 | 6.1% | 43.87 | 1.12 | 0.3384 | 2.4264 | x0.983 |
| c flat24+switch | 24 | 8.95 | 8.68 | 9.00 | 3.5% | 36.03 | 1.38 | 0.2673 | 1.9991 | x0.803 |
| d flat24+SIMA | 24 | 7.10 | 7.02 | 7.22 | 2.9% | 28.48 | 1.60 | 0.1150 | 1.9627 | x0.642 |
| g flat40+SIMA | 40 | 7.59 | 7.56 | 7.79 | 3.0% | 30.49 | 1.50 | 0.1152 | 2.3112 | x0.687 |
| e flat32+SIMA | 32 | 7.57 | 7.02 | 7.69 | 8.9% | 30.46 | 1.50 | 0.1136 | 2.0689 | x0.678 |

evals/rep=7255013 changed/rep=3489574 fingerprint-check=identical

#### topology=netlist gates=356399 inputs=0 window=64 placement=topological frag=0 activity=0.10 iters=67 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 12.44 | 11.99 | 13.78 | 14.3% | 50.04 | 0.98 | 0.2070 | 2.4747 | x1.000 |
| b arena+virtual | 40 | 12.64 | 11.02 | 12.78 | 13.9% | 50.82 | 0.96 | 0.2070 | 2.4088 | x1.016 |
| c flat24+switch | 24 | 9.53 | 8.50 | 10.07 | 16.5% | 38.33 | 1.29 | 0.1638 | 1.9936 | x0.773 |
| d flat24+SIMA | 24 | 8.78 | 7.44 | 8.92 | 16.9% | 35.39 | 1.28 | 0.0690 | 1.9605 | x0.705 |
| g flat40+SIMA | 40 | 9.93 | 9.81 | 10.01 | 2.0% | 40.06 | 1.13 | 0.0690 | 2.3033 | x0.797 |
| e flat32+SIMA | 32 | 9.29 | 9.11 | 9.53 | 4.4% | 37.46 | 1.21 | 0.0681 | 2.1902 | x0.754 |

evals/rep=6047063 changed/rep=2817672 fingerprint-check=identical

## Ablation harness, synthetic sweep (chain, tree, random, mixchain; topological and shuffled+fragmented; plus a `--vary` run)

Source: raw log `abl_synth.log` (not kept) (converted from the raw harness output; columns as printed by `tests/ablation_layout.cpp`).

#### topology=chain gates=1000 inputs=1 window=64 placement=topological frag=0 activity=0.10 iters=8008 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 6.93 | 6.92 | 6.96 | 0.6% | 27.83 | 2.63 | 0.0010 | 1.5070 | x1.000 |
| b arena+virtual | 40 | 6.99 | 6.98 | 7.10 | 1.8% | 28.08 | 2.60 | 0.0010 | 1.3790 | x1.009 |
| c flat24+switch | 24 | 4.80 | 4.80 | 4.93 | 2.8% | 19.29 | 3.94 | 0.0010 | 1.1338 | x0.693 |
| d flat24+SIMA | 24 | 4.89 | 4.86 | 4.90 | 0.9% | 19.66 | 3.57 | 0.0010 | 1.1271 | x0.706 |
| g flat40+SIMA | 40 | 4.85 | 4.85 | 4.89 | 0.8% | 19.48 | 3.70 | 0.0010 | 1.3786 | x0.700 |
| e flat32+SIMA | 32 | 4.73 | 4.72 | 4.75 | 0.5% | 18.99 | 3.80 | 0.0010 | 1.2521 | x0.682 |

evals/rep=7999992 changed/rep=7999992 fingerprint-check=identical

#### topology=chain gates=1000 inputs=1 window=64 placement=shuffled frag=192 activity=0.10 iters=8008 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 7.20 | 7.19 | 7.21 | 0.2% | 28.92 | 2.53 | 0.0010 | 2.4155 | x1.000 |
| b arena+virtual | 40 | 7.21 | 7.18 | 7.24 | 0.8% | 28.92 | 2.53 | 0.0010 | 1.8231 | x1.002 |
| c flat24+switch | 24 | 5.06 | 5.06 | 5.11 | 0.9% | 20.33 | 3.74 | 0.0010 | 1.3253 | x0.703 |
| d flat24+SIMA | 24 | 4.91 | 4.91 | 4.96 | 1.1% | 19.75 | 3.55 | 0.0010 | 1.3203 | x0.683 |
| g flat40+SIMA | 40 | 5.46 | 5.45 | 5.47 | 0.5% | 21.97 | 3.28 | 0.0010 | 1.6841 | x0.758 |
| e flat32+SIMA | 32 | 5.34 | 5.34 | 5.40 | 1.3% | 21.50 | 3.35 | 0.0010 | 1.4338 | x0.742 |

evals/rep=7999992 changed/rep=7999992 fingerprint-check=identical

#### topology=chain gates=10000 inputs=1 window=64 placement=topological frag=0 activity=0.10 iters=800 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 6.98 | 6.97 | 6.99 | 0.2% | 27.97 | 2.61 | 0.0001 | 1.5040 | x1.000 |
| b arena+virtual | 40 | 7.01 | 7.00 | 7.07 | 1.0% | 28.10 | 2.60 | 0.0001 | 1.3830 | x1.005 |
| c flat24+switch | 24 | 5.06 | 5.05 | 5.08 | 0.5% | 20.29 | 3.75 | 0.0001 | 1.1344 | x0.725 |
| d flat24+SIMA | 24 | 5.18 | 5.16 | 5.22 | 1.1% | 20.77 | 3.37 | 0.0001 | 1.1290 | x0.742 |
| g flat40+SIMA | 40 | 4.77 | 4.77 | 4.78 | 0.3% | 19.11 | 3.77 | 0.0001 | 1.3802 | x0.684 |
| e flat32+SIMA | 32 | 4.80 | 4.80 | 4.80 | 0.2% | 19.24 | 3.74 | 0.0001 | 1.2554 | x0.688 |

evals/rep=7999200 changed/rep=7999200 fingerprint-check=identical

#### topology=chain gates=10000 inputs=1 window=64 placement=shuffled frag=192 activity=0.10 iters=800 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 15.27 | 15.25 | 15.39 | 0.9% | 61.64 | 1.18 | 0.0001 | 2.4421 | x1.000 |
| b arena+virtual | 40 | 10.71 | 9.76 | 10.78 | 9.6% | 43.13 | 1.69 | 0.0001 | 2.3485 | x0.701 |
| c flat24+switch | 24 | 7.43 | 7.41 | 7.66 | 3.4% | 29.86 | 2.55 | 0.0001 | 1.9456 | x0.486 |
| d flat24+SIMA | 24 | 7.31 | 7.29 | 7.40 | 1.5% | 29.40 | 2.38 | 0.0001 | 1.9463 | x0.478 |
| g flat40+SIMA | 40 | 10.96 | 10.93 | 11.05 | 1.1% | 44.21 | 1.63 | 0.0001 | 1.9853 | x0.718 |
| e flat32+SIMA | 32 | 9.80 | 9.78 | 9.82 | 0.4% | 39.58 | 1.82 | 0.0001 | 1.7321 | x0.642 |

evals/rep=7999200 changed/rep=7999200 fingerprint-check=identical

#### topology=chain gates=100000 inputs=1 window=64 placement=topological frag=0 activity=0.10 iters=80 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 7.06 | 7.03 | 7.19 | 2.3% | 28.32 | 2.58 | 0.0000 | 1.5091 | x1.000 |
| b arena+virtual | 40 | 7.06 | 7.04 | 7.14 | 1.5% | 28.28 | 2.58 | 0.0000 | 1.3866 | x1.002 |
| c flat24+switch | 24 | 5.05 | 5.03 | 5.18 | 3.0% | 20.22 | 3.76 | 0.0000 | 1.1292 | x0.718 |
| d flat24+SIMA | 24 | 5.21 | 5.15 | 5.25 | 1.9% | 20.92 | 3.35 | 0.0000 | 1.1281 | x0.737 |
| g flat40+SIMA | 40 | 4.93 | 4.87 | 5.01 | 2.7% | 19.76 | 3.64 | 0.0000 | 1.3829 | x0.699 |
| e flat32+SIMA | 32 | 4.80 | 4.78 | 4.95 | 3.6% | 19.19 | 3.75 | 0.0000 | 1.2556 | x0.679 |

evals/rep=7999920 changed/rep=7999920 fingerprint-check=identical

#### topology=chain gates=100000 inputs=1 window=64 placement=shuffled frag=192 activity=0.10 iters=80 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 36.90 | 31.46 | 40.04 | 23.3% | 149.39 | 0.49 | 0.0001 | 2.4371 | x1.000 |
| b arena+virtual | 40 | 14.56 | 14.46 | 15.74 | 8.8% | 58.82 | 1.24 | 0.0000 | 2.4012 | x0.397 |
| c flat24+switch | 24 | 14.90 | 14.87 | 14.95 | 0.5% | 60.19 | 1.26 | 0.0000 | 2.0008 | x0.404 |
| d flat24+SIMA | 24 | 14.61 | 14.56 | 14.76 | 1.4% | 59.00 | 1.19 | 0.0000 | 2.0006 | x0.398 |
| g flat40+SIMA | 40 | 14.73 | 14.56 | 14.90 | 2.3% | 59.55 | 1.21 | 0.0000 | 2.0059 | x0.395 |
| e flat32+SIMA | 32 | 13.92 | 13.74 | 14.04 | 2.2% | 56.23 | 1.28 | 0.0000 | 1.7531 | x0.374 |

evals/rep=7999920 changed/rep=7999920 fingerprint-check=identical

#### topology=chain gates=1000000 inputs=1 window=64 placement=topological frag=0 activity=0.10 iters=8 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 8.73 | 8.70 | 8.86 | 1.8% | 34.79 | 2.10 | 0.0000 | 1.5051 | x1.000 |
| b arena+virtual | 40 | 8.11 | 8.07 | 8.31 | 3.0% | 32.16 | 2.27 | 0.0000 | 1.3847 | x0.929 |
| c flat24+switch | 24 | 6.49 | 6.47 | 6.50 | 0.5% | 25.80 | 2.95 | 0.0000 | 1.1330 | x0.743 |
| d flat24+SIMA | 24 | 6.47 | 6.46 | 6.66 | 3.1% | 26.03 | 2.69 | 0.0000 | 1.1285 | x0.741 |
| g flat40+SIMA | 40 | 7.53 | 7.51 | 7.55 | 0.5% | 30.18 | 2.39 | 0.0000 | 1.3829 | x0.863 |
| e flat32+SIMA | 32 | 7.08 | 7.08 | 7.10 | 0.2% | 28.48 | 2.53 | 0.0000 | 1.2558 | x0.812 |

evals/rep=7999992 changed/rep=7999992 fingerprint-check=identical

#### topology=chain gates=1000000 inputs=1 window=64 placement=shuffled frag=192 activity=0.10 iters=8 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 116.03 | 113.56 | 116.69 | 2.7% | 472.63 | 0.15 | 0.0001 | 2.4387 | x1.000 |
| b arena+virtual | 40 | 83.20 | 81.96 | 85.35 | 4.1% | 338.87 | 0.22 | 0.0001 | 2.4100 | x0.724 |
| c flat24+switch | 24 | 62.77 | 61.14 | 66.54 | 8.6% | 255.47 | 0.30 | 0.0001 | 2.0068 | x0.539 |
| d flat24+SIMA | 24 | 60.44 | 58.51 | 62.32 | 6.3% | 246.06 | 0.28 | 0.0001 | 2.0057 | x0.520 |
| g flat40+SIMA | 40 | 84.51 | 83.01 | 85.79 | 3.3% | 343.65 | 0.21 | 0.0001 | 2.0074 | x0.728 |
| e flat32+SIMA | 32 | 73.77 | 72.84 | 76.68 | 5.2% | 301.05 | 0.24 | 0.0001 | 1.7560 | x0.643 |

evals/rep=7999992 changed/rep=7999992 fingerprint-check=identical

#### topology=tree gates=1023 inputs=512 window=64 placement=topological frag=0 activity=0.10 iters=36925 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 6.67 | 6.66 | 6.81 | 2.1% | 26.89 | 2.53 | 0.0433 | 3.0465 | x1.000 |
| b arena+virtual | 40 | 6.90 | 6.77 | 7.98 | 17.6% | 27.77 | 2.45 | 0.0436 | 2.8512 | x1.033 |
| c flat24+switch | 24 | 6.43 | 5.77 | 7.45 | 26.0% | 26.03 | 2.63 | 0.0406 | 2.2124 | x0.964 |
| d flat24+SIMA | 24 | 5.39 | 5.38 | 5.89 | 9.5% | 21.77 | 2.96 | 0.0409 | 2.2012 | x0.807 |
| g flat40+SIMA | 40 | 5.67 | 5.66 | 5.70 | 0.7% | 22.87 | 2.82 | 0.0433 | 2.6773 | x0.849 |
| e flat32+SIMA | 32 | 5.74 | 5.74 | 5.75 | 0.2% | 23.20 | 2.78 | 0.0430 | 2.3084 | x0.860 |

evals/rep=8029688 changed/rep=7102064 fingerprint-check=identical

#### topology=tree gates=1023 inputs=512 window=64 placement=shuffled frag=192 activity=0.10 iters=36925 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 6.80 | 6.79 | 7.83 | 15.3% | 27.41 | 2.48 | 0.0408 | 2.9345 | x1.000 |
| b arena+virtual | 40 | 6.65 | 6.63 | 8.64 | 30.2% | 26.77 | 2.54 | 0.0430 | 2.6175 | x0.977 |
| c flat24+switch | 24 | 6.67 | 5.82 | 7.43 | 24.2% | 26.58 | 2.58 | 0.0403 | 2.0512 | x0.980 |
| d flat24+SIMA | 24 | 5.42 | 5.41 | 6.50 | 20.3% | 21.85 | 2.95 | 0.0409 | 2.0418 | x0.797 |
| g flat40+SIMA | 40 | 5.76 | 5.74 | 7.25 | 26.1% | 23.21 | 2.78 | 0.0435 | 2.3472 | x0.845 |
| e flat32+SIMA | 32 | 5.87 | 5.86 | 6.82 | 16.4% | 23.69 | 2.72 | 0.0409 | 1.9710 | x0.863 |

evals/rep=8029688 changed/rep=7102064 fingerprint-check=identical

#### topology=tree gates=16383 inputs=8192 window=64 placement=topological frag=0 activity=0.10 iters=2291 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 9.08 | 8.93 | 10.47 | 17.0% | 35.93 | 1.88 | 0.0039 | 5.0107 | x1.000 |
| b arena+virtual | 40 | 9.21 | 9.08 | 9.45 | 4.0% | 36.56 | 1.84 | 0.0038 | 4.8050 | x1.016 |
| c flat24+switch | 24 | 7.60 | 7.55 | 8.60 | 13.8% | 30.44 | 2.22 | 0.0039 | 4.1902 | x0.837 |
| d flat24+SIMA | 24 | 7.14 | 7.08 | 7.46 | 5.3% | 28.53 | 2.23 | 0.0038 | 4.1855 | x0.786 |
| g flat40+SIMA | 40 | 8.06 | 7.98 | 8.61 | 7.9% | 32.20 | 1.98 | 0.0038 | 4.6158 | x0.888 |
| e flat32+SIMA | 32 | 7.88 | 7.83 | 8.63 | 10.1% | 31.64 | 2.01 | 0.0038 | 4.2703 | x0.865 |

evals/rep=8022504 changed/rep=7084401 fingerprint-check=identical

#### topology=tree gates=16383 inputs=8192 window=64 placement=shuffled frag=192 activity=0.10 iters=2291 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 12.24 | 12.16 | 12.41 | 2.0% | 49.27 | 1.37 | 0.0039 | 4.4961 | x1.000 |
| b arena+virtual | 40 | 11.22 | 11.14 | 16.50 | 47.7% | 45.07 | 1.50 | 0.0038 | 4.4795 | x0.919 |
| c flat24+switch | 24 | 13.20 | 9.85 | 14.73 | 36.9% | 53.40 | 1.27 | 0.0039 | 4.1323 | x1.075 |
| d flat24+SIMA | 24 | 9.23 | 9.09 | 14.45 | 58.1% | 37.27 | 1.71 | 0.0038 | 4.1234 | x0.753 |
| g flat40+SIMA | 40 | 15.21 | 14.35 | 16.39 | 13.5% | 61.55 | 1.03 | 0.0038 | 4.1767 | x1.249 |
| e flat32+SIMA | 32 | 10.13 | 10.08 | 10.24 | 1.6% | 40.96 | 1.55 | 0.0037 | 3.8867 | x0.830 |

evals/rep=8022504 changed/rep=7084401 fingerprint-check=identical

#### topology=tree gates=131071 inputs=65536 window=64 placement=topological frag=0 activity=0.10 iters=286 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 12.48 | 12.34 | 13.01 | 5.3% | 50.13 | 1.34 | 0.0006 | 5.0490 | x1.000 |
| b arena+virtual | 40 | 10.48 | 10.34 | 10.64 | 2.9% | 41.53 | 1.62 | 0.0006 | 4.8356 | x0.840 |
| c flat24+switch | 24 | 8.55 | 8.32 | 8.69 | 4.3% | 34.04 | 1.99 | 0.0006 | 4.2177 | x0.687 |
| d flat24+SIMA | 24 | 8.12 | 7.93 | 8.42 | 6.0% | 32.35 | 1.97 | 0.0006 | 4.2118 | x0.652 |
| g flat40+SIMA | 40 | 9.43 | 9.31 | 9.75 | 4.7% | 37.80 | 1.68 | 0.0006 | 4.6617 | x0.756 |
| e flat32+SIMA | 32 | 9.24 | 9.20 | 9.45 | 2.8% | 37.12 | 1.71 | 0.0006 | 4.2926 | x0.741 |

evals/rep=8015372 changed/rep=7077454 fingerprint-check=identical

#### topology=tree gates=131071 inputs=65536 window=64 placement=shuffled frag=192 activity=0.10 iters=286 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 30.27 | 30.13 | 30.62 | 1.6% | 122.23 | 0.55 | 0.0006 | 4.5248 | x1.000 |
| b arena+virtual | 40 | 15.27 | 15.25 | 15.31 | 0.4% | 61.58 | 1.09 | 0.0006 | 4.5587 | x0.505 |
| c flat24+switch | 24 | 14.36 | 14.33 | 20.59 | 43.6% | 57.96 | 1.17 | 0.0006 | 4.2172 | x0.476 |
| d flat24+SIMA | 24 | 14.11 | 13.63 | 14.13 | 3.6% | 56.98 | 1.12 | 0.0006 | 4.2255 | x0.466 |
| g flat40+SIMA | 40 | 15.23 | 14.70 | 16.03 | 8.8% | 61.28 | 1.04 | 0.0006 | 4.2431 | x0.504 |
| e flat32+SIMA | 32 | 13.75 | 13.67 | 14.22 | 4.0% | 55.39 | 1.15 | 0.0006 | 3.9481 | x0.454 |

evals/rep=8015372 changed/rep=7077454 fingerprint-check=identical

#### topology=tree gates=1048575 inputs=524288 window=64 placement=topological frag=0 activity=0.10 iters=35 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 44.41 | 44.19 | 45.17 | 2.2% | 180.26 | 0.37 | 0.0001 | 4.9966 | x1.000 |
| b arena+virtual | 40 | 39.27 | 39.11 | 39.41 | 0.8% | 159.12 | 0.42 | 0.0001 | 4.8144 | x0.885 |
| c flat24+switch | 24 | 31.64 | 31.60 | 32.02 | 1.3% | 128.45 | 0.53 | 0.0001 | 4.2125 | x0.712 |
| d flat24+SIMA | 24 | 31.11 | 31.07 | 31.32 | 0.8% | 126.22 | 0.50 | 0.0001 | 4.2088 | x0.700 |
| g flat40+SIMA | 40 | 39.56 | 39.39 | 39.87 | 1.2% | 160.63 | 0.40 | 0.0001 | 4.6267 | x0.892 |
| e flat32+SIMA | 32 | 36.38 | 36.28 | 37.15 | 2.4% | 147.62 | 0.43 | 0.0001 | 4.2681 | x0.821 |

evals/rep=7850048 changed/rep=6931240 fingerprint-check=identical

#### topology=tree gates=1048575 inputs=524288 window=64 placement=shuffled frag=192 activity=0.10 iters=35 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 79.09 | 76.47 | 80.23 | 4.8% | 321.64 | 0.21 | 0.0002 | 4.5387 | x1.000 |
| b arena+virtual | 40 | 64.56 | 62.72 | 65.08 | 3.7% | 261.87 | 0.26 | 0.0002 | 4.5293 | x0.814 |
| c flat24+switch | 24 | 57.94 | 56.98 | 87.24 | 52.2% | 235.29 | 0.29 | 0.0002 | 4.1811 | x0.733 |
| d flat24+SIMA | 24 | 53.63 | 52.54 | 54.51 | 3.7% | 217.95 | 0.29 | 0.0002 | 4.1880 | x0.679 |
| g flat40+SIMA | 40 | 61.53 | 60.31 | 65.66 | 8.7% | 250.22 | 0.25 | 0.0002 | 4.2037 | x0.802 |
| e flat32+SIMA | 32 | 60.44 | 55.82 | 60.96 | 8.5% | 245.66 | 0.26 | 0.0002 | 3.9012 | x0.763 |

evals/rep=7850048 changed/rep=6931240 fingerprint-check=identical

#### topology=random gates=1000 inputs=100 window=64 placement=topological frag=0 activity=0.10 iters=14094 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 15.20 | 15.15 | 15.64 | 3.2% | 61.42 | 0.88 | 1.3930 | 1.1765 | x1.000 |
| b arena+virtual | 40 | 16.09 | 16.01 | 16.22 | 1.3% | 64.87 | 0.83 | 1.3911 | 1.1042 | x1.057 |
| c flat24+switch | 24 | 13.95 | 13.87 | 14.07 | 1.4% | 56.48 | 0.97 | 1.2666 | 0.7208 | x0.917 |
| d flat24+SIMA | 24 | 7.77 | 7.75 | 7.82 | 0.9% | 31.45 | 1.61 | 0.6472 | 0.7032 | x0.511 |
| g flat40+SIMA | 40 | 8.13 | 8.10 | 8.14 | 0.5% | 32.87 | 1.54 | 0.6392 | 0.9467 | x0.534 |
| e flat32+SIMA | 32 | 8.10 | 8.07 | 8.11 | 0.5% | 32.75 | 1.54 | 0.6373 | 0.7880 | x0.532 |

evals/rep=8107270 changed/rep=5753494 fingerprint-check=identical

#### topology=random gates=1000 inputs=100 window=64 placement=shuffled frag=192 activity=0.10 iters=13943 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 15.64 | 15.58 | 15.97 | 2.5% | 63.04 | 0.86 | 1.4148 | 1.3768 | x1.000 |
| b arena+virtual | 40 | 15.71 | 15.56 | 16.15 | 3.7% | 63.36 | 0.85 | 1.4145 | 1.1065 | x1.005 |
| c flat24+switch | 24 | 14.02 | 13.96 | 14.02 | 0.4% | 56.69 | 0.97 | 1.2638 | 0.7567 | x0.895 |
| d flat24+SIMA | 24 | 7.80 | 7.76 | 7.84 | 1.1% | 31.51 | 1.60 | 0.6407 | 0.7277 | x0.499 |
| g flat40+SIMA | 40 | 8.23 | 8.21 | 8.27 | 0.7% | 33.23 | 1.52 | 0.6394 | 0.9326 | x0.526 |
| e flat32+SIMA | 32 | 8.11 | 8.08 | 8.13 | 0.6% | 32.78 | 1.54 | 0.6373 | 0.7587 | x0.518 |

evals/rep=8026224 changed/rep=5696792 fingerprint-check=identical

#### topology=random gates=10000 inputs=1000 window=64 placement=topological frag=0 activity=0.10 iters=175 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 17.76 | 17.60 | 17.99 | 2.2% | 71.66 | 0.74 | 1.3655 | 2.6404 | x1.000 |
| b arena+virtual | 40 | 17.71 | 17.63 | 17.99 | 2.1% | 71.31 | 0.74 | 1.3647 | 2.6943 | x1.000 |
| c flat24+switch | 24 | 15.48 | 15.33 | 16.09 | 4.9% | 62.45 | 0.85 | 1.2352 | 2.3204 | x0.872 |
| d flat24+SIMA | 24 | 8.30 | 8.29 | 8.37 | 1.0% | 33.51 | 1.46 | 0.5753 | 2.2632 | x0.470 |
| g flat40+SIMA | 40 | 8.43 | 8.40 | 8.49 | 1.0% | 34.05 | 1.44 | 0.5769 | 2.3810 | x0.476 |
| e flat32+SIMA | 32 | 8.32 | 8.30 | 8.35 | 0.7% | 33.58 | 1.46 | 0.5765 | 2.1750 | x0.470 |

evals/rep=6394279 changed/rep=4383288 fingerprint-check=identical

#### topology=random gates=10000 inputs=1000 window=64 placement=shuffled frag=192 activity=0.10 iters=205 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 20.78 | 20.76 | 20.83 | 0.4% | 83.83 | 0.63 | 1.3551 | 2.6968 | x1.000 |
| b arena+virtual | 40 | 19.10 | 19.07 | 19.26 | 1.0% | 76.97 | 0.68 | 1.3518 | 2.7529 | x0.919 |
| c flat24+switch | 24 | 15.73 | 15.58 | 16.48 | 5.7% | 63.49 | 0.84 | 1.2350 | 2.4100 | x0.757 |
| d flat24+SIMA | 24 | 8.60 | 8.53 | 8.73 | 2.3% | 34.73 | 1.41 | 0.5754 | 2.3723 | x0.414 |
| g flat40+SIMA | 40 | 9.16 | 9.14 | 11.01 | 20.4% | 36.94 | 1.33 | 0.5767 | 2.4122 | x0.440 |
| e flat32+SIMA | 32 | 9.73 | 9.64 | 9.85 | 2.2% | 39.32 | 1.25 | 0.5762 | 2.2045 | x0.468 |

evals/rep=7518431 changed/rep=5153560 fingerprint-check=identical

#### topology=random gates=100000 inputs=10000 window=64 placement=topological frag=0 activity=0.10 iters=6 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 25.19 | 24.90 | 25.72 | 3.3% | 101.50 | 0.52 | 1.3989 | 2.9129 | x1.000 |
| b arena+virtual | 40 | 24.03 | 23.70 | 24.39 | 2.8% | 96.74 | 0.54 | 1.3990 | 2.9939 | x0.950 |
| c flat24+switch | 24 | 22.37 | 22.21 | 22.99 | 3.5% | 90.42 | 0.58 | 1.2739 | 2.6860 | x0.891 |
| d flat24+SIMA | 24 | 15.11 | 14.88 | 16.06 | 7.8% | 61.16 | 0.80 | 0.5759 | 2.6015 | x0.601 |
| g flat40+SIMA | 40 | 16.33 | 16.08 | 16.48 | 2.4% | 66.11 | 0.74 | 0.5771 | 2.6386 | x0.650 |
| e flat32+SIMA | 32 | 15.31 | 14.81 | 15.54 | 4.8% | 62.02 | 0.79 | 0.5771 | 2.4461 | x0.610 |

evals/rep=10161642 changed/rep=6892841 fingerprint-check=identical

#### topology=random gates=100000 inputs=10000 window=64 placement=shuffled frag=192 activity=0.10 iters=4 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 25.65 | 25.45 | 30.24 | 18.6% | 103.45 | 0.51 | 1.3911 | 2.9067 | x1.000 |
| b arena+virtual | 40 | 26.20 | 25.97 | 26.48 | 2.0% | 105.53 | 0.50 | 1.3942 | 3.0015 | x1.020 |
| c flat24+switch | 24 | 25.17 | 24.79 | 25.66 | 3.5% | 101.63 | 0.52 | 1.2717 | 2.7111 | x0.981 |
| d flat24+SIMA | 24 | 17.36 | 17.12 | 17.79 | 3.9% | 70.25 | 0.69 | 0.5778 | 2.6459 | x0.677 |
| g flat40+SIMA | 40 | 18.67 | 18.47 | 19.19 | 3.9% | 75.58 | 0.64 | 0.5772 | 2.6491 | x0.729 |
| e flat32+SIMA | 32 | 16.13 | 15.58 | 16.46 | 5.4% | 65.23 | 0.75 | 0.5768 | 2.4599 | x0.613 |

evals/rep=5633704 changed/rep=3836175 fingerprint-check=identical

#### topology=random gates=1000000 inputs=100000 window=64 placement=topological frag=0 activity=0.10 iters=1 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 63.57 | 58.73 | 68.42 | 15.2% | 258.36 | 0.20 | 1.3480 | 2.9424 | x1.000 |
| b arena+virtual | 40 | 64.60 | 61.45 | 66.14 | 7.2% | 261.94 | 0.20 | 1.3284 | 3.0162 | x1.009 |
| c flat24+switch | 24 | 64.81 | 60.14 | 66.20 | 9.3% | 263.31 | 0.20 | 1.2848 | 2.7218 | x1.009 |
| d flat24+SIMA | 24 | 53.46 | 50.83 | 55.29 | 8.3% | 217.61 | 0.22 | 0.5875 | 2.6305 | x0.847 |
| g flat40+SIMA | 40 | 64.18 | 60.86 | 67.68 | 10.6% | 261.39 | 0.19 | 0.5869 | 2.6608 | x1.014 |
| e flat32+SIMA | 32 | 59.24 | 53.28 | 62.78 | 16.0% | 241.19 | 0.20 | 0.5876 | 2.4693 | x0.932 |

evals/rep=26234265 changed/rep=17836696 fingerprint-check=identical

#### topology=random gates=1000000 inputs=100000 window=64 placement=shuffled frag=192 activity=0.10 iters=1 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 77.22 | 75.27 | 82.02 | 8.7% | 313.95 | 0.17 | 1.3222 | 2.9170 | x1.000 |
| b arena+virtual | 40 | 69.30 | 68.43 | 70.05 | 2.3% | 281.70 | 0.19 | 1.3168 | 3.0263 | x0.887 |
| c flat24+switch | 24 | 73.48 | 70.82 | 76.43 | 7.6% | 298.97 | 0.18 | 1.2745 | 2.7463 | x0.952 |
| d flat24+SIMA | 24 | 62.30 | 59.61 | 63.45 | 6.2% | 253.67 | 0.19 | 0.5879 | 2.6631 | x0.799 |
| g flat40+SIMA | 40 | 70.82 | 68.73 | 72.35 | 5.1% | 288.33 | 0.17 | 0.5870 | 2.6694 | x0.906 |
| e flat32+SIMA | 32 | 66.08 | 62.83 | 67.64 | 7.3% | 269.14 | 0.18 | 0.5878 | 2.4875 | x0.844 |

evals/rep=24243143 changed/rep=16437945 fingerprint-check=identical

#### topology=mixchain gates=1018 inputs=18 window=64 placement=topological frag=0 activity=0.10 iters=8000 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 11.93 | 11.88 | 11.95 | 0.6% | 48.12 | 1.52 | 0.8640 | 1.5370 | x1.000 |
| b arena+virtual | 40 | 11.91 | 11.89 | 12.02 | 1.1% | 48.02 | 1.52 | 0.8647 | 1.4050 | x0.998 |
| c flat24+switch | 24 | 9.86 | 9.85 | 9.93 | 0.9% | 39.77 | 1.92 | 0.6639 | 1.1480 | x0.827 |
| d flat24+SIMA | 24 | 4.99 | 4.98 | 5.02 | 1.0% | 20.12 | 3.48 | 0.0010 | 1.1485 | x0.419 |
| g flat40+SIMA | 40 | 4.80 | 4.78 | 4.81 | 0.6% | 19.35 | 3.73 | 0.0010 | 1.4066 | x0.403 |
| e flat32+SIMA | 32 | 4.70 | 4.69 | 4.71 | 0.4% | 18.96 | 3.80 | 0.0010 | 1.2810 | x0.394 |

evals/rep=8000000 changed/rep=8000000 fingerprint-check=identical

#### topology=mixchain gates=1018 inputs=18 window=64 placement=shuffled frag=192 activity=0.10 iters=8000 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 13.17 | 13.17 | 13.21 | 0.3% | 53.08 | 1.38 | 0.8653 | 2.4241 | x1.000 |
| b arena+virtual | 40 | 12.68 | 12.68 | 12.72 | 0.3% | 51.12 | 1.43 | 0.8649 | 1.8597 | x0.963 |
| c flat24+switch | 24 | 9.91 | 9.91 | 9.94 | 0.3% | 39.93 | 1.91 | 0.6646 | 1.4127 | x0.752 |
| d flat24+SIMA | 24 | 4.91 | 4.90 | 4.92 | 0.4% | 19.78 | 3.54 | 0.0010 | 1.4025 | x0.373 |
| g flat40+SIMA | 40 | 5.53 | 5.52 | 5.59 | 1.2% | 22.32 | 3.23 | 0.0010 | 1.7088 | x0.420 |
| e flat32+SIMA | 32 | 5.45 | 5.44 | 5.47 | 0.4% | 22.00 | 3.28 | 0.0010 | 1.4764 | x0.414 |

evals/rep=8000000 changed/rep=8000000 fingerprint-check=identical

#### topology=mixchain gates=10159 inputs=159 window=64 placement=topological frag=0 activity=0.10 iters=800 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 12.10 | 12.09 | 12.12 | 0.3% | 48.67 | 1.50 | 0.8752 | 1.5308 | x1.000 |
| b arena+virtual | 40 | 11.95 | 11.94 | 11.99 | 0.4% | 48.09 | 1.52 | 0.8757 | 1.4044 | x0.988 |
| c flat24+switch | 24 | 10.10 | 10.03 | 10.18 | 1.5% | 40.64 | 1.87 | 0.6919 | 1.1529 | x0.835 |
| d flat24+SIMA | 24 | 5.22 | 5.21 | 5.22 | 0.3% | 21.00 | 3.33 | 0.0001 | 1.1529 | x0.431 |
| g flat40+SIMA | 40 | 4.86 | 4.85 | 4.87 | 0.4% | 19.53 | 3.69 | 0.0001 | 1.4024 | x0.401 |
| e flat32+SIMA | 32 | 4.84 | 4.83 | 4.87 | 0.7% | 19.47 | 3.70 | 0.0001 | 1.2772 | x0.400 |

evals/rep=8000000 changed/rep=8000000 fingerprint-check=identical

#### topology=mixchain gates=10159 inputs=159 window=64 placement=shuffled frag=192 activity=0.10 iters=800 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 21.26 | 21.21 | 21.45 | 1.1% | 85.73 | 0.85 | 0.8757 | 2.4492 | x1.000 |
| b arena+virtual | 40 | 16.94 | 16.91 | 17.03 | 0.7% | 68.21 | 1.07 | 0.8752 | 2.3666 | x0.796 |
| c flat24+switch | 24 | 12.15 | 12.14 | 12.19 | 0.4% | 48.94 | 1.56 | 0.6932 | 1.9647 | x0.571 |
| d flat24+SIMA | 24 | 7.41 | 7.40 | 7.45 | 0.7% | 29.87 | 2.34 | 0.0001 | 1.9669 | x0.349 |
| g flat40+SIMA | 40 | 10.96 | 10.94 | 10.97 | 0.3% | 44.27 | 1.63 | 0.0001 | 2.0066 | x0.515 |
| e flat32+SIMA | 32 | 10.16 | 10.15 | 10.20 | 0.4% | 41.11 | 1.75 | 0.0001 | 1.7540 | x0.478 |

evals/rep=8000000 changed/rep=8000000 fingerprint-check=identical

#### topology=mixchain gates=101565 inputs=1565 window=64 placement=topological frag=0 activity=0.10 iters=80 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 12.07 | 12.04 | 12.11 | 0.6% | 48.52 | 1.51 | 0.8725 | 1.5210 | x1.000 |
| b arena+virtual | 40 | 12.03 | 12.01 | 12.11 | 0.9% | 48.32 | 1.51 | 0.8727 | 1.3955 | x0.996 |
| c flat24+switch | 24 | 10.02 | 9.97 | 10.14 | 1.7% | 40.30 | 1.89 | 0.6942 | 1.1446 | x0.829 |
| d flat24+SIMA | 24 | 5.23 | 5.18 | 5.25 | 1.2% | 21.04 | 3.33 | 0.0000 | 1.1440 | x0.433 |
| g flat40+SIMA | 40 | 4.97 | 4.91 | 4.99 | 1.8% | 19.95 | 3.61 | 0.0000 | 1.3978 | x0.412 |
| e flat32+SIMA | 32 | 4.77 | 4.76 | 4.84 | 1.6% | 19.17 | 3.76 | 0.0000 | 1.2685 | x0.396 |

evals/rep=8000000 changed/rep=8000000 fingerprint-check=identical

#### topology=mixchain gates=101565 inputs=1565 window=64 placement=shuffled frag=192 activity=0.10 iters=80 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 42.77 | 40.78 | 48.16 | 17.3% | 172.96 | 0.42 | 0.8706 | 2.4490 | x1.000 |
| b arena+virtual | 40 | 21.57 | 20.41 | 21.71 | 6.0% | 87.01 | 0.84 | 0.8728 | 2.4093 | x0.505 |
| c flat24+switch | 24 | 19.16 | 18.76 | 19.28 | 2.8% | 77.54 | 0.98 | 0.6963 | 2.0144 | x0.447 |
| d flat24+SIMA | 24 | 14.75 | 14.55 | 15.19 | 4.3% | 59.63 | 1.17 | 0.0000 | 2.0146 | x0.345 |
| g flat40+SIMA | 40 | 15.15 | 14.80 | 15.77 | 6.4% | 61.34 | 1.17 | 0.0000 | 2.0190 | x0.355 |
| e flat32+SIMA | 32 | 14.14 | 13.99 | 15.07 | 7.6% | 57.26 | 1.26 | 0.0000 | 1.7668 | x0.332 |

evals/rep=8000000 changed/rep=8000000 fingerprint-check=identical

#### topology=mixchain gates=1015628 inputs=15628 window=64 placement=topological frag=0 activity=0.10 iters=8 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 17.85 | 17.81 | 18.11 | 1.6% | 71.81 | 1.02 | 0.8744 | 3.9138 | x1.000 |
| b arena+virtual | 40 | 12.19 | 12.17 | 12.27 | 0.8% | 48.96 | 1.49 | 0.8731 | 1.3961 | x0.683 |
| c flat24+switch | 24 | 10.14 | 10.11 | 10.41 | 3.0% | 40.75 | 1.87 | 0.6931 | 1.1444 | x0.567 |
| d flat24+SIMA | 24 | 11.84 | 11.80 | 11.84 | 0.3% | 47.86 | 1.46 | 0.0000 | 2.1511 | x0.663 |
| g flat40+SIMA | 40 | 7.52 | 7.51 | 7.59 | 1.1% | 30.34 | 2.37 | 0.0000 | 1.3928 | x0.421 |
| e flat32+SIMA | 32 | 7.13 | 7.06 | 7.14 | 1.1% | 28.77 | 2.50 | 0.0000 | 1.2668 | x0.399 |

evals/rep=8000000 changed/rep=8000000 fingerprint-check=identical

#### topology=mixchain gates=1015628 inputs=15628 window=64 placement=shuffled frag=192 activity=0.10 iters=8 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 126.43 | 124.33 | 127.48 | 2.5% | 514.94 | 0.14 | 0.8725 | 5.0426 | x1.000 |
| b arena+virtual | 40 | 88.38 | 87.33 | 90.07 | 3.1% | 359.47 | 0.20 | 0.8730 | 2.4446 | x0.702 |
| c flat24+switch | 24 | 63.88 | 63.12 | 66.32 | 5.0% | 259.67 | 0.29 | 0.6937 | 2.0187 | x0.508 |
| d flat24+SIMA | 24 | 71.68 | 70.35 | 74.10 | 5.2% | 292.20 | 0.24 | 0.0001 | 3.0340 | x0.564 |
| g flat40+SIMA | 40 | 84.51 | 83.02 | 85.16 | 2.5% | 345.02 | 0.21 | 0.0001 | 2.0194 | x0.670 |
| e flat32+SIMA | 32 | 82.14 | 79.11 | 85.00 | 7.2% | 335.41 | 0.21 | 0.0001 | 2.7782 | x0.649 |

evals/rep=8000000 changed/rep=8000000 fingerprint-check=identical

#### topology=mixchain gates=1018 inputs=18 window=64 placement=topological frag=0 activity=0.10 iters=9503 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 12.78 | 12.76 | 12.80 | 0.3% | 51.52 | 1.36 | 0.8710 | 1.2453 | x1.000 |
| b arena+virtual | 40 | 12.77 | 12.76 | 12.79 | 0.3% | 51.50 | 1.36 | 0.8706 | 1.0811 | x1.000 |
| c flat24+switch | 24 | 10.81 | 10.80 | 10.83 | 0.2% | 43.78 | 1.65 | 0.6843 | 0.7747 | x0.846 |
| d flat24+SIMA | 24 | 5.67 | 5.66 | 5.70 | 0.7% | 22.93 | 2.90 | 0.0031 | 0.7742 | x0.444 |

evals/rep=7943962 changed/rep=7943962 fingerprint-check=identical
