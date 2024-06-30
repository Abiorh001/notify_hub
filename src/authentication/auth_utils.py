import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
import redis.asyncio as aioredis
from passlib.context import CryptContext

from src.core.config.env_data import Config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify the password password against the hashed password"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash the password using bcrypt algorithm"""
    return pwd_context.hash(password)


def create_access_token(
    payload: dict, expire: Optional[timedelta] = None, refresh: bool = False
) -> Optional[dict]:
    """
    Create an access token
    Args:
        payload: Data to encode in the token
        expire: Time to expire the token
        refresh: Refresh token
    Returns:
        Encoded JWT token
    """
    data_to_encode = payload.copy()
    if expire:
        expire = datetime.now(timezone.utc) + timedelta(minutes=expire)
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    data_to_encode.update({"jti": str(uuid.uuid4())})
    data_to_encode.update({"iat": datetime.now(timezone.utc)})
    data_to_encode.update({"exp": expire})
    data_to_encode.update({"refresh": refresh})
    encode_jwt = jwt.encode(
        data_to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM
    )
    return encode_jwt


def create_refresh_token(
    payload: dict, expire: Optional[timedelta] = None, refresh: bool = True
) -> Optional[dict]:
    """
    Create an refresh token
    Args:
        payload: Data to encode in the token
        expire: Time to expire the token
        refresh: Refresh token
    Returns:
        Encoded JWT token
    """
    data_to_encode = payload.copy()
    if expire:
        expire = datetime.now(timezone.utc) + timedelta(minutes=expire)
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=Config.REFRESH_TOKEN_EXPIRE_MINUTES
        )
    data_to_encode.update({"jti": str(uuid.uuid4())})
    data_to_encode.update({"iat": datetime.now(timezone.utc)})
    data_to_encode.update({"exp": expire})
    data_to_encode.update({"refresh": refresh})
    encode_jwt = jwt.encode(
        data_to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM
    )
    return encode_jwt


def refresh_access_token(refresh_token: str) -> Optional[str]:
    """
    Refresh the access token using a refresh token
    Args:
        refresh_token: Encoded JWT refresh token
    Returns:
        New access token if refresh is successful, None otherwise
    """
    decoded_refresh_token = decode_access_token(refresh_token)
    # Check if the refresh token is valid and refresh is True
    if decoded_refresh_token and decoded_refresh_token.get("refresh"):
        # Create a new access token with an extended expiration time
        new_access_token = create_access_token(payload=decoded_refresh_token)
        return new_access_token

    return None


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode the access token
    Args:
        token: Encoded JWT token
    Returns:
        Decoded JWT token
    """
    try:
        decode_jwt = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        return decode_jwt
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    except Exception:
        return None


async def redis_connection() -> aioredis.Redis:
    """
    Create a connection to the Redis server
    Returns:
        Redis connection object
    """
    pool = aioredis.ConnectionPool.from_url(Config.REDIS_URL + "?decode_responses=True")
    client = aioredis.Redis(connection_pool=pool)
    return client


async def blacklist_token_jti(jti: str) -> Optional[bool]:
    """
    Add the decoded token jti to the blacklist
    Args:
        jti: The decoded token jti
    """
    try:
        redis = await redis_connection()
        await redis.set(jti, "blacklisted", ex=timedelta(hours=12))
        await redis.close()
        return True
    except Exception:
        return None


async def is_token_blacklisted(jti: str) -> bool:
    """
    Check if the token jti is blacklisted
    Args:
        jti: The decoded token jti
    Returns:
        True if the token is blacklisted, False otherwise
    """
    redis = await redis_connection()
    is_blacklisted = await redis.get(jti)
    if is_blacklisted:
        await redis.close()
        return True
    return False
