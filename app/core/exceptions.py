from fastapi import HTTPException, status


class BaseAPIException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ValidationError(BaseAPIException):
    def __init__(self, message):
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


class NotFoundError(BaseAPIException):
    def __init__(self, message):
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class AuthenticationError(BaseAPIException):
    def __init__(self, message):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED)


class AuthorizationError(BaseAPIException):
    def __init__(self, message: str):
        super().__init__(message, status.HTTP_403_FORBIDDEN)


class DatabaseError(BaseAPIException):
    def __init__(self, message: str):
        super().__init__(message, status.HTTP_500_INTERNAL_SERVER_ERROR)
