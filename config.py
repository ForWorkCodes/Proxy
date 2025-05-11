from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
POSTGRES_DSN = os.getenv("POSTGRES_DSN")
API_BASE_URL = os.getenv("API_BASE_URL")