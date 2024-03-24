from interfaces.instruction import Instruction
from environment.execute import StatementExecuter
from environment.environment import Environment
from expressions.continue_statement import Continue
from environment.types import ExpressionType


class For(Instruction):
    def __init__(self, line, col, declaration, exp1, exp2, block):
        self.line = line
        self.col = col
        self.declaration = declaration
        self.exp1 = exp1
        self.exp2 = exp2
        self.block = block

    def ejecutar(self, ast, env):
        # Variables de iteración
        safe_cont = 0
        Flag = None
        result = None
        dec = self.declaration.ejecutar(ast, env)
        # Ciclo
        while True:
            safe_cont += 1
            # Obtencion de la expresión
            result = self.exp1.ejecutar(ast, env)
            # Validación
            if result.value:
                while_env = Environment(env, "WHILE")
                Flag = StatementExecuter(self.block, ast, while_env)
                # Validar si es sentencia de transferencia
                if Flag != None:
                    if Flag.type == ExpressionType.BREAK:
                        break
                    if Flag.type == ExpressionType.CONTINUE:
                        continue
                    if Flag.type == ExpressionType.RETURN:
                        return Flag
            else:
                break
            resultexp2 = self.exp2.ejecutar(ast, env)
            # Validar limite de seguridad
            if safe_cont >= 1000:
                ast.setErrors('Se ha excedido el máximo de ciclos permitidos')
                break