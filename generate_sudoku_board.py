# algorithmic sudouku generator help from https://dlbeer.co.nz/articles/sudoku.html
# rows and columns indexed 0-8
import random
import copy
emptygrid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]
completed = [1,2,3,4,5,6,7,8,9]

#returns fully valid board to play
def completedSudokuBoard():
    while True:
        board = generatePossibleSudoku()
        if checkifSudokuisvalid(board):
            break
    return board

#forms the puzzle board from the completed board according to wanted difficulty
def puzzleSudokuBoard(grid, difficulty):
    #avg of 30 empty spaces
    if difficulty == "easy":
        lbound = 2000
    #avg of 40 empty spaces
    elif difficulty == "medium":
        lbound = 15000
    #avg of 50 empty spaces
    elif difficulty == "hard": 
        lbound = 50000
    puzzlegrid = copy.deepcopy(grid)
    puzzlescore = diffultyscore(puzzlegrid)
    tempgrid = copy.deepcopy(grid)

    while not (lbound <= puzzlescore):
        #remove random cell
        row = random.choice(range(9))
        col = random.choice(range(9))
        valueremoved = copy.deepcopy(tempgrid[row][col])
        tempgrid[row][col] = 0
        tempscore = diffultyscore(tempgrid)
        
        #checks if puzzle can be uniquely solved, if not put value back
        few_cell = fewest_candidates(tempgrid)
        if len(possibleCandidates(grid, few_cell[0], few_cell[1])) > 1:
            tempgrid[row][col] = valueremoved
        
        #if difficulty score is higher and puzzle is unique, save new puzzle and score
        if tempscore > puzzlescore:
            puzzlegrid = copy.deepcopy(tempgrid)
            puzzlescore = tempscore
    
    print (diffultyscore(puzzlegrid))   

    return puzzlegrid

def diffultyscore(grid):
    emptycells = 0
    for row in grid:
        for column in row:
            if column == 0:
                emptycells += 1
    branchdifficulty = 0
    row = 0
    while row <= 8:
        col = 0
        while col <= 8:
            if isCellempty(grid, row, col):
                branchdifficulty = branchdifficulty + (len(possibleCandidates(grid, row, col)) - 1) ** 2
            col += 1
        row += 1
    score = branchdifficulty * 100 + emptycells
    print(emptycells)
    return score

#invalid Sudokus will contain 0s
def checkifSudokuisvalid(grid):
    for row in grid:
        for column in row:
            if column == 0:
                return False
    return True

#makes a Sudoku board, but may contain 0s 
def generatePossibleSudoku():
    playgrid = copy.deepcopy(emptygrid)
    while not checkifSudokuisvalid(playgrid):
        curr_cell = fewest_candidates(playgrid)
        curr_posscand = possibleCandidates(playgrid,curr_cell[0], curr_cell[1])
        #reaches this condition if it creates a sudoku that has cells that cannot be filled
        if len(curr_posscand) == 0:
            playgrid = copy.deepcopy(emptygrid)
        else: 
            playgrid[curr_cell[0]][curr_cell[1]] = random.choice(curr_posscand)
    return playgrid

# returns list of possible candidates for the cell after looking at the column
def columnCheck(board, column):
    curr_col = []
    for row in board:
        curr_col.append(row[column])
    return list(set(completed) - set(curr_col))

# returns list of possible candidates for the cell after looking at the row
def rowCheck(board, row):
    return list(set(completed) - set(board[row]))

# returns list of possible candidates for the cell after looking at the box
def boxCheck(board, row, column):
    curr_box = []

    if 0 <= column <= 2:
        search_col = 0
    elif 3 <= column <= 5: 
        search_col = 3
    elif 6 <= column <= 8:
        search_col = 6

    if 0 <= row <= 2:
        search_row = 0
    elif 3 <= row <= 5: 
        search_row = 3
    elif 6 <= row <= 8:
        search_row = 6

    counter = 3
    while counter > 0:
        curr_box.append(board[search_row][search_col])
        curr_box.append(board[search_row][search_col + 1])
        curr_box.append(board[search_row][search_col + 2])
        search_row += 1
        counter -= 1

    return list(set(completed) - set(curr_box))

# returns list of possible candidates after looking at row, column, and box
def possibleCandidates(board, row, column):
    columncand = columnCheck(board, column)
    rowcand = rowCheck(board, row)
    boxcand = boxCheck(board, row, column)
    return list(set(boxcand) & set(list(set(columncand) & set(rowcand))) )

# returns the open cell [row, column] with the fewest candidates greater than 0
# if multiple cells have the same number of candidates it returns the left-most and top-most cell
def fewest_candidates(board):
    ans_row = 0
    ans_col = 0
    least_candidates = 9
    curr_row = 0
    for row in board:
        curr_col = 0
        for column in row:
            if isCellempty(board, curr_row, curr_col) == False:
                curr_col +=1 
                continue
            curr_cands = len(possibleCandidates(board, curr_row, curr_col)) 
            if 0 <= curr_cands < least_candidates:
                ans_row = curr_row
                ans_col = curr_col
                least_candidates = curr_cands
            curr_col += 1
        curr_row += 1
    return [ans_row, ans_col]

#boolean 
def isCellempty(board, row, column):
    if board[row][column] == 0:
        return True
    return False