# Ablation harness reruns on the laptop: struct size, L3 cliff, predictor

## Rerun: struct size on the mixed-gate chain, 100k to 2M gates, 3 separate processes

Source: raw log `item1_struct_size.log` (not kept) (converted from the raw harness output; columns as printed by `tests/ablation_layout.cpp`).

### Call 1

#### topology=mixchain gates=101565 inputs=1565 window=64 placement=topological frag=0 activity=0.10 iters=80 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 11.89 | 11.88 | 11.93 | 0.4% | 48.48 | 1.51 | 0.8725 | 1.5225 | x1.000 |
| d flat24+SIMA | 24 | 5.10 | 5.09 | 5.11 | 0.3% | 20.82 | 3.36 | 0.0000 | 1.1433 | x0.428 |
| e flat32+SIMA | 32 | 4.76 | 4.70 | 4.82 | 2.5% | 19.42 | 3.71 | 0.0000 | 1.2685 | x0.400 |
| g flat40+SIMA | 40 | 4.86 | 4.79 | 4.87 | 1.7% | 19.79 | 3.64 | 0.0000 | 1.3930 | x0.408 |

evals/rep=8000000 changed/rep=8000000 fingerprint-check=identical

### Call 1

#### topology=mixchain gates=304690 inputs=4690 window=64 placement=topological frag=0 activity=0.10 iters=26 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 11.99 | 11.96 | 12.00 | 0.3% | 48.80 | 1.50 | 0.8730 | 1.5225 | x1.000 |
| d flat24+SIMA | 24 | 5.69 | 5.68 | 5.80 | 2.0% | 23.21 | 3.02 | 0.0000 | 1.1429 | x0.475 |
| e flat32+SIMA | 32 | 5.74 | 5.71 | 5.80 | 1.6% | 23.42 | 3.07 | 0.0000 | 1.2678 | x0.479 |
| g flat40+SIMA | 40 | 6.11 | 6.09 | 6.27 | 2.9% | 24.95 | 2.89 | 0.0000 | 1.3937 | x0.510 |

evals/rep=7800000 changed/rep=7800000 fingerprint-check=identical

### Call 1

#### topology=mixchain gates=507815 inputs=7815 window=64 placement=topological frag=0 activity=0.10 iters=16 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 12.07 | 12.05 | 12.14 | 0.7% | 49.16 | 1.49 | 0.8725 | 1.5225 | x1.000 |
| d flat24+SIMA | 24 | 6.00 | 5.99 | 6.01 | 0.4% | 24.43 | 2.87 | 0.0000 | 1.1426 | x0.497 |
| e flat32+SIMA | 32 | 6.29 | 6.25 | 6.55 | 4.8% | 25.69 | 2.80 | 0.0000 | 1.2674 | x0.520 |
| g flat40+SIMA | 40 | 11.62 | 11.60 | 11.64 | 0.3% | 47.61 | 1.51 | 0.0000 | 2.4042 | x0.962 |

evals/rep=8000000 changed/rep=8000000 fingerprint-check=identical

### Call 1

#### topology=mixchain gates=710940 inputs=10940 window=64 placement=topological frag=0 activity=0.10 iters=11 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 12.02 | 12.00 | 12.03 | 0.2% | 48.92 | 1.49 | 0.8727 | 1.5200 | x1.000 |
| d flat24+SIMA | 24 | 6.15 | 6.13 | 6.25 | 2.0% | 25.04 | 2.80 | 0.0000 | 1.1424 | x0.512 |
| e flat32+SIMA | 32 | 6.83 | 6.76 | 7.04 | 4.0% | 27.84 | 2.59 | 0.0000 | 1.2677 | x0.567 |
| g flat40+SIMA | 40 | 7.33 | 7.32 | 7.38 | 0.8% | 29.95 | 2.40 | 0.0000 | 1.3928 | x0.610 |

evals/rep=7700000 changed/rep=7700000 fingerprint-check=identical

### Call 1

#### topology=mixchain gates=1015628 inputs=15628 window=64 placement=topological frag=0 activity=0.10 iters=8 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 17.65 | 17.64 | 17.71 | 0.4% | 71.91 | 1.02 | 0.8743 | 3.9211 | x1.000 |
| d flat24+SIMA | 24 | 6.43 | 6.40 | 6.47 | 1.2% | 26.20 | 2.67 | 0.0000 | 1.1418 | x0.364 |
| e flat32+SIMA | 32 | 7.13 | 7.07 | 7.14 | 1.1% | 29.10 | 2.47 | 0.0000 | 1.2670 | x0.404 |
| g flat40+SIMA | 40 | 11.67 | 11.65 | 11.74 | 0.8% | 47.73 | 1.51 | 0.0000 | 2.4022 | x0.661 |

evals/rep=8000000 changed/rep=8000000 fingerprint-check=identical

### Call 1

#### topology=mixchain gates=2031253 inputs=31253 window=64 placement=topological frag=0 activity=0.10 iters=4 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 12.10 | 12.08 | 12.18 | 0.8% | 49.07 | 1.49 | 0.8731 | 1.5243 | x1.000 |
| d flat24+SIMA | 24 | 6.90 | 6.88 | 6.95 | 0.9% | 28.10 | 2.49 | 0.0000 | 1.1417 | x0.570 |
| e flat32+SIMA | 32 | 11.39 | 11.37 | 11.47 | 0.8% | 46.49 | 1.55 | 0.0000 | 2.2804 | x0.941 |
| g flat40+SIMA | 40 | 7.55 | 7.54 | 7.64 | 1.4% | 30.76 | 2.34 | 0.0000 | 1.3926 | x0.624 |

evals/rep=8000000 changed/rep=8000000 fingerprint-check=identical

### Call 2

#### topology=mixchain gates=101565 inputs=1565 window=64 placement=topological frag=0 activity=0.10 iters=80 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 12.03 | 12.01 | 12.21 | 1.6% | 48.71 | 1.50 | 0.8724 | 1.5388 | x1.000 |
| d flat24+SIMA | 24 | 5.13 | 5.12 | 5.17 | 0.9% | 20.77 | 3.37 | 0.0000 | 1.1448 | x0.427 |
| e flat32+SIMA | 32 | 4.76 | 4.75 | 4.81 | 1.4% | 19.28 | 3.74 | 0.0000 | 1.2696 | x0.395 |
| g flat40+SIMA | 40 | 4.81 | 4.80 | 4.89 | 1.9% | 19.47 | 3.70 | 0.0000 | 1.3930 | x0.399 |

evals/rep=8000000 changed/rep=8000000 fingerprint-check=identical

### Call 2

#### topology=mixchain gates=304690 inputs=4690 window=64 placement=topological frag=0 activity=0.10 iters=26 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 12.07 | 12.06 | 12.09 | 0.2% | 48.83 | 1.50 | 0.8729 | 1.5209 | x1.000 |
| d flat24+SIMA | 24 | 5.71 | 5.70 | 5.75 | 0.8% | 23.14 | 3.03 | 0.0000 | 1.1422 | x0.473 |
| e flat32+SIMA | 32 | 5.75 | 5.74 | 5.88 | 2.5% | 23.32 | 3.09 | 0.0000 | 1.2672 | x0.476 |
| g flat40+SIMA | 40 | 6.11 | 6.10 | 6.28 | 2.9% | 24.76 | 2.91 | 0.0000 | 1.3950 | x0.506 |

evals/rep=7800000 changed/rep=7800000 fingerprint-check=identical

### Call 2

#### topology=mixchain gates=507815 inputs=7815 window=64 placement=topological frag=0 activity=0.10 iters=16 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 17.72 | 17.68 | 17.76 | 0.5% | 71.88 | 1.02 | 0.8739 | 3.9099 | x1.000 |
| d flat24+SIMA | 24 | 6.00 | 6.00 | 6.05 | 0.9% | 24.35 | 2.87 | 0.0000 | 1.1420 | x0.339 |
| e flat32+SIMA | 32 | 6.32 | 6.28 | 6.40 | 1.8% | 25.64 | 2.81 | 0.0000 | 1.2674 | x0.357 |
| g flat40+SIMA | 40 | 11.69 | 11.68 | 11.76 | 0.7% | 47.60 | 1.51 | 0.0000 | 2.4041 | x0.660 |

evals/rep=8000000 changed/rep=8000000 fingerprint-check=identical

### Call 2

#### topology=mixchain gates=710940 inputs=10940 window=64 placement=topological frag=0 activity=0.10 iters=11 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 12.12 | 12.11 | 12.15 | 0.4% | 49.06 | 1.49 | 0.8727 | 1.5209 | x1.000 |
| d flat24+SIMA | 24 | 6.16 | 6.14 | 6.25 | 1.8% | 24.97 | 2.80 | 0.0000 | 1.1422 | x0.508 |
| e flat32+SIMA | 32 | 6.84 | 6.76 | 7.02 | 3.8% | 27.76 | 2.59 | 0.0000 | 1.2679 | x0.565 |
| g flat40+SIMA | 40 | 7.36 | 7.34 | 7.52 | 2.5% | 29.87 | 2.41 | 0.0000 | 1.3929 | x0.607 |

evals/rep=7700000 changed/rep=7700000 fingerprint-check=identical

### Call 2

#### topology=mixchain gates=1015628 inputs=15628 window=64 placement=topological frag=0 activity=0.10 iters=8 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 17.77 | 17.76 | 17.81 | 0.3% | 72.00 | 1.02 | 0.8743 | 3.9273 | x1.000 |
| d flat24+SIMA | 24 | 11.74 | 11.72 | 11.79 | 0.6% | 47.83 | 1.46 | 0.0000 | 2.1508 | x0.661 |
| e flat32+SIMA | 32 | 7.09 | 7.08 | 7.10 | 0.4% | 28.79 | 2.50 | 0.0000 | 1.2675 | x0.399 |
| g flat40+SIMA | 40 | 7.58 | 7.54 | 7.65 | 1.5% | 30.75 | 2.34 | 0.0000 | 1.3936 | x0.426 |

evals/rep=8000000 changed/rep=8000000 fingerprint-check=identical

### Call 2

#### topology=mixchain gates=2031253 inputs=31253 window=64 placement=topological frag=0 activity=0.10 iters=4 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 12.12 | 12.10 | 12.19 | 0.8% | 49.02 | 1.49 | 0.8732 | 1.5240 | x1.000 |
| d flat24+SIMA | 24 | 6.90 | 6.81 | 6.95 | 2.0% | 27.94 | 2.51 | 0.0000 | 1.1417 | x0.569 |
| e flat32+SIMA | 32 | 11.41 | 11.40 | 11.49 | 0.8% | 46.46 | 1.55 | 0.0000 | 2.2803 | x0.942 |
| g flat40+SIMA | 40 | 7.56 | 7.42 | 7.65 | 3.0% | 30.68 | 2.35 | 0.0000 | 1.3922 | x0.623 |

evals/rep=8000000 changed/rep=8000000 fingerprint-check=identical

### Call 3

#### topology=mixchain gates=101565 inputs=1565 window=64 placement=topological frag=0 activity=0.10 iters=80 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 11.94 | 11.92 | 11.98 | 0.5% | 48.14 | 1.52 | 0.8727 | 1.5229 | x1.000 |
| d flat24+SIMA | 24 | 5.17 | 5.12 | 5.20 | 1.5% | 20.93 | 3.34 | 0.0000 | 1.1434 | x0.433 |
| e flat32+SIMA | 32 | 4.84 | 4.77 | 4.88 | 2.2% | 19.53 | 3.69 | 0.0000 | 1.2677 | x0.405 |
| g flat40+SIMA | 40 | 4.84 | 4.83 | 4.92 | 1.9% | 19.49 | 3.69 | 0.0000 | 1.3931 | x0.405 |

evals/rep=8000000 changed/rep=8000000 fingerprint-check=identical

### Call 3

#### topology=mixchain gates=304690 inputs=4690 window=64 placement=topological frag=0 activity=0.10 iters=26 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 12.10 | 12.07 | 12.13 | 0.4% | 48.78 | 1.50 | 0.8730 | 1.5224 | x1.000 |
| d flat24+SIMA | 24 | 5.72 | 5.71 | 5.86 | 2.7% | 23.13 | 3.03 | 0.0000 | 1.1427 | x0.473 |
| e flat32+SIMA | 32 | 5.77 | 5.73 | 5.91 | 3.0% | 23.30 | 3.09 | 0.0000 | 1.2682 | x0.476 |
| g flat40+SIMA | 40 | 6.10 | 6.08 | 6.11 | 0.4% | 24.63 | 2.92 | 0.0000 | 1.3928 | x0.504 |

evals/rep=7800000 changed/rep=7800000 fingerprint-check=identical

### Call 3

#### topology=mixchain gates=507815 inputs=7815 window=64 placement=topological frag=0 activity=0.10 iters=16 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 12.10 | 12.09 | 12.11 | 0.1% | 48.88 | 1.50 | 0.8726 | 1.5235 | x1.000 |
| d flat24+SIMA | 24 | 11.77 | 11.76 | 11.83 | 0.6% | 47.86 | 1.46 | 0.0000 | 2.1525 | x0.973 |
| e flat32+SIMA | 32 | 11.42 | 11.41 | 11.49 | 0.6% | 46.43 | 1.55 | 0.0000 | 2.2805 | x0.944 |
| g flat40+SIMA | 40 | 6.89 | 6.88 | 7.13 | 3.7% | 27.90 | 2.58 | 0.0000 | 1.3929 | x0.570 |

evals/rep=8000000 changed/rep=8000000 fingerprint-check=identical

### Call 3

#### topology=mixchain gates=710940 inputs=10940 window=64 placement=topological frag=0 activity=0.10 iters=11 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 12.09 | 12.09 | 12.12 | 0.2% | 48.88 | 1.50 | 0.8727 | 1.5206 | x1.000 |
| d flat24+SIMA | 24 | 11.78 | 11.76 | 11.90 | 1.2% | 47.85 | 1.46 | 0.0000 | 2.1518 | x0.974 |
| e flat32+SIMA | 32 | 6.76 | 6.75 | 6.81 | 0.9% | 27.37 | 2.63 | 0.0000 | 1.2666 | x0.559 |
| g flat40+SIMA | 40 | 7.30 | 7.23 | 7.43 | 2.8% | 29.55 | 2.44 | 0.0000 | 1.3924 | x0.603 |

evals/rep=7700000 changed/rep=7700000 fingerprint-check=identical

### Call 3

#### topology=mixchain gates=1015628 inputs=15628 window=64 placement=topological frag=0 activity=0.10 iters=8 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 12.13 | 12.11 | 12.37 | 2.2% | 48.97 | 1.49 | 0.8730 | 1.5226 | x1.000 |
| d flat24+SIMA | 24 | 11.77 | 11.76 | 11.83 | 0.6% | 47.85 | 1.46 | 0.0000 | 2.1511 | x0.971 |
| e flat32+SIMA | 32 | 7.10 | 7.08 | 7.12 | 0.6% | 28.75 | 2.50 | 0.0000 | 1.2670 | x0.586 |
| g flat40+SIMA | 40 | 11.74 | 11.73 | 11.74 | 0.1% | 47.65 | 1.51 | 0.0000 | 2.4013 | x0.968 |

evals/rep=8000000 changed/rep=8000000 fingerprint-check=identical

### Call 3

#### topology=mixchain gates=2031253 inputs=31253 window=64 placement=topological frag=0 activity=0.10 iters=4 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 17.78 | 17.77 | 17.84 | 0.4% | 71.92 | 1.02 | 0.8745 | 3.9181 | x1.000 |
| d flat24+SIMA | 24 | 6.87 | 6.83 | 6.96 | 1.9% | 27.82 | 2.52 | 0.0000 | 1.1418 | x0.387 |
| e flat32+SIMA | 32 | 7.34 | 7.31 | 7.42 | 1.5% | 29.70 | 2.42 | 0.0000 | 1.2669 | x0.413 |
| g flat40+SIMA | 40 | 7.60 | 7.58 | 7.63 | 0.6% | 30.78 | 2.34 | 0.0000 | 1.3927 | x0.427 |

evals/rep=8000000 changed/rep=8000000 fingerprint-check=identical

## Rerun: 1M-gate shuffled chain across 7 separate processes (IDE open)

Source: raw log `item2_l3_repeat.log` (not kept) (converted from the raw harness output; columns as printed by `tests/ablation_layout.cpp`).

### Call 1

#### topology=chain gates=1000000 inputs=1 window=64 placement=shuffled frag=192 activity=0.10 iters=8 reps=5 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 120.64 | 120.58 | 120.89 | 0.3% | 490.99 | 0.15 | 0.0002 | 2.4401 | x1.000 |
| d flat24+SIMA | 24 | 78.00 | 77.62 | 84.10 | 8.3% | 317.95 | 0.22 | 0.0001 | 2.0065 | x0.647 |
| e flat32+SIMA | 32 | 86.31 | 85.43 | 91.14 | 6.6% | 351.40 | 0.20 | 0.0001 | 1.7571 | x0.716 |
| g flat40+SIMA | 40 | 92.48 | 91.65 | 93.98 | 2.5% | 374.89 | 0.19 | 0.0001 | 2.0081 | x0.767 |

evals/rep=7999992 changed/rep=7999992 fingerprint-check=identical

### Call 2

#### topology=chain gates=1000000 inputs=1 window=64 placement=shuffled frag=192 activity=0.10 iters=8 reps=5 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 120.94 | 120.79 | 121.06 | 0.2% | 489.24 | 0.15 | 0.0001 | 2.4373 | x1.000 |
| d flat24+SIMA | 24 | 78.52 | 77.71 | 82.98 | 6.7% | 317.57 | 0.22 | 0.0001 | 2.0068 | x0.649 |
| e flat32+SIMA | 32 | 86.63 | 86.07 | 91.07 | 5.8% | 350.56 | 0.21 | 0.0001 | 1.7576 | x0.717 |
| g flat40+SIMA | 40 | 95.89 | 93.77 | 97.43 | 3.8% | 385.41 | 0.19 | 0.0001 | 2.0080 | x0.794 |

evals/rep=7999992 changed/rep=7999992 fingerprint-check=identical

### Call 3

#### topology=chain gates=1000000 inputs=1 window=64 placement=shuffled frag=192 activity=0.10 iters=8 reps=5 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 121.38 | 121.01 | 121.78 | 0.6% | 488.28 | 0.15 | 0.0002 | 2.4409 | x1.000 |
| d flat24+SIMA | 24 | 77.05 | 76.92 | 79.06 | 2.8% | 311.53 | 0.22 | 0.0001 | 2.0063 | x0.636 |
| e flat32+SIMA | 32 | 86.41 | 85.92 | 86.57 | 0.8% | 348.19 | 0.21 | 0.0001 | 1.7569 | x0.713 |
| g flat40+SIMA | 40 | 96.49 | 94.69 | 97.77 | 3.2% | 386.81 | 0.19 | 0.0001 | 2.0082 | x0.795 |

evals/rep=7999992 changed/rep=7999992 fingerprint-check=identical

### Call 4

#### topology=chain gates=1000000 inputs=1 window=64 placement=shuffled frag=192 activity=0.10 iters=8 reps=5 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 121.71 | 120.79 | 122.44 | 1.4% | 488.69 | 0.15 | 0.0001 | 2.4374 | x1.000 |
| d flat24+SIMA | 24 | 78.12 | 76.98 | 78.91 | 2.5% | 315.16 | 0.22 | 0.0001 | 2.0057 | x0.644 |
| e flat32+SIMA | 32 | 85.87 | 85.59 | 86.82 | 1.4% | 346.72 | 0.21 | 0.0001 | 1.7563 | x0.707 |
| g flat40+SIMA | 40 | 94.04 | 93.82 | 96.64 | 3.0% | 380.20 | 0.19 | 0.0001 | 2.0073 | x0.771 |

evals/rep=7999992 changed/rep=7999992 fingerprint-check=identical

### Call 5

#### topology=chain gates=1000000 inputs=1 window=64 placement=shuffled frag=192 activity=0.10 iters=8 reps=5 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 123.26 | 123.12 | 124.33 | 1.0% | 496.19 | 0.15 | 0.0001 | 2.4398 | x1.000 |
| d flat24+SIMA | 24 | 87.23 | 80.18 | 90.62 | 12.0% | 351.08 | 0.20 | 0.0001 | 2.0059 | x0.707 |
| e flat32+SIMA | 32 | 97.81 | 89.73 | 97.97 | 8.4% | 394.72 | 0.18 | 0.0001 | 1.7566 | x0.794 |
| g flat40+SIMA | 40 | 100.71 | 95.88 | 102.87 | 6.9% | 405.84 | 0.18 | 0.0001 | 2.0076 | x0.810 |

evals/rep=7999992 changed/rep=7999992 fingerprint-check=identical

### Call 6

#### topology=chain gates=1000000 inputs=1 window=64 placement=shuffled frag=192 activity=0.10 iters=8 reps=5 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 121.99 | 121.18 | 122.25 | 0.9% | 488.36 | 0.15 | 0.0001 | 2.4394 | x1.000 |
| d flat24+SIMA | 24 | 78.36 | 77.28 | 78.98 | 2.2% | 315.82 | 0.22 | 0.0001 | 2.0055 | x0.645 |
| e flat32+SIMA | 32 | 85.73 | 85.45 | 88.16 | 3.2% | 346.42 | 0.21 | 0.0001 | 1.7564 | x0.705 |
| g flat40+SIMA | 40 | 93.58 | 92.96 | 94.12 | 1.2% | 377.11 | 0.19 | 0.0001 | 2.0074 | x0.766 |

evals/rep=7999992 changed/rep=7999992 fingerprint-check=identical

### Call 7

#### topology=chain gates=1000000 inputs=1 window=64 placement=shuffled frag=192 activity=0.10 iters=8 reps=5 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 121.12 | 120.93 | 121.47 | 0.4% | 488.56 | 0.15 | 0.0001 | 2.4367 | x1.000 |
| d flat24+SIMA | 24 | 77.65 | 77.40 | 86.58 | 11.8% | 314.12 | 0.22 | 0.0001 | 2.0057 | x0.642 |
| e flat32+SIMA | 32 | 86.28 | 85.72 | 89.03 | 3.8% | 348.64 | 0.21 | 0.0001 | 1.7563 | x0.712 |
| g flat40+SIMA | 40 | 92.86 | 92.67 | 93.26 | 0.6% | 375.80 | 0.19 | 0.0001 | 2.0074 | x0.766 |

evals/rep=7999992 changed/rep=7999992 fingerprint-check=identical

## Rerun: predictor memorization onset, mixed-gate chain, 54 to 10k gates, static then `--vary` per size (the 54-gate `--vary` row ran with one iteration and is invalid)

Source: raw log `item3_predictor.log` (not kept) (converted from the raw harness output; columns as printed by `tests/ablation_layout.cpp`).

#### topology=mixchain gates=54 inputs=4 window=64 placement=topological frag=0 activity=0.10 iters=160000 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 9.94 | 9.67 | 9.99 | 3.2% | 40.16 | 1.86 | 0.5980 | 0.0197 | x1.000 |
| d flat24+SIMA | 24 | 4.73 | 4.72 | 4.82 | 2.1% | 19.12 | 3.74 | 0.0000 | 0.0185 | x0.475 |

evals/rep=8000000 changed/rep=8000000 fingerprint-check=identical

#### topology=mixchain gates=54 inputs=4 window=64 placement=topological frag=0 activity=0.10 iters=1 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | inf | inf | inf | -nan% | inf | 0.49 | inf | inf | x-nan |
| d flat24+SIMA | 24 | inf | inf | inf | -nan% | inf | 0.52 | inf | inf | x-nan |

evals/rep=0 changed/rep=0 fingerprint-check=identical

#### topology=mixchain gates=104 inputs=4 window=64 placement=topological frag=0 activity=0.10 iters=80000 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 11.21 | 11.07 | 11.30 | 2.0% | 45.24 | 1.63 | 0.7608 | 0.0126 | x1.000 |
| d flat24+SIMA | 24 | 4.78 | 4.74 | 4.80 | 1.2% | 19.34 | 3.66 | 0.0100 | 0.0102 | x0.427 |

evals/rep=8000000 changed/rep=8000000 fingerprint-check=identical

#### topology=mixchain gates=104 inputs=4 window=64 placement=topological frag=0 activity=0.10 iters=216216 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 10.00 | 9.99 | 10.05 | 0.6% | 40.41 | 1.86 | 0.5759 | 0.0257 | x1.000 |
| d flat24+SIMA | 24 | 4.84 | 4.82 | 4.85 | 0.5% | 19.55 | 3.69 | 0.0000 | 0.0247 | x0.483 |

evals/rep=7999992 changed/rep=7999992 fingerprint-check=identical

#### topology=mixchain gates=206 inputs=6 window=64 placement=topological frag=0 activity=0.10 iters=40000 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 11.08 | 11.05 | 11.17 | 1.1% | 44.73 | 1.64 | 0.8013 | 0.0238 | x1.000 |
| d flat24+SIMA | 24 | 4.70 | 4.66 | 4.70 | 0.9% | 18.99 | 3.71 | 0.0050 | 0.0079 | x0.422 |

evals/rep=8000000 changed/rep=8000000 fingerprint-check=identical

#### topology=mixchain gates=206 inputs=6 window=64 placement=topological frag=0 activity=0.10 iters=105461 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 11.24 | 11.22 | 11.26 | 0.3% | 45.37 | 1.63 | 0.8060 | 0.0186 | x1.000 |
| d flat24+SIMA | 24 | 4.78 | 4.76 | 4.81 | 1.2% | 19.32 | 3.67 | 0.0144 | 0.0138 | x0.425 |

evals/rep=7894489 changed/rep=7894489 fingerprint-check=identical

#### topology=mixchain gates=409 inputs=9 window=64 placement=topological frag=0 activity=0.10 iters=20000 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 11.48 | 11.47 | 11.51 | 0.3% | 46.34 | 1.58 | 0.8297 | 1.2279 | x1.000 |
| d flat24+SIMA | 24 | 4.68 | 4.66 | 4.71 | 1.1% | 18.93 | 3.71 | 0.0025 | 0.0731 | x0.408 |

evals/rep=8000000 changed/rep=8000000 fingerprint-check=identical

#### topology=mixchain gates=409 inputs=9 window=64 placement=topological frag=0 activity=0.10 iters=39027 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 11.74 | 11.74 | 11.81 | 0.6% | 47.46 | 1.53 | 0.8456 | 0.2682 | x1.000 |
| d flat24+SIMA | 24 | 4.88 | 4.87 | 4.91 | 0.9% | 19.77 | 3.52 | 0.0064 | 0.0177 | x0.415 |

evals/rep=7870207 changed/rep=7870207 fingerprint-check=identical

#### topology=mixchain gates=713 inputs=13 window=64 placement=topological frag=0 activity=0.10 iters=11428 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 11.94 | 11.93 | 11.97 | 0.4% | 48.19 | 1.52 | 0.8596 | 1.5280 | x1.000 |
| d flat24+SIMA | 24 | 4.85 | 4.83 | 4.86 | 0.7% | 19.59 | 3.58 | 0.0014 | 1.1328 | x0.406 |

evals/rep=7999600 changed/rep=7999600 fingerprint-check=identical

#### topology=mixchain gates=713 inputs=13 window=64 placement=topological frag=0 activity=0.10 iters=16466 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 12.45 | 12.44 | 12.48 | 0.3% | 50.29 | 1.42 | 0.8832 | 1.0405 | x1.000 |
| d flat24+SIMA | 24 | 5.30 | 5.29 | 5.32 | 0.5% | 21.47 | 3.17 | 0.0037 | 0.5225 | x0.426 |

evals/rep=7750554 changed/rep=7750554 fingerprint-check=identical

#### topology=mixchain gates=1018 inputs=18 window=64 placement=topological frag=0 activity=0.10 iters=8000 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 11.76 | 11.75 | 11.77 | 0.2% | 47.43 | 1.54 | 0.8602 | 1.5456 | x1.000 |
| d flat24+SIMA | 24 | 5.03 | 5.02 | 5.06 | 0.8% | 20.33 | 3.45 | 0.0010 | 1.1577 | x0.427 |

evals/rep=8000000 changed/rep=8000000 fingerprint-check=identical

#### topology=mixchain gates=1018 inputs=18 window=64 placement=topological frag=0 activity=0.10 iters=9503 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 12.89 | 12.88 | 12.93 | 0.5% | 52.09 | 1.34 | 0.8694 | 1.2438 | x1.000 |
| d flat24+SIMA | 24 | 5.65 | 5.63 | 5.66 | 0.5% | 22.90 | 2.91 | 0.0032 | 0.7790 | x0.438 |

evals/rep=7943962 changed/rep=7943962 fingerprint-check=identical

#### topology=mixchain gates=2034 inputs=34 window=64 placement=topological frag=0 activity=0.10 iters=4000 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 11.88 | 11.86 | 11.91 | 0.4% | 47.98 | 1.52 | 0.8664 | 1.5337 | x1.000 |
| d flat24+SIMA | 24 | 4.96 | 4.94 | 5.01 | 1.3% | 20.02 | 3.50 | 0.0005 | 1.1548 | x0.417 |

evals/rep=8000000 changed/rep=8000000 fingerprint-check=identical

#### topology=mixchain gates=2034 inputs=34 window=64 placement=topological frag=0 activity=0.10 iters=2504 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 13.30 | 13.28 | 13.35 | 0.5% | 53.75 | 1.25 | 0.8718 | 1.3598 | x1.000 |
| d flat24+SIMA | 24 | 5.82 | 5.82 | 5.86 | 0.8% | 23.59 | 2.70 | 0.0015 | 0.9612 | x0.438 |

evals/rep=7695975 changed/rep=7695975 fingerprint-check=identical

#### topology=mixchain gates=5081 inputs=81 window=64 placement=topological frag=0 activity=0.10 iters=1600 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 12.17 | 12.15 | 12.25 | 0.8% | 49.09 | 1.49 | 0.8704 | 1.5366 | x1.000 |
| d flat24+SIMA | 24 | 4.99 | 4.98 | 5.00 | 0.4% | 20.16 | 3.47 | 0.0002 | 1.1575 | x0.410 |

evals/rep=8000000 changed/rep=8000000 fingerprint-check=identical

#### topology=mixchain gates=5081 inputs=81 window=64 placement=topological frag=0 activity=0.10 iters=384 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 13.90 | 13.86 | 13.92 | 0.4% | 56.27 | 1.15 | 0.8726 | 1.5202 | x1.000 |
| d flat24+SIMA | 24 | 6.75 | 6.72 | 6.78 | 1.0% | 27.36 | 2.22 | 0.0006 | 1.0969 | x0.486 |

evals/rep=7425727 changed/rep=7425727 fingerprint-check=identical

#### topology=mixchain gates=10159 inputs=159 window=64 placement=topological frag=0 activity=0.10 iters=800 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 12.07 | 11.88 | 12.22 | 2.8% | 48.63 | 1.50 | 0.8748 | 1.5328 | x1.000 |
| d flat24+SIMA | 24 | 5.09 | 5.09 | 5.14 | 0.9% | 20.57 | 3.40 | 0.0001 | 1.1519 | x0.422 |

evals/rep=8000000 changed/rep=8000000 fingerprint-check=identical

#### topology=mixchain gates=10159 inputs=159 window=64 placement=topological frag=0 activity=0.10 iters=84 reps=9 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 14.62 | 14.55 | 14.74 | 1.3% | 59.08 | 1.07 | 0.8719 | 1.6469 | x1.000 |
| d flat24+SIMA | 24 | 7.09 | 6.99 | 7.18 | 2.6% | 28.64 | 2.08 | 0.0003 | 1.1714 | x0.485 |

evals/rep=6856591 changed/rep=6856591 fingerprint-check=identical

## Rerun: 1M-gate shuffled chain, 7 separate processes, quiet (SMT sibling offline, IDE closed)

Source: raw log `l3_quiet.log` (not kept).


### Call 1

#### topology=chain gates=1000000 inputs=1 window=64 placement=shuffled frag=192 activity=0.10 iters=8 reps=5 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 116.31 | 116.17 | 117.08 | 0.8% | 475.46 | 0.15 | 0.0001 | 2.4374 | x1.000 |
| d flat24+SIMA | 24 | 63.29 | 61.53 | 64.38 | 4.5% | 258.84 | 0.27 | 0.0001 | 2.0054 | x0.545 |
| e flat32+SIMA | 32 | 74.71 | 73.65 | 75.70 | 2.7% | 305.67 | 0.24 | 0.0001 | 1.7560 | x0.642 |
| g flat40+SIMA | 40 | 85.13 | 84.46 | 87.46 | 3.5% | 348.01 | 0.21 | 0.0001 | 2.0074 | x0.732 |

evals/rep=7999992 changed/rep=7999992 fingerprint-check=identical

### Call 2

#### topology=chain gates=1000000 inputs=1 window=64 placement=shuffled frag=192 activity=0.10 iters=8 reps=5 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 116.40 | 115.55 | 116.94 | 1.2% | 475.19 | 0.15 | 0.0001 | 2.4397 | x1.000 |
| d flat24+SIMA | 24 | 61.37 | 61.18 | 62.90 | 2.8% | 250.52 | 0.28 | 0.0001 | 2.0055 | x0.529 |
| e flat32+SIMA | 32 | 76.88 | 74.37 | 78.67 | 5.6% | 313.14 | 0.23 | 0.0001 | 1.7560 | x0.663 |
| g flat40+SIMA | 40 | 83.65 | 83.56 | 84.34 | 0.9% | 341.50 | 0.21 | 0.0001 | 2.0074 | x0.720 |

evals/rep=7999992 changed/rep=7999992 fingerprint-check=identical

### Call 3

#### topology=chain gates=1000000 inputs=1 window=64 placement=shuffled frag=192 activity=0.10 iters=8 reps=5 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 117.67 | 116.90 | 117.94 | 0.9% | 480.55 | 0.15 | 0.0001 | 2.4371 | x1.000 |
| d flat24+SIMA | 24 | 59.06 | 58.38 | 59.22 | 1.4% | 241.14 | 0.29 | 0.0001 | 2.0057 | x0.502 |
| e flat32+SIMA | 32 | 72.88 | 72.84 | 73.11 | 0.4% | 297.69 | 0.24 | 0.0001 | 1.7559 | x0.620 |
| g flat40+SIMA | 40 | 83.83 | 83.47 | 84.67 | 1.4% | 342.42 | 0.21 | 0.0001 | 2.0074 | x0.712 |

evals/rep=7999992 changed/rep=7999992 fingerprint-check=identical

### Call 4

#### topology=chain gates=1000000 inputs=1 window=64 placement=shuffled frag=192 activity=0.10 iters=8 reps=5 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 116.35 | 115.73 | 116.69 | 0.8% | 475.33 | 0.15 | 0.0001 | 2.4391 | x1.000 |
| d flat24+SIMA | 24 | 61.73 | 60.76 | 64.37 | 5.8% | 252.14 | 0.28 | 0.0001 | 2.0055 | x0.529 |
| e flat32+SIMA | 32 | 75.70 | 72.85 | 76.59 | 4.9% | 308.97 | 0.23 | 0.0001 | 1.7559 | x0.650 |
| g flat40+SIMA | 40 | 85.22 | 84.68 | 85.57 | 1.0% | 348.01 | 0.21 | 0.0001 | 2.0074 | x0.732 |

evals/rep=7999992 changed/rep=7999992 fingerprint-check=identical

### Call 5

#### topology=chain gates=1000000 inputs=1 window=64 placement=shuffled frag=192 activity=0.10 iters=8 reps=5 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 116.36 | 116.33 | 117.54 | 1.0% | 475.83 | 0.15 | 0.0001 | 2.4371 | x1.000 |
| d flat24+SIMA | 24 | 61.21 | 58.89 | 62.93 | 6.6% | 250.12 | 0.28 | 0.0001 | 2.0056 | x0.526 |
| e flat32+SIMA | 32 | 72.81 | 72.44 | 73.95 | 2.1% | 297.53 | 0.24 | 0.0001 | 1.7559 | x0.626 |
| g flat40+SIMA | 40 | 84.96 | 84.11 | 85.38 | 1.5% | 347.16 | 0.21 | 0.0001 | 2.0073 | x0.730 |

evals/rep=7999992 changed/rep=7999992 fingerprint-check=identical

### Call 6

#### topology=chain gates=1000000 inputs=1 window=64 placement=shuffled frag=192 activity=0.10 iters=8 reps=5 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 116.19 | 115.85 | 116.61 | 0.6% | 475.70 | 0.15 | 0.0001 | 2.4371 | x1.000 |
| d flat24+SIMA | 24 | 62.90 | 62.17 | 64.45 | 3.6% | 257.33 | 0.27 | 0.0001 | 2.0055 | x0.541 |
| e flat32+SIMA | 32 | 73.20 | 72.74 | 74.42 | 2.3% | 299.74 | 0.24 | 0.0001 | 1.7559 | x0.628 |
| g flat40+SIMA | 40 | 84.38 | 83.77 | 86.31 | 3.0% | 345.59 | 0.21 | 0.0001 | 2.0073 | x0.728 |

evals/rep=7999992 changed/rep=7999992 fingerprint-check=identical

### Call 7

#### topology=chain gates=1000000 inputs=1 window=64 placement=shuffled frag=192 activity=0.10 iters=8 reps=5 sizeof(OOP)=40 sizeof(flat)=24

| Variant | B/gate | ns/eval (median) | min | max | spread | cycles/eval | IPC | branch miss/eval | L1 miss/eval | time vs first (paired median) |
|---|---|---|---|---|---|---|---|---|---|---|
| a heap+virtual | 40 | 116.12 | 115.78 | 116.51 | 0.6% | 475.28 | 0.15 | 0.0001 | 2.4376 | x1.000 |
| d flat24+SIMA | 24 | 61.85 | 60.37 | 64.32 | 6.4% | 253.29 | 0.28 | 0.0001 | 2.0058 | x0.533 |
| e flat32+SIMA | 32 | 75.96 | 73.13 | 76.92 | 5.0% | 310.89 | 0.23 | 0.0001 | 1.7560 | x0.655 |
| g flat40+SIMA | 40 | 83.79 | 83.39 | 85.22 | 2.2% | 343.27 | 0.21 | 0.0001 | 2.0074 | x0.721 |

evals/rep=7999992 changed/rep=7999992 fingerprint-check=identical
