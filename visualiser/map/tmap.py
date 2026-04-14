import asyncio
from point import Point
from models.map import Map
from models.hub import Hub
from typing import override, Tuple, List

from textual.widget import Widget
from textual.app import ComposeResult

from visualiser.map.thub import THub
from visualiser.ftheme import FTheme
from visualiser.animation import Anim
from visualiser.tcanvas import TCanvas
from visualiser.map.tdrone import TDrone


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▄█░█▀█░█▀█
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█░█░█▀█░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀░▀░▀░░
class TMap(Widget, Anim):
    def __init__(self, map: Map) -> None:
        Widget.__init__(self)
        Anim.__init__(self)

        self._map = map

        # Set the size & create the canvas --
        height, width = self._get_visual_size()
        self._up_visual_shift()

        width = (
            width * Point.VISUAL_SCALE if width > 0 else Point.VISUAL_SCALE
        ) + Point.VISUAL_PADDING * 2
        height = (
            height * Point.VISUAL_SCALE if height > 0 else Point.VISUAL_SCALE
        ) + Point.VISUAL_PADDING * 3

        self._canvas = TCanvas(width, height)

        # Drones --
        self._drones: List[TDrone] = [
            TDrone() for _ in range(self._map.nb_drones)
        ]

    # ########################################################################
    # ########################################################### COMPOSE ####
    def compose(self) -> ComposeResult:
        yield self._canvas

    # ########################################################################
    # ######################################################## UP COLOURS ####
    def up_colours(self) -> None:
        for d in self._drones:
            d.up_colours()

    # ########################################################################
    # ######################################################### DRAW HUBS ####
    async def draw_hubs(self) -> None:

        done = list()

        if self._canvas:
            for hub_from, hub_to in self._map.get_connections():
                if hub_from.name not in done:
                    self.mount(THub(hub_from))
                    done.append(hub_from.name)

                if hub_to.name not in done:
                    self.mount(THub(hub_to))
                    done.append(hub_to.name)

                # self.notify(f"draw that point: {hub_from.point}")
                # self.notify(f"draw that adapted: {hub_from.point.visual}")
                self._canvas.draw_adapted_circle(
                    hub_from.point, FTheme.foreground
                )
                # await asyncio.sleep(0.02)
                self._canvas.draw_adapted_circle(
                    hub_to.point, FTheme.foreground
                )
                await asyncio.sleep(0.02)
                self._canvas.draw_adapted_line(
                    hub_from.point, hub_to.point, FTheme.foreground
                )
                await asyncio.sleep(0.01)

    # ########################################################################
    # ######################################################## ANIMATIONS ####
    @override
    async def anim_on(self) -> None:
        for drone in self._drones:
            await drone.anim_on()

    @override
    async def anim_off(self) -> None:
        for drone in self._drones:
            await drone.anim_off()

    # ###################################################################### #
    # ###################################################################### #
    # ############################## VISUAL SIZE ########################### #
    # !! The canvas pixel system works by dividing a char by 2 on y !!

    # ###################################################################### #
    # ################################################### GET VISUAL SIZE ## #
    def _get_visual_size(self) -> Tuple[int, int]:
        """
        Get the required size of the canvas.
        """

        max_row: Hub = max(self._map.hubs, key=lambda h: h.point.row)
        min_row: Hub = min(self._map.hubs, key=lambda h: h.point.row)

        max_col: Hub = max(self._map.hubs, key=lambda h: h.point.col)
        min_col: Hub = min(self._map.hubs, key=lambda h: h.point.col)

        if max_row and min_row and max_col and min_col:
            rows = max_row.point.row - min_row.point.row
            cols = max_col.point.col - min_col.point.col
            return (rows, cols)

        return (0, 0)

    # ########################################################################
    # ################################################## GET VISUAL SHIFT ####
    def _up_visual_shift(self) -> None:
        """
        Compute a 'shift' value to move the graph at the top left.
        """
        if self._map.hubs:
            min_row: Hub = min(self._map.hubs, key=lambda h: h.point.row)
            min_col: Hub = min(self._map.hubs, key=lambda h: h.point.col)

            if min_row and min_col:
                row: int = min_row.point.row
                col: int = min_col.point.col

                shift_row = abs(row) if row < 0 else -row
                shift_col = abs(col) if col < 0 else -col

                Point.set_visual_shift(shift_row, shift_col)
