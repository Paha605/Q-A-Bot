from src.db import Database
from src.config import ADMIN, SUPERADMIN


class UserService:
    def __init__(self, db: Database):
        self.db = db

def is_admin(user_id):
    return user_id == ADMIN

def is_superadmin(user_id):
    return user_id == SUPERADMIN

