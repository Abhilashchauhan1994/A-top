from atop.widgets.cpu import CPUWidget
from atop.widgets.memory import MemoryWidget
from atop.widgets.process import ProcessTableWidget
from atop.widgets.disk import DiskWidget
from atop.widgets.network import NetworkWidget
from atop.widgets.system import SystemSummaryWidget


class WidgetRegistry:

    def __init__(self, engine):
        self.engine = engine
        self.widgets = []

    def register(self, widget) -> None:
        if widget not in self.widgets:
            self.widgets.append(widget)
            self.engine.subscribe(widget.update_metrics)

    def register_all(self, app) -> None:
        cpu_widget = app.query_one("#cpu-widget", CPUWidget)
        memory_widget = app.query_one("#memory-widget", MemoryWidget)
        process_widget = app.query_one("#process-widget",ProcessTableWidget,)
        disk_widget=app.query_one("#disk-widget",DiskWidget)
        network_widget=app.query_one("#network-widget",NetworkWidget)
        system_widget = app.query_one("#system-summary-widget",SystemSummaryWidget)

        self.register(cpu_widget)
        self.register(memory_widget)
        self.register(process_widget)
        self.register(disk_widget)
        self.register(network_widget)
        self.register(system_widget)

    def unregister(self, widget) -> None:
          if widget in self.widgets:
            self.widgets.remove(widget)
            self.engine.unsubscribe(widget.update_metrics)