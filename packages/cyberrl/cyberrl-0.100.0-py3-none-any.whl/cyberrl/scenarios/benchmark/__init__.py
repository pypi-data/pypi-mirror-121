import os.path as osp

from .generated import AVAIL_GEN_BENCHMARKS

BENCHMARK_DIR = osp.dirname(osp.abspath(__file__))

AVAIL_STATIC_BENCHMARKS = {
    "testag": {
        "file": osp.join(BENCHMARK_DIR, "testag.yaml"),
        "name": "testag",
        "step_limit": 1000,
        "max_score": 195
    },
    
    "enterprise": {
        "file": osp.join(BENCHMARK_DIR, "enterprise.yaml"),
        "name": "enterprise",
        "step_limit": 2000,
        "max_score": 190
    },
    "onesite_enterprise": {
        "file": osp.join(BENCHMARK_DIR, "onesite_enterprise.yaml"),
        "name": "onesite_enterprise",
        "step_limit": 2000,
        "max_score": 195
    },
    "multisite_enterprise": {
        "file": osp.join(BENCHMARK_DIR, "multisite_enterprise.yaml"),
        "name": "multisite_enterprise",
        "step_limit": 2000,
        "max_score": 190
    },
}

AVAIL_BENCHMARKS = list(AVAIL_STATIC_BENCHMARKS.keys()) \
                    + list(AVAIL_GEN_BENCHMARKS.keys())
