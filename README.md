# tk-3x+1
_On the one hand, to the extent the problem has structure, we can analyze it - yet it is precisely this structure that seems to prevent us from proving that it behaves "randomly". On the other hand, to the extent that the problem is strucureless and "random", we have nothing to analyze and consequently cannot rigorously prove anything. - **Jeffery C. Lagarias**_

[<img src="https://i.ytimg.com/vi/094y1Z2wpJg/maxresdefault.jpg">](https://www.youtube.com/watch?v=094y1Z2wpJg&ab_channel=Veritasium)

## The Most Dangerous Problem in Mathematics
Is the [Collatz Conjecture](https://en.wikipedia.org/wiki/Collatz_conjecture) false? `tk-3x+1` is a high-performance implementation of the Collatz Conjecture which can be used to brute-force verify the hypothesis over wide data ranges.

## Notes

  - We use the ["shortcut" form](https://en.wikipedia.org/wiki/Collatz_conjecture#Statement_of_the_problem) of the Collatz function

## TODO

  - C++ code needs to be updated to match recent features/notation of the python code
    - stopping time rather than total stopping time, no maps, print kth_iterate, etc.
    - input filtering to reduce search space
  - Need to implement [time-space trade-off](https://en.wikipedia.org/wiki/Collatz_conjecture#Time%E2%80%93space_tradeoff)
    - This is probably incompatible with current output; not well suited for anything other than determing finiteness of stopping time.
   
  
