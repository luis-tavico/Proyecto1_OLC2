from interfaces.expression import Expression
from environment.types import ExpressionType

class ArrayAccess(Expression):
    def __init__(self, line, col, array, index):
        self.line = line
        self.col = col
        self.array = array
        self.index = index

    def ejecutar(self, ast, env):
        # Traer el arreglo
        sym = self.array.ejecutar(ast, env)
        # Validar tipo principal
        if sym.type != ExpressionType.ARRAY:
            ast.setErrors('La variable no es un arreglo')
            return
        return self.indice(sym.value, self.index)

    
    def indice(self, arreglo, indices):
        if len(indices) == 1:
            return arreglo[indices[0].value]
        else:
            return self.indice(arreglo[indices[0].value].value, indices[1:])