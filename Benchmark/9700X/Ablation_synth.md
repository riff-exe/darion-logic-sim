# Zen 5 (Ryzen 7 9700X): ablation harness, synthetic topologies (2026-10-22)

Paper_Notes 6b step 5 on the main machine: chain, tree, random DAG and mixed-gate chain at 1k, 10k, 100k and 1M gates, topological and shuffled with `--frag 192`, 9 repeats, variants abcdge, pinned to core 2, machine idle; plus the predictor-memorization run (`mixchain --n 1000 --vary`, last row). Columns as in `Ablation_real.md`.




| Configuration | a heap+virtual | b arena | c switch | d SIMA | e 32 B | g 40 B | a/d | b/a | c/a | d/c | branch miss/eval a / d | max spread | fingerprints |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| topology=chain gates=1000 placement=topological frag=0 iters=8008 reps=9 | 4.95 | 4.95 | 2.55 | 2.58 | 2.58 | 2.57 | **1.92** | 1.00 | 0.52 | 1.01 | 0.001 / 0.001 | 1% | identical |
| topology=chain gates=1000 placement=shuffled frag=192 iters=8008 reps=9 | 4.95 | 4.95 | 2.64 | 2.57 | 2.81 | 2.91 | **1.93** | 1.00 | 0.53 | 0.97 | 0.001 / 0.001 | 1% | identical |
| topology=chain gates=10000 placement=topological frag=0 iters=800 reps=9 | 4.96 | 4.96 | 2.53 | 2.55 | 2.56 | 2.56 | **1.95** | 1.00 | 0.51 | 1.01 | 0.000 / 0.000 | 1% | identical |
| topology=chain gates=10000 placement=shuffled frag=192 iters=800 reps=9 | 7.60 | 4.95 | 3.55 | 3.47 | 3.59 | 3.78 | **2.19** | 0.65 | 0.47 | 0.98 | 0.000 / 0.000 | 1% | identical |
| topology=chain gates=100000 placement=topological frag=0 iters=80 reps=9 | 4.97 | 4.97 | 2.60 | 2.60 | 2.60 | 2.67 | **1.91** | 1.00 | 0.52 | 1.00 | 0.000 / 0.000 | 0% | identical |
| topology=chain gates=100000 placement=shuffled frag=192 iters=80 reps=9 | 12.69 | 10.45 | 9.33 | 9.16 | 9.16 | 9.76 | **1.39** | 0.82 | 0.74 | 0.98 | 0.000 / 0.000 | 35% | identical |
| topology=chain gates=1000000 placement=topological frag=0 iters=8 reps=9 | 4.98 | 4.98 | 2.60 | 2.66 | 2.67 | 2.80 | **1.87** | 1.00 | 0.52 | 1.02 | 0.000 / 0.000 | 3% | identical |
| topology=chain gates=1000000 placement=shuffled frag=192 iters=8 reps=9 | 84.88 | 42.75 | 13.23 | 12.85 | 26.81 | 43.44 | **6.61** | 0.50 | 0.16 | 0.97 | 0.000 / 0.000 | 25% | identical |
| topology=tree gates=1023 placement=topological frag=0 iters=36925 reps=9 | 3.80 | 3.75 | 2.96 | 2.75 | 2.79 | 2.85 | **1.38** | 0.99 | 0.78 | 0.93 | 0.043 / 0.041 | 1% | identical |
| topology=tree gates=1023 placement=shuffled frag=192 iters=36925 reps=9 | 3.96 | 3.81 | 2.99 | 2.78 | 2.84 | 2.92 | **1.42** | 0.96 | 0.76 | 0.93 | 0.043 / 0.041 | 1% | identical |
| topology=tree gates=16383 placement=topological frag=0 iters=2291 reps=9 | 4.63 | 4.48 | 3.59 | 3.38 | 3.57 | 3.79 | **1.37** | 0.97 | 0.78 | 0.94 | 0.004 / 0.004 | 0% | identical |
| topology=tree gates=16383 placement=shuffled frag=192 iters=2291 reps=9 | 6.15 | 5.37 | 4.40 | 4.08 | 4.28 | 4.56 | **1.51** | 0.87 | 0.72 | 0.93 | 0.004 / 0.004 | 3% | identical |
| topology=tree gates=131071 placement=topological frag=0 iters=286 reps=9 | 6.03 | 5.50 | 4.74 | 4.63 | 4.80 | 5.13 | **1.30** | 0.91 | 0.79 | 0.98 | 0.001 / 0.001 | 3% | identical |
| topology=tree gates=131071 placement=shuffled frag=192 iters=286 reps=9 | 10.69 | 7.73 | 7.34 | 7.04 | 7.20 | 7.15 | **1.52** | 0.72 | 0.69 | 0.96 | 0.001 / 0.001 | 8% | identical |
| topology=tree gates=1048575 placement=topological frag=0 iters=35 reps=9 | 21.53 | 18.88 | 16.06 | 15.29 | 16.54 | 18.60 | **1.41** | 0.88 | 0.75 | 0.95 | 0.000 / 0.001 | 2% | identical |
| topology=tree gates=1048575 placement=shuffled frag=192 iters=35 reps=9 | 38.88 | 28.49 | 22.06 | 21.49 | 23.37 | 26.67 | **1.81** | 0.73 | 0.57 | 0.97 | 0.000 / 0.000 | 4% | identical |
| topology=random gates=1000 placement=topological frag=0 iters=14094 reps=9 | 10.93 | 10.79 | 10.03 | 4.83 | 4.96 | 4.85 | **2.26** | 0.99 | 0.92 | 0.48 | 1.195 / 0.643 | 1% | identical |
| topology=random gates=1000 placement=shuffled frag=192 iters=13943 reps=9 | 11.18 | 10.81 | 10.04 | 4.87 | 4.95 | 4.87 | **2.30** | 0.97 | 0.90 | 0.49 | 1.208 / 0.642 | 1% | identical |
| topology=random gates=10000 placement=topological frag=0 iters=175 reps=9 | 13.16 | 13.10 | 10.99 | 5.18 | 5.36 | 5.27 | **2.54** | 1.00 | 0.84 | 0.47 | 1.314 / 0.581 | 1% | identical |
| topology=random gates=10000 placement=shuffled frag=192 iters=205 reps=9 | 14.10 | 13.47 | 11.17 | 5.31 | 5.48 | 5.46 | **2.66** | 0.96 | 0.79 | 0.48 | 1.318 / 0.582 | 1% | identical |
| topology=random gates=100000 placement=topological frag=0 iters=6 reps=9 | 17.77 | 17.42 | 14.32 | 7.79 | 7.98 | 8.10 | **2.28** | 0.98 | 0.81 | 0.54 | 1.450 / 0.575 | 3% | identical |
| topology=random gates=100000 placement=shuffled frag=192 iters=4 reps=9 | 19.81 | 17.97 | 15.54 | 8.67 | 8.82 | 8.95 | **2.28** | 0.91 | 0.78 | 0.56 | 1.453 / 0.574 | 3% | identical |
| topology=random gates=1000000 placement=topological frag=0 iters=1 reps=9 | 31.22 | 28.42 | 22.19 | 15.25 | 16.22 | 18.88 | **2.05** | 0.91 | 0.71 | 0.69 | 1.477 / 0.578 | 14% | identical |
| topology=random gates=1000000 placement=shuffled frag=192 iters=1 reps=9 | 39.40 | 30.99 | 25.02 | 17.65 | 18.39 | 20.83 | **2.23** | 0.79 | 0.64 | 0.71 | 1.485 / 0.579 | 11% | identical |
| topology=mixchain gates=1018 placement=topological frag=0 iters=8000 reps=9 | 4.92 | 4.92 | 2.56 | 2.58 | 2.58 | 2.59 | **1.91** | 1.00 | 0.52 | 1.01 | 0.002 / 0.001 | 0% | identical |
| topology=mixchain gates=1018 placement=shuffled frag=192 iters=8000 reps=9 | 4.91 | 4.91 | 2.66 | 2.59 | 2.85 | 2.95 | **1.90** | 1.00 | 0.54 | 0.97 | 0.002 / 0.001 | 0% | identical |
| topology=mixchain gates=10159 placement=topological frag=0 iters=800 reps=9 | 8.44 | 8.35 | 7.93 | 2.56 | 2.56 | 2.56 | **3.30** | 0.99 | 0.94 | 0.32 | 0.873 / 0.000 | 3% | identical |
| topology=mixchain gates=10159 placement=shuffled frag=192 iters=800 reps=9 | 13.29 | 9.93 | 8.10 | 3.49 | 3.64 | 3.81 | **3.81** | 0.75 | 0.61 | 0.43 | 0.873 / 0.000 | 1% | identical |
| topology=mixchain gates=101565 placement=topological frag=0 iters=80 reps=9 | 8.63 | 8.48 | 7.96 | 2.58 | 2.59 | 2.59 | **3.34** | 0.98 | 0.92 | 0.32 | 0.874 / 0.000 | 2% | identical |
| topology=mixchain gates=101565 placement=shuffled frag=192 iters=80 reps=9 | 17.34 | 13.83 | 11.65 | 9.23 | 9.23 | 9.84 | **1.88** | 0.80 | 0.67 | 0.79 | 0.874 / 0.000 | 2% | identical |
| topology=mixchain gates=1015628 placement=topological frag=0 iters=8 reps=9 | 8.60 | 8.49 | 7.96 | 2.64 | 2.66 | 2.78 | **3.26** | 0.99 | 0.93 | 0.33 | 0.875 / 0.000 | 3% | identical |
| topology=mixchain gates=1015628 placement=shuffled frag=192 iters=8 reps=9 | 86.20 | 46.81 | 13.35 | 12.61 | 27.42 | 44.28 | **6.84** | 0.54 | 0.15 | 0.94 | 1.292 / 0.000 | 14% | identical |
| topology=mixchain gates=1018 placement=topological frag=0 iters=9503 reps=9 | 8.56 | 8.54 | 7.05 | 2.84 | - | - | **3.01** | 1.00 | 0.82 | 0.40 | 0.693 / 0.004 | 1% | identical |

**Fingerprints:** identical in all 33 configurations.

**Agreement with the stored Claim 13 synthetic table:** NOT chain a/d 1.87-1.95 (stored 1.9); mixed-gate chain 1.90 at 1k and 3.26-3.34 from 10k (stored 1.9 and 3.3); random DAG a 10.9 / 13.2 / 17.8 / 31.2 ns and d 4.8 / 5.2 / 7.8 / 15.3 ns at 1k-1M (stored 10.9 / 13.1 / 17.8 / 32.0 and 4.7 / 5.0 / 7.6 / 15.7); tree 1.30-1.41 (stored 1.4). Struct-size cliff, 1M-gate shuffled chain: d 12.85, e 26.81, g 43.44 ns (stored single calls 12.6-13.0, 27-29, 44), and a/b 84.9 / 42.8 ns (stored 84.5 / 42.8). This run was on an idle machine; the 7-process repeat in `Slow_mode.md` (19.7 / 40.2 / 53.6 ns) was not, which is why its absolute values are higher. Predictor memorization: with `--vary` at 1k gates the virtual-call variant mispredicts 0.69 times per evaluation against 0.002 without it (stored 0.70 and 0.00).
