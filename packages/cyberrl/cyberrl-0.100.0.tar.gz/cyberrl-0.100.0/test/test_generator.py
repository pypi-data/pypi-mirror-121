"""Runs bruteforce agent on environment for different scenarios and
using different parameters to check no exceptions occur
"""

import pytest

import cyberrl
from cyberrl.scenarios.benchmark import \
    AVAIL_GEN_BENCHMARKS


@pytest.mark.parametrize("scenario", AVAIL_GEN_BENCHMARKS)
@pytest.mark.parametrize("seed", list(range(100)))
def test_generator(scenario, seed):
    """Tests generating all generated benchmark scenarios using a range of
    seeds, checking for any errors
    """
    cyberrl.make_benchmark(scenario, seed=seed)