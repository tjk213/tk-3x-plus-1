#!/usr/bin/env python3

from argparse import ArgumentParser
from argparse import RawTextHelpFormatter as RTHF

from time import time
from typing import Dict

DESCRIPTION="Brute-force verify the Collatz Conjecture over the given data range."

def three_x_plus_one(x: int, visited: set, maxval : int = 0, steps: int = 0) -> Dict:

    if x in visited:
        return {'verified': False, 'maxval': maxval, 'steps': steps}
    visited.add(x)

    steps += 1
    maxval = max(maxval, x)

    while (x % 2 == 0):
        x = x // 2
        steps += 1

    if x == 1:
        return {'verified': True, 'maxval': maxval, 'steps': steps}
    else:
        return three_x_plus_one(3*x+1, visited, maxval, steps)


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

    args = parser.parse_args()
    stop = 2*args.start if not args.stop else args.stop
    start = args.start if args.start % 2 == 1 else args.start+1

    visited = set()
    overflows = set()

    max_steps = 0
    total_steps = 0
    N = len(range(start, stop))

    tstart = time()
    for i in range(start, stop, 2):
        visited.clear()
        res = three_x_plus_one(i, visited)

        if res['verified'] == False:
            print(f"x = {i}")
            print(f"visited = {visited}")
            raise RuntimeError("Counter found!")

        if res['maxval'] >= 2**32:
            overflows.add(i)
        total_steps += res['steps']
        max_steps = max(max_steps, res['steps'])
    tend = time()


    perc = len(overflows) / N * 100
    avg_steps = total_steps / N
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
