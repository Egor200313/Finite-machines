from src.Edge import Edge
from src.MachineBuilder import MachineBuilder
import copy


def test_delete_eps():
    edges = [
        Edge(prev=1, next=2, symbol="a"),
        Edge(prev=2, next=3, symbol="empty"),
        Edge(prev=1, next=4, symbol="empty"),
        Edge(prev=1, next=5, symbol="empty"),
        Edge(prev=5, next=6, symbol="empty"),
        Edge(prev=4, next=5, symbol="a"),
        Edge(prev=4, next=3, symbol="c"),
        Edge(prev=6, next=3, symbol="b")
    ]
    edges_check = [
        Edge(prev=1, next=2, symbol="a"),
        Edge(prev=1, next=3, symbol="a")
    ]

    builder = MachineBuilder()
    builder.setStartState(1)
    builder.setFinalStates([3, 6])
    builder.setEdges(edges)
    builder.setAlphabet(["a", "b", "c", "empty"])
    machine = builder.getMachine()

    builder.reset()

    builder.setStartState(1)
    builder.setFinalStates([1, 2, 3])
    builder.setEdges(edges_check)
    builder.setAlphabet(["a", "b", "c"])
    check_machine = builder.getMachine()

    machine.delete_eps()

    assert machine == check_machine
    print("Delete empty test passed!")


def test_create_dfsm():
    edges = [
        Edge(prev=1, next=2, symbol="a"),
        Edge(prev=2, next=1, symbol="b"),
        Edge(prev=1, next=3, symbol="b"),
        Edge(prev=3, next=1, symbol="a"),
        Edge(prev=1, next=4, symbol="a"),
        Edge(prev=3, next=4, symbol="a")
    ]
    edges_check = [
        Edge(prev=0, next=1, symbol="a"),
        Edge(prev=0, next=2, symbol="b"),
        Edge(prev=1, next=0, symbol="b"),
        Edge(prev=2, next=3, symbol="a"),
        Edge(prev=3, next=1, symbol="a"),
        Edge(prev=3, next=2, symbol="b")
    ]

    builder = MachineBuilder()
    builder.setStartState(1)
    builder.setFinalStates([1, 4])
    builder.setEdges(edges)
    builder.setAlphabet(["a", "b"])
    machine = builder.getMachine()

    builder.reset()

    builder.setStartState(0)
    builder.setFinalStates([0, 1, 3])
    builder.setEdges(edges_check)
    builder.setAlphabet(["a", "b"])

    check_machine = builder.getMachine()

    machine.create_DFSM()

    assert machine == check_machine
    print("DFSM test passed!")


def test_complete_dfsm():
    edges = [
        Edge(prev=0, next=1, symbol="a"),
        Edge(prev=0, next=2, symbol="b"),
        Edge(prev=1, next=0, symbol="b"),
        Edge(prev=2, next=3, symbol="a"),
        Edge(prev=3, next=1, symbol="a"),
        Edge(prev=3, next=2, symbol="b")
    ]
    edges_check = [
        Edge(prev=0, next=1, symbol="a"),
        Edge(prev=0, next=2, symbol="b"),
        Edge(prev=1, next=0, symbol="b"),
        Edge(prev=2, next=3, symbol="a"),
        Edge(prev=3, next=1, symbol="a"),
        Edge(prev=3, next=2, symbol="b"),
        Edge(prev=1, next=4, symbol="a"),
        Edge(prev=2, next=4, symbol="b"),
        Edge(prev=4, next=4, symbol="a"),
        Edge(prev=4, next=4, symbol="b")
    ]

    builder = MachineBuilder()

    builder.setStartState(0)
    builder.setFinalStates([1, 0, 3])
    builder.setEdges(edges)
    builder.setAlphabet(["a", "b"])
    machine = builder.getMachine()

    builder.reset()

    builder.setStartState(0)
    builder.setFinalStates([1, 0, 3])
    builder.setEdges(edges_check)
    builder.setAlphabet(["a", "b"])
    check_machine = builder.getMachine()

    machine.complete_DFSM()

    assert machine == check_machine
    print("Complete DFSM test passed!")


def test_addition():
    edges = [
        Edge(prev=0, next=1, symbol="a"),
        Edge(prev=0, next=2, symbol="b"),
        Edge(prev=1, next=0, symbol="b"),
        Edge(prev=2, next=3, symbol="a"),
        Edge(prev=3, next=1, symbol="a"),
        Edge(prev=3, next=2, symbol="b"),
        Edge(prev=1, next=4, symbol="a"),
        Edge(prev=2, next=4, symbol="b")
    ]

    builder = MachineBuilder()

    builder.setStartState(0)
    builder.setFinalStates([1, 0, 3])
    builder.setEdges(edges)
    builder.setAlphabet(["a", "b"])
    machine = builder.getMachine()

    machine_check = copy.deepcopy(machine)
    machine_check.final_states = [2, 4]

    machine.create_addition()

    assert machine == machine_check
    print("Addition test passed!")


def test_with_reverse():
    edges = [
        Edge(prev=1, next=1, symbol="a"),
        Edge(prev=1, next=2, symbol="b"),
        Edge(prev=2, next=2, symbol="a"),
        Edge(prev=2, next=3, symbol="b"),
        Edge(prev=3, next=1, symbol="a")
    ]

    builder = MachineBuilder()

    builder.setStartState(1)
    builder.setFinalStates([3])
    builder.setEdges(edges)
    builder.setAlphabet(["a", "b"])
    machine = builder.getMachine()

    regex = machine.get_regex()

    assert regex == "(a)*b(a)*b(a(a)*b(a)*b)*"
    print("Reverse Regex test passed!")


def test_minimize():
    edges = [
        Edge(prev=0, next=1, symbol="a"),
        Edge(prev=0, next=3, symbol="b"),
        Edge(prev=1, next=2, symbol="a"),
        Edge(prev=1, next=4, symbol="b"),
        Edge(prev=2, next=0, symbol="a"),
        Edge(prev=2, next=5, symbol="b"),
        Edge(prev=3, next=4, symbol="a"),
        Edge(prev=3, next=6, symbol="b"),
        Edge(prev=4, next=5, symbol="a"),
        Edge(prev=4, next=7, symbol="b"),
        Edge(prev=5, next=3, symbol="a"),
        Edge(prev=5, next=8, symbol="b"),
        Edge(prev=6, next=7, symbol="a"),
        Edge(prev=6, next=0, symbol="b"),
        Edge(prev=7, next=8, symbol="a"),
        Edge(prev=7, next=1, symbol="b"),
        Edge(prev=8, next=6, symbol="a"),
        Edge(prev=8, next=2, symbol="b")
    ]

    builder = MachineBuilder()

    builder.setStartState(0)
    builder.setFinalStates([4, 0, 8])
    builder.setEdges(edges)
    builder.setAlphabet(["a", "b"])
    machine = builder.getMachine()

    builder.reset()

    edges_check = [
        Edge(prev=0, next=1, symbol="a"),
        Edge(prev=0, next=2, symbol="b"),
        Edge(prev=1, next=2, symbol="a"),
        Edge(prev=1, next=0, symbol="b"),
        Edge(prev=2, next=0, symbol="a"),
        Edge(prev=2, next=1, symbol="b")
    ]

    builder.setStartState(0)
    builder.setFinalStates([0])
    builder.setEdges(edges_check)
    builder.setAlphabet(["a", "b"])
    machine_check = builder.getMachine()

    machine.minimize()

    assert machine == machine_check
    print("Minimize test passed!")
