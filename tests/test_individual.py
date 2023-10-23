import pytest

from ga.individual import Individual


@pytest.fixture
def invididual_instance() -> Individual:
    params = {
        "lower_bound": 1,
        "upper_bound": 10,
        "number_of_genes": 100
    }
    return Individual(params=params)


def test_individual_values(invididual_instance: Individual):
    candidate_values = invididual_instance.get_values()
    assert len(candidate_values) == 100
    assert min(candidate_values) >= 1
    assert max(candidate_values) <= 10
