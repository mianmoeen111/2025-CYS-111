

import sys
import pygame
import math

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 650
BOARD_SIZE = 3
CELL_SIZE = 150
LINE_WIDTH = 10
MARGIN = 50

# Players
PLAYER_X = 'X'
PLAYER_O = 'O'
EMPTY = '_'

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 128, 0)
GRAY = (200, 200, 200)

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe - AI")

# Fonts
font = pygame.font.SysFont('Arial', 30)
title_font = pygame.font.SysFont('Arial', 45)

# Game variables
board = [
    [EMPTY for _ in range(BOARD_SIZE)]
    for _ in range(BOARD_SIZE)
]

# Human and AI players
HUMAN = PLAYER_X
AI = PLAYER_O

current_player = HUMAN
game_over = False
winner = None

# AI delay settings
ai_waiting = False
ai_move_time = 0
AI_DELAY = 500


# Reset game
def reset_game():
    global board, current_player, game_over, winner
    global ai_waiting

    board = [
        [EMPTY for _ in range(BOARD_SIZE)]
        for _ in range(BOARD_SIZE)
    ]

    current_player = HUMAN
    game_over = False
    winner = None
    ai_waiting = False


# Check winner
def get_winner(b):

    # Check rows
    for row in range(BOARD_SIZE):
        if b[row][0] == b[row][1] == b[row][2] != EMPTY:
            return b[row][0]

    # Check columns
    for col in range(BOARD_SIZE):
        if b[0][col] == b[1][col] == b[2][col] != EMPTY:
            return b[0][col]

    # Check main diagonal
    if b[0][0] == b[1][1] == b[2][2] != EMPTY:
        return b[0][0]

    # Check other diagonal
    if b[0][2] == b[1][1] == b[2][0] != EMPTY:
        return b[0][2]

    return None


# Check game status
def check_winner():
    global game_over, winner

    winner = get_winner(board)

    if winner:
        game_over = True
        return

    # Check draw
    if all(
        board[row][col] != EMPTY
        for row in range(BOARD_SIZE)
        for col in range(BOARD_SIZE)
    ):
        game_over = True


# Minimax algorithm
def minimax(b, depth, is_maximizing):

    result = get_winner(b)

    # AI wins
    if result == AI:
        return 10 - depth

    # Human wins
    if result == HUMAN:
        return depth - 10

    # Draw
    if all(
        b[row][col] != EMPTY
        for row in range(BOARD_SIZE)
        for col in range(BOARD_SIZE)
    ):
        return 0

    # AI maximizes score
    if is_maximizing:

        best_score = -math.inf

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):

                if b[row][col] == EMPTY:

                    b[row][col] = AI

                    score = minimax(
                        b, depth + 1, False
                    )

                    b[row][col] = EMPTY

                    best_score = max(best_score, score)

        return best_score

    # Human minimizes score
    else:

        best_score = math.inf

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):

                if b[row][col] == EMPTY:

                    b[row][col] = HUMAN

                    score = minimax(
                        b, depth + 1, True
                    )

                    b[row][col] = EMPTY

                    best_score = min(best_score, score)

        return best_score


# AI move
def ai_move():

    global current_player

    best_score = -math.inf
    best_move = None

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):

            if board[row][col] == EMPTY:

                board[row][col] = AI

                score = minimax(
                    board, 0, False
                )

                board[row][col] = EMPTY

                if score > best_score:
                    best_score = score
                    best_move = (row, col)

    if best_move is not None:

        row, col = best_move

        board[row][col] = AI

        check_winner()

        if not game_over:
            current_player = HUMAN


# Draw board and game information
def draw_board():

    screen.fill(WHITE)

    # Game title
    title = title_font.render(
        "Tic Tac Toe", True, BLACK
    )

    screen.blit(
        title,
        (WIDTH // 2 - title.get_width() // 2, 10)
    )

    # Current player information
    if not game_over:

        if current_player == HUMAN:
            message = "Your Turn: X"
        else:
            message = "AI Turn: O"

        player_text = font.render(
            message, True, BLACK
        )

        screen.blit(
            player_text,
            (WIDTH // 2 - player_text.get_width() // 2, 65)
        )

    # Draw cells and symbols
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):

            rect = pygame.Rect(
                MARGIN + col * CELL_SIZE,
                MARGIN + row * CELL_SIZE + 100,
                CELL_SIZE,
                CELL_SIZE
            )

            pygame.draw.rect(screen, GRAY, rect)

            pygame.draw.rect(
                screen, BLACK, rect, LINE_WIDTH
            )

            # Draw X
            if board[row][col] == PLAYER_X:

                pygame.draw.line(
                    screen,
                    RED,
                    (rect.left + 20, rect.top + 20),
                    (rect.right - 20, rect.bottom - 20),
                    LINE_WIDTH
                )

                pygame.draw.line(
                    screen,
                    RED,
                    (rect.right - 20, rect.top + 20),
                    (rect.left + 20, rect.bottom - 20),
                    LINE_WIDTH
                )

            # Draw O
            elif board[row][col] == PLAYER_O:

                pygame.draw.circle(
                    screen,
                    BLUE,
                    rect.center,
                    CELL_SIZE // 2 - 20,
                    LINE_WIDTH
                )

    # Display result and restart button
    if game_over:

        if winner == HUMAN:
            message = "You Win!"
            color = GREEN

        elif winner == AI:
            message = "AI Wins!"
            color = GREEN

        else:
            message = "It's a draw!"
            color = BLACK

        result_text = font.render(
            message, True, color
        )

        screen.blit(
            result_text,
            (
                WIDTH // 2 - result_text.get_width() // 2,
                HEIGHT - 115
            )
        )

        # Restart button
        restart_rect = pygame.Rect(
            WIDTH // 2 - 100,
            HEIGHT - 65,
            200,
            45
        )

        pygame.draw.rect(
            screen, GREEN, restart_rect
        )

        pygame.draw.rect(
            screen, BLACK, restart_rect, 2
        )

        restart_text = font.render(
            "Play Again", True, WHITE
        )

        screen.blit(
            restart_text,
            restart_text.get_rect(
                center=restart_rect.center
            )
        )

        return restart_rect

    return None


# Main game loop
clock = pygame.time.Clock()
restart_button = None
running = True

while running:

    for event in pygame.event.get():

        # Close game window
        if event.type == pygame.QUIT:
            running = False

        # Handle mouse clicks
        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                x, y = event.pos

                # Restart game
                if (
                    game_over
                    and restart_button is not None
                    and restart_button.collidepoint(x, y)
                ):

                    reset_game()
                    restart_button = None
                    continue

                # Human player move
                if not game_over and current_player == HUMAN:

                    col = (x - MARGIN) // CELL_SIZE
                    row = (y - MARGIN - 100) // CELL_SIZE

                    if (
                        0 <= row < BOARD_SIZE
                        and 0 <= col < BOARD_SIZE
                        and board[row][col] == EMPTY
                    ):

                        # Place X
                        board[row][col] = HUMAN

                        check_winner()

                        # Schedule AI move
                        if not game_over:

                            current_player = AI
                            ai_waiting = True

                            ai_move_time = pygame.time.get_ticks()

    # AI move after delay
    if (
        ai_waiting
        and not game_over
        and pygame.time.get_ticks() - ai_move_time >= AI_DELAY
    ):

        ai_waiting = False
        ai_move()

    # Draw game
    restart_button = draw_board()

    pygame.display.flip()

    clock.tick(60)


# Quit Pygame
pygame.quit()
sys.exit()
