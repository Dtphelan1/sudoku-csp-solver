import logging
import configparser
from classes.SudokuCSP import SudokuCSP

# Config variables & logger
config = configparser.ConfigParser()
config.read('config/config.ini')
LOGGER_NAME = config.get("LOGGER", "LOGGER_NAME")
logger = logging.getLogger(LOGGER_NAME)


class MinimumRemainingValueSudokuCSP(SudokuCSP):
    # Get the next unassignedVariable, returning None if there is none
    # In this improvement, order the unassigned variables in terms of how restricted their domain is
    def getUnassignedVariable(self):
        unassigned_variables = self.unassignedVariables()
        return sorted(unassigned_variables, key=lambda var: len(var.domain))[0] if len(unassigned_variables) > 0 else None

     # Assign a variable a value, and any other associated actions or cleanup
     # In this improvement, that means removing values from neighbor domains
    def assignVariable(self, variable, value, testing_assignment=False):
        try:
            variable.setValue(value)
            if (not testing_assignment):
                self.assignment.update({variable.id: value})
                self.actions.append(f"Assign #{variable.id} to {value} from domain {variable.domain}")
                neighbors = self.getConstrainedNeighbors(variable)
                for n in neighbors:
                    n.removeValueFromDomain(value)
        except Exception as e:
            logger.error(e)

    # Remove a variables assignment, and any other associated actions or cleanup
    # In this improvement, that means restoring values to neighbor domains
    def unassignVariable(self, variable, testing_assignment=False):
        variable.resetValue()
        value = self.assignment.pop(variable.id, None)
        if (not testing_assignment):
            self.actions.append(f"Unassigned #{variable.id}, value was {value}")
            neighbors = self.getConstrainedNeighbors(variable)
            for n in neighbors:
                n.restoreValueToDomain(value)
