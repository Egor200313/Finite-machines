class MachineVisitor:
    def __init__(self):
        self.used = []

    def dfs(self, state_machine, vertex: int):  # обходим автомат для выделения связности
        self.used[vertex] = 1
        for edge in [edge for edge in state_machine.edges
                     if edge.prev == vertex and self.used[edge.next] == 0]:
            self.dfs(state_machine, edge.next)

    def get_unreachable_states(self, state_machine):
        self.used = [0 for i in range(len(state_machine.states) + 1)]
        self.dfs(state_machine, state_machine.start_state)
        unreachable_states = set()
        for i in range(len(self.used)):
            if self.used[i] == 0:
                unreachable_states.add(i)
        return unreachable_states
