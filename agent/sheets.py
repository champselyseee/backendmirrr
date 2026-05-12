import csv
import os
from config import RESULTS_CSV, SUMMARY_TXT

HEADERS = ["Ученик", "Тип задания", "Дата", "Анализ эксперта"]


def append_row(student: str, task_type: str, date: str, analysis: str):
    os.makedirs(os.path.dirname(RESULTS_CSV), exist_ok=True)
    write_header = not os.path.exists(RESULTS_CSV)
    with open(RESULTS_CSV, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(HEADERS)
        writer.writerow([student, task_type, date, analysis])
    print(f"  ✓ {student} ({task_type}) записан в {RESULTS_CSV}")


def write_summary(task_type: str, summary_text: str, date: str):
    os.makedirs(os.path.dirname(SUMMARY_TXT), exist_ok=True)
    with open(SUMMARY_TXT, "a", encoding="utf-8") as f:
        f.write(f"{'='*60}\n")
        f.write(f"Тип: {task_type} | Дата: {date}\n")
        f.write(f"{'='*60}\n")
        f.write(summary_text + "\n\n")
    print(f"  ✓ Итог для '{task_type}' записан в {SUMMARY_TXT}")
