
class AuthenticationError(Exception):
    """Custom exception to handle authentication failures."""
    def __init__(self, message, code):
        self.message = message
        self.code = code
        super().__init__(self.message)