import unittest

from classes.Constraint import Constraint


class ConstraintTest(unittest.TestCase):
    def test_constructor(self):
        variables = [1, 2, 3]
        def constraint_fn(var_list): return sum(var_list) < 10
        constraint = Constraint(variables, constraint_fn)
        self.assertEqual(constraint.variables, variables)
        self.assertEqual(constraint.constraint_fn, constraint_fn)

    def test_is_satisfied(self):
        variables = [1, 2, 3]
        def constraint_fn_true(var_list): return sum(var_list) < 10
        def constraint_fn_false(var_list): return sum(var_list) > 10
        constraint_true = Constraint(variables, constraint_fn_true)
        constraint_false = Constraint(variables, constraint_fn_false)
        self.assertEqual(constraint_true.isSatisfied(), True)
        self.assertEqual(constraint_false.isSatisfied(), False)

    def test_get_constrained_group(self):
        variables = [1, 2, 3]
        def constraint_fn(var_list): return sum(var_list) < 10
        constraint = Constraint(variables, constraint_fn)
        in_group = variables[0]
        out_of_group = 4
        self.assertEqual(constraint.getConstrainedGroup(in_group), [v for v in variables if v is not in_group])
        self.assertEqual(constraint.getConstrainedGroup(out_of_group), [])


if __name__ == "__main__":
    unittest.main()
