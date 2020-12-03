import json
from random import randint
from copy import deepcopy
import sys

variables = ["Alarm", "Burglary", "Earthquake", "MaryCalls", "JohnCalls"]
values = ["True", "False"]

def main(num_queries, filename):
    output = list()
    for i in range(1, num_queries):
        total_num = randint(3, 5)
        percent_tofind = randint(4, 10) / 10
        num_given = int((1 - percent_tofind) * total_num)
        num_tofind = int(percent_tofind * total_num)

        if num_tofind == 0:
            num_tofind += 1
            num_given -= 1

        remaining_vars = deepcopy(variables)
        given = dict()
        tofind = dict()

        for j in range(num_given):
            index = randint(0, len(remaining_vars) - 1)
            given[remaining_vars[index]] = values[randint(0, 1)]
            remaining_vars = remaining_vars[:index] + remaining_vars[(index + 1):]

        for j in range(num_tofind):
            index = randint(0, len(remaining_vars) - 1)
            tofind[remaining_vars[index]] = values[randint(0, 1)]
            remaining_vars = remaining_vars[:index] + remaining_vars[(index + 1):]

        output.append({
            "index": i,
            "given": given,
            "tofind": tofind
        })

    with open(filename, "w") as f:
        json.dump(output, f, indent = 4)

if __name__ == "__main__":
    print("CREATING QUERY")
    main(int(sys.argv[1]), sys.argv[2])
    print("FINISHED")