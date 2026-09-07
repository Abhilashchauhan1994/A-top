from textual.widgets import Static


class ATopFooter(Static):

    def on_mount(self) -> None:
        self.update(
            "[F1] Overview   "
            "[F2] Processes   "
            "[F3] Disk   "
            "[F4] Network   "
            "[Q] Quit"
        )