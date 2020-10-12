import unittest
# NOTE: Import here initializes our logger
import classes.Logger
from classes.Variable import Variable


class VariableTest(unittest.TestCase):
    def test_has_value(self):
        domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        value = 1
        variable_no_value = Variable(domain=domain)
        variable_with_value = Variable(domain=domain, value=value)
        self.assertEqual(variable_no_value.value, None)
        self.assertEqual(variable_no_value.hasValue(), False)
        self.assertEqual(variable_with_value.value, value)
        self.assertEqual(variable_with_value.hasValue(), True)

    def test_set_value(self):
        domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        initial_value = 1
        new_value = 2
        invalid_value = 10
        variable = Variable(domain=domain, value=initial_value)
        self.assertEqual(variable.value, initial_value)
        variable.setValue(new_value)
        self.assertEqual(variable.value, new_value)
        with self.assertRaises(Exception):
            variable.setValue(invalid_value)

    def test_reset_value(self):
        domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        initial_value = 1
        variable = Variable(domain=domain, value=initial_value)
        self.assertEqual(variable.value, initial_value)
        variable.resetValue()
        self.assertEqual(variable.value, None)

    def test_remove_from_domain(self):
        domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        value_1 = 1
        value_2 = None
        variable_1 = Variable(domain=domain, value=value_1)
        variable_2 = Variable(domain=domain, value=value_2)
        self.assertEqual(variable_1.domain, domain)
        self.assertEqual(variable_2.domain, domain)
        # Removing a value should update the variables domain
        remove_1 = 8
        variable_1.removeValueFromDomain(remove_1)
        self.assertEqual(variable_1.domain, [val for val in domain if val is not remove_1])
        # Removing a value should only update this variables domain
        remove_2 = 3
        variable_2.removeValueFromDomain(remove_2)
        self.assertEqual(variable_2.domain, [val for val in domain if val is not remove_2])
        # Removing a value not in the domain shouldn't change it
        remove_irrelevant = 11
        domain_before_removal_1 = variable_1.domain.copy()
        variable_1.removeValueFromDomain(remove_irrelevant)
        self.assertEqual(domain_before_removal_1, variable_1.domain)


if __name__ == "__main__":
    unittest.main()
