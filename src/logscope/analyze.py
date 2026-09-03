"""
analyze.py
Модуль анализа данных
"""

import sys
from collections import Counter, defaultdict
from collections.abc import Iterator
from dataclasses import asdict

from logscope.models import AnalysisReport
from logscope.parser import parse_file


def count_by_total_request(data: Iterator) -> int:
    """Принимает генератор LogEntry и возвращает общее количество записей"""
    return sum(1 for _ in data)


def count_by_status(data: Iterator) -> dict[int, int]:
    """Подсчёт частоты статусов"""
    counter = Counter()
    for item in data:
        counter[item.status] += 1
    return counter


def count_by_method(data: Iterator) -> dict[str, int]:
    """Подсчёт частоты методов"""
    total = {}

    for item in data:
        item_dict = asdict(item)
        method = item_dict["method"]

        if method not in total:
            total[method] = 0

        total[method] += 1

    return total


def count_by_endpoint(data: Iterator) -> dict[str, int]:
    """Подсчёт частоты адресов"""
    total = {}
    for item in data:
        item_dict = asdict(item)
        endpoint = item_dict["path"]

        if endpoint not in total:
            total[endpoint] = 0
        total[endpoint] += 1

    return total


def average_response_time(data: Iterator) -> int:
    """Подсчёт среднего времени ответа сервера"""
    total_time = 0
    total_line = 0

    for item in data:
        item_dict = asdict(item)
        total_time += item_dict["response_time"]
        total_line += 1

    return int(total_time / total_line)


def min_response_time(data: Iterator) -> int:
    """Определение минимального времени ответа сервера"""
    min_time = float("inf")

    for item in data:
        item_dict = asdict(item)
        time = item_dict["response_time"]
        min_time = min(min_time, time)

    return int(min_time)


def max_response_time(data: Iterator) -> int:
    """Определение максимального времени ответа сервера"""
    max_time = 0

    for item in data:
        item_dict = asdict(item)
        time = item_dict["response_time"]
        max_time = max(max_time, time)

    return int(max_time)


def analyze(data: Iterator) -> AnalysisReport:
    """Функция полного анализа записей лога"""
    total_request = 0
    status_count = defaultdict(int)
    method_count = defaultdict(int)
    endpoint_count = defaultdict(int)
    avg_response_time = 0
    min_time = float("inf")
    max_time = 0
    total_time = 0

    for item in data:
        total_request += 1
        status_count[item.status] += 1
        method_count[item.method] += 1
        endpoint_count[item.path] += 1
        total_time += item.response_time

        max_time = max(max_time, item.response_time)
        min_time = min(min_time, item.response_time)

        avg_response_time = (total_time / total_request) if total_request > 0 else 0

    return AnalysisReport(
        total_request=total_request,
        status_count=status_count,
        method_count=dict(method_count),
        endpoint_count=endpoint_count,
        avg_response_time=avg_response_time,
        min_response_time=int(min_time),
        max_response_time=max_time,
    )


def analyze_main(file_name: str):
    """Точка входа для запуска анализатора"""

    # BASE_DIR = Path(__file__).resolve().parents[2]

    # log_file = str(BASE_DIR / "fake_logs_2026-08-25_06-30-09.txt")
    try:
        parsed_date = parse_file(path=file_name)
        report = analyze(parsed_date)

        print("\n" + "=" * 40)
        print("         РЕЗУЛЬТАТЫ АНАЛИЗА ЛОГОВ        ")
        print("=" * 40)
        print(f"Всего запросов:      {report.total_request}")
        print(f"Статусы ответов:     {report.status_count}")
        print(f"Методы:              {report.method_count}")
        print(f"Топ эндпоинтов:      {report.endpoint_count}")
        print(f"Минимальное время:   {report.min_response_time} мс")
        print(f"Максимальное время:  {report.max_response_time} мс")
        print(f"Среднее время:       {report.avg_response_time:.2f} мс")
        print("=" * 40)

    except FileNotFoundError:
        print(f"Ошибка: Файл '{file_name}' не найден.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    analyze_main(file_name="")
