from interfaces.instruction import Instruction
from environment.execute import StatementExecuter
from environment.environment import Environment
from expressions.continue_statement import Continue
from environment.types import ExpressionType

class InterfaceAssignment(Instruction):
    def __init__(self, line, col, acceso, exp):
        self.line = line
        self.col = col
        self.acceso = acceso
        self.exp = exp

    def ejecutar(self, ast, env):
        env_interface = self.acceso.exp.ejecutar(ast, env)
        struct = env_interface.tabla
        attribute = self.acceso.id
        struct[attribute] = self.exp.ejecutar(ast, env)
        return None