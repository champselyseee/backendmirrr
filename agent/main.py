"""
Запуск: python main.py

Структура папок:
  data/
    email/         ← файлы вида "Иванов-сочинение.docx" и "Иванов-оценка.docx"
    сочинение/
    эссе/
  results/         ← сюда пишутся analyses.csv и summary.txt (создаётся автоматически)
"""

from datetime import date
from drive import get_pairs, read_docx
from analyzer import analyze_pair, generate_summary
from sheets import append_row, write_summary
from config import FOLDERS


def process_folder(task_type: str, folder_path: str, today: str) -> list[str]:
    print(f"\n=== {task_type} ===")
    pairs = get_pairs(folder_path)
    if not pairs:
        print("  Пар не найдено (или папка пустая)")
        return []

    analyses = []
    for pair in pairs:
        print(f"  Обрабатываю: {pair['student']}...")
        essay_text = read_docx(pair["essay_path"])
        grade_text = read_docx(pair["grade_path"])
        result = analyze_pair(essay_text, grade_text, task_type)
        analysis = result["raw_analysis"]
        append_row(pair["student"], task_type, today, analysis)
        analyses.append(analysis)

    return analyses


def main():
    today = str(date.today())

    all_analyses_by_type = {}
    for task_type, folder_path in FOLDERS.items():
        analyses = process_folder(task_type, folder_path, today)
        if analyses:
            all_analyses_by_type[task_type] = analyses

    print("\n=== Генерирую итоговые промпт-аддоны ===")
    for task_type, analyses in all_analyses_by_type.items():
        print(f"  {task_type}...")
        summary = generate_summary(analyses, task_type)
        write_summary(task_type, summary, today)

    print("\nГотово!")
    print("  Анализы → results/analyses.csv")
    print("  Промпт-аддон → results/summary.txt")


if __name__ == "__main__":
    main()
