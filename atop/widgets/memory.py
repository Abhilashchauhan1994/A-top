import plotext as plt

from rich.text import Text
from textual.app import ComposeResult
from textual.widgets import Static


class MemoryWidget(Static):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.memory_history = []
        self.history_size = 30

    def compose(self) -> ComposeResult:
        yield Static(
            "Memory waiting for data...",
            id="memory-info",
        )
        yield Static(
            "",
            id="memory-chart",
        )

    def on_mount(self) -> None:
        self.call_after_refresh(self.render_chart)

    def update_metrics(self, snapshot: dict) -> None:
        memory = snapshot["current"]["memory"]
        percent = memory["percent"]
        total = memory["total"]
        used = memory["used"]
        available = memory["available"]

        self.memory_history.append(percent)

        if len(self.memory_history) > self.history_size:
            self.memory_history.pop(0)

        info = self.query_one("#memory-info", Static)

        info.update(
            f"MEM  {percent:5.1f}%    "
            f"Total  {self._format_bytes(total)}    "
            f"Used  {self._format_bytes(used)}    "
            f"Free  {self._format_bytes(available)}"
        )

        self.call_after_refresh(self.render_chart)

    def on_resize(self) -> None:
        self.call_after_refresh(self.render_chart)

    def render_chart(self) -> None:
        if not self.memory_history:
            return

        chart = self.query_one("#memory-chart", Static)

        width = chart.size.width
        height = chart.size.height

        if width <= 0 or height <= 0:
            return
        fig = plt.figure
        fig.clear()
        fig.plot_size(width, height)
        x = list(range(len(self.memory_history)))
        y = self.memory_history
        bg_rgb = (30, 41, 59)
        fig.canvas(bg_rgb)
        fig.theme("colorless")
        fig.axes(
            active=False,
            side="upper",
            axis=x,
        )
        signal = (
            fig.signal(
                x,
                y,
                marker=plt.marker(
                    "braille",
                    pixel="cyan",
                ),
            )
            .lines()
            .density(
                "full",
                scope="line",
            )
        )
        fig.draw(signal)
        fig.title()
        ansi_output = fig.build().string()
        chart.update(
            Text.from_ansi(ansi_output)
        )

    @staticmethod
    def _format_bytes(value: int) -> str:
        units = ["B", "KB", "MB", "GB", "TB"]
        size = float(value)
        for unit in units:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}PB"