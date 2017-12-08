def solver(game):
    store=game.copy()
    currentstate=game.copy()
    rowcolcheck(currentstate)
    return currentstate
                

def empty(x):
    return not x

def rowcolcheck(mat):
    currentstate=mat.copy()
    for i in range(0,9):
        for j in range(0,9):
            pos=(i,j)
            if empty(currentstate[i][j]):
                possibility=[1,2,3,4,5,6,7,8,9]
                for p in range(0,9):
                    if not empty(currentstate[p][j]) and currentstate[p][j] in possibility:
                        possibility.remove(currentstate[p][j])
                for q in range(0,9):
                    if not empty(currentstate[i][q]) and currentstate[i][q] in possibility:                               
                        possibility.remove(currentstate[i][q])
                if len(possibility)==1:
                    currentstate[i][j]=possibility[0]
                else:
                    currentstate[i][j]=possibility
    return currentstate

def smallsquare(game):
    pass

suduko=[[9,0,2,0,0,0,0,0,4],[0,3,0,4,0,1,8,0,0],[0,1,0,2,0,7,0,9,3],
        [0,8,0,0,0,2,0,0,9],[0,0,5,8,0,3,2,0,0],[7,0,0,9,0,0,0,3,0],
        [2,7,0,3,0,5,0,4,0],[0,0,9,7,0,4,0,6,0],[1,0,0,0,0,0,7,0,5]]

print(solver(suduko))
