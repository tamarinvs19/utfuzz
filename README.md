# utfuzz

`utfuzz` is a Python fuzzing engine. It supports fuzzing of Python code and code generation for error and regression suites. 

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
$ poetry build
$ python -m pip install dist/utfuzz-0.1.0.tar.gz
```

#### Java installation

`utfuzz` depends on Java 17 and newer. If you don't have an installed Java `utfuzz` will try to install (now this
function available only for Linux) or give you a link to installation instruction.

[Java installation instruction for Linux](https://docs.oracle.com/en/java/javase/17/install/installation-jdk-linux-platforms.html)

[Java installation instruction for Windows](https://docs.oracle.com/en/java/javase/17/install/installation-jdk-microsoft-windows-platforms.html)

[Java installation instruction for MacOS](https://docs.oracle.com/en/java/javase/17/install/installation-jdk-macos.html)

### Using `utfuzz`

There are 3 modes:
* dialog mode (default)
* config file mode (work if you add `--skip_dialog` argument and there are config file after previous executions)
* CLI arguments mode (work if you add `--skip_dialog` and `--skip_config_file`)

