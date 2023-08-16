import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
print(BOT_TOKEN)

admins_id = [str(os.getenv("ADMIN_ID"))]
