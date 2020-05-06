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
    def __init__(self, varname, methodName, *expressions):
        self.varname = varname
        self.methodName = methodName
        self.expressions = expressions

    def eval(self):
        retVal = "No return value"
        varnameGot = self.varname.getName()
        methodNameGot = self.methodName.getName()

        # If the object name does not exist in the variables table, raise a GroveError.
        if varnameGot not in var_table.keys():
            raise GroveError("GROVE: Undefined variable " + str(varnameGot))

        obj = var_table[varnameGot]
        methodList = [method for method in dir(obj) if callable(getattr(obj, method))]
        
        if methodNameGot not in methodList:
            raise GroveError("GROVE: Undefined method " + str(methodNameGot))

        if self.expressions:
            evalExp = []
            for exp in self.expressions:
                evalExp.append(exp.eval())
            retVal = getattr(obj, methodNameGot)(*evalExp)
        else:
            retVal = getattr(obj, methodNameGot)()

        return retVal

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
                try:
                    #Edge case, I am struggling Dr. Hutchins
                    #https://stackoverflow.com/questions/11181519/python-whats-the-difference-between-builtin-and-builtins
                    import builtins 
                    modAndObj = self.value.split(".")
                    module = eval(modAndObj[0].replace("__",""))
                    obj = getattr(module, modAndObj[1])
                except:
                    raise GroveError("GROVE: Undefined object " + self.value)

        return obj()

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