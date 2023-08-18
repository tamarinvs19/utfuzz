import json
import pathlib


def save_config(
    project_dir: pathlib.Path,
    java: str,
    sys_paths: list[str],
    analyze_targets: list[str],
    generate_only_error_suite: bool,
    timeout: int,
    output: str,
    requirements: str,
):
    with open(str(project_dir / "utfuzz_config.json"), "w") as conf:
        print(
            json.dumps(
                {
                    "java": java,
                    "sys_paths": sys_paths,
                    "analyze_targets": analyze_targets,
                    "generate_only_error_suite": generate_only_error_suite,
                    "timeout": timeout,
                    "output": output,
                    "project": str(project_dir),
                    "requirements": requirements,
                }
            ),
            file=conf,
        )


def load_config(path: pathlib.Path):
    with open(str(path), "r") as conf:
        data = "\n".join(conf.readlines())
        return json.loads(data)
