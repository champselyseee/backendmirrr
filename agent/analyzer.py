from openai import OpenAI
from config import XAI_API_KEY, XAI_MODEL, XAI_BASE_URL

client = OpenAI(api_key=XAI_API_KEY, base_url=XAI_BASE_URL)

ANALYSIS_PROMPT = """Тебе дана работа ученика и оценка эксперта.

Твоя задача — проанализировать ЛОГИКУ эксперта:
1. За что снижены баллы (конкретные критерии и примеры из текста)
2. Что эксперт отметил как хорошее
3. Какие закономерности в проверке (чему эксперт уделяет особое внимание)
4. Краткий вывод: что нужно делать / не делать, чтобы получить максимум

Отвечай структурированно, по пунктам. Будь конкретен — ссылайся на текст работы."""


def analyze_pair(essay_text: str, grade_text: str, task_type: str) -> dict:
    """
    Анализирует пару сочинение+оценка.
    Возвращает словарь с полями анализа.
    """
    user_message = f"""Тип задания: {task_type}

--- РАБОТА УЧЕНИКА ---
{essay_text}

--- ОЦЕНКА ЭКСПЕРТА ---
{grade_text}"""

    response = client.chat.completions.create(
        model=XAI_MODEL,
        messages=[
            {"role": "system", "content": ANALYSIS_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.3,
    )

    analysis = response.choices[0].message.content

    # Разбиваем на секции для удобной записи в таблицу
    return {
        "raw_analysis": analysis,
    }


SUMMARY_PROMPT = """Ты получишь таблицу анализов работ учеников, проверенных экспертом ЕГЭ.

На основе ВСЕХ анализов сформулируй итоговую добавку к системному промпту AI-проверщика:
- Топ-5 ошибок, которые эксперт чаще всего снижает
- Чему эксперт уделяет особое внимание
- Конкретные формулировки и требования этого эксперта
- Рекомендации для AI: на что обращать внимание при проверке

Пиши так, чтобы это можно было напрямую вставить в системный промпт. Чётко, по делу."""


def generate_summary(all_analyses: list[str], task_type: str) -> str:
    """Генерирует итоговый промпт-аддон по всем анализам одного типа."""
    combined = "\n\n---\n\n".join(all_analyses)
    response = client.chat.completions.create(
        model=XAI_MODEL,
        messages=[
            {"role": "system", "content": SUMMARY_PROMPT},
            {"role": "user", "content": f"Тип: {task_type}\n\n{combined}"},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content
