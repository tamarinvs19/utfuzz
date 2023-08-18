import pathlib
import typing

from utfuzz.exceptions.exceptions import EnvironmentException


def get_py_files(directory: pathlib.Path) -> typing.List[pathlib.Path]:
    return [
        d.resolve().absolute()
        for d in directory.glob(r"**/*.py")
        if d.relative_to(directory).parts[0]
        not in {
            "venv",
            ".venv",
            "env",
            ".env",
            "tests",
            ".utfuzz",
            "utfuzz_tests",
        }
        and not d.name.startswith("test_")
        and not d.name.endswith("_test.py")
    ]


def find_config(directory: pathlib.Path) -> typing.Optional[pathlib.Path]:
    configs = list(directory.glob("utfuzz_config.json"))
    if len(configs) != 1:
        raise EnvironmentException
    return configs[0]
