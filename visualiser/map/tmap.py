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
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▄█░█▀█░█▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█░█░█▀█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀░▀░▀░░░░
class TMap(Widget, Anim):
    HEIGHT_MINI = 5

    def __init__(self, map: Map) -> None:
        Widget.__init__(self)
        Anim.__init__(self)

        self._map = map

        # Get the size & create canvas --
        self._canvas = TCanvas(*self._get_visual_size())
        self._up_visual_shift()

        # Drones --
        self._drones: List[TDrone] = [
            TDrone() for _ in range(self._map.nb_drones)
        ]

    async def draw_drones(self) -> None:
        if self._map.start:
            for d in self._drones:
                self.mount(d)
                d.set_position(self._map.start.point)
                # d.set_position(Point(2, 2))

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
                if hub_from._name not in done:
                    self.mount(THub(hub_from))
                    done.append(hub_from.name)

                if hub_to._name not in done:
                    self.mount(THub(hub_to))
                    done.append(hub_to.name)

                self._canvas.draw_node(hub_from.point, FTheme.foreground)
                await asyncio.sleep(0.02)
                self._canvas.draw_node(hub_to.point, FTheme.foreground)
                await asyncio.sleep(0.02)
                self._canvas.draw_edge(hub_from.point, hub_to.point)
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

                Point.visual_shift = Point(shift_row, shift_col)
