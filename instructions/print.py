from interfaces.instruction import Instruction
from environment.types import ExpressionType

class Print(Instruction):
    def __init__(self, line, col, Exp):
        self.line = line
        self.col = col
        self.Exp = Exp

    def ejecutar(self, ast, env):
        outText = ""
        for exp in self.Exp:
            sym = exp.ejecutar(ast, env)
            if sym == None:
                continue
            if sym.type == ExpressionType.ARRAY:
                outText += self.imprimir_vector_matriz(sym.value)
            else:
                outText += " " + str(sym.value)
        ast.setConsole(outText)

    def imprimir_vector_matriz(self, array):
        result = ""
        if isinstance(array, list):
            result += "[ "
            for i, sym in enumerate(array):
                result += self.imprimir_vector_matriz(sym)
                if i < len(array) - 1:
                    result += ", "
            result += " ]"
        elif array.type == ExpressionType.ARRAY:
            result += "[ "
            for i, sym in enumerate(array.value):
                result += self.imprimir_vector_matriz(sym)
                if i < len(array.value) - 1:
                    result += ", "
            result += " ]"
        else:
            result += str(array.value)
        return result