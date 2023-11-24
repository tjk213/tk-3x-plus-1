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
        return inf, 1, 2

    while True:
        while (x_k % 2 == 0):
            k += 1
            x_k = x_k // 2

            if x_k <= x:
                stoptime = inf if x_k == x else k
                return stoptime, x_k, sup

        k += 1
        x_k = (3*x_k + 1) // 2
        sup = max(sup, x_k)

    return

def test_legarias_table1():
    n1, r1 =        1, three_x_plus_one(1)
    n2, r2 =        7, three_x_plus_one(7)
    n3, r3 =       27, three_x_plus_one(27)
    n4, r4 =  2**50-1, three_x_plus_one(2**50-1)
    n5, r5 =  2**50+0, three_x_plus_one(2**50+0)
    n6, r6 =  2**50+1, three_x_plus_one(2**50+1)
    n7, r7 = 2**500-1, three_x_plus_one(2**500-1)
    n8, r8 = 2**500+1, three_x_plus_one(2**500+1)

    assert (r1[0], round(r1[-1]/n1, +0)) == (inf, 2)
    assert (r2[0], round(r2[-1]/n2, +1)) == (7,  3.7)
    assert (r3[0], round(r3[-1]/n3, +0)) == (59, 171)
    assert (r4[0], round(r4[-1]/n4, -6)) == (143, 6.38E8)
    assert (r5[0], round(r5[-1]/n5, +0)) == (1, 1)
    assert (r6[0], round(r6[-1]/n6, +1)) == (2, 1.5)
    assert (r7[0], round(r7[-1]/n7,-86)) == (1828, 1.11E88)
    assert (r8[0], round(r8[-1]/n8, +1)) == (2, 1.5)

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

    output_parser = parser.add_argument_group(title="Output Options", description="")
    path_var = {"type": str, "metavar": "/path/to/file"}
    output_parser.add_argument("--output", "-o",  **path_var,
                               help="Save results to disk, in CSV format.\nDefault: None")

    args = parser.parse_args()
    stop = 2*args.start if not args.stop else args.stop
    start = args.start if args.start % 2 == 1 else args.start+1

    results = dict()
    vals_all =  list(range(start, stop))
    vals_to_check = vals_all[0::2]
    tstart = time()
    for i in vals_to_check:
        results[i] = three_x_plus_one(i)

        if i != 1 and results[i][0] == inf:
            print(f"COUNTER FOUND: x = {i}", file=sys.stderr)
    tend = time()

    if args.output:
        with open(args.output, 'w') as f:
            print("n, stopping_time, kth_iterate, supremum", file=f)
            pairs = list(sorted(results.items()))
            for p in pairs:
                print(f"{p[0]}, {p[1][0]}, {p[1][1]}, {p[1][2]}", file=f)

    stoptimes = [x[0] for x in results.values()]
    stoptimes_excl_inf = list(filter(lambda x: x != inf, stoptimes))

    n_total = len(vals_all)
    n_checked = len(vals_to_check)

    avg_stopping_time = sum(stoptimes_excl_inf) / n_checked
    max_stopping_time = max(stoptimes_excl_inf)

    checks_per_second  = n_checked / (tend - tstart)
    indices_per_second = n_total / (tend - tstart)

    print(f'Avg Stopping Time: {avg_stopping_time:6,.2f}')
    print(f'Max Stopping Time: {max_stopping_time:6,.2f}')
    print(f'')
    print(f' Checks Per Second: { checks_per_second:6,.0f}')
    print(f'Indices Per Second: {indices_per_second:6,.0f}')
    print(f'')
    return


if __name__ == "__main__": main()
