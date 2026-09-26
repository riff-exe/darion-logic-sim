# distutils: language = c++
from Const cimport HIGH, LOW, ERROR, UNKNOWN, DESIGN, SIMULATE, MODE
from libc.stdint cimport uint8_t,int8_t,uint16_t
from libcpp.unordered_map cimport unordered_map
from libcpp.deque cimport deque
cdef extern from "<vector>" namespace "std" nogil:
    cdef cppclass vector[T, ALLOCATOR=*]:
        cppclass iterator:
            T& operator*()
            iterator operator++()
            bint operator!=(iterator)
            bint operator==(iterator)
            
        vector()
        
        T& operator[](int)
        T& at(int)
        T& front()
        T& back()           
        T* data()           

        void push_back(T&)
        void emplace_back(...)  
        void pop_back()         
        void clear()
        void reserve(int)
        void resize(int)
        
        bint empty()
        int size()
        int capacity()
        iterator begin()
        iterator end()
        void swap(vector[T]&)

cdef class Gate
cdef class Variable

cdef extern from "Profile.h":
    cdef cppclass Profile:
        CPP_Gate* target
        int next
        uint8_t index
        uint8_t output
        Profile()
        Profile(CPP_Gate* target, int pin_index, int output)
        Profile(CPP_Gate* target, int pin_index, int output, int next)
    cdef cppclass Task:
        int gate_loc
        unsigned int time
        int location
        Task() nogil
        Task(int gate_loc, unsigned int time, int location) nogil
        bint operator>(const Task& other) nogil
    cdef cppclass CPP_Gate:
        int8_t type
        uint8_t output
        uint8_t inputlimit
        uint8_t flags
        uint8_t logic
        uint8_t seed
        uint16_t hitlist_count
        unsigned int target_time
        int hitlist
        CPP_Gate()
        CPP_Gate(uint8_t t, uint8_t lim)
        void compute() noexcept nogil

cdef enum GateFlags:
    FLAG_VALUE     = 1 << 0
    FLAG_SCHEDULED = 1 << 1
    FLAG_MARK      = 1 << 2
    FLAG_UPDATE    = 1 << 3

cdef void hide(int p_idx, vector[Profile]& profiles, CPP_Gate* gate_infolist, list gate_verse)
cdef void reveal(int p_idx, vector[Profile]& profiles, Gate source, list gate_verse)
cdef void pop(int& head, uint16_t& count, vector[Profile]& profiles, CPP_Gate* gate_infolist, CPP_Gate* target, int pin_index)
cdef void add_profile(int& head, uint16_t& count, vector[Profile]& profiles, CPP_Gate* target, int pin_index, uint8_t output)

cdef class Gate:
# --- 4-BYTE ALIGNED (HOT C-TYPES) ---
    cdef public int8_t id
    cdef public int location
    cdef CPP_Gate* info
    cdef vector[Profile]* profiles
    # --- 8-BYTE ALIGNED (COLD PYTHON OBJECTS) ---
    cdef public list _sources
    cdef public list gate_verse
    cdef public tuple code
    cdef public str codename
    cdef public str custom_name
    cdef public list delay_book

    cdef void process(self)
    cpdef void rename(self, str name)
    cpdef void deregister(self)
    cdef void connect(self, int source, int index)
    cdef void disconnect(self, int index)
    cdef void reset(self)
    cdef void hide(self)
    cdef void reveal(self)
    cpdef bint setlimits(self, int size)
    cpdef str getoutput(self)
    cpdef list full_data(self)
    cpdef list partial_data(self)
    cdef void clone(self, list dictionary, unordered_map[int,int]& pseudo)
    cpdef void load_to_cluster(self, list cluster)
    cpdef bint set_pulse(self, int val, int time_type)
    cpdef bint clock(self)

cdef class Variable(Gate):
    pass

cdef class Probe(Gate):
    pass


cdef class NOT(Gate):
    pass

