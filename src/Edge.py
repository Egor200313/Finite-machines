class Edge:
    def __init__(self, prev: int, next: int, symbol: str):
        self.prev = prev
        self.next = next
        self.symbol = symbol

    def __eq__(self, other):
        return self.prev == other.prev and self.next == other.next and self.symbol == other.symbol

    def __gt__(self, other):
        if self.prev > other.prev:
            return True
        if self.prev == other.prev:
            if self.next == other.next:
                return self.symbol > other.symbol
            return self.next > other.next
        return False
