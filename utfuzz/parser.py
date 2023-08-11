import argparse


def parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="utfuzz",
        usage="utfuzz [options]",
        description="utfuzz is a Python fuzzing engine. It supports fuzzing of Python code and generation reproducing "
                    "code for error and regression suites",
        epilog="See also main website of UnitTestBot project: utbot.org",
    )
    parser.add_argument('--skip_dialog', action='store_true', help='Do not ask parameters before execution')
    parser.add_argument('--use_config_file', action='store_true', help='Use config file in current directory')
    parser.add_argument('--generate_only_error_suite', action='store_true', help='Generate only error suite')
    parser.add_argument('-j', '--java', help='Path to Java executable file or JAVA_HOME', default='java')
    parser.add_argument('-t', '--timeout', type=int, default=60, help='Timeout in seconds for test generation process '
                                                                      'per one class or group of top-level functions '
                                                                      'from one file')
    parser.add_argument('-p', '--project_dir', default='.', help='Root directory with your code for testing (will be '
                                                                 'used for imports and dependencies resolving)')
    parser.add_argument('-o', '--output_dir', default='utbot_tests', help='Directory for generated tests collecting')

    parser.add_argument('--sys_paths', nargs='*', default=[], help='Additional path to find imports'
                                                                   '(will be added to `sys.path`, default = project '
                                                                   'directory) [optional]')
    parser.add_argument('--analyze_targets', nargs='*', type=argparse.FileType('r'), default=[],
                        help='List of files or directories for testing, empty means <<test all>> [optional]')
    parser.add_argument('--requirements_file', type=argparse.FileType('r'), help='Path to requirements.txt [optional]')
    parser.add_argument('--debug', action='store_true', help='Use debug mode')
    return parser.parse_args()
