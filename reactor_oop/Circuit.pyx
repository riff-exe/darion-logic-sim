# distutils: language = c++
# cython: boundscheck=False
# cython: wraparound=False
# cython: initializedcheck=False
# cython: cdivision=True
# cython: nonecheck=False
import orjson
import time
from Gates cimport Gate, Variable, Profile, vector, CPP_Gate, Task
from Const cimport *
from IC cimport IC
from Store cimport get, decode
from cpython.list cimport PyList_GET_SIZE, PyList_GET_ITEM
from libc.stdint cimport uint8_t
from libcpp.vector cimport vector

cdef class Circuit:
    def __cinit__(self):
        self.counter = 0
        self.eval_count = 0
    def __init__(self):
        set_MODE(DESIGN)
        self.objlist = [[] for i in range(TOTAL)]
        self.copydata = []

    def __repr__(self):
        return 'Circuit'

    cpdef object getcomponent(self, int choice):
        cdef Gate gate
        cdef IC ic
        gt = get(choice)
        if gt:
            self.counter += 1
            rank = len(self.objlist[choice])
            self.objlist[choice].append(gt)
            gt.code = (choice, rank)
            if gt.id != IC_ID:
                gate = <Gate>gt
                if gate.id == VARIABLE_ID:
                    gate.info.output = LOW if MODE != DESIGN else UNKNOWN
            if DEBUG:
                if gt.id == VARIABLE_ID:
                    gt.codename = chr(ord('A') + (rank) % 26) + str((rank + 1) // 26)
                else:
                    gt.codename = gt.codename + '-' + str(len(self.objlist[choice]))
        return gt

    cpdef object getobj(self, tuple code):
        return self.objlist[code[0]][code[1]]

    cpdef void delobj(self, object gate):
        if gate.id == IC_ID:
            self.counter -= (<IC>gate).get_gate_count()
        self.counter -= 1
        self.objlist[gate.code[0]][gate.code[1]] = None

    cpdef void renewobj(self, object gate):
        if gate.id == IC_ID:
            self.counter += (<IC>gate).get_gate_count()
        self.counter += 1
        self.objlist[gate.code[0]][gate.code[1]] = gate

    cpdef list get_components(self):
        return [gate for sublist in self.objlist for gate in sublist if gate is not None]

    cpdef list get_variables(self):
        return [gate for gate in self.objlist[VARIABLE_ID] if gate is not None]

    cpdef list get_ics(self):
        return [gate for gate in self.objlist[IC_ID] if gate is not None]

    cpdef void listComponent(self):
        cdef int i = 0
        for i, gate in enumerate(self.get_components()):
            print(f'{i}. {gate}')

    cpdef void listVar(self):
        cdef int i = 0
        for i, gate in enumerate(self.get_variables()):
            print(f'{i}. {gate}')

    cpdef bint setlimits(self, Gate gate, int size):
        return gate.setlimits(size)

    cpdef void connect(self, Gate target, Gate source, int index):
        cdef int prev = target.info.output
        target.connect(source, index)
        if prev != target.info.output:
            self.queue[0][0] = <CPP_Gate*>target.info
            self.propagate(1)

    cpdef void toggle(self, Gate target, int value):
        if value != target.info.output:
            target.info.value = value
            target.info.output = value if MODE == SIMULATE else UNKNOWN
            self.queue[0][0] = <CPP_Gate*>target.info
            self.propagate(1)

    cpdef double batch_toggle(self, list batch, int batch_size=0, bint perf_trace=False):
        '''toggles multiple variables and propagates for performance'''
        cdef int value
        cdef tuple pair
        cdef double start, end
        cdef int fd
        cdef vector[CPP_Gate*] targets
        cdef vector[uint8_t] values
        cdef int i, j, n = len(batch)
        cdef Py_ssize_t end_point = 0
        cdef CPP_Gate* info

        if batch_size <= 0:
            batch_size = n

        targets.reserve(n)
        values.reserve(n)
        for pair in batch:
            targets.push_back((<Gate>pair[0]).info)
            values.push_back(pair[1])

        if perf_trace:
            import os
            try:
                fd = os.open("/tmp/rx_perf_ctrl", os.O_WRONLY | getattr(os, 'O_NONBLOCK', 0))
                if fd >= 0:
                    os.write(fd, b"enable\n")
                    os.close(fd)
            except Exception:
                pass

        start = time.perf_counter_ns()
        for i in range(0, n, batch_size):
            end_point = 0
            for j in range(batch_size):
                if i + j >= n:
                    break
                info = targets[i + j]
                value = values[i + j]
                if value != info.output:
                    info.value = value
                    info.output = value if MODE != DESIGN else UNKNOWN
                    self.queue[0][end_point] = info
                    end_point += 1
            if end_point > 0:
                self.propagate(end_point)
        end = time.perf_counter_ns()

        if perf_trace:
            import os
            try:
                fd = os.open("/tmp/rx_perf_ctrl", os.O_WRONLY | getattr(os, 'O_NONBLOCK', 0))
                if fd >= 0:
                    os.write(fd, b"disable\n")
                    os.close(fd)
            except Exception:
                pass

        return (end - start) / 1000000.0

    cpdef void disconnect(self, Gate target, int index):
        cdef int prev = target.info.output
        target.disconnect(index)
        if prev != target.info.output:
            self.queue[0][0] = <CPP_Gate*>target.info
            self.propagate(1)

    cpdef void hide(self, list gatelist):
        cdef Gate pin
        cdef IC ic
        for gate in gatelist:
            if gate.id == IC_ID:
                ic = <IC>gate
                ic.hide()
            else:
                pin = <Gate>gate
                pin.hide()
            self.delobj(gate)

        for gate in gatelist:
            if gate.id == IC_ID:
                ic = <IC>gate
                for pin in ic.outputs:
                    self.turnoff(pin)
            else:
                self.turnoff(gate)

    cpdef void reveal(self, list gatelist):
        cdef Gate pin
        cdef IC ic
        cdef Py_ssize_t end_point = 0
        cdef CPP_Gate** read_queue = self.queue[0]
        for gate in reversed(gatelist):
            if gate.id == IC_ID:
                ic = <IC>gate
                ic.reveal()
            else:
                pin = <Gate>gate
                pin.reveal()
            self.renewobj(gate)

        for gate in reversed(gatelist):
            if gate.id == IC_ID:
                ic = <IC>gate
                for pin in ic.outputs:
                    read_queue[end_point] = <CPP_Gate*>pin.info
                    end_point += 1
            else:
                read_queue[end_point] = <CPP_Gate*>(<Gate>gate).info
                end_point += 1
        if end_point > 0:
            self.propagate(end_point)

    # Result
    cpdef void output(self, Gate gate):
        print(f'{gate} output is {gate.getoutput()}')

    cpdef str truthTable(self, list variables=None, list outputs=None):
        if variables is None:
            variables = self.get_variables()
        if len(variables) == 0 or len(variables) > 16 or MODE == DESIGN:
            return ""

        cdef list gate_list = []
        cdef list var_names, gate_names, all_names, header_parts, final_table_lines, raw_rows, row_parts
        cdef str header, separator
        cdef int col_width, bit, gate_type
        cdef Py_ssize_t i, j, k, n
        cdef list IN_MAP, OUT_MAP
        cdef tuple v_states, g_states

        # Filter gatelist
        if outputs is not None:
            gate_list = outputs
        else:
            for item in self.get_components():
                gate_type = item.id
                if gate_type == VARIABLE_ID:
                    continue
                elif gate_type != IC_ID:
                    gate_list.append(item)
                else:
                    for pin in item.outputs:
                        gate_list.append(pin)

        n = len(variables)
        cdef int rows_count = 1 << n
        cdef Gate var, gate

        var_names = [str(v) for v in variables]
        gate_names = [str(v) for v in gate_list]
        all_names = var_names + gate_names

        if len(all_names) > 0:
            col_width = max([len(name) for name in all_names]) + 2
        else:
            col_width = 4

        IN_MAP = ["0".center(col_width), "1".center(col_width)]
        OUT_MAP = ["F".center(col_width), "T".center(col_width), "X".center(col_width)]

        header_parts = [name.center(col_width) for name in all_names]
        header = " | ".join(header_parts)
        separator = "─" * len(header)

        raw_rows = [None] * rows_count

        cdef int gray = 0
        cdef int prev_gray = 0
        cdef int mask, changed_bit, temp, bl
        cdef Py_ssize_t end_point

        for i in range(rows_count):
            prev_gray = gray
            gray = i ^ (i >> 1)

            if i != 0:
                mask = prev_gray ^ gray

                if mask == 1: changed_bit = 0
                elif mask == 2: changed_bit = 1
                elif mask == 4: changed_bit = 2
                elif mask == 8: changed_bit = 3
                elif mask == 16: changed_bit = 4
                elif mask == 32: changed_bit = 5
                elif mask == 64: changed_bit = 6
                elif mask == 128: changed_bit = 7
                elif mask == 256: changed_bit = 8
                elif mask == 512: changed_bit = 9
                elif mask == 1024: changed_bit = 10
                elif mask == 2048: changed_bit = 11
                elif mask == 4096: changed_bit = 12
                elif mask == 8192: changed_bit = 13
                elif mask == 16384: changed_bit = 14
                elif mask == 32768: changed_bit = 15
                else: changed_bit = 0

                j = (n - 1) - changed_bit
                var = variables[j]
                bit = 1 if (gray & mask) else 0
                if bit != var.info.output:
                    var.info.output = bit
                    self.queue[0][0] = <CPP_Gate*>var.info
                    self.propagate(1)
            else:
                end_point = 0
                for j in range(n):
                    var = variables[j]
                    if var.info.output != 0:
                        var.info.output = 0
                        self.queue[0][end_point] = <CPP_Gate*>var.info
                        end_point += 1
                if end_point > 0:
                    self.propagate(end_point)

            v_states = tuple([(<Gate>v).info.output for v in variables])
            g_states = tuple([(<Gate>g).info.output for g in gate_list])
            raw_rows[gray] = (v_states, g_states)

        self.simulate(SIMULATE)

        final_table_lines = [separator, header, separator]
        for v_states, g_states in raw_rows:
            row_parts = [IN_MAP[v] for v in v_states]
            row_parts.extend([OUT_MAP[g] for g in g_states])
            final_table_lines.append(" | ".join(row_parts))

        final_table_lines.append(separator)
        final_table_lines.append("")

        return "\n".join(final_table_lines)

    def diagnose(self):
        print("=" * 90)
        print(" " * 35 + "CIRCUIT DIAGNOSIS")
        print("=" * 90)

        gates = [c for c in self.get_components() if c.id != IC_ID]
        if gates:
            columns = [
                ("Component", 14),
                ("Sources", 28),
                ("Book[L,H,U]", 15),
                ("Targets", 25),
                ("Out", 6)
            ]
            total_width = sum(w for _, w in columns)
            fmt = "".join(f"{{:<{w}}}" for _, w in columns)

            print("\n" + fmt.format(*[n for n, _ in columns]))
            print("-" * total_width)

            for comp in gates:
                ch = [f"[{i}]:{c}" for i, c in enumerate(comp.sources) if c is not None]
                ch_str = ", ".join(ch) if ch else "None"

                book = f"[{comp.book[0]},{comp.book[1]},{comp.book[2]}]"

                tgt = [f"{target} " for target in comp.hitlist]
                tgt_str = ", ".join(tgt) if tgt else "None"

                ch_str = ch_str[:26] + ".." if len(ch_str) > 28 else ch_str
                tgt_str = tgt_str[:23] + ".." if len(tgt_str) > 25 else tgt_str

                print(fmt.format(str(comp), ch_str, book, tgt_str, str(comp.getoutput())))

            print("-" * total_width)

        cdef list ics = [c for c in self.objlist[IC_ID] if c is not None]
        if ics:
            print("\n" + "=" * 90)
            print(" " * 40 + "IC STATUS")
            print("=" * 90)
            for ic in ics:
                print(f"\n  IC: {repr(ic)} (Code: {ic.code})")
                print("  " + "-" * 50)

                if ic.inputs:
                    print("  INPUT PINS:")
                    for pin in ic.inputs:
                        ch = [f"{c}" for c in pin.sources if c is not None]
                        targets = [f"{target} " for target in pin.hitlist]
                        print(f"    {repr(pin)}: out={pin.getoutput()}, from={', '.join(ch) if ch else 'None'}, to={', '.join(targets) if targets else 'None'}")

                if ic.outputs:
                    print("  OUTPUT PINS:")
                    for pin in ic.outputs:
                        ch = [f"{c}" for c in pin.sources if c is not None]
                        targets = [f"{target} " for target in pin.hitlist]
                        print(f"    {repr(pin)}: out={pin.getoutput()}, from={', '.join(ch) if ch else 'None'}, to={', '.join(targets) if targets else 'None'}")

        print("\n" + "=" * 90)

    cpdef void writetojson(self, str location):
        cdef list circuit = []
        for gate in self.get_components():
            circuit.append(gate.full_data())
        with open(location, 'wb') as file:
            file.write(orjson.dumps(circuit))

    cpdef void generate(self, list circuit):
        '''generate the circuit from the list of info'''
        cdef dict pseudo = {}
        pseudo[-1] = None
        cdef list varlist = []
        cdef object obj
        cdef Gate gate
        cdef IC ic
        cdef list info
        cdef list ic_list = []
        for info in circuit:
            if info[ID] == IC_ID:
                ic = <IC>self.getcomponent(info[ID])
                ic.custom_name = info[CUSTOM_NAME]
                ic.map = info[MAP]
                ic.load_components(info, pseudo)
                ic_list.append(ic)
                self.counter += ic.get_gate_count()
            else:
                gate = <Gate>self.getcomponent(info[ID])
                if gate.id == VARIABLE_ID:
                    gate.info.output = UNKNOWN
                    varlist.append(gate)
                pseudo[info[LOCATION]] = gate
        for info in circuit:
            if info[ID] != IC_ID:
                gate = <Gate>pseudo[info[LOCATION]]
                gate.clone(info, pseudo)
        for ic in ic_list:
            ic.implement(pseudo)
        self.recalculate_counter()
        if MODE != DESIGN:
            self.custom_simulate(varlist)

    cpdef void readfromjson(self, str location):
        cdef list circuit
        with open(location, 'rb') as file:
            circuit = orjson.loads(file.read())
        if isinstance(circuit, dict):
            return
        self.generate(circuit)
        if MODE != DESIGN:
            self.simulate(SIMULATE)

    cpdef IC build_ic(self):
        cdef Gate gate, target
        cdef Profile* profile
        cdef Profile* end
        cdef IC my_ic = self.getcomponent(IC_ID)
        cdef list queue = []
        cdef list outputs = [i for i in self.objlist[IC_OUTPUT_PIN_ID] if i is not None]
        cdef list inputs = [i for i in self.objlist[IC_INPUT_PIN_ID] if i is not None]
        for gate in outputs + inputs:
            gate.info.scheduled = 1
            queue.append(gate)
        cdef Py_ssize_t size = len(queue)
        cdef Py_ssize_t index = len(outputs)
        while index < size:
            gate = queue[index]
            if gate.id == IC_INPUT_PIN_ID and gate.sources[0] is not None:
                profile = (<CPP_Gate*>gate.info).hitlist.data()
                end = profile + (<CPP_Gate*>gate.info).hitlist.size()
                while profile != end:
                    target = <Gate>(<CPP_Gate*>profile.target).gate
                    target.sources[profile.index] = gate.sources[0]
                    profile += 1
            elif gate.id == IC_OUTPUT_PIN_ID and not (<CPP_Gate*>gate.info).hitlist.empty():
                profile = (<CPP_Gate*>gate.info).hitlist.data()
                end = profile + (<CPP_Gate*>gate.info).hitlist.size()
                while profile != end:
                    target = <Gate>(<CPP_Gate*>profile.target).gate
                    target.sources[profile.index] = gate.sources[0]
                    profile += 1
            profile = (<CPP_Gate*>gate.info).hitlist.data()
            end = profile + (<CPP_Gate*>gate.info).hitlist.size()
            while profile != end:
                target = <Gate>(<CPP_Gate*>profile.target).gate
                if not target.info.scheduled:
                    target.info.scheduled = 1
                    queue.append(target)
                    size += 1
                profile += 1
            index += 1
        cdef int pins = len(inputs) + len(outputs)
        for input_pin in inputs:
            my_ic.addgate(input_pin)
        for output_pin in outputs:
            my_ic.addgate(output_pin)
        for index in range(pins, size):
            gate = queue[index]
            if gate.id >= IC_INPUT_PIN_ID:
                continue
            my_ic.addgate(gate)
        return my_ic

    cpdef void ic_pin_change(self):
        cdef Gate var, probe
        for var in self.objlist[VARIABLE_ID]:
            if var is not None:
                var.code = (IC_INPUT_PIN_ID, len(self.objlist[IC_INPUT_PIN_ID]))
                var.id = IC_INPUT_PIN_ID
                self.objlist[IC_INPUT_PIN_ID].append(var)
        self.objlist[VARIABLE_ID].clear()

        for probe in self.objlist[BUFFER_ID]:
            if probe is not None:
                probe.code = (IC_OUTPUT_PIN_ID, len(self.objlist[IC_OUTPUT_PIN_ID]))
                probe.id = IC_OUTPUT_PIN_ID
                self.objlist[IC_OUTPUT_PIN_ID].append(probe)
        self.objlist[BUFFER_ID].clear()

    cpdef void transfer_info(self, Gate gate, int id):
        if id >= IC_ID or id < 0:
            return
        cdef list real_source = [source for source in gate.sources if source is not None]
        cdef int length = len(real_source)
        if not real_source or (length == 1 and id != VARIABLE_ID) or (length > 1 and id < BUFFER_ID):
            if gate.sources[0] is None:
                self.objlist[gate.code[0]][gate.code[1]] = None
                gate.id = id
                gate.code = (id, len(self.objlist[id]))
                self.objlist[id].append(gate)
                gate.process()
                self.queue[0][0] = <CPP_Gate*>gate.info
                self.propagate(1)

    cpdef void reorder(self, object gate, int index):
        cdef list lst = self.objlist[(<Gate>gate).id]
        if index < 0 or index >= len(lst):
            return
        cdef object old = lst[index]
        lst[index] = gate
        lst[gate.code[1]] = old
        if old is not None:
            old.code, gate.code = gate.code, old.code
        else:
            gate.code = (gate.code[0], index)

    cpdef void save_as_ic(self, str location, str ic_name, str tag, str description, list components):
        cdef Circuit crct
        if components:
            crct = Circuit()
            crct.copy(components)
            crct.paste()
            crct.save_as_ic(location, ic_name, tag, description, None)
            return
        if len(self.objlist[VARIABLE_ID]) or len(self.objlist[BUFFER_ID]):
            self.ic_pin_change()
        for gate in self.objlist[IC_INPUT_PIN_ID]:
            if gate and (<Gate>gate).sources[0] is not None:
                raise ValueError('Input Pin has extra sources')
        for gate in self.objlist[IC_OUTPUT_PIN_ID]:
            if gate and (<CPP_Gate*>(<Gate>gate).info).hitlist.size() > 0:
                raise ValueError('Output Pin has extra targets')

        cdef IC my_ic = self.build_ic()
        my_ic.custom_name = ic_name
        my_ic.tag = tag
        my_ic.description = description
        with open(location, 'wb') as file:
            file.write(orjson.dumps(my_ic.partial_data()))
        self.clearcircuit()

    cpdef object get_ic(self, str location):
        with open(location, 'rb') as file:
            crct = orjson.loads(file.read())
        if isinstance(crct[LOCATION], list):
            return crct
        else:
            print('Cannot Convert to IC')
            return None

    cpdef IC load_ic(self, list crct):
        cdef IC myIC = self.getcomponent(IC_ID)
        myIC.configure(crct)
        self.counter += myIC.get_gate_count()
        return myIC

    cpdef IC getIC(self, location):
        cdef list crct = self.get_ic(location)
        if crct is None:
            return None
        return self.load_ic(crct)

    cpdef void recalculate_counter(self):
        cdef int total = 0
        cdef object g
        cdef int i
        cdef IC ic
        for i in range(TOTAL):
            for g in self.objlist[i]:
                if g is not None:
                    if i == IC_ID:
                        ic = <IC>g
                        total += 1 + ic.get_gate_count()
                    else:
                        total += 1
        self.counter = total

    cpdef void rank_reset(self):
        for i in range(TOTAL):
            while self.objlist[i] and self.objlist[i][len(self.objlist[i]) - 1] is None:
                self.objlist[i].pop()

    cpdef void clearcircuit(self):
        for i in range(TOTAL):
            self.objlist[i].clear()
        self.counter = 0

    cpdef void copy(self, list components):
        if len(components) == 0:
            return
        self.copydata = []
        cluster: list = []
        for i in components:
            i.load_to_cluster(cluster)
        for i in components:
            self.copydata.append(i.partial_data())
        for i in cluster:
            (<Gate>i).info.scheduled = 0

    cpdef list paste(self):
        cdef list circuit = self.copydata
        cdef dict pseudo = {}
        pseudo[-1] = None
        cdef list new_items = []
        cdef list varlist = []
        cdef object gate
        cdef Gate g
        cdef IC ic
        cdef list ic_list = []
        for info in circuit:
            if info[ID] == IC_ID:
                ic = <IC>self.getcomponent(info[ID])
                ic.custom_name = info[CUSTOM_NAME]
                ic.map = info[MAP]
                ic.load_components(info, pseudo)
                ic_list.append(ic)
                new_items.append(ic)
            else:
                g = <Gate>self.getcomponent(info[ID])
                if g.id == VARIABLE_ID:
                    g.info.output = UNKNOWN
                    varlist.append(g)
                pseudo[info[LOCATION]] = g
                new_items.append(g)

        for gate_info in circuit:
            if gate_info[ID] != IC_ID:
                g = <Gate>pseudo[gate_info[LOCATION]]
                g.clone(gate_info, pseudo)
        for ic in ic_list:
            ic.implement(pseudo)

        if MODE != DESIGN:
            self.custom_simulate(varlist)
        return new_items

    cpdef void simulate(self, int Mod):
        set_MODE(Mod)
        cdef Gate variable
        cdef Py_ssize_t end_point = 0
        cdef CPP_Gate** read_queue = self.queue[0]
        for variable in self.objlist[VARIABLE_ID]:
            if variable is not None:
                variable.info.output = variable.info.value
                read_queue[end_point] = <CPP_Gate*>variable.info
                end_point += 1
        if end_point > 0:
            self.propagate(end_point)

    cpdef void custom_simulate(self, list varlist):
        '''simulate from a pre-collected list of variable Gate objects'''
        cdef Gate variable
        cdef Py_ssize_t end_point = 0
        cdef CPP_Gate** read_queue = self.queue[0]
        for variable in varlist:
            variable.info.output = variable.info.value
            read_queue[end_point] = <CPP_Gate*>variable.info
            end_point += 1
        if end_point > 0:
            self.propagate(end_point)

    cpdef void reset(self):
        set_MODE(DESIGN)
        for i in self.get_components():
            if i.id != IC_ID:
                (<Gate>i).reset()
            else:
                (<IC>i).reset()

    cpdef void optimize(self):
        pass  # not implemented in reactor_oop

    cpdef list geometry(self):
        '''Not implemented in reactor_oop — returns empty list.'''
        return []

    cdef inline void turnoff(self, Gate gate):
        cdef Profile* profile = (<CPP_Gate*>gate.info).hitlist.data()
        cdef Profile* end = profile + (<CPP_Gate*>gate.info).hitlist.size()
        cdef CPP_Gate* target_info
        while profile != end:
            target_info = <CPP_Gate*>profile.target
            if target_info != gate.info:
                target_info.output = UNKNOWN
                self.queue[0][0] = target_info
                self.propagate(1)
            profile += 1

    cdef void burn(self, Py_ssize_t index, Py_ssize_t size,
                   CPP_Gate** read_queue, CPP_Gate** write_queue):
        cdef CPP_Gate* gate_info
        cdef CPP_Gate* target_info
        cdef Profile* profile
        cdef Profile* end
        cdef unsigned long long eval = 0
        cdef Py_ssize_t end_point = size
        size = 0
        while index < end_point:
            while index < end_point:
                gate_info = <CPP_Gate*>read_queue[index]
                gate_info.mark = 0
                profile = gate_info.hitlist.data()
                end = profile + gate_info.hitlist.size()
                gate_info.output = UNKNOWN
                while profile != end:
                    eval += 1
                    if profile.output != UNKNOWN:
                        target_info = <CPP_Gate*>profile.target
                        target_info.logic -= (profile.output == target_info.seed)
                        if target_info.output != UNKNOWN:
                            write_queue[size] = <CPP_Gate*>target_info
                            size += 1
                        profile.output = UNKNOWN
                    profile += 1
                index += 1
            index = 0
            end_point = size
            size = 0
            read_queue, write_queue = write_queue, read_queue
        self.eval_count += eval

    cdef void propagate(self, Py_ssize_t end_point):
        cdef CPP_Gate* gate_info
        cdef CPP_Gate* target_info
        cdef Profile* profile
        cdef Profile* end
        cdef Py_ssize_t new_output, profile_output, target_output
        cdef Py_ssize_t index = 0, size = 0
        cdef unsigned long long counter = 0
        cdef unsigned long long eval = 0
        cdef CPP_Gate** read_queue = self.queue[0]
        cdef CPP_Gate** write_queue = self.queue[1]

        if unlikely(end_point == 1 and read_queue[0].output == UNKNOWN and read_queue[0].type >= BUFFER_ID):
            self.burn(0, 1, read_queue, write_queue)
            return

        while end_point > 0:
            if unlikely(counter > self.counter):
                self.eval_count += eval
                self.burn(index, end_point, read_queue, write_queue)
                return

            counter += 1
            for index in range(end_point):
                gate_info = read_queue[index]
                gate_info.mark = 0
                new_output = gate_info.output
                profile = gate_info.hitlist.data()
                end = profile + gate_info.hitlist.size()
                eval += gate_info.hitlist.size()
                while profile < end:
                    profile_output = profile.output
                    target_info = profile.target
                    target_info.logic += (new_output == target_info.seed) - (profile_output == target_info.seed)
                    target_output = target_info.output
                    if unlikely(new_output == UNKNOWN):
                        target_info.output = UNKNOWN
                    else:
                        target_info.compute()

                    write_queue[size] = target_info
                    size += (((target_info.mark == 0) & (target_output != target_info.output)))
                    target_info.mark |= (target_output != target_info.output)
                    profile.output = new_output
                    profile += 1
            end_point = size
            size = 0
            read_queue, write_queue = write_queue, read_queue

        self.eval_count += eval
