import os
from dotenv import load_dotenv

load_dotenv()

# xAI / Grok
XAI_API_KEY = os.getenv("XAI_API_KEY")
XAI_MODEL   = os.getenv("XAI_MODEL", "grok-3-mini")
XAI_BASE_URL = "https://api.x.ai/v1"

# Google — ID берёшь из URL таблицы и папок на Drive
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")   # ID Google Таблицы
DRIVE_FOLDER_EMAILS   = os.getenv("DRIVE_FOLDER_EMAILS")   # ID папки emails
DRIVE_FOLDER_SOCHIN   = os.getenv("DRIVE_FOLDER_SOCHIN")   # ID папки сочинения по русскому
DRIVE_FOLDER_ESSE     = os.getenv("DRIVE_FOLDER_ESSE")     # ID папки эссе

FOLDERS = {
    "email":     DRIVE_FOLDER_EMAILS,
    "сочинение": DRIVE_FOLDER_SOCHIN,
    "эссе":      DRIVE_FOLDER_ESSE,
}

# Путь к файлу service account (скачаешь из Google Cloud)
GOOGLE_SERVICE_ACCOUNT = os.getenv("GOOGLE_SERVICE_ACCOUNT", "service_account.json")
