
import sys
import pygame

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
pygame.display.set_caption("Tic Tac Toe")

# Fonts
font = pygame.font.SysFont('Arial', 30)
title_font = pygame.font.SysFont('Arial', 45)

# Game variables
board = [
    [EMPTY for _ in range(BOARD_SIZE)]
    for _ in range(BOARD_SIZE)
]

current_player = PLAYER_X
game_over = False
winner = None


# Reset the game
def reset_game():
    global board, current_player, game_over, winner

    board = [
        [EMPTY for _ in range(BOARD_SIZE)]
        for _ in range(BOARD_SIZE)
    ]

    current_player = PLAYER_X
    game_over = False
    winner = None


# Check winner or draw
def check_winner():
    global game_over, winner

    # Check rows
    for i in range(BOARD_SIZE):
        if (
            board[i][0] == board[i][1] == board[i][2]
            and board[i][0] != EMPTY
        ):
            winner = board[i][0]
            game_over = True
            return

    # Check columns
    for i in range(BOARD_SIZE):
        if (
            board[0][i] == board[1][i] == board[2][i]
            and board[0][i] != EMPTY
        ):
            winner = board[0][i]
            game_over = True
            return

    # Check main diagonal
    if (
        board[0][0] == board[1][1] == board[2][2]
        and board[0][0] != EMPTY
    ):
        winner = board[0][0]
        game_over = True
        return

    # Check other diagonal
    if (
        board[0][2] == board[1][1] == board[2][0]
        and board[0][2] != EMPTY
    ):
        winner = board[0][2]
        game_over = True
        return

    # Check draw
    if all(
        board[row][col] != EMPTY
        for row in range(BOARD_SIZE)
        for col in range(BOARD_SIZE)
    ):
        game_over = True


# Draw the board and game information
def draw_board():
    screen.fill(WHITE)

    # Game title
    title = title_font.render("Tic Tac Toe", True, BLACK)
    screen.blit(
        title,
        (WIDTH // 2 - title.get_width() // 2, 10)
    )

    # Current player
    if not game_over:
        player_text = font.render(
            f"Current Player: {current_player}", True, BLACK
        )
        screen.blit(
            player_text,
            (WIDTH // 2 - player_text.get_width() // 2, 65)
        )

    # Draw cells and player symbols
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):

            rect = pygame.Rect(
                MARGIN + col * CELL_SIZE,
                MARGIN + row * CELL_SIZE + 100,
                CELL_SIZE,
                CELL_SIZE
            )

            pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, BLACK, rect, LINE_WIDTH)

            if board[row][col] == PLAYER_X:

                # Draw X
                pygame.draw.line(
                    screen, RED,
                    (rect.left + 20, rect.top + 20),
                    (rect.right - 20, rect.bottom - 20),
                    LINE_WIDTH
                )

                pygame.draw.line(
                    screen, RED,
                    (rect.right - 20, rect.top + 20),
                    (rect.left + 20, rect.bottom - 20),
                    LINE_WIDTH
                )

            elif board[row][col] == PLAYER_O:

                # Draw O
                pygame.draw.circle(
                    screen,
                    BLUE,
                    rect.center,
                    CELL_SIZE // 2 - 20,
                    LINE_WIDTH
                )

    # Display result and restart button
    if game_over:

        if winner:
            message = f"Player {winner} wins!"
            color = GREEN
        else:
            message = "It's a draw!"
            color = BLACK

        result_text = font.render(message, True, color)

        screen.blit(
            result_text,
            (
                WIDTH // 2 - result_text.get_width() // 2,
                HEIGHT - 115
            )
        )

        restart_rect = pygame.Rect(
            WIDTH // 2 - 100,
            HEIGHT - 65,
            200,
            45
        )

        pygame.draw.rect(screen, GREEN, restart_rect)
        pygame.draw.rect(screen, BLACK, restart_rect, 2)

        restart_text = font.render(
            "Play Again", True, WHITE
        )

        screen.blit(
            restart_text,
            restart_text.get_rect(center=restart_rect.center)
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

                # Place X or O
                if not game_over:

                    col = (x - MARGIN) // CELL_SIZE
                    row = (y - MARGIN - 100) // CELL_SIZE

                    if (
                        0 <= row < BOARD_SIZE
                        and 0 <= col < BOARD_SIZE
                        and board[row][col] == EMPTY
                    ):

                        board[row][col] = current_player

                        check_winner()

                        # Switch player
                        if not game_over:
                            if current_player == PLAYER_X:
                                current_player = PLAYER_O
                            else:
                                current_player = PLAYER_X

    # Draw everything
    restart_button = draw_board()

    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
 





