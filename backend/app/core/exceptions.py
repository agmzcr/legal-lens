class AuthError(Exception):
    """Authentication module exceptions."""
    pass

class DatabaseError(Exception):
    """Database operation error."""
    pass

class UserNotFoundError(Exception):
    """User not found in the database."""
    pass

class DocumentNotFoundError(Exception):
    """Document not found in the database."""
    pass

class TokenError(Exception):
    """Token related errors."""
    pass

class UnsupportedFileTypeError(Exception):
    """Unsupported file type."""
    pass

class InvalidCredentialsError(AuthError):
    """Invalid username or password."""
    pass

class RefreshTokenExpiredError(AuthError):
    """Refresh token is invalid or has expired."""
    pass

class UserAlreadyExistsError(AuthError):
    """User already exists."""
    pass

class InvalidTokenError(AuthError):
    """Invalid token or unable to verify."""
    pass

class SQLAlchemyError(Exception):
    """Exception for SQLAlchemy errors."""
    pass

class PDFParseError(Exception):
    """Exception for PDF parsing errors."""
    pass

class AIEngineError(Exception):
    """Exception for AI engine errors."""
    pass