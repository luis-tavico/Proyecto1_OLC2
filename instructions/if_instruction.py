from interfaces.instruction import Instruction
from environment.execute import StatementExecuter
from environment.environment import Environment
from expressions.continue_statement import Continue

class If(Instruction):
    def __init__(self, line, col, exp, block, elseIfBlock, elseBlock):
        self.line = line
        self.col = col
        self.exp = exp
        self.block = block
        self.elseIfBlock = elseIfBlock
        self.elseBlock = elseBlock

    def ejecutar(self, ast, env):
        # Obtener simbolo
        validate = self.exp.ejecutar(ast, env)
        # Evaluar
        if validate.value:
            # Crear entorno del If
            if_env = Environment(env, "IF")
            returnValue = StatementExecuter(self.block, ast, if_env)
            if returnValue != None:
                return returnValue
            return None
        if self.elseIfBlock != None:
            for elseIf in self.elseIfBlock:
                returnValue = elseIf.ejecutar(ast, env)
                if returnValue == True:
                    return None
                if returnValue != None:
                    return returnValue
        if self.elseBlock != None:
            returnValue = self.elseBlock.ejecutar(ast, env)
            if returnValue != None:
                return returnValue
        return None