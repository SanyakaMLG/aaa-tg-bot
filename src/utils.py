def won(state: list[list[str]]) -> bool:
    """Check if crosses or zeros have won the game"""
    for i in range(3):
        if state[i][0] == state[i][1] == state[i][2] != '.':
            return True
        if state[0][i] == state[1][i] == state[2][i] != '.':
            return True
    if state[0][0] == state[1][1] == state[2][2] != '.':
        return True
    if state[0][2] == state[1][1] == state[2][0] != '.':
        return True
    return False


def is_draw(state: list[list[str]]) -> bool:
    """Check if the game is a draw"""
    return all(state[i][j] != '.' for i in range(3) for j in range(3))
