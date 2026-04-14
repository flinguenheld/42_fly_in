from models.hub import Hub
from visualiser.ftheme import FTheme

from textual.containers import Grid
from textual.app import ComposeResult
from textual.widgets import Static, Label


class THub(Static):
    WIDTH = 13
    HEIGHT = 7

    def __init__(self, hub: Hub):
        Static.__init__(self)

        self._hub = hub

        self.styles.width = THub.WIDTH
        self.styles.height = THub.HEIGHT
        self.styles.offset = (
            (hub.point.visual.x) - (THub.WIDTH // 2),
            (hub.point.visual.y // 2 - (THub.HEIGHT // 4)),
        )

        self.styles.color = FTheme.get_regular(self._hub._color)
        self.styles.border = ("double", FTheme.get_regular(self._hub._color))

        self._tcurrent = Label("Ⓒ 00", classes="hub_info")

    def compose(self) -> ComposeResult:
        with Grid(id="hub_layout"):
            yield Label(self._get_letters(), classes="hub_type")
            yield Label("Ⓜ 33", classes="hub_info")
            yield self._tcurrent
            yield Label(self._hub.name[:18], classes="hub_name")

    def _get_letters(self) -> str:
        match self._hub._zone:
            case Hub.Zone.NORMAL:
                return "⡷⣸\n⠇⠹"
            case Hub.Zone.BLOCKED:
                return "⣏⡱\n⠧⠜"
            case Hub.Zone.PRIORITY:
                return "⣏⡱\n⠇ "
            case _:
                return "⣏⡱\n⠇⠱"
