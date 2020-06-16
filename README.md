# CS3243 8-Puzzle Problem
## Description
This application solves the 8 puzzle problem using the A* Graph Search algorithm. Two separate heuristics were used in our example:
1. Manhattan Distance of each cell to its goal state
2. Number of misplaced tiles

The application will output a series of moves required to solve the puzzle. Each move will be one of "LEFT", "RIGHT", "UP" or "DOWN".

For example, a "LEFT" move will mean moving the cell on the right of the empty cell left. 
```
0 1 2                   1 0 2
3 4 5     ------>       3 4 5
6 7 8                   6 7 8
```

## Usage
1. Create an initial 8 puzzle board. Let '0' represent the empty cell. An example is shown below
```
0 1 2
3 4 5
6 7 8
```
2. Run the script using:
```bash
python a_star_manhattan.py input/input_1.txt output/output.txt
```
3. Check the output in `output/output.txt`
