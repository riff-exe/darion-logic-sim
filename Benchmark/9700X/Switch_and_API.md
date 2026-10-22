# Zen 5 (Ryzen 7 9700X): SIMA versus a type switch in the real engine, UI-queue cost and API latency (2026-10-22)

Stored so that Claims 1 and 7 have data behind them on the main machine.

## SIMA versus `switch(type)` (Claim 1)

Two scratch copies of `reactor/` built from the same sources with the same flags as `scripts/build.sh` (`-O3 -g -fno-omit-frame-pointer`, plus `-march=native` from `setup.py`), one with `-DDARION_EVAL_SWITCH`; `tests/ablation_eval.py <build> <label> b14 b15 b17 b19`, 3,000 logical vectors (the default), best of 3, pinned to core 2, the two builds alternated twice.

| Circuit | mode | SIMA best of 3, round 1 / 2 (ms) | switch best of 3, round 1 / 2 (ms) | switch / SIMA, round 1 / 2 | same evals and fingerprint |
|---|---|---:|---:|---:|---|
| b14 | prop | 168.1 / 166.1 | 288.2 / 291.6 | **1.71** / **1.76** | yes |
| b14 | sweep | 120.0 / 118.7 | 178.1 / 185.0 | **1.48** / **1.56** | yes |
| b15 | prop | 79.6 / 79.8 | 110.0 / 109.5 | **1.38** / **1.37** | yes |
| b15 | sweep | 95.9 / 96.4 | 115.4 / 110.4 | **1.20** / **1.15** | yes |
| b17 | prop | 269.3 / 266.7 | 354.4 / 353.1 | **1.32** / **1.32** | yes |
| b17 | sweep | 305.5 / 297.4 | 342.8 / 349.9 | **1.12** / **1.18** | yes |
| b19 | prop | 1480.1 / 1481.0 | 2040.2 / 2071.9 | **1.38** / **1.40** | yes |
| b19 | sweep | 1507.0 / 1509.0 | 1766.8 / 1742.7 | **1.17** / **1.15** | yes |

The switch costs 1.32-1.76x on the propagate engine and 1.12-1.56x on the sweep, with identical evaluation counts and final-state fingerprints. Stored Claim 1 values: 1.38-1.69x and 1.10-1.48x. *Note on the stored table:* its b19 row (749.8 ms SIMA) was measured with 1,500 logical vectors, half the count of the other rows; at 1,500 the production build takes 738.5 ms for b19 here, at 3,000 it takes 1,480-1,534 ms. The ratios do not depend on this.

## Cost of the visual queue (Claim 7)

`tests/ablation_eval.py --ui-cost reactor <circuit> prop|sweep`, pinned:

```
b15 prop: 24329 gates, 238400 toggles, distinct gates queued per run 8588
  blind           engine      79.1 ms (1.000x blind, spread  0.8%)  python drain    0.00 ms
  ui-queue        engine      79.1 ms (1.001x blind, spread  0.2%)  python drain    0.00 ms
  ui-queue+drain  engine      79.1 ms (1.000x blind, spread  0.1%)  python drain    0.22 ms
b15 sweep: 24329 gates, 238400 toggles, distinct gates queued per run 8742
  blind           engine      94.2 ms (1.000x blind, spread  4.4%)  python drain    0.00 ms
  ui-queue        engine      94.0 ms (0.998x blind, spread  4.6%)  python drain    0.00 ms
  ui-queue+drain  engine      93.5 ms (0.992x blind, spread  7.0%)  python drain    0.23 ms
b17 prop: 73475 gates, 244360 toggles, distinct gates queued per run 18371
  blind           engine     259.8 ms (1.000x blind, spread  2.0%)  python drain    0.00 ms
  ui-queue        engine     259.7 ms (1.000x blind, spread  0.2%)  python drain    0.00 ms
  ui-queue+drain  engine     259.8 ms (1.000x blind, spread  0.3%)  python drain    0.52 ms
b17 sweep: 73475 gates, 244360 toggles, distinct gates queued per run 18406
  blind           engine     291.9 ms (1.000x blind, spread  1.7%)  python drain    0.00 ms
  ui-queue        engine     292.4 ms (1.002x blind, spread  3.4%)  python drain    0.00 ms
  ui-queue+drain  engine     292.9 ms (1.004x blind, spread  3.6%)  python drain    0.49 ms
```

Engine time with the changed-gate queue active is 0.992-1.004x the blind time (stored 0.995-1.004x); draining 8.6k-18.4k queued gates from Python takes 0.22-0.52 ms (stored 0.3 and 0.7 ms).

## API latency (Claim 7)

`tests/ablation_eval.py --latency reactor <circuit>`, 20,000 calls each, pinned:

```
b15: 24329 gates, 38 inputs, 20000 calls each
  empty cpdef call (floor)   median     0.06 us   p99     0.07 us   max       1.6 us
  read gate.output           median     0.07 us   p99     0.08 us   max       1.0 us
  toggle(loc, val)           median     0.28 us   p99    13.57 us   max      31.5 us
  batch_toggle, 1 input      median     0.55 us   p99    13.87 us   max      26.1 us
  batch_toggle, all inputs   median    14.27 us   p99    28.16 us   max      56.3 us
b19: 356399 gates, 47 inputs, 20000 calls each
  empty cpdef call (floor)   median     0.06 us   p99     0.07 us   max       4.0 us
  read gate.output           median     0.07 us   p99     0.08 us   max       2.8 us
  toggle(loc, val)           median     0.34 us   p99   241.86 us   max     796.5 us
  batch_toggle, 1 input      median     0.58 us   p99   245.52 us   max     320.0 us
  batch_toggle, all inputs   median   194.72 us   p99   437.10 us   max     594.2 us
```

`toggle` median 0.28 us (b15) and 0.34 us (b19), one-input `batch_toggle` 0.55-0.58 us, a whole input vector 14 us and 195 us, p99 14 us and 242 us; the worst single call seen on b19 was 0.80 ms this time (stored 0.69 ms).
