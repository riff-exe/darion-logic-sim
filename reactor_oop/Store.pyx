from Gates cimport Gate, CPP_Gate, Profile, vector, make_gate
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
    cdef Gate gate
    if choice == IC_ID:
        return IC(choice, namelist[choice])
    gate = Gate(choice, namelist[choice])
    return gate

cdef tuple decode(object code):
    if len(code) == 2:
        return tuple(code)
    return (code[0], code[1], decode(code[2]))