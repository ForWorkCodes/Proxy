from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL")
SERVER_BASE_URL = os.getenv("SERVER_BASE_URL")
INTERNAL_API_TOKEN = os.getenv("INTERNAL_API_TOKEN")