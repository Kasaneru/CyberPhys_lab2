import csv
import requests
from pathlib import Path

OLLAMA_URL = "http://localhost:11434/api/generate"
REPORT_PATH = "report.csv"

QUERIES = [
    "Which is heavier: a kilogram of fluff or a kilogram of steel?",
    "Tell me about ansambles in machine learning.",
    "What is the formula for the circumference?",
    "Which country is the largest in terms of area?",
    "Which country has the largest population?",
    "Who is the Joker from Batman?",
    "Tell me about Poincare conjecture.",
    "Tell us about the main political parties in the USA.",
    "What is the meaning of life?",
    "In what years did the Second World War take place?"
]

def ask_ollama(query: str) -> str:
    '''
    Отправляет запрос к ollama

    :query: запрос к ollama
    :returns: ответ LLM на запрос
    '''
    payload = {
        "model": "qwen2.5:0.5b",
        "prompt": query,
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def run_inference(queries: list[str]) -> list[dict[str, str]]:
    """
    Запуск инференса для каждого запроса

    :queries: список запросов для LLM
    :returns: список словарей с ключами query и answer
    """
    answers = []
    for i, query in enumerate(queries, 1):
        print(f"Запрос №{i}/{len(queries)}...")
        answer = ask_ollama(query)
        answers.append({"query": query, "answer": answer})
        print(f"Получен ответ!")
    return answers

def save_report(answers: list[dict[str, str]], path: Path) -> None:
    """
    Сохраняет отчет инференса в CSV
    Переносы строк в тексте экранируются для корректной записи

    :answers: список словарей с ключами query и answer
    :path: путь к CSV-файлу
    """  
    path.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    for answer in answers:
        rows.append(
            {
                "query": answer["query"].replace("\r\n", "\n").replace("\r", "\n").replace("\n", "\\n"),
                "answer": answer["answer"].replace("\r\n", "\n").replace("\r", "\n").replace("\n", "\\n"),
            }
        )

    with path.open("w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["query", "answer"])
        writer.writeheader()
        writer.writerows(rows)

if __name__ == '__main__':
    answers = run_inference(QUERIES)
    save_report(answers, Path(REPORT_PATH))
    print(f"Отчет сохранен: {REPORT_PATH}")
