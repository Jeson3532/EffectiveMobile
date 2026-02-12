import secrets
import string

dictionary = string.ascii_letters + string.digits


def generate_jti(length: int = 8):
    return ''.join(secrets.choice(dictionary) for _ in range(length))
