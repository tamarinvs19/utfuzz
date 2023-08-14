def bool_to_char(b: bool) -> str:
    return {0: 'n', 1: 'y'}[b]


def char_to_bool(c: str, default: bool = True) -> bool:
    return {'n': 0, 'y': 1, '': default}[c.lower()]
