from rich.text import Text
from textual.app import ComposeResult
from textual.widgets import Static


class NetworkWidget(Static):

    DEFAULT_CSS = """
    NetworkWidget {
        width: 100%;
        height: 100%;
        background: #1e293b;
        padding: 1 2;
    }

    #network-info {
        width: 100%;
        height: 1fr;
    }
    """

    def compose(self) -> ComposeResult:
        yield Static(
            "Network waiting for data...",
            id="network-info",
        )

    def update_metrics(self, snapshot: dict) -> None:
        network = snapshot["current"]["network"]
        interfaces = network["interfaces"]

        output = []

        for name, stats in interfaces.items():
            output.append(f"[bold]{name}[/bold]")

            output.append(
                f"  RX   {self._format_bytes(stats['bytes_recv'])}"
            )

            output.append(
                f"  TX   {self._format_bytes(stats['bytes_sent'])}"
            )

            output.append(
                f"  PKT  RX {stats['packets_recv']}  "
                f"TX {stats['packets_sent']}"
            )

            output.append(
                f"  ERR  RX {stats['errin']}  "
                f"TX {stats['errout']}"
            )

            output.append("")

        if not output:
            output.append("No network interfaces found.")

        info = self.query_one("#network-info", Static)

        info.update(Text.from_markup("\n".join(output)))

    @staticmethod
    def _format_bytes(value: int) -> str:
        units = ["B", "KB", "MB", "GB", "TB"]

        size = float(value)

        for unit in units:
            if size < 1024:
                return f"{size:.1f}{unit}"

            size /= 1024

        return f"{size:.1f}PB"