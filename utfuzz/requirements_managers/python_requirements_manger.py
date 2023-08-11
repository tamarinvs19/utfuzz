import logging
import pathlib
import subprocess
import sys
import typing

from utfuzz.exceptions.exceptions import NotFoundRequirementsTxt, MultipleRequirementsTxt


class PythonRequirementsManager(object):
    UTBOT_REQUIREMENTS = ('utbot_executor==1.4.37', 'utbot_mypy_runner==0.2.11')

    def __init__(self, project_dir: pathlib.Path):
        self.project_dir = project_dir

    def python_requirements_install(self):
        out = subprocess.check_output([sys.executable, "-m", "pip", "install", *self.UTBOT_REQUIREMENTS],
                                      stderr=subprocess.STDOUT)
        logging.info(out)

    def project_requirements_install(self, custom_requirements: typing.Optional[pathlib.Path] = None):
        if custom_requirements is None:
            requirements_files = list(self.project_dir.glob("requirements.txt"))
            if len(requirements_files) == 0:
                raise NotFoundRequirementsTxt
            if len(requirements_files) > 1:
                raise MultipleRequirementsTxt
            out = subprocess.check_output(
                [sys.executable, "-m", "pip", "install", "-r", str(requirements_files[0].absolute())],
                stderr=subprocess.STDOUT)
            logging.info(out)
        else:
            out = subprocess.check_output(
                [sys.executable, "-m", "pip", "install", "-r", custom_requirements],
                stderr=subprocess.STDOUT)
        logging.info(out)

    def check_python(self) -> bool:
        version = sys.version_info
        return version.major == 3 and 8 <= version.minor <= 11
