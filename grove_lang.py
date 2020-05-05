from grove_parse import *
from grove_error import GroveError
import sys

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
        strVal = string[1:][:-1]
        if "\"" in strVal or "\'" in strVal:
            raise GroveError("GROVE: Invalid StringLiteral: " + string)
        self.value = strVal

    def eval(self):
        return self.value



class Name(Expr):
# see in second statement - - i do not have the value - -- I do not have an instance of the class 
# I just have the string value of the name in the set - -- so I need table of string names to what they
# evaluated to during the set operation
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

class Stmt:
    def __init__(self, varname, expr):
        self.varname = varname
        self.expr = expr
        if not isinstance(self.expr, Expr):
            raise GroveError(
                "GROVE: expected expression but received " + str(type(self.expr)))

        if not isinstance(self.varname, Name):
            raise GroveError(
                "GROVE: expected variable name but received " + str(type(self.varname)))

    def eval(self):
        var_table[self.varname.getName()] = self.expr.eval()


