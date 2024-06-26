from interfaces.instruction import Instruction
from environment.types import ExpressionType
from environment.environment import Environment

class ArrayDeclaration(Instruction):
    def __init__(self, line, col, id, type, exp):
        self.line = line
        self.col = col
        self.id = id
        self.type = type
        self.exp = exp

    def ejecutar(self, ast, env):
        # Obtener simbolo
        result = self.exp.ejecutar(ast, env)
        # Validar tipo principal
        if result.type != ExpressionType.ARRAY:
            ast.setErrors('La expresión no es un arreglo')
            return
        # Validar tipos
        for res in result.value:
            if isinstance(res, Environment):
                pass
            if res.type != self.type and res.type != ExpressionType.ARRAY:
                ast.setErrors('El arreglo contiene tipos incorrectos')
                return
        # Agregar al entorno
        env.saveVariable(ast, self.id, result)