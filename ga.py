import numpy as np


def fitness(x, y):
    return x * (x - 1) * np.cos(2 * x - 1) * np.sin(2 * x - 1) * (y - 2)


class Individual:
    def __init__(self, params, value=None):
        if value is None:
            self.value = [
                np.random.uniform(params['lower_bound'], params['upper_bound'],
                                  1)[0]
                for i in range(params['number_of_genes'])
            ]
        else:
            self.value = value

    def get_values(self):
        return self.value


class Population:
    def __init__(self,
                 individual_class,
                 pop_parameters,
                 ind_parameters,
                 fitness_function,
                 ind_values=None):
        self.individual_class = individual_class
        if ind_values is None:
            self.individuals = [
                individual_class(ind_parameters)
                for _ in range(pop_parameters['size'])
            ]
        else:
            self.individuals = [
                individual_class(ind_parameters, value) for value in ind_values
            ]
        self.fitness_function = fitness_function
        self.parents = None
        self.size = pop_parameters['size']
        self.n_parents = pop_parameters['n_parents']
        self.offspring_size = pop_parameters['offspring_size']

    def get_parents(self, n_parents):
        parents = [self.individuals[i].get_values() for i in range(self.size)]
        parents.sort(key=lambda x: self.fitness_function(x[0], x[1]),
                     reverse=True)
        return np.array(parents[:n_parents])

    def crossover(self, parents):
        offspring = np.empty(self.offspring_size)
        crossover_point = np.uint8(self.offspring_size[0] / 2)
        for k in range(self.offspring_size[1]):
            parent1_idx = k % parents.shape[0]
            # Index of the second parent to mate
            parent2_idx = (k + 1) % parents.shape[0]
            # Half of the first parent
            offspring[k, 0:crossover_point] = parents[parent1_idx,
                                                      0:crossover_point]
            # Half if the second parent
            offspring[k, crossover_point:] = parents[parent2_idx,
                                                     crossover_point:]
        return offspring

    def mutate(self, offspring_crossover, ind_params, pop_params):
        for idx in range(offspring_crossover.shape[0]):
            # select randomly the gene where randomness is going to be added
            g = np.random.choice(range(offspring_crossover.shape[0]))

            # The random value to be added to the gene.
            offspring_crossover[idx][g] = offspring_crossover[idx][g] + \
                np.random.normal(pop_params['mutation_mean'], pop_params['mutation_sd'], 1)

            # apply upper and lower bounds
            if offspring_crossover[idx][g] > ind_params['upper_bound']:
                offspring_crossover[idx][g] = ind_params['upper_bound']

            if offspring_crossover[idx][g] < ind_params['lower_bound']:
                offspring_crossover[idx][g] = ind_params['lower_bound']

        return offspring_crossover


class Evolution:
    def __init__(self, fitness, population_class, individual_class,
                 pop_parameters, ind_parameters, fitness_function):
        self.fitness = fitness_function
        self.population_class = population_class
        self.individual_class = individual_class
        self.population = population_class(individual_class, pop_parameters,
                                           ind_parameters, fitness_function)
        self.ind_parameters = ind_parameters
        self.pop_parameters = pop_parameters
        self._best_individual = None
        self._best_score = None

    def step(self):
        parents = self.population.get_parents(self.pop_parameters['n_parents'])
        offspring = self.population.crossover(parents)
        mutation = self.population.mutate(offspring, self.ind_parameters,
                                          self.population_class)
        population_values = [
            self.population.individuals[i].get_values()
            for i in range(self.population.size)
        ]
        population_values.extend(mutation)
        population_values.sort(key=lambda x: self.fitness(x[0], x[1]),
                               reverse=True)
        population_values = population_values[:self.pop_parameters['size']]
        self._best_individual = population_values[:1]
        self._best_score = self.fitness(self._best_individual[0][0],
                                        self._best_individual[0][1])
        # update population
        self.population = self.population_class(self.individual_class,
                                                self.pop_parameters,
                                                self.ind_parameters,
                                                self.fitness,
                                                population_values)
