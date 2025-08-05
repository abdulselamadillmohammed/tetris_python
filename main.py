from setting import *
from sys import exit

class Main:
    def __init__(self):

        # general
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame
        pygame.display.set_caption("Tetris")

    def run(self):
        while True:
            for event in pygame.event.get(): # Key board reading for function
                for event in pygame.event.GUIT:
                    pygame.quit
                    exit()
            
            #display
            self.display_surface.fill(GRAY)
            pygame.display.update()
if __name__ == '__main__':
    main = Main()