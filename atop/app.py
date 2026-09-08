from textual.app import App
from textual.containers import Horizontal

from atop.monitor.engine import MetricsEngine
from atop.widgets.header import ATopHeader
from atop.widgets.footer import ATopFooter
from atop.widgets.cpu import CPUWidget
from atop.widgets.memory import MemoryWidget
from atop.widgets.process import ProcessTableWidget



class ATopApp(App):

    CSS_PATH = "styles/app.tcss"

    def __init__(self):
        super().__init__()
        self.engine = MetricsEngine(interval=1.0)

    def compose(self):
        yield ATopHeader()

        with Horizontal(id="metric-row"):
            yield CPUWidget(id="cpu-widget")
            yield MemoryWidget(id="memory-widget")

        yield ProcessTableWidget(id="process-widget")
        # Main content area will go here.
        # CPU, Memory, Disk, Network and Process widgets
        # will be added later.

        yield ATopFooter()

    def on_mount(self)-> None:
        cpu = self.query_one("#cpu-widget", CPUWidget)
        memory = self.query_one("#memory-widget", MemoryWidget)
        process=self.query_one("#process-widget",ProcessTableWidget)

        self.engine.subscribe(
            lambda snapshot: cpu.update_metrics(
                snapshot["current"]["cpu"]
            )
        )

        self.engine.subscribe(
            lambda snapshot: memory.update_metrics(
                snapshot["current"]["memory"]
                )
            )

        self.engine.subscribe(
            lambda snapshot: process.update_metrics(
                snapshot["current"]["process"]["processes"]
            )
        )

        self.engine.start()

        self.set_interval(
            self.engine.interval,
            self.engine.collect,
        )

        # Get the first snapshot immediately.
        self.engine.collect()

if __name__ == "__main__":
    ATopApp().run()