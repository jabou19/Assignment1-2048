import pygame
import random

pygame.init()

# Declaration
Size = 4
Tile_size = 100
Gap_size = 10
Margine = 20
Screen_size = Size * Tile_size + (Size + 1) * Gap_size + 2 * Margine
Screen_width = Screen_size
Screen_height = Screen_size
Background_color = "#e5e5e0"
EMPTY_TILE_COLOR = "#93908c00"
Tile_colors = {
    2: "#f8f8f5c1",
    4: "#f0be95",
    8: "#f3a35e",
    16: "#f28e58",
    32: "#e77356",
    64: "#f25730",
    128: "#f0c88b",
    256: "#f1be67",
    512: "#f1c15f",
    1024: "#f1b949",
    2048: "#eeae24",
}
FONT_COLOR = (0, 0, 0)
FONT = pygame.font.SysFont("arial", 40)


# Functions
def draw_tile(screen, value, x, y):
    color = EMPTY_TILE_COLOR if value == 0 else Tile_colors.get(value, (60, 58, 50))
    rect = pygame.Rect(x, y, Tile_size, Tile_size)
    pygame.draw.rect(screen, color, rect)
    if value != 0:
        text = FONT.render(str(value), True, FONT_COLOR)
        text_rect = text.get_rect(center=(x + Tile_size / 2, y + Tile_size / 2))
        screen.blit(text, text_rect)


def draw_board(screen, board):
    screen.fill(Background_color)
    for row in range(Size):
        for col in range(Size):
            value = board[row][col]
            x = Margine + Gap_size + col * (Tile_size + Gap_size)
            y = Margine + Gap_size + row * (Tile_size + Gap_size)
            draw_tile(screen, value, x, y)


def add_new_tile(board):
    empty_tiles = [(r, c) for r in range(Size) for c in range(Size) if board[r][c] == 0]
    if empty_tiles:
        row, col = random.choice(empty_tiles)
        board[row][col] = 2 if random.random() < 0.9 else 4


def slide_row_left(row):
    new_row = [i for i in row if i != 0]
    new_row += [0] * (Size - len(new_row))
    for i in range(Size - 1):
        if new_row[i] == new_row[i + 1] and new_row[i] != 0:
            new_row[i] *= 2
            new_row[i + 1] = 0
    new_row = [i for i in new_row if i != 0]
    new_row += [0] * (Size - len(new_row))
    return new_row


def move_left(board):
    new_board = []
    for row in board:
        new_board.append(slide_row_left(row))
    return new_board


def move_right(board):
    new_board = []
    for row in board:
        new_board.append(slide_row_left(row[::-1])[::-1])
    return new_board


def move_up(board):
    new_board = list(zip(*board))
    new_board = move_left(new_board)
    return [list(row) for row in zip(*new_board)]


def move_down(board):
    new_board = list(zip(*board))
    new_board = move_right(new_board)
    return [list(row) for row in zip(*new_board)]


def check_win(board):
    for row in board:
        if 2048 in row:
            return True
    return False


def check_moves_available(board):
    for row in range(Size):
        if 0 in board[row]:
            return True
        for col in range(Size - 1):
            if board[row][col] == board[row][col + 1]:
                return True
    for col in range(Size):
        for row in range(Size - 1):
            if board[row][col] == board[row + 1][col]:
                return True
    return False


def main():
    screen = pygame.display.set_mode((Screen_width, Screen_height))
    pygame.display.set_caption("2048 Game")
    clock = pygame.time.Clock()

    board = [[0] * Size for _ in range(Size)]
    add_new_tile(board)
    add_new_tile(board)

    running = True
    won = False
    lost = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if not won and not lost:
                    if event.key == pygame.K_LEFT:
                        board = move_left(board)
                    elif event.key == pygame.K_RIGHT:
                        board = move_right(board)
                    elif event.key == pygame.K_UP:
                        board = move_up(board)
                    elif event.key == pygame.K_DOWN:
                        board = move_down(board)
                    add_new_tile(board)
                    won = check_win(board)
                    lost = not check_moves_available(board)

        draw_board(screen, board)

        if won:
            text = FONT.render("You won!", True, (255, 0, 0))
            text_rect = text.get_rect(center=(Screen_width // 2, Screen_height // 2))
            screen.blit(text, text_rect)
        elif lost:
            text = FONT.render("You lost!", True, (255, 0, 0))
            text_rect = text.get_rect(center=(Screen_width // 2, Screen_height // 2))
            screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
