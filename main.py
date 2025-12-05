#Extended calc.py remade into a compiler with JCoCo instructions


import sys

#tokens 
tokens = (
    'NAME','NUMBER',
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
    'LPAREN','RPAREN', 'MODULO', 'FLOOR'
    )



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
#list of instructions - instruction storage
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




#Assignment statement: Evaluate expression and store result in the local variable 
def p_statement_assign(t):
    'statement : NAME EQUALS expression'
    names[t[1]] = t[3]
    locals.append(t[1])
    localsIndex = locals.index(t[1])
    instructions.append(f"STORE_FAST {localsIndex}")


#Expression used as a statement: If its a variable, generate code to print its value
def p_statement_expr(t):
    'statement : expression'
    if isinstance(t[1], str) and t[1] in locals:
        if 'print' not in globals:
            globals.append('print')
        globalsIndex = globals.index('print')


        localsIndex = locals.index(t[1])
        instructions.append(f"LOAD_FAST {localsIndex}")


        instructions.append(f"LOAD_GLOBAL {globalsIndex}")
        instructions.append(f"ROT_TWO")
        instructions.append(f"CALL_FUNCTION 1")
        instructions.append("POP_TOP")

#binary operations: compute result and emit corresponding JCoCo opcode
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
      
    elif t[2] == '-': 
        t[0] = t[1] - t[3]
        instructions.append("BINARY_SUBTRACT")
    elif t[2] == '*': 
        t[0] = t[1] * t[3]
        instructions.append("BINARY_MULTIPLY")
    elif t[2] == '/': 
        t[0] = t[1] / t[3]
        instructions.append("BINARY_TRUE_DIVIDE")
        if t[0].is_integer():
            t[0] = int(t[0])

            
            
        
    elif t[2] == '%': 
        t[0] = t[1] % t[3]
        instructions.append("BINARY_MODULO")

    elif t[2] == '//': 
        t[0] = t[1] // t[3]
        instructions.append("BINARY_FLOOR_DIVIDE")

#This handles negative numbers in input by generating code equivalent to 0 - expression
def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = -t[2]
     #where my negative number stuff comes into play
    constants.append(0)

    constIndex = constants.index(0)
    instructions.append(f'LOAD_CONST {constIndex}')
    instructions.append(f'ROT_TWO')
    instructions.append(f'BINARY_SUBTRACT')
#parenthesis grouping
def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_number(t):
    'expression : NUMBER'
    t[0] = t[1]
    #add constant to list of constants if its new, and emit Load instruction
    if t[1] not in constants and t[1] > 0:
        constants.append(t[1])
    # if t[1] not in constants and t[1] < 0:
    #     t[1] = t[1] * -1
    #     constants.append(t[1])
    #     constants.append(0)
    constIndex = constants.index(t[1])
    instructions.append(f"LOAD_CONST {constIndex}")


#looks up if variable exists in Names dictionary
def p_expression_name(t):
    'expression : NAME'
    try:
        #t[0] = names[t[1]]
        t[0] = t[1]
    except LookupError:
        print("Undefined name '%s'" % t[1], file=sys.stderr)
        t[0] = 0

def p_error(t):
    print("Syntax error at '%s'" % t.value, file=sys.stderr)
    

import ply.yacc as yacc
parser = yacc.yacc()

# while True:
#     try:
#         s = input()   # Use raw_input on Python 2
#     except EOFError:
#         break
#     parser.parse(s)

# Read all input from the user and parse it line by line
# This allows multiple statements to be handled separately
source = sys.stdin.read()
for line in source.splitlines():
    parser.parse(line)


#append required final constants and instruction output
constants.append('None')
functions.append('Main/0')
constIndex = constants.index('None')
instructions.append(f'LOAD_CONST {constIndex}')
instructions.append('RETURN_VALUE')
#formatting for the output of instructions
print(f'Functions: {functions}')
print(f'Constants: {constants}')
print(f'Locals: {locals}')
print(f'Globals: {globals}')
print('BEGIN')

for x in instructions:
    print(f'     {x}')



print("END")