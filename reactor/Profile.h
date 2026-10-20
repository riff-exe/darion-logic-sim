// reactor/Profile.h
#ifndef PROFILE_H
#define PROFILE_H
#include <algorithm>
#include <cstddef> // offsetof
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <utility>

struct CPP_Gate;

struct Profile {
  CPP_Gate *target; // offset 0 (8 B) - HOTTEST: downstream gate pointer
  uint8_t logic;    // offset 8 (1 B) - HOTTEST: (output == seed) boolean
  uint8_t seed;     // offset 9 (1 B) - WARM: cached target->seed
  uint8_t index;    // offset 10 (1 B) - COLD: pin index
  Profile() : target(nullptr), logic(0), seed(0), index(0) {}
  Profile(CPP_Gate *t, uint8_t i, uint8_t l, uint8_t s) : target(t), logic(l), seed(s), index(i) {}
  inline Profile(CPP_Gate *t, uint8_t i, uint8_t o);
  bool operator<(const Profile &other) const { return target < other.target; }
};

// ─── Task ─────────────────────────────────────────────────────────────────
struct Task {
  int gate_loc;
  unsigned int time;
  Task() : gate_loc(-1), time(0) {}
  Task(int g, unsigned int t) : gate_loc(g), time(t) {}
  bool operator>(const Task &other) const {
    if (time != other.time)
      return time > other.time;
    return gate_loc > other.gate_loc;
  }
};
// ──────────────────────────────────────────────────────────────────────────

// ─── HitList (Dynamic Array) ──────────────────────────────────────────────
struct HitList {
  Profile *data;
  uint32_t size;
  uint32_t capacity;

  HitList() noexcept : data(nullptr), size(0), capacity(0) {}

  ~HitList() noexcept {
    if (data) {
      std::free(data);
      data = nullptr;
    }
    size = 0;
    capacity = 0;
  }

  HitList(const HitList &other) : data(nullptr), size(0), capacity(0) {
    if (other.size > 0) {
      data = static_cast<Profile *>(std::malloc(other.size * sizeof(Profile)));
      if (data) {
        std::memcpy(data, other.data, other.size * sizeof(Profile));
        size = other.size;
        capacity = other.size;
      }
    }
  }

  HitList &operator=(const HitList &other) {
    if (this == &other) {
      return *this;
    }

    if (capacity < other.size) {
      Profile *new_data = static_cast<Profile *>(
          std::realloc(data, other.size * sizeof(Profile)));
      if (!new_data) {
        return *this;
      }
      data = new_data;
      capacity = other.size;
    }
    if (other.size)
      std::memcpy(data, other.data, other.size * sizeof(Profile));
    size = other.size;
    return *this;
  }

  HitList &operator=(HitList &&other) noexcept {
    if (this == &other) {
      return *this;
    }
    if (data) {
      std::free(data);
    }
    data = other.data;
    size = other.size;
    capacity = other.capacity;
    other.capacity = 0;
    other.size = 0;
    other.data = nullptr;
    return *this;
  }
  HitList(HitList &&other) noexcept {
    data = other.data;
    size = other.size;
    capacity = other.capacity;
    other.capacity = 0;
    other.size = 0;
    other.data = nullptr;
  }

  void swap(HitList &other) noexcept {
    std::swap(data, other.data);
    std::swap(size, other.size);
    std::swap(capacity, other.capacity);
  }

  inline bool empty() const noexcept { return size == 0; }
  inline Profile *begin() noexcept { return data; }
  inline const Profile *begin() const noexcept { return data; }
  inline Profile *end() noexcept { return data + size; }
  inline const Profile *end() const noexcept { return data + size; }

  inline Profile &operator[](size_t idx) noexcept { return data[idx]; }
  inline const Profile &operator[](size_t idx) const noexcept {
    return data[idx];
  }

  inline void push_back(const Profile &p) {
    if (size == capacity) {
      capacity = (capacity == 0) ? 2 : capacity * 2;
      data = static_cast<Profile *>(
          std::realloc(data, capacity * sizeof(Profile)));
    }
    data[size++] = p;
  }

  inline void emplace_back(CPP_Gate *t, uint8_t i, uint8_t o);
};
// ──────────────────────────────────────────────────────────────────────────

struct CPP_Gate {
  // ── HOTTEST SCALARS (Bytes 0–7) ───────────────────────────────────────────
  // Ordered strictly from hottest to coldest based on Linux hardware PMU
  // profiling:
  //   offset 0: flags       (uint8_t, 1 B) — #1 HOTTEST: mark, update, and negate bits (~35% cycles)
  //   offset 1: output      (uint8_t, 1 B) — #2 HOTTEST: wire logic state (checked & updated)
  //   offset 2: inputlimit  (uint8_t, 1 B) — #3 HOT: guard for unresolved inputs / error state
  //   offset 3: mask        (uint8_t, 1 B) — #4 HOT: masking logic for branchless gate evaluation
  //   offset 4: logic       (uint8_t, 1 B) — #5 WARM: active input accumulator counter
  //   offset 5: seed        (uint8_t, 1 B) — #6 WARM: triggering input value invariant
  //   offset 6: type        (int8_t,  1 B) — #7 COLD: gate type ID (used only in oscillator fallback)
  //   offset 7: reserved    (uint8_t, 1 B) — [1 B natural padding aligning 8-B hitlist pointer]
  // ── HITLIST (Bytes 8–23) ─────────────────────────────────────────────────
  //   offset 8: hitlist     (HitList, 16 B, 8-B aligned: Profile* data [8B], uint32_t size [4B], uint32_t capacity [4B])
  uint8_t flags;
  uint8_t output;
  uint8_t inputlimit;
  uint8_t mask;
  uint8_t logic;
  uint8_t seed;
  int8_t type;
  uint8_t reserved;
  HitList hitlist; // 16 B; offset 8 (8-byte aligned)

#ifdef DARION_EVAL_SWITCH
  // Ablation only (build with -DDARION_EVAL_SWITCH, see tests/ablation_eval.py): a type-switch evaluator over
  // the same accumulators, used to isolate the benefit of the unified mask/invert rule below.
  inline uint8_t compute() noexcept {
    if (inputlimit) return 2;
    switch (type) {
    case 0: return logic == 0;   // AND  (logic = #zeros)
    case 1: return logic != 0;   // NAND
    case 2: return logic != 0;   // OR   (logic = #ones)
    case 3: return logic == 0;   // NOR
    case 4: return logic & 1;    // XOR
    case 5: return !(logic & 1); // XNOR
    default: return logic != 0;  // NOT (#zeros), BUFFER and pins (#ones)
    }
  }
  inline void evaluate() noexcept { output = compute(); }
#else
  inline void evaluate() noexcept {
    if (!inputlimit) {
      output = bool(logic & mask) ^ (flags & 1);
    } else {
      output = 2;
    }
  }
  inline uint8_t compute() noexcept {
    if (!inputlimit) {
      return bool(logic & mask) ^ (flags & 1);
    } else {
      return 2;
    }
  }
#endif
  CPP_Gate()
      : flags(0), output(2), inputlimit(2), mask(0xFF), logic(0), seed(1),
        type(0), reserved(2), hitlist() {}
  CPP_Gate(uint8_t t, uint8_t lim)
      : flags(0), output(2), inputlimit(lim), mask(0xFF), logic(0), seed(1),
        type(t), reserved(lim), hitlist() {}
};

inline Profile::Profile(CPP_Gate *t, uint8_t i, uint8_t o) : target(t), index(i) {
  if (t) {
    seed = t->seed;
    logic = (o == seed);
  } else {
    seed = 0;
    logic = 0;
  }
}

inline void HitList::emplace_back(CPP_Gate *t, uint8_t i, uint8_t o) {
  if (size == capacity) {
    capacity = (capacity == 0) ? 2 : capacity * 2;
    data = static_cast<Profile *>(
        std::realloc(data, capacity * sizeof(Profile)));
  }
  data[size++] = Profile(t, i, o);
}

// Compile-time assertion: hitlist must be 8-byte aligned at offset 8, and total
// size exactly 24 bytes.
static_assert(
    offsetof(CPP_Gate, hitlist) == 8,
    "CPP_Gate: hitlist must be at offset 8 for optimal 8-byte alignment");
static_assert(sizeof(CPP_Gate) == 24,
              "CPP_Gate: struct size must be exactly 24 bytes");
static_assert(sizeof(Profile) == 16,
              "Profile: struct size must be exactly 16 bytes");
#endif
