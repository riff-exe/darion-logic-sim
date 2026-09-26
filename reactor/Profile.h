// reactor/Profile.h
#ifndef PROFILE_H
#define PROFILE_H
#include <cstddef> // offsetof
#include <stdint.h>
#include <vector>

struct CPP_Gate;

struct Profile {
  CPP_Gate *target;
  int next;
  uint8_t index;
  uint8_t output;
  Profile() : target(nullptr), next(-1), index(0), output(0) {}
  Profile(CPP_Gate *t, uint8_t i, uint8_t o, int n = -1) : target(t), next(n), index(i), output(o) {}
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

// Bitmask Definitions
// (must stay in sync with Const.pxd)
static constexpr uint8_t GATE_LOGIC_1 =
    1 << 4; // 16  — all-low trigger  (AND, NOR)
static constexpr uint8_t GATE_LOGIC_2 =
    1 << 5; // 32  — any-high trigger (OR, NAND, NOT, Buffer)
static constexpr uint8_t GATE_LOGIC_3 =
    1 << 6; // 64  — dual-mode       (XOR, XNOR)

struct CPP_Gate {
  // ── HOT SCALARS (16 B total, exactly 4 gates fit in a 64-byte cache line) ──
  //
  //   offset  0: type         (int8_t,   1 B)
  //   offset  1: output       (uint8_t,  1 B)
  //   offset  2: inputlimit   (uint8_t,  1 B)
  //   offset  3: flags        (uint8_t,  1 B)
  //   offset  4: logic        (uint8_t,  1 B)
  //   offset  5: seed         (uint8_t,  1 B)
  //   offset  6: hitlist_count(uint16_t, 2 B)
  //   offset  8: target_time  (uint32_t, 4 B)
  //   offset 12: hitlist      (int32_t,  4 B) -> head index in profiles vector (-1 if none)
  // ──────────────────────────────────────────────────────────────────────────
  int8_t type;
  uint8_t output;
  uint8_t inputlimit;
  uint8_t flags;
  uint8_t logic;
  uint8_t seed;
  uint16_t hitlist_count;
  unsigned int target_time;
  int hitlist;

  inline void compute() noexcept {
    if (inputlimit) {
      // Check 1: gate has unresolved inputs — hold ERROR state
      output = 2;
    } else if (!(flags & GATE_LOGIC_3)) {
      output = (((logic == 0) & bool(flags & GATE_LOGIC_1)) |
                ((logic > 0) & bool(flags & GATE_LOGIC_2)));

    } else {
      output = (logic & 1) ^ (flags & 1);
    }
  }

  // flag is 8 means it's not going to support the ui, 0 means supported
  CPP_Gate()
      : type(0), output(2), inputlimit(2), flags(0), logic(0), seed(1),
        hitlist_count(0), target_time(0), hitlist(-1) {}
  CPP_Gate(uint8_t t, uint8_t lim)
      : type(t), output(2), inputlimit(lim), flags(0), logic(0),
        seed(t < 2 ? 0 : 1), hitlist_count(0), target_time(0), hitlist(-1) {}
};

// Compile-time assertion: hot scalars must all fit before the hitlist index.
// If the struct layout ever drifts, this will fail at compile time.
static_assert(
    offsetof(CPP_Gate, hitlist) >= 12,
    "CPP_Gate: hot scalars overflowed into hitlist — check field order");
static_assert(
    sizeof(CPP_Gate) == 16,
    "CPP_Gate must be 16 bytes for cache line packing");
#endif