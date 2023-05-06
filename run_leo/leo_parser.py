from typing import List, Tuple
import re


class ParsedStruct:
    def __init__(self, name: str, fields: List[Tuple[str, str, str]]):
        self.name = name
        self.fields = fields

    def __repr__(self):
        return f"<ParsedStruct name={self.name}, fields={self.fields}>"


class ParsedFunction:
    def __init__(self, name: str, input_params: List[Tuple[str, str]]):
        self.name = name
        self.input_params = input_params

    def __repr__(self):
        return f"<ParsedFunction name={self.name}, input_params={self.input_params}>"


class LeoParser:
    def __init__(self, content: str):
        self.content = self.remove_comments(content)
        self.structs = self.parse_structs()
        self.functions = self.parse_functions()

    @staticmethod
    def remove_comments(content: str) -> str:
        lines = content.split('\n')
        filtered_lines = [line for line in lines if not line.strip().startswith('//')]
        return '\n'.join(filtered_lines)

    def parse_structs(self) -> List[ParsedStruct]:
        struct_pattern = r"(struct|record)\s+(\w+)\s*{([^}]*)}"
        structs = re.findall(struct_pattern, self.content)
        parsed_structs = []

        for _, struct_name, struct_body in structs:
            field_pattern = r"(\w+):\s*(\w+),?"
            fields = re.findall(field_pattern, struct_body)
            parsed_structs.append(ParsedStruct(struct_name, fields))

        return parsed_structs

    def parse_functions(self) -> List[ParsedFunction]:
        function_pattern = r"transition\s+(\w+)\s*\(([^)]*)\)\s*->"
        functions = re.findall(function_pattern, self.content)
        parsed_functions = []

        for func_name, input_params in functions:
            param_pattern = r"(public|private|constant)?\s*(\w+):\s*(\w+)"
            input_params = re.findall(param_pattern, input_params)

            parsed_input_params = []
            for visibility, name, param_type in input_params:
                if not visibility:
                    visibility = "private"
                parsed_input_params.append((visibility, name, param_type))

            parsed_functions.append(ParsedFunction(func_name, parsed_input_params))

        return parsed_functions









