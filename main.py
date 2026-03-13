import argparse
import pygame

from src.game.game import ACTION_DOWN
from src.game.game import ACTION_LEFT
from src.game.game import ACTION_RIGHT
from src.game.game import ACTION_UP
from src.game.game import Game2048

BOARD_SIZE = 4
TILE_SIZE = 100
GAP_SIZE = 10
MARGIN = 20
SCREEN_SIZE = BOARD_SIZE * TILE_SIZE + (BOARD_SIZE + 1) * GAP_SIZE + 2 * MARGIN
BACKGROUND_COLOR = "#e5e5e0"
EMPTY_TILE_COLOR = "#cdc1b4"
TILE_COLORS = {
    2: "#f8f8f5",
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
FONT_COLOR = "#000000"
OVERLAY_COLOR = (255, 255, 255, 170)


def draw_tile(screen, font, value, x, y):
    color = EMPTY_TILE_COLOR if value == 0 else TILE_COLORS.get(value, "#3c3a32")
    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, color, rect, border_radius=8)
    if value != 0:
        text = font.render(str(value), True, FONT_COLOR)
        text_rect = text.get_rect(center=(x + TILE_SIZE / 2, y + TILE_SIZE / 2))
        screen.blit(text, text_rect)


def draw_board(screen, font, game):
    screen.fill(BACKGROUND_COLOR)
    board = game.get_state()
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            x = MARGIN + GAP_SIZE + col * (TILE_SIZE + GAP_SIZE)
            y = MARGIN + GAP_SIZE + row * (TILE_SIZE + GAP_SIZE)
            draw_tile(screen, font, board[row][col], x, y)

    score_text = font.render(f"Score: {game.get_score()}", True, FONT_COLOR)
    screen.blit(score_text, (MARGIN, 8))


def draw_overlay(screen, font, message):
    overlay = pygame.Surface((SCREEN_SIZE, SCREEN_SIZE), pygame.SRCALPHA)
    overlay.fill(OVERLAY_COLOR)
    screen.blit(overlay, (0, 0))
    text = font.render(message, True, (180, 30, 30))
    text_rect = text.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE // 2))
    screen.blit(text, text_rect)


def run_human_mode():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("2048")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 32)

    game = Game2048(size=BOARD_SIZE)
    continue_after_win = False
    running = True

    key_to_action = {
        pygame.K_LEFT: ACTION_LEFT,
        pygame.K_RIGHT: ACTION_RIGHT,
        pygame.K_UP: ACTION_UP,
        pygame.K_DOWN: ACTION_DOWN,
    }

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reset()
                    continue_after_win = False
                elif event.key == pygame.K_c and game.has_won:
                    continue_after_win = True
                elif event.key in key_to_action and not game.is_terminal():
                    if not game.has_won or continue_after_win:
                        game.apply_action(key_to_action[event.key])

        draw_board(screen, font, game)

        if game.is_terminal():
            draw_overlay(screen, font, "Game over")
        elif game.has_won and not continue_after_win:
            draw_overlay(screen, font, "You won! Press C to continue")

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


def run_ai_mode():
    print("AI mode is scaffolded. Connect src/ai modules to Game2048 API.")


def run_benchmark_mode():
    print("Benchmark mode is scaffolded. Connect src/benchmark/runner.py here.")


def main():
    parser = argparse.ArgumentParser(description="2048 game")
    parser.add_argument(
        "--mode",
        choices=["human", "ai", "benchmark"],
        default="human",
        help="Run mode: human, ai, or benchmark",
    )
    args = parser.parse_args()

    if args.mode == "human":
        run_human_mode()
    elif args.mode == "ai":
        run_ai_mode()
    else:
        run_benchmark_mode()


if __name__ == "__main__":
    main()
