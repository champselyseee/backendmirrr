import os
from dotenv import load_dotenv

load_dotenv()

XAI_API_KEY  = os.getenv("XAI_API_KEY")
XAI_MODEL    = os.getenv("XAI_MODEL", "grok-3-mini")
XAI_BASE_URL = "https://api.x.ai/v1"

# Папки с файлами (лежат рядом с main.py)
FOLDERS = {
    "email":     "data/email",
    "сочинение": "data/сочинение",
    "эссе":      "data/эссе",
}

# Куда пишем результаты
RESULTS_CSV     = "results/analyses.csv"
SUMMARY_TXT     = "results/summary.txt"
