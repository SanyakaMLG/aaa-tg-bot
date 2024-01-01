import random

from utils import won, is_draw

CROSS = 'X'
ZERO = 'O'


def set_bot_choose(state: list[list[str]], level_bot: str, bot_side: str = ZERO) -> None:
    """Set bot's choice on the field"""
    if level_bot == 'easy':
        available_picks = [(i, j) for i in range(3) for j in range(3) if state[i][j] == '.']
        pick = random.choice(available_picks)
        state[pick[0]][pick[1]] = bot_side
    else:
        choose_best_move(state, bot_side)


def choose_best_move(state: list[list[str]], bot_side: str) -> None:
    """Choose the best move for the bot"""
    best_score = float('-inf')
    best_move = None

    for i in range(3):
        for j in range(3):
            if state[i][j] == '.':
                state[i][j] = bot_side
                score = minimax(state, bot_side, False)
                state[i][j] = '.'  # undo the move

                if score > best_score:
                    best_score = score
                    best_move = (i, j)

    if best_move is None:
        raise IndexError('No empty space left')

    state[best_move[0]][best_move[1]] = bot_side


def minimax(state: list[list[str]], bot_side: str, maximizing_player: bool) -> int:
    """Minimax algorithm implementation"""
    if won(state):
        return -1 if maximizing_player else 1

    if is_draw(state):
        return 0

    player_side = CROSS if bot_side == ZERO else ZERO

    if maximizing_player:
        max_eval = float('-inf')
        for i in range(3):
            for j in range(3):
                if state[i][j] == '.':
                    state[i][j] = bot_side
                    cur_eval = minimax(state, bot_side, False)
                    state[i][j] = '.'  # undo the move
                    max_eval = max(max_eval, cur_eval)
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(3):
            for j in range(3):
                if state[i][j] == '.':
                    state[i][j] = player_side
                    cur_eval = minimax(state, bot_side, True)
                    state[i][j] = '.'  # undo the move
                    min_eval = min(min_eval, cur_eval)
        return min_eval
