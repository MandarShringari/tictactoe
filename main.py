import pygame
import random
import time 
pygame.init()


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 500


window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")


class Button:
    
    def __init__(self, x, y, width, height, text, font_size=30):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.color = GRAY
        self.text_surface = self.font.render(self.text, True, BLACK)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        surface.blit(self.text_surface, self.text_rect)

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

    def on_click(self, pos):
        return self.is_hovered(pos)


class Board:
    def __init__(self):
        self.window_width = 400
        self.window_height = 500
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Tic-Tac-Toe")
        self.symbol = random.choice(["X", "O"])
        self.x_positions = []
        self.o_positions = []
        self.board = [["_" for _ in range(3)] for _ in range(3)]

        
        try:
            self.x_image = pygame.image.load("/Users/veereshshringari/Documents/Mandar Project /tic tac toe /png-clipart-black-x-mark-tic-tac (1).png").convert_alpha()
            self.o_image = pygame.image.load("/Users/veereshshringari/Documents/Mandar Project /tic tac toe /otic tac.jpg").convert_alpha()
            self.x_image = pygame.transform.scale(self.x_image, (100, 100))
            self.o_image = pygame.transform.scale(self.o_image, (100, 100))
        except pygame.error as e:
            print(f"Error loading images: {e}")
            self.x_image = pygame.Surface((100, 100))
            self.o_image = pygame.Surface((100, 100))
            self.x_image.fill((255, 0, 0))
            self.o_image.fill((0, 255, 0))

    def draw(self):
        horizontal_offset = 50
        vertical_offset = 100

       
        pygame.draw.line(self.window, (0, 0, 0), [150, vertical_offset], [150, self.window_height - vertical_offset], 5)
        pygame.draw.line(self.window, (0, 0, 0), [250, vertical_offset], [250, self.window_height - vertical_offset], 5)


        pygame.draw.line(self.window, (0, 0, 0), [horizontal_offset, 200], [self.window_width - horizontal_offset, 200], 5)
        pygame.draw.line(self.window, (0, 0, 0), [horizontal_offset, 300], [self.window_width - horizontal_offset, 300], 5)

    def click(self, x, y):
        row, col = (y - 100) // 100, (x - 50) // 100
        if 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == "_":
            self.board[row][col] = self.symbol
            pos = (col * 100 + 50, row * 100 + 100)
            if self.symbol == "X":
                self.x_positions.append(pos)
                self.symbol = "O"
            else:
                self.o_positions.append(pos)
                self.symbol = "X"

    def ai_move(self, row, col):
        if self.board[row][col] == "_":
            self.board[row][col] = "O"
            pos = (col * 100 + 50, row * 100 + 100)
            self.o_positions.append(pos)
            self.symbol = "X"

    def draw_symbols(self):
        for pos in self.x_positions:
            self.window.blit(self.x_image, pos)
        for pos in self.o_positions:
            self.window.blit(self.o_image, pos)
    
    def highlight_winning_line(self, line):
        if line:
            pygame.draw.line(
                self.window, (255, 0, 0),
                line[0], line[1], 10
            )

    def check_winner(self):
        
        winning_positions = []

        for i in range(3):
            
            if self.board[i][0] == self.board[i][1] == self.board[i][2] and self.board[i][0] != "_":
                winning_positions = [
                    (50, 150 + i * 100), (350, 150 + i * 100)
                ]
                return self.board[i][0], winning_positions
      
            if self.board[0][i] == self.board[1][i] == self.board[2][i] and self.board[0][i] != "_":
                winning_positions = [
                    (100 + i * 100, 100), (100 + i * 100, 400)
                ]
                return self.board[0][i], winning_positions


        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != "_":
            winning_positions = [(50, 100), (350, 400)]
            return self.board[0][0], winning_positions
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != "_":
            winning_positions = [(350, 100), (50, 400)]
            return self.board[0][2], winning_positions


        if not any("_" in row for row in self.board):
            return "Draw", []

        return None, []


class AI:
    def __init__(self, board):
        self.board = board

    def is_moves_left(self):
        return any('_' in row for row in self.board)

    def evaluate(self):
        for row in self.board:
            if row[0] == row[1] == row[2] and row[0] != '_':
                return 10 if row[0] == 'O' else -10

        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] != '_':
                return 10 if self.board[0][col] == 'O' else -10

        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != '_':
            return 10 if self.board[0][0] == 'O' else -10

        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != '_':
            return 10 if self.board[0][2] == 'O' else -10

        return 0

    def minimax(self, depth, is_max):
        score = self.evaluate()
        if score == 10 or score == -10:
            return score
        if not self.is_moves_left():
            return 0

        if is_max:
            best = -1000
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == '_':
                        self.board[row][col] = 'O'
                        best = max(best, self.minimax(depth + 1, False))
                        self.board[row][col] = '_'
            return best
        else:
            best = 1000
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == '_':
                        self.board[row][col] = 'X'
                        best = min(best, self.minimax(depth + 1, True))
                        self.board[row][col] = '_'
            return best

    def find_best_move(self):
        best_val = -1000
        best_move = (-1, -1)

        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '_':
                    self.board[row][col] = 'O'
                    move_val = self.minimax(0, False)
                    self.board[row][col] = '_'

                    if move_val > best_val:
                        best_val = move_val
                        best_move = (row, col)
        return best_move


class EasyAI:
    def __init__(self, board):
        self.board = board

    def find_random_move(self):
        empty_cells = [(row, col) for row in range(3) for col in range(3) if self.board[row][col] == '_']
        return random.choice(empty_cells) if empty_cells else (-1, -1)

class MediumAI:
    def __init__(self, board):
        self.board = board

    def is_moves_left(self):
        return any('_' in row for row in self.board)

    def evaluate(self):
        for row in self.board:
            if row[0] == row[1] == row[2] and row[0] != '_':
                return 10 if row[0] == 'O' else -10

        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] != '_':
                return 10 if self.board[0][col] == 'O' else -10

        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != '_':
            return 10 if self.board[0][0] == 'O' else -10

        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != '_':
            return 10 if self.board[0][2] == 'O' else -10

        return 0

    def find_winning_move(self, symbol):
     
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '_':
                    self.board[row][col] = symbol
                    if self.evaluate() == (10 if symbol == 'O' else -10):
                        self.board[row][col] = '_'
                        return row, col
                    self.board[row][col] = '_'
        return None

    def find_best_move(self):

        winning_move = self.find_winning_move('O')
        if winning_move:
            return winning_move


        blocking_move = self.find_winning_move('X')
        if blocking_move:
            return blocking_move


        empty_cells = [(row, col) for row in range(3) for col in range(3) if self.board[row][col] == '_']
        return random.choice(empty_cells) if empty_cells else (-1, -1)





def show_start_screen():
    
    start_button = Button(100, 200, 200, 50, "Start Game")
    quit_button = Button(100, 300, 200, 50, "Quit Game")

    menu_running = True
    while menu_running:
        window.fill(WHITE)
        font = pygame.font.Font(None, 50)
        title_surface = font.render("Tic-Tac-Toe", True, BLACK)
        window.blit(title_surface, (100, 100))

        start_button.draw(window)
        quit_button.draw(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if start_button.on_click(pos):
                    menu_running = False
                if quit_button.on_click(pos):
                    pygame.quit()
                    exit()

        pygame.display.flip()


def graphical_difficulty_menu():
    
    easy_button = Button(100, 200, 200, 50, "Easy")
    medium_button = Button(100, 300, 200, 50, "Medium")
    hard_button = Button(100, 400, 200, 50, "Hard")

    menu_running = True
    selected_difficulty = "1"

    while menu_running:
        window.fill(WHITE)
        font = pygame.font.Font(None, 40)
        title_surface = font.render("Select Difficulty", True, BLACK)
        window.blit(title_surface, (100, 100))

        easy_button.draw(window)
        medium_button.draw(window)
        hard_button.draw(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if easy_button.on_click(pos):
                    selected_difficulty = "1"
                    menu_running = False
                if medium_button.on_click(pos):
                    selected_difficulty = "2"
                    menu_running = False
                if hard_button.on_click(pos):
                    selected_difficulty = "3"
                    menu_running = False

        pygame.display.flip()

    return selected_difficulty

def show_winner_screen(winner):
    
    winner_text = f"Winner: {winner}" if winner != "Draw" else "It's a Draw!"
    restart_button = Button(100, 200, 200, 50, "Restart")
    quit_button = Button(100, 300, 200, 50, "Quit")

    screen_running = True
    while screen_running:
        window.fill(WHITE)
        font = pygame.font.Font(None, 50)
        title_surface = font.render(winner_text, True, BLACK)
        window.blit(title_surface, (100, 100))

        restart_button.draw(window)
        quit_button.draw(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if restart_button.on_click(pos):
                    screen_running = False  # Exit to restart the game
                if quit_button.on_click(pos):
                    pygame.quit()
                    exit()

        pygame.display.flip()


def main():
    while True:
        show_start_screen()

        game = Board()
        difficulty = graphical_difficulty_menu()

        if difficulty == "1":
            ai = EasyAI(game.board)
        elif difficulty == "2":
            ai = MediumAI(game.board)
        else:
            ai = AI(game.board)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and game.symbol == "X":
                    x, y = pygame.mouse.get_pos()
                    game.click(x, y)

            if game.symbol == "O":
                time.sleep(1)  
                if difficulty == "1":
                    ai_move = ai.find_random_move()
                elif difficulty == "2":
                    ai_move = ai.find_best_move()
                else:
                    ai_move = ai.find_best_move()
                if ai_move != (-1, -1):
                    game.ai_move(ai_move[0], ai_move[1])

            winner, winning_positions = game.check_winner()
            if winner:
                game.highlight_winning_line(winning_positions)
                pygame.display.flip()
                time.sleep(3)  
                running = False  

            window.fill(WHITE)
            game.draw()
            game.draw_symbols()
            pygame.display.flip()

        show_winner_screen(winner)

    pygame.quit()

if __name__ == "__main__":
    main()
