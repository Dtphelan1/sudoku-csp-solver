import cli
import timeit
import configparser

# Config variables & logger
config = configparser.ConfigParser()
config.read('config/config.ini')
RUNS = int(config.get("BENCHMARKING", "RUNS"))

if __name__ == "__main__":
    t = timeit.timeit("cli.main()", setup="from __main__ import cli", number=RUNS)
    print(f"Average - {(t/float(RUNS))}")
