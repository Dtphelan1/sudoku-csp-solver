import time
import logging
import configparser
from classes.SudokuCSP import SudokuCSP
from classes.PuzzleParser import PuzzleParser
from classes.Variable import Variable

# Config variables & logger
config = configparser.ConfigParser()
config.read('config/config.ini')
LOGGER_NAME = config.get("LOGGER", "LOGGER_NAME")
logger = logging.getLogger(LOGGER_NAME)


class ConflictDirectedBackjumpingSudokuCSP(SudokuCSP):
    def __init__(self, file_path, delay=False):
        super().__init__(file_path=file_path, delay=delay)
        self.conflict_set_variable_pointer = None

    # Modify the solve algorithm to register conflicts when failure occurs
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
                # If the future solution is a failure, or if the current assignment is inconsistent, remove the assignment
                self.unassignVariable(next_variable)
        # After you've tried all possible values for this variable, register a pointer to a conflicted_variable
        self.registerConflicts(next_variable)
        return self.FAILURE

    # Given a variable's failure, inspect its conflict set for conflicting variable to use in our next assignment
    def registerConflicts(self, prev_variable):
        current_conflict_set = prev_variable.conflict_set
        if (len(current_conflict_set) == 0):
            return
        conflict_variable = current_conflict_set.pop()
        self.mergeConflictSets(conflict_variable, prev_variable)
        self.conflict_set_variable_pointer = conflict_variable

    # Given a new variable and an old variable, merge their conflict set, careful not to include the new_variable it it's own conflict set
    def mergeConflictSets(self, new_variable, old_variable):
        new_variable.conflict_set = [var for var in (set(new_variable.conflict_set) | set(old_variable.conflict_set)) if var is not new_variable]

    # Get the next unassignedVariable, returning None if there is none
    # In this improvement, we check to see if there's a conflict_set_prioritized variable to use
    def getUnassignedVariable(self):
        if self.conflict_set_variable_pointer:
            variable = self.conflict_set_variable_pointer
            self.conflict_set_variable_pointer = None
            return variable
        unassigned_variables = self.unassignedVariables()
        return unassigned_variables[0] if len(unassigned_variables) > 0 else None

    # Assign a variable a value, and any other associated actions or cleanup
    # In this improvement, we perform the value removal like in MRV, but we also track conflict-sets
    def assignVariable(self, variable, value, testing_assignment=False):
        try:
            variable.setValue(value)
            if (not testing_assignment):
                self.assignment.update({variable.id: value})
                self.actions.append(f"Assign #{variable.id} to {value} from domain {variable.domain}")
                neighbors = self.getConstrainedNeighbors(variable)
                for n in neighbors:
                    did_remove = n.removeValueFromDomain(value)
                    if did_remove:
                        n.addVariableToConflictSet(variable)
        except Exception as e:
            logger.error(e)

    # Remove a variables assignment, and any other associated actions or cleanup
    # In this improvement, we perform the value restoration like in MRV, but we also update conflict sets
    def unassignVariable(self, variable, testing_assignment=False):
        variable.resetValue()
        value = self.assignment.pop(variable.id, None)
        if (not testing_assignment):
            self.actions.append(f"Unassigned #{variable.id}, value was {value}")
            neighbors = self.getConstrainedNeighbors(variable)
            for n in neighbors:
                did_restore = n.restoreValueToDomain(value)
                if did_restore:
                    n.removeVariableFromConflictSet(variable)
