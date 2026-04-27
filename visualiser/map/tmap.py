import asyncio
from typing import override, Tuple, List, Set, Dict, Callable

from models.map import Map
from models.hub import Hub
from models.edge import Edge
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

    def __init__(self, map: Map, up_info: Callable[[str], None]) -> None:
        Widget.__init__(self)
        Anim.__init__(self)

        self.map = map
        self.current_turn = 0
        self.up_info_call = up_info

        self._thubs: List[THub] = []

        # Get the size & create canvas --
        self._canvas = TCanvas(*self._get_visual_size())
        self._up_visual_shift()

        self.info()

        # Drones --
        self._tdrones: Dict[str, TDrone] = dict()
        for name in self.map.drones:
            drone = TDrone()
            drone.where = self.map.start
            self._tdrones[name] = drone

    # ########################################################################
    # ################################################### NEXT / PREVIOUS ####
    async def next_turn(self) -> None:
        if self.current_turn < self.map.table.nb_turns:
            self.current_turn += 1
            self.info()

            new_positions = self.map.table.get_turn(self.current_turn)
            await self.update_drones(new_positions)

    async def previous_turn(self) -> None:
        if self.current_turn > 0:
            self.current_turn -= 1
            self.info()

            new_pos = self.map.table.get_turn(self.current_turn, all=True)
            await self.update_drones(new_pos)

    # ########################################################################
    # ############################################################ DRONES ####
    async def update_drones(
        self, new_positions: Dict[str, Hub | Edge | None]
    ) -> None:

        if self.map:
            to_await: List[TDrone] = []

            for drone, position in new_positions.items():
                if not position:
                    position = self.map.start
                self._tdrones[drone].where = position
                to_await.append(self._tdrones[drone])

            while any(d.is_flying for d in to_await):
                await asyncio.sleep(1)

            self._up_hub_counters()
            await asyncio.sleep(2)

        # Update hub counters --

    def _up_hub_counters(self) -> None:
        for thub in self._thubs:
            thub.occupied = sum(
                (1 for d in self._tdrones.values() if d.where == thub._hub)
            )

    # ########################################################################
    # ########################################################### COMPOSE ####
    def compose(self) -> ComposeResult:
        yield self._canvas

        for tdrone in self._tdrones.values():
            yield tdrone

    # ########################################################################
    # ######################################################## UP COLOURS ####
    def up_colours(self) -> None:
        for d in self._tdrones.values():
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
            for hub_fr, hub_to, restriction in self.map.get_edges():
                if hub_fr not in done:
                    _mount_and_save(hub_fr, done)

                if hub_to not in done:
                    _mount_and_save(hub_to, done)

                await asyncio.sleep(0.01)
                self._canvas.draw_node(hub_fr.point, FTheme.foreground)
                self._canvas.draw_node(hub_to.point, FTheme.foreground)
                self._canvas.draw_edge(hub_fr.point, hub_to.point, restriction)
                await asyncio.sleep(0.01)

            self._up_hub_counters()

    # ########################################################################
    # ######################################################## ANIMATIONS ####
    @override
    async def anim_on(self) -> None:
        for drone in self._tdrones.values():
            await drone.anim_on()

    @override
    async def anim_off(self) -> None:
        for drone in self._tdrones.values():
            await drone.anim_off()

    # ###################################################################### #
    # ###################################################################### #
    # ############################## VISUAL SIZE ########################### #
    # !! The canvas pixel system works by dividing a char by 2 on y !!

    # ###################################################################### #
    # ################################################### GET VISUAL SIZE ## #
    def _get_visual_size(self) -> Tuple[int, int]:
        max_row: Hub = max(self.map.hubs, key=lambda h: h.point.row)
        min_row: Hub = min(self.map.hubs, key=lambda h: h.point.row)

        max_col: Hub = max(self.map.hubs, key=lambda h: h.point.col)
        min_col: Hub = min(self.map.hubs, key=lambda h: h.point.col)

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
        if self.map.hubs:
            min_row: Hub = min(self.map.hubs, key=lambda h: h.point.row)
            min_col: Hub = min(self.map.hubs, key=lambda h: h.point.col)

            if min_row and min_col:
                row: int = min_row.point.row
                col: int = min_col.point.col

                shift_row = abs(row) if row < 0 else -row
                shift_col = abs(col) if col < 0 else -col

                Point.visual_shift = Point(shift_row, shift_col)

    # ########################################################################
    # ########################################################### UP_INFO ####
    def info(self) -> None:

        if self.current_turn == 0:
            self.up_info_call(
                f"{self.map.name}\n"
                f"-> {self.map.table.nb_turns} turns to complete <-"
            )
        else:
            self.up_info_call(
                f"{self.map.name}\n"
                f"-> Turn {self.current_turn} on {self.map.table.nb_turns} <-"
            )
