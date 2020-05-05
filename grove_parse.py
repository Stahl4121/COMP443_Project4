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
            names = tokens[2].split(".")
            check(len(names) < 3)
            if len(names) == 1:
                """ "set" <Name> "=" "new" <Name> """
                #TODO
            else:
                """ "set" <Name> "=" "new" <Name>"."<Name> """
                #TODO

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
        if (len(start) > 1):
            if ((not start[0].isalpha() and not start[0] == "_") or not (''.join(filter(lambda i: not i is '_', start[1:]))).isalnum()):
                check(False, "Variable names must be alphabetic characters only")
        elif (not start[0].isalpha() and not start[0] == "_"):
            check(False, "Variable names must be alphabetic characters only")
        return ( Name(start), tokens[1:] )




   

if __name__ == "__main__":
    # First try some things that should work
    cmds = [" + ( 3 ) ( 12 ) ",
            " - ( 5 ) ( 2 )",
            " + ( 15 ) ( - ( 3 ) ( 8 ) ) ",
            "set foo = 38",
            "foo",
            "set bar = + ( 22 ) ( foo )",
            "bar"]
            
    answers = [ 15,
                3,
                10,
                None,
                38,
                None,
                60 ]
    
    for i in range(0, len(cmds)):
        root = parse(cmds[i])
        result = root.eval()
        check(result == answers[i], "TEST FAILED for cmd " + cmds[i] + 
            ";  result was " + str(result) + " instead of " + str(answers[i]))
    
    # Testing for all errors is beyond our scope
    # But we check a few
    bad_cmds = [ " ",
                 "not-alpha",
                 " + ( nope ) ( 3 ) ",
                 " 3 + 3 ",
                 " + ( 5 ) ( 4 ) foo ",
                 " + ( set x = 6 ) ( 7 )"]
                 
    for c in bad_cmds:
        try:
            root = parse(c)
            result = root.eval()
            check(False, "Did not catch an error that we should have caught")
        except ValueError:
            pass
        
    
