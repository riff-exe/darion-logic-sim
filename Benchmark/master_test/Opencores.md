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
| pci_conf_cyc_addr_dec.v | 184 | 0.62 MB (28.2 MB peak) | N/A | 0.63 MB (8.5 MB peak) | 0.81 MB (4.4 MB peak) |
| steppermotordrive.v | 258 | 1.11 MB (28.7 MB peak) | N/A | 1.10 MB (9.0 MB peak) | 0.71 MB (4.4 MB peak) |
| ss_pcm.v | 648 | 2.41 MB (30.0 MB peak) | N/A | 2.16 MB (10.0 MB peak) | 0.73 MB (4.4 MB peak) |
| usb_phy.v | 715 | 2.62 MB (30.2 MB peak) | N/A | 2.61 MB (10.4 MB peak) | 0.73 MB (4.4 MB peak) |
| sasc.v | 1,125 | 3.18 MB (30.7 MB peak) | N/A | 2.71 MB (10.6 MB peak) | 0.76 MB (4.5 MB peak) |
| simple_spi.v | 1,489 | 3.73 MB (31.3 MB peak) | N/A | 4.04 MB (11.9 MB peak) | 0.79 MB (4.5 MB peak) |
| pci_spoci_ctrl.v | 1,696 | 2.89 MB (30.5 MB peak) | N/A | 5.06 MB (12.9 MB peak) | 0.76 MB (4.5 MB peak) |
| i2c.v | 1,496 | 3.68 MB (31.2 MB peak) | N/A | 5.41 MB (13.2 MB peak) | 0.76 MB (4.5 MB peak) |
| systemcdes.v | 4,326 | 7.04 MB (34.6 MB peak) | N/A | 13.72 MB (21.6 MB peak) | 0.82 MB (4.5 MB peak) |
| spi.v | 4,531 | 8.00 MB (35.5 MB peak) | N/A | 15.05 MB (22.9 MB peak) | 0.83 MB (4.5 MB peak) |
| wb_dma.v | 5,720 | 14.72 MB (42.2 MB peak) | N/A | 16.09 MB (23.9 MB peak) | 0.89 MB (4.6 MB peak) |
| des_area.v | 6,445 | 10.09 MB (37.7 MB peak) | N/A | 18.86 MB (26.7 MB peak) | 0.96 MB (4.7 MB peak) |
| tv80.v | 10,607 | 18.74 MB (46.3 MB peak) | N/A | 31.17 MB (39.0 MB peak) | N/A |
| systemcaes.v | 14,071 | 24.64 MB (53.0 MB peak) | N/A | 40.84 MB (48.8 MB peak) | 1.11 MB (4.8 MB peak) |
| mem_ctrl.v | 16,796 | 34.32 MB (63.2 MB peak) | N/A | 54.04 MB (61.9 MB peak) | 1.30 MB (5.0 MB peak) |
| ac97_ctrl.v | 19,069 | 48.32 MB (75.8 MB peak) | N/A | 65.53 MB (73.4 MB peak) | 1.58 MB (5.3 MB peak) |
| usb_funct.v | 18,282 | 41.18 MB (68.7 MB peak) | N/A | 59.28 MB (67.2 MB peak) | 1.29 MB (5.0 MB peak) |
| aes_core.v | 25,565 | 32.27 MB (62.7 MB peak) | N/A | 78.82 MB (86.7 MB peak) | 1.17 MB (4.9 MB peak) |
| wb_conmax.v | 49,326 | 47.46 MB (80.8 MB peak) | N/A | 144.14 MB (152.0 MB peak) | 1.34 MB (5.0 MB peak) |
| des_perf.v | 111,781 | 201.67 MB (240.2 MB peak) | N/A | 440.61 MB (448.4 MB peak) | 2.80 MB (6.4 MB peak) |
| vga_lcd.v | 187,445 | 370.94 MB (414.3 MB peak) | N/A | 592.70 MB (600.6 MB peak) | 3.16 MB (6.9 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | 184 | 7.80 ms (0.015 ms opt) | N/A | 5.12 ms | 2.52 s |
| steppermotordrive.v | 258 | 0.66 ms (0.056 ms opt) | N/A | 7.28 ms | 2.52 s |
| ss_pcm.v | 648 | 1.55 ms (0.129 ms opt) | N/A | 11.20 ms | 2.57 s |
| usb_phy.v | 715 | 1.68 ms (0.168 ms opt) | N/A | 14.12 ms | 2.60 s |
| sasc.v | 1,125 | 2.05 ms (0.193 ms opt) | N/A | 13.15 ms | 2.66 s |
| simple_spi.v | 1,489 | 2.73 ms (0.270 ms opt) | N/A | 19.18 ms | 2.76 s |
| pci_spoci_ctrl.v | 1,696 | 2.19 ms (0.223 ms opt) | N/A | 23.49 ms | 2.68 s |
| i2c.v | 1,496 | 2.47 ms (0.278 ms opt) | N/A | 24.36 ms | 2.86 s |
| systemcdes.v | 4,326 | 5.56 ms (0.594 ms opt) | N/A | 60.18 ms | 3.44 s |
| spi.v | 4,531 | 13.16 ms (0.586 ms opt) | N/A | 66.45 ms | 3.77 s |
| wb_dma.v | 5,720 | 9.88 ms (0.971 ms opt) | N/A | 68.77 ms | 5.01 s |
| des_area.v | 6,445 | 13.47 ms (0.694 ms opt) | N/A | 86.83 ms | 4.35 s |
| tv80.v | 10,607 | 19.14 ms (1.361 ms opt) | N/A | 141.64 ms | N/A |
| systemcaes.v | 14,071 | 16.73 ms (1.947 ms opt) | N/A | 197.44 ms | 9.54 s |
| mem_ctrl.v | 16,796 | 30.52 ms (3.127 ms opt) | N/A | 261.09 ms | 15.23 s |
| ac97_ctrl.v | 19,069 | 43.56 ms (6.429 ms opt) | N/A | 300.46 ms | 12.07 s |
| usb_funct.v | 18,282 | 40.00 ms (5.388 ms opt) | N/A | 292.39 ms | 11.10 s |
| aes_core.v | 25,565 | 31.87 ms (4.141 ms opt) | N/A | 419.07 ms | 9.10 s |
| wb_conmax.v | 49,326 | 57.00 ms (11.610 ms opt) | N/A | 818.23 ms | 17.83 s |
| des_perf.v | 111,781 | 318.05 ms (57.419 ms opt) | N/A | 2.32 s | 73.77 s |
| vga_lcd.v | 187,445 | 627.22 ms (100.690 ms opt) | N/A | 3.18 s | 147.81 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | 23.60 ms | 29.93 ms | 38.23 ms | N/A | 888.86 ms | 1.72 ms |
| steppermotordrive.v | 57.16 ms | 57.99 ms | 95.10 ms | N/A | 99.20 ms | 12.45 ms |
| ss_pcm.v | 252.64 ms | 263.55 ms | 404.39 ms | N/A | 575.34 ms | 45.40 ms |
| usb_phy.v | 268.46 ms | 254.43 ms | 433.34 ms | N/A | 414.82 ms | 49.07 ms |
| sasc.v | 341.50 ms | 316.79 ms | 555.29 ms | N/A | 511.74 ms | 61.26 ms |
| simple_spi.v | 322.22 ms | 292.12 ms | 466.35 ms | N/A | 599.01 ms | 93.58 ms |
| pci_spoci_ctrl.v | 231.92 ms | 211.24 ms | 475.11 ms | N/A | 820.17 ms | 64.41 ms |
| i2c.v | 382.24 ms | 336.32 ms | 635.35 ms | N/A | 1123.86 ms | 116.97 ms |
| systemcdes.v | 2793.55 ms | 2019.51 ms | 6446.89 ms | N/A | 15.45 s | 232.05 ms |
| spi.v | 606.06 ms | 621.49 ms | 895.06 ms | N/A | 2344.02 ms | 225.17 ms |
| wb_dma.v | 1578.36 ms | 1504.84 ms | 2495.38 ms | N/A | 5873.59 ms | 385.85 ms |
| des_area.v | 2819.66 ms | 2273.39 ms | 6344.42 ms | N/A | 50.16 s | 297.93 ms |
| tv80.v | 896.85 ms | 1075.33 ms | 1444.16 ms | N/A | 1006.66 ms | 408.65 ms |
| systemcaes.v | 2584.88 ms | 2681.16 ms | 4752.06 ms | N/A | 20.36 s | 739.54 ms |
| mem_ctrl.v | 2528.68 ms | 2729.91 ms | 4415.82 ms | N/A | 7448.39 ms | 942.92 ms |
| ac97_ctrl.v | 4858.49 ms | 4388.14 ms | 7793.74 ms | N/A | 4930.74 ms | 1200.72 ms |
| usb_funct.v | 1830.89 ms | 2532.07 ms | 2944.87 ms | N/A | 8005.97 ms | 1285.21 ms |
| aes_core.v | 9679.41 ms | 10.78 s | 22.26 s | N/A | 28.17 s | 924.96 ms |
| wb_conmax.v | 4397.52 ms | 5711.75 ms | 7061.60 ms | N/A | 102.55 s | 1702.25 ms |
| des_perf.v | 116.17 s | 107.71 s | 231.05 s | N/A | 560.08 s | 32.12 s |
| vga_lcd.v | 42.67 s | 39.55 s | 72.90 s | N/A | 59.34 s | 51.34 s |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | 37.66x | 29.70x | 23.25x | N/A | 1.00x | 517.31x |
| steppermotordrive.v | 1.74x | 1.71x | 1.04x | N/A | 1.00x | 7.97x |
| ss_pcm.v | 2.28x | 2.18x | 1.42x | N/A | 1.00x | 12.67x |
| usb_phy.v | 1.55x | 1.63x | 0.96x | N/A | 1.00x | 8.45x |
| sasc.v | 1.50x | 1.62x | 0.92x | N/A | 1.00x | 8.35x |
| simple_spi.v | 1.86x | 2.05x | 1.28x | N/A | 1.00x | 6.40x |
| pci_spoci_ctrl.v | 3.54x | 3.88x | 1.73x | N/A | 1.00x | 12.73x |
| i2c.v | 2.94x | 3.34x | 1.77x | N/A | 1.00x | 9.61x |
| systemcdes.v | 5.53x | 7.65x | 2.40x | N/A | 1.00x | 66.59x |
| spi.v | 3.87x | 3.77x | 2.62x | N/A | 1.00x | 10.41x |
| wb_dma.v | 3.72x | 3.90x | 2.35x | N/A | 1.00x | 15.22x |
| des_area.v | 17.79x | 22.06x | 7.91x | N/A | 1.00x | 168.34x |
| tv80.v | 1.12x | 0.94x | 0.70x | N/A | 1.00x | 2.46x |
| systemcaes.v | 7.88x | 7.59x | 4.29x | N/A | 1.00x | 27.53x |
| mem_ctrl.v | 2.95x | 2.73x | 1.69x | N/A | 1.00x | 7.90x |
| ac97_ctrl.v | 1.01x | 1.12x | 0.63x | N/A | 1.00x | 4.11x |
| usb_funct.v | 4.37x | 3.16x | 2.72x | N/A | 1.00x | 6.23x |
| aes_core.v | 2.91x | 2.61x | 1.27x | N/A | 1.00x | 30.45x |
| wb_conmax.v | 23.32x | 17.95x | 14.52x | N/A | 1.00x | 60.25x |
| des_perf.v | 4.82x | 5.20x | 2.42x | N/A | 1.00x | 17.44x |
| vga_lcd.v | 1.39x | 1.50x | 0.81x | N/A | 1.00x | 1.16x |

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

- **rx-prop (Wavefront BFS):** `3.61x`
- **rx-sweep (Linear Compiled):** `3.60x`
- **rx-oop (OOP Graph):** `2.07x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `14.54x`

### Gate Evaluation Highlights

- **Reactor Sweep vs Propagate Total Evaluations Ratio:** `0.90x` (propagate performed more evaluations)

### Cross-Engine Comparisons

- **Reactor Sweep vs Propagate Ratio:** `1.00x` (propagate faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | Instructions | Cycles | IPC | L1 Loads | L1 Misses | L2 Loads | L2 Misses | L3 Loads | DRAM Loads | Branches | Branch Misses |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| pci_conf_cyc_addr_dec.v | rx-prop | 249.83M | 95.52M | 2.62 | 130.20M | 1.22M | 1.22M | 22.20K | 53.16K | 26.14K | 42.40M | 1.14M |
| pci_conf_cyc_addr_dec.v | rx-sweep (Linear) | 246.39M | 118.74M | 2.08 | 146.19M | 1.56M | 1.56M | 20.45K | 338.81K | 310.73K | 55.71M | 2.12M |
| pci_conf_cyc_addr_dec.v | rx-oop (OOP Engine) | 236.49M | 144.47M | 1.64 | 198.75M | 1.97M | 1.97M | 43.76K | 509.79K | 389.47K | 40.65M | 1.73M |
| pci_conf_cyc_addr_dec.v | Icarus Verilog | 12.75B | 3.27B | 3.89 | 4.91B | 27.49M | 27.49M | 15.96K | 54.76K | 10.24K | 2.73B | 14.23M |
| pci_conf_cyc_addr_dec.v | Verilator C++ | 9.95M | 3.06M | 3.25 | 4.28M | 21.28K | 21.28K | 0.00 | 0.00 | 0.00 | 2.61M | 326.00 |
| steppermotordrive.v | rx-prop | 732.77M | 200.84M | 3.65 | 298.83M | 215.29K | 215.29K | 5.82K | 33.73K | 10.46K | 73.13M | 330.00K |
| steppermotordrive.v | rx-sweep (Linear) | 954.22M | 208.26M | 4.58 | 319.81M | 1.69M | 1.69M | 4.23K | 39.31K | 24.17K | 186.88M | 1.02M |
| steppermotordrive.v | rx-oop (OOP Engine) | 809.10M | 331.34M | 2.44 | 481.05M | 5.21M | 5.21M | 13.83K | 80.41K | 15.09K | 101.57M | 744.30K |
| steppermotordrive.v | Icarus Verilog | 1.54B | 401.05M | 3.84 | 650.17M | 873.44K | 873.44K | 16.87K | 48.80K | 1.54K | 320.41M | 2.25M |
| steppermotordrive.v | Verilator C++ | 87.25M | 37.42M | 2.33 | 50.72M | 35.63K | 35.63K | 435.00 | 22.03K | 0.00 | 17.85M | 248.10K |
| ss_pcm.v | rx-prop | 2.88B | 926.59M | 3.11 | 1.11B | 91.35M | 91.35M | 78.49K | 1.25M | 1.22M | 272.14M | 3.33M |
| ss_pcm.v | rx-sweep (Linear) | 3.36B | 982.66M | 3.42 | 1.15B | 126.72M | 126.72M | 90.32K | 1.66M | 1.62M | 648.31M | 9.19M |
| ss_pcm.v | rx-oop (OOP Engine) | 3.12B | 1.46B | 2.13 | 1.83B | 158.77M | 158.77M | 81.82K | 1.31M | 1.12M | 383.26M | 6.27M |
| ss_pcm.v | Icarus Verilog | 8.07B | 2.19B | 3.69 | 3.67B | 72.22M | 72.22M | 58.50K | 211.56K | 21.89K | 1.58B | 13.05M |
| ss_pcm.v | Verilator C++ | 325.51M | 160.25M | 2.03 | 186.92M | 32.39K | 32.39K | 1.06K | 9.61K | 5.08K | 44.54M | 834.88K |
| usb_phy.v | rx-prop | 2.95B | 967.00M | 3.05 | 1.17B | 99.60M | 99.60M | 55.75K | 117.67K | 90.21K | 291.77M | 3.49M |
| usb_phy.v | rx-sweep (Linear) | 3.55B | 948.82M | 3.74 | 1.18B | 131.12M | 131.12M | 79.88K | 1.74M | 1.74M | 684.31M | 6.40M |
| usb_phy.v | rx-oop (OOP Engine) | 3.28B | 1.58B | 2.08 | 1.91B | 185.25M | 185.25M | 63.64K | 897.81K | 740.97K | 401.70M | 6.77M |
| usb_phy.v | Icarus Verilog | 5.67B | 1.60B | 3.54 | 2.56B | 49.05M | 49.05M | 79.12K | 166.55K | 22.02K | 1.11B | 10.78M |
| usb_phy.v | Verilator C++ | 334.90M | 167.25M | 2.00 | 209.01M | 8.50K | 8.50K | 261.00 | 8.68K | 326.00 | 49.54M | 927.01K |
| sasc.v | rx-prop | 3.87B | 1.25B | 3.11 | 1.49B | 138.36M | 138.36M | 57.45K | 1.02M | 978.66K | 361.02M | 3.92M |
| sasc.v | rx-sweep (Linear) | 4.39B | 1.17B | 3.76 | 1.43B | 177.29M | 177.29M | 60.79K | 1.68M | 1.65M | 860.53M | 9.63M |
| sasc.v | rx-oop (OOP Engine) | 4.34B | 2.01B | 2.16 | 2.57B | 256.48M | 256.48M | 82.03K | 1.51M | 1.25M | 530.08M | 8.79M |
| sasc.v | Icarus Verilog | 7.13B | 1.96B | 3.63 | 3.24B | 70.81M | 70.81M | 113.30K | 260.78K | 20.82K | 1.41B | 11.89M |
| sasc.v | Verilator C++ | 549.46M | 220.57M | 2.49 | 298.96M | 10.73K | 10.73K | 539.00 | 105.79K | 95.00 | 56.28M | 916.69K |
| simple_spi.v | rx-prop | 3.76B | 1.18B | 3.17 | 1.44B | 147.78M | 147.78M | 67.78K | 1.12M | 1.06M | 348.16M | 1.70M |
| simple_spi.v | rx-sweep (Linear) | 4.63B | 1.08B | 4.29 | 1.41B | 191.32M | 191.32M | 76.79K | 1.54M | 1.52M | 945.40M | 5.08M |
| simple_spi.v | rx-oop (OOP Engine) | 4.12B | 1.70B | 2.43 | 2.31B | 278.45M | 278.45M | 97.17K | 2.01M | 1.70M | 503.35M | 3.50M |
| simple_spi.v | Icarus Verilog | 8.84B | 2.32B | 3.80 | 3.94B | 107.88M | 107.88M | 248.48K | 621.70K | 26.54K | 1.75B | 12.24M |
| simple_spi.v | Verilator C++ | 629.64M | 330.03M | 1.91 | 335.52M | 105.94K | 105.94K | 1.53K | 68.25K | 2.04K | 67.12M | 547.24K |
| pci_spoci_ctrl.v | rx-prop | 2.92B | 861.72M | 3.39 | 1.12B | 57.04M | 57.04M | 78.05K | 2.12M | 2.06M | 283.18M | 1.95M |
| pci_spoci_ctrl.v | rx-sweep (Linear) | 3.19B | 793.49M | 4.02 | 984.44M | 107.92M | 107.92M | 103.42K | 2.15M | 2.12M | 657.69M | 4.44M |
| pci_spoci_ctrl.v | rx-oop (OOP Engine) | 3.13B | 1.73B | 1.81 | 2.12B | 132.97M | 132.97M | 77.49K | 2.01M | 1.73M | 389.14M | 13.77M |
| pci_spoci_ctrl.v | Icarus Verilog | 11.10B | 3.15B | 3.53 | 5.16B | 148.19M | 148.19M | 1.66M | 2.88M | 51.37K | 2.16B | 18.84M |
| pci_spoci_ctrl.v | Verilator C++ | 498.88M | 229.76M | 2.17 | 249.36M | 32.33K | 32.33K | 520.00 | 10.81K | 283.00 | 45.78M | 245.53K |
| i2c.v | rx-prop | 4.47B | 1.38B | 3.23 | 1.72B | 146.98M | 146.98M | 78.37K | 1.61M | 1.54M | 407.74M | 2.39M |
| i2c.v | rx-sweep (Linear) | 5.18B | 1.24B | 4.17 | 1.63B | 199.87M | 199.87M | 86.77K | 1.97M | 1.94M | 1.03B | 6.29M |
| i2c.v | rx-oop (OOP Engine) | 4.90B | 2.29B | 2.14 | 2.95B | 297.76M | 297.76M | 212.18K | 1.35M | 931.59K | 592.18M | 10.10M |
| i2c.v | Icarus Verilog | 16.25B | 4.24B | 3.83 | 7.41B | 303.16M | 303.16M | 5.12M | 8.75M | 59.96K | 3.17B | 19.39M |
| i2c.v | Verilator C++ | 669.27M | 426.29M | 1.57 | 398.60M | 33.74K | 33.74K | 699.00 | 10.89K | 312.00 | 73.85M | 709.87K |
| systemcdes.v | rx-prop | 25.23B | 10.24B | 2.46 | 9.83B | 907.68M | 907.68M | 1.20M | 14.79M | 12.93M | 2.42B | 123.32M |
| systemcdes.v | rx-sweep (Linear) | 16.33B | 7.46B | 2.19 | 6.46B | 593.80M | 593.80M | 824.17K | 14.43M | 13.06M | 2.87B | 135.36M |
| systemcdes.v | rx-oop (OOP Engine) | 28.09B | 23.32B | 1.20 | 21.73B | 1.49B | 1.49B | 26.58M | 56.27M | 10.98M | 3.46B | 296.12M |
| systemcdes.v | Icarus Verilog | 154.64B | 56.26B | 2.75 | 83.40B | 2.91B | 2.91B | 601.87M | 827.54M | 434.95K | 30.42B | 404.08M |
| systemcdes.v | Verilator C++ | 1.60B | 827.77M | 1.94 | 793.04M | 29.07K | 29.07K | 2.80K | 90.64K | 73.80K | 120.88M | 6.33M |
| spi.v | rx-prop | 7.32B | 2.24B | 3.27 | 2.79B | 301.77M | 301.77M | 308.67K | 4.80M | 4.29M | 683.27M | 3.45M |
| spi.v | rx-sweep (Linear) | 9.73B | 2.31B | 4.21 | 2.90B | 429.91M | 429.91M | 284.06K | 4.65M | 4.43M | 2.04B | 13.87M |
| spi.v | rx-oop (OOP Engine) | 7.88B | 3.26B | 2.42 | 4.50B | 520.53M | 520.53M | 975.79K | 5.94M | 3.88M | 967.48M | 8.58M |
| spi.v | Icarus Verilog | 34.41B | 8.90B | 3.87 | 15.60B | 613.65M | 613.65M | 103.71M | 181.39M | 218.89K | 6.75B | 30.73M |
| spi.v | Verilator C++ | 1.49B | 813.41M | 1.83 | 718.46M | 127.54K | 127.54K | 1.88K | 37.22K | 1.13K | 114.90M | 567.67K |
| wb_dma.v | rx-prop | 19.32B | 5.99B | 3.23 | 7.46B | 832.16M | 832.16M | 5.76M | 32.13M | 21.50M | 1.98B | 13.78M |
| wb_dma.v | rx-sweep (Linear) | 22.14B | 5.72B | 3.87 | 7.35B | 915.63M | 915.63M | 4.06M | 29.27M | 21.63M | 4.46B | 45.70M |
| wb_dma.v | rx-oop (OOP Engine) | 20.85B | 9.23B | 2.26 | 12.06B | 1.36B | 1.36B | 72.58M | 161.75M | 19.04M | 2.66B | 26.02M |
| wb_dma.v | Icarus Verilog | 87.99B | 22.13B | 3.98 | 38.86B | 583.80M | 583.80M | 111.41M | 197.19M | 397.65K | 16.98B | 73.61M |
| wb_dma.v | Verilator C++ | 2.73B | 1.39B | 1.96 | 1.46B | 231.75K | 231.75K | 2.54K | 67.01K | 60.81K | 311.02M | 4.62M |
| des_area.v | rx-prop | 25.16B | 10.47B | 2.40 | 10.00B | 823.13M | 823.13M | 2.92M | 28.70M | 24.28M | 2.58B | 144.78M |
| des_area.v | rx-sweep (Linear) | 17.03B | 8.52B | 2.00 | 7.01B | 566.42M | 566.42M | 3.39M | 30.34M | 23.48M | 3.16B | 169.78M |
| des_area.v | rx-oop (OOP Engine) | 27.84B | 23.06B | 1.21 | 21.72B | 1.41B | 1.41B | 46.42M | 89.27M | 20.25M | 3.54B | 295.02M |
| des_area.v | Icarus Verilog | 582.87B | 181.79B | 3.21 | 222.89B | 5.66B | 5.66B | 1.05B | 1.33B | 951.01K | 137.21B | 793.11M |
| des_area.v | Verilator C++ | 2.49B | 1.07B | 2.33 | 1.24B | 74.39K | 74.39K | 1.83K | 85.01K | 81.69K | 78.06M | 6.40M |
| tv80.v | rx-prop | 10.39B | 3.24B | 3.21 | 3.91B | 481.74M | 481.74M | 1.74M | 4.11M | 718.96K | 925.66M | 5.17M |
| tv80.v | rx-sweep (Linear) | 16.01B | 3.86B | 4.15 | 4.49B | 718.17M | 718.17M | 5.08M | 10.61M | 390.58K | 3.42B | 24.57M |
| tv80.v | rx-oop (OOP Engine) | 11.51B | 5.19B | 2.22 | 6.78B | 786.07M | 786.07M | 14.33M | 25.79M | 853.86K | 1.38B | 17.76M |
| tv80.v | Icarus Verilog | 13.96B | 4.36B | 3.20 | 6.37B | 238.33M | 238.33M | 28.00M | 40.96M | 402.46K | 2.84B | 24.93M |
| tv80.v | Verilator C++ | 3.24B | 1.47B | 2.20 | 1.73B | 23.95K | 23.95K | 5.01K | 44.51K | 42.27K | 280.56M | 1.44M |
| systemcaes.v | rx-prop | 29.23B | 9.64B | 3.03 | 11.22B | 1.09B | 1.09B | 49.70M | 128.19M | 26.08M | 2.86B | 30.80M |
| systemcaes.v | rx-sweep (Linear) | 34.12B | 9.96B | 3.43 | 11.05B | 1.42B | 1.42B | 98.17M | 354.14M | 25.64M | 6.95B | 87.52M |
| systemcaes.v | rx-oop (OOP Engine) | 31.60B | 17.33B | 1.82 | 19.83B | 1.86B | 1.86B | 311.14M | 686.71M | 22.62M | 3.96B | 86.28M |
| systemcaes.v | Icarus Verilog | 308.64B | 74.90B | 4.12 | 137.86B | 4.26B | 4.26B | 1.17B | 1.95B | 2.58M | 56.54B | 175.08M |
| systemcaes.v | Verilator C++ | 6.27B | 2.66B | 2.36 | 2.73B | 212.61K | 212.61K | 106.20K | 121.41K | 20.84K | 479.28M | 1.32M |
| mem_ctrl.v | rx-prop | 29.44B | 9.24B | 3.19 | 11.07B | 1.20B | 1.20B | 37.83M | 98.94M | 10.86M | 2.70B | 16.36M |
| mem_ctrl.v | rx-sweep (Linear) | 37.74B | 9.92B | 3.81 | 11.61B | 1.62B | 1.62B | 119.07M | 489.86M | 10.96M | 7.79B | 71.89M |
| mem_ctrl.v | rx-oop (OOP Engine) | 32.04B | 15.96B | 2.01 | 18.90B | 2.14B | 2.14B | 425.52M | 982.94M | 9.12M | 3.90B | 40.35M |
| mem_ctrl.v | Icarus Verilog | 101.36B | 28.33B | 3.58 | 45.46B | 1.19B | 1.19B | 554.97M | 890.21M | 1.11M | 19.68B | 75.89M |
| mem_ctrl.v | Verilator C++ | 7.27B | 3.39B | 2.14 | 3.70B | 116.71K | 116.71K | 16.88K | 100.41K | 82.83K | 615.70M | 6.82M |
| ac97_ctrl.v | rx-prop | 50.89B | 17.53B | 2.90 | 19.08B | 2.22B | 2.22B | 259.39M | 902.58M | 7.89M | 4.51B | 8.34M |
| ac97_ctrl.v | rx-sweep (Linear) | 65.83B | 15.84B | 4.16 | 19.72B | 2.74B | 2.74B | 325.92M | 1.80B | 8.25M | 13.41B | 71.91M |
| ac97_ctrl.v | rx-oop (OOP Engine) | 55.64B | 28.04B | 1.98 | 32.08B | 3.83B | 3.83B | 1.32B | 3.42B | 6.90M | 6.67B | 20.58M |
| ac97_ctrl.v | Icarus Verilog | 67.35B | 19.46B | 3.46 | 27.74B | 1.01B | 1.01B | 501.76M | 955.61M | 1.51M | 14.00B | 39.61M |
| ac97_ctrl.v | Verilator C++ | 9.76B | 4.31B | 2.26 | 4.77B | 379.01K | 379.01K | 860.33K | 994.54K | 111.07K | 1.07B | 4.99M |
| usb_funct.v | rx-prop | 18.63B | 6.74B | 2.76 | 7.10B | 785.29M | 785.29M | 88.19M | 239.14M | 12.28M | 1.77B | 9.95M |
| usb_funct.v | rx-sweep (Linear) | 33.95B | 9.25B | 3.67 | 9.16B | 1.56B | 1.56B | 166.06M | 662.41M | 12.05M | 7.78B | 66.40M |
| usb_funct.v | rx-oop (OOP Engine) | 20.10B | 10.70B | 1.88 | 11.73B | 1.41B | 1.41B | 410.89M | 903.80M | 10.36M | 2.49B | 21.68M |
| usb_funct.v | Icarus Verilog | 116.24B | 30.54B | 3.81 | 50.75B | 1.70B | 1.70B | 505.60M | 855.19M | 1.48M | 22.63B | 74.35M |
| usb_funct.v | Verilator C++ | 9.81B | 4.60B | 2.13 | 4.80B | 364.03K | 364.03K | 831.54K | 861.22K | 28.65K | 1.05B | 6.91M |
| aes_core.v | rx-prop | 70.73B | 35.11B | 2.01 | 27.43B | 3.30B | 3.30B | 613.34M | 1.10B | 25.99M | 6.77B | 332.27M |
| aes_core.v | rx-sweep (Linear) | 74.31B | 38.99B | 1.91 | 29.31B | 3.19B | 3.19B | 539.04M | 1.57B | 25.23M | 11.88B | 602.57M |
| aes_core.v | rx-oop (OOP Engine) | 78.83B | 80.26B | 0.98 | 68.91B | 4.79B | 4.79B | 1.29B | 2.06B | 23.63M | 9.67B | 903.62M |
| aes_core.v | Icarus Verilog | 277.49B | 103.95B | 2.67 | 147.95B | 3.80B | 3.80B | 2.01B | 2.56B | 3.48M | 52.82B | 602.21M |
| aes_core.v | Verilator C++ | 5.39B | 3.32B | 1.62 | 3.04B | 70.08K | 70.08K | 8.67K | 60.36K | 51.80K | 392.96M | 27.45M |
| wb_conmax.v | rx-prop | 46.07B | 17.27B | 2.67 | 18.54B | 1.75B | 1.75B | 326.67M | 899.16M | 116.04M | 5.34B | 39.83M |
| wb_conmax.v | rx-sweep (Linear) | 66.57B | 22.00B | 3.03 | 21.24B | 2.98B | 2.98B | 458.15M | 2.13B | 112.48M | 14.92B | 201.65M |
| wb_conmax.v | rx-oop (OOP Engine) | 47.26B | 27.06B | 1.75 | 28.59B | 2.86B | 2.86B | 999.13M | 2.10B | 97.69M | 6.52B | 90.59M |
| wb_conmax.v | Icarus Verilog | 1448.12B | 375.96B | 3.85 | 647.84B | 39.86B | 39.86B | 6.29B | 9.06B | 44.75M | 274.04B | 585.06M |
| wb_conmax.v | Verilator C++ | 13.36B | 6.09B | 2.19 | 6.20B | 5.55M | 5.55M | 116.95M | 118.36M | 355.68K | 733.03M | 2.61M |
| des_perf.v | rx-prop | 657.63B | 417.42B | 1.58 | 251.12B | 32.79B | 32.79B | 18.20B | 36.95B | 42.47M | 59.18B | 2.93B |
| des_perf.v | rx-sweep (Linear) | 632.91B | 387.03B | 1.64 | 271.23B | 25.90B | 25.90B | 8.93B | 25.56B | 57.92M | 102.06B | 5.84B |
| des_perf.v | rx-oop (OOP Engine) | 725.45B | 830.46B | 0.87 | 604.85B | 46.52B | 46.52B | 31.53B | 53.67B | 743.56M | 86.94B | 6.76B |
| des_perf.v | Icarus Verilog | 59.49B | 50.33B | 1.18 | 33.80B | 1.36B | 1.36B | 864.54M | 1.15B | 247.14M | 12.31B | 182.01M |
| des_perf.v | Verilator C++ | 50.90B | 114.46B | 0.44 | 36.91B | 133.30M | 133.30M | 3.56B | 3.59B | 175.99K | 4.90B | 2.05B |
| vga_lcd.v | rx-prop | 431.88B | 153.28B | 2.82 | 160.23B | 20.20B | 20.20B | 3.17B | 23.02B | 19.33M | 37.44B | 31.37M |
| vga_lcd.v | rx-sweep (Linear) | 558.29B | 141.65B | 3.94 | 166.96B | 23.80B | 23.80B | 3.72B | 28.78B | 68.86M | 113.80B | 871.26M |
| vga_lcd.v | rx-oop (OOP Engine) | 473.02B | 261.43B | 1.81 | 278.39B | 32.30B | 32.30B | 11.86B | 37.57B | 523.86M | 56.26B | 126.23M |
| vga_lcd.v | Icarus Verilog | 38.66B | 18.46B | 2.09 | 15.74B | 842.37M | 842.37M | 181.58M | 267.58M | 29.57M | 8.34B | 88.52M |
| vga_lcd.v | Verilator C++ | 71.53B | 183.20B | 0.39 | 56.76B | 387.80M | 387.80M | 5.68B | 5.87B | 295.82K | 7.61B | 3.81B |
