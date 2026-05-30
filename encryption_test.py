from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
from cryptography.fernet import Fernet


# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# JWT Generation
SECRET_KEY = "your-super-secret-key"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Generate a key once and save it securely in your environment variables
ENCRYPTION_KEY = Fernet.generate_key()
# ENCRYPTION_KEY = b'your-32-byte-base64-encoded-key=' 
cipher = Fernet(ENCRYPTION_KEY)

def encrypt_token(token: str) -> str:
    """Encrypts a Plaid token to a string ready for DB storage."""
    return cipher.encrypt(token.encode()).decode()

def decrypt_token(encrypted_token: str) -> str:
    """Decrypts the DB string back into the raw Plaid token."""
    return cipher.decrypt(encrypted_token.encode()).decode()