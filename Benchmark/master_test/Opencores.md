# Master Test Unified Benchmark Report: tests/IWLS2005/opencores

**Execution Parameters:**
- **Target Suite / Path:** `tests/IWLS2005/opencores`
- **Circuits Benchmarked:** 21
- **Simulation Vectors (Phase 3):** 50,000 (Warmup: 10)
- **Verification Vectors (Phase 2):** 100
- **Hardware Profiler:** Linux `perf` kernel PMU counters
- **Note (2026-10-22):** re-run after the Verilator library fix: Verilator now compiles `iwls_sequential_harness.verilator_gsclib()` (the cell library with its sequential UDPs as nonblocking modules), because Verilator 5.052 lowers the original UDP flops to blocking assignments, which is order-dependent and slow. Icarus uses the original library; Darion simulates every flop as the 10-gate NAND master-slave of `tests/src/DFFSR.json`, so the flop models differ between the three tools (not a same-netlist comparison). The previous report (blocking-UDP Verilator) is in git history.

---

## 1. Zero-Testbench Memory Footprint (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | 184 | 0.58 MB (28.2 MB peak) | N/A | 0.48 MB (8.4 MB peak) | 0.69 MB (4.4 MB peak) |
| steppermotordrive.v | 258 | 1.07 MB (28.6 MB peak) | N/A | 1.07 MB (8.9 MB peak) | 0.80 MB (4.4 MB peak) |
| ss_pcm.v | 648 | 2.44 MB (30.0 MB peak) | N/A | 2.14 MB (10.0 MB peak) | 0.74 MB (4.4 MB peak) |
| usb_phy.v | 715 | 2.59 MB (30.1 MB peak) | N/A | 2.49 MB (10.4 MB peak) | 0.71 MB (4.4 MB peak) |
| sasc.v | 1,125 | 3.28 MB (30.8 MB peak) | N/A | 2.66 MB (10.6 MB peak) | 0.70 MB (4.4 MB peak) |
| simple_spi.v | 1,489 | 3.78 MB (31.4 MB peak) | N/A | 3.99 MB (11.9 MB peak) | 0.71 MB (4.3 MB peak) |
| pci_spoci_ctrl.v | 1,696 | 2.93 MB (30.5 MB peak) | N/A | 5.29 MB (13.1 MB peak) | 0.72 MB (4.4 MB peak) |
| i2c.v | 1,496 | 3.74 MB (31.3 MB peak) | N/A | 5.37 MB (13.2 MB peak) | 0.74 MB (4.4 MB peak) |
| systemcdes.v | 4,326 | 8.04 MB (35.6 MB peak) | N/A | 13.67 MB (21.6 MB peak) | 0.69 MB (4.4 MB peak) |
| spi.v | 4,531 | 7.90 MB (35.5 MB peak) | N/A | 14.99 MB (22.9 MB peak) | 0.71 MB (4.4 MB peak) |
| wb_dma.v | 5,720 | 15.85 MB (43.4 MB peak) | N/A | 15.95 MB (23.8 MB peak) | 0.78 MB (4.5 MB peak) |
| des_area.v | 6,445 | 9.01 MB (36.6 MB peak) | N/A | 18.95 MB (26.8 MB peak) | 0.91 MB (4.6 MB peak) |
| tv80.v | 10,607 | 17.81 MB (45.4 MB peak) | N/A | 31.08 MB (38.9 MB peak) | N/A |
| systemcaes.v | 14,071 | 24.79 MB (53.2 MB peak) | N/A | 40.89 MB (48.8 MB peak) | 1.02 MB (4.7 MB peak) |
| mem_ctrl.v | 16,796 | 29.34 MB (56.9 MB peak) | N/A | 54.03 MB (61.9 MB peak) | 0.97 MB (4.6 MB peak) |
| ac97_ctrl.v | 19,069 | 47.02 MB (74.5 MB peak) | N/A | 65.62 MB (73.4 MB peak) | 0.99 MB (4.7 MB peak) |
| usb_funct.v | 18,282 | 41.78 MB (69.3 MB peak) | N/A | 59.27 MB (67.1 MB peak) | 0.95 MB (4.6 MB peak) |
| aes_core.v | 25,565 | 31.69 MB (62.3 MB peak) | N/A | 78.79 MB (86.7 MB peak) | 1.10 MB (4.8 MB peak) |
| wb_conmax.v | 49,326 | 46.79 MB (79.4 MB peak) | N/A | 144.04 MB (152.0 MB peak) | 1.09 MB (4.8 MB peak) |
| des_perf.v | 111,781 | 204.47 MB (242.7 MB peak) | N/A | 440.60 MB (448.5 MB peak) | 1.84 MB (5.5 MB peak) |
| vga_lcd.v | 187,445 | 374.18 MB (417.9 MB peak) | N/A | 592.75 MB (600.5 MB peak) | 1.92 MB (5.5 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | 184 | 0.17 ms (0.015 ms opt) | N/A | 5.03 ms | 2.55 s |
| steppermotordrive.v | 258 | 0.46 ms (0.058 ms opt) | N/A | 7.17 ms | 2.54 s |
| ss_pcm.v | 648 | 1.29 ms (0.134 ms opt) | N/A | 11.37 ms | 2.58 s |
| usb_phy.v | 715 | 1.45 ms (0.173 ms opt) | N/A | 13.28 ms | 2.62 s |
| sasc.v | 1,125 | 1.82 ms (0.197 ms opt) | N/A | 13.95 ms | 2.61 s |
| simple_spi.v | 1,489 | 2.20 ms (0.246 ms opt) | N/A | 21.00 ms | 2.67 s |
| pci_spoci_ctrl.v | 1,696 | 1.71 ms (0.223 ms opt) | N/A | 24.22 ms | 2.71 s |
| i2c.v | 1,496 | 2.26 ms (0.339 ms opt) | N/A | 28.73 ms | 2.76 s |
| systemcdes.v | 4,326 | 5.19 ms (0.595 ms opt) | N/A | 71.38 ms | 3.25 s |
| spi.v | 4,531 | 5.63 ms (0.739 ms opt) | N/A | 69.14 ms | 3.30 s |
| wb_dma.v | 5,720 | 10.18 ms (0.990 ms opt) | N/A | 72.35 ms | 3.37 s |
| des_area.v | 6,445 | 5.76 ms (0.741 ms opt) | N/A | 92.55 ms | 4.11 s |
| tv80.v | 10,607 | 11.64 ms (1.470 ms opt) | N/A | 155.32 ms | N/A |
| systemcaes.v | 14,071 | 16.35 ms (1.905 ms opt) | N/A | 197.38 ms | 6.86 s |
| mem_ctrl.v | 16,796 | 24.78 ms (4.010 ms opt) | N/A | 270.30 ms | 6.91 s |
| ac97_ctrl.v | 19,069 | 38.56 ms (7.096 ms opt) | N/A | 307.52 ms | 7.59 s |
| usb_funct.v | 18,282 | 32.95 ms (6.161 ms opt) | N/A | 307.31 ms | 7.63 s |
| aes_core.v | 25,565 | 25.83 ms (5.089 ms opt) | N/A | 418.64 ms | 10.13 s |
| wb_conmax.v | 49,326 | 49.67 ms (14.317 ms opt) | N/A | 835.96 ms | 15.65 s |
| des_perf.v | 111,781 | 323.86 ms (64.407 ms opt) | N/A | 2.36 s | 63.72 s |
| vga_lcd.v | 187,445 | 609.23 ms (104.237 ms opt) | N/A | 3.24 s | 106.23 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | 22.54 ms | 29.70 ms | 36.52 ms | N/A | 877.75 ms | 1.94 ms |
| steppermotordrive.v | 48.64 ms | 59.63 ms | 87.33 ms | N/A | 97.76 ms | 6.65 ms |
| ss_pcm.v | 221.33 ms | 250.89 ms | 382.96 ms | N/A | 576.78 ms | 16.42 ms |
| usb_phy.v | 235.72 ms | 252.44 ms | 414.58 ms | N/A | 422.20 ms | 14.53 ms |
| sasc.v | 296.90 ms | 296.19 ms | 528.22 ms | N/A | 519.86 ms | 14.36 ms |
| simple_spi.v | 278.60 ms | 267.45 ms | 428.21 ms | N/A | 602.93 ms | 14.47 ms |
| pci_spoci_ctrl.v | 200.01 ms | 198.04 ms | 460.86 ms | N/A | 815.63 ms | 24.69 ms |
| i2c.v | 331.52 ms | 307.97 ms | 585.56 ms | N/A | 1125.19 ms | 36.50 ms |
| systemcdes.v | 2587.60 ms | 1901.04 ms | 6435.16 ms | N/A | 15.49 s | 96.57 ms |
| spi.v | 522.38 ms | 577.61 ms | 815.41 ms | N/A | 2356.33 ms | 87.64 ms |
| wb_dma.v | 1365.93 ms | 1487.89 ms | 2361.64 ms | N/A | 5750.42 ms | 61.48 ms |
| des_area.v | 2699.96 ms | 2103.28 ms | 6356.31 ms | N/A | 50.67 s | 97.00 ms |
| tv80.v | 782.90 ms | 1025.87 ms | 1346.10 ms | N/A | 1007.47 ms | 142.39 ms |
| systemcaes.v | 2210.62 ms | 2463.63 ms | 4542.47 ms | N/A | 20.43 s | 306.11 ms |
| mem_ctrl.v | 2185.83 ms | 2745.03 ms | 4351.62 ms | N/A | 7315.70 ms | 255.29 ms |
| ac97_ctrl.v | 4006.17 ms | 4009.63 ms | 7273.42 ms | N/A | 4909.58 ms | 179.87 ms |
| usb_funct.v | 1554.53 ms | 2446.42 ms | 2780.79 ms | N/A | 8042.32 ms | 226.04 ms |
| aes_core.v | 8714.54 ms | 9556.95 ms | 22.59 s | N/A | 28.09 s | 235.17 ms |
| wb_conmax.v | 3807.83 ms | 5422.98 ms | 6655.43 ms | N/A | 103.69 s | 732.21 ms |
| des_perf.v | 103.19 s | 108.08 s | 251.11 s | N/A | 558.60 s | 2466.37 ms |
| vga_lcd.v | 38.29 s | 39.37 s | 70.41 s | N/A | 59.76 s | 2171.85 ms |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | 38.94x | 29.55x | 24.03x | N/A | 1.00x | 453.47x |
| steppermotordrive.v | 2.01x | 1.64x | 1.12x | N/A | 1.00x | 14.70x |
| ss_pcm.v | 2.61x | 2.30x | 1.51x | N/A | 1.00x | 35.12x |
| usb_phy.v | 1.79x | 1.67x | 1.02x | N/A | 1.00x | 29.05x |
| sasc.v | 1.75x | 1.76x | 0.98x | N/A | 1.00x | 36.19x |
| simple_spi.v | 2.16x | 2.25x | 1.41x | N/A | 1.00x | 41.66x |
| pci_spoci_ctrl.v | 4.08x | 4.12x | 1.77x | N/A | 1.00x | 33.03x |
| i2c.v | 3.39x | 3.65x | 1.92x | N/A | 1.00x | 30.82x |
| systemcdes.v | 5.99x | 8.15x | 2.41x | N/A | 1.00x | 160.41x |
| spi.v | 4.51x | 4.08x | 2.89x | N/A | 1.00x | 26.89x |
| wb_dma.v | 4.21x | 3.86x | 2.43x | N/A | 1.00x | 93.53x |
| des_area.v | 18.77x | 24.09x | 7.97x | N/A | 1.00x | 522.40x |
| tv80.v | 1.29x | 0.98x | 0.75x | N/A | 1.00x | 7.08x |
| systemcaes.v | 9.24x | 8.29x | 4.50x | N/A | 1.00x | 66.73x |
| mem_ctrl.v | 3.35x | 2.67x | 1.68x | N/A | 1.00x | 28.66x |
| ac97_ctrl.v | 1.23x | 1.22x | 0.68x | N/A | 1.00x | 27.30x |
| usb_funct.v | 5.17x | 3.29x | 2.89x | N/A | 1.00x | 35.58x |
| aes_core.v | 3.22x | 2.94x | 1.24x | N/A | 1.00x | 119.47x |
| wb_conmax.v | 27.23x | 19.12x | 15.58x | N/A | 1.00x | 141.61x |
| des_perf.v | 5.41x | 5.17x | 2.22x | N/A | 1.00x | 226.49x |
| vga_lcd.v | 1.56x | 1.52x | 0.85x | N/A | 1.00x | 27.52x |

### Total Gate Evaluations

| Circuit | Gates | rx-prop Evals | rx-sweep Evals | rx-oop Evals | Pure Python Evals |
|:---|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | 184 | 5,392,574 | 5,120,319 | 5,392,574 | N/A |
| steppermotordrive.v | 258 | 23,717,113 | 23,611,913 | 23,717,113 | N/A |
| ss_pcm.v | 648 | 89,309,054 | 87,878,978 | 89,532,104 | N/A |
| usb_phy.v | 715 | 94,303,037 | 93,846,669 | 94,354,187 | N/A |
| sasc.v | 1,125 | 121,402,307 | 111,250,788 | 124,377,711 | N/A |
| simple_spi.v | 1,489 | 119,413,667 | 114,375,704 | 119,440,293 | N/A |
| pci_spoci_ctrl.v | 1,696 | 90,088,151 | 71,150,933 | 89,778,069 | N/A |
| i2c.v | 1,496 | 144,790,757 | 133,856,428 | 145,278,617 | N/A |
| systemcdes.v | 4,326 | 772,228,933 | 461,566,720 | 788,685,222 | N/A |
| spi.v | 4,531 | 234,455,303 | 227,362,614 | 234,702,648 | N/A |
| wb_dma.v | 5,720 | 572,583,673 | 548,443,835 | 576,577,418 | N/A |
| des_area.v | 6,445 | 737,296,590 | 416,181,580 | 757,389,026 | N/A |
| tv80.v | 10,607 | 335,979,209 | 337,627,357 | 339,703,774 | N/A |
| systemcaes.v | 14,071 | 899,077,652 | 835,961,603 | 908,136,485 | N/A |
| mem_ctrl.v | 16,796 | 936,995,633 | 902,722,740 | 938,916,603 | N/A |
| ac97_ctrl.v | 19,069 | 1,647,126,400 | 1,637,956,615 | 1,647,138,602 | N/A |
| usb_funct.v | 18,282 | 582,823,894 | 577,881,813 | 583,041,399 | N/A |
| aes_core.v | 25,565 | 2,147,934,816 | 2,098,290,932 | 2,180,414,370 | N/A |
| wb_conmax.v | 49,326 | 1,282,138,675 | 1,225,583,003 | 1,283,273,835 | N/A |
| des_perf.v | 111,781 | 20,771,797,777 | 19,213,988,869 | 20,807,534,081 | N/A |
| vga_lcd.v | 187,445 | 14,127,284,006 | 14,022,765,964 | 14,127,453,690 | N/A |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `4.11x`
- **rx-sweep (Linear Compiled):** `3.78x`
- **rx-oop (OOP Graph):** `2.16x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `54.62x`

### Gate Evaluation Highlights

- **Reactor Sweep vs Propagate Total Evaluations Ratio:** `0.91x` (propagate performed more evaluations)

### Cross-Engine Comparisons

- **Reactor Sweep vs Propagate Ratio:** `0.92x` (propagate faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | Instructions | Cycles | IPC | L1 Loads | L1 Misses | L2 Loads | L2 Misses | L3 Loads | DRAM Loads | Branches | Branch Misses |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| pci_conf_cyc_addr_dec.v | rx-prop | 206.40M | 86.60M | 2.38 | 145.75M | 1.12M | 1.12M | 19.73K | 100.78K | 83.94K | 38.25M | 1.24M |
| pci_conf_cyc_addr_dec.v | rx-sweep (Linear) | 242.22M | 117.39M | 2.06 | 146.37M | 1.57M | 1.57M | 28.73K | 704.31K | 678.88K | 54.64M | 2.15M |
| pci_conf_cyc_addr_dec.v | rx-oop (OOP Engine) | 278.41M | 146.75M | 1.90 | 203.34M | 2.35M | 2.35M | 58.00K | 1.18M | 1.03M | 44.24M | 1.71M |
| pci_conf_cyc_addr_dec.v | Icarus Verilog | 12.77B | 3.23B | 3.95 | 4.96B | 27.61M | 27.61M | 58.86K | 108.83K | 12.84K | 2.73B | 13.46M |
| pci_conf_cyc_addr_dec.v | Verilator C++ | 26.99M | 11.06M | 2.44 | 12.96M | 59.23K | 59.23K | 2.51K | 2.51K | 0.00 | 6.38M | 1.62K |
| steppermotordrive.v | rx-prop | 695.55M | 166.96M | 4.17 | 295.28M | 584.40K | 584.40K | 6.20K | 37.94K | 28.89K | 71.98M | 199.96K |
| steppermotordrive.v | rx-sweep (Linear) | 869.10M | 209.31M | 4.15 | 335.87M | 1.24M | 1.24M | 21.23K | 36.71K | 28.69K | 188.45M | 1.37M |
| steppermotordrive.v | rx-oop (OOP Engine) | 817.62M | 298.63M | 2.74 | 514.06M | 3.13M | 3.13M | 14.61K | 73.24K | 45.88K | 98.16M | 733.95K |
| steppermotordrive.v | Icarus Verilog | 1.58B | 399.71M | 3.95 | 648.06M | 1.33M | 1.33M | 37.07K | 101.99K | 13.44K | 321.65M | 2.17M |
| steppermotordrive.v | Verilator C++ | 14.94M | 6.33M | 2.36 | 25.72M | 19.61K | 19.61K | 485.00 | 34.01K | 56.00 | 3.40M | 24.99K |
| ss_pcm.v | rx-prop | 2.80B | 818.34M | 3.42 | 1.13B | 82.79M | 82.79M | 105.17K | 2.31M | 2.23M | 284.92M | 3.14M |
| ss_pcm.v | rx-sweep (Linear) | 3.24B | 930.12M | 3.48 | 1.15B | 116.84M | 116.84M | 92.10K | 1.97M | 1.91M | 640.04M | 9.05M |
| ss_pcm.v | rx-oop (OOP Engine) | 3.17B | 1.40B | 2.27 | 1.98B | 144.09M | 144.09M | 69.76K | 964.96K | 845.29K | 386.37M | 6.35M |
| ss_pcm.v | Icarus Verilog | 8.07B | 2.19B | 3.68 | 3.69B | 72.47M | 72.47M | 130.72K | 214.22K | 17.06K | 1.58B | 14.24M |
| ss_pcm.v | Verilator C++ | 80.01M | 57.96M | 1.38 | 53.41M | 10.01K | 10.01K | 207.00 | 65.68K | 469.00 | 11.62M | 55.00K |
| usb_phy.v | rx-prop | 2.92B | 874.04M | 3.34 | 1.16B | 93.36M | 93.36M | 87.78K | 1.46M | 1.41M | 288.46M | 3.30M |
| usb_phy.v | rx-sweep (Linear) | 3.46B | 928.00M | 3.72 | 1.19B | 123.82M | 123.82M | 72.07K | 1.37M | 1.34M | 678.81M | 7.52M |
| usb_phy.v | rx-oop (OOP Engine) | 3.26B | 1.49B | 2.19 | 2.08B | 176.33M | 176.33M | 85.24K | 633.73K | 475.99K | 394.66M | 7.00M |
| usb_phy.v | Icarus Verilog | 5.68B | 1.63B | 3.48 | 2.57B | 49.84M | 49.84M | 168.40K | 360.00K | 11.32K | 1.12B | 12.08M |
| usb_phy.v | Verilator C++ | 61.03M | 41.83M | 1.46 | 59.08M | 51.65K | 51.65K | 3.28K | 43.63K | 16.34K | 7.26M | 49.29K |
| sasc.v | rx-prop | 3.74B | 1.09B | 3.42 | 1.49B | 136.18M | 136.18M | 83.24K | 1.93M | 1.86M | 371.33M | 3.67M |
| sasc.v | rx-sweep (Linear) | 4.20B | 1.09B | 3.87 | 1.42B | 157.54M | 157.54M | 87.11K | 1.53M | 1.51M | 847.34M | 8.97M |
| sasc.v | rx-oop (OOP Engine) | 4.39B | 1.92B | 2.28 | 2.77B | 235.05M | 235.05M | 95.89K | 613.25K | 429.10K | 529.94M | 8.98M |
| sasc.v | Icarus Verilog | 7.01B | 1.96B | 3.58 | 3.28B | 73.23M | 73.23M | 295.79K | 610.33K | 37.41K | 1.39B | 12.88M |
| sasc.v | Verilator C++ | 89.99M | 39.91M | 2.25 | 70.22M | 94.74K | 94.74K | 642.00 | 91.20K | 10.04K | 7.73M | 78.98K |
| simple_spi.v | rx-prop | 3.62B | 1.02B | 3.55 | 1.43B | 142.70M | 142.70M | 93.72K | 1.42M | 1.32M | 352.10M | 1.67M |
| simple_spi.v | rx-sweep (Linear) | 4.51B | 993.34M | 4.54 | 1.39B | 177.29M | 177.29M | 98.68K | 2.25M | 2.22M | 941.73M | 4.07M |
| simple_spi.v | rx-oop (OOP Engine) | 4.10B | 1.54B | 2.66 | 2.50B | 264.51M | 264.51M | 46.22K | 704.22K | 585.08K | 496.69M | 3.51M |
| simple_spi.v | Icarus Verilog | 8.82B | 2.32B | 3.81 | 3.95B | 109.06M | 109.06M | 204.34K | 385.31K | 21.78K | 1.73B | 12.73M |
| simple_spi.v | Verilator C++ | 104.96M | 35.91M | 2.92 | 70.17M | 11.21K | 11.21K | 595.00 | 9.68K | 16.00 | 6.77M | 40.56K |
| pci_spoci_ctrl.v | rx-prop | 2.74B | 736.33M | 3.72 | 1.14B | 56.42M | 56.42M | 35.16K | 801.40K | 771.52K | 283.98M | 1.87M |
| pci_spoci_ctrl.v | rx-sweep (Linear) | 3.18B | 752.04M | 4.22 | 1.01B | 112.17M | 112.17M | 80.45K | 2.31M | 2.27M | 655.98M | 3.65M |
| pci_spoci_ctrl.v | rx-oop (OOP Engine) | 3.20B | 1.70B | 1.89 | 2.30B | 119.60M | 119.60M | 91.38K | 2.41M | 2.16M | 400.17M | 14.05M |
| pci_spoci_ctrl.v | Icarus Verilog | 11.15B | 3.15B | 3.54 | 5.17B | 148.79M | 148.79M | 459.73K | 1.03M | 71.28K | 2.17B | 20.36M |
| pci_spoci_ctrl.v | Verilator C++ | 204.34M | 86.38M | 2.37 | 123.75M | 12.45K | 12.45K | 3.84K | 130.22K | 95.76K | 12.16M | 49.95K |
| i2c.v | rx-prop | 4.30B | 1.21B | 3.55 | 1.73B | 155.54M | 155.54M | 115.31K | 1.97M | 1.87M | 418.12M | 2.28M |
| i2c.v | rx-sweep (Linear) | 5.00B | 1.14B | 4.39 | 1.62B | 194.16M | 194.16M | 84.71K | 2.16M | 2.14M | 1.02B | 5.38M |
| i2c.v | rx-oop (OOP Engine) | 5.01B | 2.13B | 2.35 | 3.19B | 273.15M | 273.15M | 106.33K | 2.03M | 1.70M | 605.12M | 10.32M |
| i2c.v | Icarus Verilog | 16.18B | 4.21B | 3.84 | 7.41B | 308.98M | 308.98M | 9.70M | 15.76M | 94.27K | 3.18B | 19.09M |
| i2c.v | Verilator C++ | 221.81M | 136.63M | 1.62 | 132.13M | 76.60K | 76.60K | 1.05K | 11.73K | 1.76K | 12.71M | 46.41K |
| systemcdes.v | rx-prop | 24.19B | 9.49B | 2.55 | 9.95B | 908.26M | 908.26M | 2.50M | 17.27M | 12.93M | 2.42B | 122.87M |
| systemcdes.v | rx-sweep (Linear) | 16.82B | 7.04B | 2.39 | 6.72B | 638.75M | 638.75M | 968.60K | 14.88M | 13.32M | 2.87B | 117.38M |
| systemcdes.v | rx-oop (OOP Engine) | 28.37B | 23.25B | 1.22 | 23.71B | 1.37B | 1.37B | 18.73M | 42.33M | 11.72M | 3.46B | 298.03M |
| systemcdes.v | Icarus Verilog | 154.60B | 56.28B | 2.75 | 83.28B | 2.93B | 2.93B | 611.60M | 872.27M | 1.16M | 30.40B | 401.00M |
| systemcdes.v | Verilator C++ | 553.59M | 341.72M | 1.62 | 333.71M | 250.12K | 250.12K | 4.94K | 256.03K | 241.51K | 9.45M | 63.12K |
| spi.v | rx-prop | 7.01B | 1.94B | 3.62 | 2.80B | 306.15M | 306.15M | 440.96K | 5.08M | 4.35M | 685.57M | 3.47M |
| spi.v | rx-sweep (Linear) | 9.43B | 2.13B | 4.43 | 2.90B | 425.77M | 425.77M | 315.57K | 4.83M | 4.48M | 2.03B | 10.95M |
| spi.v | rx-oop (OOP Engine) | 8.01B | 2.98B | 2.69 | 4.82B | 480.32M | 480.32M | 1.01M | 5.79M | 3.73M | 966.88M | 8.61M |
| spi.v | Icarus Verilog | 34.48B | 8.93B | 3.86 | 15.65B | 617.52M | 617.52M | 103.27M | 194.22M | 551.00K | 6.75B | 31.98M |
| spi.v | Verilator C++ | 552.01M | 310.88M | 1.78 | 325.71M | 111.94K | 111.94K | 3.61K | 103.99K | 93.33K | 11.83M | 81.21K |
| wb_dma.v | rx-prop | 18.52B | 5.20B | 3.56 | 7.50B | 777.61M | 777.61M | 1.88M | 23.51M | 20.29M | 1.98B | 13.69M |
| wb_dma.v | rx-sweep (Linear) | 21.55B | 5.65B | 3.82 | 7.43B | 932.60M | 932.60M | 2.82M | 26.84M | 21.43M | 4.45B | 48.49M |
| wb_dma.v | rx-oop (OOP Engine) | 20.98B | 8.67B | 2.42 | 12.87B | 1.29B | 1.29B | 60.36M | 136.88M | 17.93M | 2.66B | 26.23M |
| wb_dma.v | Icarus Verilog | 87.81B | 21.61B | 4.06 | 38.64B | 604.24M | 604.24M | 128.72M | 219.29M | 878.86K | 16.97B | 73.12M |
| wb_dma.v | Verilator C++ | 498.68M | 216.84M | 2.30 | 258.48M | 52.68K | 52.68K | 1.21K | 217.31K | 180.34K | 14.92M | 52.81K |
| des_area.v | rx-prop | 24.17B | 10.01B | 2.41 | 10.15B | 816.48M | 816.48M | 2.60M | 26.62M | 22.59M | 2.58B | 143.08M |
| des_area.v | rx-sweep (Linear) | 16.66B | 7.86B | 2.12 | 7.08B | 581.39M | 581.39M | 2.61M | 27.70M | 22.87M | 3.09B | 153.19M |
| des_area.v | rx-oop (OOP Engine) | 28.19B | 23.09B | 1.22 | 23.48B | 1.31B | 1.31B | 34.60M | 73.45M | 21.59M | 3.54B | 295.84M |
| des_area.v | Icarus Verilog | 582.67B | 183.26B | 3.18 | 228.41B | 5.68B | 5.68B | 1.12B | 1.42B | 3.18M | 137.18B | 788.26M |
| des_area.v | Verilator C++ | 795.49M | 341.13M | 2.33 | 456.18M | 123.75K | 123.75K | 4.65K | 156.58K | 155.22K | 9.07M | 123.47K |
| tv80.v | rx-prop | 9.97B | 2.82B | 3.54 | 3.91B | 445.97M | 445.97M | 1.62M | 3.92M | 714.07K | 927.47M | 5.07M |
| tv80.v | rx-sweep (Linear) | 15.79B | 3.69B | 4.28 | 4.54B | 714.26M | 714.26M | 11.56M | 28.88M | 728.56K | 3.43B | 19.43M |
| tv80.v | rx-oop (OOP Engine) | 11.65B | 4.82B | 2.42 | 7.30B | 726.75M | 726.75M | 11.81M | 22.77M | 1.37M | 1.38B | 17.98M |
| tv80.v | Icarus Verilog | 13.97B | 4.40B | 3.17 | 6.34B | 241.18M | 241.18M | 28.06M | 41.84M | 603.68K | 2.85B | 25.76M |
| tv80.v | Verilator C++ | 705.95M | 508.94M | 1.39 | 531.19M | 25.03K | 25.03K | 1.79K | 34.87K | 2.38K | 8.87M | 37.75K |
| systemcaes.v | rx-prop | 27.92B | 8.26B | 3.38 | 11.26B | 1.07B | 1.07B | 44.36M | 120.78M | 26.59M | 2.86B | 30.26M |
| systemcaes.v | rx-sweep (Linear) | 33.82B | 9.19B | 3.68 | 11.17B | 1.43B | 1.43B | 92.72M | 368.83M | 25.59M | 6.96B | 75.18M |
| systemcaes.v | rx-oop (OOP Engine) | 31.93B | 16.61B | 1.92 | 21.30B | 1.74B | 1.74B | 333.77M | 689.90M | 22.15M | 3.96B | 86.23M |
| systemcaes.v | Icarus Verilog | 308.24B | 75.05B | 4.11 | 137.81B | 4.29B | 4.29B | 1.17B | 2.02B | 3.96M | 56.52B | 177.96M |
| systemcaes.v | Verilator C++ | 1.93B | 1.09B | 1.76 | 891.98M | 84.36K | 84.36K | 3.04K | 43.38K | 41.73K | 13.77M | 99.35K |
| mem_ctrl.v | rx-prop | 28.18B | 8.00B | 3.52 | 11.11B | 1.15B | 1.15B | 41.41M | 81.20M | 10.98M | 2.70B | 16.12M |
| mem_ctrl.v | rx-sweep (Linear) | 37.76B | 9.95B | 3.80 | 11.85B | 1.74B | 1.74B | 126.46M | 558.03M | 11.19M | 8.11B | 67.91M |
| mem_ctrl.v | rx-oop (OOP Engine) | 32.28B | 15.65B | 2.06 | 20.42B | 2.00B | 2.00B | 484.54M | 1.11B | 9.44M | 3.90B | 40.22M |
| mem_ctrl.v | Icarus Verilog | 101.46B | 27.92B | 3.63 | 45.51B | 1.21B | 1.21B | 536.38M | 913.50M | 2.51M | 19.68B | 77.69M |
| mem_ctrl.v | Verilator C++ | 1.73B | 917.72M | 1.89 | 1.01B | 172.63K | 172.63K | 3.97K | 33.42K | 23.01K | 15.44M | 128.42K |
| ac97_ctrl.v | rx-prop | 48.71B | 14.42B | 3.38 | 19.07B | 2.04B | 2.04B | 220.18M | 571.32M | 7.98M | 4.51B | 8.88M |
| ac97_ctrl.v | rx-sweep (Linear) | 63.35B | 14.48B | 4.38 | 19.54B | 2.73B | 2.73B | 200.35M | 1.28B | 8.80M | 13.30B | 50.18M |
| ac97_ctrl.v | rx-oop (OOP Engine) | 56.13B | 26.10B | 2.15 | 34.45B | 3.67B | 3.67B | 1.21B | 3.39B | 6.70M | 6.67B | 18.76M |
| ac97_ctrl.v | Icarus Verilog | 67.28B | 19.26B | 3.49 | 27.83B | 1.02B | 1.02B | 493.01M | 968.97M | 3.44M | 13.99B | 38.70M |
| ac97_ctrl.v | Verilator C++ | 1.21B | 638.68M | 1.90 | 682.15M | 44.47K | 44.47K | 2.48K | 195.67K | 144.02K | 15.02M | 64.73K |
| usb_funct.v | rx-prop | 17.76B | 5.71B | 3.11 | 7.15B | 770.53M | 770.53M | 86.15M | 223.47M | 12.34M | 1.77B | 9.98M |
| usb_funct.v | rx-sweep (Linear) | 34.19B | 8.91B | 3.84 | 9.28B | 1.61B | 1.61B | 143.17M | 588.28M | 12.77M | 8.04B | 60.63M |
| usb_funct.v | rx-oop (OOP Engine) | 20.22B | 10.08B | 2.01 | 12.79B | 1.28B | 1.28B | 372.17M | 841.08M | 10.94M | 2.49B | 21.78M |
| usb_funct.v | Icarus Verilog | 116.15B | 30.63B | 3.79 | 50.68B | 1.68B | 1.68B | 504.34M | 854.15M | 2.28M | 22.63B | 74.33M |
| usb_funct.v | Verilator C++ | 1.15B | 796.79M | 1.45 | 907.18M | 42.90K | 42.90K | 2.38K | 33.64K | 4.09K | 10.26M | 109.07K |
| aes_core.v | rx-prop | 67.82B | 31.59B | 2.15 | 27.68B | 3.31B | 3.31B | 567.71M | 1.01B | 25.28M | 6.77B | 334.48M |
| aes_core.v | rx-sweep (Linear) | 79.12B | 34.57B | 2.29 | 29.70B | 3.86B | 3.86B | 504.88M | 1.52B | 25.63M | 11.79B | 428.82M |
| aes_core.v | rx-oop (OOP Engine) | 79.76B | 81.42B | 0.98 | 75.07B | 4.46B | 4.46B | 1.28B | 2.13B | 24.99M | 9.66B | 906.27M |
| aes_core.v | Icarus Verilog | 277.48B | 103.60B | 2.68 | 147.79B | 3.85B | 3.85B | 2.00B | 2.55B | 9.19M | 52.89B | 597.56M |
| aes_core.v | Verilator C++ | 1.59B | 834.22M | 1.90 | 969.73M | 84.07K | 84.07K | 7.50K | 43.81K | 35.24K | 9.49M | 39.73K |
| wb_conmax.v | rx-prop | 44.43B | 15.10B | 2.94 | 18.72B | 1.77B | 1.77B | 337.90M | 857.20M | 114.91M | 5.34B | 39.99M |
| wb_conmax.v | rx-sweep (Linear) | 65.05B | 20.89B | 3.11 | 21.38B | 3.00B | 3.00B | 377.38M | 1.98B | 112.80M | 14.89B | 185.78M |
| wb_conmax.v | rx-oop (OOP Engine) | 47.65B | 25.46B | 1.87 | 30.77B | 2.67B | 2.67B | 920.57M | 1.98B | 98.77M | 6.52B | 89.58M |
| wb_conmax.v | Icarus Verilog | 1447.85B | 379.78B | 3.81 | 646.82B | 39.51B | 39.51B | 6.29B | 9.07B | 144.97M | 274.09B | 577.96M |
| wb_conmax.v | Verilator C++ | 5.94B | 2.63B | 2.26 | 3.15B | 293.12K | 293.12K | 1.36M | 1.61M | 231.62K | 14.66M | 209.48K |
| des_perf.v | rx-prop | 629.92B | 370.48B | 1.70 | 252.79B | 32.22B | 32.22B | 17.25B | 35.03B | 70.48M | 59.16B | 2.95B |
| des_perf.v | rx-sweep (Linear) | 642.95B | 388.38B | 1.66 | 271.30B | 30.18B | 30.18B | 13.31B | 31.52B | 85.06M | 99.92B | 4.99B |
| des_perf.v | rx-oop (OOP Engine) | 733.71B | 901.88B | 0.81 | 669.81B | 42.84B | 42.84B | 28.84B | 50.11B | 1.77B | 86.91B | 6.78B |
| des_perf.v | Icarus Verilog | 59.59B | 50.04B | 1.19 | 33.53B | 1.35B | 1.35B | 861.43M | 1.15B | 263.21M | 12.26B | 179.84M |
| des_perf.v | Verilator C++ | 10.79B | 8.81B | 1.23 | 6.75B | 13.81M | 13.81M | 608.72M | 610.80M | 97.23K | 11.41M | 67.36K |
| vga_lcd.v | rx-prop | 412.98B | 137.56B | 3.00 | 160.33B | 17.76B | 17.76B | 4.48B | 19.53B | 25.31M | 37.45B | 33.91M |
| vga_lcd.v | rx-sweep (Linear) | 540.05B | 141.37B | 3.82 | 170.27B | 23.56B | 23.56B | 4.57B | 25.12B | 58.63M | 113.71B | 588.75M |
| vga_lcd.v | rx-oop (OOP Engine) | 477.46B | 252.12B | 1.89 | 294.53B | 30.30B | 30.30B | 10.15B | 35.91B | 756.41M | 56.23B | 94.48M |
| vga_lcd.v | Icarus Verilog | 38.61B | 18.42B | 2.10 | 15.65B | 821.75M | 821.75M | 178.27M | 271.78M | 33.20M | 8.32B | 87.68M |
| vga_lcd.v | Verilator C++ | 7.05B | 7.76B | 0.91 | 5.68B | 6.74M | 6.74M | 185.03M | 187.09M | 37.83K | 17.10M | 146.23K |
