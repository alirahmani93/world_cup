import uuid

from random import random


def random_code(prefix: str = None, number_length: int = 3, string_length: int = 3, numeric: bool = True,
                stringify: bool = True):
    code = ''
    if stringify:
        st = uuid.uuid4().hex[:string_length]
        code += st
    if numeric:
        int_code = int(random() * (10 ** number_length))
        if stringify:
            code += str(int_code)
        else:
            code = int_code
    if prefix:
        code = prefix + code
    return code
