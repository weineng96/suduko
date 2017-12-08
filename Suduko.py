import copy # for deepcopy

def viewer(board):
    for i in board:
        a=[]
        for k in range(3):
            a.append(i[3*k:3*k+3])
        print(a)
    return

def solve_board(board):
    ## PSEUDOCODE

    ## Board assumed to be always valid due to solving algorithm
    ## We need to process the board until two cases:
    ## 1. All empty cells are lists of length more than one -> guesswork
    ## 2. All empty cells are lists of length zero -> invalid solution
    ## 3. Empty cell is list of length one -> continue solving

    ## Check if anything changed and repeat remove_possibilities until no change
    for i in range(0,9):
        for j in range(0,9):
            if not empty(board[i][j]):
                reducepossibility(board,i,j)

    if not is_board_valid(board):
        return False

    ## Check if board is solved
    if is_board_solved(board):
        return board

    ## Check lengths of empty cells (lists)
    ## Abstract into separate function: is_board_solvable?
    if (not is_board_solvable(board)):
        return False

    ## Here, board has empty cells which are minimally of length 2
    ## Find the next box with a list, retrieve the numbers
    ## Perform depth first search for each number
    board2 = copy.deepcopy(board)
    print(board2)
    # Get empty square
    for i in range(9):
        break_flag = 0
        for j in range(9):
            if empty(board[i][j]):
                print("Empty at ({},{})".format(i,j))
                break_flag = 1
                break
        if break_flag:
            break


    # Empty square at (i,j)
    list_of_possibilities = board[i][j]
    print("Testing at Row = {}, Col = {}".format(i, j))
    print(list_of_possibilities)


    for guess in list_of_possibilities:
        print("Guessing: {}".format(guess))
        viewer(unparse_board(board2))
        print("")
        test_board = copy.deepcopy(board)
        test_board[i][j] = guess
        if (not is_board_valid(test_board)):
            print("Guess {} gives invalid board".format(guess))
            continue
        print("Guess {} is valid.".format(guess))
        print("Entering guess {} at ({},{})".format(guess, i,j))
        result = solve_board(test_board)
        if (result): # result is a board, i.e. True
            return result
        print("Guess {} gives invalid board".format(guess))

    ## Recursion fails to find a valid solution
    return False

debugger = False

def main():
    # Initialise sudoku board
    board = initialise_board()
    board = parse_board(board)
    solved = solve_board(board)
    if (not solved):
        debugger = True
        solved = solve_board(board)
    return solved



def parse_board(board):
    """ Replaces all zeros in board with possibilities list """
    possibility = [1,2,3,4,5,6,7,8,9]
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                board[i][j] = copy.copy(possibility)
    return board


def unparse_board(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if empty(board[i][j]):
                board[i][j] = 0
    return board





### Check validity of board / solutions ###

def is_board_solvable(board):
    for i in range(9):
        for j in range(9):
            if empty(board[i][j]):
                if board[i][j] == []:
                    return False
    return True

def is_board_solved(board):
    """ Checks whether the board is solved """
    if (not is_board_valid(board)):
        return False


    # Check row
    board = copy.deepcopy(board)
    for i in range(len(board)):
        if (not is_set_solved(board[i])):
            return False

    # Check column
    board = list(map(list,zip(*board))) # transposes board
    for i in range(len(board)):
        if (not is_set_solved(board[i])):
            return False

    # Check cells
    num_of_cells = 9
    for i in range(num_of_cells):
        board_cell = get_board_cell(board, i)
        if (not is_set_solved(board_cell)):
            return False

    return True

def is_board_valid(board):
    """ Checks row, columns and cells are consistent"""

    # Check row
    boards = copy.deepcopy(board)
    for i in range(len(boards)):
        if (not is_set_valid(boards[i])):
            return False

    # Check column
    boards = list(map(list,zip(*boards))) # transposes board
    for i in range(len(boards)):
        if (not is_set_valid(boards[i])):
            return False

    # Check cells
    num_of_cells = 9
    for i in range(num_of_cells):
        board_cell = get_board_cell(boards, i)
        if (not is_set_valid(board_cell)):
            return False

    return True

def get_board_cell(board, index):
    """ Generates list of numbers in cell specified by index.
        Index: [[0,1,2],[3,4,5],[6,7,8]] """
    row_num = index // 3 # ranges 0 to 2
    col_num = index % 3 # ranges 0 to 2

    num_of_cells = 9
    cell_nums = []
    for i in range(num_of_cells):
        cell_row_num = i // 3 + 3 * row_num
        cell_col_num = i % 3 + 3 * col_num
        cell_nums.append(board[cell_row_num][cell_col_num])
    return cell_nums

def is_set_valid(lst):
    for i in range(1,10):
        if lst.count(i)>1:
            return False
    return True

def is_set_solved(lst):
    """ Checks list (row/col/cell) for [1-9] without duplicates """
    existing_num = []
    for i in range(len(lst)):
        curr = lst[i]
        if empty(curr): return False # empty boxs means unsolved
        if curr in existing_num: return False
        existing_num.append(curr)
    return True



## Game solver

def empty(cell):
    #check if the cell is empty
    return type(cell)==list or cell == 0

def reducepossibility(mat,row,col):
    cell=mat[row][col]
    #delete possibilities in the row
    for rowedit in range(0,9):
        if empty(mat[row][rowedit]) and cell in mat[row][rowedit]:
            mat[row][rowedit].remove(cell)
            onlyoption(mat,row,rowedit)
    #delete possibilities in column
    for coledit in range(0,9):
        if empty(mat[coledit][col]) and cell in mat[coledit][col]:
            mat[coledit][col].remove(cell)
            onlyoption(mat,coledit,col)
    #delete possibilities in the 3*3 square
    squarepos=(row//3,col//3)
    for smallrow in range(0,3):
        for smallcol in range(0,3):
            rowpos=3*squarepos[0]+smallrow
            colpos=3*squarepos[1]+smallcol
            if empty(mat[rowpos][colpos]) and cell in mat[rowpos][colpos]:
                mat[rowpos][colpos].remove(cell)
                onlyoption(mat,rowpos,colpos)

def onlyoption(mat,row,col):
    #If the cell only have one possibility, edit the cell number to the possibility and reduce possibilities due to that cell.
    cell=mat[row][col]
    if empty(cell) and len(cell)==1:
        mat[row][col]=cell[0]
        reducepossibility(mat,row,col)


def initialise_board():
    ## To fill with sudoku randomiser or import from file
    sudoku=[[9,0,2,0,0,0,0,0,4],[0,3,0,4,0,1,8,0,0],[0,1,0,2,0,7,0,9,3],
            [0,8,0,0,0,2,0,0,9],[0,0,5,8,0,3,2,0,0],[7,0,0,9,0,0,0,3,0],
            [2,7,0,3,0,5,0,4,0],[0,0,9,7,0,4,0,6,0],[1,0,0,0,0,0,7,0,5]]

    sudoku2 = [[0,4,0,0,0,2,0,1,9],[0,0,0,3,5,1,0,8,6],[3,1,0,0,9,4,7,0,0],
               [0,9,4,0,0,0,0,0,7],[0,0,0,0,0,0,0,0,0],[2,0,0,0,0,0,8,9,0],
               [0,0,9,5,2,0,0,4,1],[4,2,0,1,6,9,0,0,0],[1,6,0,8,0,0,0,7,0]]

    sudokuhard=[[0,0,0,0,0,0,2,0,6],[0,9,0,0,1,5,0,0,0],[3,0,0,6,0,0,4,0,0],
                [0,2,0,0,5,0,3,4,0],[0,0,0,8,0,9,0,0,0],[0,4,7,0,2,0,0,6,0],
                [0,0,3,0,0,7,0,0,1],[0,0,0,1,3,0,0,8,0],[2,0,9,0,0,0,0,0,0]]
    harder=[[4,9,0,0,0,0,0,8,0],[0,0,3,0,0,0,0,0,0],[0,0,0,0,0,6,2,0,0],
            [5,0,0,0,8,0,0,9,0],[0,0,0,0,4,0,6,1,0],[6,0,1,0,2,0,5,0,0],
            [2,5,6,0,0,0,3,0,0],[1,0,0,0,0,2,0,0,0],[0,0,0,0,0,7,8,0,0]]
    blank=[[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]
    return sudokuhard

if __name__ == "__main__":
    print(main())
