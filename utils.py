from passlib.context import CryptContext

# generate password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def cleanse(text: str) -> str:
    """
    Remove all whitespace from strings
    """
    return ''.join(text.split())

def verify(plain: str, hashed: str) -> bool:
    """
    Verify plaintext password against hashed from DB
    """
    return pwd_context.verify(plain, hashed)

def hash_pw(plain: str) -> str:
    """
    Hash password using passlib CryptContext
    """
    return pwd_context.hash(plain)