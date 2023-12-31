def won(state: list[list[str]]) -> bool:
    """Check if crosses or zeros have won the game"""
    rows = [set(state[i][j] for i in range(3)) for j in range(3)]
    cols = [set(state[i][j] for j in range(3)) for i in range(3)]
    diags = [
        set(state[i][i] for i in range(3)),
        set(state[i][2 - i] for i in range(3))
    ]
    for row in rows:
        if len(row) == 1 and '.' not in row:
            return True
    for col in cols:
        if len(col) == 1 and '.' not in col:
            return True
    for diag in diags:
        if len(diag) == 1 and '.' not in diag:
            return True
    return False


def is_draw(state: list[list[str]]) -> bool:
    return all(state[i][j] != '.' for i in range(3) for j in range(3))
