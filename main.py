import pygame
from random import randint


class GameWindow:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.cell_size = 25
        self.board = [[0] * self.width for _ in range(self.height)].copy()

    def render(self, screen, size):
        screen.fill((0, 0, 0))
        for x in range(self.width):
            for y in range(self.height):
                if self.board[y][x]:
                    cell = pygame.Surface((self.cell_size, self.cell_size))
                    cell.fill(self.board[y][x].get_color())
                    screen.blit(cell, ((size[0] - self.width * self.cell_size) // 2 + x * self.cell_size, 
                                       (size[1] - self.height * self.cell_size) // 2 + y * self.cell_size))
                pygame.draw.rect(screen, (255, 255, 255),
                                  ((size[0] - self.width * self.cell_size) // 2 + x * self.cell_size, 
                                   (size[1] - self.height * self.cell_size) // 2 + y * self.cell_size, self.cell_size, self.cell_size), 1)
    
    def set_ceil(self, x, y, ceil):
        if not self.board[y][x]:
            self.board[y][x] = ceil
            return False
        else:
            screen.fill((0, 0, 0))
            f1 = pygame.font.Font(None, 36)
            text1 = f1.render('Press any button to continue game', True,
                            (0, 180, 0))
            screen.blit(text1, (100, 300))
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    elif event.type == pygame.KEYDOWN:
                        self.board = [[0] * self.width for _ in range(self.height)].copy()
                        running = False
                pygame.display.flip()
            global fig
            fig = Figure(randint(0, 6), (randint(0, 255), randint(0, 255), randint(0, 255)), last_id)
            return True

                

    def kill_ceil(self, x, y):
        self.board[y][x] = 0

    def get_ceil(self, x, y):
        return self.board[y][x]

    def cells_down(self):
        ff = False
        for y in range(self.height - 1, -1, -1):
            for x in range(self.width):
                if not ff and self.board[y][x]:
                    if y == self.height - 1:
                        if (self.board[y][x] and (y == self.height - 1) and not self.board[y][x].get_die()):
                            ff = True
                            self.board[y][x].set_die(self.height, self.width, self.board)
                            break
                    elif (self.board[y][x] and self.board[y + 1][x] and self.board[y + 1][x].get_die() and not self.board[y][x].get_die()):
                        ff = True
                        self.board[y][x].set_die(self.height, self.width, self.board)
                        break
                    


        if not ff:
            for y in range(self.height - 2, -1, -1):
                for x in range(self.width):
                    if self.board[y][x] and not self.board[y][x].get_die():
                        self.board[y][x], self.board[y + 1][x] = self.board[y + 1][x], self.board[y][x]
        
    def get_board(self):
        return self.board
                    
    def move_figure_right(self, id):
        print(id)
        copy_board = self.board.copy()
        for y in range(self.height):
            for x in range(self.width - 1, -1, -1):
                if copy_board[y][x]:
                    print(copy_board[y][x].get_id())
                if (copy_board[y][x] and copy_board[y][x].get_id() == id):
                    self.board[y][x], self.board[y][x + 1] = 0, self.board[y][x]



class Ceil:
    def __init__(self, color, last_id):
        self.color = color
        self.die = False
        self.id_figure = last_id
    
    def get_color(self) -> tuple:
        return self.color
    
    def get_die(self):
        return self.die 
    
    def still_alive(self):
        return self.die
    
    def get_id(self):
        return self.id_figure
    
    def dieing(self):
        self.die = True
    
    def set_die(self, height, width, board):
        for y in range(height - 1, -1, -1):
            for x in range(width):
                if board[y][x]:
                    if board[y][x].get_id() == self.id_figure:
                        board[y][x].dieing()
        global fig
        fig = Figure(randint(0, 6), (randint(0, 255), randint(0, 255), randint(0, 255)), last_id)

class Figure:
    def __init__(self, type, color, id):
        self.types = {0: [[0, 3], [0, 4], [0, 5], [0, 6]], 
                      1: [[0, 3], [0, 4], [0, 5], [1, 3]],
                      2: [[0, 3], [0, 4], [0, 5], [1, 5]],
                      3: [[0, 3], [0, 4], [0, 5], [1, 4]],
                      4: [[1, 4], [0, 4], [0, 5], [1, 5]],
                      5: [[1, 6], [0, 4], [0, 5], [1, 5]],
                      6: [[1, 4], [0, 4], [0, 5], [1, 3]],}
        for i in self.types[type]:
            cel = Ceil(color, id)
            if board.set_ceil(i[1], i[0], cel):
                break
            self.type = type
            self.id = id
            global last_id
            last_id += 1

    def move_right(self, width, height, copy_board):
        can_i_move = True
        for y in range(height):
            for x in range(width):
                if x != width - 1:
                    if (copy_board[y][x] and copy_board[y][x].get_id() == self.id) and (copy_board[y][x + 1] and (copy_board[y][x + 1].get_id() != self.id)):
                        can_i_move = False
                elif copy_board[y][x] and copy_board[y][x].get_id() == self.id:
                    can_i_move = False
        if can_i_move:
            board.move_figure_right(self.id)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Voice Tetris')
    size = width, height = 600, 700
    screen = pygame.display.set_mode(size)

    running = True

    fps = 10
    clock = pygame.time.Clock()

    last_id = 0

    width = 10
    height = 20

    board = GameWindow(width, height)
    
    fig = Figure(randint(0, 6), (randint(0, 255), randint(0, 255), randint(0, 255)), last_id)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    fig.move_right(width, height, board.get_board())
        board.render(screen, size)
        board.cells_down()
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()