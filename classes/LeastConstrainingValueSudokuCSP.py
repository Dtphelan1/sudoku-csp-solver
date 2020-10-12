import logging
import configparser
from collections import Counter
from classes.MinimumRemainingValueSudokuCSP import MinimumRemainingValueSudokuCSP

# Config variables & logger
config = configparser.ConfigParser()
config.read('config/config.ini')
LOGGER_NAME = config.get("LOGGER", "LOGGER_NAME")
logger = logging.getLogger(LOGGER_NAME)


class LeastConstrainingValueSudokuCSP(MinimumRemainingValueSudokuCSP):
    # Enforce an ordering on the domain values, one that prioritizes the least constraining value available
    def orderDomainValues(self, variable):
        domain = variable.domain
        neighbors = self.getConstrainedNeighbors(variable)
        neighbor_domain_counts = Counter()
        for n in neighbors:
            n_domain = n.domain
            neighbor_domain_counts.update(n_domain)
        return sorted(domain, key=lambda value: neighbor_domain_counts[value])
