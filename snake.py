import random
from Tkinter import *

def mousePressed(event):
    redrawAll()

def keyPressed(event):
    canvas.data.ignoreNextTimerEvent = True
    if (event.char == "q"):
        gameOver()
    elif (event.char == "r"):
        init()
    elif (event.char == "d"):
        canvas.data.inDebugMode = not canvas.data.inDebugMode

    if (canvas.data.isGameOver == False):
        if (event.keysym == "Up"):
            moveSnake(-1, 0)
        elif (event.keysym == "Down"):
            moveSnake(+1, 0)
        elif (event.keysym == "Left"):
            moveSnake(0,-1)
        elif (event.keysym == "Right"):
            moveSnake(0,+1)
    redrawAll()

def moveSnake(drow, dcol):
    canvas.data.snakeDrow = drow 
    canvas.data.snakeDcol = dcol
    snake_board = canvas.data.snake_board
    rows = len(snake_board)
    cols = len(snake_board[0])
    head_row = canvas.data.head_row
    head_col = canvas.data.head_col
    new_head_row = head_row + drow
    new_head_col = head_col + dcol

    if ((new_head_row < 0) or (new_head_row >= rows) or
        (new_head_col < 0) or (new_head_col >= cols)):
        gameOver()

    elif (snake_board[new_head_row][new_head_col] > 0):
        gameOver()

    elif (snake_board[new_head_row][new_head_col] < 0):
        snake_board[new_head_row][new_head_col] = 1 + snake_board[head_row][head_col];
        canvas.data.head_row = new_head_row
        canvas.data.head_col = new_head_col
        placeFood()

    else:
        snake_board[new_head_row][new_head_col] = 1 + snake_board[head_row][head_col];
        canvas.data.head_row = new_head_row
        canvas.data.head_col = new_head_col
        removeTail()

def removeTail():
    snake_board = canvas.data.snake_board
    rows = len(snake_board)
    cols = len(snake_board[0])

    for row in range(rows):
        for col in range(cols):
            if (snake_board[row][col] > 0):
                snake_board[row][col] -= 1

def gameOver():
    canvas.data.isGameOver = True

def timerFired():
    ignoreThisTimerEvent = canvas.data.ignoreNextTimerEvent
    canvas.data.ignoreNextTimerEvent = False

    if ((canvas.data.isGameOver == False) and
        (ignoreThisTimerEvent == False)):

        drow = canvas.data.snakeDrow
        dcol = canvas.data.snakeDcol
        moveSnake(drow, dcol)
        redrawAll()

    delay = 150 
    canvas.after(delay, timerFired) 

def redrawAll():
    canvas.delete(ALL)
    drawsnake_board()

    if (canvas.data.isGameOver == True):
        cx = canvas.data.canvasWidth/2
        cy = canvas.data.canvasHeight/2
        canvas.create_text(cx, cy, text="Game Over!", font=("Helvetica", 32, "bold"))

def drawsnake_board():
    snake_board = canvas.data.snake_board
    rows = len(snake_board)
    cols = len(snake_board[0])

    for row in range(rows):
        for col in range(cols):
            drawSnakeCell(snake_board, row, col)

def drawSnakeCell(snake_board, row, col):
    margin = canvas.data.margin
    cellSize = canvas.data.cellSize
    left = margin + col * cellSize

    right = left + cellSize
    top = margin + row * cellSize
    bottom = top + cellSize
    canvas.create_rectangle(left, top, right, bottom, fill="white")

    if (snake_board[row][col] > 0):
        canvas.create_oval(left, top, right, bottom, fill="blue")

    elif (snake_board[row][col] < 0):
        canvas.create_oval(left, top, right, bottom, fill="green")

    if (canvas.data.inDebugMode == True):
        canvas.create_text(left+cellSize/2,top+cellSize/2,
                           text=str(snake_board[row][col]),font=("Helvatica", 14, "bold"))

def load_board():
    rows = canvas.data.rows
    cols = canvas.data.cols
    snake_board = [ ]

    for row in range(rows): snake_board += [[0] * cols]
    snake_board[rows/2][cols/2] = 1
    canvas.data.snake_board = snake_board
    find_head()
    placeFood()

def placeFood():
    snake_board = canvas.data.snake_board
    rows = len(snake_board)
    cols = len(snake_board[0])

    while True:
        row = random.randint(0,rows-1)
        col = random.randint(0,cols-1)
        if (snake_board[row][col] == 0):
            break
    snake_board[row][col] = -1

def find_head():
    snake_board = canvas.data.snake_board
    rows = len(snake_board)
    cols = len(snake_board[0])
    head_row = 0
    head_col = 0
    for row in range(rows):
        for col in range(cols):
            if (snake_board[row][col] > snake_board[head_row][head_col]):
                head_row = row
                head_col = col
    canvas.data.head_row = head_row
    canvas.data.head_col = head_col

def printInstructions():
    print "Use the arrow keys to move the snake."
    print "In order to grow you need to eat food."
    print "You need to stay on the board without crashing into yourself!"
    print "Press 'r' to restart."


def init():
    printInstructions()
    load_board()
    canvas.data.inDebugMode = False
    canvas.data.isGameOver = False

    canvas.data.snakeDrow = 0
    canvas.data.snakeDcol = -1 
    canvas.data.ignoreNextTimerEvent = False
    redrawAll()


def run(rows, cols):
    global canvas
    root = Tk()
    margin = 5
    cellSize = 30
    canvasWidth = 2*margin + cols*cellSize
    canvasHeight = 2*margin + rows*cellSize

    canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
    canvas.pack()
    root.canvas = canvas.canvas = canvas

    class Struct: pass
    canvas.data = Struct()
    canvas.data.margin = margin
    canvas.data.cellSize = cellSize
    canvas.data.canvasWidth = canvasWidth
    canvas.data.canvasHeight = canvasHeight
    canvas.data.rows = rows
    canvas.data.cols = cols

    init()
    root.bind("<Button-1>", mousePressed)
    root.bind("<Key>", keyPressed)
    timerFired()
    root.mainloop()

run(8,16)
