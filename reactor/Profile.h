// reactor/Profile.h
#ifndef PROFILE_H
#define PROFILE_H
#include <cstddef> // offsetof
#include <cstdint>
#include <stdint.h>
#include <vector>

struct CPP_Gate;

struct Profile {
  CPP_Gate *target; // offset 0 (8 B) - HOTTEST: downstream gate pointer
  uint8_t output;   // offset 8 (1 B) - HOTTEST SCALAR: wire state (read + written)
  uint8_t index;    // offset 9 (1 B) - COLD: pin index (used only in connect/disconnect)
  Profile() : target(nullptr), output(0), index(0) {}
  Profile(CPP_Gate *t, uint8_t i, uint8_t o) : target(t), output(o), index(i) {}
  bool operator<(const Profile &other) const { return target < other.target; }
};

// ─── Task ─────────────────────────────────────────────────────────────────
struct Task {
  int gate_loc;
  unsigned int time;
  int location;
  Task() : gate_loc(-1), time(0), location(0) {}
  Task(int g, unsigned int t, int loc) : gate_loc(g), time(t), location(loc) {}
  bool operator>(const Task &other) const {
    if (time != other.time)
      return time > other.time;
    return location > other.location;
  }
};
// ──────────────────────────────────────────────────────────────────────────

struct CPP_Gate {
  // ── HOTTEST SCALARS (Bytes 0–7) ───────────────────────────────────────────
  // Ordered strictly from hottest to coldest based on Linux hardware PMU profiling:
  //   offset 0: flags       (uint8_t, 1 B) — #1 HOTTEST: mark, update, and negate bits (~35% cycles)
  //   offset 1: output      (uint8_t, 1 B) — #2 HOTTEST: wire logic state (checked & updated)
  //   offset 2: inputlimit  (uint8_t, 1 B) — #3 HOT: guard for unresolved inputs / error state
  //   offset 3: mask        (uint8_t, 1 B) — #4 HOT: masking logic for branchless gate evaluation
  //   offset 4: logic       (uint8_t, 1 B) — #5 WARM: active input accumulator counter
  //   offset 5: seed        (uint8_t, 1 B) — #6 WARM: triggering input value invariant
  //   offset 6: type        (int8_t,  1 B) — #7 COLD: gate type ID (used only in oscillator fallback)
  //   offset 7: reserved    (uint8_t, 1 B) — [1 B natural padding aligning 8-B hitlist pointer]
  // ── HITLIST (Bytes 8–31) ─────────────────────────────────────────────────
  //   offset 8: hitlist     (std::vector<Profile>, 24 B, 8-B aligned)
  uint8_t flags;
  uint8_t output;
  uint8_t inputlimit;
  uint8_t mask;
  uint8_t logic;
  uint8_t seed;
  int8_t type;
  uint8_t reserved;
  std::vector<Profile> hitlist; // 24 B; offset 8 (8-byte aligned)

  inline void evaluate() noexcept {
    if (!inputlimit) {
      output = bool(logic & mask) ^ (flags & 1);
    } else {
      output = 2;
    }
  }

  CPP_Gate()
      : flags(0), output(2), inputlimit(2), mask(0xFF), logic(0), seed(1),
        type(0), reserved(0), hitlist() {}
  CPP_Gate(uint8_t t, uint8_t lim)
      : flags(0), output(2), inputlimit(lim), mask(0xFF), logic(0),
        seed(1), type(t), reserved(0), hitlist() {}
};

// Compile-time assertion: hitlist must be 8-byte aligned at offset 8, and total
// size exactly 32 bytes.
static_assert(
    offsetof(CPP_Gate, hitlist) == 8,
    "CPP_Gate: hitlist must be at offset 8 for optimal 8-byte alignment");
static_assert(sizeof(CPP_Gate) == 32,
              "CPP_Gate: struct size must be exactly 32 bytes");
#endif
