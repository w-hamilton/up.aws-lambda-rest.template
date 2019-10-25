"""
Custom Exceptions
Exceptions should sublcass UpException
"""


class UpException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

    def __str__(self):
        return self.message
