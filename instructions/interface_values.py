from interfaces.instruction import Instruction
from environment.types import ExpressionType
from environment.symbol import Symbol

class Values():
    def __init__ (self, line, col, id):
        self.id = id
        self.line = line
        self.col = col
        
    def ejecutar(self, ast, env):
        env_interface = self.id.ejecutar(ast, env)
        struct = env_interface.tabla
        values = []
        for value in list(struct.values()):
            values.append(value)
        return Symbol(value=values, type=ExpressionType.ARRAY, line=self.line, col=self.col)