#!/usr/bin/env python3
####################################################################################
##               ,:                                                         ,:    ##
##             ,' |                                                       ,' |    ##
##            /   :                                                      /   :    ##
##         --'   /       :::::::::::   :::::::::::   :::    :::       --'   /     ##
##         \/ />/           :+:            :+:       :+:   :+:        \/ />/      ##
##         / /_\           +:+            +:+       +:+  +:+          / /_\       ##
##      __/   /           +#+            +#+       +#++:++         __/   /        ##
##      )'-. /           +#+            +#+       +#+  +#+         )'-. /         ##
##      ./  :\          #+#        #+# #+#       #+#   #+#         ./  :\         ##
##       /.' '         ###         #####        ###    ###          /.' '         ##
##     '/'                                                        '/'             ##
##     +                                                          +               ##
##    '                                                          '                ##
####################################################################################
##            Copyright © 2023 Tyler J. Kenney. All rights reserved.              ##
####################################################################################
####################################################################################

from argparse import ArgumentParser
from argparse import RawTextHelpFormatter as RTHF

from math import inf
from time import time
from typing import Dict

DESCRIPTION="Brute-force verify the Collatz Conjecture over the given data range."

def three_x_plus_one(x: int):

    k = 0
    x_k = x
    sup = x

    if x == 1:
        return inf, 1, 4

    while True:
        while (x_k % 2 == 0):
            k += 1
            x_k = x_k // 2

            if x_k <= x:
                stoptime = inf if x_k == x else k
                return stoptime, x_k, sup

        k += 1
        x_k = 3*x_k + 1
        sup = max(sup, x_k)

    return


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

    output_parser = parser.add_argument_group(title="Output Options")
    path_var = {"type": str, "metavar": "/path/to/file"}
    output_parser.add_argument("--output", "-o",  **path_var,
                               help="Save results to disk, in CSV format. [Default: None]")

    args = parser.parse_args()
    stop = 2*args.start if not args.stop else args.stop
    start = args.start if args.start % 2 == 1 else args.start+1

    stoptimes = dict()
    N = stop - start
    tstart = time()
    for i in range(start, stop, 2):
        stoptimes[i] = three_x_plus_one(i)

        if i != 1 and stoptimes[i][0] == inf:
            print(f"COUNTER FOUND: x = {i}", file=sys.stderr)
    tend = time()

    if args.output:
        with open(args.output, 'w') as f:
            print("n, stopping_time, kth_iterate, supremum", file=f)
            pairs = list(sorted(stoptimes.items()))
            for p in pairs:
                print(f"{p[0]}, {p[1][0]}, {p[1][1]}, {p[1][2]}", file=f)

    if 1 in stoptimes.keys():
        del stoptimes[1]

    avg_stopping_time = sum([x[0] for x in stoptimes.values()]) / N
    max_stopping_time = max([x[0] for x in stoptimes.values()])
    checks_per_second = N / (tend - tstart)

    print(f'Avg Stopping Time: {avg_stopping_time:6,.2f}')
    print(f'Max Stopping Time: {max_stopping_time:6,.2f}')
    print(f'')
    print(f'Checks Per Second: {checks_per_second:6,.0f}')
    print(f'')
    return


if __name__ == "__main__": main()
