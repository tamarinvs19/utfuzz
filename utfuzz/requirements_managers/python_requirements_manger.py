import os
import pathlib
import subprocess
import sys
import typing

from utfuzz.exceptions.exceptions import NotFoundRequirementsTxt, MultipleRequirementsTxt
from utfuzz.requirements_managers.abc_requirements_manager import AbstractPythonRequirementsManger


class PythonRequirementsManager(AbstractPythonRequirementsManger):
    UTBOT_REQUIREMENTS = ('utbot_executor==1.4.32', 'utbot_mypy_runner==0.2.11')

    def __init__(self, project_dir: pathlib.Path):
        self.project_dir = project_dir

    def python_requirements_install(self):
        subprocess.check_call([sys.executable, "-m", "pip", "install", *self.UTBOT_REQUIREMENTS])

    def project_requirements_install(self, custom_requirements: typing.Optional[pathlib.Path] = None):
        if custom_requirements is None:
            requirements_files = list(self.project_dir.glob("requirements.txt"))
            if len(requirements_files) == 0:
                raise NotFoundRequirementsTxt
            if len(requirements_files) > 1:
                raise MultipleRequirementsTxt
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(requirements_files[0].absolute())])
        else:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", custom_requirements])

    def check_python(self) -> bool:
        version = sys.version_info
        return version.major == 3 and 8 <= version.minor <= 11
