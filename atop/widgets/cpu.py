import plotext as plt

from rich.text import Text
from textual.app import ComposeResult
from textual.widgets import Static


class CPUWidget(Static):

    DEFAULT_CSS = """
    CPUWidget {
        width: 100%;
        height: 100%;
        background: #1e293b;
        padding: 1 2;
    }

    #cpu-info {
        width: 100%;
        height: 3;
    }

    #cpu-chart {
        width: 100%;
        height: 1fr;
    }
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cpu_history = []
        self.history_size = 30

    def compose(self) -> ComposeResult:
        yield Static("CPU waiting for data...", id="cpu-info")
        yield Static("", id="cpu-chart")

    def on_mount(self) -> None:
        # Wait until Textual has calculated widget sizes.
        self.call_after_refresh(self.render_chart)

    def update_metrics(self, snapshot: dict) -> None:

        cpu=snapshot["current"]["cpu"]

        usage = cpu["usage"]
        cores = cpu["cpu_cores"]
        load_average = cpu["load_average"]

        self.cpu_history.append(usage)

        if len(self.cpu_history) > self.history_size:
            self.cpu_history.pop(0)

        info = self.query_one("#cpu-info", Static)

        info.update(
            f"CPU  {usage:5.1f}%    "
            f"Cores  {cores}    "
            f"Load  "
            f"{load_average[0]:.2f} "
            f"{load_average[1]:.2f} "
            f"{load_average[2]:.2f}"
        )

        self.call_after_refresh(self.render_chart)

    def on_resize(self) -> None:
        self.call_after_refresh(self.render_chart)

    def render_chart(self) -> None:

        if not self.cpu_history:
            return

        chart = self.query_one("#cpu-chart", Static)

        width = chart.size.width
        height = chart.size.height

        if width <= 0 or height <= 0:
            return

        fig = plt.figure
        fig.clear()

        fig.plot_size(width, height)

        x = list(range(len(self.cpu_history)))
        y = self.cpu_history

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