class GenException(Exception):
    pass


class DestinationExistsException(GenException):
    pass


class CondaEnvironmentExistsException(GenException):
    pass


class MissingArgumentException(GenException):
    pass
