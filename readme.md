# Why did I make this?

So I've been playing this iOS game called Theseus and there's a level I couldn't beat (level 80) so I decided to write a program to solve the level for me lol.

# Theseus and the Minotaur Solver

This repository includes:

* Maze input GUI (uses tkinter) for you to easily input the walls and starting positions of player, minotaur, and the goal position. All you need to do is run `input.py` and then you input the maze and press the Finish button and it will generate code that you can then paste into the `main.py` file.
* 4 solvers - brute force, recursive backtracking, BFS, and DFS. See `main.py` for an example of how to use the solvers.
* The actual game itself. No GUI is included but you can easily print the board after each move to see ASCII representation of the board state including where the player is and where the minotaur is. A convenience function is included for you to input a list of moves and then the game will run your moves. Alternatively you can call the `ExecuteMove` function on your own.

# How to use

1. Run `input.py`, input the walls and starting positions and when you're done, press the Finish button to generate the code (it prints the code to terminal, so make sure to run `input.py` from a terminal where you can see the output)
2. Paste that code into the appropriate place in`main.py` (you'll know where it is, don't worry, it's really obvious)
3. Run `main.py`. 

## How the solvers work

* The `BruteForceSolve` function simply generates all possible sequences of moves up to a certain length and tries them all. Obviously this is exponential time so is only viable for the simplest possible boards.
* The `RecursiveBacktrackingSolve` function tries all possible moves and backtracks when it hits a dead end. This is highly inefficient because it is constantly revisiting board states and so is not viable for more complicated boards.
* The `BFSSolve` function does a BFS while avoiding visiting previously visited board states. Since the total number of possible board states is quite small, the algorithm is actually very efficient in both time and space. For a 10x10 board there are only 100k possible board states and it's no problem to just visit and store them all. Furthermore BFS has the nice property that it will find the shortest possible solution first.
* The `DFSSolve` function does a DFS while only revisiting previously visited board states if we have a shorter path. I removed the recursion limit because it turns out that even on large boards you can only make so many moves before you're at the point where every possible next move hits a previously visited state. Unfortunately the vanilla DFS will not find the shortest path if you don't allow it to revisit states, but if you allow it to unconditionally revisit board states then it will take forever. So I found a nice compromise which is to let it only revisit board states when it has found a shorter path to that board states than previously.

## Personal thoughts

All in all took me a few hours to write up the whole thing. I wrote the whole thing in less than a day. The wall input GUI probably took the most amount of time.

One of the bugs I found while debugging the BFSSolve was due to the `CanExecuteMove` function actually mutating the game state lol.

For the recursive backtracking it was okay to modify the game state since it's a DFS you just do the modification then undo it when you come back up the stack, but for DFS you need to store the full game state in the queue.

I think the greatest insight was when I realized that the entire game state is just 4 integers: the x and y coordinates of the player and the minotaur. Nothing else changes except for those 2 coordinates.

That's why in a 10x10 board there can only be 10k possible board states because there are only 100 squares and the player and the minotaur can be in one of 100 possible positions each, so 100x100 = 10k.

Once I realized that the total number of game states is only `N^2` (where N is the number of tiles on the board) I realized that BFS was viable after all. Because with BFS we want to not revisit previously visited states. And if there are only 10k possible states and each state is only just 4 integers then we can simply store all of the visited states in memory. BFS is so good here because we can say "don't revisit previously visited states". That makes sense because there is no reason why you would ever want to go to a previously visited board state for BFS (for DFS you want to do that sometimes in order to find a shorter move sequence, but for BFS there is no reason to ever do that because BFS will find the shortest path first). 

For the BFS I implemented the function which takes in a board state and a move and returns the resulting board state. I didn't realize that was necessary at first, but now that I think about it, it's actually the most intuitive and straightforward way to implement the game. Well, maybe you only need it for the BFS solver but I think if you try to implement BFS using the game-state-mutating functions then you have to remember to undo the changes and it becomes a mess. Whereas with pure functions that have no side effects it's much easier to write the code correctly.

