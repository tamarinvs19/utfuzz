import json
import pathlib


def save_config(
        project_dir: pathlib.Path,
        java: str,
        sys_paths: list[str],
        files_under_test: list[str],
        skip_regression: bool,
        timeout: int,
        output: str,
        requirements: str,
):
    with open(str(project_dir / 'utfuzz_config.json'), 'w') as conf:
        print(json.dumps({
            'java': java,
            'sys_paths': sys_paths,
            'files_under_test': files_under_test,
            'skip_regression': skip_regression,
            'timeout': timeout,
            'output': output,
            'project': str(project_dir),
            'requirements': requirements,
        }), file=conf)


def load_config(path: pathlib.Path):
    with open(str(path), 'r') as conf:
        data = '\n'.join(conf.readlines())
        return json.loads(data)
