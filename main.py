"""
Bot for playing tic tac toe game with multiple CallbackQueryHandlers.
"""
import random
from copy import deepcopy
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)
import os

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger('httpx').setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# get token using BotFather
TOKEN = os.getenv('TG_TOKEN')

CHOOSE_SIDE, CHOOSE_LEVEL, CONTINUE_GAME, FINISH_GAME = range(4)

FREE_SPACE = '.'
CROSS = 'X'
ZERO = 'O'

DEFAULT_STATE = [[FREE_SPACE for _ in range(3)] for _ in range(3)]


def get_default_state():
    """Helper function to get default state of the game"""
    return deepcopy(DEFAULT_STATE)


def generate_keyboard(state: list[list[str]]) -> list[list[InlineKeyboardButton]]:
    """Generate tic tac toe keyboard 3x3 (telegram buttons)"""
    return [
        [
            InlineKeyboardButton(state[r][c], callback_data=f'{r}{c}')
            for r in range(3)
        ]
        for c in range(3)
    ]


def set_bot_choose(state: list[list[str]], level_bot: str, bot_side: str = ZERO) -> None:
    if level_bot == 'easy':
        available_picks = [(i, j) for i in range(3) for j in range(3) if state[i][j] == '.']
        pick = random.choice(available_picks)
        state[pick[0]][pick[1]] = bot_side
    else:
        choose_best_move(state, bot_side)


def choose_best_move(state: list[list[str]], bot_side: str) -> None:
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


def is_draw(state: list[list[str]]) -> bool:
    return all(state[i][j] != '.' for i in range(3) for j in range(3))


async def choose_side(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Let the player choose their side (X or O)."""
    keyboard = [
        [InlineKeyboardButton(CROSS, callback_data=CROSS)],
        [InlineKeyboardButton(ZERO, callback_data=ZERO)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text('Choose your side:', reply_markup=reply_markup)
    return CHOOSE_SIDE


async def choose_level(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Let the player choose the bot's level."""
    keyboard = [
        [InlineKeyboardButton('Easy', callback_data='easy')],
        [InlineKeyboardButton('Hard', callback_data='hard')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Choose the bot\'s level:', reply_markup=reply_markup)
    return CHOOSE_LEVEL


async def choose_level_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Callback function for handling level selection."""
    user_data = context.user_data
    user_data['bot_level'] = update.callback_query.data
    return await choose_side(update, context)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send message on `/start`."""
    context.user_data['keyboard_state'] = get_default_state()
    return await choose_level(update, context)


async def choose_side_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Callback function for handling side selection."""
    user_data = context.user_data
    user_data['player_side'] = update.callback_query.data
    side = user_data['player_side']
    lvl = user_data['bot_level']

    if side == ZERO:
        set_bot_choose(user_data['keyboard_state'], lvl, CROSS)

    logger.info(f'Bot\'s side: {side}. '
                f'Bot\'s level: {lvl}. '
                f'Initial state: {user_data['keyboard_state']}')

    keyboard = generate_keyboard(user_data['keyboard_state'])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(f'Bot\'s level: {user_data["bot_level"]}. '
                                                  f'You chose {side}. '
                                                  f'{side} (your) turn! Please, put {side} to the free place',
                                                  reply_markup=reply_markup)
    return CONTINUE_GAME


async def game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Main processing of the game"""
    player_side = context.user_data['player_side']
    bot_side = CROSS if player_side == ZERO else ZERO
    lvl = context.user_data['bot_level']
    user_pick = map(int, update.callback_query.data)
    state = context.user_data['keyboard_state']
    state[next(user_pick)][next(user_pick)] = player_side

    logger.info(f'State after player\'s move: {state}')

    if won(state):
        logger.info(f'Player won')
        keyboard = generate_keyboard(state)
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.edit_message_text(
            f'{player_side} (your) won!', reply_markup=reply_markup
        )
        return FINISH_GAME

    try:
        set_bot_choose(state, lvl, bot_side)
    except IndexError:
        logger.info(f'Not enough space for bot\'s move. Draw')
        keyboard = generate_keyboard(state)
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.edit_message_text(
            f'Draw!', reply_markup=reply_markup
        )
        return FINISH_GAME

    logger.info(f'State after bot\'s move: {state}')

    keyboard = generate_keyboard(state)
    reply_markup = InlineKeyboardMarkup(keyboard)

    if is_draw(state):
        logger.info(f'Draw after bot\'s move')
        await update.callback_query.edit_message_text(
            f'Draw!', reply_markup=reply_markup
        )
        return FINISH_GAME

    if won(state):
        logger.info(f'Bot won')
        await update.callback_query.edit_message_text(
            f'{bot_side} (bot) won!', reply_markup=reply_markup
        )
        return FINISH_GAME

    # if nobody won continue the game
    await update.callback_query.edit_message_text(
        f'{player_side} (your) turn! '
        f'Please, put {player_side} to the free place', reply_markup=reply_markup
    )
    return CONTINUE_GAME


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


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    # reset state to default so you can play again with /start
    context.user_data['keyboard_state'] = get_default_state()
    return ConversationHandler.END


def main() -> None:
    """Run the bot"""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Setup conversation handler with the states CONTINUE_GAME and FINISH_GAME
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSE_LEVEL: [CallbackQueryHandler(choose_level_callback, pattern='^(easy|hard)$')],
            CHOOSE_SIDE: [CallbackQueryHandler(choose_side_callback, pattern='^(X|O)$')],
            CONTINUE_GAME: [
                CallbackQueryHandler(game, pattern='^' + f'{r}{c}' + '$')
                for r in range(3)
                for c in range(3)
            ],
            FINISH_GAME: [
                CallbackQueryHandler(end, pattern='^' + f'{r}{c}' + '$')
                for r in range(3)
                for c in range(3)
            ],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    # Add ConversationHandler to application that will be used for handling updates
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
