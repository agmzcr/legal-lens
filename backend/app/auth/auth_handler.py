"""
Authentication Utility Functions

Provides password hashing and JWT access token creation/validation for secure user authentication.
"""

from jose import jwt, JWTError
from datetime import datetime, timedelta
from passlib.context import CryptContext

# Security settings
SECRET_KEY = "your-secret-key"                # Replace with secure env var in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Password hashing configuration using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hashes a plaintext password using bcrypt.

    Args:
        password (str): Plaintext password

    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies that a plaintext password matches the hashed password.

    Args:
        plain_password (str): User's input
        hashed_password (str): Stored hashed password

    Returns:
        bool: True if password matches, else False
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Creates a JWT access token with an expiration timestamp.

    Args:
        data (dict): Payload to encode into the token
        expires_delta (timedelta, optional): Duration until expiration

    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> str | None:
    """
    Decodes a JWT token and retrieves the subject identifier.

    Args:
        token (str): Encoded JWT token

    Returns:
        str | None: Subject identifier ('sub') or None if invalid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None