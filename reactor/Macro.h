// reactor/Macro.h
// Macro cores: the behaviour behind a macro gate (MACRO_GATE_ID). The macro gate keeps its MacroCore* in
// hitlist.data (size = capacity = 0, borrowed, see HitList). When the engine pops the macro gate it calls eval(),
// which does all of the kind's work: read the inputs, write the output pins, update memory, and list the output
// pins it changed in changed[] for the engine to queue. A macro gate with an unconnected input stays unknown and
// is never popped, so eval can read every input.
#ifndef MACRO_H
#define MACRO_H
#include "Profile.h"
#include <cstdint>
#include <cstdlib>
#include <cstring>

struct MacroCore {
  uint16_t n_in, n_out;
  int *inputs;      // source location of each input (the macro gate's _sources)
  int *outputs;     // location of each output pin
  uint8_t *memory;  // each input's value at the previous eval (0/1/2)
  int *changed;     // output pins eval wrote with a new value
  uint16_t n_changed;
  uint8_t init;     // kept in the circuit file; the cores do not use it

  MacroCore(uint16_t ni, uint16_t no) : n_in(ni), n_out(no), n_changed(0), init(2) {
    inputs = static_cast<int *>(std::malloc((ni ? ni : 1) * sizeof(int)));
    outputs = static_cast<int *>(std::malloc((no ? no : 1) * sizeof(int)));
    changed = static_cast<int *>(std::malloc((no ? no : 1) * sizeof(int)));
    memory = static_cast<uint8_t *>(std::malloc(ni ? ni : 1));
    for (int i = 0; i < ni; ++i) inputs[i] = -1;
    for (int j = 0; j < no; ++j) outputs[j] = -1;
    reset();
  }
  virtual ~MacroCore() {
    std::free(inputs);
    std::free(outputs);
    std::free(changed);
    std::free(memory);
  }
  MacroCore(const MacroCore &) = delete;
  MacroCore &operator=(const MacroCore &) = delete;

  // `self` is the macro gate. The engine queues a macro on every input change (after each eval it sets the gate's
  // output to MACRO, a value evaluate() never produces; see Circuit.pyx), and eval compares the inputs with `memory`.
  virtual void eval(CPP_Gate *G, CPP_Gate *self) noexcept = 0;
  void reset() noexcept { std::memset(memory, 2, n_in ? n_in : 1); }
};

// D flip-flop: inputs CK, D (pin order of demos/ICs/DFF.json); outputs Q, QN. On a rising clock edge Q takes D as
// it was before this wave (memory), so flops clocked together all sample before any of them changes.
struct DFF : MacroCore {
  enum { CK, D };
  enum { Q, QN };
  DFF() : MacroCore(2, 2) {}
  void eval(CPP_Gate *G, CPP_Gate *self) noexcept override {
    uint8_t ck = G[inputs[CK]].output, d = G[inputs[D]].output;
    CPP_Gate &q = G[outputs[Q]], &qn = G[outputs[QN]];
    uint8_t v = q.output == 1;  // a flop without reset pins starts at 0
    if (memory[CK] == 0 && ck !=0) v = memory[D];
    n_changed = 0;
    if (q.output != v) {
      q.output = v;
      qn.output = v == 2 ? 2 : !v;
      changed[n_changed++] = outputs[Q];
      changed[n_changed++] = outputs[QN];
    }
    memory[CK] = ck;
    memory[D] = d;
  }
};

// D flip-flop with asynchronous active-low reset and set: inputs CK, D, RN, SN (pin order of DFFSR.json); outputs
// Q, QN. RN = 0 clears (and wins over SN), SN = 0 sets, an unknown RN or SN makes Q unknown, otherwise as DFF.
struct DFFSR : MacroCore {
  enum { CK, D, RN, SN };
  enum { Q, QN };
  DFFSR() : MacroCore(4, 2) {}
  void eval(CPP_Gate *G, CPP_Gate *self) noexcept override {
    uint8_t ck = G[inputs[CK]].output, d = G[inputs[D]].output;
    uint8_t rn = G[inputs[RN]].output, sn = G[inputs[SN]].output;
    CPP_Gate &q = G[outputs[Q]], &qn = G[outputs[QN]];
    uint8_t v = q.output;  // unknown until a clock edge or an async input loads it
    if (rn == 0) v = 0;
    else if (sn == 0) v = 1;
    else if (rn == 2 || sn == 2) v = 2;
    else if (memory[CK] == 0 && ck == 1) v = memory[D] == 1;
    n_changed = 0;
    if (q.output != v) {
      q.output = v;
      qn.output = v == 2 ? 2 : !v;
      changed[n_changed++] = outputs[Q];
      changed[n_changed++] = outputs[QN];
    }
    memory[CK] = ck;
    memory[D] = d;
    memory[RN] = rn;
    memory[SN] = sn;
  }
};

// Kind name -> new core, or nullptr for an unknown kind.
static inline MacroCore *make_core(const char *kind) {
  if (std::strcmp(kind, "dff") == 0) return new DFF();
  if (std::strcmp(kind, "dffsr") == 0) return new DFFSR();
  return nullptr;
}
#endif
