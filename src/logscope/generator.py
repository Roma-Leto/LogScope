"""
generator.py

Генератор файла логов.
"""

import argparse
import ipaddress
import random
from datetime import datetime, timedelta, timezone
from typing import TextIO

http_methods = [
    "GET",  # Запрашивает данные с сервера
    "POST",  # Отправляет новые данные на сервер
    "PUT",  # Полностью заменяет существующие данные
    "PATCH",  # Частично изменяет существующие данные
    "DELETE",  # Удаляет данные на сервере
    # "HEAD",  # Запрашивает только заголовки (без тела ответа)
    # "OPTIONS",  # Возвращает поддерживаемые сервером методы
    # "CONNECT",  # Устанавливает туннель к серверу (для прокси)
    # "TRACE",  # Возвращает полученный запрос для тестов
]

http_status_codes = [
    200,  # OK — Успешный запрос
    201,  # Created — Ресурс успешно создан
    202,  # Accepted — Запрос принят на обработку
    204,  # No Content — Успешно, но сервер ничего не вернул
    301,  # Moved Permanently — Ресурс навсегда переехал
    302,  # Found — Ресурс временно переехал
    304,  # Not Modified — Данные не менялись (кэш)
    400,  # Bad Request — Неверный запрос (ошибка клиента)
    401,  # Unauthorized — Требуется авторизация
    403,  # Forbidden — Доступ запрещен (нет прав)
    404,  # Not Found — Ресурс не найден
    405,  # Method Not Allowed — Метод (например, POST) запрещен
    409,  # Conflict — Конфликт состояния ресурса
    429,  # Too Many Requests — Слишком много запросов (лимит)
    500,  # Internal Server Error — Внутренняя ошибка сервера
    502,  # Bad Gateway — Ошибка шлюза
    503,  # Service Unavailable — Сервер временно недоступен
    504,  # Gateway Timeout — Шлюз не дождался ответа
]

http_link = ["/users", "/orders", "/auth", "/login"]


parser = argparse.ArgumentParser(
    description="Генератор лог-файла", epilog="Пример: python generator.py --lines 1000"
)

parser.add_argument(
    "--lines", default=1000, type=int, help="Количество записей (по умолчанию - 1000)."
)

args = parser.parse_args()
num_lines = args.lines


def create_log_line(time_line) -> list:
    """Генерация записи в лог файле"""

    if random.randint(0, 1):
        int_for_ip = random.randint(0, 2**32 - 1)
        ip_line = ipaddress.IPv4Address(int_for_ip)
    else:
        network = ipaddress.ip_network("192.168.1.0/24")
        ip_line = random.choice(list(network.hosts()))

    api_line = "/api" + random.choices(http_link, weights=[20, 40, 30, 10])[0]

    return [
        time_line,
        ip_line,
        random.choice(http_methods),
        api_line,
        random.choice(http_status_codes),
        random.randint(10, 500),
    ]


def record_fake_log(file_object: TextIO, log_line: list) -> None:
    """Запись в файл"""
    dt, ip, method, url, status, size = log_line
    formatted_date = dt.strftime("%Y-%m-%dT%H:%M:%S")
    log_data = f'{formatted_date} - "{ip}"/"{method}", "{url}", {status}; {size}\n'
    file_object.write(log_data)


def main():
    """Управляющая функция"""
    start_time = datetime(2016, 5, 20, 12, 0)  # noqa: DTZ001
    file_create_time = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"fake_logs_{file_create_time}.txt"
    with open(file_name, "w", encoding="utf_8") as f:
        for _ in range(1, args.lines + 1):
            log_data_list = create_log_line(start_time)
            record_fake_log(f, log_data_list)
            start_time = start_time + timedelta(seconds=random.randint(1, 600))


if __name__ == "__main__":
    main()
