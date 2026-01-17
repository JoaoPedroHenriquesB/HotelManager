class NotFoundError(Exception):
    """raise when a task is not found in database"""

    pass


class GuestNotFoundError(Exception):
    """raised when a user is not found in database"""
    pass


class RoomNotFoundError(Exception):
    """raised when a room not found"""
    pass


class StayNotFoundError(Exception):
    """raised when a room not found"""
    pass


class CouldNotValidateCredentialsError(Exception):
    """raised when could not validate credentials"""
    pass


class TokenDecodeError(Exception):
    """raised when a token is not valid"""
    pass


class TokenExpiredSignatureError(Exception):
    """raised when a token is expired"""
    pass


class NotAdminError(Exception):
    """raised when a user is not an admin"""
    pass


class PermissionDeniedError(Exception):
    """raised when an user is not allowed to perform an action"""

    pass


class DuplicateEntityError(Exception):
    """raised when attempting to create an entity that violates de uniqueness constraint"""

    def __init__(self, field: str | None = None, message: str | None = None) -> None:
        super().__init__(message or "duplicate entity")
        self.field = field
        self.message = message or "duplicate entity"


class InternalDomainError(Exception):
    """generic domain-level internal error"""
    pass


class RoomNotAvaliableError(Exception):
    """shows when a room is unavailable."""
    pass


class NotActiveStayError(Exception):
    """"""
    pass
