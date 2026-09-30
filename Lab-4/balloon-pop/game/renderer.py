"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame


WIDTH, HEIGHT = 700, 500
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (200, 230, 245)
COLOR_TEXT = (30, 30, 30)


def draw_scene(surface, balloons):
    surface.fill(COLOR_BG)

    for b in balloons:
        pygame.draw.circle(
            surface,
            b.color,
            (int(b.x), int(b.y)),
            b.radius
        )

        pygame.draw.line(
            surface,
            (120, 120, 120),
            (b.x, b.y + b.radius),
            (b.x, b.y + b.radius + 12),
            2
        )


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_banner(surface, font, text):
    surf = font.render(text, True, (180, 40, 40))
    rect = surf.get_rect(
        center=(
            surface.get_width() // 2,
            surface.get_height() // 2
        )
    )
    surface.blit(surf, rect)


def draw_game_over(surface, font, score):
    overlay = pygame.Surface(
        (surface.get_width(), surface.get_height()),
        pygame.SRCALPHA
    )
    overlay.fill((0, 0, 0, 150))
    surface.blit(overlay, (0, 0))

    game_over_text = font.render(
        "Game Over",
        True,
        (255, 255, 255)
    )

    score_text = font.render(
        f"Final Score: {score}",
        True,
        (255, 255, 255)
    )

    restart_text = font.render(
        "Press R to Restart",
        True,
        (255, 255, 255)
    )

    center_x = surface.get_width() // 2

    surface.blit(
        game_over_text,
        game_over_text.get_rect(
            center=(center_x, 200)
        )
    )

    surface.blit(
        score_text,
        score_text.get_rect(
            center=(center_x, 240)
        )
    )

    surface.blit(
        restart_text,
        restart_text.get_rect(
            center=(center_x, 280)
        )
    )
