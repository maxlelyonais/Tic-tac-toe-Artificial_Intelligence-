import pygame
import math
import os
import button

# pygame setup
pygame.init()

## Set up display
width,height = 1280, 1280
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tic-tac-toe")

## Mode
## Mode 1 = playing against player and Mode 2 = playing against machine
mode = 1

## Players turns
## 2 = player 1, 1 = machine, player
turn = 2

FILE_NAMES = ["Choose_Mode.png","vs_Machine.png","vs_Player.png"]
## Route for images and creation of buttons
current_path = os.getcwd()

for i in FILE_NAMES:
    path = os.path.join(current_path,"Images",i)
    
    images = pygame.image.load(path).convert_alpha()
    if i == "Choose_Mode.png":
        Mode_button = button.Button(500,500,images,1)
    elif i == "vs_Machine.png":
        Machine_button = button.Button(500,600,images,1)
    elif i == "vs_Player.png":
        Player_button = button.Button(500,700,images,1)

## To create a Menu for the small game

font = pygame.font.SysFont("arial",100)
TEXT_COL = (0,0,0)
menu = True
winner = False
tie = False

def draw_text(text,font,text_col,x,y):
    img = font.render(text,True,text_col)
    screen.blit(img,(x,y))

## Min-max alghorithm
def min_max(grid,alfa,beta,maximizing_player):
    score = evaluate(grid)
    if score is not None:
        return score
    if maximizing_player:
        max_eval = -math.inf
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == 0:
                    grid[i][j] = 1
                    eval = min_max(grid,alfa,beta,False)
                    grid[i][j] = 0
                    max_eval = max(max_eval,eval)
                    alfa = max(alfa,eval)
                    if beta <= alfa:
                        break
        return max_eval
    else:
        min_eval = math.inf
        for i in range(3):
            for j in range(3):
                if grid[i][j] == 0:
                    grid[i][j] = 2
                    eval = min_max(grid,alfa,beta, True)
                    grid[i][j] = 0
                    min_eval = min(min_eval, eval)
                    beta = min(beta,eval)
                    if beta <= alfa:
                        break
        return min_eval

## Check grid
def is_grid_full(grid,empty_cell):
    return all(cell != empty_cell for row in grid for cell in row)

def Winner(grid,playerTurn):

    ## Check horizontaly
    for row in grid:
        if all(element == playerTurn for element in row):
            return True
    ## Check vertically
    for col in range(len(grid)):
        if all(grid[row][col] == playerTurn for row in range(len(grid[col]))):
            return True
    ## Check diagonally
    if all(grid[i][i] == playerTurn for i in range(len(grid))):
        return True
    ## Check contradiagonally
    if all(grid[i][len(grid) - i -1] == playerTurn for i in range(len(grid)) ):
        return True
        
    return False

def PlayerPlay(secX,secY,playerTurn):
    grid[secX][secY] = playerTurn

## Evaluate if there is a winner
def evaluate(board):
    if Winner(board, 1):
        return 1
    elif Winner(board, 2):
        return -1
    elif is_grid_full(board,0):
        return 0
    else:
        return None


## Obtain the best movement
def get_best_movement(grid):

    bestMovement = (-1,-1)
    minimo = -math.inf
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 0:
                grid[i][j] = 1
                value = min_max(grid,-math.inf,math.inf,False)
                grid[i][j] = 0
                if value > minimo:
                    minimo = value
                    bestMovement = (i,j)

    return bestMovement


## Define colors
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
blue = (0,0,255)
light_blue = (173,216,230)
## Define grid parameters
grid_size = 3
grid_width = width // grid_size
grid_height = height // grid_size

## Define grid as a list
grid = [[0] * grid_size for _ in range(grid_size)]
def create_grid(screen,grid,g_w,g_h):
    ## drawing the grid and its values
    for i in range(grid_size):
        for j in range(grid_size):

            pygame.draw.rect(screen,black,pygame.Rect( j * grid_width, i * grid_height , grid_width, grid_height ), 2)
            font = pygame.font.Font(None,100)
            text = font.render(str(grid[i][j]),True,black)
            text_rect = text.get_rect(center =(j * g_w + g_w // 2, i * g_h + g_h // 2))
            screen.blit(text,text_rect)

## For playing the game

clock = pygame.time.Clock() 
running = True

while running:

    # fill the screen with a color to wipe away anything from last frame
    if menu == True:
        screen.fill(light_blue)
        draw_text("Main Menu",font,TEXT_COL,425,400)
        Mode_button.draw(screen)
        if Machine_button.draw(screen):
            mode = 2
            turn = 2
            menu = False
        if Player_button.draw(screen):
            mode = 1
            turn = 1
            menu = False
    else:
        pass

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif pygame.mouse.get_pressed()[0]:

            PosX = pygame.mouse.get_pos()[1] // (grid_width)
            PosY = pygame.mouse.get_pos()[0] // (grid_height)
            if menu == False:
                if grid[PosX][PosY] is 0:
                    if turn is 2:
                        PlayerPlay(PosX,PosY,turn)
                        if (Winner(grid,turn)):
                            winner = True
                            running = False
                        if is_grid_full(grid,0):
                            tie = True
                            running = False
                        if winner == False:
                            turn = 1
                    elif turn is 1 and mode is 1:
                        PlayerPlay(PosX,PosY,turn)
                        if (Winner(grid,turn)):
                            winner = True
                            running = False
                        if is_grid_full(grid,0):
                            tie = True
                            running = False
                        if winner == False:
                            turn = 2
    
    # RENDER YOUR GAME HERE
    if menu == False:
        screen.fill(white)
        create_grid(screen,grid,grid_width, grid_height)
        if turn is 1 and mode is 2 and not(is_grid_full(grid,0)): 
            bestMovement = get_best_movement(grid)
            grid[bestMovement[0]][bestMovement[1]] = 1
            if Winner(grid,turn):
                winner = True
                running = False
            if is_grid_full(grid,0):
                tie = True
                running = False
            if winner == False:
                turn = 2
        
    # flip() the display to put your work on screen
    pygame.display.flip()

if winner or tie:
    screen.fill(white)
    font = pygame.font.Font(None,100)
    if winner:
        text = font.render(f"{turn} is the winner" ,True,black)
    else:
        text = font.render(f"Tie of the game" ,True,black)
    text_rect = text.get_rect(center =(width // 2, height// 2))
    screen.blit(text,text_rect)
    pygame.display.flip()
    pygame.time.delay(2000)


pygame.quit()