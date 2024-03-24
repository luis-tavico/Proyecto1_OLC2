# PLY Imports
import grammar.ply.yacc as yacc
import grammar.ply.lex as Lex

# Expressions imports
from environment.types import ExpressionType
from expressions.primitive import Primitive
from expressions.operation import Operation
from expressions.access import Access
from expressions.array import Array
from expressions.array_access import ArrayAccess
from expressions.break_statement import Break
from expressions.continue_statement import Continue
from expressions.ternario import Ternario
from expressions.call import Call
from expressions.return_statement import Return
from expressions.interface_access import InterfaceAccess

# Instructions imports
from instructions.print import Print
from instructions.declaration import Declaration
from instructions.assignment import Assignment
from instructions.array_declaration import ArrayDeclaration
from instructions.array_assignment import ArrayAssignment
from instructions.array_methods import ArrayMetodos
from instructions.if_instruction import If
from instructions.elseif_instruction import ElseIf
from instructions.else_instruction import Else
from instructions.switch_instruction import Switch
from instructions.case_instruction import Case
from instructions.default_instruction import Default
from instructions.while_instruction import While
from instructions.for_instruction import For
from instructions.function import Function
from instructions.funciones_embebidas import FuncionesEmbebidas
from instructions.interface import Interface
from instructions.interface_declaration import InterfaceDeclaration
from instructions.interface_assignment import InterfaceAssignment
from instructions.interface_keys import Keys
from instructions.interface_values import Values

class codeParams:
    def __init__(self, line, column):
        self.line = line
        self.column = column

#LEXICO
reserved_words = {
    'console': 'CONSOLE', 
    'log': 'LOG',
    'var': 'VAR',
    'const': 'CONST',
    'number': 'NUMBER',
    'float': 'FLOAT',
    'string': 'STRING',
    'char'  : 'CHAR',
    'boolean': 'BOOLEAN',
    'if' : 'IF',
    'else' : 'ELSE',
    'switch' : 'SWITCH',
    'case' : 'CASE',
    'default' : 'DEFAULT',
    'while' : 'WHILE',
    'for' : 'FOR',
    'break' : 'BREAK',
    'continue' : 'CONTINUE',
    'return' : 'RETURN',
    'function' : 'FUNCTION',
    'parseInt' : 'PARSEINT',
    'parseFloat' : 'PARSEFLOAT',
    'toString' : 'TOSTRING',
    'toLowerCase' : 'TOLOWERCASE',
    'toUpperCase' : 'TOUPPERCASE',
    'typeof' : 'TYPEOF',
    'interface' : 'INTERFACE',
    'Object' : 'OBJECT',
    'keys' : 'KEYS',
    'values' : 'VALUES',
    'push' : 'PUSH',
    'pop' : 'POP',
    'indexOf' : 'INDEXOF',
    'join' : 'JOIN',
    'length' : 'LENGTH'
}

# Listado de tokens
tokens = [
    'PARIZQ',
    'PARDER',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'MODULO',
    'INCREMENTO',
    'PUNTO',
    'DOSPTS',
    'COMA',
    'PYC',
    'ENTERO',
    'DECIMAL',
    'CADENA',
    'CARACTER',
    'BOOLEANO',
    'IG',
    'IGIG',
    'DIF',
    'CORIZQ',
    'CORDER',
    'LLAVEIZQ',
    'LLAVEDER',
    'MAYOR',
    'MENOR',
    'MAYORIG',
    'MENORIG',
    'AND',
    'OR',
    'NOT',
    'TERN',
    'ID'
] + list(reserved_words.values())

t_MAYOR         = r'>'
t_MENOR         = r'<'
t_MAYORIG       = r'>='
t_MENORIG       = r'<='
t_PARIZQ        = r'\('
t_PARDER        = r'\)'
t_MAS           = r'\+'
t_MENOS         = r'-'
t_INCREMENTO    = r'\+\+'
t_POR           = r'\*'
t_DIVIDIDO      = r'/'
t_MODULO        = r'%'
t_PUNTO         = r'\.'
t_DOSPTS        = r':'
t_COMA          = r','
t_PYC           = r';'
t_IGIG          = r'=='
t_IG            = r'='
t_DIF           = r'!='
t_CORIZQ        = r'\['
t_CORDER        = r'\]'
t_LLAVEIZQ      = r'\{'
t_LLAVEDER      = r'\}'
t_AND           = r'&&'
t_OR            = r'\|\|'
t_NOT           = r'!'
t_TERN          = r'\?'

#Función de reconocimiento
def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        floatValue = float(t.value)
        line = t.lexer.lexdata.rfind('\n', 0, t.lexpos) + 1
        column = t.lexpos - line
        t.value = Primitive(line, column, floatValue, ExpressionType.FLOAT)
    except ValueError:
        print("Error al convertir a decimal %d", t.value)
        t.value = Primitive(0, 0, None, ExpressionType.NULL)
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        intValue = int(t.value)
        line = t.lexer.lexdata.rfind('\n', 0, t.lexpos) + 1
        column = t.lexpos - line
        t.value = Primitive(line, column, intValue, ExpressionType.NUMBER)
    except ValueError:
        print("Error al convertir a entero %d", t.value)
        t.value = Primitive(0, 0, None, ExpressionType.NULL)
    return t

def t_CADENA(t):
    r'\"([^\\\"]|\\.)*\"'
    try:
        strValue = str(t.value)
        line = t.lexer.lexdata.rfind('\n', 0, t.lexpos) + 1
        column = t.lexpos - line
        t.value = Primitive(line, column, strValue.replace('"', ''), ExpressionType.STRING)
    except ValueError:
        print("Error al convertir string %d", t.value)
        t.value = Primitive(0, 0, None, ExpressionType.NULL)
    return t

def t_CARACTER(t):
    r'\'(.+?)\''
    try:
        charValue = str(t.value)
        line = t.lexer.lexdata.rfind('\n', 0, t.lexpos) + 1
        column = t.lexpos - line
        t.value = Primitive(line, column, charValue.replace("'", ''), ExpressionType.CHAR)
    except ValueError:
        print("Error al convertir caracter %d", t.value)
        t.value = Primitive(0, 0, None, ExpressionType.NULL)
    return t

def t_BOOLEANO(t):
    r'true|false'
    try:
        boolValue = bool(t.value)
        line = t.lexer.lexdata.rfind('\n', 0, t.lexpos) + 1
        column = t.lexpos - line
        t.value = Primitive(line, column, True if boolValue == 'true' else False, ExpressionType.BOOLEAN)
    except ValueError:
        print("Error al convertir booleano %d", t.value)
        t.value = Primitive(0, 0, None, ExpressionType.NULL)
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    #  t.type = reserved_words.get(t.value.lower(),'ID')
    t.type = reserved_words.get(t.value,'ID')
    return t

t_ignore = " \t"

t_ignore_COMMENTLINE = r'\/\/.*'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_ignore_COMMENTBLOCK(t):
    r'\/\*[^*]*\*+(?:[^/*][^*]*\*+)*\/'
    t.lexer.lineno += t.value.count('\n')

def t_error(t):
    print("Error Léxico '%s'" % t.value[0])
    t.lexer.skip(1)

#SINTACTICO
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'IGIG', 'DIF'),
    ('left', 'MENOR', 'MENORIG', 'MAYORIG', 'MAYOR'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'DIVIDIDO', 'MODULO', 'POR'),
    ('right', 'NOT', 'UMENOS'),
    ('left', 'PARIZQ', 'PARDER', 'CORIZQ', 'CORDER')
)

#START
def p_start(t):
    '''s : block'''
    t[0] = t[1]

def p_instruction_block(t):
    '''block : block instruccion
             | instruccion '''
    if 2 < len(t):
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]

#Listado de instrucciones
def p_instruction_list(t):
    '''instruccion : print
                   | ifinstruction
                   | switchinstruction
                   | whileinstruction
                   | forinstruction
                   | declaration
                   | arraydeclaration
                   | assignment
                   | breakstmt
                   | continuestmt
                   | functionstmt
                   | call
                   | returnstmt
                   | interfacecreation
                   | interdeclaration
                   | listArray PYC
                   | typeof PYC
                   | parseint PYC
                   | parsefloat PYC'''
    t[0] = t[1]

def p_instruction_console(t):
    'print : CONSOLE PUNTO LOG PARIZQ expressionList PARDER PYC'
    params = get_params(t)
    t[0] = Print(params.line, params.column, t[5])

def p_instruction_if(t):
    '''ifinstruction : IF PARIZQ expression PARDER LLAVEIZQ block LLAVEDER
                     | IF PARIZQ expression PARDER LLAVEIZQ block LLAVEDER else_if_list
                     | IF PARIZQ expression PARDER LLAVEIZQ block LLAVEDER else
                     | IF PARIZQ expression PARDER LLAVEIZQ block LLAVEDER else_if_list else'''
    params = get_params(t)
    if len(t) > 9:
        t[0] = If(params.line, params.column, t[3], t[6], t[8], t[9])
    elif len(t) > 8:
        if isinstance(t[8], Else):
            t[0] = If(params.line, params.column, t[3], t[6], None, t[8])
        else:
            t[0] = If(params.line, params.column, t[3], t[6], t[8], None)
    elif len(t) > 7:
        t[0] = If(params.line, params.column, t[3], t[6], None, None)

def p_instruction_else_if_list(t):
    '''else_if_list : else_if_list else_if
                    | else_if'''
    if len(t) > 2:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]

def p_instruction_else_if(t):
    'else_if : ELSE IF PARIZQ expression PARDER LLAVEIZQ block LLAVEDER'
    params = get_params(t)
    t[0] = ElseIf(params.line, params.column, t[4], t[7])

def p_instruction_else(t):
    'else : ELSE LLAVEIZQ block LLAVEDER'
    params = get_params(t)
    t[0] = Else(params.line, params.column, t[3])

def p_instruction_switch(t):
    '''switchinstruction : SWITCH PARIZQ expression PARDER LLAVEIZQ caseList LLAVEDER
                         | SWITCH PARIZQ expression PARDER LLAVEIZQ default LLAVEDER
                         | SWITCH PARIZQ expression PARDER LLAVEIZQ caseList default LLAVEDER'''
    params = get_params(t)
    if len(t) > 8:
        t[0] = Switch(params.line, params.column, t[3], t[6], t[7])
    elif len(t) > 7:
        if isinstance(t[7], Default):
            t[0] = Switch(params.line, params.column, t[3], None, t[6])
        else:
            t[0] = Switch(params.line, params.column, t[3], t[6], None)

def p_instruction_case_list(t):
    '''caseList : caseList case
                | case'''
    if len(t) > 2:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]

def p_instruction_case(t):
    'case : CASE expression DOSPTS block'
    params = get_params(t)
    t[0] = Case(params.line, params.column, t[2], t[4])

def p_instruction_default(t):
    'default : DEFAULT DOSPTS block'
    params = get_params(t)
    t[0] = Default(params.line, params.column, t[3])

def p_instruction_while(t):
    'whileinstruction : WHILE PARIZQ expression PARDER LLAVEIZQ block LLAVEDER'
    params = get_params(t)
    t[0] = While(params.line, params.column, t[3], t[6])

def p_instruction_for(t):
    'forinstruction : FOR PARIZQ declaration expression PYC expression PARDER LLAVEIZQ block LLAVEDER'
    params = get_params(t)
    t[0] = For(params.line, params.column, t[3], t[4], t[6], t[9])

def p_instruction_declaration_var(t):
    'declaration : var_const ID DOSPTS type IG expression PYC'
    params = get_params(t)
    t[0] = Declaration(params.line, params.column, t[2], t[4], t[6])

def p_instruction_array_declaration(t):
    'arraydeclaration : var_const ID DOSPTS type dimension IG expression PYC'
    params = get_params(t)
    t[0] = ArrayDeclaration(params.line, params.column, t[2], t[4], t[7])

def p_instruction_array_assignment(t):
    'assignment : ID indexes IG expression PYC'
    params = get_params(t)
    t[1] = Access(params.line, params.column, t[1])
    t[0] = ArrayAssignment(params.line, params.column, t[1], t[2], t[4])

def p_dimension_array(t):
    '''dimension : dimension CORIZQ CORDER
                 | CORIZQ CORDER'''

def p_instruction_interface_declaration(t):
    'interdeclaration : var_const ID DOSPTS ID IG LLAVEIZQ interfaceContent LLAVEDER PYC'
    params = get_params(t)
    t[0] = InterfaceDeclaration(params.line, params.column, t[2], t[4], t[7])

def p_instruction_interface_content(t):
    '''interfaceContent : interfaceContent COMA ID DOSPTS expression
                        | ID DOSPTS expression'''
    arr = []
    if len(t) > 5:
        param = {t[3] : t[5]}
        arr = t[1] + [param]
    else:
        param = {t[1] : t[3]}
        arr.append(param)
    t[0] = arr

def p_var_const(t):
    '''var_const : VAR
                 | CONST'''
    t[0] = t[1]

def p_interface_assignment(t):
    'assignment : listArray IG expression PYC'
    params = get_params(t)
    t[0] = InterfaceAssignment(params.line, params.column, t[1], t[3])

def p_instruction_assignment(t):
    'assignment : ID IG expression PYC'
    params = get_params(t)
    t[0] = Assignment(params.line, params.column, t[1], t[3])

def p_instruction_return(t):
    '''returnstmt : RETURN expression PYC
                  | RETURN PYC'''
    params = get_params(t)
    if len(t) > 3:
        t[0] = Return(params.line, params.column, t[2])
    else:
        t[0] = Return(params.line, params.column, None)

def p_instruction_call_function(t):
    '''call : ID PARIZQ expressionList PARDER PYC
            | ID PARIZQ PARDER PYC'''
    params = get_params(t)
    if len(t) > 5:
        t[0] = Call(params.line, params.column, t[1], t[3])
    else:
        t[0] = Call(params.line, params.column, t[1], [])
    
def p_instruction_function(t):
    'functionstmt : FUNCTION ID funcparams functype LLAVEIZQ block LLAVEDER'
    params = get_params(t)
    t[0] = Function(params.line, params.column, t[2], t[3], t[4], t[6])

def p_instruction_function_params_list(t):
    '''funcparams : PARIZQ paramsList PARDER
                  | PARIZQ PARDER'''
    if len(t) > 3:
        t[0] = t[2]
    else:
        t[0] = []

def p_instruction_interface_creation(t):
    'interfacecreation : INTERFACE ID LLAVEIZQ attributeList LLAVEDER'
    params = get_params(t)
    t[0] = Interface(params.line, params.column, t[2], t[4])

def p_instruction_interface_attribute(t):
    '''attributeList : attributeList ID DOSPTS type PYC
                     | ID DOSPTS type PYC'''
    arr = []
    if len(t) > 5:
        param = {t[2] : t[4]}
        arr = t[1] + [param]
    else:
        param = {t[1] : t[3]}
        arr.append(param)
    t[0] = arr

def p_expression_param_list(t):
    '''paramsList : paramsList COMA parametro
                  | parametro'''
    parametros = []
    if len(t) > 2:
        parametros = t[1] + [t[3]]
    else:
        parametros.append(t[1])
    t[0] = parametros

def p_parametro(t):
    '''parametro : ID DOSPTS type
                 | ID DOSPTS type CORIZQ CORDER'''
    if len(t) > 5:
        param = {t[1] : ExpressionType.ARRAY}
        t[0] = param
    else:
        param = {t[1] : t[3]}
        t[0] = param

def p_instruction_function_type(t):
    '''functype : DOSPTS type
                | '''
    if len(t) > 2:
        t[0] = t[2]
    else:
        t[0] = ExpressionType.NULL

def p_instruction_break(t):
    'breakstmt : BREAK PYC'
    params = get_params(t)
    t[0] = Break(params.line, params.column)

def p_instruction_continue(t):
    'continuestmt : CONTINUE PYC'
    params = get_params(t)
    t[0] = Continue(params.line, params.column)

def p_type_prod(t):
    '''type : NUMBER
            | FLOAT
            | STRING
            | CHAR
            | BOOLEAN
            | ID'''
    if t[1] == 'number':
        t[0] = ExpressionType.NUMBER
    elif t[1] == 'float': 
        t[0] = ExpressionType.FLOAT
    elif t[1] == 'string':
        t[0] = ExpressionType.STRING
    elif t[1] == 'char':
        t[0] = ExpressionType.CHAR
    elif t[1] == 'boolean':
        t[0] = ExpressionType.BOOLEAN
    else:
        t[0] = ExpressionType.STRUCT

def p_expression_list(t):
    '''expressionList : expressionList COMA expression
                      | expression '''
    arr = []
    if len(t) > 2:
        arr = t[1] + [t[3]]
    else:
        arr.append(t[1])
    t[0] = arr

def p_interface_methods(t):
    '''expression : OBJECT PUNTO KEYS   PARIZQ expression PARDER
                  | OBJECT PUNTO VALUES PARIZQ expression PARDER'''
    params = get_params(t)
    if t[3] == 'keys':
        t[0] = Keys(params.line, params.column, t[5])
    elif t[3] == 'values':
        t[0] = Values(params.line, params.column, t[5])

# Expresiones aritmeticas, relacionales y lógicas
def p_expression_add(t):
    'expression : expression MAS expression'
    params = get_params(t)
    t[0] = Operation(params.line, params.column, "+", t[1], t[3])

def p_expression_sub(t):
    'expression : expression MENOS expression'
    params = get_params(t)
    t[0] = Operation(params.line, params.column, "-", t[1], t[3])

def p_expression_mult(t):
    'expression : expression POR expression'
    params = get_params(t)
    t[0] = Operation(params.line, params.column, "*", t[1], t[3])

def p_expression_div(t):
    'expression : expression DIVIDIDO expression'
    params = get_params(t)
    t[0] = Operation(params.line, params.column, "/", t[1], t[3])

def p_expression_mod(t):
    'expression : expression MODULO expression'
    params = get_params(t)
    t[0] = Operation(params.line, params.column, "%", t[1], t[3])

def p_expression_mayor(t):
    'expression : expression MAYOR expression'
    params = get_params(t)
    t[0] = Operation(params.line, params.column, ">", t[1], t[3])

def p_expression_menor(t):
    'expression : expression MENOR expression'
    params = get_params(t)
    t[0] = Operation(params.line, params.column, "<", t[1], t[3])

def p_expression_mayor_igual(t):
    'expression : expression MAYORIG expression'
    params = get_params(t)
    t[0] = Operation(params.line, params.column, ">=", t[1], t[3])

def p_expression_menor_igual(t):
    'expression : expression MENORIG expression'
    params = get_params(t)
    t[0] = Operation(params.line, params.column, "<=", t[1], t[3])

def p_expression_igual(t):
    'expression : expression IGIG expression'
    params = get_params(t)
    t[0] = Operation(params.line, params.column, "==", t[1], t[3])

def p_expression_diferente(t):
    'expression : expression DIF expression'
    params = get_params(t)
    t[0] = Operation(params.line, params.column, "!=", t[1], t[3])

def p_expression_and(t):
    'expression : expression AND expression'
    params = get_params(t)
    t[0] = Operation(params.line, params.column, "&&", t[1], t[3])

def p_expression_or(t):
    'expression : expression OR expression'
    params = get_params(t)
    t[0] = Operation(params.line, params.column, "||", t[1], t[3])

def p_expression_not(t):
    'expression : NOT expression'
    params = get_params(t)
    t[0] = Operation(params.line, params.column, "!", t[2], None)

def p_expression_negativo(t):
    'expression : MENOS expression %prec UMENOS'
    params = get_params(t)
    t[0] = Operation(params.line, params.column, "-", t[2], None)

def p_expression_incremento(t):
    'expression : expression INCREMENTO'
    params = get_params(t)
    t[0] = Operation(params.line, params.column, "++", t[1], None)

def p_expression_agrupacion(t):
    'expression : PARIZQ expression PARDER'
    t[0] = t[2]

def p_expression_ternario(t):
    'expression : expression TERN expression DOSPTS expression'
    params = get_params(t)
    t[0] = Ternario(params.line, params.column, t[1], t[3], t[5])

def p_expression_valor(t):
    'expression : listArray'
    t[0] = t[1]

def p_expression_primitiva(t):
    '''valor : ENTERO
             | DECIMAL
             | CADENA
             | CARACTER
             | BOOLEANO'''
    t[0] = t[1]

def p_expression_acceso(t):
    'valor : ID'
    params = get_params(t)
    t[0] = Access(params.line, params.column, t[1])

def p_expression_array_primitiva(t):
    '''expression : CORIZQ expressionList CORDER'''
    params = get_params(t)
    t[0] = Array(params.line, params.column, t[2])

def p_expression_call_function(t):
    '''expression : ID PARIZQ expressionList PARDER
                  | ID PARIZQ PARDER'''
    params = get_params(t)
    if len(t) > 4:
        t[0] = Call(params.line, params.column, t[1], t[3])
    else:
        t[0] = Call(params.line, params.column, t[1], [])

def p_expression_list_array(t):
    '''listArray : listArray PUNTO TOSTRING    PARIZQ PARDER
                 | listArray PUNTO TOLOWERCASE PARIZQ PARDER
                 | listArray PUNTO TOUPPERCASE PARIZQ PARDER
                 | listArray PUNTO POP         PARIZQ PARDER
                 | listArray PUNTO JOIN        PARIZQ PARDER
                 | listArray PUNTO PUSH    expression
                 | listArray PUNTO INDEXOF expression
                 | listArray PUNTO LENGTH
                 | listArray PUNTO ID
                 | listArray indexes
                 | valor'''
    params = get_params(t)
    if len(t) > 5:
        if t[3] == 'pop' or t[3] == 'join':
            t[0] = ArrayMetodos(params.line, params.column, t[1], t[3], None)
        else:
            t[0] = FuncionesEmbebidas(params.line, params.column, t[3], t[1])
    elif len(t) > 4:
        t[0] = ArrayMetodos(params.line, params.column, t[1], t[3], t[4])
    elif len(t) > 3:
        if t[3] == 'length':
            t[0] = ArrayMetodos(params.line, params.column, t[1], t[3], None)
        else:
            t[0] = InterfaceAccess(params.line, params.column, t[1], t[3])
    elif len(t) > 2:
        t[0] = ArrayAccess(params.line, params.column, t[1], t[2])
    else:
        t[0] = t[1]

def p_expression_access_array(t):
    '''indexes : indexes CORIZQ expression CORDER
               | CORIZQ expression CORDER'''
    indexes = []
    if len(t) > 4:
        indexes = t[1] + [t[3]]
    else:
        indexes.append(t[2])
    t[0] = indexes

def p_func_embebidas(t):
    '''expression : typeof
                  | parseint
                  | parsefloat'''
    t[0] = t[1]

def p_expression_typeof(t):
    'typeof : TYPEOF expression'
    params = get_params(t)
    t[0] = FuncionesEmbebidas(params.line, params.column, 'typeof', t[2])

def p_expression_parseInt(t):
    'parseint : PARSEINT expression'
    params = get_params(t)
    t[0] = FuncionesEmbebidas(params.line, params.column, 'parseInt', t[2])

def p_expression_parseFloat(t):
    'parsefloat : PARSEFLOAT expression'
    params = get_params(t)
    t[0] = FuncionesEmbebidas(params.line, params.column, 'parseFloat', t[2])

def p_error(p):
    if p:
        print(f"Error de sintaxis en línea {p.lineno}, columna {p.lexpos}: Token inesperado '{p.value}'")
    else:
        print("Error de sintaxis")

def get_params(t):
    line = t.lexer.lineno  # Obtener la línea actual desde el lexer
    lexpos = t.lexpos if isinstance(t.lexpos, int) else 0  # Verificar si lexpos es un entero
    column = lexpos - t.lexer.lexdata.rfind('\n', 0, lexpos) 
    return codeParams(line, column)

class Parser:
    def __init__(self):
        pass

    def interpretar(self, input):
        lexer = Lex.lex()
        parser = yacc.yacc()
        result = parser.parse(input)
        return result
