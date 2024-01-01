import pytest
from unittest.mock import patch
from src.bot import set_bot_choose, choose_best_move, minimax


def test_easy_level_bot_empty_cell():
    with patch('random.choice', return_value=(2, 2)):
        state = [['.', '.', '.'],
                 ['.', '.', '.'],
                 ['.', '.', '.']]
        level_bot = 'easy'
        bot_side = 'O'

        set_bot_choose(state, level_bot, bot_side)

        assert state == [['.', '.', '.'],
                         ['.', '.', '.'],
                         ['.', '.', 'O']]


def test_easy_level_bot_no_empty_cell():
    state = [['X', 'O', 'X'],
             ['X', 'O', 'O'],
             ['O', 'X', 'X']]
    level_bot = 'easy'
    bot_side = 'O'

    with pytest.raises(IndexError):
        set_bot_choose(state, level_bot, bot_side)


def test_one_empty_cell():
    state = [['X', 'O', 'X'],
             ['O', 'X', 'O'],
             ['X', 'O', '.']]
    level_bot = 'hard'
    bot_side = 'O'

    set_bot_choose(state, level_bot, bot_side)

    assert state == [['X', 'O', 'X'],
                     ['O', 'X', 'O'],
                     ['X', 'O', 'O']]


def test_no_empty_cell():
    state = [['X', 'O', 'X'],
             ['O', 'X', 'O'],
             ['X', 'O', 'X']]
    level_bot = 'hard'
    bot_side = 'O'

    with pytest.raises(IndexError):
        set_bot_choose(state, level_bot, bot_side)


def test_best_move_for_bot_to_win():
    state = [['.', '.', '.'],
             ['.', '.', '.'],
             ['.', '.', '.']]
    bot_side = 'X'
    choose_best_move(state, bot_side)
    assert state == [['X', '.', '.'],
                     ['.', '.', '.'],
                     ['.', '.', '.']]


def test_best_move_to_block_opponent():
    state = [['X', '.', '.'],
             ['.', 'X', '.'],
             ['O', '.', '.']]
    bot_side = 'O'
    choose_best_move(state, bot_side)
    assert state == [['X', '.', '.'],
                     ['.', 'X', '.'],
                     ['O', '.', 'O']]


def test_no_empty_spaces_left():
    state = [['O', 'X', 'O'],
             ['X', 'O', 'X'],
             ['X', 'O', 'X']]
    bot_side = 'X'
    with pytest.raises(IndexError):
        choose_best_move(state, bot_side)


def test_only_available_move():
    state = [['O', 'X', 'O'],
             ['X', 'O', 'X'],
             ['X', 'O', '.']]
    bot_side = 'X'
    choose_best_move(state, bot_side)
    assert state == [['O', 'X', 'O'],
                     ['X', 'O', 'X'],
                     ['X', 'O', 'X']]


def test_correct_score():
    state = [['X', 'O', 'X'],
             ['O', 'X', 'O'],
             ['.', '.', '.']]
    bot_side = 'O'
    score = minimax(state, bot_side, True)
    assert score == -1


def test_correct_score2():
    state = [['X', 'O', 'X'],
             ['O', 'X', 'O'],
             ['.', '.', '.']]
    bot_side = 'X'
    score = minimax(state, bot_side, True)
    assert score == 1


def test_correct_score_empty_state():
    state = [['.', '.', '.'],
             ['.', '.', '.'],
             ['.', '.', '.']]
    bot_side = 'X'
    score = minimax(state, bot_side, True)
    assert score == 0
