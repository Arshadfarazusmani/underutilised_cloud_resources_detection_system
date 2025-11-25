# auth.py
# 

# auth.py
import bcrypt
from db import insert_user, find_user_by_email, find_user_public_by_email

def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed)

def register_user(username: str, email: str, password: str):
    # check existing
    existing = find_user_by_email(email)
    if existing:
        return False, "Email already exists"
    hashed = hash_password(password)
    doc = {"username": username, "email": email, "password": hashed}
    uid = insert_user(doc)
    user_public = find_user_public_by_email(email)
    return True, user_public

def login_user(email: str, password: str):
    user = find_user_by_email(email)
    if not user:
        return False, "User not found"
    if verify_password(password, user["password"]):
        user_public = find_user_public_by_email(email)
        return True, user_public
    return False, "Incorrect password"
