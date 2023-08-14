def bool_to_char(b: bool) -> str:
    return {False: 'n', True: 'y'}[b]


def char_to_bool(c: str, default: bool = True) -> bool:
    return {'n': False, 'y': True, '': default}[c.lower()]
