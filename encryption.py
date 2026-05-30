import os

from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
from cryptography.fernet import Fernet
from dotenv import load_dotenv

from config import JWT_ALGORITHM


# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# SECRET_KEY = "your-super-secret-key"
# ALGORITHM = "HS256"

# JWT Generation

def create_access_token(data: dict, expires_minutes: timedelta = 15):
    to_encode = data.copy()
    
    time_now = datetime.now()
    expire = time_now + (timedelta(minutes=expires_minutes))
    
    to_encode.update({"exp": expire}) # Setting expiry time
    to_encode.update({"iat": time_now})
    to_encode.update({"nbf": time_now})

    print(f"Processed token JSON: {to_encode}")

    return jwt.encode(to_encode, os.getenv("JWT_SECRET"), algorithm=JWT_ALGORITHM)


# Plaid Token processing

def encrypt_token(token: str, cipher: Fernet) -> str:
    """Encrypts a Plaid token to a string ready for DB storage."""
    return cipher.encrypt(token.encode()).decode()

def decrypt_token(encrypted_token: str, cipher: Fernet) -> str:
    """Decrypts the DB string back into the raw Plaid token."""
    return cipher.decrypt(encrypted_token.encode()).decode()


if __name__ == "__main__":
    load_dotenv()
    cipher = Fernet(os.getenv("FERNET_ENCRYPTION_KEY"))

    text = "testing plaid token encryption"
    encrypted_text = encrypt_token(text, cipher)

    print(f'Encrypted text: "{encrypted_text}"')
    print(f'\nDecrypted text: "{decrypt_token(encrypted_text, cipher)}"')


    payload = {
        # Standard metadata
        'sub': 'arnaav1', # Unique user ID
        'iss': 'broke-ai', # Issuer name
        
        'role': 'user' # role of user
    }
    print(f'\n\nRaw payload: \n{payload}')


    jwt_result = create_access_token(payload)

    print(f"\nJWT Token formed: \n{jwt_result}")