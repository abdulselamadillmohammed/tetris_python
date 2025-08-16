# preview.py

from settings import *
from pygame.image import load
from os import path

class Preview:
    def __init__(self):

        # genral
        self.display_surface = pygame.display.get_surface()
        self.surface = pygame.Surface((SIDEBAR_WIDTH, GAME_HEIGHT * PREVIEW_HEIGHT_FRACTION))
        self.rect = self.surface.get_rect(topright= (WINDOW_WIDTH - PADDING, PADDING))


        # shapes 
        self.shape_surfaces = {
            shape: load(path.join('assets','graphics', f'{shape}.png')).convert_alpha()
            for shape in TETROMINOS.keys()
        }
    def display_pieces(self, shapes):
        for shape in shapes:
            shape_surface = self.shape_surfaces[shape]
            self.surface.blit(shape_surface, (0,0))
    

    def run(self, next_shapes):
        self.surface.fill(GRAY)
        self.display_pieces(next_shapes)
        self.display_surface.blit(self.surface, self.rect)
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2,2)