import sys
import json
from copy import deepcopy

class BayesianNetwork(object):
    def __init__(self, structure, values, queries):
        # -----------------------------------------------------------------------------------------
        # GIVEN ATTRIBUTES
        self.variables = structure["variables"]
        self.dependencies = structure["dependencies"]
        self.conditional_probabilities = values["conditional_probabilities"]
        self.prior_probabilities = values["prior_probabilities"]
        self.queries = queries
        self.answer = []
        # -----------------------------------------------------------------------------------------
        # CUSTOM ATTRIBUTES
        self.cpt = dict()
        self.network = dict()
        self.topo_order = list()
        self.topo_group = dict()

    '''
    This function constructs an adjacency list based on the self.dependencies
    The adjacency list is stored as a class attribute at self.network
    '''
    def construct(self):
        # Constructing Network
        for variable in self.variables:
            self.network[variable] = list()
        for variable, dependencies in self.dependencies.items():
            for dependency in dependencies:
                self.network[dependency].append(variable)

        # Constructing CPT
        for variable, cpt in self.conditional_probabilities.items():
            self.cpt[variable] = dict()
            for row in cpt:
                ordered_assignment = [row["own_value"]]
                for dependency in self.dependencies[variable]:
                    dependency_assignment = row[dependency]
                    ordered_assignment.append(dependency_assignment)
                self.cpt[variable][tuple(ordered_assignment)] = row["probability"]

    '''
    This function reads the queries stored in self.queries
    Using the inference by enumeration method, it generates an answer for every query
    The answers are stored in self.answer
    '''
    def infer(self):
        # Topological Sort
        self.topo_order, self.topo_group = BayesianNetwork.topo_sort(self.network, self.variables)

        for query in self.queries:
            index = query["index"]
            query_vars = query["tofind"]
            evidence_vars = query["given"]

            initial_assignment = dict()
            initial_assignment.update(query_vars)
            initial_assignment.update(evidence_vars)

            conditional_probability = self.calculate_probability(initial_assignment)
            normalization_factor = self.calculate_probability(evidence_vars)
            normalized_cond_prob = conditional_probability / normalization_factor

            self.answer.append({
                "index": index,
                "answer": normalized_cond_prob
            })
        return self.answer

    '''
    This function acts as a preprocessing before the actual calculation.
    It first finds the largest topological group number that is in the query.
    It then filters the global topo order by variables that have lower topological
        grouping numbers than the largest_topo_group_num, or same topo group num,
        but is also in the query.
    Basically, this means that we disregard variables that are descendants, or
        sibilings of the most conditioned variable.
    '''
    def calculate_probability(self, initial_assignment):
        # Finding largest topo group number within query
        largest_topo_group_num = 0
        for variable, _ in initial_assignment.items():
            if self.topo_group[variable] >= largest_topo_group_num:
                largest_topo_group_num = self.topo_group[variable]
        
        # Filtering relevant variables based on query
        topo_order = list()
        for variable in self.topo_order:
            if self.topo_group[variable] < largest_topo_group_num:
                topo_order.append(variable)
            elif self.topo_group[variable] == largest_topo_group_num and variable in initial_assignment:
                topo_order.append(variable)

        return self.calculate_probability_helper(topo_order, initial_assignment)

    '''
    This function evaluates the variables in a topological order.
    If the variable has been assigned a value, it will calculate it probability
        based on that value and given conditions
    If the variable has not been assigned a value, it will then attempt to find all
        possible value assignment, which depends on the variables' domains
    '''
    def calculate_probability_helper(self, topo_order, assignment, index = 0):
        # Stop recursion once we have assigned all variables
        if index >= len(topo_order):
            return 1

        # Recursively assign values to variables and 
        # summing out the probability of each valid assignment
        var = topo_order[index]
        total_probability = 0
        if var not in assignment:
            domains = self.variables[var]
            for domain in domains:
                assignment[var] = domain    
                total_probability += (
                    self.find_probability(var, assignment) *
                    self.calculate_probability_helper(topo_order, deepcopy(assignment), index + 1)
                )
        else:
            total_probability += (
                self.find_probability(var, assignment) *
                self.calculate_probability_helper(topo_order, assignment, index + 1)
            )
        return total_probability
            
    '''
    This function calculates the value for a single 'tofind' variable,
        that is P(var|assignment)
    '''
    def find_probability(self, var, assignment):
        value = assignment[var]
        if var not in self.dependencies:
            return self.prior_probabilities[var][value]

        ordered_assignment = [value]
        for dependency in self.dependencies[var]:
            ordered_assignment.append(assignment[dependency])
        return self.cpt[var][tuple(ordered_assignment)]

    # -----------------------------------------------------------------------------------------
    # Additional Methods
    @staticmethod
    def topo_sort(adjacency_list, vertices):
        topo_order = list()
        topo_group = dict()
        visited = set()

        for vertex in vertices:
            if vertex not in visited:
                BayesianNetwork.dfs(adjacency_list, vertex, visited, topo_order, topo_group)
        topo_order.reverse()
        return topo_order, topo_group

    @staticmethod
    def dfs(adjacency_list, vertex, visited, topo_order, topo_group, topo_group_num = 0):
        neighbours = adjacency_list[vertex]
        for neighbour in neighbours:
            if neighbour not in visited:
                visited.add(neighbour)
                BayesianNetwork.dfs(adjacency_list, neighbour, visited, topo_order, topo_group, topo_group_num + 1)
        topo_order.append(vertex)
        topo_group[vertex] = topo_group_num

# -----------------------------------------------------------------------------------------
# You may add more classes/functions if you think is useful. However, ensure
# all the classes/functions are in this file ONLY and used within the
# BayesianNetwork class.
def main():
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 4:
        print ("\nUsage: python b_net_A3_xx.py structure.json values.json queries.json \n")
        raise ValueError("Wrong number of arguments!")

    structure_filename = sys.argv[1]
    values_filename = sys.argv[2]
    queries_filename = sys.argv[3]

    try:
        with open(structure_filename, 'r') as f:
            structure = json.load(f)
        with open(values_filename, 'r') as f:
            values = json.load(f)
        with open(queries_filename, 'r') as f:
            queries = json.load(f)

    except IOError:
        raise IOError("Input file not found or not a json file")

    # testing if the code works
    b_network = BayesianNetwork(structure, values, queries)
    b_network.construct()
    answers = b_network.infer()

if __name__ == "__main__":
    main()