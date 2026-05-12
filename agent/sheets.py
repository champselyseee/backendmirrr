from googleapiclient.discovery import build
from drive import get_google_creds
from config import SPREADSHEET_ID

MAIN_SHEET = "Анализы"
SUMMARY_SHEET = "Итог-промпт"
HEADERS = ["Ученик", "Тип задания", "Дата", "Анализ эксперта"]


def get_sheets_service():
    return build("sheets", "v4", credentials=get_google_creds())


def ensure_sheet_exists(service, title):
    """Создаёт лист если его нет."""
    meta = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    existing = [s["properties"]["title"] for s in meta["sheets"]]
    if title not in existing:
        service.spreadsheets().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body={"requests": [{"addSheet": {"properties": {"title": title}}}]},
        ).execute()


def write_headers_if_empty(service):
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{MAIN_SHEET}!A1:Z1",
    ).execute()
    if not result.get("values"):
        service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{MAIN_SHEET}!A1",
            valueInputOption="RAW",
            body={"values": [HEADERS]},
        ).execute()


def append_row(student: str, task_type: str, date: str, analysis: str):
    """Добавляет строку с анализом одной работы."""
    service = get_sheets_service()
    ensure_sheet_exists(service, MAIN_SHEET)
    write_headers_if_empty(service)
    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{MAIN_SHEET}!A1",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body={"values": [[student, task_type, date, analysis]]},
    ).execute()
    print(f"  ✓ {student} ({task_type}) записан в таблицу")


def write_summary(task_type: str, summary_text: str, date: str):
    """Записывает итоговый промпт-аддон на лист Итог-промпт."""
    service = get_sheets_service()
    ensure_sheet_exists(service, SUMMARY_SHEET)
    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SUMMARY_SHEET}!A1",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body={"values": [[date, task_type, summary_text]]},
    ).execute()
    print(f"  ✓ Итог для '{task_type}' записан на лист '{SUMMARY_SHEET}'")
