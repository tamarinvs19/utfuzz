import subprocess


def generate_tests(
        java: str,
        jar_path: str,
        sys_paths: list[str],
        python_path: str,
        file_under_test: str,
        skip_regression: bool,
        timeout: int,
        output_dir: str,
):
    command = f"{java} -jar {jar_path} generate_python {file_under_test}" \
              f" -p {python_path} -o {output_dir} -s {' '.join(sys_paths)} --timeout {timeout * 1000}"
    if skip_regression:
        command += ' --do-not-generate-regression-suite'
    try:
        output = subprocess.check_output(command.split())
        print(output.decode())
    except Exception:
        pass


