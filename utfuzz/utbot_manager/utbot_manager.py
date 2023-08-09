import ast
import subprocess
import typing

from utfuzz.user_interface.printer import my_print


def find_classes(file: str) -> typing.List[str]:
    with open(file) as fh:
        root = ast.parse(fh.read(), file)
    classes = []
    for node in ast.iter_child_nodes(root):
        if isinstance(node, ast.ClassDef):
            classes.append(node.name)
    return classes


def has_top_level_functions(file: str) -> bool:
    with open(file) as fh:
        root = ast.parse(fh.read(), file)
    for node in ast.iter_child_nodes(root):
        if isinstance(node, ast.FunctionDef):
            return True
    return False


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
    my_print(command)
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
    my_print(f'\n----------- Start testing {file_under_test} -----------\n')
    if has_top_level_functions(file_under_test):
        my_print(f'Testing top-level function from {file_under_test}...')
        run_utbot(java, jar_path, sys_paths, python_path, file_under_test, None, skip_regression, timeout, output_dir)

    for c in find_classes(file_under_test):
        my_print(f'Testing class {c} form {file_under_test}...')
        run_utbot(java, jar_path, sys_paths, python_path, file_under_test, c, skip_regression, timeout, output_dir)
    my_print(f'\n----------- Finish testing {file_under_test} -----------\n')
