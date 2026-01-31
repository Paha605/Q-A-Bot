from src.db import Database
from src.config import ADMIN, SUPERADMIN


class UserService:
    def __init__(self, db: Database):
        self.db = db


admin_list = [int(ADMIN[:10]), int(ADMIN[10:19]), int(ADMIN[19:28])]
# test_admin_list = [int(ADMIN[:10])]

# admin_list = [int(ADMIN[10:19]), int(ADMIN[19:28])]

def is_admin(user_id):
    return user_id in admin_list

def is_superadmin(user_id):
    return user_id == SUPERADMIN







