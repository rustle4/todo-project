import hashlib
import secrets
from datetime import UTC, datetime, timedelta
from typing import cast

from jose import JWTError, jwt
from pwdlib import PasswordHash

import config

pwd_context = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def generate_reset_token() -> str:
    return secrets.token_urlsafe(32)


def hash_reset_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(UTC) + (
        expires_delta or timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    secret_key = cast(str, config.SECRET_KEY)
    return jwt.encode(to_encode, secret_key, algorithm=config.ALGORITHM)


def decode_access_token(token: str):
    try:
        secret_key = cast(str, config.SECRET_KEY)
        payload = jwt.decode(token, secret_key, algorithms=[config.ALGORITHM])
        return payload
    except JWTError:
        return None
