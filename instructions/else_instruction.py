from interfaces.instruction import Instruction
from environment.execute import StatementExecuter
from environment.environment import Environment
from expressions.continue_statement import Continue

class Else(Instruction):
    def __init__(self, line, col, block):
        self.line = line
        self.col = col
        self.block = block

    def ejecutar(self, ast, env):
        # Crear entorno del Else
        returnValue = StatementExecuter(self.block, ast, env)
        if returnValue != None:
            return returnValue
        return None