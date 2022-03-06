from src.MachineBuilder import MachineBuilder
from src.Edge import Edge
from src.Vertex import Vertex, union, concatenate, iteration
import string


class RegexParseTree:
    def __init__(self, regexp: str):
        self.alphabet = set(list(string.printable))
        self.follow_pos = {}  # follow_pos[position] множество позиций в регулярке с которых может
        # начинаться слово приинадлежащее языку
        vertex_symbol = dict()  # сопоставляет множеству позиций одно число
        calling_stack = []
        regexp += "#."  # добавляем терминирующий символ
        self.tree = []  # дерево в виде массива вершин
        for counter, letter in enumerate(regexp):
            if letter == "1":
                letter = "empty"
            if letter == ".":
                if len(calling_stack) < 2:  # если в стеке меньше двух компонент применить
                    # конкатенацию нельзя
                    raise Exception("Unexpected . symbol!")
                right_vertex = calling_stack.pop()
                left_vertex = calling_stack.pop()
                self.tree.append(concatenate(first_vertex=left_vertex,
                                             second_vertex=right_vertex,
                                             number=counter))
            elif letter == "*":
                if len(calling_stack) < 1:  # если в стеке меньше одной компоненты применить
                    # итерацию нельзя
                    raise Exception("Unexpected * symbol!")
                vertex = calling_stack.pop()
                self.tree.append(iteration(vertex=vertex,
                                           number=counter))
            elif letter == "+":
                if len(calling_stack) < 2:  # если в стеке меньше двух компонент применить
                    # объединение нельзя
                    raise Exception("Unexpected + symbol!")
                right_vertex = calling_stack.pop()
                left_vertex = calling_stack.pop()
                self.tree.append(union(first_vertex=left_vertex,
                                       second_vertex=right_vertex,
                                       number=counter))
            else:
                self.tree.append(Vertex(pos=counter,
                                        symbol=letter))
                vertex_symbol[counter] = letter
            calling_stack.append(self.tree[len(self.tree) - 1])

        if len(calling_stack) > 1:  # если в стеке оказалось больше одной компоненты,
            #  значит не хватает связывающих операций (+, .) и дерево несвязно
            raise Exception("Not enough operations, incoherent tree!")

    def calculate_follow_pos(self):
        self.follow_pos = {}   # словарь в котором каждой позиции соответсвующей букве в регулярке
        # сопоставляем множество всех символов которые могут идти сразу за ней
        for i in range(len(self.tree)):
            vertex = self.tree[i]
            if vertex.symbol != "." and vertex.symbol != "+" and vertex.symbol != "*":
                self.follow_pos[i] = set()  # для каждой буквенной позиции заводим множество

        for i in range(len(self.tree)):  # множества последователей могут измениться только при
            # операциях конкатенации и итерации
            if self.tree[i].symbol == ".":  # при конкатенации к последователям добавляются
                # все возможные начала правого слова
                for vertex in self.tree[i].left_child.last_pos:
                    self.follow_pos[vertex] |= self.tree[i].right_child.first_pos
            if self.tree[i].symbol == "*":  # при итерации добавляются все возможные начала текущей компоненты
                for vertex in self.tree[i].left_child.last_pos:
                    self.follow_pos[vertex] |= self.tree[i].left_child.first_pos

    def get_next_states(self, state_set)->{}:  # по множеству позиций выдает множество последователей
        transition = {}
        for state in state_set:
            letter = self.tree[state].symbol
            if letter not in transition.keys():
                transition[letter] = set()  # заводим новое множества под символ по которому еще не переходили
            transition[letter] |= self.follow_pos[state]
        return transition

    def create_machine(self):
        self.calculate_follow_pos()
        states_to_process = []  # стэк состояний которые нужно обработать
        states_rename = {}  # сопоставляет множествам позиций номер состояния
        edges = []
        # берем возможные первые символы слов языка
        start = frozenset(self.tree[len(self.tree) - 1].first_pos)
        states_to_process.append(start)
        states_rename[start] = 0
        finals = set()  # конечные состояния
        #alphabet = set()
        while states_to_process:
            state = states_to_process.pop()  # достаем очередное состояние в виде множества позиций
            for symbol, next_states in self.get_next_states(state).items():
                next_states = frozenset(next_states)
                if symbol == "#":
                    finals.add(states_rename[state])
                    continue
                #alphabet.add(symbol)
                if next_states not in states_rename.keys():  # если такой набор позиций не встречался ранее,
                    # заводим под него новое состояние
                    states_rename[next_states] = len(states_rename)
                    states_to_process.append(next_states)
                if symbol == '$':
                    for let in self.alphabet:
                        edges.append(Edge(prev=states_rename[state],
                                          next=states_rename[next_states],
                                          symbol=let))
                else:
                    edges.append(Edge(prev=states_rename[state],
                                      next=states_rename[next_states],
                                      symbol=symbol))
        # собираем автомат
        builder = MachineBuilder()
        builder.setStartState(0)
        builder.setFinalStates(list(finals))
        builder.setEdges(edges)
        builder.setAlphabet(list(self.alphabet))
        machine = builder.getMachine()
        machine.delete_eps()
        machine.create_DFSM()
        return machine


def create_machine_with_regex(regexp: str):
    regex_parse_tree = RegexParseTree(regexp=regexp)
    return regex_parse_tree.create_machine()
