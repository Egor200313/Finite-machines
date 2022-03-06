import copy
from collections import deque
from src.MachineVisitor import MachineVisitor
from src.Edge import Edge
from src.Path import Path, only_empty, symbol_empty


class StateMachine:
    def __init__(self):
        self.start_state = 0
        self.final_states = []
        self.edges = []
        self.alphabet = []
        self.states = set()

    def set_states(self):  # устанавливаем состояния по массиву переходов
        self.states = set()
        for edge in self.edges:
            self.states.add(edge.prev)
            self.states.add(edge.next)

    def has_transitive_eps_paths(self):  # ищем переходы вида -empty->-empty->
        two_edges_paths = [Path(first_edge=edge1, second_edge=edge2)
                           for edge1 in self.edges for edge2 in self.edges
                           if edge1.next == edge2.prev]

        empty_paths = list(filter(only_empty, two_edges_paths))

        no_previous = list(filter(lambda path:
                                  Edge(path.start_state, path.final_state, "empty") not in self.edges,
                                  empty_paths))

        not_loops = list(filter(lambda path: path.start_state != path.final_state, no_previous))

        return not_loops

    def add_eps(self):  # добавляем транзитивные переходы по empty
        arr = self.has_transitive_eps_paths()
        while arr:
            for path in arr:
                self.edges.append(Edge(prev=path.start_state, next=path.final_state, symbol="empty"))
            arr = self.has_transitive_eps_paths()

    def make_new_terms(self):  # добавляем в терминальные те состояния, которые по empty приводили в терминальные
        for edge in [edge for edge in self.edges if edge.next in self.final_states and edge.symbol == "empty"]:
            self.final_states.append(edge.prev)

    def has_symbol_eps_path(self):  # ищем переходы вида -a->-empty->
        two_edges_paths = [Path(first_edge=edge1, second_edge=edge2)
                           for edge1 in self.edges for edge2 in self.edges
                           if edge1.next == edge2.prev]

        symbol_empty_paths = list(filter(symbol_empty, two_edges_paths))

        no_previous = list(filter(lambda path:
                                  Edge(path.start_state, path.final_state, path.first_word) not in self.edges,
                                  symbol_empty_paths))

        not_loops = list(filter(lambda path: path.start_state != path.final_state, no_previous))

        return not_loops

    def add_one_symbol_path(self):  # добавляем переходы по одной букве там, где были переходы по букве и empty
        symbol_eps_paths = self.has_symbol_eps_path()
        while symbol_eps_paths:
            for path in symbol_eps_paths:
                self.edges.append(Edge(prev=path.start_state, next=path.final_state, symbol=path.first_word))
                symbol_eps_paths = self.has_symbol_eps_path()

    def delete_eps_paths(self):  # удаляем empty переходы
        arr = [edge for edge in self.edges if edge.symbol != "empty"]
        self.edges = arr
        self.set_states()

    def delete_unreachable_states(self, states: [int]):  # удаляем недостижимые вершины и переходы в них/из них
        self.final_states = [state for state in self.final_states if state not in states]
        arr = [edge for edge in self.edges if edge.prev not in states
               and edge.next not in states]
        self.edges = arr
        self.set_states()

    def delete_eps(self):
        self.add_eps()
        self.make_new_terms()
        self.add_one_symbol_path()
        self.delete_eps_paths()
        machine = MachineVisitor()
        self.delete_unreachable_states(machine.get_unreachable_states(self))
        self.alphabet = [symbol for symbol in self.alphabet if symbol != "empty"]

    def __eq__(self, other):
        return self.start_state == other.start_state \
               and sorted(self.edges) == sorted(other.edges) \
               and set(self.final_states) == set(other.final_states)

    def create_DFSM(self):  # создаем детерминированный конечный автомат (Deterministic Finite State Machine)
        states_to_process = deque()  # очередь перебора вершин
        new_edges = []  # новые переходы
        match_number = {}  # словарь сопоставляющий множество объединенных вершин одному числу
        first_state_set = set()
        first_state_set.add(self.start_state)
        states_to_process.append(first_state_set)
        match_number[frozenset(first_state_set)] = 0
        while states_to_process:
            state = states_to_process.popleft()  # извлекаем вершину для обработки
            for symbol in self.alphabet:
                # состояния в которые можно попасть по symbol из текущего объединения
                next_states = set([edge.next for edge in self.edges 
                                   if edge.symbol == symbol and edge.prev in state])
                if next_states:  # если есть куда идти по symbol
                    # добавляем новое состояние если оно не встречалось ранее
                    if frozenset(next_states) not in match_number.keys():
                        states_to_process.append(next_states)
                        match_number[frozenset(next_states)] = len(match_number)  # даем новому состоянию короткое имя
                    new_edges.append(Edge(prev=match_number[frozenset(state)],
                                          next=match_number[frozenset(next_states)],
                                          symbol=symbol)
                                     )

        new_final_states = [match_number[frozenset(state)] for state in match_number.keys()
                            if state & set(self.final_states)]
        new_start_state = 0
        self.final_states = new_final_states
        self.start_state = new_start_state
        self.edges = new_edges
        self.set_states()

    def complete_DFSM(self):  # строит ПДКА по ДКА DFSM = "Deterministic Finite State Machine"
        last_state_number = max(self.states)
        # заводим стоковую вершину, куда отправим переходы из каждого
        # состояния по недостающей букве
        stock_state = last_state_number + 1
        has_stock = False
        for state in self.states:
            for symbol in self.alphabet:
                path = [edge for edge in self.edges if edge.symbol == symbol and edge.prev == state]
                if not path:  # если нет перехода, отправляем его в сток
                    self.edges.append(Edge(prev=state, 
                                           next=stock_state, 
                                           symbol=symbol)
                                      )
                    has_stock = True
        if has_stock:
            # добавляем петли во всем символам алфавита для стока
            for symbol in self.alphabet:
                self.edges.append(Edge(prev=stock_state, 
                                       next=stock_state, 
                                       symbol=symbol)
                                  )
        self.set_states()

    def create_addition(self):  # строит по ПДКА дополнение к ПДКА
        self.final_states = [state for state in self.states if state not in self.final_states]

    def delete_state(self, state_to_delete: int):
        # пути из двух переходов проходящие через удаляемое состояние
        paths = [Path(first, second) for first in self.edges for second in self.edges if
                 first.next == second.prev and first.next == state_to_delete 
                 and first.prev != first.next and second.prev != second.next]

        # символы на петлях у удаляемого состояния
        cycles = [edge.symbol for edge in self.edges 
                  if edge.prev == edge.next and edge.prev == state_to_delete]

        # регулярка на петле удаляемого состояния
        cycle_regex = ""
        if cycles:
            for word in cycles[:len(cycles) - 1]:
                cycle_regex += word + "+"
            cycle_regex += cycles[len(cycles) - 1]

        for path in paths:
            # если была петля, то вклиниваем ее в путь
            if cycle_regex:
                path.word = path.first_word + "("+cycle_regex+")*" + path.second_word

            # путь, который уже присутвовал
            previous_uv_path_word = [edge.symbol for edge in self.edges if edge.prev == path.start_state
                                     and edge.next == path.final_state]
            result_regex = path.word
            if previous_uv_path_word:
                result_regex += "+" + previous_uv_path_word[0]

            # удаляем переходы которые уже были
            self.edges = [edge for edge in self.edges 
                          if edge.prev != path.start_state or edge.next != path.final_state]
            # заменяем на новый переход по регулярке
            self.edges.append(Edge(prev=path.start_state, next=path.final_state, symbol=result_regex))

        # удаляем переходы затрагивающие удаленное состояние
        self.edges = [edge for edge in self.edges 
                      if edge.prev != state_to_delete and edge.next != state_to_delete]
        self.states.remove(state_to_delete)

    @staticmethod
    def get_regex_for_one_start_one_final_state_machine(machine):
        final_state = machine.final_states[0]
        start_state_set = set()
        start_state_set.add(machine.start_state)
        to_delete = machine.states - set(machine.final_states) - start_state_set
        for state in to_delete:  # удаляем все состояния кроме начала и конца
            machine.delete_state(state)

        # ищем обратные ребра которые нужно заменить на петли у терминальной вершины
        reverse = [edge.symbol for edge in machine.edges if
                   edge.prev == final_state and edge.next == machine.start_state and edge.prev != edge.next]
        if reverse:
            final_cycle = [edge.symbol for edge in machine.edges if edge.prev == edge.next and edge.prev == final_state]
            final_cycle_regex = final_cycle[0] if final_cycle else ""

            word = reverse[0]  # слово по которому переходим из терминального состояния в начальное

            start_cycle = [edge.symbol for edge in machine.edges if edge.prev == edge.next and edge.prev == machine.start_state]
            start_cycle_regex = ("(" + start_cycle[0] + ")*") if start_cycle else ""

            # слово по которому переходим из стартового состояния в конечное
            path_to_end_word = [edge.symbol for edge in machine.edges if edge.prev == machine.start_state and edge.next == final_state]

            if final_cycle_regex:
                cycle_regex = final_cycle_regex + "+" + word + start_cycle_regex + path_to_end_word[0]
            else:
                cycle_regex = word + start_cycle_regex + path_to_end_word[0]

            # удаляем переходы назад
            machine.edges = [edge for edge in machine.edges if edge.prev != final_state or edge.next != machine.start_state]

            # добавляем новый переход как петлю из конечного состояния в конечное
            machine.edges.append(Edge(final_state, final_state, cycle_regex))

        start_loop_word = [edge.symbol for edge in machine.edges if edge.prev == machine.start_state and edge.prev == edge.next]
        transition_word = [edge.symbol for edge in machine.edges if edge.prev == machine.start_state and edge.next == final_state]
        final_loop_word = [edge.symbol for edge in machine.edges if edge.prev == final_state and edge.prev == edge.next]

        start_state_loop_regex = ("(" + start_loop_word[0] + ")*") if start_loop_word else ""
        transition_regex = (transition_word[0]) if transition_word else ""
        final_state_loop_regex = ("(" + final_loop_word[0] + ")*") if final_loop_word else ""

        final_regex = start_state_loop_regex
        final_regex += transition_regex if transition_regex else ""
        final_regex += final_state_loop_regex if final_state_loop_regex else ""

        return final_regex

    def get_regex(self):
        result_regex = ""
        for first, second in zip(self.states, self.states):  # объединяем кратные переходы
            uv_paths = [edge.symbol for edge in self.edges if edge.prev == first and edge.next == second]
            uv_regex = ""
            if uv_paths:  # если уже есть переходы между first и second, суммируем их в регулярке
                for word in uv_paths:
                    uv_regex += word + "+"
                uv_regex = uv_regex[:len(uv_regex)-1]
            if uv_regex:  # если получился переход, добавляем его в массив
                self.edges = [edge for edge in self.edges if edge.prev != first or edge.next != second]
                self.edges.append(Edge(first, second, uv_regex))
        start_state_set = set()  # множество из одного стартового состояния
        start_state_set.add(self.start_state)
        states_to_delete = self.states - set(self.final_states) - start_state_set
        for state in states_to_delete:  # удалили все состояния, которые не являются стартовыми или терминальными
            self.delete_state(state)

        for state in self.final_states:  # для каждого терминального состояния создаем свой автомат
            machine = copy.deepcopy(self)
            machine.final_states = [state]
            machine_regex = self.get_regex_for_one_start_one_final_state_machine(machine)
            if machine_regex:  # добавляем результат к итоговой регулярке
                if result_regex:
                    result_regex += "+" + machine_regex
                else:
                    result_regex += machine_regex
        return result_regex

    def minimize(self):
        go = []  # go[state][symbol] - состояние в которое переходим из state по symbol
        for state in self.states:
            match = [(edge.symbol, edge.next) for edge in self.edges if edge.prev == state]
            go.append(dict(match))

        component_for = []
        transitions = []  # transitions[class][symbol] - класс эквивалентности в который переходим из
        # класса class по символу symbol

        for i in range(len(self.states)):
            component_for.append(1 if i in self.final_states else 0)  # заполняем массив компонент
            # по 0 эквивалентности
            alphabet_match = [-1 for i in range(len(self.alphabet))]
            transitions.append(dict(zip(self.alphabet, alphabet_match)))

        last = copy.deepcopy(component_for)
        while True:
            for state in self.states:
                for symbol in self.alphabet:
                    transitions[state][symbol] = component_for[go[state][symbol]]
            match = {}  # сопоставляет наборам состояний, в которые мы переходим из текущего,
            #  новый класс эквивалентности
            for state in self.states:
                # добавляем новый класс, если такого набора еще не встречалось
                new_class = (component_for[state],) + tuple(transitions[state].values())
                if new_class not in match.keys():
                    match[new_class] = len(match)
                component_for[state] = match[new_class]
            if last == component_for:  # выходим из цикла, если компоненты не изменились
                break
            last = copy.deepcopy(component_for)

        start = component_for[self.start_state]  # стартовый класс
        finals = set()  # новые терминальные состояния
        edges = []  # новые переходы
        for state in self.states:
            if state in self.final_states:
                finals.add(component_for[state])
            for symbol in self.alphabet:
                edge = Edge(prev=component_for[state], next=transitions[state][symbol], symbol=symbol)
                if edge not in edges:
                    edges.append(edge)

        self.start_state = start
        self.final_states = list(finals)
        self.edges = edges
        self.set_states()

    def has_word(self, word: str):
        self.complete_DFSM()
        go = []  # go[state][symbol] - состояние в которое переходим из state по symbol
        for state in self.states:
            match = [(edge.symbol, edge.next) for edge in self.edges if edge.prev == state]
            go.append(dict(match))

        current_state = self.start_state
        for letter in word:
            current_state = go[current_state][letter]

        if current_state in self.final_states:
            return True
        else:
            return False

    def max_prefix(self, word: str):
        self.complete_DFSM()
        go = []  # go[state][symbol] - состояние в которое переходим из state по symbol
        for state in self.states:
            match = [(edge.symbol, edge.next) for edge in self.edges if edge.prev == state]
            go.append(dict(match))

        prefix_len = -1
        current_state = self.start_state
        for counter, letter in enumerate(word):
            if current_state in self.final_states:
                prefix_len = counter
            if letter not in self.alphabet:
                if prefix_len == -1:
                    return "INF"
                return prefix_len
            current_state = go[current_state][letter]
        if current_state in self.final_states:
            prefix_len = len(word)
        if prefix_len == -1:
            return "INF"
        return prefix_len

