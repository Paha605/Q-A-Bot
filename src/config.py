from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")
ADMIN = int(os.getenv("ADMIN"))
SUPERADMIN = int(os.getenv("SUPERADMIN"))