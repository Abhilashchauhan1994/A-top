from rich.text import Text
from textual.app import ComposeResult
from textual.widgets import Static


class DiskWidget(Static):

    def compose(self) -> ComposeResult:
        yield Static(
            "Disk waiting for data...",
            id="disk-info",
        )

    def update_metrics(self, snapshot: dict) -> None:
        disk = snapshot["current"]["disk"]

        filesystems = disk["filesystems"]
        io = disk["io"]

        output = []

        for filesystem in filesystems:
            mountpoint = filesystem["mountpoint"]
            percent = filesystem["percent"]
            used = self._format_bytes(filesystem["used"])
            total = self._format_bytes(filesystem["total"])

            output.append(
                f"{mountpoint:<12} "
                f"{percent:5.1f}%  "
                f"{used}/{total}"
            )

        output.append("")
        output.append(
            f"READ  {self._format_bytes(io['read_bytes'])}"
        )
        output.append(
            f"WRITE {self._format_bytes(io['write_bytes'])}"
        )

        info = self.query_one("#disk-info", Static)

        info.update(Text("\n".join(output)))

    @staticmethod
    def _format_bytes(value: int) -> str:
        units = ["B", "KB", "MB", "GB", "TB"]

        size = float(value)

        for unit in units:
            if size < 1024:
                return f"{size:.1f}{unit}"

            size /= 1024

        return f"{size:.1f}PB"