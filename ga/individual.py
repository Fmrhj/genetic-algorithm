import numpy as np
from typing import Dict, List
from abc import ABC, abstractmethod

class IndividualBase(ABC):
    @abstractmethod
    def get_values(self):
        pass

class Individual:
    def __init__(self, params:Dict, value: List[np.array]=None):
        if value is None:
            self.value = [
                np.random.uniform(params['lower_bound'], params['upper_bound'], 1)[0]
                for _ in range(params['number_of_genes'])
            ]
        else:
            self.value = value

    def get_values(self) -> List[np.array]:
        return self.value