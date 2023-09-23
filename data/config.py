import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

admins_id = [int(os.getenv("ADMIN_ID"))]

db_user = str(os.getenv("db_user"))

db_database = str(os.getenv("db_database"))
