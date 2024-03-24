from interfaces.instruction import Instruction
from environment.execute import StatementExecuter
from environment.environment import Environment
from expressions.continue_statement import Continue
from environment.types import ExpressionType
from environment.symbol import Symbol

class FuncionesEmbebidas(Instruction):
    def __init__(self, line, col, name, expression):
        self.line = line
        self.col = col
        self.name = name
        self.expression = expression

    def ejecutar(self, ast, env):
        if self.name == "parseInt":
            result = self.expression.ejecutar(ast, env)
            try:
                return Symbol(line=self.line, col=self.col, value=int(result.value), type=ExpressionType.NUMBER)
            except:
                ast.setErrors("Error: no se puede convertir a entero")
        elif self.name == "parseFloat":
            result = self.expression.ejecutar(ast, env)
            try:
                return Symbol(line=self.line, col=self.col, value=float(result.value), type=ExpressionType.FLOAT)
            except:
                ast.setErrors("Error: no se puede convertir a flotante")
        elif self.name == "toString":
            result = self.expression.ejecutar(ast, env)
            return Symbol(line=self.line, col=self.col, value=str(result.value), type=ExpressionType.STRING)
        elif self.name == "toLowerCase":
            result = self.expression.ejecutar(ast, env)
            return Symbol(line=self.line, col=self.col, value=result.value.lower(), type=ExpressionType.STRING)
        elif self.name == "toUpperCase":
            result = self.expression.ejecutar(ast, env)
            return Symbol(line=self.line, col=self.col, value=result.value.upper(), type=ExpressionType.STRING)
        elif self.name == "typeof":
            result = self.expression.ejecutar(ast, env)
            return Symbol(line=self.line, col=self.col, value=result.type.name.lower(), type=ExpressionType.STRING)
        return None