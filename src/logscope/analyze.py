"""
analyze.py
Модуль анализа данных
"""

from collections.abc import Iterator
from pathlib import Path

from logscope.parser import parse_file


def count_by_total_request(data: Iterator) -> int:
    """Принимает генератор LogEntry и возвращает общее количество записей"""
    total = 0
    for _ in data:
        total += 1
    return total


def count_by_status(): ...
def count_by_method(): ...
def count_by_endpoint(): ...
def average_response_time(): ...
def min_response_time(): ...
def max_response_time(): ...
def main():
    """Точка входа для запуска анализатора"""

    BASE_DIR = Path(__file__).resolve().parents[2]

    log_file = str(BASE_DIR / "fake_logs_2026-08-25_06-30-09.txt")

    print(count_by_total_request(parse_file(path=log_file)))


if __name__ == "__main__":
    main()
