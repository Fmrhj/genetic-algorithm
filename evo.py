import numpy as np

def fitness(x, y):
    return x*(x-1)*np.cos(2*x-1)*np.sin(2*x-1)*(y-2)

def individual(lower_bound=-2, upper_bound=2, number_of_genes=2):
    return [np.random.uniform(lower_bound, upper_bound, 1)[0] for i in range(number_of_genes)]

def generate_initial_population(size, individual_gen, params):
    return [individual_gen(params['lower_bound'], params['upper_bound'], params['number_of_genes']) for s in range(size)]

def get_parents(pop, n_parents, fitness_function):
    pop.sort(key=lambda x: fitness_function(x[0], x[1]), reverse = True)
    return np.array(pop[:n_parents])

def crossover(parents, offspring_size):
    offspring = np.empty(offspring_size)
    crossover_point = np.uint8(offspring_size[0]/2)
    for k in range(offspring_size[1]):
        # Index of the first parent to mate.
         parent1_idx = k%parents.shape[0]
         # Index of the second parent to mate.
         parent2_idx = (k+1)%parents.shape[0]
         # The new offspring will have its first half of its genes taken from the first parent.
         offspring[k, 0:crossover_point] = parents[parent1_idx, 0:crossover_point]
         # The new offspring will have its second half of its genes taken from the second parent.
         offspring[k, crossover_point:] = parents[parent2_idx, crossover_point:]
    return offspring 

def mutate(offspring_crossover):
    for idx in range(offspring_crossover.shape[0]):
        
        # select randomly the gene where randomness is going to be added 
        g = np.random.choice(range(offspring.shape[0]))

        # The random value to be added to the gene.
        offspring_crossover[idx][g] = offspring_crossover[idx][g] + np.random.normal(0.5, 0.25, 1)

    return offspring_crossover

class Individual:
    def __init__(self, value):
        pass

class Population:
    def __init__(self):
        pass
    
    def crossover(self):
        pass

    def mutate(self):
        pass

class Evolution:
    def __init__(self, fitness):
        self.fitness = fitness

    def step(self):
        pass
