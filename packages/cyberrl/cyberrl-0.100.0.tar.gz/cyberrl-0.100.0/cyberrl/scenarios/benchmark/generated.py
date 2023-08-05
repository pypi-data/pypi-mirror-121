"""A collection of definitions for generated benchmark scenarios.

Each generated scenario is defined by the a number of parameters that
control the size of the problem (see scenario.generator for more info):

There are also some parameters, where default values are used for all
scenarios, see DEFAULTS dict.
"""

# generated environment constants
DEFAULTS = dict(
    num_exploits=None,
    num_privescs=None,
    r_sensitive=100,
    r_user=100,
    exploit_cost=1,
    exploit_probs='mixed',
    privesc_cost=1,
    privesc_probs=1.0,
    service_scan_cost=1,
    os_scan_cost=1,
    subnet_scan_cost=1,
    process_scan_cost=1,
    uniform=False,
    alpha_H=2.0,
    alpha_V=2.0,
    lambda_V=1.0,
    random_goal=False,
    base_host_value=1,
    host_discovery_value=1,
    step_limit=1000
)

# Generated Scenario definitions
TESTAG_GEN = {**DEFAULTS,
            "name": "testag-gen",
            "num_hosts": 3,
            "num_os": 1,
            "num_services": 1,
            "num_processes": 1,
            "restrictiveness": 1}

AVAIL_GEN_BENCHMARKS = {
    "testag-gen": TESTAG_GEN,
}
