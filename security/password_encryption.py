import bcrypt


def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed.encode("utf-8"),
    )


if __name__ == "__main__":
    text = "testing pasword info"

    print(f"Unencrypted Password: '{text}'")

    hashed_text = hash_password(text)
    print(f'Encrypted Password: "{hashed_text}"')

    print(f'Testing wrong password "hello": {verify_password("hello", hashed_text)}')
    print(f'Testing correct password "{text}": {verify_password(text, hashed_text)}')