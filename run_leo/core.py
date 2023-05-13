import os.path
from typing import Type

from .leo_function import LeoFunction
from .leo_parser import LeoParser
from .leo_struct import LeoStruct, LeoRecord
from .leo_program import LeoProgram


def import_leo_program(leo_path) -> Type[LeoProgram]:
    assert os.path.exists(f'{leo_path}/src/main.leo'), f'file {leo_path}/src/main.leo not exists'

    with open(f'{leo_path}/src/main.leo', 'r') as f:
        code = f.read()

    parser = LeoParser(code)

    class_attrs = {
        'program_root': leo_path
    }

    for struct in parser.structs:
        class_attrs[struct.name] = type(struct.name, (LeoStruct,), {'fields': struct.fields})

    for record in parser.records:
        class_attrs[record.name] = type(record.name, (LeoRecord,), {'fields': record.fields})

    # parse imports
    for imp in parser.imports:
        with open(f'{leo_path}/imports/{imp}.leo', 'r') as f:
            code = f.read()
        imp_parser = LeoParser(code)
        for struct in imp_parser.structs:
            struct_name = f'{imp}__{struct.name}'
            class_attrs[struct_name] = type(struct_name, (LeoStruct,), {'fields': struct.fields})
        for record in imp_parser.records:
            record_name = f'{imp}__{record.name}'
            class_attrs[record_name] = type(record_name, (LeoRecord,), {'fields': record.fields})

    for func in parser.functions:
        output_params = [class_attrs.get(o, o) for o in func.output_params]
        class_attrs[func.name] = LeoFunction(leo_path, func.name, func.input_params, output_params)

    return type(f"{parser.program_id}", (LeoProgram,), class_attrs)
