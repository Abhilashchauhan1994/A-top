import platform
import socket

import psutil

from textual.widgets import Static


class ATopHeader(Static):

    def on_mount(self) -> None:
        self.update_header()

    def update_header(self) -> None:
        hostname = socket.gethostname()
        uptime = self._get_uptime()
        os_name = platform.system()
        kernel = platform.release()

        self.update(
            f"{hostname}  |  "
            f"Uptime: {uptime}  |  "
            f"OS: {os_name}  |  "
            f"Kernel: {kernel}"
        )

    @staticmethod
    def _get_uptime() -> str:
        uptime_seconds = int(psutil.boot_time())

        current_time = int(psutil.time.time()) if hasattr(psutil, "time") else 0

        return str(current_time - uptime_seconds)