import os
import pathlib
import re
import subprocess
import typing
import jdk
import enum


class JavaResult(enum.Enum):
    InvalidVersion = 1
    IncorrectVersion = 2
    NotFoundJava = 3
    ValidJava = 4


class JavaRequirementsManager(object):
    JAVA_VERSION = '17'
    TARGET_DIR = '.utfuzz'

    def __init__(self, project_dir: pathlib.Path):
        self.project_dir = project_dir
        self.target_dir = self.project_dir / self.TARGET_DIR

    def find_java(self) -> str:
        if self.target_dir.exists():
            target_dir_children = next(os.walk(self.target_dir))[1]
            if any(x.startswith('jdk') for x in target_dir_children):
                return str((self.target_dir / [x for x in target_dir_children if x.startswith('jdk')][0] / 'bin' / 'java').absolute())
        return "java"

    def check_java(self, java_path: str) -> JavaResult:
        try:
            path = pathlib.Path(java_path)
            if path.is_dir():
                java_path = str(path / 'bin' / 'java')
            java_info = subprocess.check_output([java_path, "-version"], stderr=subprocess.STDOUT).decode()
        except Exception:
            return JavaResult.NotFoundJava
        version_regex = re.compile(r'version "(.*)"')
        full_version = version_regex.findall(java_info)
        if len(full_version) != 1:
            return JavaResult.InvalidVersion
        version = full_version[0].split('.')[0]
        if version != self.JAVA_VERSION:
            return JavaResult.IncorrectVersion
        return JavaResult.ValidJava

    def check_base_java(self, java_path: typing.Optional[str] = None) -> typing.Tuple[JavaResult, typing.Optional[str]]:
        if java_path is not None:
            path = pathlib.Path(java_path)
            if path.is_dir():
                java_path = str(path / 'bin' / 'java')
            if self.check_java(java_path) == JavaResult.ValidJava:
                return JavaResult.ValidJava, java_path

        java_path = self.find_java()
        check_java = self.check_java(java_path)
        if check_java == JavaResult.ValidJava:
            return check_java, java_path
        else:
            return check_java, None

    def install_java(self) -> str:
        return str((pathlib.Path(jdk.install(self.JAVA_VERSION, path=str(self.target_dir.absolute()))) / 'bin' / 'java')
                   .resolve().absolute())
