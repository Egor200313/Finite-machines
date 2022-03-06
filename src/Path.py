from src.Edge import Edge


class Path:
    def __init__(self, first_edge: Edge, second_edge: Edge):
        self.start_state = first_edge.prev
        self.final_state = second_edge.next
        self.first_word = first_edge.symbol
        self.second_word = second_edge.symbol
        self.word = "(" + first_edge.symbol + ")(" + second_edge.symbol + ")"


def only_empty(path):
    return path.first_word == "empty" and path.second_word == "empty"


def symbol_empty(path):
    return path.first_word != "empty" and path.second_word == "empty"
