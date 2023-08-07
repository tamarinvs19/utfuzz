"""UnitTestBot for Python"""
import pathlib
import sys

from utfuzz.config.config_manager import save_config, load_config
from utfuzz.exceptions.exceptions import EnvironmentException, JavaIncompatible, InvalidJavaVersion, \
    NotFoundRequirementsTxt, MultipleRequirementsTxt
from utfuzz.file_manager.file_finder import find_config, get_py_files
from utfuzz.parser import parse
from utfuzz.requirements_managers.linux_java_manager import LinuxJavaManager
from utfuzz.requirements_managers.python_requirements_manger import PythonRequirementsManager
from utfuzz.requirements_managers.windows_java_manager import WindowsJavaManager
from utfuzz.utbot_manager.utbot_manager import generate_tests


def main():
    args = parse()
    project_dir = pathlib.Path(args.project_dir).absolute()
    output_dir = pathlib.Path(args.output_dir).absolute()
    java = args.java
    timeout = args.timeout
    skip_regression = args.skip_regression_tests
    files_under_test = args.files_under_test
    sys_paths = args.sys_paths
    print('utfuzz started...')
    if args.skip_dialog:
        if not args.skip_config_file:
            try:
                config = find_config(project_dir)
            except EnvironmentException:
                print('Cannot find config file')
                return
            config_params = load_config(config)
            print(config_params)
            java = config_params['java']
            timeout = config_params['timeout']
            skip_regression = config_params['skip_regression']
            files_under_test = config_params['files_under_test']
            sys_paths = config_params['sys_paths']
            output_dir = pathlib.Path(config_params['output'])
            project_dir = pathlib.Path(config_params['project'])
    else:
        if java is None:
            print('Try to find java...')
            if LinuxJavaManager().check_platform():
                java_manager = LinuxJavaManager()
            else:
                java_manager = WindowsJavaManager()
            try:
                java = java_manager.check_java(java)
            except JavaIncompatible:
                print('utfuzz depends on Java, start installation...')
                java_manager.install_java()
                return
            except InvalidJavaVersion:
                print('Cannot parse Java version. You can set Java >= 17 by using argument --java')
                return
        print(f'Selected Java: {java}')

        print(f'Set timeout (s) per one class or top-level functions in one file (set empty to choose {timeout}s)')
        custom_timeout = input(f'Timeout (default = {timeout}s): ')
        timeout = int(custom_timeout) if custom_timeout != '' else timeout

        custom_project_dir = input(f'Set project directory to generate tests (default = {project_dir}): ')
        project_dir = pathlib.Path(custom_project_dir) if custom_project_dir != '' else project_dir

        custom_output_dir = input(f'Set directory for tests (default = {output_dir}): ')
        output_dir = pathlib.Path(custom_output_dir) if custom_output_dir != '' else output_dir

        custom_skip_regression = input(f'Do you want to generate regression suite? '
                                       f'Write True/False or 1/0 (default = {not skip_regression}): ')
        skip_regression = bool(custom_skip_regression) if custom_skip_regression != '' else skip_regression

    python_manager = PythonRequirementsManager(project_dir)
    if not python_manager.check_python():
        print('Please use Python 3.9 and newer')
        return
    print('Installing python dependencies...')
    python_manager.python_requirements_install()
    try:
        if args.requirements_file is None:
            python_manager.project_requirements_install()
        else:
            python_manager.project_requirements_install(
                pathlib.Path(args.requirements_file)
            )
    except NotFoundRequirementsTxt:
        print('Cannot found requirements.txt file.'
              ' If your project has python dependencies please write it to requirements.txt')
    except MultipleRequirementsTxt:
        print('Too many requirements.txt files found! Please use --requirements_file argument to set right')
        return

    if len(files_under_test) == 0:
        files_under_test = get_py_files(project_dir)
    else:
        files_under_test = [pathlib.Path(f).absolute() for f in files_under_test]
    print(f'Found {len(files_under_test)} python files to test')

    jar_path = str((pathlib.Path(__file__).parent / 'utbot-cli-python.jar').absolute())
    sys_paths.append(str(project_dir))
    sys_paths = list(set(sys_paths))
    save_config(project_dir, java, sys_paths, [str(f) for f in files_under_test], skip_regression, timeout,
                str(output_dir))
    for f in files_under_test:
        print(f'Start testing {f}')
        test_file_name = f'test_{"_".join(f.relative_to(project_dir).parts)}'
        generate_tests(java, jar_path, sys_paths, sys.executable, str(f), skip_regression, timeout,
                       str((output_dir / test_file_name).absolute()))


if __name__ == '__main__':
    main()
