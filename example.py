import numpy as np
from ga.evolution import Evolution

# Define a fitness function
def fitness(x, y):
    return x * (x - 1) * np.cos(2 * x - 1) * np.sin(2 * x - 1) * (y - 2)

# Define parameter for each individual
ind_parameters = {'lower_bound': -2,
                  'upper_bound': 2,
                  'number_of_genes': 2}

# Define parameter for the entire population
pop_parameters = {'n_parents': 6,
                  'offspring_size':(2, ind_parameters['number_of_genes']),
                  'mutation_mean': 0.25,
                  'mutation_sd': 0.5,
                  'size': 10}
def example():
    # Instantiate an evolution
    evo = Evolution(pop_parameters, ind_parameters, fitness)
    # Repeat evolution step 200 epochs
    EPOCHS = 10000
    # Record fitness history 
    history = []
    x_history = []
    y_history = []
    for _ in range(EPOCHS):
        print('Epoch {}/{}, Progress: {}%\r'.format(_+1, EPOCHS, np.round(((_+1)/EPOCHS)*100, 2)), end="")
        evo.step()
        history.append(evo.solution.best_score)
        x_history.append(evo.solution.best_individual[0])
        y_history.append(evo.solution.best_individual[1])
    
    if evo.solution:
        print('\nResults:')
        print('Best individual:', evo.solution.best_individual)
        print('Fitness value of best individual:', evo.solution.best_score)

example()
    