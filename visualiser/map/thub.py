from textual.app import ComposeResult
from textual.containers import VerticalGroup
from textual.widgets import Static, Label


class THub(Static):
    def __init__(self, name: str = "hub name"):
        Static.__init__(self)
        self._tname = Label(name[:7], classes="hub_name")

    def compose(self) -> ComposeResult:
        with VerticalGroup():
            yield Label("█▄█\n▀ ▀", classes="hub_label")
            yield self._tname
