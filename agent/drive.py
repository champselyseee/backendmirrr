import os
from docx import Document


def read_docx(path: str) -> str:
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


def get_pairs(folder_path: str) -> list[dict]:
    """
    Ищет пары файлов по шаблону "Имя-сочинение.docx" / "Имя-оценка.docx".
    Возвращает: [{"student": "Иванов", "essay_path": "...", "grade_path": "..."}, ...]
    """
    if not os.path.exists(folder_path):
        return []

    essays = {}
    grades = {}

    for filename in os.listdir(folder_path):
        if not filename.endswith(".docx"):
            continue
        name = filename[:-5]  # убираем .docx
        if "-" not in name:
            continue
        student, tag = name.rsplit("-", 1)
        student, tag = student.strip(), tag.strip().lower()
        full_path = os.path.join(folder_path, filename)
        if tag == "сочинение":
            essays[student] = full_path
        elif tag == "оценка":
            grades[student] = full_path

    pairs = []
    for student in essays:
        if student in grades:
            pairs.append({
                "student": student,
                "essay_path": essays[student],
                "grade_path": grades[student],
            })
    return pairs
