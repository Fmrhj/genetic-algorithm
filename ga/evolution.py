from abc import abstractmethod
from typing import Dict, Callable, Optional
from ga.population import Population
from abc import abstractmethod, ABC
from dataclasses import dataclass
import numpy as np
@dataclass
class Solution:
    best_individual: np.array
    best_score: Optional[float]

class EvolutionBase(ABC):
    @abstractmethod
    def step(self):
        pass

class Evolution:
    _N_PARENTS_KEY = "n_parents"
    _SIZE_KEY = "size"

    def __init__(self, pop_parameters: Dict, ind_parameters: Dict, fitness_function: Callable):
        self.fitness = fitness_function
        self.population = Population(pop_parameters, ind_parameters, fitness_function)
        self.ind_parameters = ind_parameters
        self.pop_parameters = pop_parameters
        self._best_individual = None
        self._best_score = None

    def step(self) -> None:
        parents = self.population.get_parents(self.pop_parameters[self._N_PARENTS_KEY])
        offspring = self.population.crossover(parents)
        mutation = self.population.mutate(offspring, self.ind_parameters, self.pop_parameters)
        population_values = [
            self.population.individuals[i].get_values()
            for i in range(self.population.size)
        ]
        population_values.extend(mutation)
        population_values.sort(key=lambda x: self.fitness(*x), reverse=True)
        population_values = population_values[:self.pop_parameters[self._SIZE_KEY]]
        self._best_individual = population_values[:1]
        self._best_score = self.fitness(*self._best_individual[0])
        
        # update population
        self.population = Population(self.pop_parameters, self.ind_parameters, self.fitness, population_values)

    @property
    def solution(self) -> Optional[Solution]:
        if self._best_individual is not None:
            return Solution(self._best_individual[0], self._best_score) 
        