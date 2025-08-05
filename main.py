# main.py

from settings import *
from sys import exit

# components
from game import Game

class Main:
    def __init__(self):

        # general
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Tetris")

        # components
        self.game = Game()
        

    def run(self):
        while True:
            # Corrected code
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # Check the event type
                    pygame.quit() # Call the quit function
                    exit()
            
            #display
            self.display_surface.fill(GRAY)

            self.game.run()

            # updating the game
            pygame.display.update()
            self.clock.tick(60)

# Corrected code
if __name__ == '__main__':
    main = Main()
    main.run() # This line starts the game loop