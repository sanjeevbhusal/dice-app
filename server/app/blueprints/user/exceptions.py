class EmailAlreadyExistException(Exception):
    """Raised when an email already exists in the database"""

    def __init__(self, message="Email not available"):
        self.message = message


class UnknownEmailException(Exception):
    """raised when an unidentified email is received"""

    def __init__(self, message="Email is not recognized"):
        self.message = message


class PasswordDoesnotMatchException(Exception):
    """raised when password does not match"""

    def __init__(self, message="Invalid password"):
        self.message = message


class NoAccessTokenException(Exception):
    """raised when user tries to view protected route without access token"""

    def __init__(self, message="No Token Received"):
        self.message = message


class NotAuthorizedException(Exception):
    """raised when user tries to access something they are not authorized """

    def __init__(self, message="You are not authorized to perform this operation"):
        self.message = message


class UnknownUserException(Exception):
    """raised when a user is not recognized"""

    def __init__(self, message="Unknown User"):
        self.message = message
