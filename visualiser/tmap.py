from typing import override
from visualiser.animation import Anim
from visualiser.tdrone import TDrone
from textual.widgets import Label
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
class TMap(Widget, Anim):
    def __init__(self) -> None:
        Widget.__init__(self)
        Anim.__init__(self)

        self._canvas: TCanvas | None = None
        self._test_overlay: Label = Label("hello", id="test_overlay")
        self._layout = ScrollableContainer(classes="tmap_layout")

        self._blah_position = 2
        self._drones = [
            TDrone(),
            TDrone(),
            TDrone(),
            TDrone(),
            TDrone(),
            TDrone(),
        ]

        for i, d in enumerate(self._drones):
            d.styles.offset = (3, (i + 2) * 4)

    # ########################################################################
    # ######################################################## UP COLOURS ####
    def up_colours(self) -> None:
        for d in self._drones:
            d.up_colours()

    def move_baby(self) -> None:
        self._blah_position += 1
        # self._test_overlay.styles.offset = (self._blah_position, 6)
        for i, d in enumerate(self._drones):
            d.styles.offset = (self._blah_position, d.offset[1])

    # ########################################################################
    # ########################################################### COMPOSE ####
    def compose(self) -> ComposeResult:
        yield self._layout
        for drone in self._drones:
            yield drone

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
        self._layout.mount(self._test_overlay)

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

    # ########################################################################
    # ######################################################## ANIMATIONS ####
    @override
    def anim_on(self) -> None:
        for drone in self._drones:
            drone.anim_on()

    @override
    def anim_off(self) -> None:
        for drone in self._drones:
            drone.anim_off()
