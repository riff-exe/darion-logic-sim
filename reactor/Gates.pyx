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
from libc.stdint cimport uint8_t, uint16_t

cdef inline void pop(int& head, uint16_t& count, vector[Profile]& profiles, CPP_Gate* gate_infolist, CPP_Gate* target, int pin_index):
    '''Remove a specific entry from a hitlist by target gate and pin index'''
    cdef int curr = head
    cdef int prev = -1
    while curr != -1:
        if profiles[curr].target == target and profiles[curr].index == pin_index:
            if target.type != VARIABLE_ID:
                target.logic -= (profiles[curr].output == target.seed)
            if prev == -1:
                head = profiles[curr].next
            else:
                profiles[prev].next = profiles[curr].next
            profiles[curr].target = NULL
            profiles[curr].next = -1
            if count > 0:
                count -= 1
            break
        prev = curr
        curr = profiles[curr].next

cdef inline void add_profile(int& head, uint16_t& count, vector[Profile]& profiles, CPP_Gate* target, int pin_index, uint8_t output):
    cdef int new_idx = <int>profiles.size()
    profiles.push_back(Profile(target, pin_index, output, head))
    head = new_idx
    count += 1

cdef inline void hide(int p_idx, vector[Profile]& profiles, CPP_Gate* gate_infolist, list gate_verse):
    '''Sever one outgoing connection and zero out the target's source slot'''
    cdef CPP_Gate* target_info = profiles[p_idx].target
    if target_info == NULL: return
    if target_info.type != VARIABLE_ID:
        target_info.logic -= (profiles[p_idx].output == target_info.seed)
    target_info.inputlimit += 1
    cdef int target_loc = target_info - gate_infolist
    cdef Gate target_gate = <Gate>gate_verse[target_loc]
    target_gate._sources[profiles[p_idx].index] = -1
    profiles[p_idx].output = UNKNOWN

cdef inline void reveal(int p_idx, vector[Profile]& profiles, Gate source, list gate_verse):
    '''Restore one outgoing connection and re-register the source in the target's book'''
    cdef CPP_Gate* target_info = profiles[p_idx].target
    if target_info == NULL: return
    cdef CPP_Gate* gate_infolist = (source.info - source.location)
    target_info.inputlimit -= 1
    cdef int target_loc = target_info - gate_infolist
    cdef Gate target_gate = <Gate>gate_verse[target_loc]
    target_gate._sources[profiles[p_idx].index] = source.location


cdef class Gate:
    def __cinit__(self, *args, **kwargs):
        self.profiles = NULL
        self.info = NULL

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
        cdef CPP_Gate* info = base + self.location
        cdef list gate_verse = self.gate_verse
        cdef int p_idx = info.hitlist
        cdef Profile* p_base
        if self.profiles != NULL and self.profiles.size() > 0:
            p_base = self.profiles.data()
            while p_idx != -1:
                if p_base[p_idx].target != NULL:
                    targets.append(<Gate>(PyList_GET_ITEM(gate_verse, p_base[p_idx].target - base)))
                p_idx = p_base[p_idx].next
        return targets

    @property
    def hitlist_count(self):
        '''Number of outgoing connections currently wired to this gate'''
        return self.info.hitlist_count

    @property
    def edge_profiles(self):
        '''Outgoing connections: list of (target_loc, profile.output, pin_index)'''
        cdef list res = []
        cdef CPP_Gate* base = (self.info - self.location)
        cdef CPP_Gate* info = base + self.location
        cdef int p_idx = info.hitlist
        cdef Profile* p_base
        if self.profiles != NULL and self.profiles.size() > 0:
            p_base = self.profiles.data()
            while p_idx != -1:
                if p_base[p_idx].target != NULL:
                    res.append((p_base[p_idx].target - base, p_base[p_idx].output, p_base[p_idx].index))
                p_idx = p_base[p_idx].next
        return res

    @property
    def book(self):
        '''Input tally: counts of LOW, HIGH, UNKNOWN sources'''
        cdef CPP_Gate* gate_infolist = self.info - self.location
        cdef int low = 0, high = 0, unknown = 0
        cdef int s, out
        for s in self._sources:
            if s == -1:
                unknown += 1
            else:
                out = gate_infolist[s].output
                if out == LOW: low += 1
                elif out == HIGH: high += 1
                else: unknown += 1
        return [low, high, unknown]

    @property
    def logic(self):
        return self.info.logic

    @property
    def seed(self):
        return self.info.seed

    @property
    def inputlimit(self):
        '''How many inputs this gate accepts'''
        return self.info.inputlimit
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
            if i != -1:
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
        self.info.inputlimit = val
        
    cdef void process(self):
        '''Recompute this gate's output from its current inputs and type
        a slower yet safer method of updating output'''
        cdef CPP_Gate* gate_infolist=(self.info - self.location)
        cdef CPP_Gate* info = &gate_infolist[self.location]
        cdef CPP_Gate* src_info
        cdef int gate_type = info.type
        cdef int limit = len(self._sources)
        cdef int source_loc # Changed from Gate source to int source_loc
        cdef bint has_known = False

        if MODE == DESIGN:
            info.output = UNKNOWN
            return

        if gate_type == VARIABLE_ID:
            info.output = info.flags & FLAG_VALUE
        else:
            if info.inputlimit > 0:
                info.output = UNKNOWN
                return
            has_known = False
            for source_loc in self._sources:
                if source_loc != -1 and gate_infolist[source_loc].output != UNKNOWN:
                    has_known = True
                    break
            if not has_known:
                info.output = UNKNOWN
                return
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
            
        add_profile(src_info.hitlist, src_info.hitlist_count, self.profiles[0], &gate_infolist[self.location], index, src_info.output)
        self._sources[index] = source
        self_info.inputlimit -= 1
        if self.id!=VARIABLE_ID:
            self_info.logic += (src_info.output == self_info.seed)
        self.process()

    cdef void disconnect(self, int index):
        '''Remove whatever is wired into input slot at index and clear the output'''
        cdef CPP_Gate* gate_infolist=(self.info - self.location)
        cdef CPP_Gate* self_info = &gate_infolist[self.location]
        if self_info.type == VARIABLE_ID or self._sources[index] == -1:
            return
        cdef int src_loc = self._sources[index]
        cdef CPP_Gate* src_info = &gate_infolist[src_loc]
        pop(src_info.hitlist, src_info.hitlist_count, self.profiles[0], gate_infolist, &gate_infolist[self.location], index)
        self._sources[index] = -1
        self_info.inputlimit += 1
        self_info.output = UNKNOWN

    cdef void reset(self):
        '''Move all counted inputs back to unknown and set output to unknown'''
        cdef CPP_Gate* info = self.info
        if info.type != VARIABLE_ID:
            info.logic = 0
        info.output = UNKNOWN
        info.flags &= ~FLAG_SCHEDULED
        info.target_time = 0
        cdef int p_idx = info.hitlist
        cdef Profile* p_base
        if self.profiles != NULL and self.profiles.size() > 0:
            p_base = self.profiles.data()
            while p_idx != -1:
                p_base[p_idx].output = UNKNOWN
                p_idx = p_base[p_idx].next

    cdef void hide(self):
        '''Detach this gate from the live graph without removing it from the lists'''
        cdef list sources
        cdef int source_loc
        cdef CPP_Gate* src_info
        cdef CPP_Gate* gate_infolist=(self.info - self.location)
        cdef CPP_Gate* info = &gate_infolist[self.location]
        cdef int p_idx = info.hitlist
        cdef Profile* p_base
        if self.profiles != NULL and self.profiles.size() > 0:
            p_base = self.profiles.data()
            while p_idx != -1:
                hide(p_idx, self.profiles[0], gate_infolist, self.gate_verse)
                p_idx = p_base[p_idx].next

        sources = self._sources
        cdef Py_ssize_t i, n
        if info.type != VARIABLE_ID:
            n = len(sources)
            for i in range(n):
                source_loc = sources[i]
                if source_loc != -1:
                    src_info = &gate_infolist[source_loc]
                    pop(src_info.hitlist, src_info.hitlist_count, self.profiles[0], gate_infolist, &gate_infolist[self.location], i)

        # 3. Zero out own state
        info.output = UNKNOWN
        if info.type != VARIABLE_ID:
            info.logic = 0

    cdef void reveal(self):
        '''Re-attach this gate to the live graph and recompute its output'''
        cdef list sources = self._sources
        cdef Py_ssize_t i
        cdef Py_ssize_t n = len(sources)
        cdef int source_loc
        cdef CPP_Gate* src_info
        cdef CPP_Gate* gate_infolist=(self.info - self.location)
        cdef CPP_Gate* info = &gate_infolist[self.location]
        if info.type != VARIABLE_ID:
            for i in range(n):
                source_loc = sources[i]
                if source_loc != -1:
                    src_info = &gate_infolist[source_loc]
                    add_profile(src_info.hitlist, src_info.hitlist_count, self.profiles[0], &gate_infolist[self.location], i, src_info.output)
                    info.logic += (src_info.output == info.seed)

        cdef int p_idx = info.hitlist
        cdef Profile* p_base
        if self.profiles != NULL and self.profiles.size() > 0:
            p_base = self.profiles.data()
            while p_idx != -1:
                reveal(p_idx, self.profiles[0], self, self.gate_verse)
                p_idx = p_base[p_idx].next

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
            info.inputlimit += (size - current)
            self.process()
            return True
        elif size < current:
            for i in range(size, current):
                if self._sources[i] != -1:
                    return False
            for i in range(current - size):
                self._sources.pop()
            info.inputlimit -= (current - size)
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
            bool(info.flags & FLAG_VALUE) if info.type == VARIABLE_ID else [src_loc if src_loc != -1 and (gate_infolist[src_loc].flags & FLAG_MARK) else -1 for src_loc in self._sources],
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
        self.info.inputlimit = INFINITE
        return True

cdef class Variable(Gate):
    pass

cdef class Probe(Gate):
    pass

cdef class NOT(Gate):
    pass
