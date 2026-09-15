from textual.app import ComposeResult
from textual.widgets import Static


class SystemSummaryWidget(Static):

    def compose(self) -> ComposeResult:
        yield Static(
            "SYSTEM SUMMARY",
            id="system-summary-title",
        )

        yield Static(
            "System summary waiting for data...",
            id="system-summary-info",
        )

    def update_metrics(self, snapshot: dict) -> None:
        system = snapshot["current"]["system"]
        total_processes = system["total_processes"]
        total_threads = system["total_threads"]
        running_processes = system["running_processes"]
        sleeping_processes = system["sleeping_processes"]
        disk_sleep_processes = system["disk_sleep_processes"]
        zombie_processes = system["zombie_processes"]
        login_users = system["login_users"]

        output = (
            f"Processes       {total_processes:>6}\n"
            f"Threads         {total_threads:>6}\n"
            f"\n"
            f"Running         {running_processes:>6}\n"
            f"Sleeping        {sleeping_processes:>6}\n"
            f"Disk Sleep      {disk_sleep_processes:>6}\n"
            f"Zombie          {zombie_processes:>6}\n"
            f"\n"
            f"Login Users      {login_users:>6}"
        )

        info = self.query_one(
            "#system-summary-info",
            Static,
        )

        info.update(output)