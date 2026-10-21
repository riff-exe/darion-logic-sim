# Literature Review, Prior Art Audit, and Novelty Defense
**Project:** Darion Logic Sim (`darion-logic-sim`)  
**Target Venues (revised 2026-10-21):** realistic first targets are a regional or local conference or a workshop; a mid-tier venue or a software and tools journal is possible after the extension work (stable documented API, second platform, some real use). The earlier list (DAC, ICCAD, TCAD, DATE) is not realistic for the current state of the work: selective venues need a new technique or a surprising, broadly confirmed result.

---

## 0. Verification log (2026-10-21): what was checked and what changed

Every bibliographic entry below was looked up against Crossref (the DOI registry); factual claims about other tools were checked against their own documentation or source code. "Verified" means the title, authors, venue, year, pages and DOI match the registry record. A cited paper's *content* was not read unless stated.

### 0.1 References

| Reference | Result | Correction |
|---|---|---|
| Abramovici, Breuer, Friedman, *Digital Systems Testing and Testable Design* (1990) | Exists (Computer Science Press / W. H. Freeman, ISBN 0-7167-8179-4; IEEE Press reprint 1994, DOI 10.1109/9780470544389). | Publisher fixed. The claim that this book *treats XOR as incompatible with counting* was NOT checked in the book and is contradicted by Maurer's patents (0.3). |
| Malik, TCAD 13(7):950-956, 1994 | Verified. | **DOI was wrong**: correct is 10.1109/43.293952 (was ...293949). |
| Shiple, Singhal, Brayton, Sangiovanni-Vincentelli, ISCAS 1996, vol. 4, pp. 592-595 | Verified. | **DOI was wrong**: correct is 10.1109/ISCAS.1996.542093 (was ...541999). |
| Agrawal and Dally, "Algorithms for Accuracy Enhancement in a Hardware Logic Simulator", TCAD 9(6):615-626, 1990 | **Does not exist as written.** That title is a DAC 1989 paper by Agrawal, Tutundjian and Dally (pp. 645-648, DOI 10.1145/74382.74496). The TCAD 1990 Agrawal-Dally paper is "A Hardware Logic Simulation System", 9(1):19-29, DOI 10.1109/43.45853. | Entry replaced by the two real papers. **Neither was read**, so its relevance to inertial delay or oscillation limits is unverified: do not cite it for those points unless you read it. |
| Edwards, "Making Cyclic Circuits Acyclic", DAC 2003, pp. 159-162 | Verified. | DOI added: 10.1145/775832.775874. |
| Riedel and Bruck, "The Synthesis of Cyclic Combinational Circuits", DAC 2003 | Verified. | Pages 163-168 and DOI 10.1145/775832.775875 added. |
| Beamer and Donofrio, DAC 2020 (ESSENT) | Verified. | Pages 1-6, DOI 10.1109/DAC18072.2020.9218632 added. |
| Ulrich, CACM 12(2):102-110, 1969 | Verified. | **DOI was wrong**: correct is 10.1145/362848.362870 (was ...362835.362846). |
| Wang and Maurer, "LECSIM", DAC 1990, pp. 491-496 | Verified (DOI 10.1145/123186.123349). | Venue and pages added. |
| Szygenda and Thompson, Computer 8(3), 1975 | Exists as a two-part series (pp. 24-36 by Szygenda and Thompson; pp. 38-49 by Thompson and Szygenda). | **DOI was wrong**: pp. 24-36 is 10.1109/C-M.1975.218898 (was ...218905). Say which part is cited. |
| Bryant, "A Switch-Level Model and Simulator for MOS Digital Systems", IEEE Trans. Computers C-33(2):160-177, 1984 | Verified. | **DOI was wrong**: correct is 10.1109/TC.1984.1676408 (was ...1676409). |
| Chilimbi, Hill, Larus, PLDI 1999, pp. 1-12 | Verified (DOI 10.1145/301618.301633). | none |
| Burch, "Logisim", JERIC 2(1):5-16, 2002 | Verified (Crossref lists the title as "Logisim"; confirm the full title on the ACM page). | **DOI was wrong**: correct is 10.1145/545197.545199 (was 10.1145/773539.773541). |
| Neemann, Digital, 2016 (GitHub) | Software; exists (GPL-3.0). | none |
| Snyder, "Verilator: Open-source Verilog Compiler/Simulator", NASCUG 2004 | **Not found.** Veripool lists only talks and slides by Snyder (for 2004: "Verilator SystemC Environment", slides, NASCUG/DAC 2004-06). Verilator has no peer-reviewed paper of its own. | Replaced by a software citation (project site and version). |
| Acton, "Data-Oriented Design and C++", CppCon 2014 | Verified to exist (CppCon 2014 keynote). | none |

### 0.2 Claims about other tools

| Claim in this file | Verdict | Source |
|---|---|---|
| Verilator `--converge-limit` defaults to 100 | **Version dependent.** 100 in the 4.x manuals and in the 5.020 source; the current online guide says 10000. | Verilator `docs/guide` at tags v4.106, v4.228; `V3Options.h` at v5.020; current guide. State the version. |
| Logisim oscillation limit defaults to 1,000 | **Confirmed.** "The default of 1,000 ... number of clicks of the internal hidden clock (a simple gate takes just one click)"; the manual also says it may report false oscillation on very large circuits. | Logisim 2.7 docs, Simulation tab and "Oscillation errors". |
| Digital oscillation handling | **Verified in source.** Default limit 1,000 micro-steps (`oscillationDetectionCounter = 1000`), then 100 more steps collecting the oscillating nodes, then an error ("seems to oscillate"). An optional `setRecoverFromOscillation` mode introduces random-order noise ("use with extreme care ... covers bugs ... very slow"). | `Model.java`, Digital 0.31 and current master. |
| Digital's evaluation model | **Documented by its author:** without noise, "the steps of the model are calculated in a synchronized way ... you can observe oscillations in the model, which makes it impossible to start the model. So a RS-FF typically does not start because of oscillations." With noise, nodes are updated in random order. | Class comment of `Model.java`. This also explains why gate-level latch designs such as the tv80 export fail to start in Digital: observed directly, the limiter raises "Logic seems to oscillate" at the first vector and `errorOccurred` closes the model without throwing to the caller. |
| VCS and Xcelium defaults | Not verified; do not state numbers. | - |
| ModelSim `IterationLimit` | Previously "verified from forum quotes", not from the manual; cite the manual of the version used. | - |

### 0.3 New prior art found (important for the novelty claims)

1. **Maurer, US Patent 5,856,933 (priority 3 June 1994, filed 1997, granted 5 Jan 1999) and US 6,131,081 (divisional, filed 1998, granted 10 Oct 2000), "System and method for digital simulation of an electrical circuit", University of South Florida; both lapsed in 2011 for unpaid maintenance fees.** Both were read in full on 2026-10-21 (Google Patents text); the detailed comparison is in 0.5. They describe, for the same eight gate types (AND, NAND, OR, NOR, XOR, XNOR, NOT, BUFFER): a per-gate **count of inputs at the dominant value**, incremented or decremented on each input change; AND/NAND, OR/NOR, XOR/XNOR and NOT/BUFFER processed identically with **output inversion ignored during counting and applied later**; and **XOR, XNOR, NOT and BUFFER handled by input change events alone** ("any change in an input ... implies a change in the output"). This is the same family as SIMA. It also contradicts the statement in sections 1, 2.2.A and 6 that classical literature could not handle XOR/XNOR by counting.
2. **P. M. Maurer, "Event driven simulation without loops or conditionals", ICCAD 2000, pp. 23-26 (DOI 10.1109/ICCAD.2000.896445). Read in full on 2026-10-21** (four pages, the ICCAD version). Summary in 0.5. In short, all state is held as code addresses (EVCF, "Event-Driven Conditional-Free"), explicitly borrowed from virtual-function tables in place of type codes. Conditional-free event-driven evaluation is therefore prior art; Darion reaches it arithmetically instead of through indirect jumps.
2b. **Maurer's earlier papers behind the patents** (found through the 2000 paper's references; metadata checked against Crossref, content not read): "The Inversion Algorithm for Digital Simulation", ICCAD 1994, pp. 258-261, DOI 10.1109/ICCAD.1994.629776 (the paper version of the patents; the 2000 paper lists pp. 259-61); "The Shadow Algorithm: a scheduling technique for both compiled and interpreted simulation", IEEE TCAD 12(9):1411-1413, 1993, DOI 10.1109/43.240088 (the 2000 paper misprints it as V11 No 12); "Unit delay simulation with the inversion algorithm", ICCAD 1996, pp. 412-417, DOI 10.1109/ICCAD.1996.569831. **Cite the 1994 Inversion paper as the primary source for counting with deferred inversion**, with the patents as supporting references.
2c. **A. S. Teiche (Apple Inc.), US Patent 10,331,830 B1, "Heterogeneous logic gate simulation using SIMD instructions", filed 13 June 2016, granted 25 June 2019. Read 2026-10-21 (abstract, summary and the shuffle and popcount embodiments).** In a compiled (oblivious) simulator, up to 16 gates of *different* types are evaluated by one SIMD instruction:
   - Sum the gate's inputs (1 = true), add a per-type "operator value", then use the result as an index into a lookup table (`VPSHUFB`) or as the operand of a population count.
   - The tables cover NOR/NOT, AND, OR/BUF, NAND, XNOR and XOR for 2-input gates, with 4-state variants.

   **This is prior art for branch-free, count-based evaluation of mixed gate types, and must be cited.** It differs from SIMA in the following ways:
   - Its count is recomputed from all inputs at every evaluation, where SIMA's is a seed-relative count updated incrementally in O(1) per input change through the per-edge cached contribution.
   - It selects the type through a table offset, where SIMA uses the seed, a mask (0xFF existence, 0x01 parity) and an invert bit, with no table.
   - It is compiled and SIMD-batched, where SIMA works inside an event-driven, scalar propagation loop.
   - Its examples use 2-input gates, where SIMA supports any fan-in up to 255.
   - Gate values live in registers within a compiled block, where SIMA keeps every output in the gate record, readable through the API.

   Found by a targeted search on 2026-10-21; no source combining an incremental seed-relative count with a single mask/invert rule in an event-driven simulator was found.
3. **Driesen and Hölzle, "The direct cost of virtual function calls in C++", OOPSLA 1996, pp. 306-323 (DOI 10.1145/236337.236369), and "Accurate indirect branch prediction", ISCA 1998 (SIGARCH CAN 26(3):167-178, DOI 10.1145/279361.279380).** The cost of virtual dispatch and its dependence on indirect-branch prediction are established results. The OOP-versus-flat attribution in Claim 13 is a measurement in a new domain, not a new phenomenon.
4. **Maurer, "Is compiled simulation really faster than interpreted simulation?", ICVD 1996, pp. 303-306 (DOI 10.1109/ICVD.1996.489615).** Closely related to the crossover between compiled and event-driven simulation; read it before claiming the code-footprint explanation.
5. **Related interactive / programmatic tools not yet cited:** PyRTL (Clow et al., "A Pythonic approach for rapid hardware prototyping and instrumentation", FPL 2017, DOI 10.23919/FPL.2017.8056860; Python-embedded, instrumentation framework, simplicity over performance), cocotb (drives an external HDL simulator from Python through VPI/VHPI/FLI), DigitalJS (Materzok, "DigitalJS: a Visual Verilog Simulator for Teaching", 8th Computer Science Education Research Conference, 2019, pp. 110-115, DOI 10.1145/3375258.3375272), and Digital's own `Model` API (internal, not a supported public API).

### 0.3b Reference reading status, complete list (2026-10-21)

**A. Read (full text or the relevant sections):**
- Maurer US 5,856,933 and US 6,131,081 (full); Maurer ICCAD 2000 (full); Teiche/Apple US 10,331,830 (shuffle and popcount embodiments).
- Beamer and Donofrio, DAC 2020 (ESSENT), open copy on eScholarship. Relevant points:
  - ESSENT assumes the design is acyclic after preprocessing; combinational loops are merged into an SCC "supernode" re-evaluated until convergence (supports the sweep comparison, Claim 5).
  - It triggers partitions with a branch-free OR-reduction (related to Darion's branch-free enqueue; cite it).
  - It argues that per-signal activity tracking costs more than it saves and coarsens to partitions of 10-100s of elements. Darion keeps per-gate granularity cheap through a contiguous array and a flag test: a design difference to state.
  - Reports 1.5-29.3x over a leading open-source and an industrial simulator.
- Driesen and Hölzle, OOPSLA 1996 (abstract and introduction, copy on aminer). C++ programs spend a median 5.2% of their time in dispatch (13.7% "all virtuals"), and the overhead is "likely to increase moderately" on future processors. Darion's ~2x per-gate dispatch cost is consistent: a gate evaluation is tiny, so dispatch dominates it.
- Clow et al., FPL 2017 (PyRTL, introduction). A Python HDL for design, simulation, tracing and testing; "simplicity, usability, clarity and extensibility, rather than performance or optimization, are the overarching goals".
- **NEW: Shiple, Brayton, Berry and Sangiovanni-Vincentelli, "Logical Analysis of Combinational Cycles", UC Berkeley ERL Memorandum UCB/ERL M02/21, 24 June 2002** (open, relevant sections). It presents:
  - Brzozowski and Seger's ternary simulation: TernSim-A and TernSim-B each "converge in at most m steps" by monotonicity.
  - Malik's algorithm: topological rounds, "convergence is guaranteed within k rounds, where k is the number of feedback vertices".
  - Brzozowski and Seger's Theorem 6: a binary network with m bounded delays may need up to (2^m − 2)·D time to pass its transients.
  - **Must be cited next to V+1/2V.** Linear bounds are known for monotone ternary *analysis*; the known general bound for binary settling is exponential, which supports "2V cannot be proven". Darion's contribution is a live-size cutoff in a binary simulator with a non-fatal handoff, not the existence of linear bounds.
- Tool documentation and source: Digital `Model.java` 0.31; the Logisim docs; the Verilator guide; GHDL docs (`--stop-delta`, 5,000); the Vivado error text (10,000).

**B. Known through a reliable secondary source (cite only for what that source supports):**
- Malik 1994: via Shiple et al. 2002 and Edwards 2003's summary (three-valued simulation decides combinational cycles).
- Maurer 1994 Inversion: via the patents, which share its text.
- Driesen and Hölzle ISCA 1998: via the UCSB tech report 1997-19 abstract (two-level indirect-branch predictor, 9.8%/7.3% misprediction).
- EPICS: Mingjun Wang, ..., Huawei Li (ICT, Chinese Academy of Sciences, and CASTEST), "EPICS: Efficient Parallel Pattern Fault Simulation for Sequential Circuits via Strongly Connected Components", DAC 2025, pp. 1-7, DOI 10.1109/DAC63849.2025.11132928. Closed access (Unpaywall and Semantic Scholar: no open copy, no arXiv version, checked 2026-10-21). Full abstract read:
  - Parallel-pattern *fault* simulation of sequential circuits (ISO 26262 coverage); 5.94x over a commercial tool.
  - Simple loops are compiled into larger nodes; for large SCCs, "loop entrance nodes" are selected "based on indegree analysis", with lazy propagation for internal nodes; compiled and event-driven simulation are mixed.
  - *Closest point to Darion:* in-degree-based entry selection resembles Darion's forced placement when Kahn's sort stalls. The difference to check in the full text: EPICS does it per identified SCC (static SCC analysis first), Darion does it globally with no SCC identification. Until the full text is read, describe EPICS only by its abstract. *Status 2026-10-21:* the author could not obtain the PDF (paywalled); cite from the abstract only. Safe wording: "EPICS [wang2025epics] targets parallel-pattern fault simulation of sequential circuits; it compiles simple loops into larger nodes and, for larger SCCs, selects loop entrance nodes by in-degree analysis, mixing compiled and event-driven simulation." Do not state how EPICS identifies SCCs, its iteration limits, or its loop-handling cost, since the abstract does not say.

**A+. Maurer, "The Inversion Algorithm for Digital Simulation", ICCAD 1994, pp. 258-261: read in full on 2026-10-21 (4 pages, ACM copy).**
- Same content as the patents: dominant-value counting for AND/NAND/OR/NOR; XOR/XNOR/NOT/BUFFER as "trivial" (any input change implies an output change); net values eliminated; INCREMENT and DECREMENT routines toggling a pointer; shadows per fan-out branch; NOT/BUF elimination; homogeneous and heterogeneous collapsing; LECSIM queues; the same ISCAS85 table on a SUN IPC.
- **New fact: Maurer credits the counting algorithm to D. Schuler, "Simulation of NAND Logic", Proceedings of COMPCON 72, Sept. 1972, pp. 243-245.** Not indexed in Crossref or found online. Cite it as "[Schuler 1972], as described in [Maurer 1994]".
- Its "traditional" counting procedure branches on the input value (`if Value.of.X = Dominant.Value.of.G then increment else decrement`) and then on the count (`if Count = 1` / `if Count = 0`). This is the clearest published baseline for SIMA:
  - Maurer removes the value branch with alternating code pointers, and removes evaluation by never storing values.
  - SIMA removes the value branch arithmetically, with `(new == edge.seed) - edge.last`.
  - SIMA replaces the count tests with one masked AND, while keeping every value.
  Use the 1994 pseudocode as the "before" in the paper's SIMA figure.
- The paper explicitly calls oblivious levelized compiled-code simulation "the primary competition". It does not handle unknown values or loops beyond LECSIM's ("asynchronous cyclic circuits" may need more than one pass, per the patents).

**A++. Fleurkens, "Interactive Modelling and Simulation of Heterogeneous Systems", PhD thesis, TU Eindhoven, 1996, DOI 10.6100/IR456563 (ESCAPE). Read in full on 2026-10-21. Closest prior art for Darion's *positioning*.**
- An event-driven simulator embedded in a graphics editor, sharing one address space. There is no netlist compilation: edits update the simulation model incrementally ("re-simulated without perceivable delay").
- The design can be modified at run time, including fault injection during simulation. It has animation, discrete event monitors, and an API plus a text inter-tool protocol (master and slave modes).
- **Thesis statement 3 (Dutch "stelling", translated): "Using an interactive design and/or simulation system need not come at the cost of the performance of the simulator itself."** This anticipates Darion's "bridge" claim as a claim. Darion must cite ESCAPE and must not present "interactive without losing speed" as a new idea.
- *Difference from Darion:* ESCAPE is a system/RTL-level multi-model simulator (LISP-like HDL, C models, Petri nets, data-flow graphs, PLATO co-simulation). It has no gate-level data-oriented engine, no SIMA-like rule, no live-size oscillation budget, no sweep with runtime back-edge handoff, and no measured OOP-versus-flat attribution. Darion's mechanisms are unaffected.
- *Useful numbers:* monitors cost 2.3-6.3% (Table 2.1), against Darion's changed-gate queue at 0.995-1.004x. Animation nearly doubles CPU time (Table 4.2: 5.0 to 9.4 s), but that includes drawing, which Darion does not measure, so compare engine-side costs only.
- It states that "a compiled simulator can better exploit a cache in a computer architecture than an event driven simulator", the motivation Darion's data-oriented design answers.
- *Secondary confirmations:* LECSIM [Wan90] "compile[s] asynchronous circuits by identifying strongly connected components" (supports Claim 5's comparison). It also cites Maurer, "Two New Techniques for Unit-Delay Compiled Simulation", TCAD 11(9):1120-1130, 1992, for oblivious simulators being limited to zero or unit delay.
- *Related ESCAPE papers (not read):* Fleurkens and Jess, "ESCAPE: A Flexible Design and Simulation Environment", SASIMI '93, pp. 277-288; Fleurkens, "Interactive System Design in ESCAPE", IEEE Workshop on Rapid System Prototyping 1993, pp. 108-113.

**A+++. Wang and Maurer, "LECSIM: A Levelized Event Driven Compiled Logic Simulator", USF Technical Report DA-19, 1988 (the tech-report version of DAC 1990). Read in full on 2026-10-21 (14 pages). Cite the DAC 1990 paper; check that the DAC text keeps Fig. 5 and the 2^m+1 rule before quoting them.**
- *Preprocessing:* SCCs found by DFS; "the feedback paths in each SCC are identified. By breaking the feedback paths in the circuit, LECSIM is able to assign each gate a level."
- *Small SCCs* (no nested SCCs) are compiled into one code block with local iteration until stable. The cap is **2^m+1 iterations for m feedback arcs**; for large m, or SCCs containing latches, a user-specified default. Exceeding it calls `unstable_error()`.
- *Large SCCs, top-level loop control (Fig. 5):* one queue per level; inserting a block into a level lower than the current one sets `unstable = 1`, and the whole level scan repeats until stable or a user-specified iteration limit. **This is the same runtime test as Darion's `target <= curr`**, so Darion must cite it and not claim the test. Darion's response (event-driven handoff on the same data, live-size budget, non-fatal promotion) and its preprocessing (no SCC/feedback-arc analysis) remain different. Updated in the novelty table and Claim 5.
- *Oscillation bound:* LECSIM's static bound is exponential in feedback arcs (2^m+1), consistent with Brzozowski and Seger's exponential binary bound; it has no size-linear budget. Context for V+1/2V (Claim 3a++).
- *Quotes useful for the paper:*
  - "A primitive gate ... needs only two or three instructions for evaluation, but it may take hundreds instructions to schedule its evaluation": scheduling, not evaluation, dominates. Darion's flag-test enqueue answers this.
  - Compile time is "the major problem": 7.4 to 553 s on ISCAS85 (Fig. 9) against 0.9 to 25 s parse for the interpreter, so LECSIM "is inefficient for the applications where only a few input vectors are simulated after each circuit modification". This is exactly the interactive case; supports Claim 8 (turnaround) as a long-known trade-off that Darion addresses, not a new observation.
  - Levelized compiled simulation loses to event-driven interpretive simulation only below about 1% activity (citing HSS); LECSIM beats FHDL below 10-19% activity. Context for Darion's activity discussion.
  - "We have not yet fully examined LECSIM's performance on sequential circuits."
- Two-valued, zero-delay; no unknowns. Event insertion and dispatch about 12 machine instructions (MC68020), dispatch by computed jump (threaded code).

**A++++. Chilimbi, Davidson and Larus, "Cache-Conscious Structure Definition", PLDI 1999, pp. 13-24. Read in full on 2026-10-21.** Note: this is the *sibling* of the paper already in the BibTeX (Chilimbi, Hill and Larus, "Cache-Conscious Structure Layout", pp. 1-12, still unread). Both can be cited.
- Internal organisation of a structure: hot/cold *structure splitting* (Java, automatic) and *field reordering* by temporal affinity (C, the `bbcache` tool).
- Results: splitting cut L2 miss rates 10-27% and improved run time 6-18% beyond co-location (co-location alone 16-29% fewer L2 misses, 10-20% faster). Field reordering in SQL Server 7.0: 2-3%.
- Conclusion: "structure layouts are better left to the compiler or runtime system".
- *Relevance:* the standard citation for hot-field packing, which is what the 24-byte `CPP_Gate` does by hand. Its gains are layout gains of 2-28%, the same order as Darion's harness finding that layout is a small effect next to dispatch and the evaluation rule unless memory is scattered (Claim 13). Cite it as the layout baseline; the vtable/dispatch attribution remains Darion's measurement.

**Not the paper we needed:** Ullrich and Lückerath, "An Introduction to Discrete-Event Modeling and Simulation", Simulation Notes Europe (about 2017). A general discrete-event tutorial (future event list, Surfside Java framework), not Ernst G. Ulrich's 1969 CACM paper. Nothing in it bears on Darion; do not cite.

**A+++++. Ulrich, "Exclusive Simulation of Activity in Digital Networks", CACM 12(2):102-110, 1969, DOI 10.1145/362848.362870. Read in full on 2026-10-21.**
- *Selective trace:* only about 1% of elements are active at once (citing Case et al. 1964); following "paths of activity" saves about 88% of run time at a 12x overhead factor. Origin citation for event-driven gate simulation.
- *Wave view:* active set A1 drives destination set B1; the responding subset becomes A2, "and thus a new wave of activity is started", until an empty set ends it. This is the conceptual ancestor of Darion's wave-counted `propagate` (and of counting waves against a budget), though Ulrich sets no wave limit.
- *Element model:* a descriptor cell holds the type code, the full input/output bit pattern and a **schedule marker** set when the element is scheduled. That is prior art for Darion's per-gate "already queued" flag test; cite it. Behaviour is a per-type subroutine selected by the type code (the dispatch-by-type that SIMA removes).
- *Scheduling:* the Δt-loop, a circular table of time slots with modulo-L insertion and constant cost per event, i.e. the timing wheel. Fan-out lists are circular so a whole fan-out is one event.
- *Feedback:* with real element delays, "manual preprocessing and/or extra programming to detect and handle feedback loops is unnecessary", and "unrealistic zero-delay-element simulations are avoided, and the possibility of program-induced feedback loops is therefore eliminated".
  - *Use in the paper:* event-driven simulation never needed loop analysis (Ulrich 1969); levelized simulation did (LECSIM: SCCs, feedback-path breaking, iteration caps). Darion's sweep keeps levelized order without the analysis by falling back to the event-driven engine on back edges. That bridges the two lines of work rather than claiming loop tolerance as new.
- *Stated disadvantage:* every element must be initialised to consistent states before simulation starts.
- Clocked systems: skip-and-scan of the wheel; clocked elements rescheduled to the next clock edge.

**C. Not read, worth reading before submission (get them in a browser or through the university library):**
- Chilimbi, Hill and Larus 1999, "Cache-Conscious Structure Layout" (the paper actually in the BibTeX; optional now that the sibling is read).
- Edwards 2003 (Columbia, browser only).
- EPICS 2025.
- Driesen and Hölzle ISCA 1998.
- Burch 2002 (Logisim).
- DigitalJS 2019.
- Maurer 1996 (compiled versus interpreted).
- Maurer 1993 (Shadow).
- The Abramovici textbook chapter on simulation (library).

**D. Recommended to drop unless a specific use appears:**
- Bryant 1984 (switch-level, not related to any claim).
- Agrawal-Tutundjian-Dally 1989 and Agrawal-Dally 1990 (unread, relevance unknown).
- Szygenda and Thompson 1975 (only if the history of table-driven simulation is discussed).
- Riedel and Bruck 2003, and Shiple et al. ISCAS 1996: background only; Shiple et al. 2002 covers the same ground better.
- Maurer 1996 unit delay (unless delays are discussed with Maurer).

**E. Also found, optional:** two 2025 Chinese patents (CN 121981036 A, CN 121981029 A) on SCC-aware simulation (Tarjan/Kosaraju identification, SCCs compiled into nodes, the rest event-scheduled). Static loop analysis again; they support the sweep comparison if a reviewer asks about recent work.

### 0.4 What this does to the novelty claims

| Claim | Status after the check |
|---|---|
| SIMA (one incrementally kept seed-relative count, one mask/invert rule for eight gates, type-agnostic edge update) | **Novel formulation (revised 2026-10-21 after reading Maurer 1994-2000 and Teiche/Apple 2019 in full).** Counting at a dominant value is Maurer's and classical, and branch-free mixed-type evaluation from a sum plus a table is Teiche/Apple's (compiled SIMD). No source found encodes the basis as (seed, mask, invert) over one incremental count, answers existence and parity with one masked AND, or keeps the edge update free of gate type; it is also what makes the homogeneous data-oriented layout possible. Measured benefit: 1.35-1.5x over a type switch (harness), 1.1-1.7x on the evaluation step (engine). Wording: "to our knowledge"; see Paper_Notes 2.2 "What SIMA really is". |
| Conditional-free gate evaluation | Prior art (Maurer 2000); different mechanism. |
| Data-oriented layout, cache-conscious structures | Prior art as a technique (Chilimbi 1999; DOD practice). Novelty is the measurement in gate-level simulation. |
| Virtual-call cost, `switch` not a fix, predictor effects | Known phenomena (Driesen and Hölzle). Yours: the controlled attribution on 24 real netlists plus synthetic sweeps, and the repeated-sequence effect on the target predictor (a supported hypothesis, mechanism not probed). |
| Bounded topological sweep with back-edge escape | **Distinct mechanism, narrowed after reading LECSIM in full (2026-10-21).** The runtime back-edge test itself is *not* new: LECSIM's top-level scheduler sets an `unstable` flag when a block is inserted into a level already scanned (`index < current_level`) and re-runs the level scan (TR DA-19, Fig. 5). What remains distinct: (1) LECSIM can only assign levels after DFS SCC detection and breaking of the identified feedback paths; Darion uses one Kahn sort with forced breadth-first placement, no SCC or feedback-arc analysis. (2) LECSIM answers a back edge with another full levelized pass, capped by 2^m+1 (small SCCs, m feedback arcs) or a user-specified limit, then an error routine; Darion hands the back edge to the event-driven engine on the same data, under the live-size V+1/2V budget, with non-fatal timed promotion. (3) LECSIM must recompile after every edit (its own stated weakness); Darion needs no re-analysis. Verilator (fatal UNOPTFLAT/"didn't converge") and EPICS 2025 (static SCCs) as before. Measured: a live ring in b15/b19 under sweep, promoted, 0 output mismatches afterwards (Claim 5). Claim it "to our knowledge", and cite LECSIM for the runtime back-edge test. |
| Live-size wave budget (V+1 / 2V) and non-fatal promotion | **Novel as a simulator mechanism (revised 2026-10-21).** Every tool checked uses a fixed constant: Logisim 1,000; Digital 1,000 micro-steps; Verilator `--converge-limit` 100 or 10,000; ModelSim `IterationLimit` 5,000 or 10M; Vivado xsim 10,000 ("Iteration limit 10000 is reached"); GHDL `--stop-delta` 5,000 (GHDL docs). Most stop with an error; Digital also has an optional noise mode. Targeted searches found no simulator that derives its cutoff from the circuit's size. Darion's cutoff is the live gate count, maintained in O(1) under editing. It is proven never to fire on acyclic logic, and firing certifies that a real feedback loop was traversed. Non-convergence is promoted to timed simulation instead of stopping. What is elementary and must not be claimed as new: that acyclic zero-delay logic settles within its depth (the basis of levelized simulation). The contribution is using the live size as a self-scaling, configuration-free, sound cutoff, together with the non-fatal handoff, measured: 0 false alarms on 30 acyclic circuits up to 101,859 gates, and a real ring caught in 0.92 ms on 356k gates (claims doc 3a+). The 2V sequential tier stays a heuristic. |
| Interactive, observable engine with an API | Logisim, Digital, DigitalJS, PyRTL and cocotb occupy neighbouring points; the measured result (observation cost under 2%, microsecond calls) is yours. |

Overall (revised 2026-10-21, after reading Maurer 1993-2000 and Teiche/Apple 2019 in full and surveying simulator oscillation limits): the general ideas have ancestors (counting at a dominant value, data-oriented layout, levelized settling), but three mechanisms are novel to our knowledge:
- the SIMA formulation;
- the type-agnostic O(1) edge update;
- the live-size, edit-tracking V+1 oscillation budget, with its soundness proof and non-fatal handoff.

The measured reversal of Maurer's dispatch trade-off on modern CPUs is a finding in its own right. Together with the verification, the observation-cost results and the case study, this is a design paper with original mechanisms and the evidence for them. See Paper_Notes section 1b.

### 0.5 SIMA versus Maurer's inversion algorithm (patents read in full, 2026-10-21)

**What Maurer describes** (US 5,856,933 and US 6,131,081 share one description; the divisional changes only the claims):
* A *zero-delay, two-valued, levelized* event-driven simulator built on LECSIM (one queue per level, doubly linked lists). The evaluation used C code generated per circuit ("compiled code"); the text says the routines could instead come from a precompiled library.
* **Principle: a gate is scheduled only if its output is guaranteed to change.** A gate's "simulation" is then just an inversion of its output. The test of whether the output changes is moved into *event processing*, per fan-out branch.
* **AND/NAND/OR/NOR:** a count of inputs at the *dominant* (controlling) value. An increment that makes the count 1, or a decrement that makes it 0, means the output changes. AND and NAND are processed identically, as are OR and NOR (the inversion is ignored).
* **XOR/XNOR/NOT/BUFFER:** every input change implies an output change, so the gate is scheduled. For XOR/XNOR, a second change before simulation *de-schedules* it: parity is tracked by queue membership, not by a count.
* **No tests in the hot path:** each fan-out branch ("shadow") holds a pointer to its event routine. INCREMENT and DECREMENT overwrite that pointer with each other, so which operation comes next is held in a code address ("Shadow Technique"; the ICCAD 2000 paper generalises this to "no loops or conditionals").
* **Net values are eliminated** except for nets the user monitors. Monitored nets get an extra fan-out branch that computes their value. Before simulation, consistent initial values come from one zero-delay pass.
* Further optimisations rewrite the circuit: NOT and BUFFER gates are removed, and homogeneous and heterogeneous connections are collapsed (weighted increments such as 0.5/0.25, or a "layered" form).
* Evaluation: ISCAS85, 5,000 random vectors, checked against a levelized compiled-code simulator; about parity with it at 52–64% activity, and faster on c7552.
* **Claims:** the independent claims require either removing all NOT gates, collapsing connections, eliminating net values except user-visible ones, or only scheduling gates whose outputs will definitely change. US 6,131,081 also claims "debugging the initial design" with such a simulator. Darion does none of the circuit rewriting and keeps every net value; in any case both patents have lapsed. (This is a technical comparison, not a legal opinion.)

**Feature by feature:**

| Aspect | Maurer (1994 priority) | Darion SIMA | Same / different |
|---|---|---|---|
| Counting for AND/NAND/OR/NOR | count of inputs at the dominant value | `logic` = count of inputs equal to `seed` (0 for AND/NAND/NOT, 1 for OR/NOR/XOR/XNOR/BUF); for AND/NAND/OR/NOR, `seed` is the dominant value | **same idea** |
| Inversion handled separately | AND≡NAND etc. during processing; output inversion ignored | `flags & 1` invert bit applied in the same expression | same idea, different place |
| XOR/XNOR | every input change implies output change; schedule/deschedule by queue membership | parity of the ones-count, `logic & 1` (mask `0x01`) | **different mechanism**; Maurer has no XOR count. Do not claim "first to handle XOR with counting" until older work (e.g. Abramovici) has been read |
| Per-fan-out-branch state | each branch remembers whether its next event increments or decrements (via a code pointer) | each edge (`Profile`) caches its last contribution `logic` and the target's `seed`; update is `target.logic += curr - profile.logic` | **close analogue**: both keep per-edge state so an update is O(1) without reading other inputs. State this explicitly |
| Conditional-free hot path | yes, by self-modifying routine pointers and generated code | yes, arithmetic: one rule `bool(logic & mask) ^ (flags & 1)` for all eight types; enqueue is branch-free (`size += mark==0 & changed`) | same goal, **different mechanism** (data instead of code addresses) |
| When the output is decided | at event processing; gate scheduled only if output will change | target re-evaluated on every incoming edge and its output compared with the stored one; enqueued only if it changed | different split of work |
| Net values | eliminated except monitored nets | **every gate's output is stored and readable at any time** (the API reads any gate; changed gates go to the visual queue) | **key difference**, and the one that matters for Darion's purpose (observability) |
| Circuit rewriting | NOT/BUF removal, connection collapsing | none: the simulated netlist is the user's netlist, one-to-one | different (Darion trades some speed for observability) |
| Values | two-valued; needs consistent initial values | 0, 1, unknown: a gate with unconnected inputs (`inputlimit` > 0) outputs unknown, and an edge carrying unknown sets its target to unknown (outside the counting rule), so the circuit can start from all-unknown | different |
| Timing | zero-delay (unit/multi-delay "may require special procedures") | zero-delay waves plus a timed priority queue with load-dependent delays and oscillation promotion | different |
| Implementation | generated C per circuit, linked lists | one prebuilt engine, 24-byte structs in one array, topologically reordered; no code generation | different |
| Evidence | one table, ISCAS85, SUN-4 | ISCAS85/89, ITC99, EPFL, OpenCores; Icarus/Verilator oracles; ablation of the rule versus `switch` | different |

**Novelty statement for SIMA (author's framing, checked 2026-10-21): the novelty is how the count is kept and read, not counting.**
- Claim: "To our knowledge, SIMA is the first formulation in which an incrementally maintained, seed-relative input count and a single mask/invert rule evaluate all eight elementary gate types without a type-dependent branch inside an event-driven simulator."
- Plain wording (author's): no lookup table, no special machinery. Each gate has a one-byte count (`logic`) of only the inputs equal to its `seed`, and three configuration values (`seed`, `mask`, invert bit in `flags`). Each fan-out edge caches the target's seed and its own last contribution, so an input change is `target.logic += now - before`, O(1), without reading other inputs. All eight types are evaluated by `bool(logic & mask) ^ (flags & 1)`. Paper sentence: "Each gate keeps a single one-byte count of the inputs equal to its seed value, updated in constant time from per-edge state, and all eight gate types are evaluated by one arithmetic expression, bool(count & mask) ^ invert, with no lookup table and no type-dependent branch."
- Cite as related: Maurer (counting with deferred inversion; conditional-free through code addresses; XOR by events) and Teiche/Apple (branch-free count-plus-table evaluation of mixed types in compiled SIMD simulation).
- Scope the "no branch misses" statement to the evaluation step. The hot loop keeps two branches: the unknown-value check and the unconnected-input check. Both are almost always predictable; the misprediction counts in Claim 13 are the evidence.

**What to write in the paper:**
1. "Darion's gate evaluation follows the counting approach of Maurer [patents; ICCAD 2000]: a per-gate count of inputs at a designated value, updated in O(1) from per-edge state, with output inversion separated from the count."
2. "It differs in three ways: (a) it keeps every gate's value, so any gate can be read during simulation, where Maurer removes non-monitored net values and rewrites the circuit for speed; (b) a single arithmetic rule with a parity mask covers all eight gate types, instead of per-type event routines, and the engine also carries an unknown value; (c) it uses a fixed prebuilt engine over a flat array, not generated code."
3. "We do not claim the counting idea; we measure what the uniform rule buys over a type switch in the same engine (Claim 1) and over virtual dispatch (Claim 13)."

**The ICCAD 2000 paper (EVCF), read in full on 2026-10-21:**
* **Mechanism.** Every piece of state is a code address:
  * A net's event structure (one per fan-out branch) alternates between `EVUP` and `EVDN` routines, so the net's value is never stored.
  * A gate's dominant-input count is encoded by which routine pair (`UP0/DN0`, `UP1/DN1`, `UP2/DN2`, ...) its `Up`/`Down` fields point to: "the routines themselves are used as the counter, so no explicit count is maintained".
  * Whether an event is queued is encoded by `Schedule` pointing to `QUEUE` or `DEQUEUE`. A second change cancels the queued event.
  * Monitored nets get a "Net Monitor" gate whose routines write ASCII '0'/'1' straight into the output vector.
  * The kernel is only assignments and computed gotos, and needs some assembly language. It has no loops or conditionals except in input-vector parsing.
* **Gate types.** AND/OR/NAND/NOR use the count routines; XOR, XNOR, NOT and BUFFER use a "pass-through" routine that propagates every event. Same as the patents: no parity count for XOR.
* **Model.** Zero-delay, two-valued, on the LECSIM levelized queues. Unit/multi-delay and X/Z are said to be easy extensions but are not shown.
* **Evaluation.** ISCAS85, 50,000 random vectors, 300 MHz UltraSPARC-II. Overhead was removed by subtracting an all-zero-vector run. EVCF is 5-10x faster than a conventional event-driven simulator (60x on c6288) and about equal to the Inversion Algorithm (1994), described as "considerably more versatile".
* **The important point for this project: Maurer's design argument runs the other way from Claim 13.** Section 2 motivates EVCF from object-oriented programming. A gate's type code is replaced by "a table of virtual functions", because "the function addresses are more useful than a plain type code, because we can branch to them directly … No decoding of the type-code is necessary." EVCF then pushes this to the limit: every event executes one or more indirect jumps.
  * Darion measures the opposite trade-off on a modern out-of-order CPU. Per-gate indirect dispatch (virtual call) costs about 2x per edge even with no mispredictions, and up to 2-3x with them. A type switch, also an indirect jump, recovers little. Replacing dispatch with data (one arithmetic rule over flat records) wins (Claim 13).
  * The two results are not in conflict. On a 2000-era in-order SPARC, a type decode cost about as much as a jump, and an indirect jump was cheap relative to the work. On a deeply pipelined, speculative CPU, an unpredictable indirect jump costs a pipeline flush and blocks overlap between neighbouring gates.
* **What to write:** "Maurer [2000] replaced type decoding with code addresses, in the spirit of virtual dispatch, to remove conditionals; on a current out-of-order processor we find the opposite trade-off: per-gate indirect dispatch is the dominant cost, and a branch-free arithmetic rule over flat records removes it (Section 5.3)."
* **What not to write:** that EVCF itself would be slow today. EVCF was not implemented or measured here; that is a hypothesis.
* **Other differences from Darion** (in addition to the table above): EVCF has no net values except monitored nets, while Darion keeps every value. EVCF needs per-circuit data with assembly-level code, while Darion has a fixed engine. EVCF's count is capped by the number of routines generated, while Darion's is an 8-bit counter (fan-in up to 255).
* **Possible related-work paragraph:** Maurer's line of work (Shadow 1993, Inversion 1994/1996, EVCF 2000) is the closest prior art to Darion's evaluation core. It shares the counting idea and the goal of a branch-free hot path, and differs in mechanism (code addresses versus arithmetic on data), in observability (values removed versus kept) and in hardware era.
* The Baylor technical report of the same title (handle 2104/5448) was not compared with this version.

---

## 1. Executive Summary: What was Discovered vs. Prior Art

In academic research, discovering foundational mechanisms independently from first principles is known as **convergent evolution**. The fact that the core mechanisms of Darion align with established literature validates their correctness.

The table below maps each mechanism in Darion to its historical origin and canonical literature in Electronic Design Automation (EDA):

| Darion Component | Historical Origin / Literature Reference | Canonical Publication | Primary Overlap | Darion's Evolution / Difference |
|---|---|---|---|---|
| **Single-Invariant Masked Accumulator (SIMA)** | **Input Counting Algorithm** (Controlling Value Counting) | M. Abramovici, M. A. Breuer, A. D. Friedman, *Digital Systems Testing and Testable Design*, 1990;<br>S. A. Szygenda & E. W. Thompson, *IEEE Computer 1975* | Incremental tracking of inputs to avoid $O(k)$ fan-in rescanning on each event. | • Tracks **one singular logic state** (`seed`) instead of multi-branch counters (`c_count`, `u_count`).<br>• Uses **bitwise mask** (`mask = 0x01`) to extract **XOR/XNOR parity** from the ones-count. (Prior art: Maurer's patents US 5,856,933 / 6,131,081 already handle XOR/XNOR by change events and defer inversion, see 0.3; this row describes an arithmetic variant, not a new idea.)<br>• Unifies all 8 gates into a single branchless ALU instruction: `bool(logic & mask) ^ (flags & 1)`.<br>• Zero vtables; all gates share one flat array and one evaluation rule. (In-place type change is a side effect: $O(1)$ within a seed family, $O(\text{fan-in})$ across families; see `Gate.retype`.) Novelty is modest: this is classical input counting with parity read from the low bit. |
| **Two-Tier Dynamic Oscillation Budgeting** | **DAG Depth, Delta Cycles, and Combinational Cycles** | S. Malik, *IEEE TCAD 1994*;<br>T. R. Shiple et al., *ISCAS 1996*;<br>P. Agrawal & W. J. Dally, *IEEE TCAD 1990*;<br>R. E. Bryant, *IEEE TCAD 1984* | Bounding zero-delay feedback loop propagation and delta cycle limits. | • Simulators use static iteration limits (Verilator's default `--converge-limit` is 100 and its failure is fatal; the limits of commercial tools are **not yet cited**, see the note in 2.1.C).<br>• Formal tools use expensive static ternary BDD/SAT cycle analysis [Malik 1994].<br>• **Tier 1 (Combinational / DAG):** the **$|V| + 1$ pigeonhole bound** is sound (no false positives on acyclic circuits) but loose: the true bound is circuit depth.<br>• **Tier 2 (Sequential 2-State Feedback):** **$2|V|$ is an unproven heuristic** (no counterexample found among 16,129 converging random cyclic networks).<br>• **Non-fatal promotion:** Seamlessly defers oscillating sub-cones to an asynchronous timed priority queue without crashing. |
| **Data-Oriented Microarchitectural Layout (DOD)** | **Data-Oriented Design & Cache-Conscious Structures** | M. Acton, *CppCon 2014*;<br>T. Chilimbi et al., "Cache-Conscious Structure Layout", *PLDI 1999* | Memory defragmentation and contiguous array packing to prevent cache misses. | • Strict **24-byte POD struct** (`static_assert(sizeof(CPP_Gate) == 24)`).<br>• Field order inside the first 8 bytes has no cache effect (one 8-byte word); do not claim it as a result.<br>• Kahn topological sort physically co-locates connected gates in RAM, improving prefetch locality.<br>• Zero heap pointers in UI communication; decoupled via raw integer indices. |
| **Dynamic Bounded Topological Sweep** (`sweep`) | **Levelized Compiled Simulation (LCS)** & **Levelized Event-Driven (LEDS)** | Z. Wang and P. M. Maurer, "LECSIM", *DAC 1990*; ("Hansen et al., TCAD 1999" removed: no such paper could be verified) | Topological evaluation of logic without dynamic heap queues. | • Unlike static LCS (Verilator), which evaluates $0 \dots N-1$ unconditionally, Darion sweeps a **dynamic bounded window $[\text{curr}, \text{threshold}]$**.<br>• In-place selective trace skips quiescent gates without queue overhead.<br>• **Back-Edge Escape:** Automatically detects cyclic feedback (`target <= curr`) and delegates to the wavefront engine. |
| **Double-Buffered Wavefront DES** (`propagate`) | **Selective trace (exclusive simulation of activity); wave view of activity** | E. G. Ulrich, "Exclusive Simulation of Activity in Digital Networks", *CACM 1969* | *Corrected 2026-10-21 after reading the paper:* Ulrich describes activity as waves (active set A1 → destination set B1 → responding subset A2 → ..., "until an empty subset terminates activity") and a per-element schedule marker against double scheduling. He implements it with a time-mapped Δt-loop (timing wheel) and a two-pass or one-pass procedure, **not** with ping-pong buffers. Cite him for selective trace, the wave view and the schedule marker; the two-buffer implementation is not his. | Pre-allocated raw pointer ping-pong buffers in pure Cython `nogil` with branchless enqueue logic. |
| **Inertial Delay "Shock Absorber"** | **Inertial Delay Glitch Filtering & Lazy Cancellation** | M. Abramovici et al. (1990);<br>Szygenda & Thompson (1975) | Discarding pulses narrower than gate propagation delay. | $O(1)$ timestamp invalidation (`if task.time < gate_clocks[origin]: return;`). Absorbs high-frequency transients and race-condition spikes in-place. |
| **Decoupled Visual-AOS Interface** | **Model-View Architecture in CAD** | C. Burch, "Logisim", *JERIC 2002*;<br>H. Neemann, "Digital", 2016 | Interactive schematic capture and live simulation. | Prior interactive tools suffer from Java/JS heap object overhead. Darion bridges a dynamic PySide6 GUI to a 24-byte C++ DOD engine via integer locations and a visual-queue deque. The core is single-threaded and cooperative (asyncio), so "lockless" is not a meaningful claim. |

---

## 2. In-Depth Comparative Analysis

### 2.1 The Oscillation Cutoff Bound: Pure Graph Theory vs. Sequential Feedback vs. EDA Industry Practice

The handling of zero-delay feedback loops and oscillation cutoff represents one of the most critical challenges in digital logic simulation:

#### A. The Graph-Theoretic Foundation: Pure Combinational Logic (DAGs)
In graph theory, it is a proven mathematical property that:
- Let $G = (V, E)$ be a Directed Acyclic Graph (DAG) with $|V|$ vertices.
- The longest possible simple directed path in $G$ consists of at most $|V| - 1$ edges, visiting at most $|V|$ distinct vertices.
- Under zero-delay Discrete-Event Simulation (DES), each simulation wave corresponds to one topological edge traversal along the causal dependency tree.
- In a worst-case linear chain ($G_1 \to G_2 \to \dots \to G_V$), the signal requires $|V|$ waves to traverse the $V$ gates. Quiescence is evaluated on wave $|V| + 1$, where the write queue is empty (`end_point == 0`).
- If a wavefront survives past wave $|V| + 1$, it visits $\ge |V| + 2$ vertices along a causal path. By the **Dirichlet Pigeonhole Principle**:
  $$\text{Causal Path Length} \ge |V| + 1 \text{ evaluations} \implies \exists \, v_i, v_j \in \text{Path} \text{ such that } v_i = v_j$$
- This guarantees with mathematical certainty that at least one vertex is visited more than once—meaning the wavefront has entered an active directed cycle.
- **Result:** $|V| + 1$ is the exact, minimal tight bound that guarantees **zero false positives on maximal-depth acyclic paths** while guaranteeing cycle detection.

#### B. The Sequential Reality: 2-State Feedback and Latch Stabilization ($2|V|$ Heuristic)
When simulating sequential circuits modeled at the gate level (e.g., cross-coupled NOR/NAND RS latches, transparent latches, gate-level master-slave D-FFs), the network is no longer a DAG—it contains physical feedback cycles.
1. **The Combinational Cycle Problem in the Literature:**
   - **Sharad Malik** (*IEEE TCAD 1994*, "Analysis of Cyclic Combinational Circuits") proved that cyclic circuits can behave combinationally (without true state storage) if they stabilize to a unique value for all input assignments. Malik utilized ternary simulation (0, 1, X) and Boolean function analysis to verify cycle stabilization.
   - **Thomas R. Shiple et al.** (*ISCAS 1996*, "Analysis of Combinational Cycles in Sequential Circuits") and **Stephen A. Edwards** (*DAC 2003*, "Making Cyclic Circuits Acyclic") demonstrated that cyclic circuits require bounded multi-phase unrolling to stabilize under 2-state and multi-state logic.
2. **Two-Phase Stabilization in 2-State Logic:**
   - In 2-state logic simulation, cross-coupled feedback latches stabilize through a **two-phase transition**:
     - *Phase 1 (Forward Excitation):* The triggering transition propagates through the primary gate.
     - *Phase 2 (Feedback Locking):* The inverted output propagates back across the cross-coupled edge to clamp the complementary gate.
   - For a sequential pipeline of depth $|V|$, each feedback stage may require up to 2 evaluation waves to settle into its steady-state.
3. **Darion's $2|V|$ Heuristic:**
   - To prevent premature cutoff during normal latch state transitions in sequential netlists, Darion defines an upper heuristic threshold of **$2|V|$** (`wave_multiplier = 2`).
   - Darion exposes both modes through `set_wave_mode("combinational")` ($|V|+1$) and `set_wave_mode("sequential")` ($2|V|$), defaulting to the robust $2|V|$ sequential threshold.

#### C. What Industrial EDA Simulators Actually Do (The Hardcoded Flaw)
Despite the formal graph-theoretic foundations, **commercial and open-source simulators do not use dynamic graph-dependent bounds**. Instead:
1. **Commercial Simulators (Synopsys VCS, Cadence Xcelium, Siemens ModelSim/Questa), verified findings:**
   - **ModelSim/Questa (verified from user-forum quotes of the manual and vsim messages):** the delta-iteration limit is a configurable setting (`IterationLimit` in `modelsim.ini`, or Simulate > Runtime Options); exceeding it is a fatal "iteration limit reached ... possible zero delay oscillation" error. The default is version dependent: older manuals say 5000, newer vsim messages say 10 million. Cite the manual of the version you use.
   - **Verilator (documented):** stops with a "didn't converge" error after `--converge-limit`. The default is 100 in the 4.x manuals and in the 5.020 source, and 10000 in the current online guide: state the version.
   - **Vivado xsim:** fixed 10,000 (its error text: "Iteration limit 10000 is reached. Possible zero delay oscillation detected").
   - **GHDL:** `--stop-delta=N` stops after N delta cycles at the same time, default 5,000 (GHDL documentation, "Simulation and runtime").
   - **VCS and Xcelium: not verified.** No vendor documentation of a default delta limit was found; do not state one. (Forum posts show zero-delay loops hanging or erroring in both, without numbers.)
   - The exact message text previously quoted here was not verified and has been removed.
   - The point that a fixed limit is wasteful on small circuits is reasonable for any fixed limit, but should be argued generically.
2. **Educational Simulators (Logisim, Digital)** (checked 2026-10-21, see 0.2):
   - **Logisim (verified, official documentation):** oscillation is detected by a fixed iteration cutoff, user-configurable in the Simulation tab, with a **default of 1,000** (the document also admits large slow-settling circuits can be falsely flagged). The earlier "150-step" figure was wrong.
   - **Digital (hneemann): verified in the source of `Model.java`.** Default 1,000 micro-steps, then 100 more while collecting the oscillating nodes, then an error; an optional recovery mode adds random-order noise. Its documentation also states that in the default synchronised mode an RS flip-flop typically does not start because of oscillations.

#### D. Darion's Novel Contribution: Non-Fatal Priority Queue Promotion
Darion couples its dynamic budget to a non-fatal execution handoff:
1. **Adaptive Dynamic Budget:** The wave limit is computed directly from the active gate count:
   $$\text{wave\_limit} = |V_{\text{active}}| \cdot \text{multiplier} + \text{offset}$$
2. **Seamless Timed Queue Promotion:**
   When `wave_limit == 0`, Darion **does not crash or abort**. Instead, the remaining wavefront in `read_queue` is promoted to a timed-delay task:
   $$\text{calc\_time} = T_{\text{global}} + D_{\text{gate}} + (D_{\text{fanin}} \cdot \text{fan\_in}) + (D_{\text{fanout}} \cdot \text{hitlist.size})$$
   *(where static $\text{fan\_in}$ is preserved in `CPP_Gate.reserved` to track full port load rather than remaining unconnected slots)*
   The cycling sub-circuit is deferred to an asynchronous discrete-event priority queue (`time_queue`), while the rest of the engine continues executing. This allows interactive circuits (such as ring oscillators, clock generators, or astable multivibrators) to simulate cleanly without crashing the visual canvas.

---

### 2.2 Low-Level Gate Evaluation: Classical Input Counting vs. Darion's SIMA Model

A low-level inspection reveals fundamental architectural differences between classical textbook "Input Counting" and Darion's implementation:

#### A. Classical Input Counting (Abramovici et al. 1990)
In classical EDA literature (Abramovici et al. 1990; Szygenda & Thompson 1975; *not* Ulrich 1969, who stores each element's full input bit pattern and has no counting; corrected 2026-10-21):
- Input counting relies on the existence of a **controlling value** ($c \in \{0, 1\}$)—an input value that uniquely forces the gate's output regardless of all other inputs ($0$ for AND/NAND, $1$ for OR/NOR).
- **CORRECTION (2026-10-21):** the earlier text here said that classical literature treated XOR/XNOR as incompatible with counting. That is not supported: Maurer's patents US 5,856,933 (1999) and US 6,131,081 (2000) process XOR, XNOR, NOT and BUFFER by input-change events alone and apply output inversion afterwards (see 0.3). XOR/XNOR have no controlling value, which is why they are handled by parity of changes or of a ones-count instead of a dominant-value count.
- Classical algorithms maintained separate multi-state variables (`c_count` for controlling values, `u_count` for unknown values) evaluated through multi-branch `if-else` conditional trees.

#### B. Darion's Single-Invariant Masked Accumulator (SIMA) Model
Darion unifies all eight elementary logic gates into a single algebraic parameter tuple:
$$\mathcal{G} = (\text{seed}, \text{mask}, \text{inv}) \in \{0, 1\} \times \{0\text{x}01, 0\text{xFF}\} \times \{0, 1\}$$

Where:
1. **`seed` (The Singular Invariant):** The gate tracks exactly **one** designated logic state (LOW or HIGH). The accumulator `logic` tracks strictly:
   $$\Delta \text{logic} = (v_{\text{new}} == \text{seed}) - (v_{\text{old}} == \text{seed})$$
2. **`mask` (The Functional Mode Selector):**
   - When $\text{mask} = 0\text{xFF}$: computes existential threshold saturation ($[\text{logic} > 0]$).
   - When $\text{mask} = 0\text{x}01$: computes parity extraction directly via the least-significant bit ($[\text{logic} \ \& \ 1]$).
3. **`inv` (The Boolean Dual Inverter):** Extracted from `flags & 1`. Inverts the functional output via bitwise XOR.

The entire Boolean basis evaluates through a **single, uniform branchless instruction**:
$$\text{Output} = \left( [(\text{logic} \ \& \ \text{mask}) \neq 0] \right) \oplus (\text{flags} \ \& \ 1)$$

##### Parameterization of the Universal Gate Model:

| Gate Type | Seed (`seed`) | Accumulator Semantics (`logic`) | Mask (`mask`) | Intermediate `bool(logic & mask)` | Invert Bit (`flags & 1`) | Final Evaluation Formula |
|---|---|---|---|---|---|---|
| **AND** | `0` (LOW) | Count of zeros | `0xFF` | $1$ if $\ge 1$ zeros; $0$ if zero zeros | $1$ | $([\text{zeros} > 0]) \oplus 1$ (HIGH iff zero zeros) |
| **NAND** | `0` (LOW) | Count of zeros | `0xFF` | $1$ if $\ge 1$ zeros; $0$ if zero zeros | $0$ | $([\text{zeros} > 0]) \oplus 0$ (LOW iff zero zeros) |
| **OR** | `1` (HIGH) | Count of ones | `0xFF` | $1$ if $\ge 1$ ones; $0$ if zero ones | $0$ | $([\text{ones} > 0]) \oplus 0$ (HIGH iff $\ge 1$ ones) |
| **NOR** | `1` (HIGH) | Count of ones | `0xFF` | $1$ if $\ge 1$ ones; $0$ if zero ones | $1$ | $([\text{ones} > 0]) \oplus 1$ (HIGH iff zero ones) |
| **XOR** | `1` (HIGH) | Count of ones | `0x01` | Parity bit of ones (`logic & 1`) | $0$ | $([\text{ones} \ \& \ 1]) \oplus 0$ (HIGH iff odd ones) |
| **XNOR** | `1` (HIGH) | Count of ones | `0x01` | Parity bit of ones (`logic & 1`) | $1$ | $([\text{ones} \ \& \ 1]) \oplus 1$ (HIGH iff even ones) |
| **BUFFER** | `1` (HIGH) | Count of ones | `0xFF` | $1$ if input is $1$; $0$ if input is $0$ | $0$ | $([\text{ones} > 0]) \oplus 0$ (Pass-through) |
| **NOT** | `1` (HIGH) | Count of ones | `0xFF` | $1$ if input is $1$; $0$ if input is $0$ | $1$ | $([\text{ones} > 0]) \oplus 1$ (Inverter) |

#### C. Elimination of Vtables & $O(1)$ Runtime Gate Mutability
In conventional object-oriented simulation architectures (Logisim, Digital, and `reactor_oop`):
- Each gate type is a separate subclass (`AND_Gate`, `OR_Gate`, `XOR_Gate`) with a virtual method table (`vtable`).
- Virtual dispatch incurs double dereferences (`this -> vptr -> vtable[slot]()`), stalling CPU execution pipelines and consuming 8 bytes per struct for the `vptr`.
- Mutating a gate (e.g., when a user in the GUI morphs an AND gate into an XOR gate) requires tearing down the object, allocating a new subclass on the heap, and rewiring graph references.

In Darion's optimized `reactor`:
- The gate struct is a flat 24-byte POD (`CPP_Gate`) without a `vptr`.
- All gate types share one flat array and one evaluation rule, so changing a gate's type is an in-place update of `(type, seed, mask, invert)` with no reallocation and no change to the array layout (`Gate.retype`).
- **Cost:** $O(1)$ when the seed does not change (AND/NAND/NOT share seed 0; OR/NOR/XOR/XNOR/BUF share seed 1). Across families the `logic` counter must be recomputed and the `seed`/`logic` cached in each incoming hitlist entry rewritten, which is $O(\text{fan-in})$. It is not a "3-byte write". Earlier versions of the code changed only `type` and `id`; that bug is fixed and covered by `test_retype_exhaustive` in `tests/integrity_test.py`.
- Treat this as a consequence of the uniform representation, not as a headline contribution.

---

### 2.3 Dynamic Bounded Topological Sweep (`sweep`) vs. Static LCS

In the logic simulation literature, Levelized Compiled Simulation (LCS) (Verilator; a verified LCS reference is still needed) and Levelized Event-Driven Simulation (LEDS) (Wang & Maurer 1990) operate on contrasting extremes:
* **Static LCS (Verilator):** Evaluates all gates from index $0$ to $N - 1$ unconditionally, on every cycle, regardless of whether inputs transitioned.
* **LEDS (LECSIM):** Partitions circuits into discrete level-queues ($L_0, L_1, \dots, L_k$), popping events level by level, which incurs queue maintenance overhead.

#### Darion's Dynamic Bounded Sweep with Back-Edge Escape:
Darion's `sweep()` in [`reactor/Circuit.pyx:L1483-L1575`](file:///home/farhan/Github/darion-logic-sim/reactor/Circuit.pyx#L1483-L1575) implements a hybrid approach:
1. **Dynamic Bounded Range $[\text{curr}, \text{threshold}]$:** Rather than sweeping the full netlist ($0 \dots N-1$), Phase 1 initializes `curr` to the minimum triggered gate address and `threshold` to the maximum triggered gate address.
2. **In-Place Selective Trace:** Phase 2 sweeps linearly through memory (`curr += 1`). Instead of queue operations, it tests `if (curr.flags & FLAG_MARK)`. The CPU hardware prefetcher streams the contiguous 24-byte gate array through L1/L2 caches with near-zero latency, skipping inactive gates in-place.
3. **Dynamic Threshold Expansion:** As gates evaluate, if a newly triggered gate lies beyond `threshold` (`target > threshold`), the sweep boundary dynamically expands (`threshold = target`).
4. **Back-Edge Escape Mechanism:** If a topological violation or sequential feedback occurs (`target <= curr`), Darion detects the back-edge, stores it in `read_queue`, and automatically hands it off:
   ```cpp
   if (back_edges) self.propagate(back_edges);
   ```
   This allows linear memory execution to handle DAG logic at hardware prefetch speeds, while delegating cyclic feedback to the wavefront engine without pipeline stalling.

---

### 2.4 Activity Thresholds and the Scaling Crossover (Beamer et al. 2020)

A critical question in logic simulation benchmarking is why and when an event-driven engine outpaces a compiled cycle-based simulator like Verilator.

**Scott Beamer and D. Donofrio** (*DAC 2020*, "Efficiently Exploiting Low Activity Factors to Accelerate RTL Simulation", the ESSENT simulator generator) motivate activity-aware simulation. (An earlier version of this file listed the wrong authors.)
- In compiled simulators (Verilator), execution cost per cycle is roughly constant: $C_{\text{comp}} = O(N)$.
- In event-driven simulators, execution cost per cycle is proportional to the switching activity factor $A$: $C_{\text{event}} = O(A \cdot N) + C_{\text{overhead}}$.
- **Measured here (benchmark stimulus):** gate-output activity is about 9.5–10.4% on `b15`, `b17`, `b18`, `b19` and 18.6% on `b14`; it stays near 10% even at a 0.5% input toggle rate because the clock and Darion's gate-level DFF latches keep switching. The earlier "2–6%" figure was wrong.
- **Result:** circuits with the same activity give opposite outcomes versus Verilator (`b14`: Verilator 6–7× faster; `b17`: about parity; `b19`: Darion 2.3–3.6× faster). Activity therefore does **not** explain the crossover. Design size does: the `b19` Verilator binary has 22 MB of code, runs at IPC 0.66 and takes 117M L1-instruction-cache misses, while the `b14` binary has 0.75 MB and runs at IPC 2.3. The supported explanation is compiled-code footprint exceeding the instruction cache.
- On dense combinational netlists (e.g., `hyp.v`), Verilator is faster than Darion (245 ms vs. 851 ms for `rx-sweep`).

---

### 2.5 Double-Buffered Wavefront Propagation (`propagate`)

Darion's `propagate()` implements a zero-allocation, branchless Discrete-Event Simulation (DES) engine inside a pure Cython `nogil` context:
1. **Raw Pointer Ping-Pong Queues:** Maintains two pre-allocated buffers (`read_queue` and `write_queue` of `CPP_Gate*`). At the end of each wave, buffers are swapped in $O(1)$ pointer operations without memory allocations.
2. **Branchless Queue Insertion:**
   ```cpp
   write_queue[size] = profile.target;
   size += (((target.flags & FLAG_MARK) == 0) & (target_output != target.output));
   target.flags |= FLAG_MARK * (target_output != target.output);
   ```
   Eliminates conditional branch instructions in the hottest fan-out loop, allowing uninterrupted superscalar CPU pipelining.
3. **Dynamic Wavefront Budgeting:** Enforces the two-tier dynamic wave limit, automatically transitioning runaway oscillations into timed priority tasks.

---

### 2.6 Comparison with Educational Tools (Digital & Logisim)

Educational tools focus on visual ergonomics but suffer from performance degradation on large-scale circuits:

| Feature | Logisim / Logisim-Evolution (Burch 2002) | Digital (Neemann 2016) | Darion Logic Sim |
|---|---|---|---|
| **Target Scale** | Small educational circuits (< 1,000 gates) | Medium circuits / toy CPUs (< 50,000 gates) | Standard-cell netlists up to the largest tested (`hyp.v`, 420,896 gates; `b19` expands to 356k engine entries). Logisim/Digital figures are unmeasured estimates. |
| **Language & Architecture** | Java Swing; recursive graph traversal | Java; flattened `Node`/`Element` object graph | Cython / C++ native Array-of-Structures (AOS) |
| **Memory Model** | Heap-allocated Java objects; GC pauses | Heap-allocated Java objects; high pointer indirection | Contiguous 24-byte cache-aligned native struct |
| **Simulation Paradigms** | Event-driven with static step limits | Event-driven loop (micro-step) | Dual-engine: BFS Wavefront + Topological Linear Sweep |
| **Academic Benchmark Suite** | None | Ad-hoc processor circuits | ISCAS-85, ISCAS-89, IWLS 2005, EPFL Mammoth |
| **Hardware Baselines** | None | None | Formally benchmarked against **Icarus Verilog** and **Verilator** |

---

## 3. What Constitutes Novelty in Systems and EDA Research?

In computer systems (OSDI, SOSP, ASPLOS) and EDA (DAC, ICCAD, TCAD), novelty rarely consists of discovering a new mathematical operator. Instead, novelty typically derives from:

1. **Architectural Synthesis:** Combining previously incompatible design patterns (e.g., interactive visual CAD and high-performance low-level simulation) to break an established trade-off.
2. **Microarchitectural Realization:** Translating abstract algorithmic models into cache-conscious, branchless native implementations that run at machine limits.
3. **Dual-Mode Adaptability:** Unifying two separate paradigms (Discrete-Event Wavefront vs. Static Linear Sweep) under a single in-memory representation without recompilation.
4. **Empirical Discovery and Proof:** Providing rigorous cross-engine measurements across standardized benchmark suites that reveal operational boundary conditions (such as the low-activity inversion point against Verilator).

---

## 4. Defensible Novel Contributions of Darion

When writing the paper, the contributions should be framed around these concrete, defensible pillars:

1. **The Single-Invariant Masked Accumulator (SIMA):**
   - Unifies all eight elementary logic gates into a single 3-tuple parameter vector $(\text{seed}, \text{mask}, \text{inv})$, evaluating parity via a bitwise mask (`mask = 0x01`) and dual-inversion via bitwise XOR (`flags & 1`).
   - The entire gate library evaluates through a single, uniform branchless instruction: `bool(logic & mask) ^ (flags & 1)`.
   - Eliminates virtual method tables (`vtable`); all gates share one flat array and one evaluation rule. The benefit of the rule itself over a `switch(type)` evaluator has **not yet been isolated** (ablation pending).

2. **Microarchitectural Data-Oriented Design (DOD):**
   - Gates are packed into an exact 24-byte POD struct (`static_assert(sizeof(CPP_Gate) == 24)`). Field order inside the first 8 bytes is not a result.
   - Re-allocates gates in physical memory based on Kahn's topological sort to improve locality. IPC is not an achievement: the 4+ IPC figures come from tiny L1-resident chains, and real `hyp.v` runs at IPC 1.3–1.5.
   - The defensible systems result is the **size crossover versus compiled simulation** (compiled-code footprint versus instruction cache), not the struct layout.

3. **Dynamic Bounded Topological Sweep (`sweep`) with Back-Edge Escape:**
   - Bridges the gap between static oblivious simulation (which evaluates $0 \dots N-1$ unconditionally) and levelized event scheduling (which incurs queue overhead).
   - Dynamically bounds linear evaluation to the active range $[\text{curr}, \text{threshold}]$, dynamically expanding as downstream gates trigger.
   - Detects topological backward edges (`target <= curr`) and automatically hands them off to the double-buffered wavefront engine (`propagate`), combining L1 prefetch throughput on DAG sub-cones with robust cyclic resolution.

4. **Two-Tier Dynamic Oscillation Budgeting with Non-Fatal Promotion:**
   - Formulates a two-tier wave budget: a $|V|+1$ pigeonhole bound for pure DAGs (sound, zero false positives on acyclic circuits, but loose compared with circuit depth) and a $2|V|$ heuristic for sequential feedback (unproven).
   - Replaces fatal simulator crashes with non-fatal promotion of oscillating wavefronts into an asynchronous timed priority queue with load-dependent gate delays.

5. **Inertial Delay Glitch Absorption ("Shock Absorber"):**
   - Implements $O(1)$ inertial delay filtering via timestamp validation (`if task.time < gate_clocks[origin]: return;`).
   - Prevents transient race-condition spikes from triggering event avalanches, absorbing narrow glitches in-place.

6. **Zero-Overhead Decoupled Visual-AOS Architecture:**
   - Bridges the gap between interactive schematic CAD and industrial batch simulation.
   - Decouples a dynamic PySide6 GUI from a native C++ simulation core using integer locations and a visual-queue deque. This is sound engineering, not a research contribution; the core is single-threaded, so there is nothing to be "lockless" about.

---

## 5. Ready-to-Cite Bibliography (BibTeX Format)

```bibtex
% Verified against Crossref on 2026-10-21 (title, authors, venue, year, pages, DOI) unless marked otherwise.
% Content of the cited works was NOT read unless the note says so.

@book{abramovici1990digital,
  author    = {Miron Abramovici and Melvin A. Breuer and Arthur D. Friedman},
  title     = {Digital Systems Testing and Testable Design},
  publisher = {Computer Science Press (W. H. Freeman)},
  year      = {1990},
  isbn      = {0-7167-8179-4},
  note      = {IEEE Press reprint 1994, doi:10.1109/9780470544389}
}

@article{malik1994analysis,
  author  = {Sharad Malik},
  title   = {Analysis of Cyclic Combinational Circuits},
  journal = {IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems},
  volume  = {13}, number = {7}, pages = {950--956}, year = {1994},
  doi     = {10.1109/43.293952}
}

@inproceedings{shiple1996combinational,
  author    = {Thomas R. Shiple and Vigyan Singhal and Robert K. Brayton and Alberto L. Sangiovanni-Vincentelli},
  title     = {Analysis of Combinational Cycles in Sequential Circuits},
  booktitle = {Proceedings of the IEEE International Symposium on Circuits and Systems (ISCAS)},
  volume    = {4}, pages = {592--595}, year = {1996},
  doi       = {10.1109/ISCAS.1996.542093}
}

@inproceedings{edwards2003making,
  author    = {Stephen A. Edwards},
  title     = {Making Cyclic Circuits Acyclic},
  booktitle = {Proceedings of the 40th ACM/IEEE Design Automation Conference (DAC)},
  pages     = {159--162}, year = {2003},
  doi       = {10.1145/775832.775874}
}

@inproceedings{riedel2003synthesis,
  author    = {Marc D. Riedel and Jehoshua Bruck},
  title     = {The Synthesis of Cyclic Combinational Circuits},
  booktitle = {Proceedings of the 40th ACM/IEEE Design Automation Conference (DAC)},
  pages     = {163--168}, year = {2003},
  doi       = {10.1145/775832.775875}
}

@inproceedings{beamer2020exploiting,
  author    = {Scott Beamer and David Donofrio},
  title     = {Efficiently Exploiting Low Activity Factors to Accelerate {RTL} Simulation},
  booktitle = {Proceedings of the 57th ACM/IEEE Design Automation Conference (DAC)},
  pages     = {1--6}, year = {2020},
  doi       = {10.1109/DAC18072.2020.9218632}
}

@article{ulrich1969exclusive,
  author  = {Ernst G. Ulrich},
  title   = {Exclusive Simulation of Activity in Digital Networks},
  journal = {Communications of the ACM},
  volume  = {12}, number = {2}, pages = {102--110}, year = {1969},
  doi     = {10.1145/362848.362870}
}

@inproceedings{wang1990lecsim,
  author    = {Zhicheng Wang and Peter M. Maurer},
  title     = {{LECSIM}: A Levelized Event Driven Compiled Logic Simulator},
  booktitle = {Proceedings of the 27th ACM/IEEE Design Automation Conference (DAC)},
  pages     = {491--496}, year = {1990},
  doi       = {10.1145/123186.123349},
  note      = {Read from the tech-report version: Z. Wang, USF VCAPP Lab Technical Report DA-19, 1988.}
}

@article{szygenda1975digital,
  author  = {Stephen A. Szygenda and Edward W. Thompson},
  title   = {Digital Logic Simulation in a Time-Based, Table-Driven Environment},
  journal = {Computer},
  volume  = {8}, number = {3}, pages = {24--36}, year = {1975},
  doi     = {10.1109/C-M.1975.218898},
  note    = {Part of a two-part series; the second part is pp. 38--49 (doi:10.1109/C-M.1975.218900). State which part is cited.}
}

@article{bryant1984switch,
  author  = {Randal E. Bryant},
  title   = {A Switch-Level Model and Simulator for {MOS} Digital Systems},
  journal = {IEEE Transactions on Computers},
  volume  = {C-33}, number = {2}, pages = {160--177}, year = {1984},
  doi     = {10.1109/TC.1984.1676408}
}

@inproceedings{chilimbi1999cache,
  author    = {Trishul M. Chilimbi and Mark D. Hill and James R. Larus},
  title     = {Cache-Conscious Structure Layout},
  booktitle = {Proceedings of the ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI)},
  pages     = {1--12}, year = {1999},
  doi       = {10.1145/301618.301633}
}

@inproceedings{chilimbi1999definition,
  author    = {Trishul M. Chilimbi and Bob Davidson and James R. Larus},
  title     = {Cache-Conscious Structure Definition},
  booktitle = {Proceedings of the ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI)},
  pages     = {13--24}, year = {1999},
  doi       = {10.1145/301618.301635}
}

@article{burch2002logisim,
  author  = {Carl Burch},
  title   = {Logisim: A Graphical System for Logic Circuit Design and Simulation},
  journal = {Journal on Educational Resources in Computing (JERIC)},
  volume  = {2}, number = {1}, pages = {5--16}, year = {2002},
  doi     = {10.1145/545197.545199},
  note    = {Crossref lists the title as "Logisim"; confirm the full title on the ACM page.}
}

@misc{neemann2016digital,
  author       = {Helmut Neemann},
  title        = {Digital: A digital logic designer and circuit simulator},
  year         = {2016},
  howpublished = {\url{https://github.com/hneemann/Digital}},
  note         = {Open-source software (GPL-3.0); evaluation model documented in the class comment of core/Model.java; version 0.31 checked}
}

@misc{verilator_veripool,
  author       = {Wilson Snyder and contributors},
  title        = {Verilator},
  howpublished = {\url{https://www.veripool.org/verilator/}},
  note         = {Software. Verilator has no peer-reviewed paper; the author's talks are listed at veripool.org/papers. State the version used (the installed one: run verilator --version).}
}

@inproceedings{acton2014data,
  author    = {Mike Acton},
  title     = {Data-Oriented Design and {C++}},
  booktitle = {CppCon 2014 (keynote)},
  year      = {2014},
  note      = {Talk; existence verified, content not transcribed here}
}

% --- added 2026-10-21 (prior art found during the audit) ---

@misc{maurer1999patent,
  author       = {Peter M. Maurer},
  title        = {System and method for digital simulation of an electrical circuit},
  howpublished = {US Patent 5,856,933 (filed 1997-04-28, granted 1999-01-05); continuation US 6,131,081 (filed 1998-12-16, granted 2000-10-10)},
  note         = {Expired. Read on Google Patents: per-gate counting of dominant inputs, deferred output inversion, XOR/XNOR/NOT/BUFFER by input-change events.}
}

@inproceedings{maurer2000event,
  author    = {Peter M. Maurer},
  title     = {Event Driven Simulation without Loops or Conditionals},
  booktitle = {Proceedings of the IEEE/ACM International Conference on Computer Aided Design (ICCAD)},
  pages     = {23--26}, year = {2000},
  doi       = {10.1109/ICCAD.2000.896445},
  note      = {Read in full 2026-10-21; see section 0.5.}
}

@techreport{shiple2002logical,
  author      = {Thomas R. Shiple and Robert K. Brayton and G{\'e}rard Berry and Alberto L. Sangiovanni-Vincentelli},
  title       = {Logical Analysis of Combinational Cycles},
  institution = {Electronics Research Laboratory, University of California, Berkeley},
  number      = {UCB/ERL M02/21}, year = {2002}, month = jun,
  note        = {Open copy at www2.eecs.berkeley.edu/Pubs/TechRpts/2002/ERL-02-21.pdf. Relevant sections read 2026-10-21: ternary simulation converges in at most m steps; Malik's algorithm within k rounds (k feedback vertices); Brzozowski--Seger transient bound (2^m-2)D.}
}

@inproceedings{wang2025epics,
  author    = {Wang and others},
  title     = {{EPICS}: Efficient Parallel Pattern Fault Simulation for Sequential Circuits via Strongly Connected Components},
  booktitle = {Proceedings of the 62nd ACM/IEEE Design Automation Conference (DAC)},
  pages     = {1--7}, year = {2025},
  doi       = {10.1109/DAC63849.2025.11132928},
  note      = {Metadata from Crossref (13 authors; fill in full names from the IEEE page). Only title and abstract seen.}
}

@misc{ghdl_docs,
  title        = {{GHDL} Documentation: Simulation and Runtime},
  howpublished = {\url{https://ghdl.github.io/ghdl/using/Simulation.html}},
  note         = {Option --stop-delta, default 5000 delta cycles.}
}

@phdthesis{fleurkens1996escape,
  author = {J. W. G. (Hans) Fleurkens},
  title  = {Interactive Modelling and Simulation of Heterogeneous Systems},
  school = {Eindhoven University of Technology},
  year   = {1996},
  doi    = {10.6100/IR456563},
  note   = {ESCAPE. Read in full 2026-10-21. Thesis statement 3: interactive design/simulation need not cost simulator performance.}
}

@misc{teiche2019simd,
  author       = {Alex S. Teiche},
  title        = {Heterogeneous Logic Gate Simulation Using {SIMD} Instructions},
  howpublished = {US Patent 10,331,830 B1 (Apple Inc.)},
  year         = {2019},
  note         = {Filed 13 June 2016, granted 25 June 2019.}
}

@inproceedings{maurer1994inversion,
  author    = {Peter M. Maurer},
  title     = {The Inversion Algorithm for Digital Simulation},
  booktitle = {Proceedings of the IEEE/ACM International Conference on Computer-Aided Design (ICCAD)},
  pages     = {258--261}, year = {1994},
  doi       = {10.1109/ICCAD.1994.629776},
  note      = {Read in full 2026-10-21. Credits the counting algorithm to Schuler 1972.}
}

@inproceedings{schuler1972nand,
  author    = {D. Schuler},
  title     = {Simulation of {NAND} Logic},
  booktitle = {Proceedings of COMPCON 72},
  pages     = {243--245}, year = {1972}, month = sep,
  note      = {Not found online or in Crossref; cited as given in Maurer 1994. The origin of the counting algorithm.}
}

@article{maurer1993shadow,
  author    = {Peter M. Maurer},
  title     = {The Shadow Algorithm: A Scheduling Technique for Both Compiled and Interpreted Simulation},
  journal   = {IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems},
  volume    = {12}, number = {9}, pages = {1411--1413}, year = {1993},
  doi       = {10.1109/43.240088},
  note      = {Metadata verified on Crossref; not read.}
}

@inproceedings{maurer1996unit,
  author    = {Peter M. Maurer},
  title     = {Unit Delay Simulation with the Inversion Algorithm},
  booktitle = {Proceedings of the IEEE/ACM International Conference on Computer-Aided Design (ICCAD)},
  pages     = {412--417}, year = {1996},
  doi       = {10.1109/ICCAD.1996.569831},
  note      = {Metadata verified on Crossref; not read.}
}

@inproceedings{maurer1996compiled,
  author    = {Peter M. Maurer},
  title     = {Is Compiled Simulation Really Faster Than Interpreted Simulation?},
  booktitle = {Proceedings of the 9th International Conference on VLSI Design},
  pages     = {303--306}, year = {1996},
  doi       = {10.1109/ICVD.1996.489615},
  note      = {Not read; relevant to the compiled-versus-event-driven crossover.}
}

@inproceedings{driesen1996direct,
  author    = {Karel Driesen and Urs H{\"o}lzle},
  title     = {The Direct Cost of Virtual Function Calls in {C++}},
  booktitle = {Proceedings of the 11th ACM SIGPLAN Conference on Object-Oriented Programming, Systems, Languages, and Applications (OOPSLA)},
  pages     = {306--323}, year = {1996},
  doi       = {10.1145/236337.236369}
}

@article{driesen1998accurate,
  author  = {Karel Driesen and Urs H{\"o}lzle},
  title   = {Accurate Indirect Branch Prediction},
  journal = {ACM SIGARCH Computer Architecture News (ISCA 1998)},
  volume  = {26}, number = {3}, pages = {167--178}, year = {1998},
  doi     = {10.1145/279361.279380}
}

@inproceedings{agrawal1989accuracy,
  author    = {Prathima Agrawal and R. Tutundjian and William J. Dally},
  title     = {Algorithms for Accuracy Enhancement in a Hardware Logic Simulator},
  booktitle = {Proceedings of the 26th ACM/IEEE Design Automation Conference (DAC)},
  pages     = {645--648}, year = {1989},
  doi       = {10.1145/74382.74496},
  note      = {Not read. Replaces the earlier entry that mixed this title with a 1990 TCAD citation. Cite only after reading.}
}

@article{agrawal1990hardware,
  author  = {Prathima Agrawal and William J. Dally},
  title   = {A Hardware Logic Simulation System},
  journal = {IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems},
  volume  = {9}, number = {1}, pages = {19--29}, year = {1990},
  doi     = {10.1109/43.45853},
  note    = {Not read.}
}

@inproceedings{clow2017pyrtl,
  author    = {John Clow and Georgios Tzimpragos and Deeksha Dangwal and Sammy Guo and Joseph McMahan and Timothy Sherwood},
  title     = {A Pythonic Approach for Rapid Hardware Prototyping and Instrumentation},
  booktitle = {27th International Conference on Field Programmable Logic and Applications (FPL)},
  pages     = {1--7}, year = {2017},
  doi       = {10.23919/FPL.2017.8056860},
  note      = {Verified on Crossref. Not read.}
}

@inproceedings{materzok2019digitaljs,
  author    = {Marek Materzok},
  title     = {{DigitalJS}: A Visual Verilog Simulator for Teaching},
  booktitle = {Proceedings of the 8th Computer Science Education Research Conference},
  pages     = {110--115}, year = {2019},
  doi       = {10.1145/3375258.3375272},
  note      = {Verified on Crossref (title "DigitalJS: a Visual Verilog Simulator for Teaching"). Not read.}
}
```

---

## 6. Publication-Ready "Related Work" Section

Here is the complete, publication-ready Related Works section for your paper:

> ### Related Work
> 
> **Logic Simulation Paradigms and Activity Thresholds:** Digital logic simulation fundamentally partitions into Discrete-Event Simulation (DES) \cite{ulrich1969exclusive} and Levelized Compiled-Code Simulation (LCS) \cite{wang1990lecsim} \textbf{[add a verified LCS reference]}. DES computes signal transitions dynamically based on event sensitivity, making it well-suited for circuits with sparse dynamic switching activity. In contrast, cycle-based compiled simulators, such as Verilator \cite{verilator_veripool}, translate logic netlists into straight-line machine instructions that evaluate the entire gate topology unconditionally on every active clock edge. Recent work by Beamer and Donofrio \cite{beamer2020exploiting} shows that exploiting low activity factors accelerates RTL simulation by skipping quiescent logic. We find that on gate-level netlists the observed crossover against a compiled simulator tracks design size, through the instruction-cache footprint of the generated code, rather than activity. Darion offers both paradigms within a single native runtime, dynamically supporting both double-buffered wavefront DES and linear topological sweeps over a contiguous memory layout without requiring offline C++ compilation passes.
> 
> **Gate Evaluation and Universal Parameterization:** Classical gate evaluation scans a gate's inputs or maintains a count of inputs at the gate's controlling value, updated on each input change \cite{abramovici1990digital, szygenda1975digital}. Maurer showed that gate outputs need not be computed explicitly: counting dominant-valued inputs suffices for AND/NAND/OR/NOR, XOR, XNOR, NOT and BUFFER can be processed by input changes alone, and output inversion can be applied afterwards \cite{maurer1994inversion, maurer1999patent}, and that state-testing code can be removed altogether by encoding gate state in subroutine addresses, an idea he motivated by virtual-function dispatch in place of type codes \cite{maurer1993shadow, maurer2000event}. On current out-of-order processors we measure the opposite trade-off: per-gate indirect dispatch dominates the cost, and replacing it with arithmetic over flat records removes it (Section 5.3). Our Single-Invariant Masked Accumulator (SIMA) is an arithmetic realization of this family: each gate keeps one count of inputs equal to a seed value, a mask selects an existence test or parity, and an inversion bit complements the result, so all eight elementary gates share one branch-free rule over a 24-byte record that also holds the output. We do not claim the counting idea as new; we contribute the uniform formulation, its verification, and a measured comparison with a type switch in the same engine.
>
> **Microarchitecture and Data-Oriented Design:** The widening disparity between CPU arithmetic throughput and memory latency (the "Memory Wall") has established memory locality as the primary bottleneck in large-scale simulation \cite{chilimbi1999cache}. While high-performance software engineering has widely adopted Data-Oriented Design (DOD) \cite{acton2014data}, commercial EDA tools remain burdened by legacy polymorphic C++ codebases, and interactive educational environments such as Logisim \cite{burch2002logisim} and Digital \cite{neemann2016digital} rely on heap-allocated Java/JVM object graphs subject to garbage collection pauses and cache pollution. Darion introduces a pure Data-Oriented architecture to logic simulation: gate structures are compacted into an exact 24-byte POD layout. Coupled with Kahn-based topological memory reordering, this keeps the working set compact and prefetch-friendly, and the engine's instruction footprint is independent of netlist size.
> 
> **Feedback Loops, Bounded Convergence, and Glitch Filtering:** Handling cyclic combinational loops in zero-delay simulation represents a classical challenge \cite{bryant1984switch, malik1994analysis, shiple1996combinational}. Simulators enforce fixed iteration limits on zero-delay loops: Verilator's \texttt{--converge-limit} (default 100 in 4.x and 5.020, 10000 in the current guide; exceeding it is an error), Logisim (1,000 iterations by default, then simulation stops \cite{burch2002logisim}) and Digital (1,000 micro-steps, then an error, with an optional random-order recovery mode \cite{neemann2016digital}); the behaviour of commercial tools was not verified. Formal cycle analysis \cite{malik1994analysis, edwards2003making} relies on expensive ternary BDD or SAT traversals during synthesis. Darion establishes a dynamic two-tier wave budgeting system: for Directed Acyclic Graphs (DAGs), reaching quiescence in a worst-case linear chain requires at most $|V| + 1$ wavefront evaluations, establishing a pigeonhole bound that guarantees zero false positives on acyclic circuits (the exact requirement is the circuit depth, so the bound is loose). For sequential circuits modeled with gate-level feedback latches, Darion uses a $2|V|$ heuristic budget, which we have not proven; non-convergence within it is not fatal because the cone is promoted to timed simulation. When the wave limit is reached, Darion seamlessly promotes oscillating wavefronts into an asynchronous timed priority queue with individual physical gate delays without crashing. Furthermore, Darion incorporates $O(1)$ timestamp validation to implement inertial delay glitch filtering \cite{abramovici1990digital}, physically absorbing transient race-condition spikes in-place.
> 
> **Interactive CAD vs. Batch Compilation:** Existing EDA software enforces a strict division between interactive schematic design and high-throughput simulation. Educational visual tools provide intuitive drag-and-drop wiring but degrade severely on large designs due to dynamic object overheads. Conversely, industrial engines achieve exceptional throughput but operate as offline, batch-compiled command-line tools devoid of real-time visual feedback. Darion bridges this divide with a model-view decoupling: the interactive PySide6 frontend communicates with the native C++ simulation backend through integer gate indices and a visual-queue deque, achieving sub-second elaboration of industrial netlists (about 90$\times$ lower turnaround than Verilator's compile flow on `b19`, measured with the Verilog parse included) and competitive simulation throughput on large designs.
