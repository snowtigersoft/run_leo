import json
import re

from .leo_struct import LeoStruct
from .utils import run_command_in_directory, LeoDataType


class LeoFunction:
    def __init__(self, leo_folder, name, input_params, output_params):
        self.leo_folder = leo_folder
        self.name = name
        self.input_params = input_params
        self.output_params = output_params

        # set doc string
        param_docs = []
        for visibility, param_name, param_type in input_params:
            param_docs.append(f"{visibility} {param_name}: {param_type}")
        self.__doc__ = "Parameters:\n" + "\n".join(param_docs) + \
                       "\nReturns: " + ','.join([p if isinstance(p, str) else p.__name__ for p in output_params])

    def parse_run_command(self, *args, **kwargs):
        command_args = []
        for pos, param in enumerate(self.input_params):
            if pos < len(args):
                value = args[pos]
            elif param[1] in kwargs:
                value = kwargs[param[1]]
            else:
                raise AssertionError(f'Missing function args {param[1]}')
            data_type = param[2]
            if data_type in LeoDataType.BOOL:
                assert isinstance(value, bool), f'{param[1]} type error, require bool'
                tmp = 'true' if value else 'false'
            elif data_type in LeoDataType.SIGNED:
                assert isinstance(value, int), f'{param[1]} type error, require {data_type}'
                tmp = f'{value}{data_type}'
            elif data_type in LeoDataType.ARITHMETIC:
                assert isinstance(value, int) and value >= 0, f'{param[1]} type error, require unsigned int'
                tmp = f'{value}{data_type}'
            elif data_type in LeoDataType.ADDRESS:
                tmp = value
            else:
                # Struct or Record
                assert isinstance(value, LeoStruct) and value.__class__.__name__ == data_type, \
                    f"{param[1]} type error, require {data_type}"
                tmp = "'" + str(value) + "'"
            command_args.append(tmp)
        return f'leo run {self.name} {" ".join(command_args)}'

    def __parse_type(self, data_type, value):
        """
        parse return value to python datatype
        :param data_type:
        :param value:
        :return:
        """
        if data_type in LeoDataType.BOOL:
            return value == 'true'
        elif data_type in LeoDataType.ARITHMETIC:
            return int(value.replace(data_type, ''))
        elif data_type in LeoDataType.ADDRESS:
            return value
        elif issubclass(data_type, LeoStruct):
            # For LeoStruct or LeoRecord types, we assume that 'value' is a dictionary
            # where keys are field names and values are string representations of field values.
            instance = data_type()
            for field_name, field_value in value.items():
                if field_name == '_nonce':
                    vis, field_type = 'public', 'group'
                else:
                    vis, field_type = next((field[0], field[2]) for field in data_type.fields if field[1] == field_name)
                if isinstance(field_value, str) and field_value.endswith(f'.{vis}'):
                    field_value = field_value[:-1 - len(vis)]
                instance[field_name] = self.__parse_type(field_type, field_value)
            return instance

    def __parse_output(self, output):
        """
        parse the output to data_type
        :param output:
        :return:
        """
        output_pattern = re.compile(r"➡️\s*Outputs?\n\n(.*?)\n\n\s*Leo ✅ Executed", re.DOTALL)
        output_match = output_pattern.search(output)
        outputs = []

        if output_match:
            output_string = output_match.group(1)
            parts = re.split("•", output_string)
            part_pattern = re.compile(r"\s*(\w+)\s*:\s*(.*),?")
            for part in parts:
                part = part.strip()
                if part:
                    output_type = self.output_params[len(outputs)]
                    part_match = part_pattern.findall(part)
                    if part_match:
                        outputs.append(self.__parse_type(output_type, json.loads(re.sub(r'\b(\w+(?:\.\w+)?)\b', r'"\1"', part))))
                    else:
                        outputs.append(self.__parse_type(output_type, part))
        return outputs[0] if len(outputs) == 1 else tuple(outputs)

    def __call__(self, *args, **kwargs):
        run_command = self.parse_run_command(*args, **kwargs)
        output = run_command_in_directory(run_command, self.leo_folder)
        return self.__parse_output(output)
