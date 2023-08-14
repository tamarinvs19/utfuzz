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
        debug_mode: bool,
):
    jar_command = f"{java} -jar {jar_path}"
    command = f" generate_python {file_under_test}" \
              f" -p {python_path} -o {output_dir} -s {','.join(sys_paths)} --timeout {timeout * 1000}"
    if skip_regression:
        command += ' --do-not-generate-regression-suite'
    if class_under_test is not None:
        command += f' -c {class_under_test}'
    if debug_mode:
        jar_command += ' --verbosity DEBUG'
    command = jar_command + command
    try:
        output = subprocess.check_output(command.split(), stderr=subprocess.STDOUT)
        my_print(output.decode())
    except Exception as e:
        my_print(str(e))
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
        debug_mode: bool,
):
    has_top_level = has_top_level_functions(file_under_test)
    all_classes = find_classes(file_under_test)
    if has_top_level or len(all_classes) > 0:
        my_print(f'\n   -------- Start fuzzing {file_under_test} --------   ')
        if has_top_level:
            run_utbot(java, jar_path, sys_paths, python_path, file_under_test, None, skip_regression, timeout, output_dir, debug_mode)

        for c in all_classes:
            run_utbot(java, jar_path, sys_paths, python_path, file_under_test, c, skip_regression, timeout, output_dir, debug_mode)
