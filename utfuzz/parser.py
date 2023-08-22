import argparse


def parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="utfuzz",
        description="UtFuzzer is a Python fuzzing engine, generating ready-to-use unit tests "
        "for both error and regression suites.",
        # epilog="See also main website of UnitTestBot project: utbot.org",
        # epilog="See utbot.org/python for more information.",
    )
    parser.add_argument(
        "--skip-dialog",
        action="store_true",
        help="do not ask for options interactively",
    )
    parser.add_argument(
        "--use-config-file",
        action="store_true",
        help="use config file from current directory",
    )
    parser.add_argument(
        "--generate-only-error-suite",
        action="store_true",
        help="generate only error suite",
    )
    parser.add_argument(
        "-j", "--java",
        help="path to Java executable file or JAVA_HOME",
        default="java"
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=int,
        default=60,
        help="timeout in seconds for generating tests "
        "per class or group of top-level functions "
        "from one file",
    )
    parser.add_argument(
        "-p",
        "--project-dir",
        default=".",
        help="root directory with code under test "
        "(used for imports and dependency resolving)",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default="utfuzz_tests",
        help="directory for generated tests",
    )

    parser.add_argument(
        "--sys-paths",
        nargs="*",
        default=[],
        help="additional path to find imports "
        "(will be added to `sys.path`; default = project directory)",
    )
    parser.add_argument(
        "--analyze-targets",
        nargs="*",
        default=[],
        help="list of files or directories to test; empty value field means <<test all>>",
    )
    parser.add_argument(
        "--requirements-file",
        help="path to requirements.txt",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="use debug mode")
    return parser.parse_args()
