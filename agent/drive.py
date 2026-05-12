import io
import os
import tempfile
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
from docx import Document
from config import GOOGLE_SERVICE_ACCOUNT

SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/spreadsheets",
]


def get_google_creds():
    return service_account.Credentials.from_service_account_file(
        GOOGLE_SERVICE_ACCOUNT, scopes=SCOPES
    )


def get_drive_service():
    return build("drive", "v3", credentials=get_google_creds())


def list_files_in_folder(folder_id):
    """Возвращает список файлов в папке: [{name, id}, ...]"""
    service = get_drive_service()
    result = service.files().list(
        q=f"'{folder_id}' in parents and trashed=false",
        fields="files(id, name)",
    ).execute()
    return result.get("files", [])


def download_docx_text(file_id):
    """Скачивает .docx и возвращает его текст строкой"""
    service = get_drive_service()
    request = service.files().get_media(fileId=file_id)
    buf = io.BytesIO()
    downloader = MediaIoBaseDownload(buf, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    buf.seek(0)
    doc = Document(buf)
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


def get_pairs(folder_id):
    """
    Находит пары файлов по шаблону "Имя-сочинение" / "Имя-оценка".
    Возвращает список словарей:
      [{"student": "Иванов", "essay_id": "...", "grade_id": "..."}, ...]
    """
    files = list_files_in_folder(folder_id)

    essays = {}
    grades = {}
    for f in files:
        name = os.path.splitext(f["name"])[0]  # убираем .docx
        if "-" not in name:
            continue
        parts = name.rsplit("-", 1)
        student, tag = parts[0].strip(), parts[1].strip().lower()
        if tag == "сочинение":
            essays[student] = f["id"]
        elif tag == "оценка":
            grades[student] = f["id"]

    pairs = []
    for student in essays:
        if student in grades:
            pairs.append({
                "student": student,
                "essay_id": essays[student],
                "grade_id": grades[student],
            })
    return pairs
