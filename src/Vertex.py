import copy


class Vertex:
    def __init__(self, pos: int, symbol: str):
        self.first_pos = set()  # possible start positions
        self.last_pos = set()  # possible ending positions
        self.nullable = False  # if string can be empty
        self.symbol = symbol  # symbol of operation or letter
        self.first_pos.add(pos)
        self.last_pos.add(pos)
        self.left_child = None
        self.right_child = None


def concatenate(first_vertex: Vertex, second_vertex: Vertex, number: int) -> Vertex:
    new_vertex = Vertex(pos=number, symbol=".")
    new_vertex.nullable = first_vertex.nullable and second_vertex.nullable
    new_vertex.first_pos = copy.deepcopy(first_vertex.first_pos)  # add firsts of first vertex
    if first_vertex.nullable:
        new_vertex.first_pos |= second_vertex.first_pos  # add second firsts if first can be empty

    new_vertex.last_pos = copy.deepcopy(second_vertex.last_pos)
    if second_vertex.nullable:
        new_vertex.last_pos |= first_vertex.last_pos

    new_vertex.left_child, new_vertex.right_child = first_vertex, second_vertex
    return new_vertex


def union(first_vertex: Vertex, second_vertex: Vertex, number: int) -> Vertex:
    new_vertex = Vertex(pos=number, symbol="+")
    new_vertex.nullable = first_vertex.nullable or second_vertex.nullable
    new_vertex.first_pos = first_vertex.first_pos | second_vertex.first_pos
    new_vertex.last_pos = first_vertex.last_pos | second_vertex.last_pos
    new_vertex.left_child, new_vertex.right_child = first_vertex, second_vertex

    return new_vertex


def iteration(vertex: Vertex, number: int) -> Vertex:
    new_vertex = Vertex(pos=number, symbol="*")
    new_vertex.first_pos = copy.deepcopy(vertex.first_pos)
    new_vertex.last_pos = copy.deepcopy(vertex.last_pos)
    new_vertex.nullable = True

    new_vertex.left_child = vertex
    return new_vertex
