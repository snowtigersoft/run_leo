import json

from .aleo_account import Account
from .leo_struct import LeoStruct


class LeoProgram:
    program_root = None

    def __init__(self):
        self.config_file = f'{self.program_root}/program.json'
        with open(self.config_file, 'r') as f:
            self.config = json.load(f)
        self.program_id = self.config['program']
        self.__replace_struct_data_type()

    def __replace_struct_data_type(self):
        """
        Replace custom struct or record data_type in struct/record
        :return:
        """
        for attr in self.__dir__():
            if attr.startswith('__'):
                continue
            val = getattr(self, attr)
            if type(val) == type:
                new_fields = []
                for field in val.fields:
                    new_fields.append((field[0], field[1], getattr(self, field[2], field[2])))
                val.fields = new_fields

    def show_config(self):
        print(self.config)

    def set_account(self, account: Account):
        """
        Set the account use for development
        :param account:
        :return:
        """
        self.config['development'].update({
            'address': account.address,
            'private_key': account.private_key,
            'view_key': account.view_key
        })
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f)
