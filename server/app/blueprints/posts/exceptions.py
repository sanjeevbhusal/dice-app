class PostNotFoundException(Exception):
    """
    Raised when the post is not available in the database.
    :param message: Message to Display
    :type message: str
    """

    def __init__(self, message="Post does not Exist"):
        self.message = message
