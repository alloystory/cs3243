import sys
import copy
from Queue import Queue

class CSP(object):
    def __init__(self):
        self.variables = [(x, y) for x in xrange(9) for y in xrange(9)]
        self.domains = dict()
        for x in xrange(9):
             for y in xrange(9):
                 self.domains[(x,y)] = set(range(1,10))
                 
        self.constraints = dict()
        for x in xrange(9):
            for y in xrange(9):
                self.constraints[(x, y)] = set()
                self.constraints[(x, y)].update(set((a, y) for a in xrange(9)))
                self.constraints[(x, y)].update(set((x, b) for b in xrange(9)))
                self.constraints[(x, y)].update(set((int(x / 3) * 3 + a, int(y / 3) * 3 + b) for a in xrange(3) for b in xrange(3)))
                self.constraints[(x, y)].discard((x, y))

class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle                    # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle)        # self.ans is a list of lists
        self.csp = CSP()

    def readPuzzle(self):
        queue = Queue()
        for x in xrange(9):
            for y in xrange(9):
                if self.puzzle[x][y] != 0:
                    target_cell = (x, y)
                    self.csp.domains[target_cell] = set([self.puzzle[x][y]])
                    for neighbour in self.csp.constraints[target_cell]:
                        queue.put((neighbour, target_cell))

        return queue

    def AC3(self, queue = Queue()):
        # Make cell_i consistent with cell_j
        while not queue.empty():
            cell_i, cell_j = queue.get()
            if self.revise(cell_i, cell_j):
                if len(self.csp.domains[cell_i]) == 0:
                    return False
                for cell_i_neighbour in self.csp.constraints[cell_i]:
                    queue.put((cell_i_neighbour, cell_i))
        return True

    def revise(self, cell_i, cell_j):
        revised = False
        rejected_values = set()

        for value in self.csp.domains[cell_i]:
            reduced_cell_j_domain = self.csp.domains[cell_j] - set([value])
            if len(reduced_cell_j_domain) == 0:
                rejected_values.add(value)
                revised = True

        self.csp.domains[cell_i] = self.csp.domains[cell_i] - rejected_values
        return revised

    def backtrackSearch(self):
        unconfirmed_cells = list()
        for cell, domain in self.csp.domains.items():
            if len(domain) > 1:
                unconfirmed_cells.append(cell)

        if self.backtrackSearchHelper(unconfirmed_cells):
            for cell in self.csp.variables:
                self.ans[cell[0]][cell[1]] = self.csp.domains[cell].pop()

    def backtrackSearchHelper(self, unconfirmed_cells):
        if not unconfirmed_cells:
            return True
        
        unconfirmed_cells.sort(key = lambda cell: len(self.csp.domains[cell]), reverse = True)
        cell = unconfirmed_cells.pop()

        copied_domains = copy.deepcopy(self.csp.domains)
        cell_domain = self.csp.domains[cell]

        for value in cell_domain:
            self.csp.domains[cell] = set([value])
            affected_arcs = Queue()
            
            for neighbour in self.csp.constraints[cell]:
                affected_arcs.put((neighbour, cell))

            if self.AC3(affected_arcs):
                result = self.backtrackSearchHelper(unconfirmed_cells)
                if result:
                    return True
            self.csp.domains = copied_domains
        unconfirmed_cells.append(cell)
        return False

    def solve(self):
        #TODO: Your code here
        initial_queue = self.readPuzzle()
        self.AC3(initial_queue)
        self.backtrackSearch()

        return self.ans

    # you may add more classes/functions if you think is useful
    # However, ensure all the classes/functions are in this file ONLY

if __name__ == "__main__":
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 3:
        print ("\nUsage: python sudoku_A2_xx.py input.txt output.txt\n")
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print ("\nUsage: python sudoku_A2_xx.py input.txt output.txt\n")
        raise IOError("Input file not found!")

    puzzle = [[0 for i in range(9)] for j in range(9)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0

    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()

    with open(sys.argv[2], 'w') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")