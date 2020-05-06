from grove_parse import *
from grove_error import GroveError
import sys
import importlib

var_table = {}

class Expr:
    pass


class Num(Expr):
# inheritance Expr..... NOT constructor value like in other languages
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value

class Addition(Expr):

    def __init__(self, child1, child2):
        self.child1 = child1
        self.child2 = child2

        # requires both children to be expressions
        if not isinstance(self.child1, Expr):
            raise GroveError(
                "GROVE: expected expression but received " + str(type(self.child1)))

        if not isinstance(self.child2, Expr):
            raise GroveError(
                "GROVE: expected expression but received " + str(type(self.child2)))

        if not isinstance(self.child1.eval(),type(self.child2.eval())):
            raise GroveError(
                "GROVE: expected type " + str(type(self.child2)) + " but received " + str(type(self.child1)))

    def eval(self):
        return self.child1.eval() + self.child2.eval()


class StringLiteral(Expr):
    def __init__(self, string):
        self.value = string[1:][:-1]

    def eval(self):
        return self.value
        
class Method(Expr):
    def __init__(self, objName, methodName, *expressions):
        self.objName = objName
        self.methodName = methodName
        self.expressions = expressions

    def eval(self):
        # If the object name does not exist in the variables table, raise a GroveError.
        #TODO

        # Check that the specified object has the method by using introspection. If
        # the method is not defined, raise a GroveError with a message indicating which
        # method is not defined.
        # Make sure to pass the expressions variable (if not empty) to the method 
        #TODO

        return

class Name(Expr):
    def __init__(self, name):
        self.name = name

    def getName(self):
        return self.name

    def eval(self):
        if self.name in var_table:
            return var_table[self.name]
        elif self.name == "quit" or self.name == "exit":
            sys.exit()
        else:
            raise GroveError("GROVE: undefined variable " + self.name)

class PyObject(Expr):
    def __init__(self, value):
        self.value = value

    def eval(self):
        try:
            obj = eval(self.value)
        except:
            try:
                # Must access through module
                modAndObj = self.value.split(".")
                module = eval(modAndObj[0])
                obj = getattr(module, modAndObj[1])
            except:
                #Edge case, I am struggling Dr. Hutchins
                #https://stackoverflow.com/questions/11181519/python-whats-the-difference-between-builtin-and-builtins
                import builtins 
                modAndObj = self.value.split(".")
                module = eval(modAndObj[0].replace("__",""))
                obj = getattr(module, modAndObj[1])

        return obj

class Stmt:
    def __init__(self, varname, expr):
        self.varname = varname
        self.expr = expr
        if not isinstance(self.expr, Expr) and not self.varname == "import":
            raise GroveError(
                "GROVE: expected expression but received " + str(type(self.expr)))

        if not isinstance(self.varname, Name) and not self.varname == "import":
            raise GroveError(
                "GROVE: expected variable name but received " + str(type(self.varname)))

    def eval(self):
        if (self.varname == "import"):
            try:
                globals()[str(self.expr)] = importlib.import_module(str(self.expr))
            except:
                raise GroveError("GROVE: cannot import that module")
        else:
            var_table[self.varname.getName()] = self.expr.eval()

