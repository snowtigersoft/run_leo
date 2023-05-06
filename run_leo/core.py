import os.path

from .leo_function import LeoFunction
from .leo_parser import LeoParser
from .leo_struct import LeoStruct


def import_leo_program(leo_path):
    assert os.path.exists(f'{leo_path}/src/main.leo'), f'file {leo_path}/src/main.leo not exists'

    with open(f'{leo_path}/src/main.leo', 'r') as f:
        code = f.read()

    parser = LeoParser(code)

    class_attrs = {}

    for struct in parser.structs:
        class_attrs[struct.name] = type(struct.name, (LeoStruct,), {'fields': struct.fields})

    for func in parser.functions:
        class_attrs[func.name] = LeoFunction(leo_path, func.name, func.input_params)

    return type("LeoProgram", (object,), class_attrs)
