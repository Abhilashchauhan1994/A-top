from textual.app import ComposeResult
from textual.widgets import DataTable,Static
from textual.containers import Container

class ProcessTableWidget(Container):
    def compose(self) -> ComposeResult:
        yield Static("PROCESSES", classes="widget-title")
        yield DataTable(id="process_table")

    def _on_mount(self, event) -> None:
        table=self.query_one("#process_table",DataTable)

        table.add_columns(
            "PID",
            "NAME",
            "CPU %",
            "MEM %",
            "STATUS",
            "THREADS",
            "COMMAND",
        )

    def update_metrics(self,processes)->None:
        table=self.query_one("#process_table",DataTable)
        # table.clear()

        for process in processes:
            table.add_row(
                str(process["pid"]),
                str(process["name"])[:25],
                f"{process['cpu_percent']:.1f}",
                f"{process['memory_percent']:.1f}",
                str(process["status"]),
                str(process["num_threads"]),
                str(process["cmdline"])[:60],
            )

