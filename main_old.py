# use edge like this:
# edge[x1, y1][x2, y2] = is there an edge between (x1,y1)
import os
import sys
from collections import defaultdict
from typing import Tuple

edge = defaultdict(dict)

# Manually input the board
numrows = 4
numcols = 3
PlayerStartPos = (1,1)
MinotaurStartPos = (0,1)
GoalPos = (1,2)

def addEdge(cell1, cell2):
    print("Adding edge between", cell1, "and", cell2)
    edge[cell1][cell2] = True
    edge[cell2][cell1] = True

# Initialize edges
for row in range(numrows):
    for col in range(numcols):
        if row > 0:
            addEdge((row, col), (row-1, col))
        if row < numrows-1:
            addEdge((row, col), (row+1, col))
        if col > 0:
            addEdge((row, col), (row, col-1))
        if col < numcols-1:
            addEdge((row, col), (row, col+1))

### Manually input the walls
walls = [
    ((1,1), (0,1)),
    ((2,0), (2,1)),
    ((2,0), (3,0))
]

### End of manual input

class BoardState:
    playerPos: Tuple[int, int]
    minotaurPos: Tuple[int, int]
    goalPos: Tuple[int, int]

def canMove(source, destination) -> bool:
    if destination not in edge[source]:
        return False
    return edge[source][destination]

def movePlayer(boardstate:BoardState, destination):
    if canMove(boardstate.playerPos, destination):
        boardstate.playerPos = destination
    else:
        raise Exception("Invalid move")

def moveMinotaur(boardstate:BoardState, destination):
    if canMove(boardstate.minotaurPos, destination):
        boardstate.minotaurPos = destination
    else:
        raise Exception("Invalid move")

def tryMoveMinotaur(boardstate:BoardState, destination):
    if canMove(boardstate.minotaurPos, destination):
        boardstate.minotaurPos = destination
        #print("Successfully moved minotaur")
        return True
    #print("Failed to move minotaur: no path between", boardstate.minotaurPos, "and", destination)
    return False

def tryMovePlayer(boardstate:BoardState, destination):
    if canMove(boardstate.playerPos, destination):
        boardstate.playerPos = destination
        return True
    return False

# Do one step of the minotaur move
def MoveMinotaurByOneStep(boardstate:BoardState):
    pX, pY = boardstate.playerPos
    mX, mY = boardstate.minotaurPos
    if mY > pY:
        # try to move left
        if tryMoveMinotaur(boardstate, (mX, mY-1)):
            return
    elif mY < pY:
        # try to move right
        if tryMoveMinotaur(boardstate, (mX, mY+1)):
            return
    if mX > pX:
        # try to move up
        if tryMoveMinotaur(boardstate, (mX-1, mY)):
            return
    elif mX < pX:
        # try to move down
        if tryMoveMinotaur(boardstate, (mX+1, mY)):
            return

def IsGameLost(boardstate:BoardState):
    return boardstate.minotaurPos == boardstate.playerPos

def IsGameWon(boardstate:BoardState):
    return boardstate.playerPos == boardstate.goalPos

def ExecuteMove(boardstate:BoardState, move):
    curX, curY = boardstate.playerPos
    if move == "U":
        tryMovePlayer(boardstate, (curX-1, curY))
    elif move == "D":
        tryMovePlayer(boardstate, (curX+1, curY))
    elif move == "L":
        tryMovePlayer(boardstate, (curX, curY-1))
    elif move == "R":
        tryMovePlayer(boardstate, (curX, curY+1))
    elif move == "S":
        # do nothing.
        pass

    # After moving player, move the minotaur
    MoveMinotaurByOneStep(boardstate)
    MoveMinotaurByOneStep(boardstate)


    print("============== Board state: ============")
    #print("Player pos:", boardstate.playerPos)
    #print("Minotaur pos:", boardstate.minotaurPos)
    #print("Goal pos:", boardstate.goalPos)
    printBoard(boardstate)


    if IsGameLost(boardstate):
        print("Game lost!")
        sys.exit(0)
    elif IsGameWon(boardstate):
        print("Game won!")
        sys.exit(0)



def main():
    # Initialize game state
    boardstate = BoardState()
    boardstate.playerPos = PlayerStartPos
    boardstate.minotaurPos = MinotaurStartPos
    boardstate.goalPos = GoalPos
    for cell1, cell2 in walls:
        edge[cell1][cell2] = False
        edge[cell2][cell1] = False


    # Do the moves
    moves = "DDLSRRUU"
    print("Executing moves...")
    printBoard(boardstate)
    for move in moves:
        ExecuteMove(boardstate, move)

    print("Finished executing moves.")



def printBoard(boardstate):
    for row in range(numrows):
        for col in range(numcols):
            # print cell
            if not canMove((row,col),(row+1,col)):
                if boardstate.playerPos == (row,col):
                    print("\033[4mp\033[0m",end="")
                elif boardstate.minotaurPos == (row,col):
                    print("\033[4mM\033[0m",end="")
                else:
                    print("_", end="")
            else:
                if boardstate.playerPos == (row,col):
                    print("p",end="")
                elif boardstate.minotaurPos == (row,col):
                    print("M",end="")
                else:
                    print(" ", end="")

            # print wall
            if not canMove((row,col), (row, col+1)):
                print("|", end="")
            else:
                print(" ", end="")
        print("")





if __name__ == "__main__":
    main()

