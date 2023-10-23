import numpy as np
import pytest

from ga.evolution import Evolution, Solution

NUMBER_OF_GENES = 2
MANY_ITERATIONS = 100


def fitness(x: int | float, y: int | float) -> float:
    return x * (x - 1) * np.cos(2 * x - 1) * np.sin(2 * x - 1) * (y - 2)


@pytest.fixture
def individual_params() -> dict:

    return {"lower_bound": -2,
            "upper_bound": 2,
            "number_of_genes": NUMBER_OF_GENES}


@pytest.fixture
def population_params() -> dict:
    return {"n_parents": 6,
            "offspring_size": (NUMBER_OF_GENES, NUMBER_OF_GENES),
            "mutation_mean": 0.25,
            "mutation_sd": 0.5,
            "size": 10
            }


def test_one_iteration(population_params: dict,
                       individual_params: dict):
    def fitness(x: int | float, y: int | float) -> float:
        return x * (x - 1) * np.cos(2 * x - 1) * np.sin(2 * x - 1) * (y - 2)

    evo = Evolution(population_params,
                    individual_params,
                    fitness)

    for _ in range(1):
        evo.step()

    assert evo.solution
    assert all([isinstance(solution, float)
               for solution in evo.solution.best_individual])
    assert len(evo.solution.best_individual) == NUMBER_OF_GENES
    assert isinstance(evo.solution, Solution)


def test_many_iterations(population_params: dict,
                         individual_params: dict):

    evo = Evolution(population_params,
                    individual_params,
                    fitness)

    for _ in range(MANY_ITERATIONS):
        evo.step()

    assert evo.solution
    assert all([isinstance(solution, float)
               for solution in evo.solution.best_individual])
    assert len(evo.solution.best_individual) == NUMBER_OF_GENES
    assert isinstance(evo.solution, Solution)
