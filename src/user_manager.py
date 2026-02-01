from src.db import Database
from src.config import ADMIN, SUPERADMIN

# Преобразуем строки в список целых чисел
admin_list = [int(x.strip()) for x in ADMIN.split(",") if x.strip()]
superadmin_id = int(SUPERADMIN)

def is_admin(user_id):
    return user_id in admin_list

def is_superadmin(user_id):
    return user_id == superadmin_id
