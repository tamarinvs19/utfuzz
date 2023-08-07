# utfuzz

`utfuzz` is a Python fuzzing engine. It supports fuzzing of Python code and generation reproducing code for error and regression suites. 

### Installation

`utfuzz` supports Python versions 3.8-3.11

You can install it as a python module:
```shell
$ python -m pip install utfuzz
```

Or from source code using `poetry`:
```shell
$ git clone https://github.com/tamarinvs19/utfuzz
$ cd utfuzz
$ python -m pip install build
```

#### Java installation

`utfuzz` depends on Java 17 and newer. If you don't have an installed Java `utfuzz` will try to install (now this
function available only for Linux) or give you a link to installation instruction.

[Java installation instruction for Linux](https://docs.oracle.com/en/java/javase/17/install/installation-jdk-linux-platforms.html)

[Java installation instruction for Windows](https://docs.oracle.com/en/java/javase/17/install/installation-jdk-microsoft-windows-platforms.html)

[Java installation instruction for MacOS](https://docs.oracle.com/en/java/javase/17/install/installation-jdk-macos.html)

### Using `utfuzz`

You can use `utfuzz` one of three modes:
* dialog mode (default)
* config file mode (work if you add `--skip_dialog` argument and there are config file after previous executions)
* CLI arguments mode (work if you add `--skip_dialog` and `--skip_config_file`)

```
options:
  -h, --help            show this help message and exit
  --skip_dialog         Do not ask parameters before execution
  --skip_config_file    Do not use config file in current directory
  --skip_regression_tests
                        Do not generate regression suite
  -j JAVA, --java JAVA  Path to Java
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout for test generation process per one class or group of top-level functions from one file
  -p PROJECT_DIR, --project_dir PROJECT_DIR
                        Directory with your code for testing
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        Directory for generated tests collecting
  --sys_paths [SYS_PATHS ...]
                        Additional path to find imports(will be added to `sys.path`, default = project directory) [optional]
  --files_under_test [FILES_UNDER_TEST ...]
                        List of files for testing, empty means <<test all>> [optional]
  --requirements_file REQUIREMENTS_FILE
                        Path to requirements.txt [optional]
```

See also main [website](utbot.org) of UnitTestBot project and [GitHub repository](github.com/UnitTestBot/UTBotJava).

