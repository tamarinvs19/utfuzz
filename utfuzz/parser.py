import argparse


def parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="utfuzz",
        description="utfuzz is a Python fuzzing engine. It supports fuzzing of Python code and generation reproducing "
        "code for error and regression suites",
        epilog="See also main website of UnitTestBot project: utbot.org",
    )
    parser.add_argument(
        "--skip-dialog",
        action="store_true",
        help="Do not ask parameters before execution",
    )
    parser.add_argument(
        "--use-config-file",
        action="store_true",
        help="Use config file in current directory",
    )
    parser.add_argument(
        "--generate-only-error-suite",
        action="store_true",
        help="Generate only error suite",
    )
    parser.add_argument(
        "-j", "--java", help="Path to Java executable file or JAVA_HOME", default="java"
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=int,
        default=60,
        help="Timeout in seconds for test generation process "
        "per one class or group of top-level functions "
        "from one file",
    )
    parser.add_argument(
        "-p",
        "--project-dir",
        default=".",
        help="Root directory with your code for testing (will be "
        "used for imports and dependencies resolving)",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default="utfuzz_tests",
        help="Directory for generated tests collecting",
    )

    parser.add_argument(
        "--sys-paths",
        nargs="*",
        default=[],
        help="Additional path to find imports"
        "(will be added to `sys.path`, default = project directory) [optional]",
    )
    parser.add_argument(
        "--analyze-targets",
        nargs="*",
        default=[],
        help="List of files or directories for testing, empty means <<test all>> [optional]",
    )
    parser.add_argument(
        "--requirements-file",
        help="Path to requirements.txt [optional]",
    )
    parser.add_argument("--debug", action="store_true", help="Use debug mode")
    return parser.parse_args()
