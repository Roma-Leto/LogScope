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

    def __repr__(self):
        return (
            f"AnalysisReport(\n"
            f"  total_request={self.total_request},\n"
            f"  status_count={dict(self.status_count)},\n"
            f"  method_count={self.method_count},\n"
            f"  endpoint_count={dict(self.endpoint_count)},\n"
            f"  avg_response_time={self.avg_response_time:.2f},\n"
            f"  min_response_time={self.min_response_time},\n"
            f"  max_response_time={self.max_response_time}\n"
            f")"
        )
