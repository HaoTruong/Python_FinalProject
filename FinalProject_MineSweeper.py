"""
 Example program to show using an array to back a grid on-screen.
 
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
 Explanation video: http://youtu.be/mdTeqiWyFnc
"""
import pygame, random, time, sys




# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 20
HEIGHT = 20
# This sets the margin between each cell
MARGIN = 5
numGrid = 10
#Number of mines is 15% of number of grid
mineNum = (15/100)*(numGrid**2)

# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = []
opened = []
flagged = []
for row in range(numGrid):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    opened.append([])
    flagged.append([])
    for column in range(numGrid):
        grid[row].append(0)  # Append a cell
        opened[row].append(0)
        flagged[row].append(0)
#Random mine
count = 0
while (count < mineNum):
    i = random.randrange(numGrid)
    j = random.randrange(numGrid)
    if (grid[i][j] != 10):
        count += 1
        grid[i][j] = 10
        opened[i][j] = 1
#Setting number of mines around free squares
def countSurrounding():
    global grid, numGrid
    for row in range(numGrid):
        for column in range(numGrid):
            if grid[row][column] != 10:
                mineCount = 0
                i = -1
                while i < 2:
                    j =-1
                    while j < 2:
                        if (i+row >= 0 and i+row <= numGrid-1 and j+column >= 0 and j+column <= numGrid-1):
                            if (grid[row+i][column+j] == 10):
                                mineCount +=1
                        j += 1
                    i += 1
                grid[row][column] = mineCount

 
# Initialize pygame
pygame.init()
 
# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [500, 500]
winSize = 500
screen = pygame.display.set_mode(WINDOW_SIZE)
 
# Set title of screen
pygame.display.set_caption("Array Backed Grid")

#Game over message
def game_over():
    my_font = pygame.font.SysFont('times new roman',50)
    result = "Game over!"
    game_over_surf = my_font.render(result, True, RED)
    game_over_rect = game_over_surf.get_rect()
    game_over_rect.midtop = (winSize /2 , winSize /2)
    screen.fill(WHITE)
    screen.blit(game_over_surf, game_over_rect)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit(0) 

def game_won():
    my_font = pygame.font.SysFont('times new roman',50)
    result = "You won!"
    game_over_surf = my_font.render(result, True, RED)
    game_over_rect = game_over_surf.get_rect()
    game_over_rect.midtop = (winSize /2 , winSize /2)
    screen.fill(WHITE)
    screen.blit(game_over_surf, game_over_rect)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit(0)

done = False
def reveal(row, col,flagged):
    global grid, opened
    if (flagged[row][col] != 0):
        pygame.draw.rect(screen, WHITE,[(MARGIN + WIDTH) * col + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])
    screen.blit(digit_text[grid[row][col]],[(MARGIN + WIDTH) * col + MARGIN,
                                    (MARGIN + HEIGHT) * row + MARGIN,
                                    WIDTH,
                                    HEIGHT])
    opened[row][col] = 1
   
    if (grid[row][col] == 0 ):
        i = -1
        while i < 2:
            j =-1
            while j < 2:
                if (i != 0 or j != 0):
                    if (i+row >= 0 and i+row <= numGrid-1 and j+col >= 0 and j+col <= numGrid-1):
                        if (opened[row+i][col+j] == 0):
                            reveal(row+i, col+j, flagged)
                j += 1
            i += 1

    

    
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
font = pygame.font.SysFont('times new roman',20)
text1 = font.render('1', True, BLACK)
text2 = font.render('2', True, BLACK)
text3 = font.render('3', True, BLACK)
text4 = font.render('4', True, BLACK)
text5 = font.render('5', True, BLACK)
text6 = font.render('6', True, BLACK)
text7 = font.render('7', True, BLACK)
text8 = font.render('8', True, BLACK)
text0 = font.render('0', True, BLACK)
textF = font.render('F', True, BLACK)
rect1 = text1.get_rect()
rect2 = text2.get_rect()
rect3 = text3.get_rect()
rect4 = text4.get_rect()
rect5 = text5.get_rect()
rect6 = text6.get_rect()
rect7 = text7.get_rect()
rect8 = text8.get_rect() 
digit_text = {1:text1, 2:text2, 3:text3, 4:text4,
                 5:text5, 6:text6, 7:text7, 8:text8, 0:text0}
# -------- Main Program Loop -----------
# Set the screen background
screen.fill(BLACK)
# Draw the grid:
for row in range(numGrid):
    for column in range(numGrid):
        color = WHITE
        '''
        if (grid[row][column] == 10):
            color = RED
        '''
        pygame.draw.rect(screen, color,[(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])
first = True
wincond = 0
countSurrounding()
# Loop until the user clicks the close button.
while not done:
    #check win condition
    if (wincond == mineNum):
        done = True
       
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to grid coordinates
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            if (event.button == 1):
                if (first):
                    if grid[row][column] == 10:
                        mineNum -= 1
                    grid[row][column] = 0
                    first = False
                    countSurrounding()
                if (grid[row][column] == 10):
                    game_over()
                elif (grid[row][column] != 0):
                    screen.blit(digit_text[grid[row][column]],[(MARGIN + WIDTH) * column + MARGIN,
                                    (MARGIN + HEIGHT) * row + MARGIN,
                                    WIDTH,
                                    HEIGHT])
                else:
                    reveal(row, column, flagged)
            elif (event.button == 3):
                if flagged[row][column] == 0:
                    if (grid[row][column] == 10):
                        wincond += 1
                        grid[row][column] = 11
                        pygame.draw.rect(screen, WHITE,[(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])
                        screen.blit(textF,[(MARGIN + WIDTH) * column + MARGIN,
                                        (MARGIN + HEIGHT) * row + MARGIN,
                                        WIDTH,
                                        HEIGHT])
                    elif grid[row][column] == 11:
                        wincond -= 1
                        grid[row][column] = 10
                        pygame.draw.rect(screen, WHITE,[(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])
                    else:
                        screen.blit(textF,[(MARGIN + WIDTH) * column + MARGIN,
                                        (MARGIN + HEIGHT) * row + MARGIN,
                                        WIDTH,
                                        HEIGHT])
                    flagged[row][column] = 1
                else:
                    flagged[row][column] = 0
                    pygame.draw.rect(screen, WHITE,[(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])
    # Limit to 60 frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
game_won()
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()