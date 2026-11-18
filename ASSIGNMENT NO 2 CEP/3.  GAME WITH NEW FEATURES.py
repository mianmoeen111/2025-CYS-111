
import sys
import math
import random
from array import array

import pygame

# =========================================================
# 1. INITIALIZATION
# =========================================================

pygame.init()

try:
    pygame.mixer.init()
    SOUND_ENABLED = True
except pygame.error:
    SOUND_ENABLED = False

WIDTH, HEIGHT = 750, 850
screen = pygame.display.set_mode(
    (WIDTH, HEIGHT),
    pygame.RESIZABLE
)
pygame.display.set_caption("Tic Tac Toe - AI Edition")

clock = pygame.time.Clock()

# Board settings
BOARD_SIZE = 3
EMPTY = "_"
PLAYER_X = "X"
PLAYER_O = "O"

# Colors
WHITE = (248, 250, 255)
BLACK = (25, 32, 45)
BLUE = (40, 110, 220)
RED = (235, 75, 75)
GREEN = (35, 165, 105)
GRAY = (215, 222, 232)
DARK_GRAY = (95, 105, 120)
LIGHT_BLUE = (225, 237, 255)
YELLOW = (255, 205, 80)
PURPLE = (135, 90, 200)

# Fonts
title_font = pygame.font.SysFont("Arial", 48, bold=True)
heading_font = pygame.font.SysFont("Arial", 30, bold=True)
font = pygame.font.SysFont("Arial", 23)
small_font = pygame.font.SysFont("Arial", 18)

# Game settings
AI_DELAY = 450
ANIMATION_DURATION = 180

# =========================================================
# 2. SOUND EFFECTS
# =========================================================

def create_sound(frequency=440, duration=0.12, volume=0.25):
    """Create a simple sound without requiring external files."""
    if not SOUND_ENABLED:
        return None

    sample_rate = 22050
    samples = array("h")

    for i in range(int(sample_rate * duration)):
        t = i / sample_rate
        fade = min(1, i / 300, (sample_rate * duration - i) / 500)
        value = int(
            32767 * volume * fade *
            math.sin(2 * math.pi * frequency * t)
        )
        samples.append(value)

    try:
        return pygame.mixer.Sound(buffer=samples.tobytes())
    except pygame.error:
        return None


SOUNDS = {
    "move": create_sound(520),
    "win": create_sound(780, 0.35),
    "lose": create_sound(220, 0.35),
    "draw": create_sound(400, 0.25),
    "click": create_sound(650, 0.08),
}


def play_sound(name):
    if sound_on and SOUNDS.get(name):
        SOUNDS[name].play()


# =========================================================
# 3. GAME VARIABLES
# =========================================================

board = [
    [EMPTY for _ in range(BOARD_SIZE)]
    for _ in range(BOARD_SIZE)
]

game_state = "menu"  # menu or game

difficulty = "Beginner"
human_symbol = PLAYER_X
ai_symbol = PLAYER_O
starter = "Human"

current_player = human_symbol
winner = None
game_over = False

ai_waiting = False
ai_move_time = 0

sound_on = True

# Scores are maintained across rounds
scores = {
    "wins": 0,
    "losses": 0,
    "draws": 0
}

# Animation start times for board symbols
animation_times = {}


# =========================================================
# 4. GAME LOGIC
# =========================================================

def reset_board():
    global board, current_player, winner, game_over
    global ai_waiting, animation_times

    board = [
        [EMPTY for _ in range(BOARD_SIZE)]
        for _ in range(BOARD_SIZE)
    ]

    winner = None
    game_over = False
    ai_waiting = False
    animation_times = {}

    if starter == "Human":
        current_player = human_symbol
    elif starter == "AI":
        current_player = ai_symbol
    else:
        current_player = random.choice(
            [human_symbol, ai_symbol]
        )

    if current_player == ai_symbol:
        schedule_ai_move()


def start_game():
    global game_state, ai_symbol

    ai_symbol = PLAYER_O if human_symbol == PLAYER_X else PLAYER_X

    game_state = "game"
    reset_board()


def get_winner(b):
    """Return X or O if a player has won; otherwise None."""

    for row in range(BOARD_SIZE):
        if (
            b[row][0] == b[row][1] == b[row][2]
            and b[row][0] != EMPTY
        ):
            return b[row][0]

    for col in range(BOARD_SIZE):
        if (
            b[0][col] == b[1][col] == b[2][col]
            and b[0][col] != EMPTY
        ):
            return b[0][col]

    if b[0][0] == b[1][1] == b[2][2] != EMPTY:
        return b[0][0]

    if b[0][2] == b[1][1] == b[2][0] != EMPTY:
        return b[0][2]

    return None


def is_board_full(b):
    return all(
        b[row][col] != EMPTY
        for row in range(BOARD_SIZE)
        for col in range(BOARD_SIZE)
    )


def check_game_status():
    global winner, game_over

    winner = get_winner(board)

    if winner is not None:
        game_over = True

        if winner == human_symbol:
            scores["wins"] += 1
            play_sound("win")
        else:
            scores["losses"] += 1
            play_sound("lose")

        return

    if is_board_full(board):
        game_over = True
        scores["draws"] += 1
        play_sound("draw")


def available_moves(b):
    moves = []

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if b[row][col] == EMPTY:
                moves.append((row, col))

    return moves


# =========================================================
# 5. MINIMAX ALGORITHM
# =========================================================

def minimax(b, depth, is_maximizing):
    """
    AI maximizes the score.
    Human minimizes the score.

    Positive score = good for AI.
    Negative score = good for human.
    """

    result = get_winner(b)

    if result == ai_symbol:
        return 10 - depth

    if result == human_symbol:
        return depth - 10

    if is_board_full(b):
        return 0

    if is_maximizing:
        best_score = -math.inf

        for row, col in available_moves(b):
            b[row][col] = ai_symbol

            score = minimax(b, depth + 1, False)

            b[row][col] = EMPTY
            best_score = max(best_score, score)

        return best_score

    else:
        best_score = math.inf

        for row, col in available_moves(b):
            b[row][col] = human_symbol

            score = minimax(b, depth + 1, True)

            b[row][col] = EMPTY
            best_score = min(best_score, score)

        return best_score


def get_best_ai_move():
    """Find the best move using Minimax."""

    best_score = -math.inf
    best_move = None

    for row, col in available_moves(board):
        board[row][col] = ai_symbol

        score = minimax(board, 0, False)

        board[row][col] = EMPTY

        if score > best_score:
            best_score = score
            best_move = (row, col)

    return best_move


# =========================================================
# 6. AI DIFFICULTY LEVELS
# =========================================================

def choose_ai_move():
    moves = available_moves(board)

    if not moves:
        return None

    # BEGINNER: Completely random legal move
    if difficulty == "Beginner":
        return random.choice(moves)

    # MEDIUM: Sometimes random, sometimes strategic
    if difficulty == "Medium":
        if random.random() < 0.35:
            return random.choice(moves)

        return get_best_ai_move()

    # HARD: Always uses Minimax
    return get_best_ai_move()


def schedule_ai_move():
    global ai_waiting, ai_move_time

    ai_waiting = True
    ai_move_time = pygame.time.get_ticks()


def make_ai_move():
    global current_player, ai_waiting

    ai_waiting = False

    if game_over:
        return

    move = choose_ai_move()

    if move is None:
        return

    row, col = move

    board[row][col] = ai_symbol
    animation_times[(row, col)] = pygame.time.get_ticks()

    play_sound("move")
    check_game_status()

    if not game_over:
        current_player = human_symbol


# =========================================================
# 7. DRAWING HELPERS
# =========================================================

def draw_text(text, selected_font, color, center):
    surface = selected_font.render(text, True, color)
    rect = surface.get_rect(center=center)
    screen.blit(surface, rect)
    return rect


def draw_button(text, rect, selected=False, color=BLUE):
    button_color = color if selected else LIGHT_BLUE
    text_color = WHITE if selected else BLACK

    pygame.draw.rect(
        screen,
        button_color,
        rect,
        border_radius=12
    )

    pygame.draw.rect(
        screen,
        BLUE if selected else GRAY,
        rect,
        2,
        border_radius=12
    )

    label = font.render(text, True, text_color)
    screen.blit(label, label.get_rect(center=rect.center))


def get_layout():
    """Calculate board dimensions based on current window size."""

    width, height = screen.get_size()

    board_size = min(width - 50, height - 300)
    board_size = max(180, min(board_size, 480))

    cell_size = board_size / 3

    board_x = (width - board_size) // 2
    board_y = max(160, (height - board_size) // 2 - 20)

    return board_x, board_y, board_size, cell_size


# =========================================================
# 8. DRAW ANIMATED BOARD
# =========================================================

def draw_symbol(symbol, rect, row, col):
    now = pygame.time.get_ticks()

    start_time = animation_times.get((row, col), now)
    progress = min(
        1,
        (now - start_time) / ANIMATION_DURATION
    )

    progress = max(0.08, progress)

    center = rect.center
    padding = int(rect.width * 0.20 * progress)
    line_width = max(2, int(rect.width * 0.07 * progress))

    if symbol == PLAYER_X:
        pygame.draw.line(
            screen,
            RED,
            (rect.left + padding, rect.top + padding),
            (rect.right - padding, rect.bottom - padding),
            line_width
        )

        pygame.draw.line(
            screen,
            RED,
            (rect.right - padding, rect.top + padding),
            (rect.left + padding, rect.bottom - padding),
            line_width
        )

    elif symbol == PLAYER_O:
        radius = int(rect.width * 0.30 * progress)

        pygame.draw.circle(
            screen,
            BLUE,
            center,
            max(2, radius),
            line_width
        )


def draw_board():
    screen.fill(WHITE)

    width, height = screen.get_size()

    draw_text(
        "TIC TAC TOE",
        title_font,
        BLACK,
        (width // 2, 45)
    )

    draw_text(
        f"Difficulty: {difficulty}",
        small_font,
        PURPLE,
        (width // 2, 88)
    )

    # Scoreboard
    score_text = (
        f"Wins: {scores['wins']}     "
        f"Losses: {scores['losses']}     "
        f"Draws: {scores['draws']}"
    )

    draw_text(
        score_text,
        small_font,
        BLACK,
        (width // 2, 120)
    )

    # Current turn / result
    if game_over:
        if winner == human_symbol:
            message = "You Win!"
            color = GREEN
        elif winner == ai_symbol:
            message = "AI Wins!"
            color = RED
        else:
            message = "It's a Draw!"
            color = BLACK

    elif current_player == human_symbol:
        message = f"Your Turn ({human_symbol})"
        color = GREEN

    else:
        message = f"AI Thinking ({ai_symbol})..."
        color = BLUE

    draw_text(
        message,
        heading_font,
        color,
        (width // 2, 155)
    )

    # Board
    board_x, board_y, board_size, cell_size = get_layout()

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):

            rect = pygame.Rect(
                int(board_x + col * cell_size),
                int(board_y + row * cell_size),
                int(cell_size),
                int(cell_size)
            )

            pygame.draw.rect(
                screen,
                LIGHT_BLUE,
                rect,
                border_radius=5
            )

            pygame.draw.rect(
                screen,
                BLACK,
                rect,
                3
            )

            if board[row][col] != EMPTY:
                draw_symbol(
                    board[row][col],
                    rect,
                    row,
                    col
                )

    # Bottom buttons
    button_y = min(
        height - 75,
        board_y + board_size + 35
    )

    restart_rect = pygame.Rect(
        width // 2 - 165,
        button_y,
        150,
        48
    )

    menu_rect = pygame.Rect(
        width // 2 + 15,
        button_y,
        150,
        48
    )

    draw_button("Play Again", restart_rect, color=GREEN)
    draw_button("Main Menu", menu_rect, color=PURPLE)

    return restart_rect, menu_rect


# =========================================================
# 9. START MENU
# =========================================================

def draw_menu():
    screen.fill(WHITE)

    width, height = screen.get_size()

    draw_text(
        "TIC TAC TOE AI",
        title_font,
        BLACK,
        (width // 2, 75)
    )

    draw_text(
        "Play against Artificial Intelligence",
        font,
        DARK_GRAY,
        (width // 2, 125)
    )

    # Difficulty options
    draw_text(
        "Choose Difficulty",
        heading_font,
        BLACK,
        (width // 2, 205)
    )

    button_width = min(150, (width - 60) // 3)
    gap = 10
    total_width = button_width * 3 + gap * 2
    start_x = (width - total_width) // 2

    beginner_rect = pygame.Rect(
        start_x, 240, button_width, 50
    )
    medium_rect = pygame.Rect(
        start_x + button_width + gap, 240,
        button_width, 50
    )
    hard_rect = pygame.Rect(
        start_x + 2 * (button_width + gap), 240,
        button_width, 50
    )

    draw_button(
        "Beginner",
        beginner_rect,
        difficulty == "Beginner"
    )

    draw_button(
        "Medium",
        medium_rect,
        difficulty == "Medium"
    )

    draw_button(
        "Hard",
        hard_rect,
        difficulty == "Hard"
    )

    # Symbol selection
    draw_text(
        "Choose Your Symbol",
        heading_font,
        BLACK,
        (width // 2, 350)
    )

    symbol_width = 120

    x_rect = pygame.Rect(
        width // 2 - 130, 385, symbol_width, 50
    )
    o_rect = pygame.Rect(
        width // 2 + 10, 385, symbol_width, 50
    )

    draw_button(
        "Play as X",
        x_rect,
        human_symbol == PLAYER_X,
        RED
    )

    draw_button(
        "Play as O",
        o_rect,
        human_symbol == PLAYER_O,
        BLUE
    )

    # First turn selection
    draw_text(
        "Who Starts First?",
        heading_font,
        BLACK,
        (width // 2, 495)
    )

    starter_width = 110

    human_rect = pygame.Rect(
        width // 2 - 175, 530, starter_width, 50
    )
    ai_rect = pygame.Rect(
        width // 2 - 55, 530, starter_width, 50
    )
    random_rect = pygame.Rect(
        width // 2 + 65, 530, starter_width, 50
    )

    draw_button("You", human_rect, starter == "Human")
    draw_button("AI", ai_rect, starter == "AI")
    draw_button("Random", random_rect, starter == "Random")

    # Sound option
    sound_rect = pygame.Rect(
        width // 2 - 80,
        620,
        160,
        45
    )

    sound_label = "Sound: ON" if sound_on else "Sound: OFF"
    draw_button(sound_label, sound_rect, sound_on, GREEN)

    # Start button
    start_rect = pygame.Rect(
        width // 2 - 130,
        700,
        260,
        65
    )

    draw_button(
        "START GAME",
        start_rect,
        True,
        GREEN
    )

    return {
        "beginner": beginner_rect,
        "medium": medium_rect,
        "hard": hard_rect,
        "x": x_rect,
        "o": o_rect,
        "human": human_rect,
        "ai": ai_rect,
        "random": random_rect,
        "sound": sound_rect,
        "start": start_rect
    }


# =========================================================
# 10. MOUSE CLICK HANDLING
# =========================================================

def handle_menu_click(position):
    global difficulty, human_symbol, starter, sound_on

    buttons = draw_menu()

    if buttons["beginner"].collidepoint(position):
        difficulty = "Beginner"
        play_sound("click")

    elif buttons["medium"].collidepoint(position):
        difficulty = "Medium"
        play_sound("click")

    elif buttons["hard"].collidepoint(position):
        difficulty = "Hard"
        play_sound("click")

    elif buttons["x"].collidepoint(position):
        human_symbol = PLAYER_X
        play_sound("click")

    elif buttons["o"].collidepoint(position):
        human_symbol = PLAYER_O
        play_sound("click")

    elif buttons["human"].collidepoint(position):
        starter = "Human"
        play_sound("click")

    elif buttons["ai"].collidepoint(position):
        starter = "AI"
        play_sound("click")

    elif buttons["random"].collidepoint(position):
        starter = "Random"
        play_sound("click")

    elif buttons["sound"].collidepoint(position):
        sound_on = not sound_on

    elif buttons["start"].collidepoint(position):
        play_sound("click")
        start_game()


def handle_game_click(position):
    global current_player, game_state

    restart_rect, menu_rect = draw_board()

    if restart_rect.collidepoint(position):
        play_sound("click")
        reset_board()
        return

    if menu_rect.collidepoint(position):
        play_sound("click")
        game_state = "menu"
        return

    # Only accept human moves during the human turn
    if game_over or current_player != human_symbol:
        return

    if ai_waiting:
        return

    board_x, board_y, board_size, cell_size = get_layout()

    x, y = position

    if not (
        board_x <= x < board_x + board_size
        and board_y <= y < board_y + board_size
    ):
        return

    col = int((x - board_x) // cell_size)
    row = int((y - board_y) // cell_size)

    if (
        0 <= row < BOARD_SIZE
        and 0 <= col < BOARD_SIZE
        and board[row][col] == EMPTY
    ):
        board[row][col] = human_symbol

        animation_times[(row, col)] = pygame.time.get_ticks()

        play_sound("move")
        check_game_status()

        if not game_over:
            current_player = ai_symbol
            schedule_ai_move()


# =========================================================
# 11. MAIN GAME LOOP
# =========================================================

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Responsive resizing
        elif event.type == pygame.VIDEORESIZE:
            new_width = max(400, event.w)
            new_height = max(500, event.h)

            screen = pygame.display.set_mode(
                (new_width, new_height),
                pygame.RESIZABLE
            )

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:

                if game_state == "menu":
                    handle_menu_click(event.pos)

                elif game_state == "game":
                    handle_game_click(event.pos)

    # AI turn
    if (
        game_state == "game"
        and ai_waiting
        and not game_over
        and pygame.time.get_ticks() - ai_move_time >= AI_DELAY
    ):
        make_ai_move()

    # Draw current screen
    if game_state == "menu":
        draw_menu()
    else:
        draw_board()

    pygame.display.flip()
    clock.tick(60)


# =========================================================
# 12. EXIT
# =========================================================

pygame.quit()
sys.exit()
