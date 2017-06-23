import numpy as np


class Agent(object):

    name = "Agent"

    def __init__(self, u, production, production_difficulty, exchange_strategies, production_costs, n_goods, idx, model):

        self.n_goods = n_goods
        self.idx = idx
        self.stock = np.zeros(self.n_goods, dtype=int)

        self.production = np.asarray(production, dtype=int)
        self.production_difficulty = np.asarray(production_difficulty)
        self.production_costs = np.asarray(production_costs)

        self.exchange_strategies = exchange_strategies

        self.u = u
        self.mod = model

        self.n_consumption = 0
        self.fitness = 0

        self.exchange = None

        self.involved = False
        self.goal = None
        self.current_strategy = None
        self.step = 0


    def produce(self):

        self.stock += self.production

    def which_exchange_do_you_want_to_try(self):

        if not self.involved:

            min_stock = min(self.stock)
            self.goal = np.random.choice(np.arange(self.n_goods)[self.stock == min_stock])

            max_stock = max(self.stock)
            to_be_sold = np.random.choice(np.arange(self.n_goods)[self.stock == max_stock])

            self.current_strategy = self.exchange_strategies[(to_be_sold, self.goal)]
            exch_hist = self.mod.hist.back_up["n_strategies"][self.mod.t]
            exch_hist[self.current_strategy] = exch_hist.get(self.current_strategy, 0) + 1

            self.step = 0
            self.involved = True

        self.exchange = self.current_strategy[self.step]

        return self.exchange

    def consume(self):

        n_consumption_t = min(self.stock)
        if n_consumption_t:
            self.stock[:] -= n_consumption_t
            self.n_consumption += n_consumption_t

    def proceed_to_exchange(self):

        self.stock[self.exchange[0]] -= 1
        self.stock[self.exchange[1]] += 1

        if self.exchange[1] == self.goal:
            self.involved = False

        else:
            self.step += 1

    def compute_fitness(self):

        pos = self.u * self.n_consumption
        neg = sum(self.production * self.production_costs * self.production_difficulty)

        self.fitness = \
            pos - neg

        return self.fitness

    def reset(self):

        self.stock[:] = 0
        self.fitness = 0
        self.n_consumption = 0
        self.involved = False
