from grove_parse import *
from grove_error import GroveError

"""
Wesley Curtis, Matt Lew, Logan Stahl
Grove language uses dynamic typing, because we do not need to explicitly state 
what data type each variable is to set it. Also, since we just set the variable equal
to the value given, it depends on what python is. Python is dynamically typed, so Grove is as well.
You can, for instance, say 
set l = "hi"
l
set l = 5
l

and it will return
hi
5


"""


if __name__ == "__main__":
    while True:
        ln = input("Grove>> ")
        try:
            root = parse(ln)
            output = root.eval()
            if output is not None:
                print(output)
        except GroveError as GE:
            print(GE)
