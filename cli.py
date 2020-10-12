import sys
import time
import argparse
import configparser
import logging
import traceback
# NOTE: Import here initializes our logger
import classes.Logger
from classes.SudokuCSPFactory import SudokuCSPFactory
from classes.PuzzleParser import PuzzleParser

# Config variables & logger
config = configparser.ConfigParser()
config.read('config/config.ini')
DEFAULT_PUZZLE = config.get("APP", "DEFAULT_PUZZLE")
LOGGER_NAME = config.get("LOGGER", "LOGGER_NAME")
logger = logging.getLogger(LOGGER_NAME)

# Globals for cli
START_TIME = time.time()


def main():
    parser = argparse.ArgumentParser(
        description='Solve Sudoku puzzles by modelling them as Constraint Satisfaction Problems using a number of CSP solver approaches'
    )
    parser.add_argument(
        "-p",
        "--puzzle_path",
        default=DEFAULT_PUZZLE,
        help="A path to a sudoku puzzle, represented in the format described in this project's README"
    )
    parser.add_argument(
        "-d",
        "--delay",
        default=False,
        help="A delay between variable attempts, for facilitated debugging; defaults to False",
        action="store_true"
    )
    parser.add_argument(
        "-s",
        "--solver",
        default=SudokuCSPFactory.defaultSudokuCSPType(),
        help=f"The solver to use, options are: {SudokuCSPFactory.getSudokuCSPOptions()}; defaults to {SudokuCSPFactory.defaultSudokuCSPType()}"
    )
    args = parser.parse_args()
    logger.critical("Running solver")
    logger.debug(f"With path: {args.puzzle_path}")

    # Parse the problem statement
    CspClass = SudokuCSPFactory.getSudokuCSP(args.solver)
    if (type(CspClass) == str):
        logger.error(CspClass)
        return
    logger.critical(f"Using Solver: {CspClass.__name__}")
    csp = CspClass(args.puzzle_path, delay=args.delay)
    assn = csp.solve()
    if (assn == csp.FAILURE):
        logger.critical("--- FAILURE: Could not find a valid assignment with the following action history")
        for act in csp.actions:
            logger.critical(act)
    else:
        logger.critical("--- SUCCESS: Assignment is as follows")
        logger.critical(sorted(assn.items(), key=lambda key_value_tup: int(key_value_tup[0])))
        PuzzleParser.printPuzzle(csp, level=logging.CRITICAL)
    logger.critical(f"--- RUNTIME:  {(time.time() - START_TIME)} seconds ---")


if __name__ == "__main__":
    main()
