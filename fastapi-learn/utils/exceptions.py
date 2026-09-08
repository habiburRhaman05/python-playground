class AppBaseException(Exception):
    """The parent exception for all custom app errors."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

class UserNotFoundError(AppBaseException):
    """Raised when a user cannot be found in the database."""
    pass

class DuplicateEmailError(AppBaseException):
    """Raised when an email registration conflicts."""
    pass
