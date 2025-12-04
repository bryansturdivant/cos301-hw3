#new repo 

# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables -- all in one file.
# -----------------------------------------------------------------------------
import sys

tokens = (
    'NAME','NUMBER',
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
    'LPAREN','RPAREN', 'MODULO', 'FLOOR'
    )

# Tokens

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_MODULO = r'%'
t_FLOOR = r'//'

# dictionary of names - variable storage
names = { }
#list of instructions - instructions torage
instructions = []
#liste of functions
functions = []
#list of constants
constants = []
#list of locals
locals = []
#list of globals
globals = []


def t_NUMBER(t):
    r'[0-9]+[.]?[0-9]*'
    try:
        t.value = int(t.value)
    except ValueError:
        try:
            t.value = float(t.value)
        except ValueError:
            print("Integer value too large %d", t.value, file=sys.stderr)
            t.value = 0
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0], file=sys.stderr)
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules

precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE', 'MODULO', 'FLOOR'),
    ('right','UMINUS'),
    )





def p_statement_assign(t):
    'statement : NAME EQUALS expression'
    names[t[1]] = t[3]

def p_statement_expr(t):
    'statement : expression'
    print(t[1])

def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MODULO expression
                  | expression FLOOR expression'''
    if t[2] == '+'  : #                 if const, load_const 0, load_const 1, BINARY_ADD, etc....
        t[0] = t[1] + t[3]
        instructions.append("BINARY_ADD")
        print(instructions)
    elif t[2] == '-': 
        t[0] = t[1] - t[3]
        instructions.append("BINARY_SUBTRACT")#KEEP GOING WITH THESE
    elif t[2] == '*': 
        t[0] = t[1] * t[3]
    elif t[2] == '/': 
        t[0] = t[1] / t[3]
        if t[0].is_integer():
            t[0] = int(t[0])

            
            
        
    elif t[2] == '%': t[0] = t[1] % t[3]
    elif t[2] == '//': t[0] = t[1] // t[3]

def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = -t[2]

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_number(t):
    'expression : NUMBER'
    t[0] = t[1]
    #append to constants
    if t[1] not in constants:
        constants.append(t[1])
    constIndex = constants.index(t[1])
    instructions.append(f"LOAD_CONST {constIndex}")



def p_expression_name(t):
    'expression : NAME'
    try:
        t[0] = names[t[1]]
    except LookupError:
        print("Undefined name '%s'" % t[1], file=sys.stderr)
        t[0] = 0

def p_error(t):
    print("Syntax error at '%s'" % t.value, file=sys.stderr)
    

import ply.yacc as yacc
parser = yacc.yacc()

while True:
    try:
        s = input()   # Use raw_input on Python 2
    except EOFError:
        break
    parser.parse(s)