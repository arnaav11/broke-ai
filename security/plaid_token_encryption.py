from cryptography.fernet import Fernet


# Plaid Token processing

def encrypt_token(token: str, cipher: Fernet) -> str:
    """Encrypts a Plaid token to a string ready for DB storage."""
    return cipher.encrypt(token.encode()).decode()

def decrypt_token(encrypted_token: str, cipher: Fernet) -> str:
    """Decrypts the DB string back into the raw Plaid token."""
    return cipher.decrypt(encrypted_token.encode()).decode()


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()
    cipher = Fernet(os.getenv("FERNET_ENCRYPTION_KEY"))

    text = "testing plaid token encryption"
    encrypted_text = encrypt_token(text, cipher)

    print(f'Encrypted text: "{encrypted_text}"')
    print(f'\nDecrypted text: "{decrypt_token(encrypted_text, cipher)}"')