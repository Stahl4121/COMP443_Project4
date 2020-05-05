from grove_parse import *
from grove_error import GroveError

if __name__ == "__main__":
    while True:
        ln = input("Grove>> ")
        try:
            root = parse(ln)
            output = root.eval()
            if output:
                print(output)
        except GroveError as GE:
            print(GE)
