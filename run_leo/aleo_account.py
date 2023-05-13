import json
import re

from .utils import run_command_in_directory


class Account:
    def __init__(self, address=None, private_key=None, view_key=None):
        self.address = address
        self.private_key = private_key
        self.view_key = view_key

    def __repr__(self):
        return f"<Account address={self.address} private_key={self.private_key} view_key={self.view_key}>"

    @classmethod
    def new(cls, seed=None):
        """
        To create a new account

        :param seed: To create a new account from seeded randomness, default None
        :return:
        """
        command = 'aleo account new'
        if seed:
            command += f' -s {seed}'
        resp = run_command_in_directory(command)

        private_key_search = re.search(r"Private Key  (\w+)", resp)
        view_key_search = re.search(r"View Key  (\w+)", resp)
        address_search = re.search(r"Address  (\w+)", resp)

        if private_key_search and view_key_search and address_search:
            private_key = private_key_search.group(1)
            view_key = view_key_search.group(1)
            address = address_search.group(1)
            return cls(address, private_key, view_key)

        raise Exception("Create aleo account failed")

    @classmethod
    def load(cls, file_path):
        """
        Load account info from file_path
        :param file_path:
        :return:
        """
        with open(file_path, 'f') as f:
            info = json.load(f)
        return cls(info['address'], info['private_key'], info['view_key'])

    def save(self, file_path):
        """
        Save account info to file_path
        :param file_path:
        :return:
        """
        with open(file_path, 'w') as f:
            json.dump({
                'account': self.address,
                'private_key': self.private_key,
                'view_key': self.view_key
            }, f)
