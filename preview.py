from settings import *
import pygame
from pygame.image import load
from pygame import transform
from pathlib import Path

class Preview:
    SLOTS = 3
    PAD = 8

    def __init__(self):
        # general
        self.display_surface = pygame.display.get_surface()
        self.surface = pygame.Surface((SIDEBAR_WIDTH, int(GAME_HEIGHT * PREVIEW_HEIGHT_FRACTION)))
        self.rect = self.surface.get_rect(topright=(WINDOW_WIDTH - PADDING, PADDING))

        # assets dir (robust)
        gfx_dir = Path(__file__).resolve().parent / "assets" / "graphics"

        # images (after set_mode, so convert_alpha() is OK)
        self.shape_surfaces = {
            shape: load(str(gfx_dir / f"{shape}.png")).convert_alpha()
            for shape in TETROMINOS.keys()
        }

        # layout
        self.slot_h = self.surface.get_height() / self.SLOTS
        self.max_h = self.slot_h - 2 * self.PAD
        self.max_w = self.surface.get_width() - 2 * self.PAD

    def display_pieces(self, shapes):
        # show up to SLOTS shapes, vertically stacked and centered
        for i, shape in enumerate(shapes[:self.SLOTS]):
            surf = self.shape_surfaces[shape]

            # scale to fit (keep aspect), but never upscale
            scale = min(self.max_w / surf.get_width(), self.max_h / surf.get_height(), 1.0)
            if scale < 1.0:
                new_size = (int(surf.get_width() * scale), int(surf.get_height() * scale))
                surf = transform.smoothscale(surf, new_size)

            cx = self.surface.get_width() // 2
            cy = int((i + 0.5) * self.slot_h)
            rect = surf.get_rect(center=(cx, cy))
            self.surface.blit(surf, rect)

    def run(self, next_shapes):
        self.surface.fill(GRAY)
        self.display_pieces(next_shapes)
        self.display_surface.blit(self.surface, self.rect)
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)
