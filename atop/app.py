from textual.app import App
from textual.containers import Horizontal

from atop.monitor.engine import MetricsEngine
from atop.monitor.register import WidgetRegistry
from atop.widgets.header import ATopHeader
from atop.widgets.footer import ATopFooter
from atop.widgets.cpu import CPUWidget
from atop.widgets.memory import MemoryWidget
from atop.widgets.process import ProcessTableWidget
from atop.widgets.disk import DiskWidget
from atop.widgets.network import NetworkWidget



class ATopApp(App):

    CSS_PATH = "styles/app.tcss"

    def __init__(self):
        super().__init__()
        self.engine = MetricsEngine(interval=1.0)
        self.registry = WidgetRegistry(self.engine)

    def compose(self):
        yield ATopHeader()

        with Horizontal(id="metric-row"):
            yield CPUWidget(id="cpu-widget")
            yield MemoryWidget(id="memory-widget")
            yield DiskWidget(id="disk-widget")
            yield NetworkWidget(id="network-widget")

        yield ProcessTableWidget(id="process-widget")


        yield ATopFooter()

    def on_mount(self)-> None:
        self.registry.register_all(self)
        self.engine.start()

        self.set_interval(
            self.engine.interval,
            self.engine.collect,
        )

        # Get the first snapshot immediately.
        self.engine.collect()

if __name__ == "__main__":
    ATopApp().run()