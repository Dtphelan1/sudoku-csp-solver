from classes.SudokuCSP import SudokuCSP
from classes.MinimumRemainingValueSudokuCSP import MinimumRemainingValueSudokuCSP
from classes.LeastConstrainingValueSudokuCSP import LeastConstrainingValueSudokuCSP
from classes.ConflictDirectedBackjumpingSudokuCSP import ConflictDirectedBackjumpingSudokuCSP


class SudokuCSPFactory():
    DEFAULT = 'def'
    sudoku_csp_options = {
        DEFAULT: SudokuCSP,
        'mrv': MinimumRemainingValueSudokuCSP,
        'lcv': LeastConstrainingValueSudokuCSP,
        'cbg': ConflictDirectedBackjumpingSudokuCSP
    }

    @classmethod
    def getSudokuCSPOptions(cls):
        return list(cls.sudoku_csp_options.keys())

    @ classmethod
    def getSudokuCSP(cls, ty):
        return cls.sudoku_csp_options.get(ty, f"No SudokuCSP of type {ty} available")

    @ classmethod
    def defaultSudokuCSPType(cls):
        return cls.DEFAULT
