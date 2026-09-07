import time

from atop.monitor.metrics import collect_metrics


class MetricsSampler:

    def __init__(self):
        self.previous = None
        self.previous_time = None

    def collect(self) -> dict:
        current = collect_metrics()
        current_time = time.monotonic()

        result = {
            "current": current,
            "previous": self.previous,
            "elapsed": (
                current_time - self.previous_time
                if self.previous_time is not None
                else None
            ),
        }

        self.previous = current
        self.previous_time = current_time

        return result