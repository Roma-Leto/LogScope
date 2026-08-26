"""
models.py
Модуль, описывающий структуру данных
"""

from dataclasses import dataclass
from datetime import datetime
from ipaddress import IPv4Address, IPv6Address


@dataclass
class LogEntry:
    """Класс структуры записи в логах"""

    timestamp: datetime
    ip: IPv4Address | IPv6Address
    method: str
    path: str
    status: int
    response_time: int
