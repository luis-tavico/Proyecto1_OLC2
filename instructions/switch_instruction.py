from interfaces.instruction import Instruction
from environment.execute import StatementExecuter
from environment.environment import Environment
from expressions.continue_statement import Continue

class Switch(Instruction):
    def __init__(self, line, col, exp, cases, default):
        self.line = line
        self.col = col
        self.exp = exp
        self.cases = cases
        self.default = default

    def ejecutar(self, ast, env):
        # Obtener simbolo
        switch_env = Environment(env, "SWITCH")
        validate = self.exp.ejecutar(ast, switch_env)
        # Evaluar
        for case in self.cases:
            validata_case = case.exp.ejecutar(ast, switch_env)
            if validate.value == validata_case.value:
                returnValue = case.ejecutar(ast, switch_env)
                if returnValue != None:
                    return returnValue
                return None
        if self.default != None:
            returnValue = self.default.ejecutar(ast, env)
            if returnValue != None:
                return returnValue
        return None