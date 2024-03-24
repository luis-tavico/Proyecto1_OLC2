from enum import Enum

class ExpressionType(Enum):
    NUMBER = 0
    FLOAT = 1
    STRING = 2
    CHAR = 3
    BOOLEAN = 4
    ARRAY = 5
    STRUCT = 6
    NULL = 7
    BREAK = 8
    CONTINUE = 9
    RETURN = 10