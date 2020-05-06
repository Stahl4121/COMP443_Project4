#exec(open("grove_lang.py").read())
from grove_lang import *
from grove_error import GroveError


def check(condition, message = "Unexpected end of expression"):
    """ Checks if condition is true, raising a GroveError otherwise """
    if not condition:
        raise GroveError("GROVE: " + message)
        
def expect(token, expected):
    """ Checks that token matches expected
        If not, throws a GroveError with explanatory message """
    if token != expected:
        check(False, "Expected '" + expected + "' but found '" + token + "'")
        
def is_expr(x):
    if not isinstance(x, Expr):
        check(False, "Expected expression but found " + str(type(x)))
        
        
def is_int(s):
    """ Takes a string and returns True if it can be converted to an integer """
    try:
        int(s)
        return True
    except ValueError:
        return False

def is_stringLiteral(s):
    if (s[0] == '"' and s[-1] == '"' and '"' not in s[1:][:-1] and '\'' not in s[1:][:-1]):
        return True
    return False

        
def parse(s):
    """ Return an object representing a parsed command
        Throws GroveError for improper syntax """
    (root, remaining_tokens) = parse_tokens(s.split())
    
    # The parse call should have used all the tokens
    check(len(remaining_tokens) == 0,
        "Expected end of command but found '" + " ".join(remaining_tokens) + "'")
        
    return root
        
        
        
def parse_tokens(tokens):
    """ Returns a tuple:
        (an object representing the next part of the expression,
         the remaining tokens)
    """
    
    check(len(tokens) > 0)

    start = tokens[0]
    
    if is_int(start):
        return ( Num(int(start)), tokens[1:] )
        #else raise GroveError("GROVE: negative value found")

    elif is_stringLiteral(start):
        return (StringLiteral(start), tokens[1:] )
    
    elif start == "+":
        # An addition 
        check(len(tokens) > 2)
        expect(tokens[1], "(")
        (child1, tokens) = parse_tokens(tokens[2:])
        check(len(tokens) > 1)
        expect(tokens[0], ")")
        expect(tokens[1], "(")
        (child2, tokens) = parse_tokens(tokens[2:])
        check(len(tokens) > 0)
        expect(tokens[0], ")")
       
        return ( Addition(child1, child2), tokens[1:] )
            
    elif start == "set":
        # An assignment statement
        # Get the name
        (varname, tokens) = parse_tokens (tokens[1:])
        check(len(tokens) > 1)
        expect(tokens[0], "=")
        if tokens[1] == "new":
            check(len(tokens) > 2)
            (child, tokens) = parse_tokens(tokens[1:])
            print(tokens)
            child = eval(tokens[2])
            return ( Stmt(varname, child), tokens )
        else:
            #Assign an expr
            (child, tokens) = parse_tokens(tokens[1:])
            return ( Stmt(varname, child), tokens )
    
    elif start == "import":
        check(len(tokens) > 1)
        return ( Stmt(start, tokens[1]), tokens[2:] )
        
    
    elif start == "call":
        """ See bullet point in pdf doc """
        #TODO

    else:
        # A variable
        # Check that it is alphabetic characters
        if not (start[0].isalpha() or start[0] == "_"):
            check(False, "Variable names must start with an alphabetic character")

        if (len(start) > 1):
            if not ''.join(filter(lambda i: i != '_', start[1:])).isalnum():
                check(False, "Variable names must be alphanumeric characters only")

        return ( Name(start), tokens[1:] )

