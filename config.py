from dotenv import load_dotenv
import os

load_dotenv()

OUTLINE_API_URL = os.getenv("OUTLINE_API_URL")
OUTLINE_API_SECRET = os.getenv("OUTLINE_API_SECRET")
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
CSV_PATH = os.getenv("CSV_PATH", "users.csv")