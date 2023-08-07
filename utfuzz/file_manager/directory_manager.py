import pathlib


def get_or_create(directory: pathlib.Path):
    if not directory.exists():
        directory.touch()
