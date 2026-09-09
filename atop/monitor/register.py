from atop.widgets.cpu import CPUWidget
from atop.widgets.memory import MemoryWidget
from atop.widgets.process import ProcessTableWidget


class WidgetRegistry:

    def __init__(self, engine):
        self.engine = engine
        self.widgets = []

    def register(self, widget) -> None:
        """Register a widget and subscribe it to the metrics engine."""

        if widget not in self.widgets:
            self.widgets.append(widget)
            self.engine.subscribe(widget.update_metrics)

    def register_all(self, app) -> None:
        """Create and register all application widgets."""

        cpu_widget = app.query_one("#cpu-widget", CPUWidget)
        memory_widget = app.query_one("#memory-widget", MemoryWidget)
        process_widget = app.query_one("#process-widget",ProcessTableWidget,)

        self.register(cpu_widget)
        self.register(memory_widget)
        self.register(process_widget)

    def unregister(self, widget) -> None:
        """Remove a widget from the metrics engine."""

        if widget in self.widgets:
            self.widgets.remove(widget)
            self.engine.unsubscribe(widget.update_metrics)