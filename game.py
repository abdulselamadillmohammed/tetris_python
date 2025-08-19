# game.py
from settings import *
from random import choice
from timer import Timer
import pygame

class Game:
    def __init__(self, get_next_shape, on_score_update):

        
        # general
        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft=(PADDING, PADDING))
        self.sprites = pygame.sprite.Group()

        # game connected
        self.get_next_shape = get_next_shape
        self.on_score_update = on_score_update


        # lines
        self.line_surface = self.surface.copy()
        self.line_surface.fill((0, 255, 0))
        self.line_surface.set_colorkey((0, 255, 0))
        self.line_surface.set_alpha(120)

        # 2D grid: ROWS x COLUMNS (falsy until a block is placed)
        self.field_data = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]

        # tetromino
        self.tetromino = Tetromino(
            self.get_next_shape(),  # was: choice(list(TETROMINOS.keys()))
            self.sprites,
            self.create_new_tetromino,
            self.field_data
        )


        self.down_speed = UPDATE_START_SPEED
        self.down_speed_faster = self.down_speed * 0.3
        self.down_pressed = False
        
        self.timers = {
            'vertical move': Timer(UPDATE_START_SPEED, True, self.move_down),
            'horizontal move': Timer(MOVE_WAIT_TIME),
            'rotate': Timer(ROTATE_WAIT_TIME)
        }

        self.timers['vertical move'].activate()

        # score
        self.current_level = 1
        self.current_score = 0
        self.current_lines = 0

        if self.on_score_update:
            self.on_score_update(self.current_lines, self.current_score, self.current_level)


    def calculate_score(self, num_lines):
        if num_lines <= 0:
            return
        self.current_lines += num_lines
        self.current_score += SCORE_DATA[num_lines] * self.current_level

        # level up every 10 lines total
        if self.current_lines // 10 >= self.current_level:
            self.current_level += 1
            self.down_speed *= 0.75
            self.down_speed_faster = self.down_speed * 0.3
            self.timers['vertical move'].duration = self.down_speed

        if self.on_score_update:
            self.on_score_update(self.current_lines, self.current_score, self.current_level)  # was self.update_score(...)

    def create_new_tetromino(self):
        self.check_finished_rows()

        self.tetromino = Tetromino(

            self.get_next_shape(),
            self.sprites,
            self.create_new_tetromino,
            self.field_data
        )

    def timer_update(self):
        for timer in self.timers.values():
            timer.update()

    def move_down(self):
        self.tetromino.move_down()

    def draw_grid(self):
        for col in range(1, COLUMNS):
            x = col * CELL_SIZE
            pygame.draw.line(self.surface, LINE_COLOR, (x, 0), (x, self.surface.get_height()), 1)

        for row in range(1, ROWS):
            y = row * CELL_SIZE
            pygame.draw.line(self.surface, LINE_COLOR, (0, y), (self.surface.get_width(), y))

        self.surface.blit(self.line_surface, (0, 0))

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.timers['horizontal move'].active:
            if keys[pygame.K_LEFT]:
                self.tetromino.move_horizontal(-1)
                self.timers['horizontal move'].activate()
            if keys[pygame.K_RIGHT]:
                self.tetromino.move_horizontal(1)
                self.timers['horizontal move'].activate()

        # check for rotation
        if not self.timers['rotate'].active:
            if keys[pygame.K_UP]:
                self.tetromino.rotate()
                self.timers['rotate'].activate()

        # down speedup
        if not self.down_pressed and keys[pygame.K_DOWN]:
            self.down_pressed = True
            self.timers['vertical move'].duration = self.down_speed_faster

        if self.down_pressed and not keys[pygame.K_DOWN]:
            self.down_pressed = False
            self.timers['vertical move'].duration = self.down_speed

    def check_finished_rows(self):
        # get the full row indexes
        delete_rows = []
        for i, row in enumerate(self.field_data):
            if all(row):
                delete_rows.append(i)

        if delete_rows:
            for delete_row in delete_rows:
                # delete all blocks in that row
                for block in self.field_data[delete_row]:
                    if block:  # make sure it's not 0
                        block.kill()

            # move blocks down
            for row_index in range(max(delete_rows) - 1, -1, -1):
                for block in self.field_data[row_index]:
                    if block:
                        block.pos.y += sum(1 for dr in delete_rows if dr > row_index)

            # rebuild the field_data grid
            self.field_data = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
            for block in self.sprites:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block

            self.calculate_score(len(delete_rows))

    def run(self):
        self.input()

        # update
        self.timer_update()
        self.sprites.update()

        self.surface.fill(GRAY)
        self.sprites.draw(self.surface)

        self.draw_grid()
        self.display_surface.blit(self.surface, (PADDING, PADDING))
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)

class Tetromino:
    def __init__(self, shape, group, create_new_tetromino, field_data):
        self.shape = shape
        # setup
        self.block_positions = TETROMINOS[shape]['shape']
        self.color = TETROMINOS[shape]['color']
        self.create_new_tetromino = create_new_tetromino
        self.field_data = field_data

        # create blocks
        self.blocks = [Block(group, pos, self.color) for pos in self.block_positions]

    # collisions
    def next_move_horizontal_collide(self, blocks, amount):
        collision_list = [block.horizontal_collide(int(block.pos.x + amount), self.field_data) for block in self.blocks]
        return True if any(collision_list) else False

    def next_move_vertical_collide(self, blocks, amount):
        collision_list = [block.vertical_collide(int(block.pos.y + amount), self.field_data) for block in self.blocks]
        return True if any(collision_list) else False

    def move_horizontal(self, amount):
        if not self.next_move_horizontal_collide(self.blocks, amount):
            for block in self.blocks:
                block.pos.x += amount

    def move_down(self):
        if not self.next_move_vertical_collide(self.blocks, 1):
            for block in self.blocks:
                block.pos.y += 1
        else:
            # landed → lock into grid
            for block in self.blocks:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block
            self.create_new_tetromino()

            for row in self.field_data:
                print(row)

    def rotate(self):
        if self.shape != 'O':

            # 1. pivot point 
            pivot_pos = self.blocks[0].pos

            # 2. new block positions
            new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]

            # 3. collision check
            for pos in new_block_positions:
                # horizontal 
                if pos.x < 0 or pos.x >= COLUMNS:
                    return 
                
                # field check -> collision with other pieces
                if self.field_data[int(pos.y)][int(pos.x)]:
                    return

                # verical / floor check
                if pos.y >= ROWS:
                    return


            # 4. Implement new positions     
            for i, block in enumerate(self.blocks):
                block.pos = new_block_positions[i]


class Block(pygame.sprite.Sprite):
    def __init__(self, group, pos, color):
        super().__init__(group)
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(color)

        # position
        self.pos = pygame.Vector2(pos) + BLOCK_OFFSET
        self.rect = self.image.get_rect(topleft=self.pos * CELL_SIZE)

    def rotate(self, pivot_pos):
        # distance = self.pos - pivot_pos
        # rotated = distance.rotate(90)
        # new_pos = pivot_pos + rotated
        # return new_pos

        return pivot_pos + (self.pos - pivot_pos).rotate(90)
    
    def horizontal_collide(self, x, field_data):
        if not 0 <= x < COLUMNS:
            return True
        if field_data[int(self.pos.y)][x]:
            return True
        return False

    def vertical_collide(self, y, field_data):
        if y >= ROWS:
            return True
        if y >= 0 and field_data[y][int(self.pos.x)]:
            return True
        return False

    def update(self):
        self.rect.topleft = self.pos * CELL_SIZE

    def __str__(self):
        return "hello"
