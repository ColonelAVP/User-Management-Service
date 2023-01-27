from passlib.context import CryptContext

# Passlib Config
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    """
    get_hashed_password() takes password as param and return hashstring
    params -> Password
    return -> str
    """
    pass_len = len(password)
    if pass_len == 4:
        return password_context.hash(password)
    else:
        return False


def verify_password(password: str, hashed_pass: str) -> bool:
    """
    verify_password() verifies the password
    params -> password, hashed_pass
    return -> bool
    """
    return password_context.verify(password, hashed_pass)
