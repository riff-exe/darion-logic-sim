# distutils: language = c++
# cython: boundscheck=False
# cython: wraparound=False
# cython: initializedcheck=False
# cython: cdivision=True
# cython: nonecheck=False
from Gates cimport vector, CPP_Gate, Profile, make_gate, pop, hide, reveal
from cpython.list cimport PyList_GET_SIZE, PyList_GET_ITEM
from Const cimport *
from libc.string cimport memmove
from Store cimport decode
from libc.stdint cimport uint16_t

cdef inline void pop(vector[Profile]& hitlist, CPP_Gate* target, int pin_index):
    cdef Profile* profile = hitlist.data()
    cdef Profile* end = profile + hitlist.size()
    while profile < end:
        if profile.target == target and profile.index == pin_index:
            profile[0] = (end - 1)[0]
            hitlist.pop_back()
            break
        profile += 1

cdef inline void hide(Profile& profile):
    cdef CPP_Gate* target_info = <CPP_Gate*>profile.target
    cdef Gate target = <Gate>target_info.gate
    if profile.output == HIGH: target_info.high -= 1
    elif profile.output == LOW: target_info.low -= 1
    target_info.inputlimit += 1
    target.sources[profile.index] = None
    profile.output = UNKNOWN

cdef inline void reveal(Profile& profile, Gate source):
    cdef CPP_Gate* target_info = <CPP_Gate*>profile.target
    cdef Gate target = <Gate>target_info.gate
    target_info.inputlimit -= 1
    target.sources[profile.index] = source

cdef class Gate:
    def __init__(self, int id, str name):
        self.id = id
        self.codename = name
        self.location = -1
        cdef uint8_t limit = 1 if id >= BUFFER_ID else 2
        self.info = make_gate(<void*>self, id, limit)
        if id >= BUFFER_ID:
            self.sources = [None]
        else:
            self.sources = [None, None]
        self.code = ()
        self.custom_name = ''

    def __dealloc__(self):
        if self.info != NULL:
            del self.info

    def __repr__(self):
        return self.codename if self.custom_name == '' else self.custom_name

    def __str__(self):
        return self.codename if self.custom_name == '' else self.custom_name

    @property
    def hitlist(self):
        cdef list result = []
        cdef size_t i
        cdef size_t size = self.info.hitlist.size()
        cdef Profile* profile = self.info.hitlist.data()
        for i in range(size):
            result.append(<Gate>(<CPP_Gate*>profile[i].target).gate)
        return result

    cdef void process(self):
        if MODE == DESIGN:
            self.info.output = UNKNOWN
        elif self.info.inputlimit == 0:
            self.compute()
        else:
            self.info.output = UNKNOWN

    cdef void compute(self):
        self.info.compute()

    cpdef void rename(self, str name):
        self.custom_name = name

    cdef void connect(self, Gate source, int index):
        if self.sources[index] is not None:
            return
        source.info.hitlist.emplace_back(<CPP_Gate*>self.info, index, source.info.output)
        self.sources[index] = source
        if source.info.output == HIGH: self.info.high += 1
        elif source.info.output == LOW: self.info.low += 1
        self.info.inputlimit -= 1
        if source.info.output == UNKNOWN:
            self.info.output = UNKNOWN
        else:
            self.process()

    cdef void disconnect(self, int index):
        if self.sources[index] is None:
            return
        cdef Gate source = self.sources[index]
        pop(source.info.hitlist, <CPP_Gate*>self.info, index)
        self.sources[index] = None
        if source.info.output == HIGH: self.info.high -= 1
        elif source.info.output == LOW: self.info.low -= 1
        self.info.inputlimit += 1
        self.info.output = UNKNOWN

    cdef void reset(self):
        self.info.high = 0
        self.info.low = 0
        self.info.output = UNKNOWN
        cdef Profile* profile = self.info.hitlist.data()
        cdef Profile* end = profile + self.info.hitlist.size()
        while profile < end:
            profile.output = UNKNOWN
            profile += 1

    cdef void hide(self):
        cdef Py_ssize_t i
        cdef Py_ssize_t n = self.info.hitlist.size()
        cdef Profile* hitlist = self.info.hitlist.data()
        for i in range(n):
            hide(hitlist[i])
        cdef list sources = self.sources
        n = len(sources)
        cdef Gate source
        for i in range(n):
            source = <Gate>PyList_GET_ITEM(sources, i)
            if source is not None:
                pop(source.info.hitlist, <CPP_Gate*>self.info, i)
        self.info.output = UNKNOWN
        self.info.high = 0
        self.info.low = 0
        self.info.inputlimit = len(sources)

    cdef void reveal(self):
        cdef Profile* hitlist = self.info.hitlist.data()
        cdef Py_ssize_t i
        cdef list sources = self.sources
        cdef Py_ssize_t n = len(sources)
        cdef Gate source
        for i in range(n):
            source = <Gate>PyList_GET_ITEM(sources, i)
            if source is not None:
                source.info.hitlist.emplace_back(<CPP_Gate*>self.info, i, source.info.output)
                if source.info.output == HIGH: self.info.high += 1
                elif source.info.output == LOW: self.info.low += 1
                self.info.inputlimit -= 1
        n = self.info.hitlist.size()
        for i in range(n):
            reveal(hitlist[i], self)
        self.process()

    cpdef bint setlimits(self, int size):
        return False

    cpdef str getoutput(self):
        if self.info.output == UNKNOWN:
            return 'X'
        return 'T' if self.info.output == HIGH else 'F'

    @property
    def output(self):
        '''Current output value of this gate'''
        return self.info.output

    @property
    def invalid(self):
        '''Alias for inputlimit (number of unresolved inputs)'''
        return self.info.inputlimit

    @property
    def inputlimit(self):
        return self.info.inputlimit

    @property
    def book(self):
        cdef int connected = len(self.sources) - self.info.inputlimit
        return [self.info.low, self.info.high, self.info.inputlimit]

    @property
    def value(self):
        '''Stored toggle value'''
        return bool(self.info.value)

    @value.setter
    def value(self, val):
        self.info.value = 1 if val else 0

    @property
    def scheduled(self):
        return bool(self.info.scheduled)

    @scheduled.setter
    def scheduled(self, val):
        self.info.scheduled = 1 if val else 0

    @property
    def update(self):
        return bool(self.info.update)

    @update.setter
    def update(self, val):
        self.info.update = 1 if val else 0

    cpdef list full_data(self):
        cdef Gate source
        cdef list dictionary = [
            self.custom_name,
            self.id,
            self.location,
            self.info.inputlimit,
            [source.location if source else -1 for source in self.sources],
        ]
        return dictionary

    cpdef list partial_data(self):
        cdef Gate source
        cdef list dictionary = [
            self.custom_name,
            self.id,
            self.location,
            self.info.inputlimit,
            [source.location if source and source.info.scheduled else -1 for source in self.sources],
        ]
        return dictionary

    cpdef void clone(self, list dictionary, dict pseudo):
        self.custom_name = dictionary[CUSTOM_NAME]
        self.setlimits(dictionary[INPUTLIMIT])
        for index, source_loc in enumerate(dictionary[SOURCES]):
            if source_loc != -1 and source_loc in pseudo:
                self.connect(pseudo[source_loc], index)

    cpdef void load_to_cluster(self, list cluster):
        cluster.append(self)
        self.info.scheduled = 1

cdef class MultiInputGate(Gate):
    def __init__(self, int id, str name=''):
        self.id = id
        self.codename = name if name else 'MultiInputGate'
        self.location = -1
        self.info = make_gate(<void*>self, id, 2)
        self.sources = [None, None]
        self.code = ()
        self.custom_name = ''

    cpdef bint setlimits(self, int size):
        if size < 2:
            return False
        cdef int limit = self.info.inputlimit
        cdef int connected = len(self.sources) - limit
        if size > len(self.sources):
            self.sources.extend([None] * (size - len(self.sources)))
            self.info.inputlimit = size - connected
            self.process()
            return True
        elif size < len(self.sources):
            for i in range(size, len(self.sources)):
                if self.sources[i]: return False
            self.sources = self.sources[:size]
            self.info.inputlimit = size - connected
            self.process()
            return True
        return False

cdef class AND(MultiInputGate):
    def __init__(self, int id=AND_ID, str name='AND'):
        super().__init__(id, name)

    cdef void compute(self):
        self.info.output = (self.info.low == 0)

cdef class NAND(MultiInputGate):
    def __init__(self, int id=NAND_ID, str name='NAND'):
        super().__init__(id, name)

    cdef void compute(self):
        self.info.output = (self.info.low > 0)

cdef class OR(MultiInputGate):
    def __init__(self, int id=OR_ID, str name='OR'):
        super().__init__(id, name)

    cdef void compute(self):
        self.info.output = (self.info.high > 0)

cdef class NOR(MultiInputGate):
    def __init__(self, int id=NOR_ID, str name='NOR'):
        super().__init__(id, name)

    cdef void compute(self):
        self.info.output = (self.info.high == 0)

cdef class XOR(MultiInputGate):
    def __init__(self, int id=XOR_ID, str name='XOR'):
        super().__init__(id, name)

    cdef void compute(self):
        self.info.output = self.info.high & 1

cdef class XNOR(MultiInputGate):
    def __init__(self, int id=XNOR_ID, str name='XNOR'):
        super().__init__(id, name)

    cdef void compute(self):
        self.info.output = (self.info.high & 1) ^ 1

cdef class SingleInputGate(Gate):
    def __init__(self, int id, str name=''):
        self.id = id
        self.codename = name if name else 'SingleInputGate'
        self.location = -1
        self.info = make_gate(<void*>self, id, 1)
        self.sources = [None]
        self.code = ()
        self.custom_name = ''

    cpdef bint setlimits(self, int size):
        return False

cdef class BUFFER(SingleInputGate):
    def __init__(self, int id=BUFFER_ID, str name='BUFFER'):
        super().__init__(id, name)

    cdef void compute(self):
        self.info.output = self.info.high & 1

cdef class Probe(BUFFER):
    def __init__(self, int id=BUFFER_ID, str name='Probe'):
        super().__init__(id, name)

cdef class NOT(SingleInputGate):
    def __init__(self, int id=NOT_ID, str name='NOT'):
        super().__init__(id, name)

    cdef void compute(self):
        self.info.output = (self.info.high & 1) ^ 1

cdef class IC_Input(SingleInputGate):
    def __init__(self, int id=IC_INPUT_PIN_ID, str name='In'):
        super().__init__(id, name)

    cdef void compute(self):
        self.info.output = self.info.high & 1

cdef class IC_Output(SingleInputGate):
    def __init__(self, int id=IC_OUTPUT_PIN_ID, str name='Out'):
        super().__init__(id, name)

    cdef void compute(self):
        self.info.output = self.info.high & 1

cdef class Variable(Gate):
    def __init__(self, int id=VARIABLE_ID, str name='Variable'):
        self.id = id
        self.codename = name
        self.location = -1
        self.info = make_gate(<void*>self, id, 1)
        self.sources = [None]
        self.code = ()
        self.custom_name = ''

    cdef void process(self):
        if MODE == DESIGN:
            self.info.output = UNKNOWN
        else:
            self.info.output = self.info.value

    cdef void compute(self):
        self.info.output = self.info.value

    cdef void connect(self, Gate source, int index):
        return

    cdef void disconnect(self, int index):
        return

    cdef void reset(self):
        self.info.output = UNKNOWN
        cdef Profile* profile = self.info.hitlist.data()
        cdef Profile* end = profile + self.info.hitlist.size()
        while profile < end:
            profile.output = UNKNOWN
            profile += 1

    cdef void hide(self):
        cdef Py_ssize_t i
        cdef Py_ssize_t n = self.info.hitlist.size()
        cdef Profile* hitlist = self.info.hitlist.data()
        for i in range(n):
            hide(hitlist[i])
        self.info.output = UNKNOWN

    cdef void reveal(self):
        cdef Profile* hitlist = self.info.hitlist.data()
        cdef Py_ssize_t i
        cdef Py_ssize_t n = self.info.hitlist.size()
        for i in range(n):
            reveal(hitlist[i], self)
        self.process()

    cpdef bint setlimits(self, int size):
        return False

    cpdef list full_data(self):
        return [
            self.custom_name,
            self.id,
            self.location,
            self.info.inputlimit,
            bool(self.info.value),
        ]

    cpdef list partial_data(self):
        return [
            self.custom_name,
            self.id,
            self.location,
            self.info.inputlimit,
            bool(self.info.value),
        ]

    cpdef void clone(self, list dictionary, dict pseudo):
        self.custom_name = dictionary[CUSTOM_NAME]
        self.info.value = 1 if dictionary[VALUE] else 0

Buffer = BUFFER
In = IC_Input
Out = IC_Output

