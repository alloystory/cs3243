from pomegranate import *
from itertools import product
import json, sys

def create_model():
    burglary = DiscreteDistribution({'True': 0.01, 'False': 0.99})
    earthquake = DiscreteDistribution({'True': 0.02, 'False': 0.98})
    alarm = ConditionalProbabilityTable(
        [['True', 'True', 'True', 0.95],
        ['True', 'True', 'False', 0.05],
        ['True', 'False', 'True', 0.94],
        ['True', 'False', 'False', 0.06],
        ['False', 'True', 'True', 0.29],
        ['False', 'True', 'False', 0.71],
        ['False', 'False', 'True', 0.001],
        ['False', 'False', 'False', 0.999]
        ], [burglary, earthquake]
    )
    john_calls = ConditionalProbabilityTable(
        [['True', 'True', 0.90],
        ['True', 'False', 0.10],
        ['False', 'True', 0.05],
        ['False', 'False', 0.95]
        ], [alarm]
    )
    mary_calls = ConditionalProbabilityTable(
        [['True', 'True', 0.70],
        ['True', 'False', 0.30],
        ['False', 'True', 0.01],
        ['False', 'False', 0.99]
        ], [alarm]
    )

    s1 = Node(burglary, name="Burglary")
    s2 = Node(earthquake, name="Earthquake")
    s3 = Node(alarm, name="Alarm")
    s4 = Node(john_calls, name="JohnCalls")
    s5 = Node(mary_calls, name="MaryCalls")

    model = BayesianNetwork("bay_network_1")
    model.add_states(s1, s2, s3, s4, s5)
    model.add_edge(s1, s3)
    model.add_edge(s2, s3)
    model.add_edge(s3, s4)
    model.add_edge(s3, s5)
    model.bake()
    
    return model

def calculate(given, toFind, model, count):
    find_map_idx = {
        'Burglary':0,
        'Earthquake':1,
        'Alarm':2,
        'JohnCalls':3,
        'MaryCalls':4
    }
    total_probability = 1

    for key, value in toFind.items():
        obj = model.predict_proba(given)[find_map_idx[key]]

        obj_items = obj.items()
        for value_assignment, probability in obj_items:
            if value_assignment == value:
                total_probability = total_probability * probability

    return {
        'index': count,
        'answer': total_probability
    }

def main():
    # Loading
    model = create_model()
    # with open(sys.argv[1], "r") as query_input:
    #     query_array = json.load(query_input)
    
    one = model.probability(["True", None, "True", None, None])
    # two = model.probability([None, None, None, "True", None])
    print(one)
    # print(two)
    # print(one / two)
    beliefs = model.predict_proba({
        "Alarm": "True"
    })

    print("\n".join("{}\t{}".format(state.name, belief) for state, belief in zip(model.states, beliefs)))


    # # Calculating
    # output_data = []
    # count = 1
    # for query in query_array:
    #     output_data.append(calculate(query["given"], query["tofind"], model, count))
    #     count += 1

    # with open(sys.argv[2], "w") as output_file:
    #     json.dump(output_data, output_file, indent = 4)

if __name__ == "__main__":
    print("STARTING")
    main()
    print("COMPLETED")