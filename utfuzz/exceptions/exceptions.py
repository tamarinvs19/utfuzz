class UtException(Exception):
    pass


class EnvironmentException(UtException):
    pass


class NotFoundRequirementsTxt(EnvironmentException):
    pass


class MultipleRequirementsTxt(EnvironmentException):
    pass


class JavaIncompatible(UtException):
    pass


class InvalidJavaVersion(UtException):
    pass


class InvalidPlatform(UtException):
    pass


class JavaIsNotInstalled(UtException):
    def __init__(self, command: str):
        self.command = command
