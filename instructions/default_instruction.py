from interfaces.instruction import Instruction
from environment.execute import StatementExecuter
from environment.environment import Environment
from expressions.continue_statement import Continue

class Default(Instruction):
    def __init__(self, line, col, block):
        self.line = line
        self.col = col
        self.block = block

    def ejecutar(self, ast, env):
        # Crear entorno del Default
        default_env = Environment(env, "DEFAULT")
        returnValue = StatementExecuter(self.block, ast, default_env)
        if returnValue != None:
            return returnValue
        return None