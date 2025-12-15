import time
from typing import Optional, Dict, Type
from types import TracebackType
from .aggregator import LockFreeMetricsAggregator, MetricType

class PylightTimer:
    def __init__(self, name: str, tags: Optional[Dict[str, str]] = None):
        self.name = name
        self.tags = tags or {}
        self.start_time = 0.0
        self._aggregator = LockFreeMetricsAggregator()

    def __enter__(self) -> 'PylightTimer':
        self.start_time = time.time()
        return self

    def __exit__(self, 
                 exc_type: Optional[Type[BaseException]], 
                 exc_val: Optional[BaseException], 
                 exc_tb: Optional[TracebackType]) -> None:
        """
        Stop timer and record metric.
        """
        duration = time.time() - self.start_time
        # NOTE: In v0.2.0, we ignore tags to prioritize raw speed in sharding.
        # We pass only name, value, and type.
        self._aggregator.add_metric(
            self.name, 
            duration, 
            metric_type=MetricType.TIMER
        )

def measure_time(name: str, tags: Optional[Dict[str, str]] = None) -> PylightTimer:
    """
    Context manager to measure execution time.
    """
    return PylightTimer(name, tags)

def counter(name: str, value: int = 1, tags: Optional[Dict[str, str]] = None) -> None:
    """
    Increment a counter.
    """
    # NOTE: Tags are currently ignored in the high-performance engine
    LockFreeMetricsAggregator().add_metric(
        name, 
        float(value), 
        metric_type=MetricType.COUNTER
    )
