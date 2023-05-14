from typing import List, Tuple
import re


class ParsedStruct:
    def __init__(self, name: str, fields: List[Tuple[str, str, str]]):
        self.name = name
        self.fields = self.__parse_fields(fields)

    @staticmethod
    def __parse_fields(fields):
        parsed_fields = []
        for visibility, field_name, field_type in fields:
            if not visibility:
                visibility = 'private'
            parsed_fields.append((visibility, field_name, field_type))
        return parsed_fields

    def __repr__(self):
        return f"<ParsedStruct name={self.name}, fields={self.fields}>"


class ParsedRecord(ParsedStruct):
    def __repr__(self):
        return f"<ParsedRecord name={self.name}, fields={self.fields}>"


class ParsedFunction:
    def __init__(self, name: str, input_params: List[Tuple[str, str, str]], output_params: List[str]):
        self.name = name
        self.input_params = input_params
        self.output_params = output_params

    def __repr__(self):
        return f"<ParsedFunction name={self.name}, input_params={self.input_params}, output_params={self.output_params}>"


class LeoParser:
    def __init__(self, content: str):
        self.content = self.remove_comments(content)
        self.imports = self.parse_imports()
        self.program_id = self.parse_program_id()
        self.structs, self.records = self.parse_structs()
        self.functions = self.parse_functions()

    @staticmethod
    def remove_comments(content: str) -> str:
        lines = content.split('\n')
        filtered_lines = [line for line in lines if not line.strip().startswith('//')]
        return '\n'.join(filtered_lines)

    def parse_program_id(self) -> str:
        program_id_pattern = r"program (\w+)\.aleo"
        return re.findall(program_id_pattern, self.content)[0]

    def parse_imports(self):
        import_pattern = r"\s*import\s+(\w+)\.leo"
        return re.findall(import_pattern, self.content)

    def parse_structs(self) -> tuple[List[ParsedStruct], List[ParsedRecord]]:
        struct_pattern = r"(struct|record)\s+(\w+)\s*{([^}]*)}"
        structs = re.findall(struct_pattern, self.content)
        parsed_structs = []
        parsed_records = []

        for struct_type, struct_name, struct_body in structs:
            field_pattern = r"(public|private|constant)?\s*(\w+):\s*(\w+),?"
            fields = re.findall(field_pattern, struct_body)
            if struct_type == "struct":
                parsed_structs.append(ParsedStruct(struct_name, fields))
            else:
                parsed_records.append(ParsedRecord(struct_name, fields))

        return parsed_structs, parsed_records

    def parse_functions(self) -> List[ParsedFunction]:
        function_pattern = r"transition\s+(\w+)\s*\(([^)]*)\)\s*(->\s*\(?(.+?)\)?\s*)?\{"
        functions = re.findall(function_pattern, self.content)
        parsed_functions = []

        for func_name, input_params, _, out_params in functions:
            param_pattern = r"(public|private|constant)?\s*(\w+):\s*((\w+\.leo\/)?\w+)(\.record)?"
            input_params = re.findall(param_pattern, input_params)

            parsed_input_params = []
            for visibility, name, param_type, _, _ in input_params:
                if not visibility:
                    visibility = "private"
                parsed_input_params.append((visibility, name, param_type.replace('.leo/', '__')))

            output_param_pattern = r'((\w+\.leo\/)?\w+)(\.record)?'
            out_params = re.findall(output_param_pattern, out_params)
            parsed_output_params = [p[0].replace('.leo/', '__') for p in out_params]

            parsed_functions.append(ParsedFunction(func_name, parsed_input_params, parsed_output_params))

        return parsed_functions
