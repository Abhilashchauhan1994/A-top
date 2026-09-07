import time

from atop.collectors.cpu import collect_cpu_metrics


class CPUHistory:

    def __init__(self, max_points: int = 60):
        self.max_points = max_points
        self.history = []
        self.start_time = time.monotonic()

    def collect(self) -> dict:
        cpu = collect_cpu_metrics()

        elapsed = int(time.monotonic() - self.start_time)

        point = {
            "time": elapsed,
            "cpu": cpu["usage"],
        }

        self.history.append(point)

        if len(self.history) > self.max_points:
            self.history.pop(0)

        return point

    def get_history(self) -> list[dict]:
        return self.history