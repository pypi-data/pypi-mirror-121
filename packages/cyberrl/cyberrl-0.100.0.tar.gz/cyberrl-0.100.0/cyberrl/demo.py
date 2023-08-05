"""Script for running cyberrl demo

Usage
-----

$ python demo [-ai] [-h] env_name
"""

import os.path as osp

import cyberrl
from cyberrl.agents.dqn_agent import DQNAgent
from cyberrl.agents.keyboard_agent import run_keyboard_agent


DQN_POLICY_DIR = osp.join(
    osp.dirname(osp.abspath(__file__)),
    "agents",
    "policies"
)
DQN_POLICIES = {
    "testag": osp.join(DQN_POLICY_DIR, "testag.pt"),
}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description=(
            "run an agent"
        )
    )
    parser.add_argument("env_name", type=str,
                        help="benchmark scenario name")
    parser.add_argument("-ai", "--run_ai", action="store_true",
                        help=("Run AI policy (currently ony supported for"
                              " 'testag' environment"))
    args = parser.parse_args()

    if args.run_ai:
        assert args.env_name in DQN_POLICIES, \
            ("AI demo only supported for the following environments:"
             f" {list(DQN_POLICIES)}")

    env = cyberrl.make_benchmark(
        args.env_name,
        fully_obs=True,
        flat_actions=True,
        flat_obs=True
    )

    line_break = f"\n{'-'*60}"
    print(line_break)
    print(f"Running Demo on {args.env_name} environment")
    if args.run_ai:
        print("Using AI policy")
        print(line_break)
        dqn_agent = DQNAgent(env, verbose=False, **vars(args))
        dqn_agent.load(DQN_POLICIES[args.env_name])
        ret, steps, goal = dqn_agent.run_eval_episode(
            env, True, 0.01, "readable"
        )
    else:
        pass
    print(line_break)
    print(f"Episode Complete")
    print(line_break)
    if goal:
        print("Goal accomplished. Sensitive target penetrated.")
    print(f"Final Score={ret}")
    print(f"Steps taken={steps}")
