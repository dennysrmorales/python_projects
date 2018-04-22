#This code allows you to play the game of Connect 4 with another player.

def Connect4():
    rows = 6
    cols = 7
    puzzle = make_puzzle(rows, cols)
    player = "X"
    move_count = 0
    print_puzzle(puzzle)
   
    while (move_count < rows*cols):
        move_col = get_move_col(puzzle, player)
        move_row = get_move_row(puzzle, move_col)
        puzzle[move_row][move_col] = player
        print_puzzle(puzzle)
        
        if check_for_win(puzzle, player):
            print "Player %s Wins!!!" % player
            return
        move_count += 1
        player = "O" if (player == "X") else "X"
    print "Tie Game"


def make_puzzle(rows, cols):
    return [ (["-"] * cols) for row in xrange(rows) ]
make_puzzle

def print_puzzle(puzzle):
    rows = len(puzzle)
    cols = len(puzzle[0])
    print
    print "   ",
    
    for col in xrange(cols):
        print str(col+1).center(3),
    print
   
    for row in range(rows):
        print "   ",
        for col in xrange(cols):
            print puzzle[row][col].center(3),
        print

def get_move_col(puzzle, player):
    cols = len(puzzle[0])
    while True:
        response = raw_input("Enter player %s's move (column number) --> " %
                             (player))
        
        try:
            move_col = int(response)-1  
            if ((move_col < 0) or (move_col >= cols)):
                print ("Columns must be between 1 and %d." % (cols)),
            elif (puzzle[0][move_col] != "-"):
                print "That column is full!",
            else:
                return move_col
        
        except:
            # this doesn't allow the user to enter anything that is not an integer 
            print "Columns must be integer values!",
        print "Please try again."

def get_move_row(puzzle, move_col):
   
    rows = len(puzzle)
    for move_row in xrange(rows-1, -1, -1):
        if (puzzle[move_row][move_col] == "-"):
            return move_row
  
    assert(False)

def check_for_win(puzzle, player):
    winning_word = player * 4
    return (wordSearch(puzzle, winning_word) != None)

def wordSearch(puzzle, word):
    rows = len(puzzle)
    cols = len(puzzle[0])
    
    for start_row in xrange(rows):
        for start_col in xrange(cols):
            solution = word_search_1(puzzle, word, start_row, start_col)
            if (solution != None):
                return solution
    return None

def word_search_1(puzzle, word, start_row, start_col):
    rows = len(puzzle)
    cols = len(puzzle[0])
    
    for drow in xrange(-1,2):
        for dcol in xrange(-1, 2):
            if ((drow != 0) or (dcol != 0)):
                solution = word_search_2(puzzle, word, start_row, start_col,
                                       drow, dcol)
                if (solution != None):
                    return solution
    return None

def word_search_2(puzzle, word, start_row, start_col, drow, dcol):
    rows = len(puzzle)
    cols = len(puzzle[0])
    
    for i in xrange(len(word)):
        cWord = word[i]
        puzzle_row = start_row+i*drow
        puzzle_col = start_col+i*dcol
        if ((puzzle_row < 0) or (puzzle_row >= rows) or
            (puzzle_col < 0) or (puzzle_col >= cols)):
            return None
        cPuzzle = puzzle[puzzle_row][puzzle_col]
        if (cWord != cPuzzle):
            return None
    
    return (start_row, start_col, (drow, dcol))

Connect4()