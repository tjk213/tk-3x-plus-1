#!/usr/bin/env python3

from argparse import ArgumentParser
from argparse import RawTextHelpFormatter as RTHF

from time import time
from typing import Dict

DESCRIPTION="Brute-force verify the Collatz Conjecture over the given data range."

def three_x_plus_one(x: int, step_map: dict[int,int] = None, lower_bound: int = None) -> Dict:

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

        if lower_bound and x < lower_bound:
            assert x in step_map.keys(), "Missing index!"
            steps += step_map[x]
            return {'verified': True, 'maxval': maxval, 'steps': steps}

        steps += 1
        maxval = max(maxval, x)
        x = 3*x+1

    return {'verified': True, 'maxval': maxval, 'steps': steps}


def main():
    parser = ArgumentParser(description=DESCRIPTION,
                            formatter_class=lambda prog: RTHF(prog, max_help_position=80))

    range_parser = parser.add_argument_group(
        title="Test Range Options", description="\n"
        "These options control the data range over which the Conjecture will be verified.\n"
        "The start and end points are, respectively, inclusive and exclusive:\n\n"
        "    VerifyCollatzConjecture(i) ∀ i ∈ [start, stop)\n"
    )
    int_arg = {"type": int, "metavar": "<int>"}
    range_parser.add_argument("--start", **int_arg, required=True, help="Starting index.")
    range_parser.add_argument("--stop",  **int_arg, help="Ending index. [Default: 2*start]")

    step_map_parser = parser.add_argument_group(
        title="Step Map Options", description="\n"
        "Step maps are a data structure that point from any index to the number of steps in\n"
        "the conjecture verification. Step maps enable one CC verification run to build on\n"
        "the results from a prior run, which can, in some cases, lead to significant speedups.\n"
        "Step maps are saved in CSV format."
    )

    path_var = {"type": str, "metavar": "/path/to/step/map"}
    step_map_parser.add_argument("--step-map-in",  **path_var, help="Load given step map.")
    step_map_parser.add_argument("--step-map-out", **path_var, help="Save results as step map.")

    args = parser.parse_args()
    stop = 2*args.start if not args.stop else args.stop
    start = args.start if args.start % 2 == 1 else args.start+1

    if args.step_map_in:
        with open(args.step_map_in, 'r') as f:
            header_in = f.readline()
            steps = {int(line.split(',')[0]): int(line.split(',')[1]) for line in f}
        lower_bound = max(steps.keys())
        for i in range(1, lower_bound, 2):
            assert i in steps.keys(), f"Error: Invalid step-map: missing index {i}"
        assert start == lower_bound+2, "Error: Unexpected start value"
    else:
        steps = dict()

    overflows = set()
    N = len(range(start, stop))

    tstart = time()
    for i in range(start, stop, 2):
        res = three_x_plus_one(i, steps, i)

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
