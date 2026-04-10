from models.hub import Hub
from textual.app import ComposeResult
from textual.containers import VerticalGroup
from textual.widgets import Static, Label


class THub(Static):
    WIDTH = 11
    HEIGHT = 6

    def __init__(self, hub: Hub):
        Static.__init__(self)

        self._tname = Label(hub.name[:18], classes="hub_name")

        self.styles.width = THub.WIDTH
        self.styles.height = THub.HEIGHT
        self.styles.offset = (
            (hub.point.visual.x) - (THub.WIDTH // 2),
            (hub.point.visual.y // 2 - (THub.HEIGHT // 4)),
        )

    def compose(self) -> ComposeResult:
        with VerticalGroup():
            yield Label(" █▄█\n ▀ ▀", classes="hub_h")
            yield self._tname
