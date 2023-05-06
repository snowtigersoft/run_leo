class LeoStruct(dict):
    fields = []

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        output = "{"
        items = []
        for field in self.fields:
            assert field[0] in self, f"Missing key {field[0]}"
            value = self[field[0]]
            data_type = field[1]
            tmp = f"{field[0]}: "
            if data_type == 'bool':
                assert isinstance(value, bool), f'{field[0]} type error, require bool'
                tmp += 'true' if value else 'false'
            elif data_type in ['i8', 'i16', 'i32', 'i64', 'i128']:
                assert isinstance(value, int), f'{field[0]} type error, require {data_type}'
                tmp += f'{value}{data_type}'
            elif data_type in ['u8', 'u16', 'u32', 'u64', 'u128', 'group', 'field', 'scalar']:
                assert isinstance(value, int) and value >= 0, f'{field[0]} type error, require unsigned int'
                tmp += f'{value}{data_type}'
            elif data_type == 'address':
                tmp += value
            else:
                # Struct or Record
                assert isinstance(value, LeoStruct) and value.__class__.__name__ == data_type, \
                    f"{field[0]} type error, require {data_type}"
                tmp += str(value)
            items.append(tmp)
        output += ','.join(items)
        output += "}"
        return output
