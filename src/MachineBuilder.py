from src.Edge import Edge
from src.StateMachine import StateMachine
import copy


class MachineBuilder:
    def __init__(self):
        self.machine = StateMachine()

    def reset(self):
        self.machine = StateMachine()

    def setEdges(self, edges: [Edge]):
        self.machine.edges = edges
        self.machine.set_states()

    def setAlphabet(self, alphabet: [str]):
        self.machine.alphabet = alphabet

    def setStartState(self, start_state: int):
        self.machine.start_state = start_state

    def setFinalStates(self, final_states: [int]):
        self.machine.final_states = final_states

    def getMachine(self):
        return copy.deepcopy(self.machine)
