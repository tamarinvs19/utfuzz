# utfuzz

`utfuzz` is a Python fuzzing engine. It supports fuzzing of Python code and generation reproducing code for error and regression suites.

### Installation

`utfuzz` supports Python versions 3.8-3.11

You can use one of these ways:
1. Install from package archive:
    - download [utfuzz.tar.gz](https://github.com/tamarinvs19/utfuzz/raw/master/utfuzz_build/utfuzz.tar.gz?download=)
    - run
      `
      python -m pip install utfuzz.tar.gz
      `

2. Install from GitHub (if you have [`lfs`](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage)):
    ```shell
    python -m pip install git+https://github.com/tamarinvs19/utfuzz
    ```
3. Install from source code (if you have [`lfs`](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage))
    ```shell
    git clone https://github.com/tamarinvs19/utfuzz
    cd utfuzz
    python -m pip install -e ./
    ```

To run `utfuzz` you can use module `python -m utfuzz` or command `utfuzz` with active python environment.

#### Java installation

`utfuzz` depends on Java 17 and newer. If you don't have an installed Java `utfuzz` will try to install it or your can install Java by yourself using these instructions:

[Java installation instruction for Linux](https://docs.oracle.com/en/java/javase/17/install/installation-jdk-linux-platforms.html)

[Java installation instruction for Windows](https://docs.oracle.com/en/java/javase/17/install/installation-jdk-microsoft-windows-platforms.html)

[Java installation instruction for MacOS](https://docs.oracle.com/en/java/javase/17/install/installation-jdk-macos.html)

### Using `utfuzz`

To run:
```shell
python -m utfuzz
```
or
```shell
utfuzz
```

You can use `utfuzz` one of three modes:
* dialog mode (default)
* config file mode
* CLI arguments mode

After each test generation settings will be saved to file `utfuzz_config.json`

Priority:
* if `--use_config_file` default values will be from config file
* if not `--use_config_file` default values will be from cli-arguments
* then if not `--skip-dialog` new values will be from dialog

```
usage: utfuzz [-h] [--skip-dialog] [--use-config-file] [--generate-only-error-suite]
              [-j JAVA] [-t TIMEOUT] [-p PROJECT_DIR] [-o OUTPUT_DIR]
              [--sys-paths [SYS_PATHS ...]] [--analyze-targets [ANALYZE_TARGETS ...]]
              [--requirements-file REQUIREMENTS_FILE] [--debug]

utfuzz is a Python fuzzing engine. It supports fuzzing of Python code and
generation reproducing code for error and regression suites

options:
  -h, --help            show this help message and exit
  --skip-dialog         Do not ask parameters before execution
  --use-config-file     Use config file in current directory
  --generate-only-error-suite
                        Generate only error suite
  -j JAVA, --java JAVA  Path to Java executable file or JAVA_HOME
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout in seconds for test generation process per one
                        class or group of top-level functions from one file
  -p PROJECT_DIR, --project-dir PROJECT_DIR
                        Root directory with your code for testing (will be
                        used for imports and dependencies resolving)
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        Directory for generated tests collecting
  --sys-paths [SYS_PATHS ...]
                        Additional path to find imports(will be added to
                        `sys.path`, default = project directory) [optional]
  --analyze-targets [ANALYZE_TARGETS ...]
                        List of files or directories for testing, empty means
                        <<test all>> [optional]
  --requirements-file REQUIREMENTS_FILE
                        Path to requirements.txt [optional]
  --debug               Use debug mode
```

See also main website of UnitTestBot project: utbot.org

### UnitTestBot sources
You can change UnitTestBot source java file by changing `jar`-file `utfuzz/utbot-cli-python.jar` (Note: don't change the file name).

After replacing `jar`-file you should reinstall this module.


See also main [website](https://utbot.org) of UnitTestBot project and [GitHub repository](github.com/UnitTestBot/UTBotJava).

