# Constraint Satisfaction Problem - Sudoku Solver
This repository contains an implementation of a constraint satisfaction problem (CSP) solver, one catered towards solving Sudoku puzzles. 

## Solution:
One of the questions called out in the problem spec was "Could Conflict-directed Backjumping be used?" The answer is yes, and so this repository implements that approach on top of the straightforward CSP solver. In addition, this repository implements the Least Constrained Value improvement, as well as the Minimum Remaining Value improvement in separate classes. One can use the CLI to switch between CSP solvers and compare the run-times manually. Instructions for using the CLI are provided below. 

I've used the `timeit` module to perform some benchmarking (NOTE: the log-level was set to `WARN` when running; different levels and print statements may vary the results you see). Below is a table of my findings, but there is some additional context I can offer. In a straightforward implementation of Sudoku as a CSP (labeled "straightforward" below) the Conflict-directed Backjumping approach is the most performant for hard puzzles, this straightforward implementation misses a crucial piece of information contained in the problem structure, one that any self-respecting puzzle solver will take before-hand. Since all sudoku puzzles come with partially filled-in cells, we can cull the 'true' initial domains of our variables accordingly. Said another way: in our initial state, the domain of each variable isn't simply 1-9; rather, variables can be constrained based on the initial values on the board when the puzzle is constructed. To do this, I've defined a function in the `SudokuCSP` class, `updateDomainsAfterConstraints`, and added to our `Variable` class the ability to lock the current domain as the true initial_domain of the variable. With this improvement added (labelled "With Domain Culling"), benchmarking demonstrates speed-ups across the board. Importantly, speed-ups approach orders-of-magnitude in difference for MRV/LCV approaches. This makes sense, since both approaches benefit early-on from the reduced domain sizes of potential variables

| Solver Type | Easy, Straightforward (n=10) | Hard, Straightforward (n=10) | Easy, With Domain Culling (n=10) | Hard, With Domain Culling (n=10) |
|-------------|------------------------------|------------------------------|----------------------------------|----------------------------------|
| Simple      | 0.27564029040000004s         | 4.481068142300001s           | 0.1591175367s                    | 2.6720516678s                    |
| MRV         | 0.22340652380000003s         | 7.9292556807s                | 0.0163756366s                    | 0.30885527710000005s             |
| LCV         | 0.1879437256s                | 5.0104542265s                | 0.0189222386s                    | 1.3317150736s                    |
| CBG         | 0.22587920339999998s         | 3.4320174049000003s          | 0.1676099129s                    | 2.4213584793s                    |



## Setting Up The Code
This code was written using python version `3.7.5`, managed with `pyenv` and `pyenv-virtualenv`. Thankfully, however, this solution is lightweight/un-optimized enough to not need external packages, leveraging just the default modules supplied with python. Just make sure you are running it against python 3.7.5 or higher

## Running The Code 
Running `python cli.py -h` displays the following help-text
```
usage: cli.py [-h] [-p PUZZLE_PATH] [-d] [-s SOLVER]

Solve Sudoku puzzles by modelling them as Constraint Satisfaction Problems
using a number of CSP solver approaches

optional arguments:
  -h, --help            show this help message and exit
  -p PUZZLE_PATH, --puzzle_path PUZZLE_PATH
                        A path to a sudoku puzzle, represented in the format
                        described in this project's README
  -d, --delay           A delay between variable attempts, for facilitated 
                        debugging; defaults to False
  -s SOLVER, --solver SOLVER
                        The solver to use, options are: ['def', 'mrv', 'lcv',
                        'cbg']; defaults to def
```
Example puzzles you can run against can be found in the `data` directory. Below are examples of valid CLI usage from the source directory: 
```bash
# Run the ConflictDirectedBackjumping solver against the hard puzzle
python cli.py -p ./data/hard.txt -s cbg
```
```bash
# Runs the LeastConstrainingValue solver against the default (easy) puzzle with a delay
python cli.py -p ./data/easy.txt -s lcv -d
```
```bash
# Runs the basic SudokuCSP solver against the default (easy) puzzle
python cli.py
```

### Puzzle Format
Examples of the puzzle format can be found in `./data`. In short, the cells are comma-delimited, and the rows are newline-, `\n`-, delimited. Blank spaces are encoded with a `_` character, and the leading line of the file specifies the puzzle-size dimensions (e.g. is this a 4x4, a 9x9, a 16x16, etc). The only sizes tested are 4 and 9, but I'm curious to see if 16 could also be managed by the existing codebase. 

## Troubleshooting
Below are some suggestions for where to look when trying to understand why a particular puzzle isn't solving

### Running tests 
To run the available tests: 
```bash
python -m unittest discover -s ./tests -p "*_test.py"
```

### Benchmarking
I've provided a `timing.py` file, which is a simple wrapper on top of the CLI itself. This means that it accepts arguments in the same fashion. Feel free to run similar experiments. The number of runs is defined in the configuration file. For edification, here's an example command that runs `timing.py`:
```bash
# run the benchmarking script against the ConflictDirectedBackjumping solver with the default (easy) puzzle
python timing.py -s cbg 
```

### Debugging
Some tips and tricks for debugging the code-base
- `./config/config.ini` contains a few global variables that can be modified to facilitate debugging. Specifically, changing the log level to `INFO` or even `DEBUG` will provide for greater granularity of error checking
- As mentioned above, the CLI argument `delay` can be helpful in getting a better understanding changes between board states. After changing the log level, add the `-d` flag to your CLI arguments to slow down the rate at which new variables are explored
- (Not to be too assuming) Make sure that your puzzle is formatted properly and is valid. If a valid assignment isn't produced by any approach, it's possible that there is an issue with the configuration/encoding of the problem. Specifically, `\n` is as assumed newline character and may need to be modified on Windows environments.
