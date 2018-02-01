# Simple implementation of a crosswords puzzle solver in Python

## Run the solver

Simply run

```bash
> python main.py
```

You can change the source file for the crosswords directly in `main.py`

## Explainations

The solver works with constraint programming. The global idea is to create two variables:

1. **For the individual letter slots**: They can be any of the letters in our word bank
1. **For the word slots**: The slots will be identified with their line/column, starting column/line, ending columns/line and orientation. They can be any of the words, as long as the size matches

We will then constrain every word slot and every letter slot together, with the idea that if a word is in this particular spot, then the first letter has to be `x`, the second `y` and so on.

The package `constraint_programming` takes care of the rest.

### Parsing

Parsing is straightforward. We enumerate each character, skip the `#` and keep a boolean helper to know when we are parsing a word or not. To save time, only the lines are parsed on the first run. The table is then changed to a matrix, transposed and turned back into lists, and the same algorithm runs agains, thus parsing the columns.

### Creating variables and constraints

The variables names were chosen to easily know the underlying structure. They are initialized with all the letters for the letter slots, and the suitable words for the ords slots.

The binary constraints are set on every pair `word_slot/letter_slot`: for every pair, we associate a set of tuples (`word, letter` ) where if the word is in the spot, then the letter in the letter slot is the one imposed by the word.

Those constraints are enough to make it work !

## Tests and time

| Test ID | Arc Consistence | Time |
| - | - | - |
| 1 | True | 3.479 s |
| 2 | True | 2.811 s |
| 3 | True | 2.925 s |
| 4 | False | 2.859 s |
| 5 | False | 3.431 s |
| 6 | False | 2.841 s |

Tests were run on a MacBook Air i7@2*1.7 GHz, 8GB DDR3

There is no difference when maintaining arc consistency or not.

## Constraint Programming

`constraint_programming.py` was entirely developped by C. Dürr at Ecole Centrale Supélec.

---
Charles Ferault