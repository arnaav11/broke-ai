import os

from datetime import datetime, timedelta
from jose import jwt

# JWT Generation

def create_access_token(data: dict, expires_minutes: int = 15, jwt_algorithm: str = 'HS256'):
    to_encode = data.copy()
    
    time_now = datetime.now()
    expire = time_now + (timedelta(minutes=expires_minutes))
    
    to_encode.update({"exp": expire}) # Setting expiry time
    to_encode.update({"iat": time_now})
    to_encode.update({"nbf": time_now})

    print(f"Processed token JSON: {to_encode}")

    return jwt.encode(to_encode, os.getenv("JWT_SECRET"), algorithm=jwt_algorithm)


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    payload = {
        # Standard metadata
        'sub': 'arnaav1', # Unique user ID
        'iss': 'broke-ai', # Issuer name
        
        'role': 'user' # role of user
    }
    print(f'\n\nRaw payload: \n{payload}')

    jwt_result = create_access_token(payload)
    print(f"\nJWT Token formed: \n{jwt_result}")