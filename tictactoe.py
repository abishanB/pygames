import random
import sys
import time

import pygame

winningBoards = ([0,1,2], [3,4,5], [6,7,8], #horizontal 
                 [0,3,6], [1,4,7], [2,5,8], #vertical
                 [0,4,8], [2,4,6]           #horizontal
                 )

            #spot, coloumn and row
boardArray = {0:[0,0],
              1:[0,1],
              2:[0,2],
              3:[1,0],
              4:[1,1],
              5:[1,2],
              6:[2,0],
              7:[2,1],
              8:[2,2]}

players = ["O", "X"]

def most_frequent(List):
    counter = 0
    num = List[0]
      
    for i in List:
        curr_frequency = List.count(i)
        if(curr_frequency> counter):
            counter = curr_frequency
            num = i
  
    return num

for defineConstants in range(1):
    BLACK = (0, 0, 0)
    GRAY = (127, 127, 127)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    
    LINE_COLOR = WHITE
    LINE_WIDTH = 15
    SPACE = 55
    DIAGONAL_SPACE = SPACE *4
    CROSS_COLOR = WHITE
    CROSS_WIDTH = 25

    SQUARE_SIZE = 200
    HALF_SQUARE_SIZE = SQUARE_SIZE/2
    
    CIRCLE_COLOR = WHITE
    CIRCLE_RADIUS = 60
    CIRCLE_WIDTH = 15

pygame.init()

WIDTH = 600
HEIGHT = 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(BLACK)
pygame.display.set_caption("TIC TAC TOE")

def drawBoard():
    for location, player in board.items():
        row, col = boardArray[location]
        
        if player == "O":#Draw O
            pygame.draw.circle( screen, CIRCLE_COLOR, (int( col * SQUARE_SIZE + SQUARE_SIZE//2 ), int( row * SQUARE_SIZE + SQUARE_SIZE//2 )), CIRCLE_RADIUS, CIRCLE_WIDTH )
        
        if player == "X":#draw X
            pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)	
            pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)

def drawWinLine(winning_line):  #drawFinalLine
    start_row, start_col = boardArray[winning_line[0]]
    end_row, end_col = boardArray[winning_line[2]]
    
    pygame.draw.line(screen, RED, (start_col * SQUARE_SIZE + HALF_SQUARE_SIZE, start_row * SQUARE_SIZE + HALF_SQUARE_SIZE),
                     (end_col * SQUARE_SIZE + HALF_SQUARE_SIZE, end_row * SQUARE_SIZE + HALF_SQUARE_SIZE), CROSS_WIDTH)	  

def winner(player):
    if player is None:
        print("\nTIE!!")
        tieText = pygame.font.Font('freesansbold.ttf', 27)
        tieText = tieText.render("TIE!!", True, GREEN)
        screen.blit(tieText, ((SQUARE_SIZE*1) + (SQUARE_SIZE/3), SQUARE_SIZE*3 + 10 ))
        return
    
    text = f"{player} WINS!"
    print("\n",text)
    winnerText = pygame.font.Font('freesansbold.ttf', 27)
    winnerText = winnerText.render(text, True, GREEN)
    screen.blit(winnerText, ((SQUARE_SIZE*1) + (SQUARE_SIZE/4), SQUARE_SIZE*3 + 10 ))
        
def checkForWinner():#check if any player has won
    for player in players:
        for winBoard in winningBoards:
            if board[winBoard[0]] == player and board[winBoard[1]] == player and board[winBoard[2]] == player:
                drawBoard()
                winner(player)
                drawWinLine(winBoard)
                return True
            
    if spotsTaken == 9:
        drawBoard()
        winner(None)
        return True

def computerMove():
    for Player in players:   #if 2 out of 3 win positions are filled 
        for winBoard in winningBoards:
            if board[winBoard[0]] == Player and board[winBoard[1]] == Player:      
                if board[winBoard[2]] == " ":
                    board[winBoard[2]] = "O"
                    return
            if board[winBoard[1]] == Player and board[winBoard[2]] == Player:
                if board[winBoard[0]] == " ":
                    board[winBoard[0]] = "O"
                    return
            if board[winBoard[0]] == Player and board[winBoard[2]] == Player:
                if board[winBoard[1]] == " ":
                    board[winBoard[1]] = "O"
                    return
    
    if spotsTaken == 1:
        if board[4] != "O" and board[4] != "X":    #always go middle on on first move if possible
            board[4] = "O"
            return
    
    if spotsTaken == 3:
        playerPositons = []
        for spot, player in board.items():
            if board[spot] == "X":
                playerPositons.append(spot)

        possibleMoves = []
        for winBoard in winningBoards:
            if playerPositons[0] in winBoard or playerPositons[1] in winBoard:
                for positon in winBoard:
                    if positon == playerPositons[0] or positon == playerPositons[1] or board[positon]== "O":
                        continue
                    
                    possibleBoard = True
                    winBoard_copy = winBoard.copy()
                    winBoard_copy.remove(positon)
                    for p in winBoard_copy:
                        if board[p] == "O":
                            possibleBoard = False
                            break
                    if possibleBoard:                           #if winning board is possible for opponet
                        possibleMoves.append(positon)
                
        board[most_frequent(possibleMoves)] = "O"
        return
    

    availableSpots=[]
    for spot, player in board.items():
        if player == " ":
            availableSpots.append(spot)
    board[random.choice(availableSpots)] = "O"
    
def newGame(): #set display and draw lines
    screen.fill(BLACK)
    pygame.display.set_caption("TIC TAC TOE")
    #draw lines
    pygame.draw.line(screen, LINE_COLOR, (0, 200), (600, 200), LINE_WIDTH) #left
    pygame.draw.line(screen, LINE_COLOR, (0, 400), (600, 400), LINE_WIDTH) #right
    
    pygame.draw.line(screen, LINE_COLOR, (200, 0), (200, 600), LINE_WIDTH) #top
    pygame.draw.line(screen, LINE_COLOR, (400, 0), (400, 600), LINE_WIDTH) #bottom
    
    restartText = pygame.font.Font('freesansbold.ttf', 27)
    restartText = restartText.render("Restart", True, GRAY)
    screen.blit(restartText, (SQUARE_SIZE/4, SQUARE_SIZE*3 + 10 ))

    exitText = pygame.font.Font('freesansbold.ttf', 27)
    exitText = exitText.render("Exit", True, GRAY)
    screen.blit(exitText, ((SQUARE_SIZE*2) + (SQUARE_SIZE/3), SQUARE_SIZE*3 + 10 ))
    
def game():
    screen.fill(BLACK)
    pygame.display.set_caption("TIC TAC TOE")
    newGame()
    global board
    board = {0:" ", 1:" ", 2:" ",
             3:" ", 4:" ", 5:" ",
             6:" ", 7:" ", 8:" "} 
    
    global spotsTaken
    spotsTaken = 0 
    userTurn= True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and userTurn:#if clicked
                mouseX = event.pos[0] # x           
                mouseY = event.pos[1] # y

                clicked_row = int(mouseY // SQUARE_SIZE)           
                clicked_col = int(mouseX // SQUARE_SIZE)

                if (clicked_row, clicked_col) == (3, 0): #restart button
                    return
                
                if (clicked_row, clicked_col) == (3,2):  #exit button
                    sys.exit()
                    
                #find spot assosciated with the coloum and row
                for pos in boardArray.values():                         #reverse search dictionary
                    if pos == [clicked_row, clicked_col]: 
                        clicked_pos = list(boardArray.values()).index(pos)    
                        break 
                
                if board[clicked_pos] == " ":
                    spotsTaken += 1 
                    board[clicked_pos] = "X"
                    userTurn =False
                
        drawBoard()
        
        
        if checkForWinner():
            break
        
        if not userTurn:
            computerMove()
            spotsTaken += 1 
            userTurn = True
            
        if checkForWinner():
            break
                
        
        pygame.display.update()
    pygame.display.update()#update one last time before restarting
    time.sleep(2)
    return
            

while True:
    game()
