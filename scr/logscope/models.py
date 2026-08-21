"""
models.py
Модуль, описывающий структуру данных
"""

from dataclasses import dataclass
from datetime import date
from ipaddress import IPv4Address, IPv6Address


@dataclass
class LogEntry:
    """Класс структуры записи в логах"""

    timestamp: date
    ip: IPv4Address | IPv6Address
    method: tuple
    path: str
    status: str
    response_time: int
