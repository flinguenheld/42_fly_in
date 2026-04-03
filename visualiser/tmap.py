from textual.containers import ScrollableContainer
from textual.app import ComposeResult
import asyncio
from typing import Tuple
from models.hub import Hub
from models.map import Map
from visualiser.tcanvas import TCanvas
from textual.widget import Widget


class TMap(Widget):
    def __init__(self) -> None:
        super().__init__()
        self._canvas: TCanvas | None = None
        # self._layout = ScrollableContainer(classes="tmap_layout")

    # ########################################################################
    # ########################################################### COMPOSE ####
    # def compose(self) -> ComposeResult:
    #     yield self._layout

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
        # self._layout.mount(self._canvas)
        self.mount(self._canvas)

    async def draw_hubs(self, map: Map):

        if self._canvas:
            start = map.start
            if start:
                self.notify(f"here: {start.next_nodes}")
            else:
                self.notify("NO START !!!!!!!")

            for hub_from, hub_to in map.get_connections():
                # self.notify(f"hub: {hub.point}")
                self._canvas._draw_circle(hub_from.point)
                await asyncio.sleep(0.05)
                self._canvas._draw_circle(hub_to.point)
                await asyncio.sleep(0.05)
                self._canvas._draw_line(hub_from.point, hub_to.point)
                await asyncio.sleep(0.02)
