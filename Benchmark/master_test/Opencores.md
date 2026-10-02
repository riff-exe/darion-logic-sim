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
| pci_conf_cyc_addr_dec.v | 184 | 0.61 MB (28.1 MB peak) | N/A | 0.54 MB (8.4 MB peak) | 0.71 MB (4.4 MB peak) |
| steppermotordrive.v | 258 | 1.10 MB (28.7 MB peak) | N/A | 1.07 MB (8.9 MB peak) | 0.71 MB (4.4 MB peak) |
| ss_pcm.v | 648 | 2.43 MB (30.0 MB peak) | N/A | 2.07 MB (9.9 MB peak) | 0.70 MB (4.4 MB peak) |
| usb_phy.v | 715 | 2.61 MB (30.2 MB peak) | N/A | 2.52 MB (10.4 MB peak) | 0.73 MB (4.4 MB peak) |
| sasc.v | 1,125 | 3.23 MB (30.8 MB peak) | N/A | 2.54 MB (10.5 MB peak) | 0.76 MB (4.5 MB peak) |
| simple_spi.v | 1,489 | 3.76 MB (31.2 MB peak) | N/A | 4.07 MB (11.9 MB peak) | 0.80 MB (4.5 MB peak) |
| pci_spoci_ctrl.v | 1,696 | 2.93 MB (30.5 MB peak) | N/A | 5.20 MB (13.0 MB peak) | 0.74 MB (4.4 MB peak) |
| i2c.v | 1,496 | 3.75 MB (31.3 MB peak) | N/A | 5.37 MB (13.2 MB peak) | 0.73 MB (4.4 MB peak) |
| systemcdes.v | 4,326 | 10.95 MB (38.5 MB peak) | N/A | 13.68 MB (21.5 MB peak) | 0.80 MB (4.5 MB peak) |
| spi.v | 4,531 | 8.07 MB (35.7 MB peak) | N/A | 14.91 MB (22.8 MB peak) | 0.81 MB (4.5 MB peak) |
| wb_dma.v | 5,720 | 15.54 MB (43.1 MB peak) | N/A | 16.00 MB (23.9 MB peak) | 0.89 MB (4.6 MB peak) |
| des_area.v | 6,445 | 10.13 MB (37.6 MB peak) | N/A | 18.93 MB (26.8 MB peak) | 1.00 MB (4.6 MB peak) |
| tv80.v | 10,607 | 19.70 MB (47.1 MB peak) | N/A | 31.12 MB (39.0 MB peak) | N/A |
| systemcaes.v | 14,071 | 23.75 MB (52.2 MB peak) | N/A | 41.02 MB (48.9 MB peak) | 1.16 MB (4.8 MB peak) |
| mem_ctrl.v | 16,796 | 34.45 MB (63.8 MB peak) | N/A | 53.99 MB (61.9 MB peak) | 1.25 MB (4.9 MB peak) |
| ac97_ctrl.v | 19,069 | 47.28 MB (74.9 MB peak) | N/A | 65.51 MB (73.3 MB peak) | 1.33 MB (5.0 MB peak) |
| usb_funct.v | 18,282 | 40.15 MB (67.8 MB peak) | N/A | 59.46 MB (67.3 MB peak) | 1.26 MB (5.0 MB peak) |
| aes_core.v | 25,565 | 30.72 MB (61.6 MB peak) | N/A | 78.80 MB (86.6 MB peak) | 1.24 MB (4.9 MB peak) |
| wb_conmax.v | 49,326 | 47.80 MB (80.9 MB peak) | N/A | 144.09 MB (151.9 MB peak) | 1.27 MB (4.9 MB peak) |
| des_perf.v | 111,781 | 204.78 MB (241.0 MB peak) | N/A | 440.55 MB (448.5 MB peak) | 2.80 MB (6.5 MB peak) |
| vga_lcd.v | 187,445 | 374.33 MB (415.0 MB peak) | N/A | 592.62 MB (600.5 MB peak) | 3.34 MB (6.9 MB peak) |

---

## 2. Zero-Testbench Load & Compilation Times (Phase 1)

| Circuit | Gates | Cython Reactor | Pure Python | Icarus Verilog | Verilator C++ |
|:---|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | 184 | 0.16 ms (0.021 ms opt) | N/A | 4.99 ms | 2.53 s |
| steppermotordrive.v | 258 | 0.44 ms (0.064 ms opt) | N/A | 7.04 ms | 2.60 s |
| ss_pcm.v | 648 | 1.28 ms (0.147 ms opt) | N/A | 11.44 ms | 2.63 s |
| usb_phy.v | 715 | 1.51 ms (0.198 ms opt) | N/A | 13.77 ms | 2.59 s |
| sasc.v | 1,125 | 1.79 ms (0.215 ms opt) | N/A | 13.66 ms | 2.83 s |
| simple_spi.v | 1,489 | 2.12 ms (0.266 ms opt) | N/A | 19.37 ms | 2.88 s |
| pci_spoci_ctrl.v | 1,696 | 1.77 ms (0.237 ms opt) | N/A | 23.62 ms | 2.73 s |
| i2c.v | 1,496 | 2.09 ms (0.298 ms opt) | N/A | 24.92 ms | 2.87 s |
| systemcdes.v | 4,326 | 5.02 ms (0.637 ms opt) | N/A | 61.70 ms | 3.49 s |
| spi.v | 4,531 | 5.39 ms (0.595 ms opt) | N/A | 65.50 ms | 3.75 s |
| wb_dma.v | 5,720 | 9.64 ms (1.024 ms opt) | N/A | 70.22 ms | 5.11 s |
| des_area.v | 6,445 | 5.74 ms (0.789 ms opt) | N/A | 89.01 ms | 4.27 s |
| tv80.v | 10,607 | 10.67 ms (1.347 ms opt) | N/A | 151.50 ms | N/A |
| systemcaes.v | 14,071 | 16.12 ms (2.067 ms opt) | N/A | 204.06 ms | 9.71 s |
| mem_ctrl.v | 16,796 | 22.45 ms (3.127 ms opt) | N/A | 267.50 ms | 15.39 s |
| ac97_ctrl.v | 19,069 | 36.97 ms (7.658 ms opt) | N/A | 304.53 ms | 12.26 s |
| usb_funct.v | 18,282 | 32.51 ms (5.889 ms opt) | N/A | 303.33 ms | 11.20 s |
| aes_core.v | 25,565 | 24.16 ms (4.893 ms opt) | N/A | 432.71 ms | 9.44 s |
| wb_conmax.v | 49,326 | 47.57 ms (12.387 ms opt) | N/A | 838.08 ms | 18.28 s |
| des_perf.v | 111,781 | 307.81 ms (57.502 ms opt) | N/A | 2.39 s | 73.87 s |
| vga_lcd.v | 187,445 | 616.39 ms (101.132 ms opt) | N/A | 3.29 s | 150.22 s |

---

## 3. High-Throughput Simulation Performance (Phase 3)

### Simulation Wall-Clock Time (ms)

| Circuit | rx-prop (ms) | rx-sweep (ms) | rx-oop (ms) | Pure Python (ms) | Icarus (ms) | Verilator (ms) |
|:---|---:|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | 22.63 ms | 30.33 ms | N/A | N/A | 874.63 ms | 1.63 ms |
| steppermotordrive.v | 55.44 ms | 61.56 ms | N/A | N/A | 97.30 ms | 22.04 ms |
| ss_pcm.v | 258.63 ms | 277.19 ms | N/A | N/A | 581.92 ms | 48.82 ms |
| usb_phy.v | 269.05 ms | 266.01 ms | N/A | N/A | 414.82 ms | 50.20 ms |
| sasc.v | 342.31 ms | 348.69 ms | N/A | N/A | 516.51 ms | 59.82 ms |
| simple_spi.v | 328.94 ms | 322.08 ms | N/A | N/A | 607.31 ms | 96.51 ms |
| pci_spoci_ctrl.v | 229.49 ms | 241.37 ms | N/A | N/A | 817.67 ms | 62.12 ms |
| i2c.v | 391.82 ms | 367.23 ms | N/A | N/A | 1118.98 ms | 118.40 ms |
| systemcdes.v | 2763.04 ms | 2114.37 ms | N/A | N/A | 15.67 s | 231.54 ms |
| spi.v | 613.01 ms | 719.59 ms | N/A | N/A | 2367.62 ms | 220.02 ms |
| wb_dma.v | 1579.88 ms | 1660.91 ms | N/A | N/A | 5710.91 ms | 388.55 ms |
| des_area.v | 2796.09 ms | 2412.41 ms | N/A | N/A | 50.61 s | 358.31 ms |
| tv80.v | 905.57 ms | 1270.05 ms | N/A | N/A | 1026.86 ms | 433.92 ms |
| systemcaes.v | 2699.12 ms | 3005.85 ms | N/A | N/A | 20.57 s | 743.00 ms |
| mem_ctrl.v | 2645.61 ms | 3055.23 ms | N/A | N/A | 7414.74 ms | 959.15 ms |
| ac97_ctrl.v | 5136.26 ms | 5091.02 ms | N/A | N/A | 4950.78 ms | 1215.02 ms |
| usb_funct.v | 1914.10 ms | 3121.44 ms | N/A | N/A | 8139.19 ms | 1325.98 ms |
| aes_core.v | 9737.18 ms | 11.24 s | N/A | N/A | 28.45 s | 973.30 ms |
| wb_conmax.v | 4713.29 ms | 6461.07 ms | N/A | N/A | 102.20 s | 1744.85 ms |
| des_perf.v | 124.50 s | 115.56 s | N/A | N/A | 585.88 s | 32.38 s |
| vga_lcd.v | 51.13 s | 48.87 s | N/A | N/A | 70.97 s | 52.71 s |

### Speedup Analysis (vs Baseline: Icarus = 1.00x)

| Circuit | rx-prop | rx-sweep | rx-oop | Pure Python | Icarus | Verilator C++ |
|:---|---:|---:|---:|---:|---:|---:|
| pci_conf_cyc_addr_dec.v | 38.64x | 28.83x | N/A | N/A | 1.00x | 537.77x |
| steppermotordrive.v | 1.76x | 1.58x | N/A | N/A | 1.00x | 4.41x |
| ss_pcm.v | 2.25x | 2.10x | N/A | N/A | 1.00x | 11.92x |
| usb_phy.v | 1.54x | 1.56x | N/A | N/A | 1.00x | 8.26x |
| sasc.v | 1.51x | 1.48x | N/A | N/A | 1.00x | 8.63x |
| simple_spi.v | 1.85x | 1.89x | N/A | N/A | 1.00x | 6.29x |
| pci_spoci_ctrl.v | 3.56x | 3.39x | N/A | N/A | 1.00x | 13.16x |
| i2c.v | 2.86x | 3.05x | N/A | N/A | 1.00x | 9.45x |
| systemcdes.v | 5.67x | 7.41x | N/A | N/A | 1.00x | 67.69x |
| spi.v | 3.86x | 3.29x | N/A | N/A | 1.00x | 10.76x |
| wb_dma.v | 3.61x | 3.44x | N/A | N/A | 1.00x | 14.70x |
| des_area.v | 18.10x | 20.98x | N/A | N/A | 1.00x | 141.26x |
| tv80.v | 1.13x | 0.81x | N/A | N/A | 1.00x | 2.37x |
| systemcaes.v | 7.62x | 6.84x | N/A | N/A | 1.00x | 27.68x |
| mem_ctrl.v | 2.80x | 2.43x | N/A | N/A | 1.00x | 7.73x |
| ac97_ctrl.v | 0.96x | 0.97x | N/A | N/A | 1.00x | 4.07x |
| usb_funct.v | 4.25x | 2.61x | N/A | N/A | 1.00x | 6.14x |
| aes_core.v | 2.92x | 2.53x | N/A | N/A | 1.00x | 29.23x |
| wb_conmax.v | 21.68x | 15.82x | N/A | N/A | 1.00x | 58.57x |
| des_perf.v | 4.71x | 5.07x | N/A | N/A | 1.00x | 18.09x |
| vga_lcd.v | 1.39x | 1.45x | N/A | N/A | 1.00x | 1.35x |

### Geo-Mean Speedup Highlights (Baseline: Icarus = 1.00x)

- **rx-prop (Wavefront BFS):** `3.57x`
- **rx-sweep (Linear Compiled):** `3.30x`
- **Icarus Verilog:** `1.00x (Baseline)`
- **Verilator C++:** `14.05x`

### Cross-Engine Comparisons

- **Reactor Sweep vs Propagate Ratio:** `0.92x` (propagate faster)

---

## 4. Hardware PMU & Cache Hierarchy Profiling (Phase 3)

| Circuit | Engine Variant | Instructions | Cycles | IPC | L1 Loads | L1 Misses | L2 Loads | L2 Misses | L3 Loads | DRAM Loads | Branches | Branch Misses |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| pci_conf_cyc_addr_dec.v | rx-prop | 279.41M | 95.66M | 2.92 | 139.68M | 1.35M | 1.35M | 25.11K | 334.11K | 308.10K | 39.94M | 1.14M |
| pci_conf_cyc_addr_dec.v | rx-sweep (Linear) | 256.95M | 121.63M | 2.11 | 147.92M | 1.71M | 1.71M | 35.20K | 721.00K | 692.29K | 54.77M | 2.18M |
| pci_conf_cyc_addr_dec.v | Icarus Verilog | 12.78B | 3.23B | 3.96 | 4.88B | 27.59M | 27.59M | 20.09K | 55.71K | 7.05K | 2.74B | 13.79M |
| pci_conf_cyc_addr_dec.v | Verilator C++ | 124.92K | 2.93M | 0.04 | 3.70M | 43.31K | 43.31K | 1.49K | 1.49K | 0.00 | 2.02M | 450.00 |
| steppermotordrive.v | rx-prop | 803.31M | 196.35M | 4.09 | 304.49M | 609.76K | 609.76K | 3.81K | 33.33K | 29.33K | 77.37M | 189.50K |
| steppermotordrive.v | rx-sweep (Linear) | 977.06M | 231.27M | 4.22 | 317.37M | 1.56M | 1.56M | 17.59K | 28.84K | 25.11K | 193.06M | 1.03M |
| steppermotordrive.v | Icarus Verilog | 1.54B | 382.91M | 4.03 | 654.04M | 1.08M | 1.08M | 33.29K | 80.87K | 33.71K | 310.62M | 2.23M |
| steppermotordrive.v | Verilator C++ | 107.75M | 78.58M | 1.37 | 78.54M | 24.82K | 24.82K | 3.02K | 24.22K | 5.52K | 21.82M | 382.24K |
| ss_pcm.v | rx-prop | 3.09B | 953.61M | 3.24 | 1.18B | 109.98M | 109.98M | 93.54K | 1.99M | 1.87M | 312.25M | 3.27M |
| ss_pcm.v | rx-sweep (Linear) | 3.32B | 1.02B | 3.25 | 1.15B | 154.73M | 154.73M | 114.54K | 1.99M | 1.90M | 646.46M | 9.25M |
| ss_pcm.v | Icarus Verilog | 8.07B | 2.19B | 3.68 | 3.68B | 72.42M | 72.42M | 194.65K | 351.27K | 53.94K | 1.59B | 13.72M |
| ss_pcm.v | Verilator C++ | 284.41M | 163.95M | 1.73 | 222.15M | 50.59K | 50.59K | 2.38K | 9.60K | 6.07K | 45.70M | 860.61K |
| usb_phy.v | rx-prop | 3.18B | 980.49M | 3.24 | 1.22B | 112.69M | 112.69M | 72.70K | 1.16M | 1.12M | 306.56M | 3.51M |
| usb_phy.v | rx-sweep (Linear) | 3.53B | 977.63M | 3.61 | 1.18B | 157.11M | 157.11M | 60.80K | 1.53M | 1.51M | 680.05M | 6.42M |
| usb_phy.v | Icarus Verilog | 5.71B | 1.61B | 3.54 | 2.54B | 48.35M | 48.35M | 224.81K | 476.25K | 74.40K | 1.12B | 10.82M |
| usb_phy.v | Verilator C++ | 344.32M | 170.43M | 2.02 | 214.69M | 27.64K | 27.64K | 1.44K | 24.84K | 313.00 | 48.92M | 1.01M |
| sasc.v | rx-prop | 4.12B | 1.24B | 3.32 | 1.56B | 160.81M | 160.81M | 82.14K | 1.08M | 1.00M | 393.29M | 3.88M |
| sasc.v | rx-sweep (Linear) | 4.38B | 1.27B | 3.44 | 1.44B | 203.73M | 203.73M | 145.90K | 1.91M | 1.79M | 856.68M | 9.72M |
| sasc.v | Icarus Verilog | 7.02B | 1.94B | 3.62 | 3.25B | 72.46M | 72.46M | 269.05K | 549.20K | 82.90K | 1.39B | 12.30M |
| sasc.v | Verilator C++ | 522.71M | 204.47M | 2.56 | 299.87M | 83.70K | 83.70K | 644.00 | 76.41K | 31.69K | 51.76M | 924.14K |
| simple_spi.v | rx-prop | 3.98B | 1.19B | 3.34 | 1.52B | 177.46M | 177.46M | 110.49K | 1.37M | 1.25M | 381.82M | 1.67M |
| simple_spi.v | rx-sweep (Linear) | 4.55B | 1.16B | 3.93 | 1.41B | 232.42M | 232.42M | 68.35K | 1.57M | 1.55M | 932.17M | 5.15M |
| simple_spi.v | Icarus Verilog | 8.78B | 2.32B | 3.78 | 3.95B | 108.24M | 108.24M | 412.31K | 912.36K | 112.76K | 1.74B | 12.50M |
| simple_spi.v | Verilator C++ | 613.49M | 337.70M | 1.82 | 339.32M | 88.59K | 88.59K | 2.32K | 52.22K | 15.00K | 64.04M | 622.46K |
| pci_spoci_ctrl.v | rx-prop | 3.09B | 848.55M | 3.64 | 1.20B | 58.99M | 58.99M | 96.68K | 1.36M | 1.27M | 312.27M | 1.86M |
| pci_spoci_ctrl.v | rx-sweep (Linear) | 3.24B | 917.34M | 3.54 | 997.09M | 133.20M | 133.20M | 109.11K | 2.31M | 2.24M | 665.52M | 4.64M |
| pci_spoci_ctrl.v | Icarus Verilog | 11.08B | 3.16B | 3.51 | 5.18B | 147.85M | 147.85M | 1.29M | 2.22M | 119.65K | 2.18B | 19.70M |
| pci_spoci_ctrl.v | Verilator C++ | 450.95M | 214.31M | 2.10 | 244.39M | 16.04K | 16.04K | 1.17K | 11.03K | 1.22K | 42.09M | 270.47K |
| i2c.v | rx-prop | 4.78B | 1.42B | 3.38 | 1.81B | 167.59M | 167.59M | 111.84K | 1.72M | 1.59M | 455.30M | 2.35M |
| i2c.v | rx-sweep (Linear) | 5.17B | 1.35B | 3.85 | 1.62B | 238.51M | 238.51M | 84.18K | 2.06M | 2.02M | 1.02B | 6.31M |
| i2c.v | Icarus Verilog | 16.18B | 4.19B | 3.86 | 7.40B | 307.88M | 307.88M | 4.51M | 7.85M | 198.40K | 3.18B | 18.77M |
| i2c.v | Verilator C++ | 667.81M | 428.95M | 1.56 | 400.42M | 98.91K | 98.91K | 2.11K | 10.52K | 4.73K | 74.10M | 853.56K |
| systemcdes.v | rx-prop | 26.81B | 10.02B | 2.68 | 10.43B | 1.04B | 1.04B | 2.29M | 17.58M | 13.50M | 2.65B | 124.31M |
| systemcdes.v | rx-sweep (Linear) | 16.50B | 7.74B | 2.13 | 6.51B | 686.10M | 686.10M | 1.84M | 16.55M | 12.96M | 2.90B | 138.08M |
| systemcdes.v | Icarus Verilog | 154.67B | 56.78B | 2.72 | 82.53B | 2.93B | 2.93B | 619.41M | 871.86M | 658.06K | 30.40B | 403.86M |
| systemcdes.v | Verilator C++ | 1.59B | 828.36M | 1.92 | 811.41M | 223.10K | 223.10K | 1.85K | 30.74K | 23.34K | 124.07M | 6.35M |
| spi.v | rx-prop | 7.78B | 2.26B | 3.44 | 2.98B | 325.85M | 325.85M | 338.14K | 4.62M | 4.14M | 771.03M | 3.53M |
| spi.v | rx-sweep (Linear) | 9.71B | 2.62B | 3.70 | 2.91B | 503.75M | 503.75M | 290.95K | 4.80M | 4.51M | 2.04B | 14.11M |
| spi.v | Icarus Verilog | 34.43B | 8.95B | 3.85 | 15.58B | 618.47M | 618.47M | 104.49M | 183.30M | 166.30K | 6.74B | 31.54M |
| spi.v | Verilator C++ | 1.46B | 782.15M | 1.86 | 725.93M | 48.01K | 48.01K | 1.75K | 37.73K | 28.50K | 110.09M | 612.81K |
| wb_dma.v | rx-prop | 20.48B | 5.97B | 3.43 | 7.90B | 911.57M | 911.57M | 2.04M | 24.15M | 21.04M | 2.16B | 13.73M |
| wb_dma.v | rx-sweep (Linear) | 22.12B | 6.24B | 3.54 | 7.40B | 1.07B | 1.07B | 12.16M | 66.09M | 21.44M | 4.45B | 46.99M |
| wb_dma.v | Icarus Verilog | 87.95B | 21.45B | 4.10 | 38.47B | 583.77M | 583.77M | 111.59M | 195.22M | 609.47K | 16.98B | 70.65M |
| wb_dma.v | Verilator C++ | 2.78B | 1.40B | 1.98 | 1.45B | 187.00K | 187.00K | 2.02K | 51.11K | 26.65K | 309.17M | 4.53M |
| des_area.v | rx-prop | 26.71B | 10.28B | 2.60 | 10.57B | 915.67M | 915.67M | 3.86M | 31.35M | 24.58M | 2.79B | 144.75M |
| des_area.v | rx-sweep (Linear) | 17.23B | 8.93B | 1.93 | 7.03B | 641.61M | 641.61M | 3.06M | 29.58M | 23.74M | 3.18B | 171.46M |
| des_area.v | Icarus Verilog | 583.04B | 182.32B | 3.20 | 221.97B | 5.67B | 5.67B | 1.05B | 1.33B | 1.18M | 137.16B | 787.78M |
| des_area.v | Verilator C++ | 2.48B | 1.27B | 1.96 | 1.24B | 64.01K | 64.01K | 4.64K | 161.32K | 150.16K | 77.60M | 6.50M |
| tv80.v | rx-prop | 11.07B | 3.26B | 3.39 | 4.14B | 512.05M | 512.05M | 2.78M | 5.82M | 342.55K | 1.04B | 5.37M |
| tv80.v | rx-sweep (Linear) | 16.12B | 4.57B | 3.53 | 4.49B | 858.09M | 858.09M | 15.04M | 56.17M | 1.27M | 3.44B | 26.02M |
| tv80.v | Icarus Verilog | 13.87B | 4.44B | 3.13 | 6.36B | 239.59M | 239.59M | 28.03M | 43.17M | 1.05M | 2.84B | 25.62M |
| tv80.v | Verilator C++ | 3.24B | 1.56B | 2.08 | 1.73B | 39.59K | 39.59K | 4.20K | 9.21K | 5.65K | 281.03M | 1.58M |
| systemcaes.v | rx-prop | 31.06B | 10.01B | 3.10 | 11.90B | 1.14B | 1.14B | 76.28M | 202.06M | 26.78M | 3.16B | 31.15M |
| systemcaes.v | rx-sweep (Linear) | 34.27B | 11.05B | 3.10 | 11.08B | 1.66B | 1.66B | 124.99M | 535.67M | 25.29M | 6.96B | 90.67M |
| systemcaes.v | Icarus Verilog | 308.47B | 74.98B | 4.11 | 137.99B | 4.31B | 4.31B | 1.19B | 2.01B | 4.88M | 56.54B | 177.40M |
| systemcaes.v | Verilator C++ | 6.28B | 2.66B | 2.36 | 2.74B | 79.51K | 79.51K | 41.39K | 226.73K | 192.91K | 477.66M | 1.28M |
| mem_ctrl.v | rx-prop | 31.30B | 9.58B | 3.27 | 11.76B | 1.31B | 1.31B | 62.27M | 151.05M | 11.17M | 3.01B | 16.99M |
| mem_ctrl.v | rx-sweep (Linear) | 37.87B | 11.05B | 3.43 | 11.56B | 1.91B | 1.91B | 116.70M | 692.70M | 10.95M | 7.80B | 75.80M |
| mem_ctrl.v | Icarus Verilog | 101.32B | 27.98B | 3.62 | 45.64B | 1.18B | 1.18B | 554.57M | 893.91M | 1.76M | 19.70B | 76.03M |
| mem_ctrl.v | Verilator C++ | 7.27B | 3.44B | 2.12 | 3.70B | 194.56K | 194.56K | 124.61K | 278.07K | 135.32K | 617.03M | 6.95M |
| ac97_ctrl.v | rx-prop | 54.19B | 18.36B | 2.95 | 20.21B | 2.38B | 2.38B | 363.81M | 1.26B | 8.18M | 5.07B | 8.51M |
| ac97_ctrl.v | rx-sweep (Linear) | 65.94B | 18.21B | 3.62 | 19.72B | 3.23B | 3.23B | 349.20M | 2.26B | 8.37M | 13.43B | 79.21M |
| ac97_ctrl.v | Icarus Verilog | 67.30B | 19.34B | 3.48 | 27.79B | 1.01B | 1.01B | 514.83M | 959.96M | 1.60M | 13.99B | 39.43M |
| ac97_ctrl.v | Verilator C++ | 9.82B | 4.34B | 2.26 | 4.73B | 352.97K | 352.97K | 968.33K | 1.13M | 198.47K | 1.06B | 5.14M |
| usb_funct.v | rx-prop | 19.81B | 7.04B | 2.81 | 7.54B | 836.85M | 836.85M | 129.11M | 336.05M | 12.33M | 1.97B | 10.19M |
| usb_funct.v | rx-sweep (Linear) | 33.92B | 11.30B | 3.00 | 9.18B | 1.91B | 1.91B | 195.84M | 1.04B | 12.70M | 7.76B | 72.03M |
| usb_funct.v | Icarus Verilog | 116.19B | 30.69B | 3.79 | 51.06B | 1.67B | 1.67B | 513.18M | 846.81M | 2.99M | 22.65B | 75.81M |
| usb_funct.v | Verilator C++ | 9.88B | 4.74B | 2.08 | 4.78B | 392.64K | 392.64K | 897.27K | 920.61K | 40.04K | 1.06B | 7.83M |
| aes_core.v | rx-prop | 75.00B | 34.91B | 2.15 | 29.03B | 3.62B | 3.62B | 692.57M | 1.19B | 26.96M | 7.35B | 339.60M |
| aes_core.v | rx-sweep (Linear) | 76.24B | 40.47B | 1.88 | 29.75B | 3.54B | 3.54B | 594.57M | 1.91B | 26.74M | 12.10B | 605.65M |
| aes_core.v | Icarus Verilog | 277.46B | 104.39B | 2.66 | 147.86B | 3.84B | 3.84B | 2.02B | 2.58B | 14.13M | 52.92B | 597.20M |
| aes_core.v | Verilator C++ | 5.40B | 3.46B | 1.56 | 3.02B | 118.73K | 118.73K | 129.88K | 316.56K | 208.16K | 395.20M | 27.54M |
| wb_conmax.v | rx-prop | 48.81B | 18.35B | 2.66 | 19.68B | 1.93B | 1.93B | 440.90M | 1.16B | 116.42M | 5.83B | 40.46M |
| wb_conmax.v | rx-sweep (Linear) | 66.72B | 24.58B | 2.71 | 21.32B | 3.52B | 3.52B | 475.42M | 2.67B | 112.72M | 14.93B | 205.91M |
| wb_conmax.v | Icarus Verilog | 1448.02B | 374.10B | 3.87 | 653.99B | 39.81B | 39.81B | 6.37B | 9.22B | 44.88M | 274.05B | 581.57M |
| wb_conmax.v | Verilator C++ | 13.33B | 6.21B | 2.14 | 6.20B | 4.43M | 4.43M | 135.20M | 135.76M | 381.42K | 727.34M | 2.32M |
| des_perf.v | rx-prop | 699.36B | 446.06B | 1.57 | 269.75B | 35.37B | 35.37B | 21.19B | 40.50B | 131.74M | 65.36B | 2.95B |
| des_perf.v | rx-sweep (Linear) | 643.49B | 412.32B | 1.56 | 274.79B | 28.46B | 28.46B | 10.31B | 28.93B | 139.82M | 103.53B | 5.90B |
| des_perf.v | Icarus Verilog | 59.54B | 51.66B | 1.15 | 33.69B | 1.35B | 1.35B | 867.41M | 1.15B | 266.89M | 12.29B | 180.47M |
| des_perf.v | Verilator C++ | 50.91B | 114.10B | 0.45 | 36.96B | 228.95M | 228.95M | 3.71B | 3.77B | 200.99K | 4.91B | 2.06B |
| vga_lcd.v | rx-prop | 460.10B | 182.01B | 2.53 | 173.34B | 20.46B | 20.46B | 5.41B | 26.34B | 54.38M | 42.24B | 34.79M |
| vga_lcd.v | rx-sweep (Linear) | 558.61B | 173.60B | 3.22 | 165.55B | 27.74B | 27.74B | 5.93B | 34.13B | 340.32M | 113.78B | 880.53M |
| vga_lcd.v | Icarus Verilog | 38.63B | 19.40B | 1.99 | 15.63B | 827.35M | 827.35M | 183.12M | 267.13M | 44.75M | 8.35B | 87.69M |
| vga_lcd.v | Verilator C++ | 71.50B | 185.57B | 0.39 | 56.97B | 353.12M | 353.12M | 5.98B | 6.15B | 124.82K | 7.62B | 3.83B |
