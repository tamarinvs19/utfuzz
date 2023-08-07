import pathlib
import typing

from utfuzz.exceptions.exceptions import EnvironmentException


def get_py_files(directory: pathlib.Path) -> typing.List[pathlib.Path]:
    # return list(directory.glob(r"^(?!venv|\.venv|env|\.env|build).*/*.py"))
    return [d.absolute() for d in directory.glob(r"**/*.py") if d.parts[0] not in {'venv', '.venv', 'env', '.env'}]


def find_config(directory: pathlib.Path) -> typing.Optional[pathlib.Path]:
    configs = list(directory.glob("utfuzz_config.json"))
    if len(configs) != 1:
        raise EnvironmentException
    return configs[0]
