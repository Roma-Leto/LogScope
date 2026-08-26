"""
Модуль parser.py
Функции логики анализатора логов

parser_line(line: str) -> LogEntry - Разбирает строку. Кидает исключение при ошибке
def parser_file(path: str) -> Iterator[LogEntry] - Читает файл логов построчно. Логирует ошибки
"""

import re
import sys
from collections.abc import Iterator
from datetime import datetime
from ipaddress import ip_address
from pathlib import Path

from logscope.exceptions import InvalidLogLineError
from logscope.models import LogEntry


def _validate_method(raw: str) -> str:
    allowed = {"GET", "POST", "PUT", "DELETE"}
    if raw not in allowed:
        raise InvalidLogLineError(f"Неверный метод: {raw}")
    return raw


def _validate_path(raw: str) -> str:
    if not raw.startswith("/"):
        raise InvalidLogLineError(f"Путь должен начинаться с '/': {raw}")
    return raw


def parse_line(line: str) -> LogEntry:
    """Валидация строки"""

    line = line.strip()

    if not line:
        raise InvalidLogLineError("Пустая строка")

    log_pattern = r'^([\d\-T:]+)\s*-\s*"([^"]+)"\s*/\s*"([^"]+)"\s*,\s*"([^"]+)"\s*,\s*(\d+)\s*;\s*(\d+)$'

    match = re.match(log_pattern, line)

    if match is None:
        raise InvalidLogLineError(f"Неверный формат: {line}")

    result = match.groups()

    try:
        timestamp = datetime.fromisoformat(result[0])
        ip = ip_address(result[1])
        method = _validate_method(result[2])
        path = _validate_path(result[3])
        status = result[4]
        response_time = int(result[5])
    except ValueError as e:
        raise InvalidLogLineError(f"Ошибка валидации: {e}") from e

    return LogEntry(
        timestamp=timestamp,
        ip=ip,
        method=method,
        path=path,
        status=status,
        response_time=response_time,
    )


def parse_file(path: str | Path) -> Iterator[LogEntry]:
    """Разбор файла по строкам"""

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                entry = parse_line(line)
                yield entry

            except InvalidLogLineError as e:
                print(f"Ошибочная строка в файле. {e}", file=sys.stderr)


def main():
    """Точка входа для запуска парсера файлов логов."""

    BASE_DIR = Path(__file__).resolve().parents[2]

    log_file = str(BASE_DIR / "fake_logs_2026-08-26_14-55-41.txt")

    for _ in parse_file(path=log_file):  # изменить после написания анализатора
        pass


if __name__ == "__main__":
    main()
