import asyncio
from textual.app import ComposeResult
from textual.containers import ScrollableContainer

from models.map import Map
from textual.widget import Widget
from visualiser.tcanvas import TCanvas


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▄█░█▀█░█▀█
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█░█░█▀█░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀░▀░▀░░
class TMap(Widget):
    def __init__(self) -> None:
        super().__init__()
        self._canvas: TCanvas | None = None
        self._layout = ScrollableContainer(classes="tmap_layout")

    # ########################################################################
    # ########################################################### COMPOSE ####
    def compose(self) -> ComposeResult:
        yield self._layout

    # ########################################################################
    # ###################################################### RESET CANVAS ####
    def new_canvas(self, map: Map) -> None:
        """
        Delete the current canvas to create and mount a brand new one
        (mandatory to change the area size and adapt the position)
        """
        if self._canvas:
            self._canvas.clear()
            self._canvas.remove()

        self._canvas = TCanvas(map)
        self._layout.mount(self._canvas)

    # ########################################################################
    # ######################################################### DRAW HUBS ####
    async def draw_hubs(self, map: Map) -> None:

        if self._canvas:
            for hub_from, hub_to in map.get_connections():
                self._canvas.draw_adapted_circle(hub_from.point)
                await asyncio.sleep(0.02)
                self._canvas.draw_adapted_circle(hub_to.point)
                await asyncio.sleep(0.02)
                self._canvas.draw_adapted_line(hub_from.point, hub_to.point)
                await asyncio.sleep(0.01)
