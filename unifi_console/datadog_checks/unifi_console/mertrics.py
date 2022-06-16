from typing import List

from attr import dataclass


@dataclass
class Metric:
    type: str
    name: str
    value: float
    tags: List[str]


def Gauge(name: str, value: float, tags: List[str]) -> Metric:
    return Metric("gauge", name, value, tags)


def Count(name: str, value: float, tags: List[str]) -> Metric:
    return Metric("count", name, value, tags)


def Rate(name: str, value: float, tags: List[str]) -> Metric:
    return Metric("rate", name, value, tags)
