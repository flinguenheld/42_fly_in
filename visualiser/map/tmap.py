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
        self.is_running_all_steps = False

        self._thubs: List[THub] = []
        self._tdrones: Dict[str, TDrone] = dict()

        # Get the size & create canvas --
        self._canvas = TCanvas(*self._get_visual_size())
        self._up_visual_shift()

    # ########################################################################
    # ########################################################## INIT MAP ####
    async def initialise_map(self) -> None:
        """Draw hubs, add drones, up counters and info"""

        await self.draw_hubs()

        for name in self.map.drones:
            drone = TDrone()
            self.mount(drone)
            self._tdrones[name] = drone

            drone.where = self.map.start

        self._up_hub_counters()
        self.info()

    # ########################################################################
    # ################################################# RUNNING ALL STEPS ####
    def stop_running(self) -> None:
        self.is_running_all_steps = False

    async def run_all_steps(self) -> None:
        self.is_running_all_steps = True

        while self.current_turn < self.map.table.nb_turns:
            if not self.is_running_all_steps:
                break

            self.next_turn()

            # Wait the reactive TDrone event
            while not self.is_flying:
                await asyncio.sleep(0.3)

            # And wait the end of the turn
            while self.is_flying:
                await asyncio.sleep(0.3)

            await asyncio.sleep(0.8)

        self.stop_running()

    # ########################################################################
    # ################################################### NEXT / PREVIOUS ####
    def next_turn(self) -> None:
        if self.current_turn < self.map.table.nb_turns:
            self.current_turn += 1
            self.info()

            new_positions = self.map.table.get_turn(self.current_turn)
            self._update_drones(new_positions)

    def previous_turn(self) -> None:
        """
        The previous is tricky since get_turn() only returns edges and
        nothing if the before the first move.
        So compare the current and the previous to create a new dict which
        can contain Edge and Hub.
        """

        if self.current_turn > 0:
            current_positions = self.map.table.get_turn(
                self.current_turn, with_duplicates=True
            )

            self.current_turn -= 1
            self.info()

            previous_positions = self.map.table.get_turn(
                self.current_turn, with_duplicates=True
            )

            manage_start: Dict[str, Hub | Edge] = {}
            for drone, where in current_positions.items():
                if drone not in previous_positions:
                    manage_start[drone] = self.map.start
                else:
                    manage_start[drone] = previous_positions[drone]

            self._update_drones(manage_start)

    # ########################################################################
    # ######################################################### IS FLYING ####
    @property
    def is_flying(self) -> bool:
        return any(d.is_flying for d in self._tdrones.values())

    # ########################################################################
    # ######################################################### UP DRONES ####
    def _update_drones(
        self, new_positions: Dict[str, Edge] | Dict[str, Edge | Hub]
    ) -> None:
        for drone, position in new_positions.items():
            if isinstance(position, Hub) or position.first_on_restricted_zone:
                self._tdrones[drone].where = position

            else:
                self._tdrones[drone].where = position.hub_to

        self._up_hub_counters()

    # ########################################################################
    # ################################################### UP HUB COUNTERS ####
    def _up_hub_counters(self) -> None:
        for thub in self._thubs:
            thub.occupied = sum(
                (1 for d in self._tdrones.values() if d.where == thub._hub)
            )

    # ########################################################################
    # ########################################################### COMPOSE ####
    def compose(self) -> ComposeResult:
        yield self._canvas

    # ########################################################################
    # ######################################################## UP COLOURS ####
    def up_colours(self) -> None:
        for d in self._tdrones.values():
            d.up_colours()

    # ########################################################################
    # ######################################################### DRAW HUBS ####
    async def draw_hubs(self) -> None:

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

    # ########################################################################
    # ######################################################## ANIMATIONS ####
    @override
    async def anim_on(self) -> None:
        for drone in self._tdrones.values():
            await drone.anim_on()

    @override
    async def anim_off(self) -> None:
        self.is_running_all_steps = False

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
