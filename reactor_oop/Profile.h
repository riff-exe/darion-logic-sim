// reactor_oop/Profile.h
#ifndef PROFILE_H
#define PROFILE_H
#include <vector>
#include <stdint.h>
#include <cstddef>

// ─── Forward declaration ───────────────────────────────────────────────────────
struct CPP_Gate;

enum LogicLevel : uint8_t {
    LOGIC_LOW     = 0,
    LOGIC_HIGH    = 1,
    LOGIC_UNKNOWN = 2
};

// ─── Profile (hitlist entry) ───────────────────────────────────────────────────
struct Profile {
    CPP_Gate* target;
    uint8_t   index;
    uint8_t   output;
    Profile() : target(nullptr), index(0), output(LOGIC_UNKNOWN) {}
    Profile(CPP_Gate* t, uint8_t i, uint8_t o) : target(t), index(i), output(o) {}
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
    void*                gate;        // back-pointer to Python Gate object
    int8_t               type;
    uint8_t              output;
    uint8_t              inputlimit;
    uint8_t              mark;
    uint8_t              update;
    uint8_t              value;
    uint8_t              scheduled;
    uint8_t              logic;       // count of inputs matching seed
    uint8_t              seed;        // triggering input value for this gate type
    unsigned int         target_time;
    std::vector<Profile> hitlist;

    CPP_Gate() : gate(nullptr), type(0), output(LOGIC_UNKNOWN),
                 inputlimit(2), mark(0), update(1), value(0), scheduled(0), logic(0), seed(1), target_time(0) {}
    CPP_Gate(void* g, int8_t t, uint8_t lim) : gate(g), type(t), output(LOGIC_UNKNOWN),
              inputlimit(lim), mark(0), update(1), value(0), scheduled(0), logic(0), seed(1), target_time(0) {}

    virtual void compute() noexcept { output = LOGIC_UNKNOWN; }
    virtual ~CPP_Gate() = default;
};

// ─── Typed gate subclasses ────────────────────────────────────────────────────

// AND (id=0): HIGH iff no LOW input  → seed=0, HIGH when logic==0
struct AND_Gate : CPP_Gate {
    AND_Gate(void* g, uint8_t lim) : CPP_Gate(g, 0, lim) { seed = 0; }
    inline void compute() noexcept override { output = inputlimit ? LOGIC_UNKNOWN : (logic == 0); }
};

// NAND (id=1): LOW iff no LOW input (inverted AND) → seed=0, HIGH when logic>0
struct NAND_Gate : CPP_Gate {
    NAND_Gate(void* g, uint8_t lim) : CPP_Gate(g, 1, lim) { seed = 0; }
    inline void compute() noexcept override { output = inputlimit ? LOGIC_UNKNOWN : (logic > 0); }
};

// OR (id=2): HIGH iff any HIGH input → seed=1, HIGH when logic>0
struct OR_Gate : CPP_Gate {
    OR_Gate(void* g, uint8_t lim) : CPP_Gate(g, 2, lim) { seed = 1; }
    inline void compute() noexcept override { output = inputlimit ? LOGIC_UNKNOWN : (logic > 0); }
};

// NOR (id=3): HIGH iff no HIGH input (inverted OR) → seed=1, HIGH when logic==0
struct NOR_Gate : CPP_Gate {
    NOR_Gate(void* g, uint8_t lim) : CPP_Gate(g, 3, lim) { seed = 1; }
    inline void compute() noexcept override { output = inputlimit ? LOGIC_UNKNOWN : (logic == 0); }
};

// XOR (id=4): HIGH iff odd HIGH count → seed=1, HIGH when logic&1
struct XOR_Gate : CPP_Gate {
    XOR_Gate(void* g, uint8_t lim) : CPP_Gate(g, 4, lim) { seed = 1; }
    inline void compute() noexcept override { output = inputlimit ? LOGIC_UNKNOWN : (logic & 1); }
};

// XNOR (id=5): HIGH iff even HIGH count (inverted XOR) → seed=1, HIGH when (logic&1)^1
struct XNOR_Gate : CPP_Gate {
    XNOR_Gate(void* g, uint8_t lim) : CPP_Gate(g, 5, lim) { seed = 1; }
    inline void compute() noexcept override { output = inputlimit ? LOGIC_UNKNOWN : ((logic & 1) ^ 1); }
};

// BUFFER (id=6): pass-through, 1 input → seed=1, HIGH when logic>0
struct BUFFER_Gate : CPP_Gate {
    BUFFER_Gate(void* g) : CPP_Gate(g, 6, 1) { seed = 1; }
    inline void compute() noexcept override { output = inputlimit ? LOGIC_UNKNOWN : (logic > 0); }
};

// NOT (id=7): inverter, 1 input → seed=1, HIGH when logic==0
struct NOT_Gate : CPP_Gate {
    NOT_Gate(void* g) : CPP_Gate(g, 7, 1) { seed = 1; }
    inline void compute() noexcept override { output = inputlimit ? LOGIC_UNKNOWN : (logic == 0); }
};

// IC_INPUT_PIN (id=8): internal input pin, pass-through → seed=1, HIGH when logic>0
struct IC_Input_Gate : CPP_Gate {
    IC_Input_Gate(void* g) : CPP_Gate(g, 8, 1) { seed = 1; }
    inline void compute() noexcept override { output = inputlimit ? LOGIC_UNKNOWN : (logic > 0); }
};

// VARIABLE (id=9): driven by value, ignores logic/seed
struct Variable_Gate : CPP_Gate {
    Variable_Gate(void* g) : CPP_Gate(g, 9, 1) { seed = 1; }
    inline void compute() noexcept override { output = inputlimit ? LOGIC_UNKNOWN : value; }
};

// IC_OUTPUT_PIN (id=10): internal output pin, pass-through → seed=1, HIGH when logic>0
struct IC_Output_Gate : CPP_Gate {
    IC_Output_Gate(void* g) : CPP_Gate(g, 10, 1) { seed = 1; }
    inline void compute() noexcept override { output = inputlimit ? LOGIC_UNKNOWN : (logic > 0); }
};

// ─── Factory ──────────────────────────────────────────────────────────────────
// Returns a heap-allocated typed subclass for polymorphic dispatch via compute().
inline CPP_Gate* make_gate(void* g, int8_t type_id, uint8_t lim) {
    switch (type_id) {
        case 0:  return new AND_Gate      (g, lim);
        case 1:  return new NAND_Gate     (g, lim);
        case 2:  return new OR_Gate       (g, lim);
        case 3:  return new NOR_Gate      (g, lim);
        case 4:  return new XOR_Gate      (g, lim);
        case 5:  return new XNOR_Gate     (g, lim);
        case 6:  return new BUFFER_Gate   (g);
        case 7:  return new NOT_Gate      (g);
        case 8:  return new IC_Input_Gate (g);
        case 9:  return new Variable_Gate (g);
        case 10: return new IC_Output_Gate(g);
        default: return new CPP_Gate      (g, type_id, lim);
    }
}

#endif // PROFILE_H