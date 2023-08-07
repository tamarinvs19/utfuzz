import abc
import re
import subprocess
import typing

from utfuzz.exceptions.exceptions import JavaIncompatible, InvalidJavaVersion


class AbstractJavaRequirementsManger(abc.ABC):
    MINIMAL_JAVA_VERSION = 17

    @staticmethod
    @abc.abstractmethod
    def check_platform(self) -> bool:
        raise NotImplemented

    def find_java(self) -> str:
        return "java"

    def check_java(self, java_path: typing.Optional[str] = None):
        java_path = self.find_java() if java_path is None else java_path
        try:
            java_info = str(subprocess.check_output([java_path, "-version"], stderr=subprocess.STDOUT))
        except Exception as e:
            raise JavaIncompatible from e
        version_regex = re.compile(r'version "(.*)"')
        full_version = version_regex.findall(java_info)
        if len(full_version) != 1:
            raise InvalidJavaVersion
        version = int(full_version[0].split('.')[0])
        if version < self.MINIMAL_JAVA_VERSION:
            raise JavaIncompatible
        return java_path

    @abc.abstractmethod
    def install_java(self):
        return NotImplemented


class AbstractPythonRequirementsManger(abc.ABC):
    @abc.abstractmethod
    def check_python(self):
        return NotImplemented

    @abc.abstractmethod
    def python_requirements_install(self):
        return NotImplemented

    @abc.abstractmethod
    def project_requirements_install(self):
        return NotImplemented
