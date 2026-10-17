# Master Test Unified Benchmark Report: tests/IWLS2005/opencores

**Execution Parameters:**
- **Target Suite / Path:** `tests/IWLS2005/opencores`
- **Circuits Benchmarked:** 21
- **Simulation Vectors (Phase 3):** 50,000 (Warmup: 10)
- **Verification Vectors (Phase 2):** 100
- **Hardware Profiler:** Linux `perf` kernel PMU counters

---

## 1. Zero-Testbench Memory Footprint (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | 184 | 0.38 MB (30.3 MB peak) | N/A | 0.56 MB (8.4 MB peak) | 0.70 MB (4.4 MB peak) |
| steppermotordrive.v | 258 | 0.86 MB (28.7 MB peak) | N/A | 1.08 MB (8.9 MB peak) | 0.71 MB (4.4 MB peak) |
| ss_pcm.v | 648 | 2.15 MB (30.0 MB peak) | N/A | 2.11 MB (9.9 MB peak) | 0.74 MB (4.4 MB peak) |
| usb_phy.v | 715 | 2.36 MB (30.1 MB peak) | N/A | 2.57 MB (10.4 MB peak) | 0.74 MB (4.4 MB peak) |
| sasc.v | 1,125 | 2.97 MB (30.9 MB peak) | N/A | 2.64 MB (10.6 MB peak) | 0.77 MB (4.5 MB peak) |
| simple_spi.v | 1,489 | 3.45 MB (31.3 MB peak) | N/A | 3.92 MB (11.8 MB peak) | 0.82 MB (4.5 MB peak) |
| pci_spoci_ctrl.v | 1,696 | 2.66 MB (30.5 MB peak) | N/A | 5.12 MB (13.0 MB peak) | 0.76 MB (4.5 MB peak) |
| i2c.v | 1,496 | 5.41 MB (33.3 MB peak) | N/A | 5.24 MB (13.2 MB peak) | 0.71 MB (4.4 MB peak) |
| systemcdes.v | 4,326 | 6.77 MB (34.6 MB peak) | N/A | 13.60 MB (21.5 MB peak) | 0.90 MB (4.6 MB peak) |
| spi.v | 4,531 | 7.55 MB (35.4 MB peak) | N/A | 15.04 MB (22.9 MB peak) | 0.82 MB (4.5 MB peak) |
| wb_dma.v | 5,720 | 15.96 MB (43.8 MB peak) | N/A | 16.07 MB (24.0 MB peak) | 0.91 MB (4.6 MB peak) |
| des_area.v | 6,445 | 7.95 MB (35.8 MB peak) | N/A | 19.02 MB (26.8 MB peak) | 0.95 MB (4.6 MB peak) |
| tv80.v | 10,607 | 17.83 MB (45.7 MB peak) | N/A | 31.12 MB (39.0 MB peak) | N/A |
| systemcaes.v | 14,071 | 24.24 MB (52.7 MB peak) | N/A | 40.95 MB (48.8 MB peak) | 1.14 MB (4.8 MB peak) |
| mem_ctrl.v | 16,796 | 33.57 MB (63.2 MB peak) | N/A | 54.02 MB (61.9 MB peak) | 1.37 MB (5.0 MB peak) |
| ac97_ctrl.v | 19,069 | 47.61 MB (75.5 MB peak) | N/A | 65.51 MB (73.4 MB peak) | 1.56 MB (5.2 MB peak) |
| usb_funct.v | 18,282 | 39.61 MB (67.5 MB peak) | N/A | 59.46 MB (67.2 MB peak) | 1.34 MB (5.0 MB peak) |
| aes_core.v | 25,565 | 29.35 MB (60.4 MB peak) | N/A | 78.77 MB (86.7 MB peak) | 1.19 MB (4.9 MB peak) |
| wb_conmax.v | 49,326 | 48.05 MB (81.2 MB peak) | N/A | 144.24 MB (152.1 MB peak) | 1.25 MB (4.9 MB peak) |
| des_perf.v | 111,781 | 201.63 MB (240.6 MB peak) | N/A | 440.61 MB (448.5 MB peak) | 2.58 MB (6.3 MB peak) |
| vga_lcd.v | 187,445 | 370.74 MB (414.7 MB peak) | N/A | 592.68 MB (600.5 MB peak) | 3.29 MB (7.0 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | 184 | 0.33 ms (0.015 ms opt) | N/A | 4.62 ms | 2.50 s |
| steppermotordrive.v | 258 | 0.80 ms (0.057 ms opt) | N/A | 6.93 ms | 2.50 s |
| ss_pcm.v | 648 | 1.49 ms (0.133 ms opt) | N/A | 10.86 ms | 2.53 s |
| usb_phy.v | 715 | 1.63 ms (0.166 ms opt) | N/A | 13.69 ms | 2.58 s |
| sasc.v | 1,125 | 2.04 ms (0.204 ms opt) | N/A | 13.22 ms | 2.67 s |
| simple_spi.v | 1,489 | 2.44 ms (0.252 ms opt) | N/A | 19.45 ms | 2.73 s |
| pci_spoci_ctrl.v | 1,696 | 2.02 ms (0.258 ms opt) | N/A | 24.47 ms | 2.67 s |
| i2c.v | 1,496 | 2.42 ms (0.283 ms opt) | N/A | 23.68 ms | 2.87 s |
| systemcdes.v | 4,326 | 5.17 ms (0.588 ms opt) | N/A | 59.45 ms | 3.35 s |
| spi.v | 4,531 | 5.35 ms (0.611 ms opt) | N/A | 65.01 ms | 3.72 s |
| wb_dma.v | 5,720 | 9.51 ms (0.989 ms opt) | N/A | 69.02 ms | 5.03 s |
| des_area.v | 6,445 | 5.63 ms (0.705 ms opt) | N/A | 84.71 ms | 4.15 s |
| tv80.v | 10,607 | 10.53 ms (1.358 ms opt) | N/A | 141.34 ms | N/A |
| systemcaes.v | 14,071 | 16.55 ms (1.886 ms opt) | N/A | 190.06 ms | 9.51 s |
| mem_ctrl.v | 16,796 | 22.58 ms (3.232 ms opt) | N/A | 258.87 ms | 15.30 s |
| ac97_ctrl.v | 19,069 | 43.99 ms (6.655 ms opt) | N/A | 300.96 ms | 11.94 s |
| usb_funct.v | 18,282 | 39.44 ms (5.249 ms opt) | N/A | 293.37 ms | 11.01 s |
| aes_core.v | 25,565 | 31.71 ms (4.271 ms opt) | N/A | 409.82 ms | 9.07 s |
| wb_conmax.v | 49,326 | 54.13 ms (12.227 ms opt) | N/A | 817.55 ms | 17.65 s |
| des_perf.v | 111,781 | 312.73 ms (63.292 ms opt) | N/A | 2.35 s | 74.09 s |
| vga_lcd.v | 187,445 | 614.60 ms (96.249 ms opt) | N/A | 3.17 s | 147.31 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | 22.08 ms | 30.09 ms | 37.36 ms | N/A | 892.45 ms | 1.80 ms |
| steppermotordrive.v | 47.78 ms | 59.77 ms | 93.52 ms | N/A | 95.74 ms | 20.02 ms |
| ss_pcm.v | 219.93 ms | 262.20 ms | 405.97 ms | N/A | 567.83 ms | 50.63 ms |
| usb_phy.v | 232.68 ms | 256.17 ms | 431.30 ms | N/A | 407.95 ms | 50.16 ms |
| sasc.v | 297.17 ms | 328.71 ms | 556.45 ms | N/A | 507.16 ms | 64.56 ms |
| simple_spi.v | 282.69 ms | 301.93 ms | 465.83 ms | N/A | 598.42 ms | 93.35 ms |
| pci_spoci_ctrl.v | 199.75 ms | 227.80 ms | 477.01 ms | N/A | 802.92 ms | 63.06 ms |
| i2c.v | 330.61 ms | 349.44 ms | 629.45 ms | N/A | 1100.88 ms | 115.13 ms |
| systemcdes.v | 2505.61 ms | 2002.32 ms | 6444.34 ms | N/A | 15.36 s | 242.59 ms |
| spi.v | 519.00 ms | 675.38 ms | 897.41 ms | N/A | 2371.84 ms | 218.89 ms |
| wb_dma.v | 1382.40 ms | 1560.21 ms | 2476.54 ms | N/A | 5736.14 ms | 386.27 ms |
| des_area.v | 2555.77 ms | 2270.33 ms | 6240.52 ms | N/A | 51.06 s | 299.92 ms |
| tv80.v | 780.99 ms | 1198.79 ms | 1440.35 ms | N/A | 1000.81 ms | 414.02 ms |
| systemcaes.v | 2205.09 ms | 2798.22 ms | 4818.22 ms | N/A | 20.45 s | 744.03 ms |
| mem_ctrl.v | 2194.28 ms | 2881.09 ms | 4528.12 ms | N/A | 7269.59 ms | 950.79 ms |
| ac97_ctrl.v | 4058.44 ms | 4572.23 ms | 7707.43 ms | N/A | 4910.52 ms | 1218.89 ms |
| usb_funct.v | 1565.56 ms | 2868.48 ms | 2893.69 ms | N/A | 8141.21 ms | 1282.92 ms |
| aes_core.v | 8408.40 ms | 10.34 s | 22.00 s | N/A | 27.84 s | 921.28 ms |
| wb_conmax.v | 3947.47 ms | 6134.74 ms | 7187.32 ms | N/A | 101.53 s | 1622.16 ms |
| des_perf.v | 100.28 s | 102.22 s | 228.96 s | N/A | 552.76 s | 31.24 s |
| vga_lcd.v | 36.18 s | 40.51 s | 68.11 s | N/A | 59.58 s | 51.25 s |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | 40.41x | 29.66x | 23.89x | N/A | 1.00x | 497.03x |
| steppermotordrive.v | 2.00x | 1.60x | 1.02x | N/A | 1.00x | 4.78x |
| ss_pcm.v | 2.58x | 2.17x | 1.40x | N/A | 1.00x | 11.22x |
| usb_phy.v | 1.75x | 1.59x | 0.95x | N/A | 1.00x | 8.13x |
| sasc.v | 1.71x | 1.54x | 0.91x | N/A | 1.00x | 7.86x |
| simple_spi.v | 2.12x | 1.98x | 1.28x | N/A | 1.00x | 6.41x |
| pci_spoci_ctrl.v | 4.02x | 3.52x | 1.68x | N/A | 1.00x | 12.73x |
| i2c.v | 3.33x | 3.15x | 1.75x | N/A | 1.00x | 9.56x |
| systemcdes.v | 6.13x | 7.67x | 2.38x | N/A | 1.00x | 63.33x |
| spi.v | 4.57x | 3.51x | 2.64x | N/A | 1.00x | 10.84x |
| wb_dma.v | 4.15x | 3.68x | 2.32x | N/A | 1.00x | 14.85x |
| des_area.v | 19.98x | 22.49x | 8.18x | N/A | 1.00x | 170.26x |
| tv80.v | 1.28x | 0.83x | 0.69x | N/A | 1.00x | 2.42x |
| systemcaes.v | 9.27x | 7.31x | 4.24x | N/A | 1.00x | 27.48x |
| mem_ctrl.v | 3.31x | 2.52x | 1.61x | N/A | 1.00x | 7.65x |
| ac97_ctrl.v | 1.21x | 1.07x | 0.64x | N/A | 1.00x | 4.03x |
| usb_funct.v | 5.20x | 2.84x | 2.81x | N/A | 1.00x | 6.35x |
| aes_core.v | 3.31x | 2.69x | 1.27x | N/A | 1.00x | 30.22x |
| wb_conmax.v | 25.72x | 16.55x | 14.13x | N/A | 1.00x | 62.59x |
| des_perf.v | 5.51x | 5.41x | 2.41x | N/A | 1.00x | 17.70x |
| vga_lcd.v | 1.65x | 1.47x | 0.87x | N/A | 1.00x | 1.16x |

### Total Gate Evaluations

| Circuit | Gates | rx-prop Evals | rx-sweep Evals | rx-oop Evals | Pure Python Evals |
|:---|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | 184 | 5,392,574 | 5,120,319 | 5,392,574 | N/A |
| steppermotordrive.v | 258 | 23,717,113 | 24,212,742 | 23,717,113 | N/A |
| ss_pcm.v | 648 | 89,309,054 | 87,884,380 | 89,532,104 | N/A |
| usb_phy.v | 715 | 94,303,037 | 94,119,059 | 94,354,187 | N/A |
| sasc.v | 1,125 | 121,402,307 | 112,797,152 | 124,377,711 | N/A |
| simple_spi.v | 1,489 | 119,413,667 | 114,555,779 | 119,440,293 | N/A |
| pci_spoci_ctrl.v | 1,696 | 90,088,151 | 70,531,752 | 89,778,069 | N/A |
| i2c.v | 1,496 | 144,790,757 | 134,518,240 | 145,278,617 | N/A |
| systemcdes.v | 4,326 | 772,228,933 | 437,185,596 | 788,685,222 | N/A |
| spi.v | 4,531 | 234,455,249 | 227,095,968 | 234,702,648 | N/A |
| wb_dma.v | 5,720 | 574,083,385 | 547,433,206 | 578,078,202 | N/A |
| des_area.v | 6,445 | 737,296,590 | 415,562,551 | 757,389,026 | N/A |
| tv80.v | 10,607 | 335,979,209 | 334,814,524 | 339,703,774 | N/A |
| systemcaes.v | 14,071 | 902,122,183 | 816,589,406 | 908,136,485 | N/A |
| mem_ctrl.v | 16,796 | 936,994,709 | 903,255,740 | 938,916,603 | N/A |
| ac97_ctrl.v | 19,069 | 1,647,126,400 | 1,637,746,473 | 1,647,138,602 | N/A |
| usb_funct.v | 18,282 | 582,823,894 | 577,879,277 | 583,041,399 | N/A |
| aes_core.v | 25,565 | 2,147,934,816 | 1,955,822,064 | 2,180,414,370 | N/A |
| wb_conmax.v | 49,326 | 1,282,138,675 | 1,224,547,509 | 1,283,273,835 | N/A |
| des_perf.v | 111,781 | 20,771,797,777 | 18,642,919,801 | 20,807,534,081 | N/A |
| vga_lcd.v | 187,445 | 14,127,284,006 | 14,024,791,415 | 14,127,453,690 | N/A |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `4.11x`
- **rx-sweep (Linear Compiled):** `3.46x`
- **rx-oop (OOP Graph):** `2.07x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `14.00x`

### Gate Evaluation Highlights

- **Reactor Sweep vs Propagate Total Evaluations Ratio:** `0.90x` (propagate performed more evaluations)

### Cross-Engine Comparisons

- **Reactor Sweep vs Propagate Ratio:** `0.84x` (propagate faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | Instructions | Cycles | IPC | L1 Loads | L1 Misses | L2 Loads | L2 Misses | L3 Loads | DRAM Loads | Branches | Branch Misses |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| pci_conf_cyc_addr_dec.v | rx-prop | 235.15M | 89.50M | 2.63 | 115.15M | 1.34M | 1.34M | 18.38K | 298.65K | 265.94K | 33.80M | 1.13M |
| pci_conf_cyc_addr_dec.v | rx-sweep (Linear) | 231.34M | 118.55M | 1.95 | 131.80M | 1.51M | 1.51M | 25.34K | 339.96K | 308.92K | 52.68M | 2.04M |
| pci_conf_cyc_addr_dec.v | rx-oop (OOP Engine) | 236.79M | 141.65M | 1.67 | 199.08M | 1.81M | 1.81M | 23.72K | 506.43K | 415.71K | 42.39M | 1.68M |
| pci_conf_cyc_addr_dec.v | Icarus Verilog | 12.75B | 3.29B | 3.87 | 4.90B | 27.82M | 27.82M | 27.09K | 58.51K | 12.96K | 2.74B | 14.89M |
| pci_conf_cyc_addr_dec.v | Verilator C++ | 10.17M | 4.26M | 2.39 | 7.31M | 57.53K | 57.53K | 1.00K | 1.00K | 0.00 | 3.33M | 293.00 |
| steppermotordrive.v | rx-prop | 716.36M | 171.47M | 4.18 | 294.06M | 287.59K | 287.59K | 5.48K | 31.00K | 5.36K | 72.54M | 197.21K |
| steppermotordrive.v | rx-sweep (Linear) | 943.89M | 220.27M | 4.29 | 310.79M | 1.18M | 1.18M | 12.91K | 44.52K | 9.34K | 187.91M | 1.08M |
| steppermotordrive.v | rx-oop (OOP Engine) | 834.66M | 335.50M | 2.49 | 474.05M | 4.65M | 4.65M | 5.15K | 63.78K | 9.91K | 102.39M | 730.12K |
| steppermotordrive.v | Icarus Verilog | 1.53B | 381.68M | 4.01 | 655.32M | 1.14M | 1.14M | 38.51K | 101.68K | 3.58K | 316.67M | 2.12M |
| steppermotordrive.v | Verilator C++ | 110.40M | 73.51M | 1.50 | 72.74M | 15.68K | 15.68K | 1.16K | 3.99K | 1.00 | 21.02M | 310.11K |
| ss_pcm.v | rx-prop | 2.77B | 813.40M | 3.40 | 1.10B | 87.75M | 87.75M | 77.67K | 1.21M | 1.18M | 267.75M | 3.30M |
| ss_pcm.v | rx-sweep (Linear) | 3.21B | 983.54M | 3.27 | 1.13B | 125.98M | 125.98M | 94.90K | 2.25M | 2.22M | 641.65M | 9.18M |
| ss_pcm.v | rx-oop (OOP Engine) | 3.13B | 1.48B | 2.12 | 1.83B | 157.92M | 157.92M | 62.79K | 950.15K | 717.20K | 385.01M | 6.28M |
| ss_pcm.v | Icarus Verilog | 8.10B | 2.17B | 3.74 | 3.68B | 72.21M | 72.21M | 52.37K | 176.62K | 19.39K | 1.58B | 13.13M |
| ss_pcm.v | Verilator C++ | 313.81M | 166.85M | 1.88 | 207.79M | 56.33K | 56.33K | 616.00 | 14.52K | 753.00 | 43.23M | 878.13K |
| usb_phy.v | rx-prop | 2.86B | 844.27M | 3.38 | 1.14B | 98.54M | 98.54M | 39.45K | 104.89K | 68.20K | 278.77M | 3.58M |
| usb_phy.v | rx-sweep (Linear) | 3.41B | 944.02M | 3.61 | 1.17B | 129.58M | 129.58M | 72.70K | 846.15K | 814.14K | 674.38M | 6.79M |
| usb_phy.v | rx-oop (OOP Engine) | 3.24B | 1.56B | 2.08 | 1.90B | 182.59M | 182.59M | 47.81K | 560.72K | 462.69K | 399.40M | 6.81M |
| usb_phy.v | Icarus Verilog | 5.69B | 1.58B | 3.60 | 2.55B | 48.75M | 48.75M | 86.75K | 190.53K | 6.36K | 1.11B | 10.64M |
| usb_phy.v | Verilator C++ | 340.52M | 171.65M | 1.98 | 203.59M | 43.26K | 43.26K | 361.00 | 32.18K | 126.00 | 48.84M | 904.68K |
| sasc.v | rx-prop | 3.70B | 1.08B | 3.44 | 1.47B | 137.47M | 137.47M | 59.21K | 697.53K | 636.69K | 355.09M | 3.87M |
| sasc.v | rx-sweep (Linear) | 4.22B | 1.21B | 3.49 | 1.43B | 175.16M | 175.16M | 83.06K | 1.63M | 1.61M | 855.97M | 10.27M |
| sasc.v | rx-oop (OOP Engine) | 4.31B | 2.01B | 2.15 | 2.56B | 257.01M | 257.01M | 71.41K | 695.58K | 511.76K | 524.96M | 8.79M |
| sasc.v | Icarus Verilog | 7.16B | 1.94B | 3.68 | 3.22B | 70.90M | 70.90M | 126.84K | 271.29K | 6.27K | 1.40B | 11.80M |
| sasc.v | Verilator C++ | 553.50M | 232.71M | 2.38 | 300.19M | 61.35K | 61.35K | 331.00 | 9.30K | 207.00 | 56.18M | 940.73K |
| simple_spi.v | rx-prop | 3.61B | 1.04B | 3.48 | 1.41B | 158.08M | 158.08M | 40.12K | 791.36K | 746.22K | 342.93M | 1.71M |
| simple_spi.v | rx-sweep (Linear) | 4.46B | 1.11B | 4.01 | 1.40B | 195.03M | 195.03M | 86.09K | 1.28M | 1.26M | 941.25M | 5.79M |
| simple_spi.v | rx-oop (OOP Engine) | 4.09B | 1.69B | 2.41 | 2.30B | 267.88M | 267.88M | 57.35K | 562.80K | 387.23K | 498.96M | 3.68M |
| simple_spi.v | Icarus Verilog | 8.85B | 2.31B | 3.83 | 3.91B | 107.11M | 107.11M | 250.62K | 504.92K | 19.63K | 1.73B | 12.02M |
| simple_spi.v | Verilator C++ | 633.28M | 333.02M | 1.90 | 336.40M | 108.45K | 108.45K | 2.34K | 8.24K | 0.00 | 67.63M | 578.10K |
| pci_spoci_ctrl.v | rx-prop | 2.79B | 746.86M | 3.73 | 1.10B | 57.10M | 57.10M | 69.61K | 2.10M | 2.07M | 273.81M | 2.10M |
| pci_spoci_ctrl.v | rx-sweep (Linear) | 3.09B | 858.05M | 3.60 | 967.54M | 109.24M | 109.24M | 130.45K | 2.46M | 2.42M | 648.12M | 4.69M |
| pci_spoci_ctrl.v | rx-oop (OOP Engine) | 3.08B | 1.70B | 1.81 | 2.14B | 137.81M | 137.81M | 75.40K | 2.06M | 1.76M | 384.39M | 13.71M |
| pci_spoci_ctrl.v | Icarus Verilog | 11.12B | 3.10B | 3.58 | 5.18B | 148.05M | 148.05M | 541.35K | 1.11M | 21.78K | 2.17B | 18.97M |
| pci_spoci_ctrl.v | Verilator C++ | 507.67M | 229.06M | 2.22 | 253.44M | 23.79K | 23.79K | 477.00 | 10.76K | 308.00 | 45.93M | 298.29K |
| i2c.v | rx-prop | 4.29B | 1.20B | 3.56 | 1.71B | 150.96M | 150.96M | 87.09K | 1.40M | 1.35M | 400.47M | 2.42M |
| i2c.v | rx-sweep (Linear) | 4.97B | 1.28B | 3.88 | 1.61B | 195.46M | 195.46M | 83.55K | 1.87M | 1.85M | 1.01B | 6.52M |
| i2c.v | rx-oop (OOP Engine) | 4.91B | 2.27B | 2.16 | 2.93B | 285.79M | 285.79M | 95.65K | 1.17M | 916.54K | 592.50M | 10.07M |
| i2c.v | Icarus Verilog | 16.23B | 4.15B | 3.91 | 7.40B | 305.06M | 305.06M | 5.97M | 9.67M | 23.13K | 3.17B | 17.53M |
| i2c.v | Verilator C++ | 646.14M | 403.64M | 1.60 | 388.70M | 28.21K | 28.21K | 912.00 | 48.26K | 556.00 | 70.43M | 818.53K |
| systemcdes.v | rx-prop | 24.06B | 9.20B | 2.62 | 9.86B | 914.13M | 914.13M | 1.14M | 14.38M | 12.58M | 2.37B | 126.13M |
| systemcdes.v | rx-sweep (Linear) | 15.61B | 7.39B | 2.11 | 6.43B | 590.70M | 590.70M | 2.14M | 17.11M | 13.09M | 2.82B | 137.96M |
| systemcdes.v | rx-oop (OOP Engine) | 28.10B | 23.34B | 1.20 | 21.77B | 1.49B | 1.49B | 16.89M | 40.41M | 11.20M | 3.46B | 296.29M |
| systemcdes.v | Icarus Verilog | 154.77B | 55.98B | 2.76 | 82.46B | 2.91B | 2.91B | 600.38M | 816.50M | 256.42K | 30.41B | 400.81M |
| systemcdes.v | Verilator C++ | 1.60B | 864.79M | 1.84 | 809.87M | 249.78K | 249.78K | 6.68K | 133.42K | 7.05K | 123.95M | 6.40M |
| spi.v | rx-prop | 6.98B | 1.93B | 3.62 | 2.76B | 300.42M | 300.42M | 285.86K | 4.79M | 4.37M | 663.57M | 3.53M |
| spi.v | rx-sweep (Linear) | 9.38B | 2.50B | 3.75 | 2.86B | 429.10M | 429.10M | 320.36K | 5.14M | 4.97M | 2.01B | 14.41M |
| spi.v | rx-oop (OOP Engine) | 7.90B | 3.28B | 2.41 | 4.50B | 530.26M | 530.26M | 1.80M | 7.63M | 3.67M | 970.38M | 8.58M |
| spi.v | Icarus Verilog | 34.51B | 9.00B | 3.84 | 15.58B | 615.00M | 615.00M | 107.00M | 183.75M | 123.40K | 6.75B | 31.67M |
| spi.v | Verilator C++ | 1.47B | 793.12M | 1.86 | 729.97M | 163.22K | 163.22K | 4.53K | 31.62K | 55.00 | 115.96M | 610.35K |
| wb_dma.v | rx-prop | 18.33B | 5.26B | 3.49 | 7.28B | 833.60M | 833.60M | 5.17M | 30.35M | 20.73M | 1.89B | 14.03M |
| wb_dma.v | rx-sweep (Linear) | 21.18B | 5.89B | 3.59 | 7.19B | 915.64M | 915.64M | 3.06M | 27.82M | 20.97M | 4.36B | 48.12M |
| wb_dma.v | rx-oop (OOP Engine) | 20.82B | 9.15B | 2.28 | 12.02B | 1.35B | 1.35B | 59.65M | 144.42M | 18.40M | 2.66B | 26.38M |
| wb_dma.v | Icarus Verilog | 88.00B | 21.65B | 4.06 | 38.55B | 585.78M | 585.78M | 115.21M | 198.67M | 292.03K | 16.99B | 76.21M |
| wb_dma.v | Verilator C++ | 2.75B | 1.39B | 1.98 | 1.45B | 184.09K | 184.09K | 3.78K | 68.67K | 18.85K | 307.56M | 4.55M |
| des_area.v | rx-prop | 23.97B | 9.53B | 2.51 | 9.95B | 839.71M | 839.71M | 1.60M | 26.04M | 23.88M | 2.49B | 145.22M |
| des_area.v | rx-sweep (Linear) | 16.20B | 8.48B | 1.91 | 6.89B | 569.23M | 569.23M | 2.42M | 28.37M | 23.47M | 3.07B | 170.71M |
| des_area.v | rx-oop (OOP Engine) | 27.87B | 22.74B | 1.23 | 21.53B | 1.40B | 1.40B | 17.87M | 47.71M | 20.01M | 3.54B | 295.38M |
| des_area.v | Icarus Verilog | 582.89B | 185.16B | 3.15 | 228.94B | 5.66B | 5.66B | 1.05B | 1.32B | 386.39K | 137.19B | 839.29M |
| des_area.v | Verilator C++ | 2.47B | 1.07B | 2.30 | 1.23B | 187.03K | 187.03K | 2.11K | 55.95K | 8.47K | 78.63M | 6.37M |
| tv80.v | rx-prop | 9.96B | 2.83B | 3.52 | 3.90B | 484.45M | 484.45M | 1.02M | 3.08M | 998.80K | 924.26M | 5.26M |
| tv80.v | rx-sweep (Linear) | 15.62B | 4.32B | 3.61 | 4.50B | 725.88M | 725.88M | 8.02M | 19.52M | 451.81K | 3.42B | 27.06M |
| tv80.v | rx-oop (OOP Engine) | 11.52B | 5.19B | 2.22 | 6.79B | 769.08M | 769.08M | 14.48M | 24.70M | 208.39K | 1.39B | 17.58M |
| tv80.v | Icarus Verilog | 13.91B | 4.35B | 3.20 | 6.38B | 237.17M | 237.17M | 26.97M | 41.06M | 246.59K | 2.84B | 25.65M |
| tv80.v | Verilator C++ | 3.19B | 1.47B | 2.17 | 1.75B | 16.59K | 16.59K | 3.35K | 6.70K | 25.00 | 280.01M | 1.55M |
| systemcaes.v | rx-prop | 27.81B | 8.27B | 3.36 | 11.04B | 1.09B | 1.09B | 49.94M | 122.79M | 26.51M | 2.75B | 31.61M |
| systemcaes.v | rx-sweep (Linear) | 32.83B | 10.39B | 3.16 | 10.84B | 1.41B | 1.41B | 103.91M | 406.84M | 25.47M | 6.85B | 92.18M |
| systemcaes.v | rx-oop (OOP Engine) | 31.65B | 17.62B | 1.80 | 19.86B | 1.85B | 1.85B | 315.85M | 689.21M | 22.15M | 3.96B | 86.22M |
| systemcaes.v | Icarus Verilog | 308.64B | 75.27B | 4.10 | 137.82B | 4.33B | 4.33B | 1.19B | 1.95B | 1.03M | 56.55B | 179.78M |
| systemcaes.v | Verilator C++ | 6.28B | 2.68B | 2.35 | 2.72B | 239.62K | 239.62K | 37.53K | 242.68K | 160.38K | 474.53M | 1.24M |
| mem_ctrl.v | rx-prop | 28.04B | 8.02B | 3.50 | 11.01B | 1.20B | 1.20B | 43.49M | 97.24M | 10.52M | 2.64B | 17.26M |
| mem_ctrl.v | rx-sweep (Linear) | 36.53B | 10.48B | 3.49 | 11.50B | 1.61B | 1.61B | 103.12M | 485.66M | 11.14M | 7.75B | 75.65M |
| mem_ctrl.v | rx-oop (OOP Engine) | 32.03B | 16.36B | 1.96 | 19.05B | 2.15B | 2.15B | 452.49M | 994.22M | 9.49M | 3.90B | 40.12M |
| mem_ctrl.v | Icarus Verilog | 101.34B | 27.70B | 3.66 | 45.59B | 1.18B | 1.18B | 550.21M | 886.24M | 1.10M | 19.70B | 76.27M |
| mem_ctrl.v | Verilator C++ | 7.26B | 3.42B | 2.12 | 3.70B | 218.52K | 218.52K | 145.27K | 285.10K | 110.07K | 615.10M | 7.15M |
| ac97_ctrl.v | rx-prop | 48.57B | 14.65B | 3.31 | 19.04B | 2.16B | 2.16B | 238.36M | 849.17M | 7.59M | 4.48B | 8.43M |
| ac97_ctrl.v | rx-sweep (Linear) | 63.61B | 16.50B | 3.85 | 19.68B | 2.75B | 2.75B | 276.13M | 1.73B | 7.81M | 13.38B | 81.34M |
| ac97_ctrl.v | rx-oop (OOP Engine) | 55.60B | 27.73B | 2.00 | 31.95B | 3.83B | 3.83B | 1.34B | 3.48B | 6.63M | 6.67B | 21.30M |
| ac97_ctrl.v | Icarus Verilog | 67.21B | 19.32B | 3.48 | 27.76B | 993.13M | 993.13M | 527.59M | 922.66M | 1.06M | 13.99B | 40.49M |
| ac97_ctrl.v | Verilator C++ | 9.87B | 4.38B | 2.26 | 4.72B | 2.67M | 2.67M | 10.75M | 11.05M | 52.44K | 1.07B | 4.36M |
| usb_funct.v | rx-prop | 17.75B | 5.78B | 3.07 | 7.02B | 784.55M | 784.55M | 90.18M | 246.65M | 11.99M | 1.72B | 10.03M |
| usb_funct.v | rx-sweep (Linear) | 33.08B | 10.47B | 3.16 | 9.04B | 1.57B | 1.57B | 155.03M | 676.71M | 12.61M | 7.73B | 72.15M |
| usb_funct.v | rx-oop (OOP Engine) | 20.09B | 10.51B | 1.91 | 11.59B | 1.36B | 1.36B | 431.45M | 924.60M | 10.56M | 2.48B | 21.33M |
| usb_funct.v | Icarus Verilog | 116.22B | 31.04B | 3.74 | 50.71B | 1.70B | 1.70B | 526.30M | 865.03M | 1.02M | 22.63B | 75.68M |
| usb_funct.v | Verilator C++ | 9.85B | 4.61B | 2.14 | 4.78B | 143.28K | 143.28K | 113.10K | 395.63K | 282.48K | 1.06B | 7.69M |
| aes_core.v | rx-prop | 67.61B | 30.52B | 2.21 | 27.49B | 3.32B | 3.32B | 585.34M | 1.03B | 26.12M | 6.67B | 332.12M |
| aes_core.v | rx-sweep (Linear) | 71.54B | 37.44B | 1.91 | 29.39B | 3.20B | 3.20B | 540.76M | 1.69B | 25.19M | 11.78B | 604.99M |
| aes_core.v | rx-oop (OOP Engine) | 78.84B | 79.37B | 0.99 | 68.59B | 4.86B | 4.86B | 1.29B | 2.06B | 22.40M | 9.66B | 903.90M |
| aes_core.v | Icarus Verilog | 277.55B | 102.79B | 2.70 | 148.54B | 3.85B | 3.85B | 2.03B | 2.61B | 2.41M | 52.84B | 601.37M |
| aes_core.v | Verilator C++ | 5.39B | 3.30B | 1.63 | 3.05B | 174.73K | 174.73K | 10.25K | 156.19K | 130.83K | 392.16M | 27.29M |
| wb_conmax.v | rx-prop | 43.18B | 15.59B | 2.77 | 17.64B | 1.75B | 1.75B | 436.15M | 1.06B | 115.68M | 4.88B | 39.88M |
| wb_conmax.v | rx-sweep (Linear) | 63.73B | 23.45B | 2.72 | 20.25B | 2.98B | 2.98B | 443.74M | 2.18B | 112.10M | 14.47B | 209.67M |
| wb_conmax.v | rx-oop (OOP Engine) | 47.27B | 27.53B | 1.72 | 28.63B | 2.87B | 2.87B | 1.01B | 2.16B | 98.53M | 6.53B | 89.60M |
| wb_conmax.v | Icarus Verilog | 1448.40B | 372.60B | 3.89 | 646.06B | 39.93B | 39.93B | 6.32B | 9.02B | 16.64M | 274.07B | 592.30M |
| wb_conmax.v | Verilator C++ | 13.37B | 5.81B | 2.30 | 6.20B | 3.70M | 3.70M | 84.87M | 86.14M | 266.75K | 732.95M | 2.23M |
| des_perf.v | rx-prop | 629.85B | 360.49B | 1.75 | 253.12B | 32.96B | 32.96B | 18.17B | 36.91B | 28.94M | 59.08B | 2.92B |
| des_perf.v | rx-sweep (Linear) | 608.03B | 367.48B | 1.65 | 273.03B | 25.84B | 25.84B | 8.93B | 25.51B | 31.12M | 101.97B | 5.89B |
| des_perf.v | rx-oop (OOP Engine) | 725.72B | 822.92B | 0.88 | 603.09B | 45.86B | 45.86B | 31.31B | 52.97B | 696.88M | 86.93B | 6.75B |
| des_perf.v | Icarus Verilog | 59.56B | 49.60B | 1.20 | 33.64B | 1.36B | 1.36B | 868.49M | 1.15B | 240.58M | 12.29B | 181.03M |
| des_perf.v | Verilator C++ | 50.90B | 111.43B | 0.46 | 36.70B | 130.00M | 130.00M | 3.54B | 3.58B | 200.82K | 4.90B | 2.05B |
| vga_lcd.v | rx-prop | 412.87B | 129.96B | 3.18 | 160.27B | 20.08B | 20.08B | 3.03B | 22.92B | 15.13M | 37.41B | 31.58M |
| vga_lcd.v | rx-sweep (Linear) | 539.86B | 145.05B | 3.72 | 166.19B | 23.88B | 23.88B | 3.78B | 28.42B | 120.11M | 113.76B | 877.71M |
| vga_lcd.v | rx-oop (OOP Engine) | 473.06B | 243.88B | 1.94 | 265.80B | 30.84B | 30.84B | 10.65B | 36.73B | 483.85M | 56.25B | 90.23M |
| vga_lcd.v | Icarus Verilog | 38.67B | 18.43B | 2.10 | 15.69B | 825.28M | 825.28M | 185.87M | 268.74M | 29.08M | 8.34B | 88.06M |
| vga_lcd.v | Verilator C++ | 71.53B | 182.90B | 0.39 | 56.75B | 331.54M | 331.54M | 5.65B | 5.74B | 239.34K | 7.61B | 3.82B |
