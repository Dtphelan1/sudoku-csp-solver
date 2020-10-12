import logging
import configparser
from pathlib import Path

# Config variables & logger
config = configparser.ConfigParser()
config.read('config/config.ini')
LOGGER_NAME = config.get("LOGGER", "LOGGER_NAME")
logger = logging.getLogger(LOGGER_NAME)

# Parser Globals
LINE_SEP = "\n"
VALUE_SEP = ","


class PuzzleParser():
    @classmethod
    def parsePuzzle(cls, file_path):
        logger.info(f"loading puzzle data from {file_path}")
        with Path(file_path).open() as puzzle:
            size_line = cls._nextLine(puzzle)
            puzzle_size = int(size_line[0])
            values = []
            for _ in range(puzzle_size):
                row = cls._nextLine(puzzle)
                row_values = cls._getValues(row)
                values += cls._parseValuesFromStrings(puzzle_size, row_values)
            return (puzzle_size, values)

    @classmethod
    def printPuzzle(cls, puzzle, level=logging.INFO):
        puzzle_size = puzzle.puzzle_size
        values = [v.value for v in puzzle.variables]
        logger.log(level, '---Current Solution---')
        for i in range(puzzle_size):
            start_row = 0 if (i <= 0) else (i * puzzle_size)
            end_row = len(values) if (i >= puzzle_size) else ((i + 1) * puzzle_size)
            row = cls._parseStringsFromValues(puzzle_size, values[start_row:end_row])
            logger.log(level, VALUE_SEP.join(row))
        logger.log(level, '---------------------\n')

    @staticmethod
    def _nextLine(file):
        return file.readline().replace(LINE_SEP, '')

    @staticmethod
    def _getValues(row):
        return row.split(VALUE_SEP)

    @staticmethod
    def _parseValuesFromStrings(puzzle_size, values):
        value_map = {
            '_': None,
        }
        for i in range(1, puzzle_size + 1):
            value_map[str(i)] = i
        return[value_map.get(val, "Invalid character used in puzzle definition") for val in values]

    @staticmethod
    def _parseStringsFromValues(puzzle_size, values):
        value_map = {
            '_': None,
        }
        for i in range(1, puzzle_size + 1):
            value_map[str(i)] = i
        inv_map = {v: k for k, v in value_map.items()}
        return[inv_map.get(val, "Invalid character used in puzzle definition") for val in values]
