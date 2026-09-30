"""
GameEngine: owns all balloons, spawns new ones, handles clicks,
and manages the player's lives and round timer.
"""

import random
import pygame

from game.balloon import Balloon
from game.click_detection import check_pop
from game.renderer import WIDTH, HEIGHT


SPAWN_INTERVAL_FRAMES = 45
ROUND_DURATION_SECONDS = 30


class GameEngine:
    def __init__(self):
        self.balloons = []
        self.frames_until_spawn = 0
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.start_time = pygame.time.get_ticks()
        self.time_left = ROUND_DURATION_SECONDS

    def restart(self):
        self.balloons.clear()
        self.frames_until_spawn = 0
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.start_time = pygame.time.get_ticks()
        self.time_left = ROUND_DURATION_SECONDS

    def _spawn_balloon(self):
        radius = random.randint(16, 44)
        x = random.randint(radius + 10, WIDTH - radius - 10)
        speed = random.uniform(1.5, 3.0)

        balloon_type = random.choices(
            ["normal", "bonus", "penalty"],
            weights=[65, 20, 15],
            k=1
        )[0]

        self.balloons.append(
            Balloon(
                x=x,
                y=-radius,
                radius=radius,
                speed=speed,
                balloon_type=balloon_type
            )
        )

    def handle_click(self, pos):
        if self.game_over:
            return

        popped = check_pop(self.balloons, pos)

        if popped is not None:
            # Remove immediately so it cannot count as a miss.
            self.balloons.remove(popped)

            self.score += popped.points
            self.score = max(0, self.score)

    def update(self):
        if self.game_over:
            return

        elapsed_seconds = (
            pygame.time.get_ticks() - self.start_time
        ) / 1000

        self.time_left = max(
            0,
            ROUND_DURATION_SECONDS - elapsed_seconds
        )

        if self.time_left <= 0:
            self.time_left = 0
            self.game_over = True
            return

        self.frames_until_spawn -= 1

        if self.frames_until_spawn <= 0:
            self._spawn_balloon()
            self.frames_until_spawn = SPAWN_INTERVAL_FRAMES

        missed_balloons = []

        for balloon in self.balloons:
            balloon.update()

            if balloon.is_past_bottom(HEIGHT):
                missed_balloons.append(balloon)

        for balloon in missed_balloons:
            self.balloons.remove(balloon)
            self.lives -= 1

        if self.lives <= 0:
            self.lives = 0
            self.game_over = True

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(surface, self.balloons)

        renderer.draw_text(
            surface,
            font,
            f"Score: {self.score}",
            (10, 10)
        )

        renderer.draw_text(
            surface,
            font,
            f"Lives: {self.lives}",
            (10, 40)
        )

        renderer.draw_text(
            surface,
            font,
            f"Time: {int(self.time_left)}",
            (10, 70)
        )

        if self.game_over:
            renderer.draw_game_over(
                surface,
                font,
                self.score
            )
