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
| pci_conf_cyc_addr_dec.v | 184 | 0.57 MB (31.9 MB peak) | N/A | 0.61 MB (8.4 MB peak) | 0.70 MB (4.4 MB peak) |
| steppermotordrive.v | 258 | 1.11 MB (32.4 MB peak) | N/A | 1.06 MB (8.9 MB peak) | 0.76 MB (4.4 MB peak) |
| ss_pcm.v | 648 | 2.44 MB (33.7 MB peak) | N/A | 2.06 MB (9.9 MB peak) | 0.77 MB (4.4 MB peak) |
| usb_phy.v | 715 | 2.66 MB (34.0 MB peak) | N/A | 2.64 MB (10.5 MB peak) | 0.75 MB (4.4 MB peak) |
| sasc.v | 1,125 | 3.26 MB (34.6 MB peak) | N/A | 2.69 MB (10.5 MB peak) | 0.76 MB (4.5 MB peak) |
| simple_spi.v | 1,489 | 3.82 MB (35.2 MB peak) | N/A | 4.02 MB (11.9 MB peak) | 0.75 MB (4.5 MB peak) |
| pci_spoci_ctrl.v | 1,696 | 2.96 MB (34.2 MB peak) | N/A | 5.18 MB (13.0 MB peak) | 0.87 MB (4.5 MB peak) |
| i2c.v | 1,496 | 5.67 MB (37.0 MB peak) | N/A | 5.19 MB (13.1 MB peak) | 0.77 MB (4.5 MB peak) |
| systemcdes.v | 4,326 | 7.09 MB (38.5 MB peak) | N/A | 13.57 MB (21.5 MB peak) | 0.89 MB (4.6 MB peak) |
| spi.v | 4,531 | 8.79 MB (40.1 MB peak) | N/A | 15.00 MB (22.8 MB peak) | 0.87 MB (4.5 MB peak) |
| wb_dma.v | 5,720 | 15.79 MB (47.1 MB peak) | N/A | 16.04 MB (23.9 MB peak) | 0.97 MB (4.6 MB peak) |
| des_area.v | 6,445 | 9.15 MB (40.4 MB peak) | N/A | 18.93 MB (26.8 MB peak) | 0.94 MB (4.6 MB peak) |
| tv80.v | 10,607 | 18.53 MB (49.9 MB peak) | N/A | 31.13 MB (39.0 MB peak) | N/A |
| systemcaes.v | 14,071 | 25.76 MB (57.4 MB peak) | N/A | 40.91 MB (48.8 MB peak) | 1.25 MB (4.8 MB peak) |
| mem_ctrl.v | 16,796 | 32.92 MB (65.9 MB peak) | N/A | 53.96 MB (61.8 MB peak) | 1.19 MB (4.9 MB peak) |
| ac97_ctrl.v | 19,069 | 52.66 MB (85.4 MB peak) | N/A | 65.52 MB (73.4 MB peak) | 1.30 MB (5.0 MB peak) |
| usb_funct.v | 18,282 | 46.28 MB (78.8 MB peak) | N/A | 59.35 MB (67.2 MB peak) | 1.26 MB (5.0 MB peak) |
| aes_core.v | 25,565 | 29.65 MB (64.4 MB peak) | N/A | 78.86 MB (86.7 MB peak) | 1.18 MB (4.9 MB peak) |
| wb_conmax.v | 49,326 | 48.48 MB (84.6 MB peak) | N/A | 144.18 MB (152.0 MB peak) | 1.31 MB (5.0 MB peak) |
| des_perf.v | 111,781 | 206.85 MB (245.1 MB peak) | N/A | 440.62 MB (448.4 MB peak) | 2.73 MB (6.4 MB peak) |
| vga_lcd.v | 187,445 | 379.26 MB (419.9 MB peak) | N/A | 592.68 MB (600.5 MB peak) | 3.32 MB (7.0 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | 184 | 8.26 ms (0.023 ms opt) | N/A | 6.78 ms | 3.62 s |
| steppermotordrive.v | 258 | 9.17 ms (0.084 ms opt) | N/A | 9.39 ms | 3.63 s |
| ss_pcm.v | 648 | 10.00 ms (0.221 ms opt) | N/A | 15.36 ms | 3.70 s |
| usb_phy.v | 715 | 10.62 ms (0.240 ms opt) | N/A | 18.30 ms | 3.76 s |
| sasc.v | 1,125 | 10.84 ms (0.298 ms opt) | N/A | 18.41 ms | 3.86 s |
| simple_spi.v | 1,489 | 11.41 ms (0.355 ms opt) | N/A | 26.91 ms | 3.95 s |
| pci_spoci_ctrl.v | 1,696 | 10.89 ms (0.345 ms opt) | N/A | 35.30 ms | 3.84 s |
| i2c.v | 1,496 | 15.38 ms (0.429 ms opt) | N/A | 36.53 ms | 4.02 s |
| systemcdes.v | 4,326 | 15.72 ms (0.858 ms opt) | N/A | 93.46 ms | 4.82 s |
| spi.v | 4,531 | 16.80 ms (0.920 ms opt) | N/A | 93.85 ms | 5.21 s |
| wb_dma.v | 5,720 | 22.04 ms (1.470 ms opt) | N/A | 96.43 ms | 6.95 s |
| des_area.v | 6,445 | 16.94 ms (1.198 ms opt) | N/A | 127.46 ms | 5.87 s |
| tv80.v | 10,607 | 24.54 ms (2.204 ms opt) | N/A | 203.15 ms | N/A |
| systemcaes.v | 14,071 | 32.68 ms (3.448 ms opt) | N/A | 275.00 ms | 12.77 s |
| mem_ctrl.v | 16,796 | 44.70 ms (5.900 ms opt) | N/A | 371.69 ms | 21.37 s |
| ac97_ctrl.v | 19,069 | 64.05 ms (10.486 ms opt) | N/A | 427.93 ms | 15.82 s |
| usb_funct.v | 18,282 | 57.53 ms (10.323 ms opt) | N/A | 402.08 ms | 14.62 s |
| aes_core.v | 25,565 | 44.82 ms (7.359 ms opt) | N/A | 566.00 ms | 11.82 s |
| wb_conmax.v | 49,326 | 82.73 ms (17.357 ms opt) | N/A | 1.11 s | 22.95 s |
| des_perf.v | 111,781 | 422.24 ms (73.173 ms opt) | N/A | 3.07 s | 96.52 s |
| vga_lcd.v | 187,445 | 792.58 ms (146.590 ms opt) | N/A | 4.14 s | 189.97 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | 7.82 ms | 8.84 ms | 7.76 ms | N/A | 254.14 ms | 1.69 ms |
| steppermotordrive.v | 16.65 ms | 23.01 ms | 19.81 ms | N/A | 29.46 ms | 3.57 ms |
| ss_pcm.v | 87.18 ms | 102.38 ms | 94.40 ms | N/A | 165.32 ms | 13.44 ms |
| usb_phy.v | 93.02 ms | 111.07 ms | 99.21 ms | N/A | 119.39 ms | 15.13 ms |
| sasc.v | 114.56 ms | 134.05 ms | 123.77 ms | N/A | 153.27 ms | 19.46 ms |
| simple_spi.v | 104.72 ms | 129.97 ms | 111.85 ms | N/A | 173.63 ms | 28.63 ms |
| pci_spoci_ctrl.v | 75.95 ms | 89.41 ms | 83.95 ms | N/A | 236.75 ms | 19.81 ms |
| i2c.v | 128.66 ms | 147.96 ms | 131.05 ms | N/A | 330.01 ms | 35.58 ms |
| systemcdes.v | 1156.08 ms | 736.73 ms | 1344.79 ms | N/A | 4492.43 ms | 76.06 ms |
| spi.v | 211.82 ms | 278.48 ms | 210.20 ms | N/A | 694.24 ms | 66.27 ms |
| wb_dma.v | 518.39 ms | 624.69 ms | 635.41 ms | N/A | 1671.21 ms | 124.88 ms |
| des_area.v | 1241.23 ms | 759.88 ms | 1313.39 ms | N/A | 14.90 s | 100.17 ms |
| tv80.v | 308.84 ms | 493.13 ms | 343.84 ms | N/A | 298.07 ms | 121.14 ms |
| systemcaes.v | 983.87 ms | 1106.51 ms | 1197.48 ms | N/A | 6036.45 ms | 236.73 ms |
| mem_ctrl.v | 876.02 ms | 1187.75 ms | 1248.77 ms | N/A | 2176.61 ms | 299.44 ms |
| ac97_ctrl.v | 1745.00 ms | 2018.11 ms | 2428.16 ms | N/A | 1501.43 ms | 372.08 ms |
| usb_funct.v | 666.92 ms | 1155.27 ms | 860.15 ms | N/A | 2431.83 ms | 393.46 ms |
| aes_core.v | 4585.08 ms | 4629.82 ms | 5199.76 ms | N/A | 8614.82 ms | 288.17 ms |
| wb_conmax.v | 1676.35 ms | 2318.16 ms | 2040.91 ms | N/A | 32.26 s | 547.51 ms |
| des_perf.v | 56.26 s | 40.70 s | 72.20 s | N/A | 148.41 s | 9516.39 ms |
| vga_lcd.v | 17.88 s | 18.58 s | 20.49 s | N/A | 16.01 s | 15.11 s |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | 32.49x | 28.73x | 32.76x | N/A | 1.00x | 150.14x |
| steppermotordrive.v | 1.77x | 1.28x | 1.49x | N/A | 1.00x | 8.26x |
| ss_pcm.v | 1.90x | 1.61x | 1.75x | N/A | 1.00x | 12.30x |
| usb_phy.v | 1.28x | 1.07x | 1.20x | N/A | 1.00x | 7.89x |
| sasc.v | 1.34x | 1.14x | 1.24x | N/A | 1.00x | 7.88x |
| simple_spi.v | 1.66x | 1.34x | 1.55x | N/A | 1.00x | 6.06x |
| pci_spoci_ctrl.v | 3.12x | 2.65x | 2.82x | N/A | 1.00x | 11.95x |
| i2c.v | 2.57x | 2.23x | 2.52x | N/A | 1.00x | 9.28x |
| systemcdes.v | 3.89x | 6.10x | 3.34x | N/A | 1.00x | 59.06x |
| spi.v | 3.28x | 2.49x | 3.30x | N/A | 1.00x | 10.48x |
| wb_dma.v | 3.22x | 2.68x | 2.63x | N/A | 1.00x | 13.38x |
| des_area.v | 12.01x | 19.61x | 11.35x | N/A | 1.00x | 148.79x |
| tv80.v | 0.97x | 0.60x | 0.87x | N/A | 1.00x | 2.46x |
| systemcaes.v | 6.14x | 5.46x | 5.04x | N/A | 1.00x | 25.50x |
| mem_ctrl.v | 2.48x | 1.83x | 1.74x | N/A | 1.00x | 7.27x |
| ac97_ctrl.v | 0.86x | 0.74x | 0.62x | N/A | 1.00x | 4.04x |
| usb_funct.v | 3.65x | 2.10x | 2.83x | N/A | 1.00x | 6.18x |
| aes_core.v | 1.88x | 1.86x | 1.66x | N/A | 1.00x | 29.89x |
| wb_conmax.v | 19.24x | 13.92x | 15.81x | N/A | 1.00x | 58.92x |
| des_perf.v | 2.64x | 3.65x | 2.06x | N/A | 1.00x | 15.60x |
| vga_lcd.v | 0.90x | 0.86x | 0.78x | N/A | 1.00x | 1.06x |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `2.89x`
- **rx-sweep (Linear Compiled):** `2.55x`
- **rx-oop (OOP Graph):** `2.52x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `13.03x`

### Cross-Engine Comparisons

- **Reactor Sweep vs Propagate Ratio:** `0.88x` (propagate faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | IPC | Cycles | Instructions | L1 Loads | L1 Hit% | L2 Hit% | LLC Misses | Brn Miss% |
|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | rx-prop | 3.49 | 15.71M | 54.77M | 20.36M | 99.90% | 76.84% | 4.75K | 4.81% |
| pci_conf_cyc_addr_dec.v | rx-sweep (Linear) | 3.05 | 22.17M | 67.65M | 29.74M | 99.11% | 95.47% | 11.89K | 3.12% |
| pci_conf_cyc_addr_dec.v | rx-oop (OOP Engine) | 3.32 | 16.37M | 54.36M | 17.97M | 99.71% | 90.59% | 4.94K | 5.49% |
| pci_conf_cyc_addr_dec.v | Icarus Verilog | 3.97 | 729.10M | 2.89B | 1.11B | 99.43% | 99.60% | 23.32K | 0.49% |
| steppermotordrive.v | rx-prop | 5.10 | 38.00M | 193.71M | 58.74M | 99.87% | 93.70% | 4.82K | 0.37% |
| steppermotordrive.v | rx-sweep (Linear) | 4.74 | 65.83M | 311.84M | 93.79M | 99.44% | 96.07% | 22.06K | 0.46% |
| steppermotordrive.v | rx-oop (OOP Engine) | 4.37 | 44.28M | 193.38M | 60.14M | 99.31% | 98.06% | 7.92K | 0.36% |
| steppermotordrive.v | Icarus Verilog | 4.04 | 101.74M | 411.05M | 155.99M | 99.61% | 92.22% | 43.97K | 0.88% |
| ss_pcm.v | rx-prop | 3.33 | 238.94M | 796.63M | 255.64M | 89.52% | 99.98% | 4.33K | 1.08% |
| ss_pcm.v | rx-sweep (Linear) | 3.74 | 279.78M | 1.05B | 321.45M | 88.94% | 99.98% | 5.47K | 1.15% |
| ss_pcm.v | rx-oop (OOP Engine) | 3.12 | 251.64M | 785.39M | 256.97M | 86.13% | 99.97% | 10.30K | 1.20% |
| ss_pcm.v | Icarus Verilog | 3.68 | 523.14M | 1.92B | 867.44M | 98.03% | 99.69% | 60.77K | 0.82% |
| usb_phy.v | rx-prop | 3.31 | 250.49M | 828.61M | 262.98M | 89.02% | 99.98% | 5.79K | 1.10% |
| usb_phy.v | rx-sweep (Linear) | 3.73 | 302.00M | 1.13B | 344.89M | 88.66% | 99.97% | 9.31K | 1.01% |
| usb_phy.v | rx-oop (OOP Engine) | 3.06 | 265.20M | 812.00M | 272.27M | 85.63% | 99.97% | 7.89K | 1.17% |
| usb_phy.v | Icarus Verilog | 3.51 | 404.13M | 1.42B | 614.48M | 98.02% | 99.37% | 73.07K | 0.99% |
| sasc.v | rx-prop | 3.41 | 301.18M | 1.03B | 325.64M | 88.12% | 99.98% | 8.26K | 1.02% |
| sasc.v | rx-sweep (Linear) | 3.79 | 368.42M | 1.39B | 421.64M | 88.00% | 99.98% | 10.38K | 1.07% |
| sasc.v | rx-oop (OOP Engine) | 3.23 | 330.49M | 1.07B | 359.36M | 85.25% | 99.98% | 11.40K | 1.07% |
| sasc.v | Icarus Verilog | 3.64 | 486.53M | 1.77B | 754.09M | 97.77% | 99.38% | 106.68K | 0.91% |
| simple_spi.v | rx-prop | 3.55 | 293.09M | 1.04B | 322.67M | 86.50% | 99.93% | 34.48K | 0.38% |
| simple_spi.v | rx-sweep (Linear) | 4.04 | 352.05M | 1.42B | 432.19M | 86.56% | 99.97% | 16.36K | 0.65% |
| simple_spi.v | rx-oop (OOP Engine) | 3.45 | 299.19M | 1.03B | 331.73M | 84.43% | 99.84% | 87.63K | 0.47% |
| simple_spi.v | Icarus Verilog | 3.71 | 592.30M | 2.20B | 965.38M | 97.22% | 99.36% | 170.05K | 0.69% |
| pci_spoci_ctrl.v | rx-prop | 3.92 | 206.42M | 808.72M | 253.28M | 94.05% | 99.74% | 42.57K | 0.71% |
| pci_spoci_ctrl.v | rx-sweep (Linear) | 3.86 | 242.49M | 935.89M | 287.61M | 87.86% | 99.96% | 12.75K | 0.74% |
| pci_spoci_ctrl.v | rx-oop (OOP Engine) | 3.45 | 227.42M | 784.58M | 257.47M | 88.03% | 99.98% | 6.66K | 0.89% |
| pci_spoci_ctrl.v | Icarus Verilog | 3.49 | 797.16M | 2.78B | 1.25B | 97.06% | 99.13% | 317.90K | 0.92% |
| i2c.v | rx-prop | 3.50 | 352.37M | 1.23B | 395.07M | 88.62% | 99.98% | 10.31K | 0.49% |
| i2c.v | rx-sweep (Linear) | 4.03 | 403.74M | 1.63B | 482.26M | 87.26% | 99.97% | 17.46K | 0.63% |
| i2c.v | rx-oop (OOP Engine) | 3.49 | 356.53M | 1.24B | 410.39M | 84.29% | 99.95% | 33.66K | 0.51% |
| i2c.v | Icarus Verilog | 3.72 | 1.05B | 3.90B | 1.76B | 95.87% | 96.42% | 2.57M | 0.59% |
| systemcdes.v | rx-prop | 2.10 | 3.21B | 6.74B | 2.55B | 91.16% | 99.51% | 1.10M | 6.29% |
| systemcdes.v | rx-sweep (Linear) | 2.49 | 2.05B | 5.12B | 1.83B | 90.65% | 99.34% | 1.16M | 4.74% |
| systemcdes.v | rx-oop (OOP Engine) | 1.93 | 3.72B | 7.18B | 2.87B | 88.95% | 97.82% | 6.97M | 6.82% |
| systemcdes.v | Icarus Verilog | 2.77 | 12.79B | 35.46B | 18.70B | 96.43% | 79.49% | 136.83M | 1.28% |
| spi.v | rx-prop | 3.46 | 589.98M | 2.04B | 648.11M | 87.02% | 99.85% | 126.51K | 0.44% |
| spi.v | rx-sweep (Linear) | 3.89 | 777.80M | 3.02B | 907.62M | 85.53% | 99.61% | 547.67K | 0.71% |
| spi.v | rx-oop (OOP Engine) | 3.48 | 577.44M | 2.01B | 661.48M | 83.44% | 99.60% | 446.39K | 0.49% |
| spi.v | Icarus Verilog | 3.66 | 2.31B | 8.46B | 3.75B | 96.10% | 83.78% | 23.86M | 0.50% |
| wb_dma.v | rx-prop | 3.59 | 1.47B | 5.29B | 1.75B | 85.92% | 98.79% | 2.97M | 0.60% |
| wb_dma.v | rx-sweep (Linear) | 3.93 | 1.76B | 6.92B | 2.15B | 87.82% | 98.13% | 4.98M | 0.98% |
| wb_dma.v | rx-oop (OOP Engine) | 2.95 | 1.78B | 5.25B | 1.80B | 84.30% | 92.57% | 21.04M | 0.67% |
| wb_dma.v | Icarus Verilog | 4.00 | 5.14B | 20.56B | 8.95B | 98.40% | 80.90% | 27.28M | 0.45% |
| des_area.v | rx-prop | 2.03 | 3.48B | 7.08B | 2.78B | 91.81% | 99.39% | 1.40M | 6.48% |
| des_area.v | rx-sweep (Linear) | 2.43 | 2.15B | 5.22B | 1.93B | 91.50% | 99.25% | 1.21M | 4.91% |
| des_area.v | rx-oop (OOP Engine) | 1.94 | 3.65B | 7.10B | 2.87B | 89.03% | 97.55% | 7.75M | 6.54% |
| des_area.v | Icarus Verilog | 3.16 | 41.63B | 131.63B | 49.87B | 97.42% | 81.15% | 241.95M | 0.55% |
| tv80.v | rx-prop | 3.50 | 846.20M | 2.96B | 932.66M | 85.96% | 99.35% | 867.27K | 0.67% |
| tv80.v | rx-sweep (Linear) | 3.63 | 1.33B | 4.82B | 1.45B | 84.62% | 96.93% | 6.95M | 0.90% |
| tv80.v | rx-oop (OOP Engine) | 3.14 | 937.98M | 2.95B | 990.37M | 84.04% | 97.55% | 3.84M | 0.76% |
| tv80.v | Icarus Verilog | 2.83 | 1.63B | 4.60B | 2.00B | 96.07% | 91.04% | 6.83M | 1.05% |
| systemcaes.v | rx-prop | 2.96 | 2.76B | 8.15B | 2.72B | 88.60% | 88.92% | 34.39M | 1.23% |
| systemcaes.v | rx-sweep (Linear) | 3.42 | 3.09B | 10.57B | 3.35B | 87.57% | 90.26% | 40.55M | 1.31% |
| systemcaes.v | rx-oop (OOP Engine) | 2.42 | 3.33B | 8.06B | 2.83B | 86.23% | 76.15% | 92.89M | 1.44% |
| systemcaes.v | Icarus Verilog | 4.01 | 17.76B | 71.21B | 31.66B | 96.84% | 73.72% | 262.06M | 0.34% |
| mem_ctrl.v | rx-prop | 3.36 | 2.42B | 8.15B | 2.62B | 86.27% | 91.29% | 31.51M | 0.59% |
| mem_ctrl.v | rx-sweep (Linear) | 3.68 | 3.27B | 12.04B | 3.70B | 86.44% | 91.95% | 40.49M | 0.88% |
| mem_ctrl.v | rx-oop (OOP Engine) | 2.37 | 3.43B | 8.14B | 2.78B | 84.14% | 71.34% | 126.25M | 0.70% |
| mem_ctrl.v | Icarus Verilog | 3.41 | 7.42B | 25.32B | 11.20B | 97.20% | 60.92% | 122.47M | 0.48% |
| ac97_ctrl.v | rx-prop | 2.99 | 4.79B | 14.31B | 4.53B | 85.42% | 79.78% | 133.37M | 0.17% |
| ac97_ctrl.v | rx-sweep (Linear) | 3.75 | 5.55B | 20.80B | 6.34B | 87.19% | 89.03% | 89.07M | 0.60% |
| ac97_ctrl.v | rx-oop (OOP Engine) | 2.13 | 6.66B | 14.16B | 4.77B | 83.97% | 52.71% | 360.86M | 0.24% |
| ac97_ctrl.v | Icarus Verilog | 3.15 | 5.80B | 18.26B | 7.43B | 96.31% | 59.80% | 110.23M | 0.41% |
| usb_funct.v | rx-prop | 2.81 | 1.85B | 5.20B | 1.69B | 86.85% | 79.59% | 45.63M | 0.50% |
| usb_funct.v | rx-sweep (Linear) | 3.13 | 3.19B | 9.99B | 3.14B | 83.31% | 90.75% | 48.54M | 0.88% |
| usb_funct.v | rx-oop (OOP Engine) | 2.18 | 2.37B | 5.15B | 1.72B | 84.14% | 58.77% | 112.53M | 0.56% |
| usb_funct.v | Icarus Verilog | 3.49 | 8.27B | 28.84B | 12.48B | 96.59% | 73.03% | 115.08M | 0.43% |
| aes_core.v | rx-prop | 1.58 | 12.61B | 19.89B | 8.37B | 89.80% | 80.13% | 169.83M | 7.80% |
| aes_core.v | rx-sweep (Linear) | 1.77 | 12.70B | 22.51B | 9.11B | 90.33% | 82.00% | 158.80M | 6.66% |
| aes_core.v | rx-oop (OOP Engine) | 1.39 | 14.31B | 19.93B | 8.89B | 88.76% | 69.82% | 301.62M | 7.75% |
| aes_core.v | Icarus Verilog | 2.55 | 26.01B | 66.40B | 34.55B | 97.27% | 50.91% | 464.33M | 1.13% |
| wb_conmax.v | rx-prop | 2.57 | 4.85B | 12.47B | 4.41B | 88.42% | 69.11% | 157.85M | 0.84% |
| wb_conmax.v | rx-sweep (Linear) | 2.90 | 6.62B | 19.20B | 6.40B | 86.08% | 86.98% | 115.85M | 1.51% |
| wb_conmax.v | rx-oop (OOP Engine) | 2.03 | 5.90B | 12.00B | 4.38B | 86.47% | 55.81% | 262.28M | 0.98% |
| wb_conmax.v | Icarus Verilog | 3.55 | 93.47B | 331.92B | 147.68B | 93.89% | 84.20% | 1.43B | 0.23% |
| des_perf.v | rx-prop | 1.18 | 154.53B | 182.51B | 72.76B | 88.85% | 34.80% | 5.29B | 6.33% |
| des_perf.v | rx-sweep (Linear) | 1.81 | 111.87B | 202.92B | 77.54B | 91.01% | 64.05% | 2.51B | 6.03% |
| des_perf.v | rx-oop (OOP Engine) | 0.93 | 198.15B | 184.31B | 79.91B | 87.91% | 21.15% | 7.62B | 6.42% |
| des_perf.v | Icarus Verilog | 1.29 | 51.94B | 66.98B | 37.71B | 95.95% | 36.21% | 972.46M | 1.44% |
| vga_lcd.v | rx-prop | 2.47 | 49.07B | 121.26B | 37.91B | 85.22% | 57.89% | 2.36B | 0.07% |
| vga_lcd.v | rx-sweep (Linear) | 3.47 | 50.96B | 176.89B | 53.36B | 86.41% | 78.60% | 1.55B | 0.68% |
| vga_lcd.v | rx-oop (OOP Engine) | 2.15 | 56.15B | 120.91B | 39.57B | 83.97% | 50.98% | 3.11B | 0.10% |
| vga_lcd.v | Icarus Verilog | 2.17 | 20.06B | 43.53B | 17.66B | 94.66% | 78.67% | 201.16M | 1.06% |
