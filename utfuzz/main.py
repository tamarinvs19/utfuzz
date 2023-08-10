"""UnitTestBot for Python"""
import pathlib
import sys

from utfuzz.user_interface.printer import my_print

from utfuzz.config.config_manager import save_config, load_config
from utfuzz.exceptions.exceptions import EnvironmentException, NotFoundRequirementsTxt, MultipleRequirementsTxt
from utfuzz.file_manager.file_finder import find_config, get_py_files
from utfuzz.parser import parse
from utfuzz.requirements_managers.java_requirements_manager import JavaRequirementsManager, JavaResult
from utfuzz.requirements_managers.python_requirements_manger import PythonRequirementsManager
from utfuzz.utbot_manager.utbot_manager import generate_tests


def main():
    args = parse()
    project_dir = pathlib.Path(args.project_dir).absolute()
    java = 'java'
    timeout = 60
    output_dir = project_dir / 'utbot_tests'
    skip_regression = False
    requirements_file = None
    sys_paths = []
    files_under_test = []

    # Firstly we use config file
    if args.use_config_file:
        try:
            config = find_config(project_dir)
        except EnvironmentException:
            my_print('Cannot find config file')
            return
        config_params = load_config(config)
        java = config_params['java']
        timeout = config_params['timeout']
        skip_regression = config_params['skip_regression']
        files_under_test = config_params['files_under_test']
        sys_paths = config_params['sys_paths']
        output_dir = pathlib.Path(config_params['output'])
        project_dir = pathlib.Path(config_params['project'])
        requirements_file = config_params['requirements']

    # Secondly we use cli-arguments
    if '--output_dir' in sys.argv or '-o' in sys.argv:
        output_dir = pathlib.Path(args.output_dir).absolute()
    if '--java' in sys.argv or '-j' in sys.argv:
        java = args.java
    if '--timeout' in sys.argv or '-t' in sys.argv:
        timeout = args.timeout
    if '--skip_regression_tests' in sys.argv or '-' in sys.argv:
        skip_regression = args.skip_regression_tests

    if '--files_under_test' in sys.argv:
        files_under_test = args.files_under_test
    if '--sys_paths' in sys.argv:
        sys_paths = args.sys_paths
    if '--requirements_file' in sys.argv:
        requirements_file = args.requirements_file

    my_print('utfuzz started...')
    java_manager = JavaRequirementsManager(project_dir)

    java_result, java = java_manager.check_base_java(java)
    if java_result != JavaResult.ValidJava:
        install = input('utfuzz depends on Java 17, install it? (Y/n) ')
        if install in {'Y', ''}:
            my_print('Start Java installation...')
            java = java_manager.install_java()
            my_print(f'Installed Java 17 to {java}. You can set it by --java argument at the next time.')

    if java is None:
        my_print('Some problems with Java! Your can set a correct path to Java 17 using argument --java. See '
                 'installation instruction in README.md')
        return

    my_print(f'Selected Java: {java}')

    # Thirdly we use dialog
    if not args.skip_dialog:
        my_print(f'Set timeout (s) per one class or top-level functions in one file (set empty to choose {timeout}s)')
        custom_timeout = input(f'Timeout (default = {timeout}s): ')
        timeout = int(custom_timeout) if custom_timeout != '' else timeout

        custom_project_dir = input(f'Set your project root directory (default = {project_dir}): ')
        project_dir = pathlib.Path(custom_project_dir) if custom_project_dir != '' else project_dir

        my_print(f'Specify files and directories to generate tests, print one file/directory to one line, empty line '
                 f'marks the end (default = all):')
        files_under_test = []
        while file_under_test := input(' * '):
            file_path = pathlib.Path(file_under_test)
            if file_path.is_file():
                files_under_test.append(file_path)
            elif file_path.is_dir():
                files_under_test += get_py_files(file_path)

        custom_output_dir = input(f'Set directory for tests (default = {output_dir}): ')
        output_dir = pathlib.Path(custom_output_dir) if custom_output_dir != '' else output_dir

        custom_skip_regression = input(f'Do you want to generate regression suite? '
                                       f'Write True/False or 1/0 (default = {not skip_regression}): ')
        skip_regression = bool(custom_skip_regression) if custom_skip_regression != '' else skip_regression

    python_manager = PythonRequirementsManager(project_dir)
    if not python_manager.check_python():
        my_print('Please use Python 3.9 and newer')
        return
    my_print('Installing python dependencies...')
    python_manager.python_requirements_install()
    try:
        if requirements_file is None:
            python_manager.project_requirements_install()
        else:
            python_manager.project_requirements_install(
                pathlib.Path(requirements_file)
            )
    except NotFoundRequirementsTxt:
        my_print('Cannot find requirements.txt file.'
                 ' If your project has python dependencies please write it to requirements.txt')
    except MultipleRequirementsTxt:
        my_print('Too many requirements.txt files found! Please use --requirements_file argument to set right')
        return

    if len(files_under_test) == 0:
        files_under_test = get_py_files(project_dir)
    else:
        files_under_test = [pathlib.Path(f).absolute() for f in files_under_test]
    my_print(f'Found {len(files_under_test)} python files to test')

    jar_path = pathlib.Path(__file__).parent / 'utbot-cli-python.jar'
    sys_paths.append(str(project_dir))
    sys_paths = list(set(sys_paths))

    # Save config before test generation process
    save_config(project_dir, java, sys_paths, [str(f) for f in files_under_test], skip_regression, timeout,
                str(output_dir), requirements_file)

    for f in files_under_test:
        test_file_name = f'test_{"_".join(f.relative_to(project_dir).parts)}'
        generate_tests(java, str(jar_path.absolute()), sys_paths, sys.executable, str(f), skip_regression, timeout,
                       str((output_dir / test_file_name).absolute()))
