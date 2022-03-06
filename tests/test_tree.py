from src.Tree import create_machine_with_regex, RegexParseTree
from src.Vertex import Vertex, union, concatenate, iteration


#       Concatenation tests

left_vertex = Vertex(1, "a")
right_vertex = Vertex(2, "b")
result = concatenate(left_vertex, right_vertex, 3)


def test_symbols_concatenation():
    global result
    assert result.symbol == "."
    assert result.nullable is False
    assert len(result.first_pos) == 1
    assert 1 in result.first_pos

    assert len(result.last_pos) == 1
    assert 2 in result.last_pos
# result = ab (12)


def test_symbol_concat_concatenation():
    global left_vertex
    left_vertex = Vertex(4, "c")
    global result
    result = concatenate(left_vertex, result, 5)

    assert result.nullable is False
    assert len(result.first_pos) == 1
    assert 4 in result.first_pos

    assert len(result.last_pos) == 1
    assert 2 in result.last_pos
# result = cab (412)


right_vertex = Vertex(6, "d")
result_of_iteration = iteration(right_vertex, 7)


def test_iteration():
    global result_of_iteration
    assert result_of_iteration.symbol == "*"
    assert result_of_iteration.nullable is True

    assert len(result_of_iteration.first_pos) == 1
    assert 6 in result_of_iteration.first_pos

    assert len(result_of_iteration.last_pos) == 1
    assert 6 in result_of_iteration.last_pos
# result_of_iteration = d* (6)


def test_concat_symbol_iteration():
    global result_of_iteration
    global result
    result = concatenate(result, result_of_iteration, 8)

    assert result.nullable is False
    assert len(result.first_pos) == 1
    assert 4 in result.first_pos

    assert len(result.last_pos) == 2
    assert 2 in result.last_pos
    assert 6 in result.last_pos
# result = cabd* (4126)


#       Union tests
left_vertex = Vertex(1, "a")
right_vertex = Vertex(2, "b")
union_result = union(left_vertex, right_vertex, 3)


def test_symbols_union():
    global union_result
    assert union_result.symbol == "+"
    assert union_result.nullable is False
    assert len(union_result.first_pos) == 2
    assert 1 in union_result.first_pos
    assert 2 in union_result.first_pos

    assert len(union_result.last_pos) == 2
    assert 1 in union_result.last_pos
    assert 2 in union_result.last_pos

# result = a+b (1+2)


def test_symbol_concat_union():
    global left_vertex
    left_vertex = Vertex(4, "c")
    global union_result
    union_result = union(left_vertex, union_result, 5)

    assert union_result.nullable is False
    assert len(union_result.first_pos) == 3
    assert 4 in union_result.first_pos
    assert 1 in union_result.first_pos
    assert 2 in union_result.first_pos

    assert len(union_result.last_pos) == 3
    assert 4 in union_result.last_pos
    assert 1 in union_result.last_pos
    assert 2 in union_result.last_pos

# result = c+a+b (4+1+2)


right_vertex = Vertex(6, "d")
# result_of_iteration = d* (6)


def test_unite_symbol_iteration():
    global result_of_iteration
    global union_result
    union_result = union(union_result, result_of_iteration, 8)

    assert union_result.nullable is True
    assert len(union_result.first_pos) == 4
    assert 4 in union_result.first_pos
    assert 1 in union_result.first_pos
    assert 2 in union_result.first_pos
    assert 6 in union_result.first_pos

    assert len(union_result.last_pos) == 4
    assert 4 in union_result.last_pos
    assert 1 in union_result.last_pos
    assert 2 in union_result.last_pos
    assert 6 in union_result.last_pos
# result = c+a+b+d* (4126)


regex_parse_tree = RegexParseTree("ab+c*.")  # (a+b)c*


def test_max_prefix_inf():
    reg = "ab.c.d."
    word = "ab"
    machine = create_machine_with_regex(reg)
    assert machine.max_prefix(word) == "INF"


def test_max_prefix_whole_word():
    reg = "ab+c.*"  # ((a+b)c)*
    word = ""
    machine = create_machine_with_regex(reg)
    assert machine.max_prefix(word) == 0

    word = "acbc"
    assert machine.max_prefix(word) == 4

    word = "acacac"
    assert machine.max_prefix(word) == 6


def test_max_prefix_with_empty():
    reg = "a*1+c."  # (a*+1)c = a*c + c
    machine = create_machine_with_regex(reg)

    word = "ca"
    assert machine.max_prefix(word) == 1

    word = "aaaaaaaaaaaaaaaac"
    assert machine.max_prefix(word) == 17


def test_max_prefix_common():
    reg = "ab+c.aba.*.bac.+.+*"
    machine = create_machine_with_regex(reg)
    word = "abacb"

    assert machine.max_prefix(word) == 4

    reg = "acb..bab.c.*.ab.ba.+.+*a."
    machine = create_machine_with_regex(reg)
    word = "acbac"

    assert machine.max_prefix(word) == 4


def test_exception():
    reg = "ab++"
    try:
        machine = create_machine_with_regex(reg)
    except Exception as e:
        assert str(e) == "Unexpected + symbol!"

    reg = "ab+."
    try:
        machine = create_machine_with_regex(reg)
    except Exception as e:
        assert str(e) == "Unexpected . symbol!"

    reg = "ab+a"
    try:
        machine = create_machine_with_regex(reg)
    except Exception as e:
        assert str(e) == "Not enough operations, incoherent tree!"

    reg = "*ab+"
    try:
        machine = create_machine_with_regex(reg)
    except Exception as e:
        assert str(e) == "Unexpected * symbol!"
