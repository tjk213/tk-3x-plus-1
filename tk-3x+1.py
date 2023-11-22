#!/usr/bin/env python3

from argparse import ArgumentParser
from argparse import RawTextHelpFormatter as RTHF

from time import time
from typing import Dict

DESCRIPTION="Brute-force verify the Collatz Conjecture over the given data range."

def three_x_plus_one(x: int) -> Dict:

    steps = 0
    maxval = x
    visited = set()

    while True:
        if x in visited:
            return {'verified': False, 'maxval': maxval, 'steps': steps}
        visited.add(x)

        while (x % 2 == 0):
            x = x // 2
            steps += 1

        if x == 1:
            break

        steps += 1
        maxval = max(maxval, x)
        x = 3*x+1

    return {'verified': True, 'maxval': maxval, 'steps': steps}


def main():
    parser = ArgumentParser(description=DESCRIPTION,
                            formatter_class=lambda prog: RTHF(prog, max_help_position=80))

    range_parser = parser.add_argument_group(
        title="Test Range Options",
        description="\nThese options control the data range over which the Conjecture will be verified.\n"
        "The start and end points are, respectively, inclusive and exclusive:\n"
        "\n"
        "    VerifyCollatzConjecture(i) ∀ i ∈ [start, stop)\n"
    )
    range_parser.add_argument("--start", type=int, metavar="<int>", required=True, help="Starting index.")
    range_parser.add_argument("--stop", type=int, metavar="<int>", default=None, help="Ending index. [Default: 2*start]")

    step_map_parser = parser.add_argument_group(
        title="Step Map Options", description="\n"
        "Step maps are a data structure that point from any index to the number of steps in\n"
        "the conjecture verification. Step maps enable one CC verification run to build on\n"
        "the results from a prior run, which can, in some cases, lead to significant speedups.\n"
        "Step maps are saved in CSV format."
    )
    step_map_parser.add_argument("--step-map-in", type=str, metavar="/path/to/step/map", help="Load given step map.")
    step_map_parser.add_argument("--step-map-out",type=str, metavar="/path/to/step/map", help="Save results as step map.")

    args = parser.parse_args()
    stop = 2*args.start if not args.stop else args.stop
    start = args.start if args.start % 2 == 1 else args.start+1

    steps = dict()

    overflows = set()

    N = len(range(start, stop))

    tstart = time()
    for i in range(start, stop, 2):
        res = three_x_plus_one(i)

        if res['verified'] == False:
            print(f"x = {i}")
            raise RuntimeError("Counter found!")

        if res['maxval'] >= 2**32:
            overflows.add(i)
        steps[i] = res['steps']
    tend = time()

    if args.step_map_out:
        with open(args.step_map_out, 'w') as f:
            print("index, steps", file=f)
            pairs = list(sorted(steps.items()))
            for p in pairs:
                print(f"{p[0]}, {p[1]}", file=f)

    perc = len(overflows) / N * 100
    total_steps = sum(steps.values())
    avg_steps = total_steps / N
    max_steps = max(steps.values())
    checks_per_second = N / (tend - tstart)

    #print(f'Collatz Conjecture Confirmed.')
    #print(f'\n')
    print(f'Overflows: {len(overflows):6,.2f} ({perc:.3f}%)')
    print(f'Avg Steps: {avg_steps:6,.2f}')
    print(f'Max Steps: {max_steps:6,.2f}')
    print(f'\n')
    print(f'Checks Per Second: {checks_per_second:6,.0f}')
    print(f'\n')
    return


if __name__ == "__main__": main()
