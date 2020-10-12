import unittest
# NOTE: Import here initializes our logger
import classes.Logger
from classes.SudokuCSP import SudokuCSP
from classes.PuzzleParser import PuzzleParser

# global test fixture paths
one_missing_path = "tests/fixtures/1_missing.txt"
finished_path = "tests/fixtures/finished.txt"
half_finished_path = "tests/fixtures/half_finished.txt"
invalid_path = "tests/fixtures/invalid.txt"


class SudokuCSPTest(unittest.TestCase):
    def test_constructor(self):
        one_missing = SudokuCSP(file_path=one_missing_path)
        # Should only be one variable missing a value
        unassigned_variable_list = [var for var in one_missing.variables if var.value == None]
        self.assertEqual(len(unassigned_variable_list), 1)
        unassigned_variable = unassigned_variable_list[0]
        # Assignment and action history should be empty
        self.assertEqual(one_missing.assignment, dict())
        self.assertEqual(one_missing.actions, [])
        # The number of constraints in the puzzle should equal puzzle_size * 3 (one for each row, col and block)
        self.assertEqual(len(one_missing.constraints), one_missing.puzzle_size * 3)
        # The domain of unassigned variables should be updated so that 15/16 have empty domains, and one should have a single-value domain
        unassigned_variable_domain = unassigned_variable.domain
        self.assertEqual(len(unassigned_variable_domain), 1)

    def test_unassigned_variables(self):
        one_missing = SudokuCSP(file_path=one_missing_path)
        self.assertEqual(len(one_missing.unassignedVariables()), 1)
        finished = SudokuCSP(file_path=finished_path)
        self.assertEqual(len(finished.unassignedVariables()), 0)
        half_finished = SudokuCSP(file_path=half_finished_path)
        self.assertEqual(len(half_finished.unassignedVariables()), 8)

    def test_all_constraints_satisfied(self):
        one_missing = SudokuCSP(file_path=one_missing_path)
        invalid = SudokuCSP(file_path=invalid_path)
        self.assertEqual(one_missing.allConstraintsSatisfied(), True)
        self.assertEqual(invalid.allConstraintsSatisfied(), False)
        # Adding a value from unassigned variables domains should maintain this condition
        unassigned_variable = one_missing.unassignedVariables()[0]
        unassigned_domain = unassigned_variable.domain
        unassigned_variable.setValue(unassigned_domain[0])
        self.assertEqual(one_missing.allConstraintsSatisfied(), True)
        unassigned_variable.resetValue()
        # Adding a value not in the unassigned variable's domain should fail this condition
        invalid_value = [x + 1 for x in range(one_missing.puzzle_size) if (x + 1) not in unassigned_domain][0]
        unassigned_variable.value = invalid_value
        self.assertEqual(one_missing.allConstraintsSatisfied(), False)

    def test_goal_test(self):
        one_missing = SudokuCSP(file_path=one_missing_path)
        invalid = SudokuCSP(file_path=invalid_path)
        finished = SudokuCSP(file_path=finished_path)
        self.assertEqual(one_missing.goalTest(), False)
        self.assertEqual(invalid.goalTest(), False)
        self.assertEqual(finished.goalTest(), True)
        # For the one_missing puzzle, a valid assignment of that variable should pass the goal_test
        unassigned_variable = one_missing.unassignedVariables()[0]
        unassigned_domain = unassigned_variable.domain
        unassigned_variable.setValue(unassigned_domain[0])
        self.assertEqual(one_missing.goalTest(), True)
        # And reseting a successfully set variable should result in a failing goal test
        unassigned_variable.resetValue()
        self.assertEqual(one_missing.goalTest(), False)
        # For the one_missing puzzle, an invalid assignment using a value not in domain should fail the goal test
        invalid_value = [x + 1 for x in range(one_missing.puzzle_size) if (x + 1) not in unassigned_domain][0]
        unassigned_variable.value = invalid_value  # don't use setValue because of the bounds checking that function performs
        self.assertEqual(one_missing.allConstraintsSatisfied(), False)

    def test_get_unassigned_variable(self):
        one_missing = SudokuCSP(file_path=one_missing_path)
        finished = SudokuCSP(file_path=finished_path)
        # From one_missing, should return the only missing variable:
        unassigned_variable = one_missing.unassignedVariables()[0]
        self.assertEqual(one_missing.getUnassignedVariable(), unassigned_variable)
        # From finished, should return None
        self.assertEqual(finished.getUnassignedVariable(), None)

    def test_order_domain_values(self):
        one_missing = SudokuCSP(file_path=one_missing_path)
        half_finished = SudokuCSP(file_path=half_finished_path)
        # From one_missing, domain should only contain one value
        unassigned_variable = one_missing.getUnassignedVariable()
        unassigned_domain = unassigned_variable.domain
        self.assertEqual(one_missing.orderDomainValues(unassigned_variable), unassigned_domain)
        # From half missing, domain should be sorted
        unassigned_variable = half_finished.getUnassignedVariable()
        unassigned_domain = unassigned_variable.domain
        self.assertEqual(half_finished.orderDomainValues(unassigned_variable), sorted(unassigned_domain))

    def test_assign_variable(self):
        half_finished = SudokuCSP(file_path=half_finished_path)
        # Assigning a variable should change the variable value, update assignment, and add an action to the history
        unassigned_variable = half_finished.getUnassignedVariable()
        unassigned_domain = unassigned_variable.domain
        value_1 = unassigned_domain[0]
        half_finished.assignVariable(unassigned_variable, value_1)
        self.assertEqual(unassigned_variable.value, value_1)
        self.assertEqual(len(half_finished.assignment), 1)
        self.assertEqual(len(half_finished.actions), 1)
        # Assigning the same variable a new value should change the number of actions, but the assignments stay constant
        value_2 = unassigned_domain[0]
        half_finished.assignVariable(unassigned_variable, value_2)
        self.assertEqual(unassigned_variable.value, value_2)
        self.assertEqual(len(half_finished.assignment), 1)
        self.assertEqual(len(half_finished.actions), 2)

    def test_unassign_variable(self):
        half_finished = SudokuCSP(file_path=half_finished_path)
        unassigned_variable = half_finished.getUnassignedVariable()
        unassigned_domain = unassigned_variable.domain
        value_1 = unassigned_domain[0]
        half_finished.assignVariable(unassigned_variable, value_1)
        # Unassign the same variable should increase the number of actions, but decrease the number of assignments; as well as making the value None
        half_finished.unassignVariable(unassigned_variable)
        self.assertEqual(unassigned_variable.value, None)
        self.assertEqual(len(half_finished.assignment), 0)
        self.assertEqual(len(half_finished.actions), 2)

    def test_assignment_consistent_check(self):
        one_missing = SudokuCSP(file_path=one_missing_path)
        unassigned_variable = one_missing.getUnassignedVariable()
        # A value from the domain should make for a consistent value since one_missing's variable domain is culled
        unassigned_domain = unassigned_variable.domain
        value_1 = unassigned_domain[0]
        is_consistent = one_missing.isAssignmentConsistent(unassigned_variable, value_1)
        self.assertEqual(is_consistent, True)
        # TODO: write a check in the negative case


if __name__ == "__main__":
    unittest.main()
