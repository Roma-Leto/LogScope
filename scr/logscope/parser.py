"""
Модуль parser.py
Функции логики анализатора логов

parser_line(line: str) -> LogEntry - Разбирает строку. Кидает исключение при ошибке
def parser_file(path: str) -> Iterator[LogEntry] - Читает файл логов построчно. Логирует ошибки
"""

import re
from collections.abc import Iterator
from dataclasses import asdict
from datetime import datetime, timezone
from ipaddress import ip_address
from pathlib import Path

from models import LogEntry


def save_reports(status: int, message: str) -> None:
    """Создание и сохранение отчёта"""

    if status:
        file_name = f"errors_report_{datetime.now(timezone.utc).strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    else:
        file_name = (
            f"report_{datetime.now(timezone.utc).strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        )

    with open(file_name, "w", encoding="utf_8") as f:
        f.write(message + "\n")


def parser_line(line: str) -> LogEntry:
    """Разбирает строку. Кидает ValueError при любой ошибке."""
    line = line.strip()

    # 1. Проверка на пустоту и базовую длину
    if not line or len(line.split()) < 5:
        raise ValueError(f"Недостаточно данных в строке или она пустая: '{line}'")

    r_log = r'^([\d\-T:]+)\s*:\s*"([^"]+)"\s*/\s*"([^"]+)"\s*,\s*"([^"]+)"\s*,\s*(\d+)\s*;\s*(\d+)$'
    match = re.match(r_log, line)

    # 2. Проверка регулярного выражения
    if match is None:
        raise ValueError(f"Строка не соответствует формату лога: '{line}'")

    # Линтер уверен, что match — не None, распаковка безопасна
    result = match.groups()

    return LogEntry(
        timestamp=datetime.fromisoformat(result[0]).date(),
        ip=ip_address(result[1]),
        method=[result[2]],
        path=result[3],
        status=result[4],
        response_time=int(result[5]),
    )


def parser_file(path: Path) -> Iterator[LogEntry]:
    """Читает файл и генерирует только валидные LogEntry, логируя ошибки."""
    with open(path, "r", encoding="utf-8") as f:
        for raw_line in f:
            try:
                entry = parser_line(raw_line)

                save_reports(
                    status=0,
                    message=f"Успешно обработан лог от {entry.timestamp} для IP {entry.ip}",
                )

                yield entry

            except ValueError as err:
                # Ловим ошибку из parser_line, пишем отчет и идем дальше
                save_reports(status=1, message=str(err))
                continue


if __name__ == "__main__":
    # Получаем абсолютный путь к папке, где лежит текущий файл parser.py
    BASE_DIR = Path(__file__).resolve().parents[2]

    # Строим точный путь к файлу логов относительно этой папки
    log_file_path = BASE_DIR / "docs" / "test_logs.txt"

    for entry in parser_file(path=log_file_path):
        if entry is None:
            continue
        log_entry = asdict(entry)
        print(f"Успешно: astuple{entry}")
