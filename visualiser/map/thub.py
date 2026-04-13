from visualiser.ftheme import FTheme
from models.hub import Hub
from textual.app import ComposeResult
from textual.containers import VerticalGroup
from textual.widgets import Static, Label


class THub(Static):
    WIDTH = 11
    HEIGHT = 6

    def __init__(self, hub: Hub):
        Static.__init__(self)

        self._hub = hub

        self._tname = Label(hub.name[:18], classes="hub_name")

        self.styles.width = THub.WIDTH
        self.styles.height = THub.HEIGHT
        self.styles.offset = (
            (hub.point.visual.x) - (THub.WIDTH // 2),
            (hub.point.visual.y // 2 - (THub.HEIGHT // 4)),
        )

        self.styles.color = FTheme.get_regular(self._hub._color)
        self.styles.border = ("double", FTheme.get_regular(self._hub._color))

    def compose(self) -> ComposeResult:
        with VerticalGroup():
            yield Label(self._get_letter(), classes="hub_h")
            yield self._tname

    def _get_letter(self) -> str:
        match self._hub._zone:
            case Hub.Zone.NORMAL:
                return "⡷⣸\n⠇⠹"
            case Hub.Zone.BLOCKED:
                return "⣏⡱\n⠧⠜"
            case Hub.Zone.PRIORITY:
                return "⣏⡱\n⠇ "
            case _:
                return "⣏⡱\n⠇⠱"
