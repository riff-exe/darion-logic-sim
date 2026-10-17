// reactor_oop/Profile.h
#ifndef PROFILE_H
#define PROFILE_H
#include <algorithm>
#include <cstddef>
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <utility>

// ─── Forward declaration ───────────────────────────────────────────────────────
struct CPP_Gate;

enum LogicLevel : uint8_t {
    LOGIC_LOW     = 0,
    LOGIC_HIGH    = 1,
    LOGIC_UNKNOWN = 2
};

// ─── Profile (hitlist entry) ───────────────────────────────────────────────────
struct Profile {
    CPP_Gate* target; // offset 0 (8 B) - downstream gate pointer
    uint8_t   logic;  // offset 8 (1 B) - (output == seed) boolean
    uint8_t   seed;   // offset 9 (1 B) - cached target->seed
    uint8_t   index;  // offset 10 (1 B) - pin index
    Profile() : target(nullptr), logic(0), seed(0), index(0) {}
    Profile(CPP_Gate* t, uint8_t i, uint8_t l, uint8_t s) : target(t), logic(l), seed(s), index(i) {}
    inline Profile(CPP_Gate* t, uint8_t i, uint8_t o);
    bool operator<(const Profile& other) const { return target < other.target; }
};

// ─── Task ─────────────────────────────────────────────────────────────────────
struct Task {
    int          gate_loc;
    unsigned int time;
    int          location;
    Task() : gate_loc(-1), time(0), location(0) {}
    Task(int g, unsigned int t, int loc) : gate_loc(g), time(t), location(loc) {}
    bool operator>(const Task& other) const {
        if (time != other.time) return time > other.time;
        return location > other.location;
    }
};

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

// ==============================================================================
// CPP_Gate — polymorphic base.
//
// Each gate type is a subclass that overrides compute().
// Cython accesses fields via named member access (ptr->field), which the C++
// compiler resolves correctly — the vtable pointer is transparent to Cython.
//
// Gate IDs (Const.pxd):
//   0=AND  1=NAND  2=OR  3=NOR  4=XOR  5=XNOR
//   6=BUFFER  7=NOT  8=IC_INPUT_PIN  9=VARIABLE  10=IC_OUTPUT_PIN  11=IC
//
// inputlimit — number of unresolved (not-yet-connected) inputs.
//              inputlimit == 0  →  all inputs resolved, compute() is valid.
//              inputlimit  > 0  →  pending inputs, output must stay UNKNOWN.
//
// logic  — count of connected inputs whose current output == seed.
// seed   — the "triggering" value for this gate type:
//            seed=0 (LOW)  for AND/NAND  (count LOWs to detect a 0-pulling input)
//            seed=1 (HIGH) for OR/NOR/XOR/XNOR/BUFFER/NOT/IC_Input/IC_Output
// ==============================================================================
struct CPP_Gate {
    int8_t               type;
    uint8_t              output;
    uint8_t              inputlimit;
    uint8_t              mark;
    uint8_t              update;
    uint8_t              value;
    uint8_t              scheduled;
    uint8_t              logic;       // count of inputs matching seed
    uint8_t              seed;        // triggering input value for this gate type
    HitList              hitlist;

    CPP_Gate() : type(0), output(LOGIC_UNKNOWN),
                 inputlimit(2), mark(0), update(1), value(0), scheduled(0), logic(0), seed(1), hitlist() {}
    CPP_Gate(int8_t t, uint8_t lim) : type(t), output(LOGIC_UNKNOWN),
              inputlimit(lim), mark(0), update(1), value(0), scheduled(0), logic(0), seed(1), hitlist() {}

    virtual void compute() noexcept { output = LOGIC_UNKNOWN; }
    virtual ~CPP_Gate() = default;
};

// ─── Typed gate subclasses ────────────────────────────────────────────────────

// AND (id=0): HIGH iff no LOW input  → seed=0, HIGH when logic==0
struct AND_Gate : CPP_Gate {
    AND_Gate(uint8_t lim) : CPP_Gate(0, lim) { seed = 0; }
    inline void compute() noexcept override { output = inputlimit ? LOGIC_UNKNOWN : (logic == 0); }
};

// NAND (id=1): LOW iff no LOW input (inverted AND) → seed=0, HIGH when logic>0
struct NAND_Gate : CPP_Gate {
    NAND_Gate(uint8_t lim) : CPP_Gate(1, lim) { seed = 0; }
    inline void compute() noexcept override { output = inputlimit ? LOGIC_UNKNOWN : (logic > 0); }
};

// OR (id=2): HIGH iff any HIGH input → seed=1, HIGH when logic>0
struct OR_Gate : CPP_Gate {
    OR_Gate(uint8_t lim) : CPP_Gate(2, lim) { seed = 1; }
    inline void compute() noexcept override { output = inputlimit ? LOGIC_UNKNOWN : (logic > 0); }
};

// NOR (id=3): HIGH iff no HIGH input (inverted OR) → seed=1, HIGH when logic==0
struct NOR_Gate : CPP_Gate {
    NOR_Gate(uint8_t lim) : CPP_Gate(3, lim) { seed = 1; }
    inline void compute() noexcept override { output = inputlimit ? LOGIC_UNKNOWN : (logic == 0); }
};

// XOR (id=4): HIGH iff odd HIGH count → seed=1, HIGH when logic&1
struct XOR_Gate : CPP_Gate {
    XOR_Gate(uint8_t lim) : CPP_Gate(4, lim) { seed = 1; }
    inline void compute() noexcept override { output = inputlimit ? LOGIC_UNKNOWN : (logic & 1); }
};

// XNOR (id=5): HIGH iff even HIGH count (inverted XOR) → seed=1, HIGH when (logic&1)^1
struct XNOR_Gate : CPP_Gate {
    XNOR_Gate(uint8_t lim) : CPP_Gate(5, lim) { seed = 1; }
    inline void compute() noexcept override { output = inputlimit ? LOGIC_UNKNOWN : ((logic & 1) ^ 1); }
};

// BUFFER (id=6): pass-through, 1 input → seed=1, HIGH when logic>0
struct BUFFER_Gate : CPP_Gate {
    BUFFER_Gate() : CPP_Gate(6, 1) { seed = 1; }
    inline void compute() noexcept override { output = inputlimit ? LOGIC_UNKNOWN : (logic > 0); }
};

// NOT (id=7): inverter, 1 input → seed=1, HIGH when logic==0
struct NOT_Gate : CPP_Gate {
    NOT_Gate() : CPP_Gate(7, 1) { seed = 1; }
    inline void compute() noexcept override { output = inputlimit ? LOGIC_UNKNOWN : (logic == 0); }
};

// IC_INPUT_PIN (id=8): internal input pin, pass-through → seed=1, HIGH when logic>0
struct IC_Input_Gate : CPP_Gate {
    IC_Input_Gate() : CPP_Gate(8, 1) { seed = 1; }
    inline void compute() noexcept override { output = inputlimit ? LOGIC_UNKNOWN : (logic > 0); }
};

// VARIABLE (id=9): driven by value, ignores logic/seed
struct Variable_Gate : CPP_Gate {
    Variable_Gate() : CPP_Gate(9, 1) { seed = 1; }
    inline void compute() noexcept override { output = inputlimit ? LOGIC_UNKNOWN : value; }
};

// IC_OUTPUT_PIN (id=10): internal output pin, pass-through → seed=1, HIGH when logic>0
struct IC_Output_Gate : CPP_Gate {
    IC_Output_Gate() : CPP_Gate(10, 1) { seed = 1; }
    inline void compute() noexcept override { output = inputlimit ? LOGIC_UNKNOWN : (logic > 0); }
};

// ─── Factory ──────────────────────────────────────────────────────────────────
// Returns a heap-allocated typed subclass for polymorphic dispatch via compute().
inline CPP_Gate* make_gate(int8_t type_id, uint8_t lim) {
    switch (type_id) {
        case 0:  return new AND_Gate      (lim);
        case 1:  return new NAND_Gate     (lim);
        case 2:  return new OR_Gate       (lim);
        case 3:  return new NOR_Gate      (lim);
        case 4:  return new XOR_Gate      (lim);
        case 5:  return new XNOR_Gate     (lim);
        case 6:  return new BUFFER_Gate   ();
        case 7:  return new NOT_Gate      ();
        case 8:  return new IC_Input_Gate ();
        case 9:  return new Variable_Gate ();
        case 10: return new IC_Output_Gate();
        default: return new CPP_Gate      (type_id, lim);
    }
}

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

static_assert(sizeof(Profile) == 16,
              "Profile: struct size must be exactly 16 bytes");

#endif // PROFILE_H