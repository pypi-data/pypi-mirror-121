from typing import Type

import torch
from torch import nn
import optproblems.cec2005 as op
from optproblems.base import TestProblem

from detorch import DE, Policy, Strategy
from detorch.config import default_config, Config


class Problem(Policy):
    def __init__(self, problem=op.F1, dim=1):
        super().__init__()

        f = problem(dim)
        self.f = f
        self.params = nn.Parameter((f.min_bounds[0] - f.max_bounds[0]) * torch.rand(dim) + f.max_bounds[0])

    def evaluate(self):
        self.params.clip_(self.f.min_bounds[0], self.f.max_bounds[0])
        return -abs(self.f(self.params))


config = Config(default_config)


@config('policy')
class PolicyConfig():
    policy: Type[Policy] = Problem
    problem: TestProblem = op.F2
    dim: int = 1


@config('de')
class DEConfig():
    n_step: int = 50
    population_size: int = 256
    differential_weight: float = 0.7
    crossover_probability: float = 0.5
    strategy: Strategy = Strategy.scaledbest1soft
    seed: int = 123123


if __name__ == '__main__':
    de = DE(config)

    @de.selection.add_hook()
    def after_selection(self, *args, **kwargs):
        print(f'Generation: {self.gen} Best Reward: {self.rewards[self.current_best]}')

    de.train()

    print(de.population[de.current_best].params)
