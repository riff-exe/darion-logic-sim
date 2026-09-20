// reactor/Profile.h
#ifndef PROFILE_H
#define PROFILE_H
#include <cstddef> // offsetof
#include <stdint.h>
#include <vector>

struct CPP_Gate;

struct Profile {
  CPP_Gate *target;
  uint8_t index;
  uint8_t output;
  Profile() : target(nullptr), index(0), output(0) {}
  Profile(CPP_Gate *t, uint8_t i, uint8_t o) : target(t), index(i), output(o) {}
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

struct CPP_Gate {
  // ── HOT DATA ON TOP ──────────────────────────────────────────────────────
  uint8_t output;  // offset 0 (1 B)
  uint8_t flags;   // offset 1 (1 B)
  uint8_t invalid; // offset 2 (1 B): count of unconnected inputs (0 = valid)
  uint8_t limit;   // offset 3 (1 B): static count = sources.size() (or INFINITE
                   // for clock)
  uint8_t logic;   // offset 4 (1 B): matching input tally
  uint8_t seed;    // offset 5 (1 B): matching target (0 for AND/NAND, 1 for others)
  // offset 6..7: 2 bytes natural padding for 8-byte aligned hitlist
  // ── HOT VECTORS ──────────────────────────────────────────────────────────
  std::vector<CPP_Gate *> hitlist; // offset  8 (24 B): target gates
  std::vector<CPP_Gate *> sources; // offset 32 (24 B): source gates
  // ── COLD DATA ON THE BOTTOM ──────────────────────────────────────────────
  int8_t type; // offset 56 (1 B)
  // offset 57..59: 3 bytes natural padding for 4-byte aligned target_time
  unsigned int target_time; // offset 60 (4 B)

  inline void compute() noexcept {
    if (invalid) {
      output = 2; // UNKNOWN
      return;
    }
    logic = 0;
    for (auto &src : sources) {
      logic += (src->output == seed);
    }
    if (flags & 16) {
      output = (logic == 0) ^ (flags & 1);
    } else if (flags & 32) {
      output = (logic > 0) ^ (flags & 1);
    } else {
      output = (logic & 1) ^ (flags & 1);
    }
  }

  // flag is 8 means it's not going to support the ui, 0 means supported
  CPP_Gate()
      : output(2), flags(0), invalid(2), limit(2), logic(0), seed(1),
        hitlist(), sources(2, nullptr), type(0), target_time(0) {}
  CPP_Gate(uint8_t t, uint8_t lim)
      : output(2), flags(0), invalid(lim), limit(lim), logic(0),
        seed(t < 2 ? 0 : 1), hitlist(), sources(lim, nullptr), type(t),
        target_time(0) {}
};

static_assert(sizeof(CPP_Gate) == 64, "CPP_Gate must be exactly 64 bytes (1 cache line)");
static_assert(offsetof(CPP_Gate, output) == 0, "output at offset 0");
static_assert(offsetof(CPP_Gate, flags) == 1, "flags at offset 1");
static_assert(offsetof(CPP_Gate, invalid) == 2, "invalid at offset 2");
static_assert(offsetof(CPP_Gate, limit) == 3, "limit at offset 3");
static_assert(offsetof(CPP_Gate, logic) == 4, "logic at offset 4");
static_assert(offsetof(CPP_Gate, seed) == 5, "seed at offset 5");
static_assert(offsetof(CPP_Gate, hitlist) == 8, "hitlist at offset 8");
static_assert(offsetof(CPP_Gate, sources) == 32, "sources at offset 32");
static_assert(offsetof(CPP_Gate, type) == 56, "type at offset 56");
static_assert(offsetof(CPP_Gate, target_time) == 60, "target_time at offset 60");
#endif