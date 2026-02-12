"""Password hashing and verification utilities."""
import secrets

try:
    import bcrypt
    USE_DIRECT_BCRYPT = True
except ImportError:
    USE_DIRECT_BCRYPT = False
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        password: Plain text password

    Returns:
        Hashed password
    """
    if USE_DIRECT_BCRYPT:
        # Use bcrypt directly to avoid passlib compatibility issues
        password_bytes = password.encode('utf-8')
        # Bcrypt has a 72-byte limit
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')
    else:
        # Fallback to passlib
        return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash.

    Args:
        plain_password: Plain text password
        hashed_password: Hashed password

    Returns:
        True if password matches
    """
    if USE_DIRECT_BCRYPT:
        # Use bcrypt directly
        plain_bytes = plain_password.encode('utf-8')
        if len(plain_bytes) > 72:
            plain_bytes = plain_bytes[:72]
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(plain_bytes, hashed_bytes)
    else:
        # Fallback to passlib
        return pwd_context.verify(plain_password, hashed_password)


def generate_salt() -> str:
    """
    Generate a random salt string.

    Returns:
        Random salt string (hex)
    """
    return secrets.token_hex(16)
