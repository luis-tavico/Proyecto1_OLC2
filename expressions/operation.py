from interfaces.expression import Expression
from environment.types import ExpressionType
from environment.symbol import Symbol

dominant_table = [
    [ExpressionType.NUMBER,  ExpressionType.FLOAT, ExpressionType.NULL,   ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL],
    [ExpressionType.FLOAT,   ExpressionType.FLOAT, ExpressionType.NULL,   ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL],
    [ExpressionType.NULL,    ExpressionType.NULL,  ExpressionType.STRING, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL],
    [ExpressionType.NULL,    ExpressionType.NULL,  ExpressionType.NULL,   ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL],
    [ExpressionType.NULL,    ExpressionType.NULL,  ExpressionType.NULL,   ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL],
    [ExpressionType.NULL,    ExpressionType.NULL,  ExpressionType.NULL,   ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL],
    [ExpressionType.NULL,    ExpressionType.NULL,  ExpressionType.NULL,   ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL],
    [ExpressionType.NULL,    ExpressionType.NULL,  ExpressionType.NULL,   ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL],
    [ExpressionType.NULL,    ExpressionType.NULL,  ExpressionType.NULL,   ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL],
    [ExpressionType.NULL,    ExpressionType.NULL,  ExpressionType.NULL,   ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL],
    [ExpressionType.NULL,    ExpressionType.NULL,  ExpressionType.NULL,   ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL]
]

class Operation(Expression):
    def __init__(self, line, col, operador, opL, opR):
        self.line = line
        self.col = col
        self.operador = operador
        self.opL = opL
        self.opR = opR

    def ejecutar(self, ast, env):
        op1 = self.opL.ejecutar(ast, env)
        op2 = None
        dominant_type = ExpressionType.NULL
        if self.opR != None:
            op2 = self.opR.ejecutar(ast, env)
            dominant_type = dominant_table[op1.type.value][op2.type.value]
        elif self.operador == '!':
            dominant_type = ExpressionType.BOOLEAN
        # Suma
        if self.operador == "+":
            symbol = Symbol(line=self.line, col=self.col, value=op1.value+op2.value, type=dominant_type)
            return symbol
        # Resta
        if self.operador == "-":
            if self.opR != None:
                if dominant_type == ExpressionType.NUMBER or dominant_type == ExpressionType.FLOAT:
                    return Symbol(line=self.line, col=self.col, value=op1.value-op2.value, type=dominant_type)
                ast.setErrors('Error: tipos incorrectos para restar')
            # NEGATIVO
            else:
                if op1.type == ExpressionType.NUMBER or op1.type == ExpressionType.FLOAT:
                    return Symbol(line=self.line, col=self.col, value=-op1.value, type=op1.type)
                ast.setErrors('Error: tipos incorrectos para negativo')
        # Multiplicación
        if self.operador == "*":
            if dominant_type == ExpressionType.NUMBER or dominant_type == ExpressionType.FLOAT:
                return Symbol(line=self.line, col=self.col, value=op1.value*op2.value, type=dominant_type)
            ast.setErrors('Error: tipos incorrectos para multiplicar')
        # División
        if self.operador == "/":
            if op2.value == 0:
                ast.setErrors("Error: no se puede dividir por 0")
                return 
            if dominant_type == ExpressionType.NUMBER or dominant_type == ExpressionType.FLOAT:
                return Symbol(line=self.line, col=self.col, value=op1.value/op2.value, type=dominant_type)
            ast.setErrors('Error: tipos incorrectos para dividir')
        # Módulo
        if self.operador == "%":
            if dominant_type == ExpressionType.NUMBER or dominant_type == ExpressionType.FLOAT:
                return Symbol(line=self.line, col=self.col, value=op1.value%op2.value, type=dominant_type)
            ast.setErrors('Error: tipos incorrectos para módulo')
        # MAYOR QUE
        if self.operador == ">":
            if dominant_type == ExpressionType.NUMBER or dominant_type == ExpressionType.FLOAT:
                return Symbol(line=self.line, col=self.col, value=op1.value > op2.value, type=ExpressionType.BOOLEAN)
            ast.setErrors('Error: tipos incorrectos para mayor qué')
        # MENOR QUE
        if self.operador == "<":
            if dominant_type == ExpressionType.NUMBER or dominant_type == ExpressionType.FLOAT:
                return Symbol(line=self.line, col=self.col, value=op1.value < op2.value, type=ExpressionType.BOOLEAN)
            ast.setErrors('Error: tipos incorrectos para menor qué')
        # MAYOR IGUAL QUE
        if self.operador == ">=":
            if dominant_type == ExpressionType.NUMBER or dominant_type == ExpressionType.FLOAT:
                return Symbol(line=self.line, col=self.col, value=op1.value >= op2.value, type=ExpressionType.BOOLEAN)
            ast.setErrors('Error: tipos incorrectos para mayor igual qué')
        # MENOR IGUAL QUE
        if self.operador == "<=":
            if dominant_type == ExpressionType.NUMBER or dominant_type == ExpressionType.FLOAT:
                return Symbol(line=self.line, col=self.col, value=op1.value <= op2.value, type=ExpressionType.BOOLEAN)
            ast.setErrors('Error: tipos incorrectos para menor igual qué')
        # IGUAL
        if self.operador == "==":
            return Symbol(line=self.line, col=self.col, value=op1.value == op2.value, type=ExpressionType.BOOLEAN)
        # DIFERENTE
        if self.operador == "!=":
            return Symbol(line=self.line, col=self.col, value=op1.value != op2.value, type=ExpressionType.BOOLEAN)
        # AND
        if self.operador == "&&":
            return Symbol(line=self.line, col=self.col, value=op1.value and op2.value, type=ExpressionType.BOOLEAN)
        # OR
        if self.operador == "||":
            return Symbol(line=self.line, col=self.col, value=op1.value or op2.value, type=ExpressionType.BOOLEAN)
        # NOT
        if self.operador == "!":
            return Symbol(line=self.line, col=self.col, value=not op1.value, type=ExpressionType.BOOLEAN)
        # INCREMENTO
        if self.operador == "++":
            if op1.type == ExpressionType.NUMBER or op1.type == ExpressionType.FLOAT:
                sym = Symbol(line=self.line, col=self.col, value=op1.value+1, type=op1.type)
                env.setVariable(ast, self.opL.id, sym)
                return sym
            ast.setErrors('Error: tipos incorrectos para incremento')
        return Symbol(line=self.line, col=self.col, value=None, type=ExpressionType.NULL)