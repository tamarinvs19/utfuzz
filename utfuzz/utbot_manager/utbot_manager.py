import importlib.machinery
import inspect
import pathlib
import subprocess
import typing

from utfuzz.user_interface.printer import my_print


def find_classes(file: str) -> typing.List[str]:
    path = pathlib.Path(file)
    module = importlib.machinery.SourceFileLoader(path.stem, file).load_module()
    class_members = inspect.getmembers(module, inspect.isclass)
    return [c[0] for c in class_members]


def has_top_level_functions(file: str) -> bool:
    path = pathlib.Path(file)
    module = importlib.machinery.SourceFileLoader(path.stem, file).load_module()
    return len(inspect.getmembers(module, inspect.isfunction)) > 0


def run_utbot(
        java: str,
        jar_path: str,
        sys_paths: typing.List[str],
        python_path: str,
        file_under_test: str,
        class_under_test: typing.Optional[str],
        skip_regression: bool,
        timeout: int,
        output_dir: str,
):
    command = f"{java} -jar {jar_path} generate_python {file_under_test}" \
              f" -p {python_path} -o {output_dir} -s {','.join(sys_paths)} --timeout {timeout * 1000}"
    if skip_regression:
        command += ' --do-not-generate-regression-suite'
    if class_under_test is not None:
        command += f' -c {class_under_test}'
    try:
        output = subprocess.check_output(command.split())
        my_print(output.decode())
    except Exception:
        pass


def generate_tests(
        java: str,
        jar_path: str,
        sys_paths: typing.List[str],
        python_path: str,
        file_under_test: str,
        skip_regression: bool,
        timeout: int,
        output_dir: str,
):
    if has_top_level_functions(file_under_test):
        my_print(f'Testing top-level function from {file_under_test}...')
        run_utbot(java, jar_path, sys_paths, python_path, file_under_test, None, skip_regression, timeout, output_dir)

    for c in find_classes(file_under_test):
        my_print(f'Testing class {c} form {file_under_test}...')
        run_utbot(java, jar_path, sys_paths, python_path, file_under_test, c, skip_regression, timeout, output_dir)


