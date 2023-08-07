import argparse


def parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="utfuzz",
        usage="utfuzz [options]",
        description="utfuzz is a Python fuzzing engine. It supports fuzzing of Python code and code generation for "
                    "error and regression suites",
        epilog="",
    )
    parser.add_argument('--skip_dialog', action='store_true')
    parser.add_argument('--skip_config_file', action='store_false')
    parser.add_argument('--skip_regression_tests', action='store_true')
    parser.add_argument('-j', '--java')
    parser.add_argument('-t', '--timeout', type=int, default=60)
    parser.add_argument('-p', '--project_dir', default='.')
    parser.add_argument('-o', '--output_dir', default='utbot_tests')

    parser.add_argument('--sys_paths', nargs='*', default=[])
    parser.add_argument('--files_under_test', nargs='*', type=argparse.FileType('r'), default=[])
    parser.add_argument('--requirements_file', type=argparse.FileType('r'))
    return parser.parse_args()
