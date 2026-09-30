"""
Balloon: falls from the top of the screen. The player must pop it
before it reaches the bottom.
"""

import pygame


class Balloon:
    def __init__(self, x, y, radius, speed, balloon_type="normal"):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.balloon_type = balloon_type

        if balloon_type == "bonus":
            self.color = (255, 215, 0)       # Gold/Yellow
            self.points = 30
        elif balloon_type == "penalty":
            self.color = (80, 20, 20)        # Dark Red
            self.points = -20
        else:
            self.color = (220, 90, 120)      # Normal
            self.points = 10

    def update(self):
        self.y += self.speed

    def is_past_bottom(self, height):
        return self.y - self.radius > height

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.radius),
            int(self.y - self.radius),
            self.radius * 2,
            self.radius * 2
        )
