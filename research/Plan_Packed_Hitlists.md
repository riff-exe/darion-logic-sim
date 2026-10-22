# Plan: packed hitlists in `optimize()` (P1)

Status: design for discussion (2026-10-22). Nothing implemented. Engine change, the author implements; this document is the working plan and the list of open issues. Line numbers refer to the tree as of 2026-10-22.

## 1. Goal

After `optimize()` reorders the gates, place every gate's fan-out list (`hitlist`) in one contiguous block, in the new gate order, so that a wave walks the edges in memory order. Keep the gate struct, the edge entries, the pointers and the propagation loops exactly as they are.

Non-goals: indices instead of pointers (measured slower, see 2.1), a flattened CSR structure (needs rebuilds on edits), any change to `reactor_oop/` or `engine/` (the comparison engines stay as they are).

## 2. Evidence so far

### 2.1 Harness (`tests/ablation_layout.cpp`, 25 real netlists, `Benchmark/9700X/Index_vs_pointer.md`)

| Variant against `d` (24 B gate, per-gate pointer lists allocated during wiring) | Geomean | 100k gates or more | Faster on |
|---|---|---|---|
| `i` index edges, same layout | 1.128 (slower) | 1.202 | 0/25 |
| `q` lists packed into one block in placement order | **0.911** | **0.854** | 25/25 |
| `p` flattened CSR with pointers, 16 B gate | 0.926 | 0.851 | 20/25 |

Packing captures all of the CSR gain; pointers beat indices in every layout.

### 2.2 The real engine is not the harness's `d`

`Circuit.hitlist_mem_layout()` on b15 and b19 (JSON load, as the app loads):

| State | Consecutive lists adjacent | Going backwards | Median gap |
|---|---:|---:|---:|
| before `optimize()` | 16-18% | 34-35% | 736-896 B |
| after `optimize()`, clean heap | 96-98% | 1-2% | 16 B (malloc header) |
| after `optimize()`, heap with list-sized holes (long-session model) | 52% | 24% | 16 B |

`optimize()` already copies every list into a fresh allocation in the new order (2.3, step 4), so on a clean heap the layout is already nearly packed. Packing therefore buys (a) a guaranteed ordered layout independent of heap state, (b) removal of the 16-byte header between lists (most gates have 1-2 edges, 16-32 B, so headers are a third to a half of the walked memory). **The real-engine gain is unknown and is the first thing to measure** (section 7.2).

### 2.3 Life cycle of a hitlist today

1. **Creation:** `Store.get` ([Store.pyx:67](../reactor/Store.pyx#L67)) `emplace_back(CPP_Gate(choice, lim))`; the hitlist starts empty. `gate_infolist` is reserved to 500,000 at construction ([Circuit.pyx:34](../reactor/Circuit.pyx#L34)); beyond that `Store.get` doubles it and shifts every `profile.target` and `Gate.info` by `diff` ([Store.pyx:44-64](../reactor/Store.pyx#L44-L64)); the vector moves gates with `HitList`'s move constructor.
2. **Growth:** `HitList::emplace_back` / `push_back` ([Profile.h:127-134, 214-221](../reactor/Profile.h#L214-L221)) `realloc` when `size == capacity`. Callers: `Gate.connect` ([Gates.pyx:246](../reactor/Gates.pyx#L246)), `Gate.reveal`, `Gate.retype`, `IC.reveal` ([IC.pyx:203](../reactor/IC.pyx#L203)).
3. **Shrink:** `pop()` ([Gates.pyx:15-26](../reactor/Gates.pyx#L15-L26)) swap-and-pop in place (`size -= 1`), used by `disconnect`, `Gate.hide`, `IC.hide`.
4. **`optimize()`** ([Circuit.pyx:823-999](../reactor/Circuit.pyx#L823-L999), `_topological_sort`): computes `serial`/`hash_map`, then `new_gate_infolist.resize(n)` and `new_gate_infolist[i] = gate_infolist[serial[i]]` (line 972, `CPP_Gate` copy assignment, so `HitList::operator=` mallocs a fresh array per list), rewrites every `profile.target` and `profile.seed` (lines 973-981), sorts each list by target address (line 983), `swap`s (985); the old vector is destroyed at the end of the function, freeing every old list.
5. **`refresh()`** ([Circuit.pyx:673](../reactor/Circuit.pyx#L673)): `optimize()` then `pop_back` of hidden gates (destructors run).
6. **`clearcircuit()`** ([Circuit.pyx:1258](../reactor/Circuit.pyx#L1258)): `gate_infolist.clear()` (all destructors).
7. **Teardown:** `__dealloc__` is empty ([Circuit.pyx:72](../reactor/Circuit.pyx#L72)); the C++ member vector is destroyed with the object (all destructors).
8. `hide`/`reveal`/`delobj` are deprecated by the author (deletion now rebuilds from stored connections) but still in the code; they only use `pop`/`emplace_back`, so they are covered by the same rules.

## 3. Design

### 3.1 Ownership encoded in `capacity` (no new field, `uint32_t` kept)

| `data` | `size` | `capacity` | Meaning | Grow | Free |
|---|---|---|---|---|---|
| `nullptr` | 0 | 0 | empty | malloc | nothing |
| own array | n | >= n, > 0 | owned (before `optimize()`, or grown out of the block) | malloc + copy, free old | `free(data)` |
| slice of the block | n > 0 | **0** | packed | malloc + copy, **old not freed** | nothing |
| `Macro*` | 0 | 0 | macro stub (P2, `FLAG_MACRO`) | never | nothing |

Rules: free only when `capacity > 0`; grow when `size >= capacity` (with `==` a packed slice, `size 3, capacity 0`, never looks full and writes into the next gate's slice); growth is always malloc + copy (the author prefers this to `realloc`; growth is a cold path).

`uint32_t` stays: vga_lcd's clock fan-out is 33,833, so 16-bit `capacity` would wrap when doubling to 65,536, and 16-bit fields save nothing (8-byte alignment keeps `HitList` at 16 B).

### 3.2 The block

* Owned by `Circuit`: `Profile* edge_block` (and its size for debugging). One block per circuit object; sandbox circuits (`save_as_ic`, IC creation) have their own.
* Created only in `optimize()`; never resized or moved; edits never touch it (a gate that grows leaves it, a gate that shrinks stays in it).
* Freed: by the next `optimize()` after every list points into the new block; by `clearcircuit()` after `gate_infolist.clear()`; by `__dealloc__` after the vector is destroyed (the member destructor runs after `__dealloc__`, so the block must be freed in a way that does not precede the lists' destructors: free it in `__dealloc__` is safe because slices are never freed by their destructors; the order only matters for owned lists, which do not live in the block).

### 3.3 The packing step (replaces line 972)

Today the copy is `new_gate_infolist[i] = gate_infolist[serial[i]]`, one malloc per list. Packing replaces it with an explicit copy: header fields copied, list data copied into the block. A C++ helper in `Profile.h` keeps it out of Cython:

```cpp
// Copy src into dst (a default-constructed gate in the new vector), placing src's edges at *cursor.
inline void pack_gate(CPP_Gate &dst, const CPP_Gate &src, Profile *&cursor) {
  std::memcpy(&dst, &src, offsetof(CPP_Gate, hitlist));        // the 8 header bytes
  const HitList &h = src.hitlist;
  if (h.size) {
    std::memcpy(cursor, h.data, h.size * sizeof(Profile));
    dst.hitlist.data = cursor; dst.hitlist.size = h.size; dst.hitlist.capacity = 0;
    cursor += h.size;
  } else {                                                     // empty list, or a macro stub's Macro* (P2)
    dst.hitlist.data = h.data; dst.hitlist.size = 0; dst.hitlist.capacity = 0;
  }
}
```

Order in `_topological_sort`:
1. Count `total = sum(gate_infolist[i].hitlist.size)` over all `n` gates (hidden ones too; they sit at the end of the order).
2. `new_block = malloc(total * sizeof(Profile))` (aligned to 64 is optional).
3. `new_gate_infolist.resize(n)`; for `i` in `0..n-1`: `pack_gate(new_gate_infolist[i], gate_infolist[serial[i]], cursor)`.
4. The existing target/seed rewrite and per-list sort (lines 973-983) run unchanged; they operate on slices.
5. `swap` (985). The old vector is destroyed at function exit: owned lists are freed, slices of the previous block are not.
6. After the old vector is gone (end of the function or an explicit `clear()` of the local), `free(old_block)`; `self.edge_block = new_block`.

The header `memcpy` assumes the 8 header bytes are trivially copyable (they are) and that `offsetof(CPP_Gate, hitlist) == 8` (static-asserted in `Profile.h`).

### 3.4 `HitList` changes ([Profile.h:39-137, 214-221](../reactor/Profile.h#L39-L221))

| Member | Line | Change |
|---|---|---|
| destructor | 46 | `if (capacity) std::free(data);` |
| copy constructor | 55 | none: already allocates its own array and sets `capacity = other.size` |
| copy assignment | 66 | if `capacity < other.size` (which includes every slice, `capacity 0`): malloc a new array, copy, free the old one only if `capacity > 0`; never `realloc` a slice |
| move assignment | 86 | free own `data` only if `capacity > 0` |
| move constructor, `swap` | 101, 110 | none (they carry `capacity`, i.e. ownership, to the new owner) |
| `push_back`, `emplace_back` | 127, 214 | `if (size >= capacity)`: `nc = size ? size*2 : 2`; malloc `nc`; copy `size` entries; free old only if `capacity > 0`; `data = new; capacity = nc` |

`pop()` and the per-list `sort` work on slices unchanged (they only write inside `[data, data+size)`).

### 3.5 What does not change

The gate struct (24 B, static asserts stay), `Profile` (16 B), the hot loops (`propagate`, `sweep`, `complete_task`; they read `data` and `size` only), `connect`/`disconnect` call sites, `Store.get` and its pointer fix-up loop, `Store`/JSON format, `reactor_oop/`, `engine/`.

## 4. Edge cases

* **Empty circuit:** `_topological_sort` returns early (line 825); no block.
* **Second `optimize()`:** lists still in the old block are copied into the new one like any other; the old block is freed last.
* **Gate-vector growth after `optimize()`** (beyond the 500k reservation): the move constructor keeps `data` (slice), `capacity 0`; `Store.get`'s `diff` loop rewrites targets inside slices; fine.
* **`refresh()`:** `pop_back` of hidden gates; slices are not freed; fine.
* **`clearcircuit()`:** must also free the block (after `clear()`), or the block leaks.
* **Hidden gates:** packed at the end like the others; harmless.
* **Debug dump `hitlist_mem_layout()`** ([Circuit.pyx:167](../reactor/Circuit.pyx#L167)) reports `capacity`; it will show 0 for packed lists. If the measurement script uses `capacity` to compute gaps, use `size` instead.
* **Memory peak:** during `optimize()` the old lists and the new block coexist, as today (old lists and new mallocs coexist now). No new peak.
* **Sandbox circuits** (`save_as_ic` with components, IC creation): separate `Circuit` objects, separate blocks; destroyed normally.

## 5. Interaction with P2 (macros)

A macro stub keeps a `Macro*` in `hitlist.data` with `size = capacity = 0`. `pack_gate` copies `data` for empty lists, so the pointer survives `optimize()` (today's copy assignment would drop it: it copies nothing for `other.size == 0`). The stub never grows (`connect` refuses a stub as a source), so its `data` is never treated as edges, freed or reallocated.

## 6. Implementation steps

1. `Profile.h`: ownership rules in `HitList` (3.4); `pack_gate` helper (3.3).
2. `Circuit.pxd`: `cdef Profile* edge_block`; declare `pack_gate` in the `extern` block (`Gates.pxd`).
3. `Circuit.pyx` `_topological_sort`: replace line 972 with the packing loop; free the old block after the swap.
4. `Circuit.pyx`: free the block in `clearcircuit()` and `__dealloc__`; initialise it to `NULL` in `__cinit__`.
5. Optional: a debug counter of lists that have left the block (for the long-session question, 8.3).

Estimated size: about 60-100 lines in `Profile.h`, `Circuit.pyx`, `Circuit.pxd`, `Gates.pxd`.

## 7. Validation

### 7.1 Correctness

* `tests/integrity_test.py` (28,115 tests) and `tests/test_timing.py` (all three suites): unchanged results.
* New cases in `integrity_test.py` (extend the existing file): optimize, then connect to a packed gate (grows out of the block), disconnect from a packed gate (shrinks in place), optimize again, clearcircuit, repeated optimize/edit cycles, `refresh()` with hidden gates; after each step compare outputs against an unoptimized copy of the same circuit.
* A build with AddressSanitizer (`-fsanitize=address`) running the integrity tests once: any `free` of a slice, overlap or use-after-free shows up immediately.
* `hitlist_mem_layout()` after `optimize()`: every list adjacent with gap 0 (no header), 100% in order, on a clean and on a fragmented heap.
* `tests/verify_state.py` on b14, b15 and two OpenCores designs: unchanged.

### 7.2 Performance (scratch build, never in `reactor/` for the experiment)

* Copy `reactor/` to the scratchpad, apply the change, build there, point `PYTHONPATH` at it (as `tests/ablation_eval.py` does for the switch ablation).
* Measure current build against packed build, interleaved, pinned to core 2, 7-9 repeats, median and spread, on b15, b17, b18, b19, vga_lcd, des_perf, aes_core, ac97_ctrl:
  * clean heap (fresh process, load, optimize, run);
  * fragmented heap (before loading, allocate and free list-sized blocks in a scattered pattern, the recipe used for 2.2).
* Expected: small gain on a clean heap (headers only), larger on a fragmented one. Report as measured.
* If adopted: re-run the master tests behind Claim 13 (rx-prop and rx-sweep change; rx-oop does not), and update Claim 13 (the data-oriented engine gets faster, so the OOP/prop ratio grows; say why).

## 8. Open issues for discussion

1. **Is the gain worth it on a clean heap?** If the scratch build shows only a percent or two on a clean heap, the case rests on fragmented heaps (long sessions). Decide whether that is enough, or whether to also check whether the app's heap actually gets that fragmented (the UI process after an hour of editing).
2. **Hidden gates:** pack them or leave them owned? Packing everything is simpler; leaving hidden ones owned saves block space if many are hidden. Hide/reveal are deprecated, so this probably does not matter.
3. **Drift between optimizes:** every gate that grows leaves the block. After heavy editing in SIMULATE mode, the layout degrades toward today's. Is `optimize()` called often enough (it is the user's or the app's choice), or should the app call it after N edits?
4. **Alignment:** align the block to 64 bytes? Lists start wherever the previous one ended; cache-line alignment of the block start is a few bytes and cannot hurt.
5. **`hitlist_mem_layout()` semantics:** report packed lists distinctly (e.g. capacity 0 means packed) so future layout checks are not misread.
6. **Claim 13 framing:** packing makes the data-oriented engine faster without changing the OOP engine. The comparison stays fair only if the paper states it (layout optimization is part of the data-oriented design; the OOP engine has no equivalent because its objects are heap-allocated individually by design).
