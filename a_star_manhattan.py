import os
import sys
from heapq import heappush, heappop
from copy import deepcopy

# This program solves then 8-puzzle problem using an A* GRAPH SEARCH
# algorithm, using the total manhattan distance from the current state
# to the goal state as a heuristic

class Puzzle(object):
    goal_state = None
    def __init__(self, init_state, goal_state):
        Puzzle.goal_state = Puzzle.State(goal_state, calculate_eval_value = False)
        self.init_state = Puzzle.State(init_state, calculate_eval_value = False)

        self.actions = list()
        self.solvable = False
        self.frontier = Puzzle.PriorityQueue()
        self.visited = set()

    # -----------------------------------------------------------------------------------------
    # A* GRAPH SEARCH Algorithm
    def solve(self):
        self.frontier.add(self.init_state)

        while not self.frontier.is_empty():
            current_state = self.frontier.poll()
            if current_state.is_goal_state():
                self.solvable = True
                while current_state.parent is not None:
                    self.actions.append(current_state.move_taken)
                    current_state = current_state.parent
                break
            else:
                possible_states = current_state.calculate_moves()
                for state in possible_states:
                    if state not in self.visited:
                        self.frontier.add(state)
                self.visited.add(current_state)
        self.actions.reverse()
        
        # Return Values
        if not self.solvable:
            return ["UNSOLVABLE"]
        return self.actions

    # -----------------------------------------------------------------------------------------
    # Helper Classes
    class State(object):
        def __init__(self, values, moves = 0, parent = None, move_taken = None, calculate_eval_value = True):
            self.values = values
            self.parent = parent
            self.moves = moves
            self.move_taken = move_taken
            self.evaluation_value = self.calculate_heuristic() + moves if calculate_eval_value else 0

        # Total Manhattan Distance
        def calculate_heuristic(self):
            flattened_values = [item for row in self.values for item in row]
            flattened_goal_state = [item for row in Puzzle.goal_state.values for item in row]
            distance = 0
            for current_idx, current_value in enumerate(flattened_values):
                goal_state_idx = flattened_goal_state.index(current_value)
                (current_row, current_col) = int(current_idx / 3), current_idx % 3
                (goal_state_row, goal_state_col) = int(goal_state_idx / 3), goal_state_idx % 3

                distance += (abs(goal_state_row - current_row) + abs(goal_state_col - current_col))
            return distance

        # Get all possible children states from the current state
        def calculate_moves(self):
            output = []
            for row_idx, row in enumerate(self.values):
                for col_idx, col in enumerate(row):
                    if col != 0:
                        continue

                    # If '0' is in the top two row, a possible state is to move the '0' down
                    if row_idx in [0, 1]:
                        output.append(self.move_zero_down(row_idx, col_idx))

                    # If '0' is in the bottom two row, a possible state is to move the '0' up
                    if row_idx in [1, 2]:
                        output.append(self.move_zero_up(row_idx, col_idx))

                    # If '0' is in the left two cols, a possible state is to move the '0' right
                    if col_idx in [0, 1]:
                        output.append(self.move_zero_right(row_idx, col_idx))

                    # If '0' is in the right two cols, a possible state is to move the '0' left
                    if col_idx in [1, 2]:
                        output.append(self.move_zero_left(row_idx, col_idx))
            return output

        def move_zero_left(self, row, col):
            values = deepcopy(self.values)
            values[row][col-1], values[row][col] = values[row][col], values[row][col-1]
            return Puzzle.State(values, self.moves + 1, self, "RIGHT")
        
        def move_zero_right(self, row, col):
            values = deepcopy(self.values)
            values[row][col+1], values[row][col] = values[row][col], values[row][col+1]
            return Puzzle.State(values, self.moves+1, self, "LEFT")

        def move_zero_up(self, row, col):
            values = deepcopy(self.values)
            values[row-1][col], values[row][col] = values[row][col], values[row-1][col]
            return Puzzle.State(values, self.moves+1, self, "DOWN")

        def move_zero_down(self, row, col):
            values = deepcopy(self.values)
            values[row+1][col], values[row][col] = values[row][col], values[row+1][col]
            return Puzzle.State(values, self.moves+1, self, "UP")

        def is_goal_state(self):
            return self == Puzzle.goal_state
        
        def __hash__(self):
            return hash(str(self.values))

        def __lt__(self, other):
            return self.evaluation_value < other.evaluation_value

        def __eq__(self, other):
            return self.values == other.values

    class PriorityQueue(object):
        def __init__(self):
            self.queue = []
            self.count = 0
            self.current_size = 0
            self.max_size = 0

        def add(self, item):
            heappush(self.queue, item)
            self.count += 1
            self.current_size += 1
            self.max_size = max(self.max_size, self.current_size)

        def poll(self):
            self.current_size -= 1
            return heappop(self.queue)

        def peek(self):
            return self.queue[0]
        
        def is_empty(self):
            return len(self.queue) == 0

if __name__ == "__main__":
    # Do NOT modify below
    if len(sys.argv) != 3:
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        raise IOError("Input file not found!")

    init_state = [[0 for i in range(3)] for j in range(3)]
    goal_state = [[0 for i in range(3)] for j in range(3)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '8':
                init_state[i][j] = int(number)
                j += 1
                if j == 3:
                    i += 1
                    j = 0

    for i in range(1, 9):
        goal_state[(i-1)//3][(i-1) % 3] = i
    goal_state[2][2] = 0

    puzzle = Puzzle(init_state, goal_state)
    ans = puzzle.solve()

    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer+'\n')
