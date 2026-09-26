from Gates cimport CPP_Gate, Profile, vector
from libc.stdint cimport uint8_t
cdef tuple namelist
cdef object get(int choice, vector[CPP_Gate]& gate_infolist, vector[Profile]& profiles, list gate_verse)
cdef tuple decode(object code)
