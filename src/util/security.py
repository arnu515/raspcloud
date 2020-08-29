import bcrypt
from cryptography.fernet import Fernet
import os

enc = Fernet(os.getenv("FERNET_KEY").encode())
pw_enc = Fernet(os.getenv("FERNET_PWKEY").encode())


# Passwords
def enc_pwd(pwd: str) -> str:
    return pw_enc.encrypt(bcrypt.hashpw(pwd.encode(), bcrypt.gensalt())).decode()


def check_pwd(pwd: str, h: str) -> bool:
    return bcrypt.checkpw(pwd.encode(), pw_enc.decrypt(h.encode()))


# Regular
def encrypt(text: str) -> str:
    return enc.encrypt(text.encode()).decode()


def decrypt(h: str) -> str:
    return enc.decrypt(h.encode()).decode()

