# distutils: language = c++
# cython: boundscheck=False
# cython: wraparound=False
# cython: initializedcheck=False
# cython: cdivision=True
# cython: nonecheck=False
from Gates cimport vector
from cpython.list cimport PyList_GET_SIZE, PyList_GET_ITEM
from Const cimport *
from libc.string cimport memmove
from Store cimport decode
from libc.stdint cimport uint8_t
from libcpp.unordered_map cimport unordered_map

cdef inline void pop(vector[CPP_Gate*]& hitlist, CPP_Gate* target):
    '''Remove a specific entry from a hitlist by target gate'''
    cdef CPP_Gate** ptr = hitlist.data()
    cdef CPP_Gate** end = ptr + hitlist.size()
    while ptr < end:
        if ptr[0] == target:
            ptr[0] = (end-1)[0] # swap and pop
            hitlist.pop_back()
            break
        ptr += 1


cdef class Gate:
    def __init__(self, int id, str name):
        self.codename = name
        self.location = -1
        self.id = id
        if id >= SINGLE_INPUT_ID:
            self._sources = [-1]
        else:
            self._sources = [-1, -1]
        self.code = ()
        self.custom_name = ''
        if id == VARIABLE_ID:
            self.delay_book = [0, 0, 0]

    def __repr__(self):
        return self.codename if self.custom_name == '' else self.custom_name

    def __str__(self):
        cdef str name = self.codename if self.custom_name == '' else self.custom_name
        cdef int output
        if self.location == -1:
            output = UNKNOWN
        else:
            output = self.info.output
        if output == LOW: return f'\033[94m{name}\033[0m'
        elif output == HIGH: return f'\033[92m{name}\033[0m'
        else: return f'\033[97m{name}\033[0m'
    def __int__(self):
        return self.location

    @property
    def hitlist(self):
        '''All gates this gate currently drives'''
        cdef list targets = []
        cdef CPP_Gate* base = (self.info - self.location)
        cdef CPP_Gate* info=base+self.location
        cdef CPP_Gate** target = info.hitlist.data()
        cdef CPP_Gate** end = target + info.hitlist.size()
        cdef list gate_verse = self.gate_verse
        while target < end:
            targets.append(<Gate>(PyList_GET_ITEM(gate_verse, target[0] - base)))
            target += 1
        return targets

    @property
    def edge_profiles(self):
        '''Outgoing connections: list of (target_loc, target.output, pin_index)'''
        cdef list res = []
        cdef CPP_Gate* base = (self.info - self.location)
        cdef CPP_Gate* info = base + self.location
        cdef CPP_Gate** target = info.hitlist.data()
        cdef CPP_Gate** end = target + info.hitlist.size()
        while target < end:
            res.append((target[0] - base, target[0].output, 0))
            target += 1
        return res

    @property
    def book(self):
        '''Input tally: counts of LOW, HIGH, UNKNOWN sources'''
        cdef int low = 0, high = 0, unknown = 0
        cdef CPP_Gate* info = self.info
        cdef CPP_Gate* src
        cdef size_t j
        for j in range(info.sources.size()):
            src = info.sources[j]
            if src == NULL or src.output == UNKNOWN:
                unknown += 1
            elif src.output == HIGH:
                high += 1
            else:
                low += 1
        return [low, high, unknown]

    @property
    def inputlimit(self):
        '''How many inputs this gate accepts'''
        return self.info.limit

    @property
    def limit(self):
        return self.info.limit

    @property
    def invalid(self):
        return self.info.invalid

    @property
    def logic(self):
        return self.info.logic

    @property
    def high(self):
        return self.info.logic

    @property
    def seed(self):
        return self.info.seed

    @property 
    def scheduled(self):
        '''Whether this gate is already queued for propagation this tick'''
        return bool(self.info.flags & FLAG_SCHEDULED)
    
    @scheduled.setter
    def scheduled(self, bint val):
        if val: self.info.flags |= FLAG_SCHEDULED
        else: self.info.flags &= ~FLAG_SCHEDULED

    @property
    def mark(self):
        return bool(self.info.flags & FLAG_MARK)
        
    @mark.setter
    def mark(self, bint val):
        if val: self.info.flags |= FLAG_MARK
        else: self.info.flags &= ~FLAG_MARK

    @property
    def update(self):
        return bool(self.info.flags & FLAG_UPDATE)
        
    @update.setter
    def update(self, bint val):
        if val: self.info.flags |= FLAG_UPDATE
        else: self.info.flags &= ~FLAG_UPDATE

    @property
    def output(self):
        '''Current output value of this gate'''
        return self.info.output

    @property
    def value(self):
        '''Stored toggle value, only meaningful for variables'''
        return bool(self.info.flags & FLAG_VALUE)
    
    @property
    def sources(self):
        '''The gate objects wired into each input slot, or None for empty slots'''
        cdef list source_list=[]
        cdef int i
        for i in self._sources:
            if i >= 0 and i < len(self.gate_verse):
                source_list.append(self.gate_verse[i])
            else:
                source_list.append(None)
        return source_list
    @output.setter
    def output(self, int val):
        self.info.output = val
    @value.setter
    def value(self, int val):
        if val: self.info.flags |= FLAG_VALUE
        else: self.info.flags &= ~FLAG_VALUE
    @inputlimit.setter
    def inputlimit(self, int val):
        self.info.invalid = val
        self.info.limit = val
    @limit.setter
    def limit(self, int val):
        self.info.limit = val
    @invalid.setter
    def invalid(self, int val):
        self.info.invalid = val
        
    cdef void process(self):
        '''Recompute this gate's output from its current inputs and type'''
        cdef CPP_Gate* gate_infolist=(self.info - self.location)
        cdef CPP_Gate* info = &gate_infolist[self.location]

        if MODE == DESIGN:
            info.output = UNKNOWN
            return

        if info.type == VARIABLE_ID:
            info.output = info.flags & FLAG_VALUE
        else:
            info.compute()

    cpdef void rename(self, str name):
        '''Give the gate a display name'''
        self.custom_name = name

    cpdef void deregister(self):
        '''Remove the gate from the global list and mark its slot as deleted'''
        self.all_gates[self.location] = None
        self.info.type = -1
        self.info.flags &= ~FLAG_SCHEDULED

    cdef void connect(self, int source, int index):
        '''Wire a source gate into this gate's input slot at index'''
        cdef CPP_Gate* gate_infolist=(self.info - self.location)
        cdef CPP_Gate* self_info = &gate_infolist[self.location]
        if self_info.type == VARIABLE_ID or self._sources[index] != -1:
            return
        cdef CPP_Gate* src_info = &gate_infolist[source]
        
        if src_info.output == UNKNOWN:
            (<Gate>PyList_GET_ITEM(self.gate_verse, source)).process()
            
        src_info.hitlist.push_back(&gate_infolist[self.location])
        self._sources[index] = source
        self_info.sources[index] = src_info
        self_info.invalid -= 1
        self.process()

    cdef void disconnect(self, int index):
        '''Remove whatever is wired into input slot at index and clear the output'''
        cdef CPP_Gate* gate_infolist=(self.info - self.location)
        cdef CPP_Gate* self_info = &gate_infolist[self.location]
        if self_info.type == VARIABLE_ID or self._sources[index] == -1:
            return
        cdef int src_loc = self._sources[index]
        cdef CPP_Gate* src_info = &gate_infolist[src_loc]
        pop(src_info.hitlist, &gate_infolist[self.location])
        self._sources[index] = -1
        self_info.sources[index] = NULL
        self_info.invalid += 1
        self_info.output = UNKNOWN
        self.process()

    cdef void reset(self):
        '''Move all counted inputs back to unknown and set output to unknown'''
        cdef CPP_Gate* info = self.info
        info.output = UNKNOWN
        info.flags &= ~FLAG_SCHEDULED
        info.target_time = 0

    cdef void hide(self):
        '''Detach this gate from the live graph without removing it from the lists'''
        cdef Py_ssize_t i, pin
        cdef CPP_Gate* target_info
        cdef Gate target_gate
        cdef list sources
        cdef int source_loc
        cdef CPP_Gate* src_info
        cdef Py_ssize_t n
        cdef CPP_Gate** hitlist_data
        cdef CPP_Gate* gate_infolist=(self.info - self.location)
        cdef CPP_Gate* info = &gate_infolist[self.location]
        
        n = info.hitlist.size()
        hitlist_data = info.hitlist.data()
        for i in range(n):
            target_info = hitlist_data[i]
            target_gate = <Gate>self.gate_verse[target_info - gate_infolist]
            for pin in range(len(target_gate._sources)):
                if target_gate._sources[pin] == self.location:
                    target_gate._sources[pin] = -self.location - 2
                    target_info.sources[pin] = NULL
                    target_info.invalid += 1

        sources = self._sources
        if info.type != VARIABLE_ID:
            n = len(sources)
            for i in range(n):
                source_loc = sources[i]
                if source_loc >= 0:
                    src_info = &gate_infolist[source_loc]
                    pop(src_info.hitlist, &gate_infolist[self.location])

        # Zero out own state
        info.output = UNKNOWN

    cdef void reveal(self):
        '''Re-attach this gate to the live graph and recompute its output'''
        cdef list sources = self._sources
        cdef Py_ssize_t i, pin
        cdef Py_ssize_t n = len(sources)
        cdef int source_loc
        cdef CPP_Gate* src_info
        cdef CPP_Gate* target_info
        cdef Gate target_gate
        cdef CPP_Gate** hitlist_data
        cdef CPP_Gate* gate_infolist=(self.info - self.location)
        cdef CPP_Gate* info = &gate_infolist[self.location]
        if info.type != VARIABLE_ID:
            for i in range(n):
                source_loc = sources[i]
                if source_loc >= 0:
                    src_info = &gate_infolist[source_loc]
                    src_info.hitlist.push_back(&gate_infolist[self.location])
                    info.sources[i] = src_info

        n = info.hitlist.size()
        hitlist_data = info.hitlist.data()
        for i in range(n):
            target_info = hitlist_data[i]
            target_gate = <Gate>self.gate_verse[target_info - gate_infolist]
            for pin in range(len(target_gate._sources)):
                if target_gate._sources[pin] == -self.location - 2:
                    target_gate._sources[pin] = self.location
                    target_info.sources[pin] = &gate_infolist[self.location]
                    target_info.invalid -= 1

        self.process()

    cpdef bint setlimits(self, int size):
        '''Resize the input list; returns False if slots are in use and can't be trimmed'''
        cdef CPP_Gate* info = self.info
        cdef int i
        cdef int current
        if size < 2 or info.type >= SINGLE_INPUT_ID:
            return False
        current = len(self._sources)

        if size > current:
            for _ in range(size - current):
                self._sources.append(-1)
            info.sources.resize(size)
            for i in range(current, size):
                info.sources[i] = NULL
            info.invalid += (size - current)
            info.limit = size
            self.process()
            return True
        elif size < current:
            for i in range(size, current):
                if self._sources[i] != -1:
                    return False
            for i in range(current - size):
                self._sources.pop()
            info.sources.resize(size)
            info.invalid -= (current - size)
            info.limit = size
            self.process()
            return True
        return False

    cpdef str getoutput(self):
        '''Return the output as a human-readable character: T, F, E, or X'''
        cdef int output=self.info.output
        if output == HIGH: return 'T'
        elif output == LOW: return 'F'
        else: return 'X'
        
    cpdef list full_data(self):
        '''Serialise the gate with full connection info, used for saving the circuit'''
        cdef CPP_Gate* info = self.info
        cdef list dictionary = [
            self.custom_name,
            self.id,
            self.location,
            len(self._sources) if self.id!=VARIABLE_ID else self.inputlimit,
            bool(info.flags & FLAG_VALUE) if info.type == VARIABLE_ID else list(self._sources),
            ]
        return dictionary

    cpdef list partial_data(self):
        '''Serialise the gate with only the in-cluster connections, for copy/paste and IC export'''
        cdef CPP_Gate* gate_infolist=(self.info - self.location)
        cdef CPP_Gate* info = &gate_infolist[self.location]
        cdef list dictionary = [
            self.custom_name,
            self.id,
            self.location,
            len(self._sources) if self.id!=VARIABLE_ID else self.inputlimit,
            bool(info.flags & FLAG_VALUE) if info.type == VARIABLE_ID else [src_loc if src_loc >= 0 and (gate_infolist[src_loc].flags & FLAG_MARK) else -1 for src_loc in self._sources],
            ]
        return dictionary

    cdef void clone(self, list dictionary, unordered_map[int, int]& pseudo):
        '''Restore gate state from serialised data, remapping source locations via pseudo'''
        self.custom_name = dictionary[CUSTOM_NAME]
        cdef CPP_Gate* info = self.info
        if info.type == VARIABLE_ID:
            if dictionary[VALUE]: info.flags |= FLAG_VALUE
            else: info.flags &= ~FLAG_VALUE
        else:
            self.setlimits(dictionary[INPUTLIMIT])
            for index, source in enumerate(dictionary[SOURCES]):
                if source != -1:
                    self.connect(pseudo[source], index)

    cpdef void load_to_cluster(self, list cluster):
        '''Mark this gate as scheduled and add it to the copy cluster'''
        cluster.append(self.location)
        self.info.flags |= FLAG_MARK

    cpdef bint set_pulse(self, int val, int time_type):
        if self.id != VARIABLE_ID or time_type < 0 or time_type > 2 or val < 0 or val > 65535:
            return False
        self.delay_book[time_type] = val
        return True

    cpdef bint clock(self):
        if self.id != VARIABLE_ID:
            return False
        self.info.limit = INFINITE
        return True

cdef class Variable(Gate):
    pass

cdef class Probe(Gate):
    pass

cdef class NOT(Gate):
    pass
