# This file contains all of the code needed to run the game
# The code could be cleaned up a bit, a lot of repetition

# use edge like this:
# edge[x1, y1][x2, y2] = is there an edge between (x1,y1)
from collections import defaultdict
from typing import Tuple, List


class BoardInput:
    numrows: int
    numcols: int
    PlayerStartPos: Tuple[int, int]
    MinotaurStartPos: Tuple[int, int]
    GoalPos: Tuple[int, int]
    Walls: List[Tuple[Tuple[int, int], Tuple[int, int]]]

    def __init__(self, *, numrows, numcols, PlayerStartPos, MinotaurStartPos, GoalPos, Walls):
        self.numrows = numrows
        self.numcols = numcols
        self.PlayerStartPos = PlayerStartPos
        self.MinotaurStartPos = MinotaurStartPos
        self.GoalPos = GoalPos
        self.Walls = Walls



class Game:
    edge = defaultdict(dict)    
    playerPos: Tuple[int, int]
    minotaurPos: Tuple[int, int]
    goalPos: Tuple[int, int]
    numrows: int
    numcols: int


    def addEdge(self, cell1, cell2):
        print("Adding edge between", cell1, "and", cell2)
        self.edge[cell1][cell2] = True
        self.edge[cell2][cell1] = True


    def canMove(self, source, destination) -> bool:
        if any(x < 0 for x in source + destination):
            return
        if destination not in self.edge[source]:
            return False
        return self.edge[source][destination]

    def movePlayer(self, destination):
        if self.canMove(self.playerPos, destination):
            self.playerPos = destination
        else:
            raise Exception("Invalid move")

    def moveMinotaur(self, destination):
        if self.canMove(self.minotaurPos, destination):
            self.minotaurPos = destination
        else:
            raise Exception("Invalid move")

    def tryMoveMinotaur(self, destination):
        if self.canMove(self.minotaurPos, destination):
            self.minotaurPos = destination
            #print("Successfully moved minotaur")
            return True
        #print("Failed to move minotaur: no path between", self.minotaurPos, "and", destination)
        return False

    def canMovePlayer(self, destination):
        return self.canMove(self.playerPos, destination)

    def tryMovePlayer(self, destination):
        if self.canMove(self.playerPos, destination):
            self.playerPos = destination
            return True
        return False

    # Do one step of the minotaur move
    def MoveMinotaurByOneStep(self):
        pX, pY = self.playerPos
        mX, mY = self.minotaurPos
        if mY > pY:
            # try to move left
            if self.tryMoveMinotaur((mX, mY-1)):
                return
        elif mY < pY:
            # try to move right
            if self.tryMoveMinotaur((mX, mY+1)):
                return
        if mX > pX:
            # try to move up
            if self.tryMoveMinotaur((mX-1, mY)):
                return
        elif mX < pX:
            # try to move down
            if self.tryMoveMinotaur((mX+1, mY)):
                return

    def IsGameLost(self):
        return self.minotaurPos == self.playerPos

    def IsGameWon(self):
        return self.playerPos == self.goalPos

    def CanExecuteMove(self, move) -> bool:
        curX, curY = self.playerPos
        if move == "U":
            return self.canMovePlayer((curX-1, curY))
        elif move == "D":
            return self.canMovePlayer((curX+1, curY))
        elif move == "L":
            return self.canMovePlayer((curX, curY-1))
        elif move == "R":
            return self.canMovePlayer((curX, curY+1))
        elif move == "S":
            return True


    def CanExecuteMoveInBoardstate(self, boardstate:Tuple[int,int,int,int], move) -> bool:
        self.playerPos = (boardstate[0], boardstate[1])
        self.minotaurPos = (boardstate[2], boardstate[3])

        curX, curY = self.playerPos
        if move == "U":
            return self.canMovePlayer((curX-1, curY))
        elif move == "D":
            return self.canMovePlayer((curX+1, curY))
        elif move == "L":
            return self.canMovePlayer((curX, curY-1))
        elif move == "R":
            return self.canMovePlayer((curX, curY+1))
        elif move == "S":
            return True


    def ExecuteMove(self, move):
        curX, curY = self.playerPos
        if move == "U":
            self.tryMovePlayer((curX-1, curY))
        elif move == "D":
            self.tryMovePlayer((curX+1, curY))
        elif move == "L":
            self.tryMovePlayer((curX, curY-1))
        elif move == "R":
            self.tryMovePlayer((curX, curY+1))
        elif move == "S":
            # do nothing.
            pass

        # After moving player, move the minotaur
        self.MoveMinotaurByOneStep()
        self.MoveMinotaurByOneStep()


    def CheckIfGameIsWon(self, boardstate:Tuple[int,int,int,int]):
        if self.CheckIfGameIsLost(boardstate):
            return False
        return (boardstate[0], boardstate[1]) == self.goalPos

    def CheckIfGameIsLost(self, boardstate:Tuple[int,int,int,int]) -> bool:
        return (boardstate[0], boardstate[1]) == (boardstate[2], boardstate[3])


    def GetBoardstateAfterMove(self, previous_boardstate:Tuple[int,int,int,int], move) -> Tuple[int,int,int,int]:
        self.playerPos = (previous_boardstate[0], previous_boardstate[1])
        self.minotaurPos = (previous_boardstate[2], previous_boardstate[3])

        curX, curY = self.playerPos
        if move == "U":
            self.tryMovePlayer((curX-1, curY))
        elif move == "D":
            self.tryMovePlayer((curX+1, curY))
        elif move == "L":
            self.tryMovePlayer((curX, curY-1))
        elif move == "R":
            self.tryMovePlayer((curX, curY+1))
        elif move == "S":
            # do nothing.
            pass

        # After moving player, move the minotaur
        self.MoveMinotaurByOneStep()
        self.MoveMinotaurByOneStep()

        return (self.playerPos[0], self.playerPos[1], self.minotaurPos[0], self.minotaurPos[1])







    def printBoard(self):
        for row in range(self.numrows):
            for col in range(self.numcols):
                # print cell
                if not self.canMove((row,col),(row+1,col)):
                    if self.playerPos == (row,col):
                        print("\033[4mp\033[0m",end="")
                    elif self.minotaurPos == (row,col):
                        print("\033[4mM\033[0m",end="")
                    elif self.goalPos == (row,col):
                        print("\033[4mG\033[0m",end="")
                    else:
                        print("_", end="")
                else:
                    if self.playerPos == (row,col):
                        print("p",end="")
                    elif self.minotaurPos == (row,col):
                        print("M",end="")
                    elif self.goalPos == (row,col):
                        print("G",end="")
                    else:
                        print(" ", end="")

                # print wall
                if not self.canMove((row,col), (row, col+1)):
                    print("|", end="")
                else:
                    print(" ", end="")
            print("")

    def reset(self):
        self.minotaurPos = self.InitialMinotaurPos
        self.playerPos = self.InitialPlayerPos

    def __init__(self, boardinput:BoardInput):
        # Initialize edges
        for row in range(boardinput.numrows):
            for col in range(boardinput.numcols):
                if row > 0:
                    self.addEdge((row, col), (row - 1, col))
                if row < boardinput.numrows - 1:
                    self.addEdge((row, col), (row + 1, col))
                if col > 0:
                    self.addEdge((row, col), (row, col - 1))
                if col < boardinput.numcols - 1:
                    self.addEdge((row, col), (row, col + 1))


        # Initialize game state
        self.InitialPlayerPos = boardinput.PlayerStartPos
        self.InitialMinotaurPos = boardinput.MinotaurStartPos
        self.playerPos = boardinput.PlayerStartPos
        self.minotaurPos = boardinput.MinotaurStartPos
        self.goalPos = boardinput.GoalPos
        self.numcols = boardinput.numcols
        self.numrows = boardinput.numrows
        # Add walls
        for cell1, cell2 in boardinput.Walls:
            self.edge[cell1][cell2] = False
            self.edge[cell2][cell1] = False
            print("Adding wall between", cell1, cell2)


    def RunGame(self, moves:str):
        # Do the moves
        print("Executing moves...")
        self.printBoard()
        for move in moves:
            self.ExecuteMove(move)
            print("============== Board state: ============")
            self.printBoard()

            if self.IsGameLost():
                print("Game lost!")
                return
            elif self.IsGameWon():
                print("Game won!")
                return

        print("Finished executing moves.")


    def RunGameQuiet(self, moves:str):
        # Reset state
        self.reset()
        # Do the moves
        for move in moves:
            if not self.CanExecuteMove(move):
                return False
            self.ExecuteMove(move)
            if self.IsGameLost():
                return False
            elif self.IsGameWon():
                return True
        return False

