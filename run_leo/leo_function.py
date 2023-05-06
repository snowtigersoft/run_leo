import subprocess

from run_leo.leo_struct import LeoStruct


def run_command_in_directory(command, directory):
    full_command = f"source $HOME/.cargo/env && {command}"

    process = subprocess.Popen(
        full_command,
        shell=True,
        cwd=directory,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    stdout, stderr = process.communicate()

    if process.returncode != 0:
        raise Exception(stderr.decode('utf-8'))
    else:
        return stdout.decode('utf-8')


class LeoFunction:
    def __init__(self, leo_folder, name, input_params):
        self.leo_folder = leo_folder
        self.name = name
        self.input_params = input_params

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
            if data_type == 'bool':
                assert isinstance(value, bool), f'{param[1]} type error, require bool'
                tmp = 'true' if value else 'false'
            elif data_type in ['i8', 'i16', 'i32', 'i64', 'i128']:
                assert isinstance(value, int), f'{param[1]} type error, require {data_type}'
                tmp = f'{value}{data_type}'
            elif data_type in ['u8', 'u16', 'u32', 'u64', 'u128', 'group', 'field', 'scalar']:
                assert isinstance(value, int) and value >= 0, f'{param[1]} type error, require unsigned int'
                tmp = f'{value}{data_type}'
            elif data_type == 'address':
                tmp = value
            else:
                # Struct or Record
                assert isinstance(value, LeoStruct) and value.__class__.__name__ == data_type, \
                    f"{param[1]} type error, require {data_type}"
                tmp = '"' + str(value) + '"'
            command_args.append(tmp)
        return f'leo run {self.name} {" ".join(command_args)}'

    def __call__(self, *args, **kwargs):
        run_command = self.parse_run_command(*args, **kwargs)
        return run_command_in_directory(run_command, self.leo_folder)
