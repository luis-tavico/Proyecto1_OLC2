from interfaces.instruction import Instruction
from environment.types import ExpressionType
from environment.symbol import Symbol

class Keys(Instruction):
    def __init__ (self, line, col, id):
        self.id = id
        self.line = line
        self.col = col

    def ejecutar(self, ast, env):
        env_interface = self.id.ejecutar(ast, env)
        struct = env_interface.tabla
        keys = []
        for key in list(struct.keys()):
            keys.append(Symbol(value=key, type=ExpressionType.STRING, line=self.line, col=self.col))
        return Symbol(value=keys, type=ExpressionType.ARRAY, line=self.line, col=self.col)