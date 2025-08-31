# app/services/jwt.py

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
from app.config import settings
from app.schemas.token import TokenData

logger = logging.getLogger(__name__)

class JWTService:
    def __init__(
        self,
        secret_key: str,
        algorithm: str,
        expire_minutes: int,
    ):
        self._secret = secret_key
        self._alg = algorithm
        self._exp = expire_minutes

    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """
        Creates a JWT access token with the specified data and an expiration time.
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=self._exp))
        to_encode.update({"exp": expire, "iat": datetime.utcnow()})
        return jwt.encode(to_encode, self._secret, algorithm=self._alg)

    def verify_access_token(self, token: str) -> Dict[str, Any]:
        """
        Verifies a JWT access token and returns its decoded payload.
        Raises ExpiredSignatureError or JWTError if the token is invalid.
        """
        return jwt.decode(token, self._secret, algorithms=[self._alg])

jwt_service = JWTService(
    secret_key=settings.JWT_SECRET_KEY,
    algorithm=settings.JWT_ALGORITHM,
    expire_minutes=settings.JWT_ACCESS_TOKEN_EXPIRES_MINUTES,
)