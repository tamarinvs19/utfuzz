import platform
import subprocess
import sys
import typing

from utfuzz.exceptions.exceptions import JavaIsNotInstalled
from utfuzz.requirements_managers.abc_requirements_manager import AbstractJavaRequirementsManger


class WindowsJavaManager(AbstractJavaRequirementsManger):
    def check_platform(self) -> bool:
        return platform.system() == 'Windows'

    def install_java(self):
        print('You can see instruction here: '
              'https://docs.oracle.com/en/java/javase/17/install/installation-jdk-microsoft-windows-platforms.html'
              )
