def split_string(s, part_length=1900):
    return [s[i:i + part_length] for i in range(0, len(s), part_length)]
