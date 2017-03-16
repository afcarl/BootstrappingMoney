import numpy as np
from economy import Economy
from graph import graph


def main():

    random_seed = np.random.randint(4294967295)

    parameters = {
        "random_seed": 2997058545,
        "n_generations": 2000,
        "n_periods_per_generation": 50,
        "n_goods": 4,
        "n_agents": 50,
        "p_mutation": 0.1,
        "mating_rate": 0.3
    }

    e = Economy(**parameters)

    backup = e.run()
    graph(results=backup, parameters=parameters)

if __name__ == "__main__":

    main()
