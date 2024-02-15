# This file contains all of the solver stuff
# Input: Board
# Output: Moves that win
import itertools
from typing import Tuple, List

from game import Game, BoardInput
def BruteForceSolve(input_board: BoardInput, maxlength):
    game = Game(input_board)
    chars = "UDLRS"
    for i in range(maxlength):
        moves = itertools.product(chars, repeat=i)
        for move in moves:
            won = game.RunGameQuiet(move)
            if won:
                print("length", i, "winning move:", move)
                return
    print("No winning moves found.")


# Not great...will take a long time on more complicated boards.
def RecursiveBacktrackingSolve(input_board: BoardInput, maxdepth):
    game = Game(input_board)
    chars = "UDLRS"

    #class BoardState:
    #    PlayerPos: Tuple[int, int]
    #    MinoPos: Tuple[int, int]

    cur_move = []
    badstates = set() # keeps track of board states that we know will lead to failure
    def helper(boardstate: Tuple[int, int, int, int], recursion_depth) -> bool:
        if boardstate in badstates:
            return False

        if game.IsGameLost():
            badstates.add(boardstate)
            return False

        if game.IsGameWon():
            print("Solution found:", cur_move)
            return True

        if recursion_depth > maxdepth:
            return False

        # Try every move
        for move in chars:
            # Reset the game state
            game.playerPos = (boardstate[0], boardstate[1])
            game.minotaurPos = (boardstate[2], boardstate[3])

            if not game.CanExecuteMove(move):
                continue

            # If we can try it, then try it.
            cur_move.append(move)
            game.ExecuteMove(move)
            newboardstate = game.playerPos + game.minotaurPos
            if helper(newboardstate, recursion_depth + 1):
                return True
            cur_move.pop()

        return False


    boardstate = game.playerPos + game.minotaurPos

    if helper(boardstate, 0) == False:
        print("No solutions found.")
    else:
        print("Found a solution.")



# The best
def BFSSolve(input_board: BoardInput):
    game = Game(input_board)
    chars = "UDLRS"

    #class BoardState:
    #    PlayerPos: Tuple[int, int]
    #    MinoPos: Tuple[int, int]

    cur_move = []
    visited = set() # keeps track of board states that we know will lead to failure

    initialboardstate = game.playerPos + game.minotaurPos
    q = [(initialboardstate, "")]
    def run_one_iteration(q):
        print("q:",q)
        newq = []
        for boardstate, moveseq in q:
            for move in chars:
                if not game.CanExecuteMoveInBoardstate(boardstate, move):
                    continue

                # If we can try it, then try it.
                #cur_move.append(move)
                newboardstate = game.GetBoardstateAfterMove(boardstate, move)
                # check if it's a win or loss
                if game.CheckIfGameIsWon(newboardstate):
                    print("Solution found!", newboardstate, moveseq+move)
                    return True

                # Check if we've already seen it
                if newboardstate not in visited:
                    newq.append((newboardstate, moveseq+move))
                    # don't revisit it
                    visited.add(newboardstate)
        return newq

    while q:
        q = run_one_iteration(q)
        if q == True:
            return

    print("No solutions found!")







# Pretty cool too
def DFSSolve(input_board: BoardInput):
    game = Game(input_board)
    chars = "UDLRS"

    #class BoardState:
    #    PlayerPos: Tuple[int, int]
    #    MinoPos: Tuple[int, int]

    cur_move = []
    shortest_way_to_state = {} # keeps track of board states that we know will lead to failure
    def helper(boardstate: Tuple[int, int, int, int]) -> bool:
        # if we've already visited this boardstate before, don't revisit it UNLESS we have a new, shorter path to it
        if boardstate in shortest_way_to_state:
            if shortest_way_to_state[boardstate] > len(cur_move):
                shortest_way_to_state[boardstate] = len(cur_move)
            else:
                return False
        else:
            shortest_way_to_state[boardstate] = len(cur_move)

        if game.IsGameLost():
            return False

        if game.IsGameWon():
            print(len(cur_move), "length solution found:", cur_move)
            return True

        # Try every move
        for move in chars:
            # Reset the game state
            game.playerPos = (boardstate[0], boardstate[1])
            game.minotaurPos = (boardstate[2], boardstate[3])

            if not game.CanExecuteMove(move):
                continue

            # If we can try it, then try it.
            game.ExecuteMove(move)
            newboardstate = game.playerPos + game.minotaurPos
            cur_move.append(move)
            if helper(newboardstate):
            #    return True # we want it to find all solutions
                pass
            cur_move.pop()

        return False


    boardstate = game.playerPos + game.minotaurPos

    helper(boardstate)
    print("End of DFS")
#    if helper(boardstate) == False:
#        print("No solutions found.")
#    else:
#        print("Found a solution.")
