import torch
from torch import nn
from typing import Type
import numpy as np
import argparse

from detorch import DE, Policy, Strategy
from detorch.config import default_config, Config, Argument


config = Config(default_config)


class Ackley(Policy):
    def __init__(self):
        super().__init__()
        self.params = nn.Parameter(torch.rand(2), requires_grad=False)

    def evaluate(self):
        x = self.params[0]
        y = self.params[1]
        first_term = -20 * torch.exp(-0.2*torch.sqrt(0.5*(x**2+y**2)))
        second_term = -torch.exp(0.5*(torch.cos(2*np.pi*x)+np.cos(2*np.pi*y)))+np.e + 20
        return -(second_term + first_term).item()

class EnumAction(argparse.Action):
    def __init__(self, **kwargs):
        enum_type = kwargs.pop("type", None)
        kwargs['choices'] = tuple(e.name for e in enum_type)
        super(EnumAction, self).__init__(**kwargs)
        self._enum = enum_type

    def __call__(self, parser, namespace, values, option_string=None):
        value = getattr(self._enum, values)
        setattr(namespace, self.dest, value)

@config('policy')
class PolicyConfig():
    policy: Type[Policy] = Ackley


@config('de')
class DEConfig():
    n_step: int = 20
    population_size: int = 256
    differential_weight: float = 0.7
    crossover_probability: float = 0.5
    strategy: Strategy = Argument(default=Strategy.scaledbest1soft, action=EnumAction)
    # strategy: Strategy = Strategy.scaledbest1soft
    seed: int = 123123


if __name__ == '__main__':
    config = config.parse_args()
    de = DE(config)

    @de.selection.add_hook()
    def after_selection(self, *args, **kwargs):
        print(f'Generation: {self.gen} Best Reward: {self.rewards[self.current_best]}')

    de.train()
