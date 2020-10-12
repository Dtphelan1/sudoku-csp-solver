import uuid
import logging
import configparser

# Config variables & logger
config = configparser.ConfigParser()
config.read('config/config.ini')
LOGGER_NAME = config.get("LOGGER", "LOGGER_NAME")
logger = logging.getLogger(LOGGER_NAME)


class Variable():
    def __init__(self, value=None, id=None, domain=[]):
        self.id = id if id is not None else uuid.uuid4()
        self.value = value
        self.domain = domain.copy()
        self.initial_domain = domain.copy()
        self.conflict_set = []

    def hasValue(self):
        return self.value is not None

    def setValue(self, value):
        if (value not in self.domain):
            error_message = f"Trying to set value of {self.id} to {value} but domain only contains {[x for x in self.domain]}"
            logger.error(error_message)
            raise Exception(error_message)
        else:
            self.value = value

    def resetValue(self):
        self.value = None

    def removeValueFromDomain(self, value):
        value_to_remove = value in self.domain
        if value_to_remove:
            self.domain.remove(value)
        return value_to_remove

    def restoreValueToDomain(self, value):
        value_to_restore = value in self.initial_domain and value not in self.domain
        if value_to_restore:
            self.domain.append(value)
        return value_to_restore

    # Locking an initial domain allows us to make domain modifications to varaibles based on pre-filled out information in the CSP problem
    def lockDomainAsInitial(self):
        self.initial_domain = self.domain.copy()

    def addVariableToConflictSet(self, variable):
        var_in_conflict_set = variable in self.conflict_set
        if var_in_conflict_set:
            self.conflict_set.append(var_in_conflict_set)

    def removeVariableFromConflictSet(self, variable):
        var_in_conflict_set = variable in self.conflict_set
        if var_in_conflict_set:
            self.conflict_set.remove(var_in_conflict_set)
