# Zen 5 machine record (main machine for every Zen 5 number)

```
CPU(s):                                  16
Model name:                              AMD Ryzen 7 9700X 8-Core Processor
Thread(s) per core:                      2
Core(s) per socket:                      8
CPU(s) scaling MHz:                      70%
L1d cache:                               384 KiB (8 instances)
L1i cache:                               256 KiB (8 instances)
L2 cache:                                8 MiB (8 instances)
L3 cache:                                32 MiB (1 instance)
kernel: 7.2.11-arch1-1
perf_event_paranoid: 2
governor (cpu2): performance
SMT sibling of cpu2: 2,10
THP: [always] madvise never
g++ (GCC) 16.2.1 20260810
Python: Python 3.14.8
Verilator 5.052 2026-09-05 rev v5.052
Icarus Verilog version 13.0 (stable) (v13_0-dirty)
```

Recorded 2026-10-22. Note: `tests/src/perf.py` pins to core 2, whose SMT sibling is cpu 10 on this machine (the laptop's is cpu 3).
