from interfaces.instruction import Instruction
from environment.execute import StatementExecuter
from environment.environment import Environment
from expressions.continue_statement import Continue

class ElseIf(Instruction):
    def __init__(self, line, col, exp, block):
        self.line = line
        self.col = col
        self.exp = exp
        self.block = block

    def ejecutar(self, ast, env):
        # Obtener simbolo
        validate = self.exp.ejecutar(ast, env)
        # Evaluar
        if validate.value:
            # Crear entorno del ElseIf
            returnValue = StatementExecuter(self.block, ast, env)
            if returnValue != None:
                return returnValue
            return True
        return None
