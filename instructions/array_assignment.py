from interfaces.instruction import Instruction
from environment.execute import StatementExecuter
from environment.environment import Environment
from expressions.continue_statement import Continue
from environment.types import ExpressionType

class ArrayAssignment(Instruction):
    def __init__(self, line, col, id, index, exp):
        self.line = line
        self.col = col
        self.id = id
        self.index = index
        self.exp = exp

    def ejecutar(self, ast, env): 
        sym = self.id.ejecutar(ast, env)
        if sym.type != ExpressionType.ARRAY:
            ast.setErrors('La variable no es un arreglo')
            return
        exp = self.exp.ejecutar(ast, env)
        return self.nuevo_valor(sym.value, self.index, exp)
    

    def nuevo_valor(self, array, index, valor):
        if len(index) == 1:
            array[index[0].value] = valor
        else:
            self.nuevo_valor(array[index[0].value].value, index[1:], valor)