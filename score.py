from settings import *
import pygame

class Score:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        h = int(GAME_HEIGHT * SCORE_HEIGHT_FRACTION - PADDING)
        self.surface = pygame.Surface((SIDEBAR_WIDTH, h))
        self.rect = self.surface.get_rect(bottomright=(WINDOW_WIDTH - PADDING, WINDOW_HEIGHT - PADDING))

        # state
        self.lines = 0
        self.score = 0
        self.level = 1

        # fonts
        self.title_font = pygame.font.Font(None, 36)
        self.value_font = pygame.font.Font(None, 30)

    # called by Game
    def update(self, lines, score, level):
        self.lines = lines
        self.score = score
        self.level = level

    def _blit_pair(self, title, value, y):
        color = LINE_COLOR
        t = self.title_font.render(title, True, color)
        v = self.value_font.render(str(value), True, color)
        self.surface.blit(t, (PADDING, y))
        self.surface.blit(v, (PADDING, y + 28))

    def run(self):
        self.surface.fill(GRAY)
        y = PADDING
        self._blit_pair("SCORE", self.score, y); y += 70
        self._blit_pair("LEVEL", self.level, y); y += 70
        self._blit_pair("LINES", self.lines, y)

        self.display_surface.blit(self.surface, self.rect)
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)
