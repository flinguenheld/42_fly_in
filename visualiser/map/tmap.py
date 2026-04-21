import asyncio
from typing import override, Tuple, List, Set

from models.map import Map
from models.hub import Hub
from models.point import Point

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
        self._thubs: List[THub] = []

        # Get the size & create canvas --
        self._canvas = TCanvas(*self._get_visual_size())
        self._up_visual_shift()

        # Drones --
        self._tdrones: List[TDrone] = [
            TDrone(d) for d in self._map.get_drones()
        ]

    # ########################################################################
    # ############################################################ DRONES ####
    async def update_drones(self) -> None:
        to_await = []
        for tdrone in self._tdrones:
            to_await.append(asyncio.create_task(tdrone.fly_to_new_position()))

        for a in to_await:
            await a

        # Update hub counters --
        for thub in self._thubs:
            thub.occupied = sum(
                (1 for d in self._map.drones if d.where == thub._hub)
            )

    # ########################################################################
    # ########################################################### COMPOSE ####
    def compose(self) -> ComposeResult:
        yield self._canvas

        for tdrone in self._tdrones:
            yield tdrone

    # ########################################################################
    # ######################################################## UP COLOURS ####
    def up_colours(self) -> None:
        for d in self._tdrones:
            d.up_colours()

    # ########################################################################
    # ######################################################### DRAW HUBS ####
    async def draw_hubs(self) -> None:

        if self._canvas:

            def _mount_and_save(new: Hub, done: Set[Hub]) -> None:
                h = THub(new)
                done.add(new)
                self.mount(h)
                self._thubs.append(h)

            done: Set[Hub] = set()
            for hub_fr, hub_to, restriction in self._map.get_edges():
                if hub_fr not in done:
                    _mount_and_save(hub_fr, done)

                if hub_to not in done:
                    _mount_and_save(hub_to, done)

                await asyncio.sleep(0.01)
                self._canvas.draw_node(hub_fr.point, FTheme.foreground)
                self._canvas.draw_node(hub_to.point, FTheme.foreground)
                self._canvas.draw_edge(hub_fr.point, hub_to.point, restriction)
                await asyncio.sleep(0.01)

    # ########################################################################
    # ######################################################## ANIMATIONS ####
    @override
    async def anim_on(self) -> None:
        for drone in self._tdrones:
            await drone.anim_on()

    @override
    async def anim_off(self) -> None:
        for drone in self._tdrones:
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
