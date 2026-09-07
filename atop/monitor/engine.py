from collections.abc import Callable
from typing import Any

from atop.monitor.sampler import MetricsSampler


MetricsSnapshot = dict[str, Any]
MetricsSubscriber = Callable[[MetricsSnapshot], None]


class MetricsEngine:
    """
    Central metrics runtime for A-Top.

    Responsibilities:
        - Manage metrics collection lifecycle
        - Collect snapshots through MetricsSampler
        - Publish snapshots to subscribers
        - Keep UI independent from collectors
        - Provide a single metrics pipeline for all widgets
    """

    def __init__(self, interval: float = 1.0):
        if interval <= 0:
            raise ValueError("interval must be greater than 0")

        self.interval = interval
        self.sampler = MetricsSampler()

        self._subscribers: list[MetricsSubscriber] = []
        self._running = False

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    @property
    def running(self) -> bool:
        return self._running

    def start(self) -> None:
        """Mark the metrics engine as running."""
        self._running = True

    def stop(self) -> None:
        """Stop the metrics engine."""
        self._running = False

    # ---------------------------------------------------------
    # Subscription
    # ---------------------------------------------------------

    def subscribe(self, subscriber: MetricsSubscriber) -> None:
        """
        Register a subscriber to receive metrics snapshots.

        Duplicate subscribers are ignored.
        """

        if subscriber not in self._subscribers:
            self._subscribers.append(subscriber)

    def unsubscribe(self, subscriber: MetricsSubscriber) -> None:
        """Remove a previously registered subscriber."""

        if subscriber in self._subscribers:
            self._subscribers.remove(subscriber)

    # ---------------------------------------------------------
    # Collection
    # ---------------------------------------------------------

    def collect(self) -> MetricsSnapshot:
        """
        Collect one metrics snapshot and publish it.
        """

        result = self.sampler.collect()

        self._publish(result)

        return result

    # ---------------------------------------------------------
    # Publishing
    # ---------------------------------------------------------

    def _publish(self, snapshot: MetricsSnapshot) -> None:
        """
        Send a snapshot to all registered subscribers.

        A failure in one subscriber must not prevent
        other subscribers from receiving metrics.
        """

        for subscriber in tuple(self._subscribers):

            try:
                subscriber(snapshot)

            except Exception:
                # UI subscribers should never be able to
                # break the metrics pipeline.
                continue