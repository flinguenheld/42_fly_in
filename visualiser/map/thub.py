from models.hub import Hub
from visualiser.ftheme import FTheme

from textual.containers import Grid
from textual.app import ComposeResult
from textual.widgets import Static, Label


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█░█░█░█░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█▀█░█░█░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀▀░░░
class THub(Static):
    WIDTH = 13
    HEIGHT = 7

    def __init__(self, hub: Hub):
        Static.__init__(self)

        self._hub = hub

        self.styles.width = THub.WIDTH
        self.styles.height = THub.HEIGHT
        self.styles.offset = (
            hub.point.visual.x - 3,
            hub.point.visual.y - 5,
        )

        self.styles.color = FTheme.get_regular(self._hub._color)
        self.styles.border = ("double", FTheme.get_regular(self._hub._color))

        self._tcurrent = Label("Ⓒ  0", classes="hub_info")

    # ########################################################################
    # ########################################################### COMPOSE ####
    def compose(self) -> ComposeResult:
        with Grid(id="hub_layout"):
            yield Label(self._get_letter(), classes="hub_type")
            yield Label(self._get_max(), classes="hub_info")
            yield self._tcurrent
            yield Label(self._get_name(), classes="hub_name")

    # ########################################################################
    # ######################################################## GET LETTER ####
    def _get_letter(self) -> str:
        match self._hub._zone:
            case Hub.Zone.NORMAL:
                return "⡷⣸ ⡇\n⠇⠹ ⠧⠤"
            case Hub.Zone.BLOCKED:
                return "⣏⡱ ⣇⠜\n⠧⠜ ⠇⠱"
            case Hub.Zone.PRIORITY:
                return "⣏⡱ ⣏⡱\n⠇  ⠇⠱"
            case _:
                return "⣏⡱ ⣏⡉\n⠇⠱ ⠧⠤"

    # ########################################################################
    # #################################################### GET MAX DRONES ####
    def _get_max(self) -> str:
        if self._hub._max_drones <= 0:
            return "Ⓜ  ∞"
        else:
            return f"Ⓜ {self._hub._max_drones:2}"

    # ########################################################################
    # ########################################################## GET NAME ####
    def _get_name(self) -> str:

        name = self._hub.name

        if "_" in name:
            return name.replace("_", "\n", count=1)

        elif len(name) > 11:
            cut = len(name) // 2
            return f"{name[:cut]}\n{name[cut:]}"

        return name
