import math
import time
import logging
import configparser
from classes.PuzzleParser import PuzzleParser
from classes.Variable import Variable
from classes.Constraint import Constraint

# Config variables & logger
config = configparser.ConfigParser()
config.read('config/config.ini')
LOGGER_NAME = config.get("LOGGER", "LOGGER_NAME")
logger = logging.getLogger(LOGGER_NAME)


class SudokuCSP():
    # Constants
    FAILURE = "FAILURE"
    SLEEP_DELAY = .3

    def __init__(self, file_path, delay=False):
        self.delay = delay
        (puzzle_size, values) = PuzzleParser.parsePuzzle(file_path)
        # just to track the domain somewhere
        self.puzzle_size = int(puzzle_size)
        self.puzzle_size_root = int(math.sqrt(puzzle_size))
        domain = [x + 1 for x in range(0, self.puzzle_size)]
        self.variables = [
            Variable(id=i, domain=domain, value=value)
            for (i, value) in enumerate(values)
        ]
        self.constraints = []
        self.assignment = dict()
        self.defineSudokuConstraints()
        self.updateDomainsAfterConstraints()
        self.actions = []

    def solve(self):
        if (self.delay):
            time.sleep(self.SLEEP_DELAY)
        if(self.goalTest()):
            PuzzleParser.printPuzzle(self)
            return self.assignment
        next_variable = self.getUnassignedVariable()
        possible_values = self.orderDomainValues(next_variable)
        logger.debug(f"-- Looking at {next_variable.id}")
        PuzzleParser.printPuzzle(self)
        for value in possible_values:
            if (self.isAssignmentConsistent(next_variable, value)):
                self.assignVariable(next_variable, value)
                future_solution = self.solve()
                if future_solution is not self.FAILURE:
                    return future_solution
                else:
                    # If the future solution is a failure, or if the current assignment is inconsistent
                    self.unassignVariable(next_variable)
        return self.FAILURE

    # Locally assign and unassign variable to check its consistency,
    def isAssignmentConsistent(self, variable, value):
        self.assignVariable(variable, value, testing_assignment=True)
        isConsistent = self.allConstraintsSatisfied()
        self.unassignVariable(variable, testing_assignment=True)
        return isConsistent

    # Assign a variable a value, and any other associated actions or cleanup
    def assignVariable(self, variable, value, testing_assignment=False):
        try:
            variable.setValue(value)
            if (not testing_assignment):
                self.assignment.update({variable.id: value})
                self.actions.append(f"Assign #{variable.id} to {value} from domain {variable.domain}")
        except Exception as e:
            logger.error(e)

    # Remove a variables assignment, and any other associated actions or cleanup
    def unassignVariable(self, variable, testing_assignment=False):
        variable.resetValue()
        if (not testing_assignment):
            old_value = self.assignment.pop(variable.id, None)
            self.actions.append(f"Unassigned #{variable.id}, value was {old_value}")

    # Enforce some ordering on the domain values so that we can avoid loops
    def orderDomainValues(self, variable):
        domain = variable.domain
        return sorted(domain)

    # Get the next unassignedVariable, returning None if there is none
    def getUnassignedVariable(self):
        unassigned_variables = self.unassignedVariables()
        return unassigned_variables[0] if len(unassigned_variables) > 0 else None

    # Defining the win-condition of the CSP:
    # For sudoku, the game is over when there are 0 unassigned variables and the constraints are all satisfied
    def goalTest(self):
        all_assigned = len(self.unassignedVariables()) == 0
        return all_assigned and self.allConstraintsSatisfied()

    # Returns a list of all variables that do not have a value
    def unassignedVariables(self):
        return [x for x in self.variables if not x.hasValue()]

    # Straightforward
    def allConstraintsSatisfied(self):
        return all(constraint.isSatisfied() for constraint in self.constraints)

    ######################
    # Constraint Helpers
    #####
    # Make a contraint group for every row, col and block in our grid
    def defineSudokuConstraints(self):
        for i in range(self.puzzle_size):
            row = self.getRow(i)
            row_constraint = Constraint(row, self.allDiff)
            self.constraints.append(row_constraint)

            col = self.getCol(i)
            col_constraint = Constraint(col, self.allDiff)
            self.constraints.append(col_constraint)

            block = self.getBlock(i)
            block_constraint = Constraint(block, self.allDiff)
            self.constraints.append(block_constraint)

    # After the constraints have been applied, update all unassignedVariables to scope their domain appropriately
    def updateDomainsAfterConstraints(self):
        # after constraints have been set, update the free-variable domains accordingly
        for var in self.unassignedVariables():
            neighbors = self.getConstrainedNeighbors(var)
            # illegal values are all the ones currently set by variables
            invalid_values = [var.value for var in neighbors if var.hasValue()]
            for value in invalid_values:
                var.removeValueFromDomain(value)
            # lock this as the initial domain for forward-checking weirdness later
            var.lockDomainAsInitial()

    # Iterate over every constraint and get any variables constrained by this one
    def getConstrainedNeighbors(self, variable):
        return list(set([neighbor for c in self.constraints for neighbor in c.getConstrainedGroup(variable)]))

    @ staticmethod
    def allDiff(variables):
        assigned_variables = list(filter(lambda val: val is not None, [v.value for v in variables]))
        return (len(assigned_variables) == len(set(assigned_variables)))

    ###########################
    # Sudoku Grid Operations
    # NOTE: Assumes 0-indexed rows
    #######
    def getRowIndices(self, k):
        startOfRow = 0 if (k <= 0) else (k * self.puzzle_size)
        endOfRow = len(self.variables) if (k >= self.puzzle_size) else ((k + 1) * self.puzzle_size)
        return list(range(startOfRow, endOfRow))

    def getRow(self, k):
        return [self.variables[i] for i in self.getRowIndices(k)]

    # Assumes 0-indexed cols
    def getColIndices(self, k):
        return [k + (i * self.puzzle_size) for i in range(self.puzzle_size)]

    def getCol(self, k):
        return [self.variables[i] for i in self.getColIndices(k)]

    # To get a particular block, we'll get the all the rows and columns associated with that block, and determine the block by set intersection
    def getBlockIndices(self, k):
        block_row = int(k / self.puzzle_size_root)
        block_col = int(k % self.puzzle_size_root)
        # Get the block by evaluating the set intersection of the rows associated with block_row and cols with block_cols
        row_indices = set()
        col_indices = set()
        for k in range(self.puzzle_size_root):
            row = (block_row * self.puzzle_size_root) + k
            col = (block_col * self.puzzle_size_root) + k
            row_indices.update(self.getRowIndices(row))
            col_indices.update(self.getColIndices(col))
        index_union = sorted(list(row_indices & col_indices))
        return index_union

    def getBlock(self, k):
        return [self.variables[i] for i in self.getBlockIndices(k)]
