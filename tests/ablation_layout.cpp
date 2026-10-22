// OOP versus data-oriented ablation, standalone (does not touch reactor/).
//
// Four gate representations run the SAME algorithm (the propagate() loop of reactor/Circuit.pyx: fan-out walk over
// Profile entries, cached seed/logic per edge, double-buffered work queues, mark bit to avoid duplicates) on the SAME
// netlist, input vectors and placement order:
//
//   a  heap       separately `new`ed C++ subclasses with a virtual compute()          (as reactor_oop; --frag scatters them)
//   b  arena      the same objects placement-new'd contiguously in placement order     (still virtual)
//   c  flat+sw    24-byte CPP_Gate structs in one array, evaluation by switch(type)
//   d  flat+SIMA  the same 24-byte structs, evaluation by the branch-free mask/invert rule (reactor/Profile.h)
//   e  flat32     (optional, --variants includes e) variant d with the struct padded to 32 bytes
//   g  flat40     (optional) variant d padded to 40 bytes, the size of the OOP objects
//
// Steps:  a->b changes allocation/layout only (same object, same virtual call),
//         b->c removes the vtable call but ALSO shrinks the object (40 -> 24 bytes) and drops the vptr,
//         c->d changes the evaluation rule only (same struct, same layout),
//         d->e changes the struct size only (24 -> 32 bytes; alignment of the 64-byte line),
//         b->g changes dispatch AND rule at equal object size (40 B virtual -> 40 B SIMA, no vtable call), g->d then changes size only (40 -> 24).
//   i  flat+idx   (optional) variant d with 32-bit index edges (8-byte entries instead of 16) and uint32 work queues
//   j  flat32+idx (optional) variant i with the gate padded to 32 bytes (power-of-two stride); compare with e
//   k  flat16+CSR (optional) index edges in one shared array ordered by gate placement (CSR); the gate is 16 bytes
//                 (8-byte header + first-edge offset + edge count) instead of carrying a per-gate list
//   p  CSR+ptr    (optional) variant k with pointer edges (16-byte entries) and pointer queues; k->p isolates index vs pointer in CSR
//   q  packed     (optional) variant d with all hitlist arrays copied into one block in placement order (gate stays 24 B,
//                 loop unchanged); d->q is the contiguous-edges part of p's gain, q->p the 24 -> 16 B gate part
//         d->i changes the edge reference only (pointer -> index, same gate struct and per-gate lists),
//         i->k changes where edges live (per-gate malloc'd lists -> one contiguous array) and shrinks the gate 24 -> 16.
// Fan-out lists are per-gate malloc'd Profile arrays in variants a-g, so edges are not a difference among them.
// All variants must report identical evaluation counts, changed-gate counts and final-state fingerprints.
//
// Build:  g++ -O3 -march=native -std=c++20 -o ablation_layout tests/ablation_layout.cpp
//         --netlist FILE replays a real netlist exported by tests/ablation_eval.py --export (Darion layout order, benchmark vectors).
//         --topology chain|tree|random|mixchain; mixchain --vary toggles random side inputs so the evaluated sequence
//         changes every iteration (predictor-memorization test, versus the fixed sequence without --vary).
// Run:    taskset -c 2 ./ablation_layout --topology random --n 100000 --iters 200 --reps 9
//         --only a   runs one variant (for perf stat); counters are read in-process (user mode) otherwise.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <map>
#include <memory>
#include <random>
#include <string>
#include <vector>
#include <linux/perf_event.h>
#include <sys/ioctl.h>
#include <sys/syscall.h>
#include <unistd.h>

enum : uint8_t { AND, NAND, OR, NOR, XOR, XNOR, BUF, NOT, VAR };
static const uint8_t UNKNOWN = 2;

// ------------------------------------------------------------------------------------------------ shared pieces
template <class G> struct Prof {          // 16 B, identical to reactor/Profile.h
  G *target; uint8_t logic, seed, index;
};
template <class G> struct Hit {           // 16 B, same growth policy as HitList
  Prof<G> *data = nullptr; uint32_t size = 0, capacity = 0;
  void push(G *t, uint8_t i, uint8_t out, uint8_t tseed) {
    if (size == capacity) { capacity = capacity ? capacity * 2 : 2; data = (Prof<G> *)std::realloc(data, capacity * sizeof(Prof<G>)); }
    data[size++] = Prof<G>{t, uint8_t(out == tseed), tseed, i};
  }
};

static uint8_t seed_of(uint8_t t) { return (t == AND || t == NAND) ? 0 : 1; }

// ---- OOP gate (layout of reactor_oop/Profile.h) ----
struct OG {
  int8_t type; uint8_t output, inputlimit, mark, update, value, scheduled, logic, seed;
  Hit<OG> hit;
  OG(int8_t t, uint8_t lim, uint8_t s) : type(t), output(UNKNOWN), inputlimit(lim), mark(0), update(1), value(0), scheduled(0), logic(0), seed(s) {}
  virtual void compute() noexcept { output = UNKNOWN; }
  virtual ~OG() = default;
};
#define OG_SUB(NAME, ID, EXPR) \
  struct NAME : OG { NAME() : OG(ID, 0, seed_of(ID)) {} void compute() noexcept override { output = inputlimit ? UNKNOWN : (EXPR); } };
OG_SUB(OG_AND, AND, logic == 0) OG_SUB(OG_NAND, NAND, logic > 0) OG_SUB(OG_OR, OR, logic > 0) OG_SUB(OG_NOR, NOR, logic == 0)
OG_SUB(OG_XOR, XOR, logic & 1) OG_SUB(OG_XNOR, XNOR, (logic & 1) ^ 1) OG_SUB(OG_BUF, BUF, logic > 0) OG_SUB(OG_NOT, NOT, logic == 0)
OG_SUB(OG_VAR, VAR, value)
static_assert(sizeof(OG_AND) == sizeof(OG) && sizeof(OG_VAR) == sizeof(OG), "subclasses must not add fields");

// ---- flat gate (layout of reactor/Profile.h) ----
enum : uint8_t { F_NEGATE = 1, F_MARK = 4, F_UPDATE = 8 };
template <size_t PAD> struct FG_t {
  uint8_t flags = F_UPDATE, output = UNKNOWN, inputlimit = 0, mask = 0xFF, logic = 0, seed = 1; int8_t type = 0; uint8_t reserved = 0;
  Hit<FG_t> hit;
  uint8_t pad[PAD] = {};
};
template <> struct FG_t<0> {
  uint8_t flags = F_UPDATE, output = UNKNOWN, inputlimit = 0, mask = 0xFF, logic = 0, seed = 1; int8_t type = 0; uint8_t reserved = 0;
  Hit<FG_t> hit;
};
using FG = FG_t<0>;
using FG32 = FG_t<8>;
using FG40 = FG_t<16>;
static_assert(sizeof(FG) == 24 && sizeof(FG32) == 32 && sizeof(FG40) == 40 && sizeof(OG) == 40, "unexpected struct sizes");

static void init_flat(auto &g, uint8_t t) {
  g.type = t; g.seed = seed_of(t); g.mask = (t == XOR || t == XNOR) ? 1 : 0xFF;
  g.flags = F_UPDATE | ((t == AND || t == NOR || t == XNOR || t == NOT) ? F_NEGATE : 0);
}

// ---- policies: how a target is evaluated and marked (everything else in propagate() is shared) ----
struct PolVirtual {                       // a, b
  static inline void eval(OG *t) { t->compute(); }
  static inline bool is_marked(OG *t) { return t->mark; }
  static inline void set_mark(OG *t, bool c) { t->mark |= c; }
  static inline void clear_mark(OG *t) { t->mark = 0; }
  static inline bool unknown_out(OG *t) { return t->output == UNKNOWN; }
};
template <class G> struct PolSwitch {     // c: same accumulators, switch(type) dispatch (the DARION_EVAL_SWITCH ablation)
  static inline void eval(G *t) {
    uint8_t r;
    if (t->inputlimit) r = UNKNOWN;
    else switch (t->type) {
      case AND: r = t->logic == 0; break;   case NAND: r = t->logic != 0; break;
      case OR: r = t->logic != 0; break;    case NOR: r = t->logic == 0; break;
      case XOR: r = t->logic & 1; break;    case XNOR: r = !(t->logic & 1); break;
      case NOT: r = t->logic == 0; break;   default: r = t->logic != 0; break;   // BUF
    }
    t->output = r;
  }
  static inline bool is_marked(G *t) { return t->flags & F_MARK; }
  static inline void set_mark(G *t, bool c) { t->flags |= F_MARK * c; }
  static inline void clear_mark(G *t) { t->flags &= ~F_MARK; }
  static inline bool unknown_out(G *t) { return t->output == UNKNOWN; }
};
template <class G> struct PolSima {       // d, e: unified mask/invert rule
  static inline void eval(G *t) { t->output = t->inputlimit ? UNKNOWN : (bool(t->logic & t->mask) ^ (t->flags & 1)); }
  static inline bool is_marked(G *t) { return t->flags & F_MARK; }
  static inline void set_mark(G *t, bool c) { t->flags |= F_MARK * c; }
  static inline void clear_mark(G *t) { t->flags &= ~F_MARK; }
  static inline bool unknown_out(G *t) { return t->output == UNKNOWN; }
};

// ------------------------------------------------------------------------------------------------ netlist
struct Net {
  int n = 0, nin = 0;
  std::vector<uint8_t> type;                  // by id; ids are topologically ordered, inputs first
  std::vector<std::vector<int>> in;           // predecessor ids per pin
  std::vector<int> slot;                      // placement: memory position of each id
  std::vector<uint8_t> out, logic;            // reference initial state
};

static Net make_net(const std::string &topo, int n, int window, uint32_t seed, bool shuffle) {
  Net N; std::mt19937 rng(seed);
  if (topo == "chain") {                      // one input, NOT chain: every toggle evaluates every gate
    N.n = n; N.nin = 1; N.type.assign(n, NOT); N.in.assign(n, {}); N.type[0] = VAR;
    for (int i = 1; i < n; i++) N.in[i] = {i - 1};
  } else if (topo == "mixchain") {            // chain whose gates are all 8 kinds (2-input gates are fed a constant so every
                                              // change still propagates): the virtual-call target sequence is long and fixed.
                                              // Taps (XOR with a side input every `window` gates) are used by --vary.
    int taps = std::max(1, n / std::max(window, 1));
    N.nin = 3 + taps; N.n = n + N.nin; N.type.assign(N.n, VAR); N.in.assign(N.n, {});
    for (int i = N.nin; i < N.n; i++) {
      int prev = (i == N.nin) ? 0 : i - 1; int k = i - N.nin;
      if (k % window == window - 1) { N.type[i] = XOR; N.in[i] = {prev, 3 + (k / window) % taps}; continue; }
      static const uint8_t kinds[] = {AND, NAND, OR, NOR, XOR, XNOR, BUF, NOT};
      uint8_t t = kinds[rng() % 8]; N.type[i] = t;
      if (t == BUF || t == NOT) N.in[i] = {prev};
      else N.in[i] = {prev, (t == AND || t == NAND) ? 1 : 2};                 // const 1 for AND/NAND, const 0 otherwise
    }
    N.out.assign(N.n, 0); N.logic.assign(N.n, 0);
    N.slot.resize(N.n); for (int i = 0; i < N.n; i++) N.slot[i] = i;
    if (shuffle) std::shuffle(N.slot.begin(), N.slot.end(), rng);
    N.out[0] = rng() & 1; N.out[1] = 1; N.out[2] = 0; for (int i = 3; i < N.nin; i++) N.out[i] = rng() & 1;
    goto settle;
  } else if (topo == "tree") {                // complete binary tree of XORs, leaves are the inputs
    int leaves = 1; while (2 * leaves - 1 < n) leaves *= 2;
    N.n = 2 * leaves - 1; N.nin = leaves; N.type.assign(N.n, XOR); N.in.assign(N.n, {});
    for (int i = 0; i < leaves; i++) N.type[i] = VAR;
    for (int i = leaves, a = 0; i < N.n; i++, a += 2) N.in[i] = {a, a + 1};
  } else {                                    // random DAG, locality window, mixed gate types
    N.n = n; N.nin = std::max(16, n / 10); N.type.assign(n, VAR); N.in.assign(n, {});
    const uint8_t kinds[] = {AND, NAND, OR, NOR, XOR, XNOR, NOT, BUF};
    for (int i = N.nin; i < n; i++) {
      uint8_t t = kinds[rng() % 8]; N.type[i] = t;
      int pins = (t == NOT || t == BUF) ? 1 : 2;
      for (int p = 0; p < pins; p++) {
        int j;
        if (rng() % 5) { int w = std::min(window, i); j = i - 1 - int(rng() % w); }   // 80% local
        else j = int(rng() % i);                                                      // 20% anywhere earlier
        N.in[i].push_back(j);
      }
    }
  }
  N.slot.resize(N.n); for (int i = 0; i < N.n; i++) N.slot[i] = i;
  if (shuffle) std::shuffle(N.slot.begin(), N.slot.end(), rng);
  N.out.assign(N.n, 0); N.logic.assign(N.n, 0);
  for (int i = 0; i < N.nin; i++) N.out[i] = rng() & 1;
settle:                                       // reference initial state by direct evaluation
  for (int i = N.nin; i < N.n; i++) {
    uint8_t s = seed_of(N.type[i]); int l = 0;
    for (int j : N.in[i]) l += (N.out[j] == s);
    N.logic[i] = l;
    switch (N.type[i]) {
      case AND: N.out[i] = l == 0; break; case NAND: N.out[i] = l > 0; break; case OR: N.out[i] = l > 0; break;
      case NOR: N.out[i] = l == 0; break; case XOR: N.out[i] = l & 1; break; case XNOR: N.out[i] = !(l & 1); break;
      case BUF: N.out[i] = l > 0; break; case NOT: N.out[i] = l == 0; break;
    }
  }
  return N;
}


// Real netlist exported by `tests/ablation_eval.py --export` (Darion's gate array after reset and warm-up, plus the
// benchmark's input vectors). Text format: "n nvec", then n lines "type output nin src...", then nvec lines
// "k loc val loc val ...". Ids are Darion locations (the engine's layout order); --shuffle permutes the placement.
static Net load_net(const std::string &path, bool shuffle, uint32_t seed, std::vector<std::vector<int>> &vecs) {
  Net N; FILE *f = std::fopen(path.c_str(), "r"); if (!f) { std::perror(path.c_str()); std::exit(2); }
  int nvec; if (std::fscanf(f, "%d %d", &N.n, &nvec) != 2) std::exit(2);
  N.nin = 0; N.type.resize(N.n); N.in.resize(N.n); N.out.resize(N.n); N.logic.assign(N.n, 0);
  for (int i = 0; i < N.n; i++) {
    int t, o, k; if (std::fscanf(f, "%d %d %d", &t, &o, &k) != 3) std::exit(2);
    N.type[i] = t <= 5 ? t : t == 7 ? NOT : t == 9 ? VAR : BUF;       // pins (8, 10) and anything else behave as BUF
    N.out[i] = o;
    for (int j = 0; j < k; j++) { int s; if (std::fscanf(f, "%d", &s) != 1) std::exit(2); N.in[i].push_back(s); }
  }
  vecs.resize(nvec);
  for (auto &v : vecs) { int k; if (std::fscanf(f, "%d", &k) != 1) std::exit(2); for (int j = 0; j < k; j++) { int l, x; if (std::fscanf(f, "%d %d", &l, &x) != 2) std::exit(2); v.push_back(l * 4 + x); } }
  std::fclose(f);
  for (int i = 0; i < N.n; i++) { uint8_t s = seed_of(N.type[i]); int l = 0; for (int j : N.in[i]) l += (N.out[j] == s); N.logic[i] = l; }
  N.slot.resize(N.n); for (int i = 0; i < N.n; i++) N.slot[i] = i;
  if (shuffle) { std::mt19937 rng(seed); std::shuffle(N.slot.begin(), N.slot.end(), rng); }
  return N;
}

// ------------------------------------------------------------------------------------------------ perf counters
struct Counters { uint64_t cycles = 0, instr = 0, branch_miss = 0, l1_miss = 0; };
struct Perf {
  int fd[4] = {-1, -1, -1, -1};
  static int open_ev(uint32_t type, uint64_t cfg) {
    perf_event_attr a; std::memset(&a, 0, sizeof a); a.size = sizeof a; a.type = type; a.config = cfg;
    a.disabled = 1; a.exclude_kernel = 1; a.exclude_hv = 1;
    return (int)syscall(SYS_perf_event_open, &a, 0, -1, -1, 0);
  }
  Perf() {
    fd[0] = open_ev(PERF_TYPE_HARDWARE, PERF_COUNT_HW_CPU_CYCLES);
    fd[1] = open_ev(PERF_TYPE_HARDWARE, PERF_COUNT_HW_INSTRUCTIONS);
    fd[2] = open_ev(PERF_TYPE_HARDWARE, PERF_COUNT_HW_BRANCH_MISSES);
    fd[3] = open_ev(PERF_TYPE_HW_CACHE, PERF_COUNT_HW_CACHE_L1D | (PERF_COUNT_HW_CACHE_OP_READ << 8) | (PERF_COUNT_HW_CACHE_RESULT_MISS << 16));
  }
  bool ok() const { return fd[0] >= 0 && fd[1] >= 0 && fd[2] >= 0; }
  void start() { for (int f : fd) if (f >= 0) { ioctl(f, PERF_EVENT_IOC_RESET, 0); ioctl(f, PERF_EVENT_IOC_ENABLE, 0); } }
  Counters stop() {
    Counters c; uint64_t v[4] = {0, 0, 0, 0};
    for (int i = 0; i < 4; i++) if (fd[i] >= 0) { ioctl(fd[i], PERF_EVENT_IOC_DISABLE, 0); if (read(fd[i], &v[i], 8) != 8) v[i] = 0; }
    c.cycles = v[0]; c.instr = v[1]; c.branch_miss = v[2]; c.l1_miss = v[3]; return c;
  }
};

// ------------------------------------------------------------------------------------------------ the engine under test
struct Result { double ms; Counters pmu; uint64_t evals, changed; };

struct Variant {
  std::string name, desc; size_t gate_bytes;
  virtual Result run(const std::vector<std::vector<int>> &toggles, Perf *perf) = 0;
  virtual uint64_t fingerprint(const Net &) const = 0;
  virtual ~Variant() = default;
};

template <class G, class P> struct Engine : Variant {
  std::vector<G *> gate;                      // id -> gate
  std::vector<G *> q0, q1;
  std::vector<std::unique_ptr<char[]>> junk;  // fragmentation filler (kept alive)

  uint64_t evals = 0, changed = 0;

  // wire hitlists in id order (identical for every variant)
  void wire(const Net &N) {
    for (int i = N.nin; i < N.n; i++)
      for (size_t p = 0; p < N.in[i].size(); p++) {
        int j = N.in[i][p];
        gate[j]->hit.push(gate[i], uint8_t(p), N.out[j], gate[i]->seed);
      }
    q0.resize(N.n); q1.resize(N.n);
  }
  void load_state(const Net &N) {
    for (int i = 0; i < N.n; i++) { gate[i]->output = N.out[i]; gate[i]->logic = N.logic[i]; if constexpr (std::is_same_v<G, OG>) { if (N.type[i] == VAR) gate[i]->value = N.out[i]; } }
  }

  void propagate(size_t end_point) {
    G **rq = q0.data(), **wq = q1.data(); size_t size = 0;
    uint64_t ev = 0, ch = 0;
    while (end_point > 0) {
      for (size_t index = 0; index < end_point; index++) {
        G *src = rq[index];
        P::clear_mark(src);
        uint8_t new_output = src->output;
        Prof<G> *pr = src->hit.data, *end = pr + src->hit.size;
        ev += src->hit.size;
        for (; pr < end; pr++) {
          uint8_t curr = (new_output == pr->seed);
          G *t = pr->target;
          t->logic += curr - pr->logic;
          uint8_t before = t->output;
          if (__builtin_expect(new_output == UNKNOWN, 0)) t->output = UNKNOWN; else P::eval(t);
          wq[size] = t;
          bool c = before != t->output;
          size += (!P::is_marked(t)) & c;
          P::set_mark(t, c);
          ch += c;
          pr->logic = curr;
        }
      }
      end_point = size; size = 0; std::swap(rq, wq);
    }
    evals += ev; changed += ch;
  }

  Result run(const std::vector<std::vector<int>> &toggles, Perf *perf) override {
    evals = changed = 0;
    if (perf) perf->start();
    auto t0 = std::chrono::steady_clock::now();
    for (const auto &tg : toggles) {
      size_t n = 0;
      for (int code : tg) {                    // code = id * 4 + mode; mode 2 toggles, mode 0/1 sets the value
        G *v = gate[code >> 2]; int mode = code & 3;
        uint8_t nv = (mode == 2) ? v->output ^ 1 : mode;
        if (nv == v->output || P::is_marked(v)) continue;
        v->output = nv; if constexpr (std::is_same_v<G, OG>) v->value = nv;
        q0[n++] = v; P::set_mark(v, true);
      }
      propagate(n);
    }
    auto t1 = std::chrono::steady_clock::now();
    Result r; r.pmu = perf ? perf->stop() : Counters{};
    r.ms = std::chrono::duration<double, std::milli>(t1 - t0).count(); r.evals = evals; r.changed = changed;
    return r;
  }
  uint64_t fingerprint(const Net &N) const override {   // FNV-1a over id-ordered outputs
    uint64_t h = 1469598103934665603ull;
    for (int i = 0; i < N.n; i++) { h ^= gate[i]->output + 1u; h *= 1099511628211ull; h ^= gate[i]->logic; h *= 1099511628211ull; }
    return h;
  }
};

static OG *make_og(uint8_t t, void *where) {
  switch (t) {
    case AND: return where ? new (where) OG_AND : new OG_AND;   case NAND: return where ? new (where) OG_NAND : new OG_NAND;
    case OR: return where ? new (where) OG_OR : new OG_OR;      case NOR: return where ? new (where) OG_NOR : new OG_NOR;
    case XOR: return where ? new (where) OG_XOR : new OG_XOR;   case XNOR: return where ? new (where) OG_XNOR : new OG_XNOR;
    case BUF: return where ? new (where) OG_BUF : new OG_BUF;   case NOT: return where ? new (where) OG_NOT : new OG_NOT;
    default: return where ? new (where) OG_VAR : new OG_VAR;
  }
}

struct HeapOOP : Engine<OG, PolVirtual> {
  HeapOOP(const Net &N, int frag, uint32_t seed) {
    name = "a heap+virtual"; gate_bytes = sizeof(OG); gate.assign(N.n, nullptr);
    std::mt19937 rng(seed ^ 0x9e3779b9u);
    std::vector<int> order(N.n); for (int i = 0; i < N.n; i++) order[N.slot[i]] = i;   // allocate in placement order
    for (int id : order) {
      gate[id] = make_og(N.type[id], nullptr);
      if (frag) junk.emplace_back(new char[8 + rng() % frag]);
    }
    for (int i = 0; i < N.n; i++) gate[i]->inputlimit = 0;
    wire(N); load_state(N);
  }
};
struct ArenaOOP : Engine<OG, PolVirtual> {
  void *arena = nullptr;
  ArenaOOP(const Net &N) {
    name = "b arena+virtual"; gate_bytes = sizeof(OG); gate.assign(N.n, nullptr);
    arena = std::aligned_alloc(64, ((size_t)N.n * sizeof(OG) + 63) / 64 * 64);
    for (int i = 0; i < N.n; i++) gate[i] = make_og(N.type[i], (char *)arena + (size_t)N.slot[i] * sizeof(OG));
    for (int i = 0; i < N.n; i++) gate[i]->inputlimit = 0;
    wire(N); load_state(N);
  }
};
template <class G, class P> struct Flat : Engine<G, P> {
  G *arr = nullptr;
  Flat(const Net &N, const char *nm) {
    this->name = nm; this->gate_bytes = sizeof(G); this->gate.assign(N.n, nullptr);
    arr = (G *)std::aligned_alloc(64, ((size_t)N.n * sizeof(G) + 63) / 64 * 64);
    for (int i = 0; i < N.n; i++) { G *g = new (&arr[N.slot[i]]) G(); init_flat(*g, N.type[i]); this->gate[i] = g; }
    this->wire(N); this->load_state(N);
  }
};

// ---- q: variant d with every hitlist's data copied into one shared block in placement order (as optimize() could do);
//      gate (24 B), lists, pointers and the propagate() loop are unchanged, only where the edge arrays live differs ----
struct FlatPacked : Flat<FG, PolSima<FG>> {
  Prof<FG> *block = nullptr;
  FlatPacked(const Net &N) : Flat<FG, PolSima<FG>>(N, "q flat24+packed") {
    size_t total = 0;
    for (int s = 0; s < N.n; s++) total += arr[s].hit.size;
    block = (Prof<FG> *)std::aligned_alloc(64, (total * sizeof(Prof<FG>) + 63) / 64 * 64 + 64);
    size_t off = 0;
    for (int s = 0; s < N.n; s++) {                          // slot order = memory order of the gates
      Hit<FG> &h = arr[s].hit;
      if (h.size) std::memcpy(block + off, h.data, h.size * sizeof(Prof<FG>));
      std::free(h.data); h.data = block + off; h.capacity = h.size; off += h.size;
    }
  }
};

// ---- index variants (i, k): the same propagate() loop with gates addressed by their array slot ----
struct IEdge { uint32_t target; uint8_t logic, seed, index; };          // 8 B (pointer Profile: 16 B)
static_assert(sizeof(IEdge) == 8, "unexpected edge size");
struct IHit { IEdge *data = nullptr; uint32_t size = 0, capacity = 0;   // 16 B, same growth policy as Hit
  void push(const IEdge &e) {
    if (size == capacity) { capacity = capacity ? capacity * 2 : 2; data = (IEdge *)std::realloc(data, capacity * sizeof(IEdge)); }
    data[size++] = e;
  }
};
struct IG24 { uint8_t flags = F_UPDATE, output = UNKNOWN, inputlimit = 0, mask = 0xFF, logic = 0, seed = 1; int8_t type = 0; uint8_t reserved = 0; IHit hit; };
struct IG16 { uint8_t flags = F_UPDATE, output = UNKNOWN, inputlimit = 0, mask = 0xFF, logic = 0, seed = 1; int8_t type = 0; uint8_t reserved = 0; uint32_t first = 0, count = 0; };
struct IG32 { uint8_t flags = F_UPDATE, output = UNKNOWN, inputlimit = 0, mask = 0xFF, logic = 0, seed = 1; int8_t type = 0; uint8_t reserved = 0; IHit hit; uint8_t pad[8] = {}; };
static_assert(sizeof(IG24) == 24 && sizeof(IG16) == 16 && sizeof(IG32) == 32, "unexpected index-gate sizes");

template <class G, bool CSR> struct IndexEngine : Variant {
  using P = PolSima<G>;
  G *arr = nullptr;
  std::vector<uint32_t> at;                   // id -> slot
  std::vector<IEdge> edges;                   // CSR only: all edges, grouped by source slot in placement order
  std::vector<uint32_t> q0, q1;
  uint64_t evals = 0, changed = 0;

  IndexEngine(const Net &N, const char *nm) {
    name = nm; gate_bytes = sizeof(G); at.resize(N.n);
    arr = (G *)std::aligned_alloc(64, ((size_t)N.n * sizeof(G) + 63) / 64 * 64);
    for (int i = 0; i < N.n; i++) { at[i] = N.slot[i]; G *g = new (&arr[at[i]]) G(); init_flat(*g, N.type[i]); }
    // edges in the same order as Engine::wire: target ids ascending, then pin
    std::vector<std::vector<IEdge>> per(CSR ? N.n : 0);
    for (int i = N.nin; i < N.n; i++)
      for (size_t p = 0; p < N.in[i].size(); p++) {
        int j = N.in[i][p]; G &t = arr[at[i]];
        IEdge e{at[i], uint8_t(N.out[j] == t.seed), t.seed, uint8_t(p)};
        if constexpr (CSR) per[at[j]].push_back(e); else arr[at[j]].hit.push(e);
      }
    if constexpr (CSR) {
      for (int s = 0; s < N.n; s++) { arr[s].first = (uint32_t)edges.size(); arr[s].count = (uint32_t)per[s].size(); edges.insert(edges.end(), per[s].begin(), per[s].end()); }
    }
    for (int i = 0; i < N.n; i++) { arr[at[i]].output = N.out[i]; arr[at[i]].logic = N.logic[i]; }
    q0.resize(N.n); q1.resize(N.n);
  }

  void propagate(size_t end_point) {
    uint32_t *rq = q0.data(), *wq = q1.data(); size_t size = 0;
    uint64_t ev = 0, ch = 0;
    G *const base = arr;
    while (end_point > 0) {
      for (size_t index = 0; index < end_point; index++) {
        G *src = base + rq[index];
        P::clear_mark(src);
        uint8_t new_output = src->output;
        IEdge *pr, *end;
        if constexpr (CSR) { pr = edges.data() + src->first; end = pr + src->count; }
        else { pr = src->hit.data; end = pr + src->hit.size; }
        ev += end - pr;
        for (; pr < end; pr++) {
          uint8_t curr = (new_output == pr->seed);
          G *t = base + pr->target;
          t->logic += curr - pr->logic;
          uint8_t before = t->output;
          if (__builtin_expect(new_output == UNKNOWN, 0)) t->output = UNKNOWN; else P::eval(t);
          wq[size] = pr->target;
          bool c = before != t->output;
          size += (!P::is_marked(t)) & c;
          P::set_mark(t, c);
          ch += c;
          pr->logic = curr;
        }
      }
      end_point = size; size = 0; std::swap(rq, wq);
    }
    evals += ev; changed += ch;
  }

  Result run(const std::vector<std::vector<int>> &toggles, Perf *perf) override {
    evals = changed = 0;
    if (perf) perf->start();
    auto t0 = std::chrono::steady_clock::now();
    for (const auto &tg : toggles) {
      size_t n = 0;
      for (int code : tg) {
        uint32_t s = at[code >> 2]; G *v = arr + s; int mode = code & 3;
        uint8_t nv = (mode == 2) ? v->output ^ 1 : mode;
        if (nv == v->output || P::is_marked(v)) continue;
        v->output = nv; q0[n++] = s; P::set_mark(v, true);
      }
      propagate(n);
    }
    auto t1 = std::chrono::steady_clock::now();
    Result r; r.pmu = perf ? perf->stop() : Counters{};
    r.ms = std::chrono::duration<double, std::milli>(t1 - t0).count(); r.evals = evals; r.changed = changed;
    return r;
  }
  uint64_t fingerprint(const Net &N) const override {
    uint64_t h = 1469598103934665603ull;
    for (int i = 0; i < N.n; i++) { const G &g = arr[at[i]]; h ^= g.output + 1u; h *= 1099511628211ull; h ^= g.logic; h *= 1099511628211ull; }
    return h;
  }
};

// ---- p: CSR with pointer edges (16-byte gate, one contiguous 16-byte-edge array, pointer queues) ----
struct PG16;
struct PEdge { PG16 *target; uint8_t logic, seed, index; };             // 16 B, as the pointer Profile
struct PG16 { uint8_t flags = F_UPDATE, output = UNKNOWN, inputlimit = 0, mask = 0xFF, logic = 0, seed = 1; int8_t type = 0; uint8_t reserved = 0; uint32_t first = 0, count = 0; };
static_assert(sizeof(PG16) == 16 && sizeof(PEdge) == 16, "unexpected pointer-CSR sizes");

struct CsrPtrEngine : Variant {
  using G = PG16; using P = PolSima<G>;
  G *arr = nullptr;
  std::vector<uint32_t> at;
  std::vector<PEdge> edges;
  std::vector<G *> q0, q1;
  uint64_t evals = 0, changed = 0;

  CsrPtrEngine(const Net &N) {
    name = "p flat16+CSR+ptr"; gate_bytes = sizeof(G); at.resize(N.n);
    arr = (G *)std::aligned_alloc(64, ((size_t)N.n * sizeof(G) + 63) / 64 * 64);
    for (int i = 0; i < N.n; i++) { at[i] = N.slot[i]; G *g = new (&arr[at[i]]) G(); init_flat(*g, N.type[i]); }
    std::vector<std::vector<PEdge>> per(N.n);
    for (int i = N.nin; i < N.n; i++)
      for (size_t p = 0; p < N.in[i].size(); p++) {
        int j = N.in[i][p]; G &t = arr[at[i]];
        per[at[j]].push_back(PEdge{&t, uint8_t(N.out[j] == t.seed), t.seed, uint8_t(p)});
      }
    for (int s = 0; s < N.n; s++) { arr[s].first = (uint32_t)edges.size(); arr[s].count = (uint32_t)per[s].size(); edges.insert(edges.end(), per[s].begin(), per[s].end()); }
    for (int i = 0; i < N.n; i++) { arr[at[i]].output = N.out[i]; arr[at[i]].logic = N.logic[i]; }
    q0.resize(N.n); q1.resize(N.n);
  }

  void propagate(size_t end_point) {
    G **rq = q0.data(), **wq = q1.data(); size_t size = 0;
    uint64_t ev = 0, ch = 0;
    PEdge *const E = edges.data();
    while (end_point > 0) {
      for (size_t index = 0; index < end_point; index++) {
        G *src = rq[index];
        P::clear_mark(src);
        uint8_t new_output = src->output;
        PEdge *pr = E + src->first, *end = pr + src->count;
        ev += src->count;
        for (; pr < end; pr++) {
          uint8_t curr = (new_output == pr->seed);
          G *t = pr->target;
          t->logic += curr - pr->logic;
          uint8_t before = t->output;
          if (__builtin_expect(new_output == UNKNOWN, 0)) t->output = UNKNOWN; else P::eval(t);
          wq[size] = t;
          bool c = before != t->output;
          size += (!P::is_marked(t)) & c;
          P::set_mark(t, c);
          ch += c;
          pr->logic = curr;
        }
      }
      end_point = size; size = 0; std::swap(rq, wq);
    }
    evals += ev; changed += ch;
  }

  Result run(const std::vector<std::vector<int>> &toggles, Perf *perf) override {
    evals = changed = 0;
    if (perf) perf->start();
    auto t0 = std::chrono::steady_clock::now();
    for (const auto &tg : toggles) {
      size_t n = 0;
      for (int code : tg) {
        G *v = arr + at[code >> 2]; int mode = code & 3;
        uint8_t nv = (mode == 2) ? v->output ^ 1 : mode;
        if (nv == v->output || P::is_marked(v)) continue;
        v->output = nv; q0[n++] = v; P::set_mark(v, true);
      }
      propagate(n);
    }
    auto t1 = std::chrono::steady_clock::now();
    Result r; r.pmu = perf ? perf->stop() : Counters{};
    r.ms = std::chrono::duration<double, std::milli>(t1 - t0).count(); r.evals = evals; r.changed = changed;
    return r;
  }
  uint64_t fingerprint(const Net &N) const override {
    uint64_t h = 1469598103934665603ull;
    for (int i = 0; i < N.n; i++) { const G &g = arr[at[i]]; h ^= g.output + 1u; h *= 1099511628211ull; h ^= g.logic; h *= 1099511628211ull; }
    return h;
  }
};

// ------------------------------------------------------------------------------------------------ driver
static double median(std::vector<double> v) { std::sort(v.begin(), v.end()); size_t n = v.size(); return n % 2 ? v[n / 2] : 0.5 * (v[n / 2 - 1] + v[n / 2]); }

int main(int argc, char **argv) {
  std::string topo = "random", variants = "abcd", only, netlist;
  int n = 100000, iters = 0, target_evals = 8000000, reps = 9, window = 64, frag = 0; double activity = 0.1; bool shuffle = false, vary = false; uint32_t seed = 42;
  for (int i = 1; i < argc; i++) {
    std::string a = argv[i]; auto nx = [&]() { return std::string(argv[++i]); };
    if (a == "--topology") topo = nx(); else if (a == "--n") n = std::stoi(nx()); else if (a == "--iters") iters = std::stoi(nx());
    else if (a == "--reps") reps = std::stoi(nx()); else if (a == "--window") window = std::stoi(nx());
    else if (a == "--activity") activity = std::stod(nx()); else if (a == "--shuffle") shuffle = true; else if (a == "--vary") vary = true;
    else if (a == "--frag") frag = std::stoi(nx()); else if (a == "--variants") variants = nx(); else if (a == "--only") only = nx();
    else if (a == "--target-evals") target_evals = std::stoi(nx());
    else if (a == "--netlist") netlist = nx();
    else if (a == "--seed") seed = std::stoul(nx());
    else { std::fprintf(stderr, "unknown option %s\n", a.c_str()); return 2; }
  }
  if (!only.empty()) variants = only;
  std::vector<std::vector<int>> file_vecs; size_t cursor = 0;
  Net N = netlist.empty() ? make_net(topo, n, window, seed, shuffle) : load_net(netlist, shuffle, seed, file_vecs);
  if (!netlist.empty()) topo = "netlist";
  std::vector<std::unique_ptr<Variant>> vs;
  for (char c : variants) {
    if (c == 'a') vs.emplace_back(new HeapOOP(N, frag, seed));
    else if (c == 'b') vs.emplace_back(new ArenaOOP(N));
    else if (c == 'c') vs.emplace_back(new Flat<FG, PolSwitch<FG>>(N, "c flat24+switch"));
    else if (c == 'd') vs.emplace_back(new Flat<FG, PolSima<FG>>(N, "d flat24+SIMA"));
    else if (c == 'g') vs.emplace_back(new Flat<FG40, PolSima<FG40>>(N, "g flat40+SIMA"));
    else if (c == 'e') vs.emplace_back(new Flat<FG32, PolSima<FG32>>(N, "e flat32+SIMA"));
    else if (c == 'i') vs.emplace_back(new IndexEngine<IG24, false>(N, "i flat24+idx"));
    else if (c == 'k') vs.emplace_back(new IndexEngine<IG16, true>(N, "k flat16+CSR"));
    else if (c == 'j') vs.emplace_back(new IndexEngine<IG32, false>(N, "j flat32+idx"));
    else if (c == 'p') vs.emplace_back(new CsrPtrEngine(N));
    else if (c == 'q') vs.emplace_back(new FlatPacked(N));
  }
  auto toggle_vec = [&](std::mt19937 &g) {
    if (!file_vecs.empty()) return file_vecs[cursor++ % file_vecs.size()];
    std::vector<int> v;
    if (topo == "chain" || (topo == "mixchain" && !vary)) v = {2};
    else if (topo == "mixchain") { for (int i = 3; i < N.nin; i++) if (g() < 0.1 * 4294967296.0) v.push_back(i * 4 + 2); if (v.empty()) v.push_back(int(3 + g() % (N.nin - 3)) * 4 + 2); }
    else { for (int i = 0; i < N.nin; i++) if (g() < activity * 4294967296.0) v.push_back(i * 4 + 2);
           if (v.empty()) v.push_back(int(g() % N.nin) * 4 + 2); }
    return v;
  };
  if (iters == 0) {                             // --iters 0: pick the iteration count so one rep does about --target-evals edge visits
    Flat<FG, PolSima<FG>> probe(N, "probe"); std::mt19937 g(seed + 7); int k = 1; uint64_t ev = 0;
    for (; k <= 4096 && ev < 200000; k *= 2) { std::vector<std::vector<int>> t(k); for (auto &x : t) x = toggle_vec(g); ev = probe.run(t, nullptr).evals; }
    iters = std::max<int>(1, (int)((double)target_evals * (k / 2 ? k / 2 : 1) / std::max<uint64_t>(ev, 1)));
    cursor = 0;
  }
  Perf perf; Perf *pp = perf.ok() ? &perf : nullptr;
  std::printf("# topology=%s gates=%d inputs=%d window=%d placement=%s frag=%d activity=%.2f iters=%d reps=%d sizeof(OOP)=%zu sizeof(flat)=%zu\n",
              topo.c_str(), N.n, N.nin, window, shuffle ? "shuffled" : "topological", frag, activity, iters, reps, sizeof(OG), sizeof(FG));

  std::mt19937 rng(seed + 1);
  auto make_toggles = [&]() {
    std::vector<std::vector<int>> t(iters);
    for (auto &v : t) v = toggle_vec(rng);
    return t;
  };
  std::map<std::string, std::vector<double>> ms; std::map<std::string, std::vector<Counters>> pm;
  std::map<std::string, std::vector<double>> evs; std::map<std::string, Result> last; bool mismatch = false;
  for (int rep = -1; rep < reps; rep++) {   // rep -1 is the warm-up and is not recorded
    auto tg = make_toggles();
    uint64_t ref_fp = 0, ref_ev = 0, ref_ch = 0; bool first = true;
    for (size_t k = 0; k < vs.size(); k++) {
      auto &v = vs[(k + (rep < 0 ? 0 : rep)) % vs.size()];              // rotate the order each rep (interleaving)
      Result r = v->run(tg, pp);
      uint64_t fp = v->fingerprint(N);
      if (first) { ref_fp = fp; ref_ev = r.evals; ref_ch = r.changed; first = false; }
      else if (fp != ref_fp || r.evals != ref_ev || r.changed != ref_ch) {
        mismatch = true; std::fprintf(stderr, "MISMATCH rep %d %s: fp %llx/%llx evals %llu/%llu changed %llu/%llu\n", rep, v->name.c_str(),
          (unsigned long long)fp, (unsigned long long)ref_fp, (unsigned long long)r.evals, (unsigned long long)ref_ev, (unsigned long long)r.changed, (unsigned long long)ref_ch);
      }
      if (rep >= 0) { ms[v->name].push_back(r.ms * 1e6 / r.evals); pm[v->name].push_back(r.pmu); evs[v->name].push_back((double)r.evals); }
      last[v->name] = r; last[v->name].pmu.cycles = last[v->name].pmu.cycles;
    }
  }
  // ms[] holds ns per gate evaluation for each rep (work differs between reps because the input vectors do);
  // the last column is the median of the per-rep ratios against the first variant, which are paired by rep.
  std::printf("%-18s %5s %9s %9s %9s %7s %9s %7s %9s %9s %s\n", "variant", "B/gate", "med ns/ev", "min", "max", "spread", "cyc/eval", "IPC", "brmiss/ev", "L1miss/ev", "time vs first (paired median)");
  for (auto &v : vs) {
    auto &m = ms[v->name]; double med = median(m), mn = *std::min_element(m.begin(), m.end()), mx = *std::max_element(m.begin(), m.end());
    std::vector<double> cyc, ipc, bm, l1, ratio;
    for (size_t r = 0; r < m.size(); r++) {
      const Counters &c = pm[v->name][r]; double e = evs[v->name][r];
      cyc.push_back(c.cycles / e); ipc.push_back(c.cycles ? (double)c.instr / c.cycles : 0); bm.push_back(c.branch_miss / e); l1.push_back(c.l1_miss / e);
      ratio.push_back(m[r] / ms[vs[0]->name][r]);
    }
    std::printf("%-18s %5zu %9.2f %9.2f %9.2f %6.1f%% %9.2f %7.2f %9.4f %9.4f  x%.3f\n", v->name.c_str(), v->gate_bytes, med, mn, mx,
                100.0 * (mx - mn) / med, median(cyc), median(ipc), median(bm), median(l1), median(ratio));
  }
  std::printf("# evals/rep=%llu changed/rep=%llu fingerprint-check=%s\n", (unsigned long long)last[vs[0]->name].evals, (unsigned long long)last[vs[0]->name].changed, mismatch ? "MISMATCH" : "identical");
  return mismatch ? 1 : 0;
}
