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


@dataclass
class AnalysisReport:
    """Класс структуры данных анализатора"""

    total_request: int
    status_count: dict[int, int]
    method_count: dict[str, int]
    endpoint_count: dict[str, int]
    avg_response_time: float
    min_response_time: int
    max_response_time: int
