from Gates cimport (
    Gate, MultiInputGate, SingleInputGate,
    AND, NAND, OR, NOR, XOR, XNOR,
    BUFFER, Probe, NOT, IC_Input, IC_Output, Variable,
    CPP_Gate, Profile, vector, make_gate
)
from libcpp.vector cimport vector
from IC cimport IC
from Const cimport *
from libc.stdint cimport uint8_t

# Display names at each ID slot (matches original HEAD order)
cdef tuple namelist = (
    'AND',       # 0  AND_ID
    'NAND',      # 1  NAND_ID
    'OR',        # 2  OR_ID
    'NOR',       # 3  NOR_ID
    'XOR',       # 4  XOR_ID
    'XNOR',      # 5  XNOR_ID
    'NOT',       # 6  BUFFER_ID  (display name only)
    'Variable',  # 7  NOT_ID     (display name only)
    'Probe',     # 8  IC_INPUT_PIN_ID
    'In',        # 9  VARIABLE_ID
    'Out',       # 10 IC_OUTPUT_PIN_ID
    'IC',        # 11 IC_ID
)

cpdef object get(int choice):
    cdef str name = namelist[choice]
    if choice == IC_ID:
        return IC(choice, name)
    elif choice == AND_ID:
        return AND(choice, name)
    elif choice == NAND_ID:
        return NAND(choice, name)
    elif choice == OR_ID:
        return OR(choice, name)
    elif choice == NOR_ID:
        return NOR(choice, name)
    elif choice == XOR_ID:
        return XOR(choice, name)
    elif choice == XNOR_ID:
        return XNOR(choice, name)
    elif choice == BUFFER_ID:
        return Probe(choice, name)
    elif choice == NOT_ID:
        return NOT(choice, name)
    elif choice == IC_INPUT_PIN_ID:
        return IC_Input(choice, name)
    elif choice == VARIABLE_ID:
        return Variable(choice, name)
    elif choice == IC_OUTPUT_PIN_ID:
        return IC_Output(choice, name)
    return Gate(choice, name)

cdef tuple decode(object code):
    if len(code) == 2:
        return tuple(code)
    return (code[0], code[1], decode(code[2]))