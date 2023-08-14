import dataclasses
import pathlib
import typing

from utfuzz.user_interface.printer import my_print
from utfuzz.user_interface.utils import char_to_bool

T = typing.TypeVar('T')
U = typing.TypeVar('U')


class Status(typing.Generic[T]):
    pass


@dataclasses.dataclass
class Ok(Status):
    result: T


@dataclasses.dataclass
class Fail(Status):
    message: str


def my_read(message: str) -> str:
    return input(message)


def read_with_action(message: str, validate: typing.Callable[[str], Status[T]]) -> T:
    answer = my_read(message)
    check_answer = validate(answer)
    if isinstance(check_answer, Ok):
        return check_answer.result
    elif isinstance(check_answer, Fail):
        my_print('\n'.join([
            check_answer.message,
            'Please try again.',
        ]))
        return read_with_action(message, validate)


def check_with_default(check: typing.Callable[[str], Status[T]], default: T) -> typing.Callable[[str], Status[T]]:
    def inner(value: str) -> Status[T]:
        if value == '':
            return Ok(default)
        return check(value)
    return inner


def check_int(value: typing.Any) -> Status[int]:
    if isinstance(value, str) and value.isdigit():
        return Ok(int(value))
    return Fail(f'{value} is not a number')


def check_int_with_default(default: int) -> typing.Callable[[str], Status[int]]:
    return check_with_default(check_int, default)


def check_exists_path(value: typing.Any) -> Status[pathlib.Path]:
    if isinstance(value, str):
        path = pathlib.Path(value)
        if path.exists():
            return Ok(path)
    return Fail(f'{value} does not exists')


def check_exists_path_with_default(default: pathlib.Path) -> typing.Callable[[str], Status[pathlib.Path]]:
    return check_with_default(check_exists_path, default)


def check_valid_path(value: typing.Any) -> Status[pathlib.Path]:
    if isinstance(value, str):
        try:
            path = pathlib.Path(value)
        except Exception:
            return Fail(f'Invalid path {value}')
        return Ok(path)
    return Fail(f'Invalid path {value}')


def check_valid_path_with_default(default: pathlib.Path) -> typing.Callable[[str], Status[pathlib.Path]]:
    return check_with_default(check_valid_path, default)


def check_yes_no(value: str) -> Status[bool]:
    try:
        return Ok(char_to_bool(value))
    except KeyError:
        return Fail('Invalid answer')


def check_yes_no_with_default(default: bool):
    return check_with_default(check_yes_no, default)
