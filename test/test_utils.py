from src.utils import won, is_draw


def test_row_win():
    state = [['X', 'X', 'X'], ['.', '.', '.'], ['.', '.', '.']]
    assert won(state)


def test_column_win():
    state = [['X', '.', '.'], ['X', '.', '.'], ['X', '.', '.']]
    assert won(state)


def test_diagonal_win():
    state = [['X', '.', '.'], ['.', 'X', '.'], ['.', '.', 'X']]
    assert won(state)


def test_no_win():
    state = [['X', '.', '.'], ['.', '.', '.'], ['.', '.', '.']]
    assert not won(state)


def test_draw():
    state = [['X', 'O', 'X'], ['X', 'O', 'O'], ['O', 'X', 'X']]
    assert is_draw(state)


def test_no_draw():
    state = [['X', '.', '.'], ['.', '.', '.'], ['.', '.', '.']]
    assert not is_draw(state)
