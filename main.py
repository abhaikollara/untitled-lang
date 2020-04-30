import sys
from evaluator import Evaluator

if __name__ == "__main__":
    try:
        path = sys.argv[1]
    except IndexError:
        print("Usage: python main.py source_file")
    else:
        with open(path) as f:
            source = f.read()

        evaluator = Evaluator()
        evaluator.eval_source(source)