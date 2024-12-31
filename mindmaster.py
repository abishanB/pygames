import pygame, math, random

#initialize pygame and font
pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)
MyClock = pygame.time.Clock() #Create a clock to restrict framerate
# Set up the drawing window
WIDTH = 500
HEIGHT = 700
screen = pygame.display.set_mode([500, 800])

#preset colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
BROWN = (156, 102, 31)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)
ORANGE = (255, 140, 0)
BLANK = (230, 232, 211)

#bottom colors properties
colorCircleRadius = 12
colorsX = 65
colorsY = 650
colorsXSpacing = 45

colors = [BLACK, BLUE, BROWN, RED, GREEN, PURPLE, YELLOW, ORANGE]


def createRandomCode():#generate random 4 color code, no duplicates
  colorsCopy = colors.copy()
  random.shuffle(colorsCopy)
  return colorsCopy[:4]


def drawColors(screen):#draw colors at the bottom
  for color in range(len(colors)):
    pygame.draw.circle(screen, colors[color], (colorsX + (colorsXSpacing * color), colorsY), colorCircleRadius)

def drawBoard(screen):
  circleRadius = 16
  firstRowX = 100
  firstRowY = 580
  xSpacing = 60
  ySpacing = 55

  for row in range(10):#draw holding cells for colors
    for colorSpace in range(4):
        pygame.draw.circle(screen, BLANK,(firstRowX + (xSpacing * colorSpace), firstRowY - (ySpacing * row)), circleRadius)

  circleRadius = 5
  firstRowX = 310
  firstRowY = 585
  xSpacing = 60
  ySpacing = 55
  color = (255, 255, 255)
  for row in range(10):#output result cells
    pygame.draw.circle(screen, color,
                       (firstRowX, firstRowY - (ySpacing * row)),
                       circleRadius)
    pygame.draw.circle(screen, color,
                       (firstRowX, firstRowY - (ySpacing * row) - 13),
                       circleRadius)

    pygame.draw.circle(screen, color,
                       (firstRowX + 13, firstRowY - (ySpacing * row)),
                       circleRadius)
    pygame.draw.circle(screen, color,
                       (firstRowX + 13, firstRowY - (ySpacing * row) - 13),
                       circleRadius)

  pygame.draw.line(screen, BLACK, (60, 62), (350, 62), 2)
  
  text_surface = my_font.render('Check', False, (0, 0, 0))#check button
  checkButtonRect = screen.blit(text_surface, (75, 685))

  text_surface1 = my_font.render('Del', False, (0, 0, 0))#Del button
  delButtonRect = screen.blit(text_surface1, (275, 685))
  
  return checkButtonRect, delButtonRect


def colorPress(screen, x, y):#check which color was pressed
  for color in range(8):
    sqx = (x - (65 + (colorsXSpacing * color)))**2
    sqy = (y - 650)**2

    if math.sqrt(sqx + sqy) < colorCircleRadius:
      return colors[color]
		
def updateColors(screen, colorsGuess, count):#redraw colors after color press or delete
  circleRadius = 16
  firstRowX = 100
  firstRowY = 580
  xSpacing = 60
  ySpacing = 55

  for color in range(4):
    pygame.draw.circle(screen, colorsGuess[color],(firstRowX + (xSpacing * color), firstRowY -(ySpacing * count)), circleRadius)

  pygame.display.flip()#update display
    

def updateSideColors(guessAccuracy, count):#update output colors after a guess
  circleRadius = 5
  firstRowX = 310
  firstRowY = 585
  ySpacing = 55

  pygame.draw.circle(screen, guessAccuracy[0],
                     (firstRowX, firstRowY - (ySpacing * count)),
                     circleRadius)
  pygame.draw.circle(screen, guessAccuracy[1],
                     (firstRowX, firstRowY - (ySpacing * count) - 13),
                     circleRadius)

  pygame.draw.circle(screen, guessAccuracy[2],
                     (firstRowX + 13, firstRowY - (ySpacing * count)),
                     circleRadius)
  pygame.draw.circle(screen, guessAccuracy[3],
                     (firstRowX + 13, firstRowY - (ySpacing * count) - 13),
                     circleRadius)

def checkCode(guess):#check  code
  if guess == CODE:
    return [GREEN, GREEN, GREEN, GREEN]
  data = []#returns information of guess accuracy in rgb values
  correctColors = []
  for color in range(4):#check if color is in correct positon
    if guess[color] == CODE[color]:
      data.append(GREEN)
      correctColors.append(guess[color])

  for color in range(4):
    if guess[color] in correctColors:#dont check color if already recorded
      continue
    if guess[color] in CODE:#check if color is in code
      correctColors.append(guess[color])
      data.append(BLACK)

  while len(data) < 4:#fill remaining data with blank spaces
    data.append(WHITE)
  return data

def gameEnd(screen, gameWon):#draw correct code at the top when game is over
  circleRadius = 16
  firstRowX = 100
  firstRowY = 580
  xSpacing = 60
  ySpacing = 55
  
  for color in range(4):
    pygame.draw.circle(screen, CODE[color],(firstRowX + (xSpacing * color), firstRowY -(ySpacing * 10)), circleRadius)

  if gameWon:
    txt = my_font.render('WINNER', False, (0, 255, 0))
  else:
    txt = my_font.render('Loser', False, (255, 0, 0))
  screen.blit(txt, (160, 725))

run = True
setup = False
count = 0
currentGuess = [BLANK, BLANK, BLANK, BLANK]
CODE = createRandomCode()
print(CODE)
while run:
  if setup is False:#setup background and board
    screen.fill((158, 158, 158))#fill screen with gray
    pygame.display.set_caption('Mindmaster')
    checkButtonRect, delButtonRect = drawBoard(screen)
    drawColors(screen)
    setup = True

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
        run = False
    #mouseCLICK
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:#if left mouse click
      x, y = pygame.mouse.get_pos()#coordinates of click
      if checkButtonRect.collidepoint((x, y)):#check button clicked
        if currentGuess[-1] != BLANK:#check if code is filled
          guessAccuracy = checkCode(currentGuess)
          updateSideColors(guessAccuracy, count)
          if guessAccuracy == [GREEN, GREEN, GREEN, GREEN]:#Correct Code
            print("WINNER")
            gameEnd(screen, True)
            run = False
          if guessAccuracy != [GREEN, GREEN, GREEN, GREEN] and count == 9:#game lost
            print("Loser")
            gameEnd(screen, False)
            run = False
          count += 1
          currentGuess = [BLANK, BLANK, BLANK, BLANK]
          
      if delButtonRect.collidepoint((x, y)):#delete button, removes last color in code
        if currentGuess[-1] != BLANK:
          currentGuess[-1] = BLANK
          updateColors(screen,currentGuess, count)
          break
        for color in currentGuess:
          if color == BLANK:
            currentGuess[currentGuess.index(color) - 1] = BLANK
            updateColors(screen, currentGuess, count)
            break

      guess = colorPress(screen, x, y)#get which color was clicked
      if guess is not None:
        for color in currentGuess:
          if color == BLANK:
            currentGuess[currentGuess.index(color)] = guess#update guess
            updateColors(screen, currentGuess, count)#update screen
            break
          
  pygame.display.flip()#update display
  MyClock.tick(60)

input()
pygame.quit()
