from textual.reactive import reactive
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

    occupied = reactive(0)

    def __init__(self, hub: Hub):
        Static.__init__(self)

        self._hub = hub

        self.styles.width = THub.WIDTH
        self.styles.height = THub.HEIGHT
        self.styles.offset = (hub.point.visual.x - 3, hub.point.visual.y - 5)

        self.styles.color = FTheme.get_regular(self._hub.color)
        if self._hub.type == Hub.Type.REGULAR:
            self.styles.border = (
                "round",
                FTheme.get_regular(self._hub.color),
            )
        else:
            self.styles.border = (
                "outer",
                FTheme.get_regular(self._hub.color),
            )

        self._toccupied = Label("Ⓒ  0", classes="hub_info")

    # ########################################################################
    # ############################################### OCCUPIED REACTIVITY ####
    def watch_occupied(self, old_occupied: int, new_occupied: int) -> None:
        self._toccupied.update(f"Ⓒ {new_occupied:2}")

    # ########################################################################
    # ########################################################### COMPOSE ####
    def compose(self) -> ComposeResult:
        with Grid(id="hub_layout"):
            yield Label(self._get_letter(), classes="hub_type")
            yield Label(self._get_max(), classes="hub_info")
            yield self._toccupied
            yield Label(self._get_name(), classes="hub_name")

    # ########################################################################
    # ######################################################## GET LETTER ####
    def _get_letter(self) -> str:
        match self._hub.zone:
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
        if self._hub.type in [Hub.Type.START, Hub.Type.END]:
            return "Ⓜ  ∞"
        else:
            return f"Ⓜ {self._hub.max_drones:2}"

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
