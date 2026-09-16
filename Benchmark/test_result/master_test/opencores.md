# Master Test Unified Benchmark Report: tests/IWLS2005/opencores

**Execution Parameters:**
- **Target Suite / Path:** `tests/IWLS2005/opencores`
- **Circuits Benchmarked:** 21
- **Simulation Vectors (Phase 3):** 10,000 (Warmup: 10)
- **Verification Vectors (Phase 2):** 100
- **Hardware Profiler:** Linux `perf` kernel PMU counters

---

## 1. Zero-Testbench Memory Footprint (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | 184 | 0.47 MB (31.9 MB peak) | N/A | 0.60 MB (8.5 MB peak) | 0.71 MB (4.4 MB peak) |
| steppermotordrive.v | 258 | 1.02 MB (32.4 MB peak) | N/A | 1.10 MB (8.9 MB peak) | 0.71 MB (4.4 MB peak) |
| ss_pcm.v | 648 | 2.35 MB (33.7 MB peak) | N/A | 2.04 MB (9.9 MB peak) | 0.72 MB (4.4 MB peak) |
| usb_phy.v | 715 | 2.58 MB (33.9 MB peak) | N/A | 2.63 MB (10.4 MB peak) | 0.73 MB (4.4 MB peak) |
| sasc.v | 1,125 | 3.20 MB (34.6 MB peak) | N/A | 2.68 MB (10.5 MB peak) | 0.76 MB (4.4 MB peak) |
| simple_spi.v | 1,489 | 3.77 MB (35.1 MB peak) | N/A | 4.01 MB (11.8 MB peak) | 0.80 MB (4.5 MB peak) |
| pci_spoci_ctrl.v | 1,696 | 2.90 MB (34.3 MB peak) | N/A | 5.14 MB (13.0 MB peak) | 0.76 MB (4.4 MB peak) |
| i2c.v | 1,496 | 3.71 MB (35.1 MB peak) | N/A | 5.38 MB (13.1 MB peak) | 0.80 MB (4.5 MB peak) |
| systemcdes.v | 4,326 | 7.07 MB (38.3 MB peak) | N/A | 13.57 MB (21.4 MB peak) | 0.83 MB (4.5 MB peak) |
| spi.v | 4,531 | 8.86 MB (40.2 MB peak) | N/A | 15.00 MB (22.9 MB peak) | 0.82 MB (4.5 MB peak) |
| wb_dma.v | 5,720 | 15.74 MB (47.1 MB peak) | N/A | 16.05 MB (23.9 MB peak) | 0.90 MB (4.6 MB peak) |
| des_area.v | 6,445 | 9.13 MB (40.5 MB peak) | N/A | 18.88 MB (26.7 MB peak) | 0.95 MB (4.6 MB peak) |
| tv80.v | 10,607 | 19.45 MB (50.8 MB peak) | N/A | 31.07 MB (39.0 MB peak) | N/A |
| systemcaes.v | 14,071 | 25.62 MB (57.8 MB peak) | N/A | 41.01 MB (48.8 MB peak) | 1.02 MB (4.7 MB peak) |
| mem_ctrl.v | 16,796 | 33.45 MB (66.3 MB peak) | N/A | 54.10 MB (61.9 MB peak) | 1.30 MB (5.0 MB peak) |
| ac97_ctrl.v | 19,069 | 52.06 MB (84.9 MB peak) | N/A | 65.48 MB (73.4 MB peak) | 1.52 MB (5.2 MB peak) |
| usb_funct.v | 18,282 | 45.60 MB (78.3 MB peak) | N/A | 59.39 MB (67.2 MB peak) | 1.30 MB (5.0 MB peak) |
| aes_core.v | 25,565 | 33.20 MB (66.8 MB peak) | N/A | 78.84 MB (86.7 MB peak) | 1.11 MB (4.8 MB peak) |
| wb_conmax.v | 49,326 | 47.99 MB (83.6 MB peak) | N/A | 144.08 MB (151.9 MB peak) | 1.21 MB (4.9 MB peak) |
| des_perf.v | 111,781 | 206.46 MB (244.9 MB peak) | N/A | 440.56 MB (448.3 MB peak) | 2.83 MB (6.5 MB peak) |
| vga_lcd.v | 187,445 | 379.50 MB (420.0 MB peak) | N/A | 592.82 MB (600.6 MB peak) | 3.27 MB (7.0 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | 184 | 0.38 ms (0.015 ms opt) | N/A | 5.75 ms | 2.56 s |
| steppermotordrive.v | 258 | 8.43 ms (0.059 ms opt) | N/A | 6.84 ms | 2.60 s |
| ss_pcm.v | 648 | 9.22 ms (0.150 ms opt) | N/A | 11.34 ms | 2.64 s |
| usb_phy.v | 715 | 9.37 ms (0.177 ms opt) | N/A | 14.27 ms | 2.64 s |
| sasc.v | 1,125 | 10.05 ms (0.225 ms opt) | N/A | 13.59 ms | 2.79 s |
| simple_spi.v | 1,489 | 10.34 ms (0.248 ms opt) | N/A | 19.13 ms | 2.85 s |
| pci_spoci_ctrl.v | 1,696 | 2.26 ms (0.216 ms opt) | N/A | 25.03 ms | 2.74 s |
| i2c.v | 1,496 | 10.41 ms (0.301 ms opt) | N/A | 26.56 ms | 2.93 s |
| systemcdes.v | 4,326 | 5.92 ms (0.628 ms opt) | N/A | 64.97 ms | 3.63 s |
| spi.v | 4,531 | 13.57 ms (0.641 ms opt) | N/A | 67.84 ms | 3.95 s |
| wb_dma.v | 5,720 | 18.26 ms (1.090 ms opt) | N/A | 75.25 ms | 5.31 s |
| des_area.v | 6,445 | 14.04 ms (0.740 ms opt) | N/A | 90.26 ms | 4.39 s |
| tv80.v | 10,607 | 13.09 ms (1.475 ms opt) | N/A | 153.73 ms | N/A |
| systemcaes.v | 14,071 | 25.78 ms (3.820 ms opt) | N/A | 208.97 ms | 9.95 s |
| mem_ctrl.v | 16,796 | 32.27 ms (3.655 ms opt) | N/A | 282.54 ms | 15.89 s |
| ac97_ctrl.v | 19,069 | 41.38 ms (9.382 ms opt) | N/A | 331.28 ms | 12.57 s |
| usb_funct.v | 18,282 | 41.63 ms (6.689 ms opt) | N/A | 307.93 ms | 11.47 s |
| aes_core.v | 25,565 | 36.10 ms (6.134 ms opt) | N/A | 448.09 ms | 9.49 s |
| wb_conmax.v | 49,326 | 60.12 ms (14.610 ms opt) | N/A | 868.99 ms | 18.59 s |
| des_perf.v | 111,781 | 329.87 ms (64.212 ms opt) | N/A | 2.38 s | 75.42 s |
| vga_lcd.v | 187,445 | 645.51 ms (136.182 ms opt) | N/A | 3.29 s | 152.99 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | 5.44 ms | 6.17 ms | 7.18 ms | N/A | 176.54 ms | 1.37 ms |
| steppermotordrive.v | 11.26 ms | 16.12 ms | 18.51 ms | N/A | 19.33 ms | 4.59 ms |
| ss_pcm.v | 60.29 ms | 71.61 ms | 78.99 ms | N/A | 113.80 ms | 10.05 ms |
| usb_phy.v | 64.03 ms | 73.53 ms | 84.91 ms | N/A | 83.27 ms | 10.82 ms |
| sasc.v | 78.23 ms | 91.05 ms | 107.38 ms | N/A | 103.10 ms | 13.83 ms |
| simple_spi.v | 72.03 ms | 91.91 ms | 89.65 ms | N/A | 121.06 ms | 19.44 ms |
| pci_spoci_ctrl.v | 51.66 ms | 61.73 ms | 96.09 ms | N/A | 163.53 ms | 12.96 ms |
| i2c.v | 88.61 ms | 103.16 ms | 122.74 ms | N/A | 225.69 ms | 24.37 ms |
| systemcdes.v | 798.91 ms | 504.85 ms | 1330.72 ms | N/A | 3128.30 ms | 51.65 ms |
| spi.v | 145.03 ms | 189.20 ms | 171.78 ms | N/A | 476.93 ms | 45.04 ms |
| wb_dma.v | 356.00 ms | 426.24 ms | 498.45 ms | N/A | 1154.56 ms | 83.59 ms |
| des_area.v | 860.84 ms | 522.65 ms | 1330.05 ms | N/A | 10.12 s | 68.87 ms |
| tv80.v | 210.11 ms | 336.82 ms | 289.27 ms | N/A | 205.92 ms | 85.71 ms |
| systemcaes.v | 671.86 ms | 753.10 ms | 988.58 ms | N/A | 4133.99 ms | 156.06 ms |
| mem_ctrl.v | 593.35 ms | 824.42 ms | 940.43 ms | N/A | 1488.53 ms | 198.69 ms |
| ac97_ctrl.v | 1165.70 ms | 1388.18 ms | 1494.23 ms | N/A | 994.95 ms | 279.14 ms |
| usb_funct.v | 472.73 ms | 788.18 ms | 605.06 ms | N/A | 1608.84 ms | 272.51 ms |
| aes_core.v | 3158.09 ms | 3164.03 ms | 4665.51 ms | N/A | 5705.56 ms | 199.26 ms |
| wb_conmax.v | 1121.74 ms | 1568.37 ms | 1440.96 ms | N/A | 20.72 s | 366.32 ms |
| des_perf.v | 33.81 s | 27.71 s | 61.45 s | N/A | 123.77 s | 6475.95 ms |
| vga_lcd.v | 12.30 s | 13.41 s | 15.15 s | N/A | 15.40 s | 10.30 s |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | 32.48x | 28.59x | 24.60x | N/A | 1.00x | 129.01x |
| steppermotordrive.v | 1.72x | 1.20x | 1.04x | N/A | 1.00x | 4.21x |
| ss_pcm.v | 1.89x | 1.59x | 1.44x | N/A | 1.00x | 11.33x |
| usb_phy.v | 1.30x | 1.13x | 0.98x | N/A | 1.00x | 7.70x |
| sasc.v | 1.32x | 1.13x | 0.96x | N/A | 1.00x | 7.46x |
| simple_spi.v | 1.68x | 1.32x | 1.35x | N/A | 1.00x | 6.23x |
| pci_spoci_ctrl.v | 3.17x | 2.65x | 1.70x | N/A | 1.00x | 12.62x |
| i2c.v | 2.55x | 2.19x | 1.84x | N/A | 1.00x | 9.26x |
| systemcdes.v | 3.92x | 6.20x | 2.35x | N/A | 1.00x | 60.56x |
| spi.v | 3.29x | 2.52x | 2.78x | N/A | 1.00x | 10.59x |
| wb_dma.v | 3.24x | 2.71x | 2.32x | N/A | 1.00x | 13.81x |
| des_area.v | 11.76x | 19.37x | 7.61x | N/A | 1.00x | 146.97x |
| tv80.v | 0.98x | 0.61x | 0.71x | N/A | 1.00x | 2.40x |
| systemcaes.v | 6.15x | 5.49x | 4.18x | N/A | 1.00x | 26.49x |
| mem_ctrl.v | 2.51x | 1.81x | 1.58x | N/A | 1.00x | 7.49x |
| ac97_ctrl.v | 0.85x | 0.72x | 0.67x | N/A | 1.00x | 3.56x |
| usb_funct.v | 3.40x | 2.04x | 2.66x | N/A | 1.00x | 5.90x |
| aes_core.v | 1.81x | 1.80x | 1.22x | N/A | 1.00x | 28.63x |
| wb_conmax.v | 18.47x | 13.21x | 14.38x | N/A | 1.00x | 56.57x |
| des_perf.v | 3.66x | 4.47x | 2.01x | N/A | 1.00x | 19.11x |
| vga_lcd.v | 1.25x | 1.15x | 1.02x | N/A | 1.00x | 1.49x |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `2.96x`
- **rx-sweep (Linear Compiled):** `2.59x`
- **rx-oop (OOP Graph):** `2.09x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `12.72x`

### Cross-Engine Comparisons

- **Reactor Sweep vs Propagate Ratio:** `0.87x` (propagate faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | IPC | Cycles | Instructions | L1 Loads | L1 Hit% | L2 Hit% | LLC Misses | Brn Miss% |
|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | rx-prop | 3.79 | 13.95M | 52.84M | 12.07M | 99.96% | 89.99% | 509 | 3.86% |
| pci_conf_cyc_addr_dec.v | rx-sweep (Linear) | 3.10 | 28.61M | 88.72M | 30.26M | 98.88% | 96.48% | 12.00K | 2.73% |
| pci_conf_cyc_addr_dec.v | rx-oop (OOP Engine) | 2.16 | 30.67M | 66.10M | 41.24M | 99.06% | 94.99% | 19.99K | 3.59% |
| pci_conf_cyc_addr_dec.v | Icarus Verilog | 3.96 | 731.73M | 2.90B | 1.10B | 99.43% | 99.55% | 27.63K | 0.52% |
| steppermotordrive.v | rx-prop | 4.74 | 31.77M | 150.72M | 56.99M | 99.84% | 96.79% | 2.86K | 0.32% |
| steppermotordrive.v | rx-sweep (Linear) | 5.54 | 51.00M | 282.45M | 73.85M | 99.57% | 99.01% | 3.18K | 0.57% |
| steppermotordrive.v | rx-oop (OOP Engine) | 2.80 | 63.69M | 178.49M | 104.76M | 99.40% | 98.48% | 10.21K | 0.81% |
| steppermotordrive.v | Icarus Verilog | 3.87 | 98.58M | 381.19M | 158.74M | 99.74% | 90.75% | 40.17K | 0.75% |
| ss_pcm.v | rx-prop | 3.33 | 230.65M | 767.75M | 246.79M | 89.39% | 99.94% | 16.11K | 1.08% |
| ss_pcm.v | rx-sweep (Linear) | 3.82 | 273.82M | 1.05B | 310.15M | 88.61% | 99.95% | 15.78K | 1.17% |
| ss_pcm.v | rx-oop (OOP Engine) | 2.43 | 319.63M | 776.80M | 436.33M | 91.17% | 99.92% | 31.88K | 1.66% |
| ss_pcm.v | Icarus Verilog | 3.77 | 508.33M | 1.92B | 847.22M | 98.02% | 99.33% | 107.14K | 0.84% |
| usb_phy.v | rx-prop | 3.22 | 258.34M | 832.28M | 267.07M | 89.19% | 99.98% | 5.84K | 1.11% |
| usb_phy.v | rx-sweep (Linear) | 3.81 | 299.99M | 1.14B | 347.13M | 88.73% | 99.96% | 15.34K | 0.88% |
| usb_phy.v | rx-oop (OOP Engine) | 2.50 | 325.05M | 811.31M | 431.29M | 90.17% | 99.95% | 22.19K | 1.78% |
| usb_phy.v | Icarus Verilog | 3.50 | 403.68M | 1.41B | 608.33M | 98.03% | 99.30% | 97.72K | 0.99% |
| sasc.v | rx-prop | 3.38 | 316.75M | 1.07B | 331.18M | 88.25% | 99.91% | 34.63K | 0.97% |
| sasc.v | rx-sweep (Linear) | 3.81 | 364.39M | 1.39B | 418.69M | 88.09% | 99.96% | 16.73K | 1.00% |
| sasc.v | rx-oop (OOP Engine) | 2.52 | 429.21M | 1.08B | 614.24M | 90.72% | 99.93% | 40.98K | 1.57% |
| sasc.v | Icarus Verilog | 3.62 | 485.56M | 1.76B | 762.35M | 97.79% | 99.50% | 87.22K | 0.90% |
| simple_spi.v | rx-prop | 3.56 | 283.53M | 1.01B | 313.62M | 86.49% | 99.99% | 6.98K | 0.40% |
| simple_spi.v | rx-sweep (Linear) | 4.01 | 358.46M | 1.44B | 416.88M | 86.21% | 99.95% | 27.22K | 0.65% |
| simple_spi.v | rx-oop (OOP Engine) | 2.88 | 345.04M | 993.81M | 529.90M | 89.36% | 99.93% | 46.88K | 0.68% |
| simple_spi.v | Icarus Verilog | 3.77 | 582.81M | 2.19B | 945.29M | 97.22% | 99.30% | 191.03K | 0.74% |
| pci_spoci_ctrl.v | rx-prop | 4.04 | 201.50M | 813.13M | 247.06M | 94.31% | 99.95% | 5.15K | 0.77% |
| pci_spoci_ctrl.v | rx-sweep (Linear) | 3.88 | 247.30M | 959.06M | 282.12M | 88.09% | 99.98% | 9.42K | 0.73% |
| pci_spoci_ctrl.v | rx-oop (OOP Engine) | 2.03 | 380.15M | 771.72M | 490.55M | 92.70% | 99.92% | 27.55K | 3.74% |
| pci_spoci_ctrl.v | Icarus Verilog | 3.45 | 796.10M | 2.75B | 1.25B | 97.09% | 99.01% | 347.80K | 0.93% |
| i2c.v | rx-prop | 3.63 | 349.13M | 1.27B | 377.77M | 88.65% | 99.94% | 33.85K | 0.51% |
| i2c.v | rx-sweep (Linear) | 3.94 | 419.29M | 1.65B | 497.22M | 87.62% | 99.94% | 43.69K | 0.60% |
| i2c.v | rx-oop (OOP Engine) | 2.50 | 489.78M | 1.22B | 708.08M | 90.35% | 99.93% | 47.14K | 1.66% |
| i2c.v | Icarus Verilog | 3.77 | 1.04B | 3.91B | 1.74B | 95.86% | 96.11% | 2.80M | 0.63% |
| systemcdes.v | rx-prop | 2.07 | 3.25B | 6.73B | 2.55B | 91.18% | 99.62% | 881.48K | 6.37% |
| systemcdes.v | rx-sweep (Linear) | 2.47 | 2.06B | 5.10B | 1.84B | 90.65% | 99.63% | 635.21K | 4.79% |
| systemcdes.v | rx-oop (OOP Engine) | 1.31 | 5.33B | 6.99B | 5.28B | 93.80% | 98.26% | 5.78M | 8.61% |
| systemcdes.v | Icarus Verilog | 2.73 | 13.01B | 35.51B | 18.88B | 96.49% | 79.59% | 135.18M | 1.33% |
| spi.v | rx-prop | 3.47 | 586.44M | 2.03B | 651.45M | 87.22% | 99.79% | 174.11K | 0.43% |
| spi.v | rx-sweep (Linear) | 3.96 | 748.10M | 2.97B | 879.74M | 85.13% | 99.32% | 910.26K | 0.72% |
| spi.v | rx-oop (OOP Engine) | 2.86 | 681.74M | 1.95B | 1.06B | 88.95% | 99.67% | 387.84K | 0.88% |
| spi.v | Icarus Verilog | 3.65 | 2.32B | 8.45B | 3.74B | 96.04% | 81.67% | 27.20M | 0.54% |
| wb_dma.v | rx-prop | 3.66 | 1.46B | 5.34B | 1.70B | 85.80% | 99.22% | 1.93M | 0.62% |
| wb_dma.v | rx-sweep (Linear) | 3.91 | 1.77B | 6.92B | 2.16B | 87.83% | 97.85% | 5.65M | 0.98% |
| wb_dma.v | rx-oop (OOP Engine) | 2.51 | 2.04B | 5.13B | 2.92B | 89.31% | 94.24% | 17.92M | 0.95% |
| wb_dma.v | Icarus Verilog | 4.00 | 5.15B | 20.57B | 8.85B | 98.39% | 80.56% | 28.04M | 0.45% |
| des_area.v | rx-prop | 2.02 | 3.50B | 7.06B | 2.74B | 91.74% | 99.37% | 1.49M | 6.60% |
| des_area.v | rx-sweep (Linear) | 2.40 | 2.17B | 5.21B | 1.92B | 91.52% | 99.32% | 1.11M | 4.94% |
| des_area.v | rx-oop (OOP Engine) | 1.29 | 5.37B | 6.91B | 5.28B | 93.82% | 94.17% | 18.97M | 8.48% |
| des_area.v | Icarus Verilog | 3.19 | 41.31B | 131.66B | 50.11B | 97.45% | 81.44% | 236.67M | 0.58% |
| tv80.v | rx-prop | 3.49 | 838.30M | 2.92B | 934.91M | 85.92% | 99.30% | 950.99K | 0.67% |
| tv80.v | rx-sweep (Linear) | 3.58 | 1.35B | 4.82B | 1.48B | 84.70% | 94.52% | 12.41M | 0.88% |
| tv80.v | rx-oop (OOP Engine) | 2.54 | 1.13B | 2.86B | 1.61B | 89.77% | 97.57% | 4.22M | 1.28% |
| tv80.v | Icarus Verilog | 2.83 | 1.59B | 4.51B | 2.01B | 96.09% | 91.19% | 7.15M | 1.08% |
| systemcaes.v | rx-prop | 2.94 | 2.77B | 8.14B | 2.70B | 88.56% | 88.85% | 34.43M | 1.24% |
| systemcaes.v | rx-sweep (Linear) | 3.42 | 3.09B | 10.57B | 3.33B | 87.56% | 90.92% | 37.70M | 1.28% |
| systemcaes.v | rx-oop (OOP Engine) | 1.95 | 3.97B | 7.75B | 4.78B | 91.31% | 73.40% | 110.79M | 2.11% |
| systemcaes.v | Icarus Verilog | 4.00 | 17.79B | 71.20B | 31.57B | 96.86% | 73.37% | 263.41M | 0.35% |
| mem_ctrl.v | rx-prop | 3.40 | 2.40B | 8.15B | 2.62B | 86.33% | 92.41% | 27.07M | 0.60% |
| mem_ctrl.v | rx-sweep (Linear) | 3.66 | 3.27B | 11.98B | 3.66B | 86.38% | 91.79% | 41.13M | 0.89% |
| mem_ctrl.v | rx-oop (OOP Engine) | 2.10 | 3.79B | 7.97B | 4.61B | 89.97% | 68.27% | 147.01M | 0.98% |
| mem_ctrl.v | Icarus Verilog | 3.40 | 7.44B | 25.28B | 11.18B | 97.21% | 60.24% | 123.80M | 0.49% |
| ac97_ctrl.v | rx-prop | 3.07 | 4.66B | 14.29B | 4.51B | 85.39% | 80.71% | 127.16M | 0.16% |
| ac97_ctrl.v | rx-sweep (Linear) | 3.72 | 5.58B | 20.76B | 6.33B | 87.14% | 88.63% | 92.46M | 0.61% |
| ac97_ctrl.v | rx-oop (OOP Engine) | 2.30 | 6.02B | 13.83B | 7.58B | 89.01% | 57.14% | 357.30M | 0.23% |
| ac97_ctrl.v | Icarus Verilog | 3.22 | 5.67B | 18.25B | 7.42B | 96.31% | 59.20% | 111.63M | 0.42% |
| usb_funct.v | rx-prop | 2.74 | 1.91B | 5.23B | 1.67B | 86.84% | 74.33% | 56.35M | 0.50% |
| usb_funct.v | rx-sweep (Linear) | 3.15 | 3.17B | 9.99B | 3.14B | 83.36% | 90.71% | 48.58M | 0.87% |
| usb_funct.v | rx-oop (OOP Engine) | 2.05 | 2.42B | 4.98B | 2.88B | 89.46% | 64.87% | 107.09M | 0.89% |
| usb_funct.v | Icarus Verilog | 3.57 | 8.06B | 28.79B | 12.45B | 96.58% | 73.19% | 113.94M | 0.44% |
| aes_core.v | rx-prop | 1.57 | 12.63B | 19.85B | 8.31B | 89.73% | 80.16% | 169.82M | 7.82% |
| aes_core.v | rx-sweep (Linear) | 1.77 | 12.73B | 22.51B | 9.13B | 90.34% | 82.14% | 157.66M | 6.68% |
| aes_core.v | rx-oop (OOP Engine) | 1.05 | 18.75B | 19.60B | 16.67B | 93.80% | 69.24% | 318.24M | 9.23% |
| aes_core.v | Icarus Verilog | 2.63 | 25.20B | 66.30B | 34.96B | 97.31% | 50.75% | 461.42M | 1.16% |
| wb_conmax.v | rx-prop | 2.59 | 4.82B | 12.49B | 4.40B | 88.47% | 70.81% | 148.42M | 0.84% |
| wb_conmax.v | rx-sweep (Linear) | 2.93 | 6.56B | 19.20B | 6.32B | 86.03% | 87.57% | 110.12M | 1.49% |
| wb_conmax.v | rx-oop (OOP Engine) | 1.87 | 6.16B | 11.55B | 6.96B | 90.94% | 56.70% | 273.26M | 1.33% |
| wb_conmax.v | Icarus Verilog | 3.77 | 88.01B | 331.74B | 149.11B | 93.89% | 84.49% | 1.41B | 0.24% |
| des_perf.v | rx-prop | 1.34 | 136.02B | 182.41B | 71.43B | 88.61% | 35.53% | 5.25B | 6.35% |
| des_perf.v | rx-sweep (Linear) | 1.83 | 111.10B | 202.81B | 77.66B | 90.99% | 64.10% | 2.51B | 6.01% |
| des_perf.v | rx-oop (OOP Engine) | 0.73 | 246.50B | 180.32B | 153.76B | 93.51% | 24.27% | 7.57B | 7.64% |
| des_perf.v | Icarus Verilog | 1.10 | 61.04B | 67.02B | 37.71B | 95.97% | 35.95% | 971.58M | 1.47% |
| vga_lcd.v | rx-prop | 2.46 | 49.36B | 121.26B | 37.95B | 85.23% | 57.90% | 2.36B | 0.07% |
| vga_lcd.v | rx-sweep (Linear) | 3.30 | 53.60B | 176.96B | 53.75B | 86.46% | 78.11% | 1.59B | 0.70% |
| vga_lcd.v | rx-oop (OOP Engine) | 1.94 | 60.64B | 117.65B | 65.44B | 89.57% | 58.11% | 2.86B | 0.13% |
| vga_lcd.v | Icarus Verilog | 1.97 | 22.16B | 43.55B | 17.57B | 94.71% | 78.25% | 202.62M | 1.06% |
