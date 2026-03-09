import secrets
from typing import Optional, Dict

from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt

from src.app.config.setting import get_setting

setting = get_setting()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_token(data: dict,expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    to_encode.update({"iat": datetime.utcnow()})  # Issued at time
    return jwt.encode(to_encode, setting.SECRET_KEY, algorithm=setting.ALGORITHM)


def create_access_token(user_id: int, email: str) -> str:
    return create_token(
        {
            "sub": str(user_id),
            "email": email,
            "type": "access",
            "jti": secrets.token_urlsafe(16)
        },
        timedelta(hours=setting.ACCESS_TOKEN_EXPIRE_HOURS)
    )

def create_refresh_token(user_id: int, email: str) -> str:
    return create_token(
        {
            "sub": str(user_id),
            "email": email,
            "type": "refresh",
            "family": secrets.token_urlsafe(16),  # Token family for rotation
            "jti": secrets.token_urlsafe(16)  # Unique token ID
        },
        timedelta(days=setting.REFRESH_TOKEN_EXPIRE_DAYS)
    )

def verify_token(token: str, token_type: str) -> Optional[Dict]:
    try:
        payload = jwt.decode(token, setting.SECRET_KEY, algorithms=[setting.ALGORITHM])

        # Verify token type
        if payload.get("type") != token_type:
            return None

        return payload
    except JWTError:
        return None