from interfaces.instruction import Instruction
from environment.execute import StatementExecuter
from environment.environment import Environment
from expressions.continue_statement import Continue
from environment.types import ExpressionType
from environment.symbol import Symbol

class ArrayMetodos(Instruction):
    def __init__(self, line, col, id, name, expression):
        self.line = line
        self.col = col
        self.id = id
        self.name = name
        self.expression = expression

    def ejecutar(self, ast, env):
        result = self.id.ejecutar(ast, env)
        if self.name == "push":
            if result.type == ExpressionType.ARRAY:
                val = self.expression.ejecutar(ast, env)
                result.value.append(val)
                return None
            else:
                ast.setErrors("Error: el metodo push solo puede ser aplicado a arreglos")
        elif self.name == "pop":
            if len(result.value) > 0:
                return result.value.pop()
            else:
                ast.setErrors("Error: no se puede aplicar el metodo pop a un arreglo vacio")
        elif self.name == "indexOf":
            if result.type == ExpressionType.ARRAY:
                val = self.expression.ejecutar(ast, env)
                for i, val_arr in enumerate(result.value):
                    if val_arr.value == val.value:
                        return Symbol(value=i, type=ExpressionType.NUMBER, line=self.line, col=self.col)
                return Symbol(value=-1, type=ExpressionType.NUMBER, line=self.line, col=self.col)
            else:
                ast.setErrors("Error: el metodo indexOf solo puede ser aplicado a arreglos")
        elif self.name == "join":
            if result.type == ExpressionType.ARRAY:
                return Symbol(value=", ".join([str(val.value) for val in result.value]), type=ExpressionType.STRING, line=self.line, col=self.col)
            else:
                ast.setErrors("Error: el metodo join solo puede ser aplicado a arreglos")
        elif self.name == "length":
            return Symbol(line=self.line, col=self.col, value=len(result.value), type=ExpressionType.NUMBER)
        return None