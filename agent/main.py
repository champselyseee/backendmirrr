"""
Запуск: python main.py

Что делает:
  1. Читает 3 папки на Google Drive
  2. Находит пары файлов (Иванов-сочинение / Иванов-оценка)
  3. Анализирует каждую пару через Grok
  4. Пишет результат в Google Таблицу
  5. Генерирует итоговый промпт-аддон (лист "Итог-промпт")
"""

from datetime import date
from drive import get_pairs, download_docx_text
from analyzer import analyze_pair, generate_summary
from sheets import append_row, write_summary
from config import FOLDERS


def process_folder(task_type: str, folder_id: str, today: str) -> list[str]:
    if not folder_id:
        print(f"[{task_type}] папка не задана в .env, пропускаю")
        return []

    print(f"\n=== {task_type} ===")
    pairs = get_pairs(folder_id)
    if not pairs:
        print("  Пар не найдено")
        return []

    analyses = []
    for pair in pairs:
        print(f"  Обрабатываю: {pair['student']}...")
        essay_text = download_docx_text(pair["essay_id"])
        grade_text = download_docx_text(pair["grade_id"])
        result = analyze_pair(essay_text, grade_text, task_type)
        analysis = result["raw_analysis"]
        append_row(pair["student"], task_type, today, analysis)
        analyses.append(analysis)

    return analyses


def main():
    today = str(date.today())
    all_analyses_by_type = {}

    for task_type, folder_id in FOLDERS.items():
        analyses = process_folder(task_type, folder_id, today)
        if analyses:
            all_analyses_by_type[task_type] = analyses

    # Генерируем итог для каждого типа
    print("\n=== Генерирую итоговые промпт-аддоны ===")
    for task_type, analyses in all_analyses_by_type.items():
        print(f"  {task_type}...")
        summary = generate_summary(analyses, task_type)
        write_summary(task_type, summary, today)

    print("\nГотово! Открой Google Таблицу и проверь результат.")


if __name__ == "__main__":
    main()
