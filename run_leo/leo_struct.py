class LeoStruct(dict):
    fields = []

    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__
    __delattr__ = dict.__delitem__

    def __repr__(self):
        return self.__str__()

    def fields_to_str(self):
        items = []
        for field in self.fields:
            _, field_name, data_type = field
            assert field_name in self, f"Missing key {field_name} in {self.__class__.__name__}"
            value = self[field_name]
            tmp = f"{field_name}: "
            if data_type == 'bool':
                assert isinstance(value, bool), f'{field_name} type error, require bool'
                tmp += 'true' if value else 'false'
            elif data_type in ['i8', 'i16', 'i32', 'i64', 'i128']:
                assert isinstance(value, int), f'{field_name} type error, require {data_type}'
                tmp += f'{value}{data_type}'
            elif data_type in ['u8', 'u16', 'u32', 'u64', 'u128', 'group', 'field', 'scalar']:
                assert isinstance(value, int) and value >= 0, f'{field_name} type error, require unsigned int'
                tmp += f'{value}{data_type}'
            elif data_type == 'address':
                tmp += value
            else:
                # Struct or Record
                assert isinstance(value, LeoStruct) and value.__class__ == data_type, \
                    f"{field_name} type error, require {data_type.__name__}"
                tmp += str(value)
            items.append(tmp)
        return items

    def __str__(self):
        output = "{"
        items = self.fields_to_str()
        output += ','.join(items)
        output += "}"
        return output


class LeoRecord(LeoStruct):
    def __init__(self, seq=None, **kwargs):
        super().__init__(seq or {}, **kwargs)

    def __str__(self):
        output = "{\n"
        items = self.fields_to_str()
        items = [f'{item}.{self.fields[i][0]}' for i, item in enumerate(items)]
        items.append(f"_nonce: {self.get('_nonce', 0)}group.public")
        output += ',\n'.join(items)
        output += "\n}"
        return output
