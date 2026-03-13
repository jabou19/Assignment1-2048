import argparse
import pygame

from src.game.game import ACTION_DOWN
from src.game.game import ACTION_LEFT
from src.game.game import ACTION_RIGHT
from src.game.game import ACTION_UP
from src.game.game import Game2048

BOARD_SIZE = 4
TILE_SIZE = 90
GAP_SIZE = 8
MARGIN = 16
HUD_HEIGHT = 92
FOOTER_HEIGHT = 62
BOARD_PIXEL_SIZE = BOARD_SIZE * TILE_SIZE + (BOARD_SIZE + 1) * GAP_SIZE
SCREEN_WIDTH = BOARD_PIXEL_SIZE + 2 * MARGIN
SCREEN_HEIGHT = HUD_HEIGHT + BOARD_PIXEL_SIZE + FOOTER_HEIGHT
BACKGROUND_COLOR = "#e5e5e0"
EMPTY_TILE_COLOR = "#93908c00"
TILE_COLORS = {
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
FONT_COLOR = "#000000"
OVERLAY_COLOR = (255, 255, 255, 170)
HUD_CARD_COLOR = "#56f20e"
HUD_CARD_BORDER_COLOR = "#f41414"
BUTTON_COLOR = "#4df012"
BUTTON_HOVER_COLOR = "#e6fbd9"
BUTTON_BORDER_COLOR = "#f41414"


def reset_human_game(game):
    game.reset()
    return False, 0


def draw_tile(screen, font, value, x, y):
    color = EMPTY_TILE_COLOR if value == 0 else TILE_COLORS.get(value, "#3c3a32")
    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, color, rect, border_radius=6)
    if value != 0:
        text = font.render(str(value), True, FONT_COLOR)
        text_rect = text.get_rect(center=(x + TILE_SIZE / 2, y + TILE_SIZE / 2))
        screen.blit(text, text_rect)


def draw_hud(screen, label_font, value_font, button_font, game, moves, mouse_pos):
    hud_rect = pygame.Rect(MARGIN, 8, BOARD_PIXEL_SIZE, HUD_HEIGHT - 16)

    button_width = 100
    button_height = 30
    button_rect = pygame.Rect(
        hud_rect.right - button_width - 10,
        hud_rect.top + 8,
        button_width,
        button_height,
    )
    button_color = (
        BUTTON_HOVER_COLOR if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    )
    pygame.draw.rect(screen, button_color, button_rect, border_radius=7)
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, button_rect, width=2, border_radius=7)

    card_gap = 18
    card_padding_x = 12
    available_width = (
        button_rect.left - hud_rect.left - (2 * card_padding_x) - card_gap - 12
    )
    card_width = available_width // 2
    score_card = pygame.Rect(MARGIN + card_padding_x, 18, card_width, 56)
    moves_card = pygame.Rect(score_card.right + card_gap, 24, card_width, 64)
    moves_card = pygame.Rect(score_card.right + card_gap, 18, card_width, 56)
    pygame.draw.rect(screen, HUD_CARD_COLOR, score_card, border_radius=7)
    pygame.draw.rect(screen, HUD_CARD_COLOR, moves_card, border_radius=7)
    pygame.draw.rect(
        screen, HUD_CARD_BORDER_COLOR, score_card, width=2, border_radius=7
    )
    pygame.draw.rect(
        screen, HUD_CARD_BORDER_COLOR, moves_card, width=2, border_radius=7
    )

    score_label = label_font.render("SCORE", True, FONT_COLOR)
    score_value = value_font.render(str(game.get_score()), True, FONT_COLOR)
    moves_label = label_font.render("MOVES", True, FONT_COLOR)
    moves_value = value_font.render(str(moves), True, FONT_COLOR)
    restart_text = button_font.render("Restart", True, FONT_COLOR)

    screen.blit(
        score_label,
        score_label.get_rect(center=(score_card.centerx, score_card.top + 11)),
    )
    screen.blit(
        score_value,
        score_value.get_rect(center=(score_card.centerx, score_card.centery + 7)),
    )
    screen.blit(
        moves_label,
        moves_label.get_rect(center=(moves_card.centerx, moves_card.top + 11)),
    )
    screen.blit(
        moves_value,
        moves_value.get_rect(center=(moves_card.centerx, moves_card.centery + 7)),
    )
    screen.blit(restart_text, restart_text.get_rect(center=button_rect.center))

    return button_rect


def draw_footer_buttons(screen, button_font, mouse_pos):
    footer_top = HUD_HEIGHT + BOARD_PIXEL_SIZE + 10
    run_button_rect = pygame.Rect(MARGIN, footer_top, 108, 34)
    choose_button_rect = pygame.Rect(run_button_rect.right + 14, footer_top, 176, 34)

    run_button_color = (
        BUTTON_HOVER_COLOR if run_button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    )
    choose_button_color = (
        BUTTON_HOVER_COLOR
        if choose_button_rect.collidepoint(mouse_pos)
        else BUTTON_COLOR
    )

    pygame.draw.rect(screen, run_button_color, run_button_rect, border_radius=7)
    pygame.draw.rect(
        screen, BUTTON_BORDER_COLOR, run_button_rect, width=2, border_radius=7
    )
    pygame.draw.rect(screen, choose_button_color, choose_button_rect, border_radius=7)
    pygame.draw.rect(
        screen, BUTTON_BORDER_COLOR, choose_button_rect, width=2, border_radius=7
    )

    run_text = button_font.render("Run", True, FONT_COLOR)
    choose_text = button_font.render("Choose Algorithm", True, FONT_COLOR)
    screen.blit(run_text, run_text.get_rect(center=run_button_rect.center))
    screen.blit(choose_text, choose_text.get_rect(center=choose_button_rect.center))

    return run_button_rect, choose_button_rect


def draw_board(screen, font, game):
    screen.fill(BACKGROUND_COLOR)
    board = game.get_state()
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            x = MARGIN + GAP_SIZE + col * (TILE_SIZE + GAP_SIZE)
            y = HUD_HEIGHT + GAP_SIZE + row * (TILE_SIZE + GAP_SIZE)
            draw_tile(screen, font, board[row][col], x, y)


def draw_overlay(screen, font, message):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill(OVERLAY_COLOR)
    screen.blit(overlay, (0, 0))
    text = font.render(message, True, (180, 30, 30))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)


def run_human_mode():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("2048")
    clock = pygame.time.Clock()
    tile_font = pygame.font.SysFont("arial", 28)
    hud_label_font = pygame.font.SysFont("arial", 16, bold=True)
    hud_value_font = pygame.font.SysFont("arial", 26, bold=True)
    hud_button_font = pygame.font.SysFont("arial", 16, bold=True)
    overlay_font = pygame.font.SysFont("arial", 28, bold=True)

    game = Game2048(size=BOARD_SIZE)
    continue_after_win = False
    moves = 0
    running = True
    restart_button_rect = pygame.Rect(0, 0, 0, 0)
    run_button_rect = pygame.Rect(0, 0, 0, 0)
    choose_button_rect = pygame.Rect(0, 0, 0, 0)

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
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if restart_button_rect.collidepoint(event.pos):
                    continue_after_win, moves = reset_human_game(game)
                elif run_button_rect.collidepoint(event.pos):
                    pass
                elif choose_button_rect.collidepoint(event.pos):
                    pass
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    continue_after_win, moves = reset_human_game(game)
                elif event.key == pygame.K_c and game.has_won:
                    continue_after_win = True
                elif event.key in key_to_action and not game.is_terminal():
                    if not game.has_won or continue_after_win:
                        if game.apply_action(key_to_action[event.key]):
                            moves += 1

        draw_board(screen, tile_font, game)
        restart_button_rect = draw_hud(
            screen,
            hud_label_font,
            hud_value_font,
            hud_button_font,
            game,
            moves,
            pygame.mouse.get_pos(),
        )
        run_button_rect, choose_button_rect = draw_footer_buttons(
            screen,
            hud_button_font,
            pygame.mouse.get_pos(),
        )

        if game.is_terminal():
            draw_overlay(screen, overlay_font, "Game over")
        elif game.has_won and not continue_after_win:
            draw_overlay(screen, overlay_font, "You won! Press C to continue")

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
