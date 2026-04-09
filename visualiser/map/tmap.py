from point import Point
from models.hub import Hub
from visualiser.map.thub import THub
import asyncio
from typing import override, Tuple

from textual.widget import Widget
from textual.app import ComposeResult

from models.map import Map
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

        # Size ?
        # TODO: embelish that
        height, width = self._get_visual_size()
        self._get_visual_shift()

        width = (
            width * Point.VISUAL_SCALE if width > 0 else Point.VISUAL_SCALE
        ) + Point.VISUAL_PADDING * 2
        height = (
            height * Point.VISUAL_SCALE if height > 0 else Point.VISUAL_SCALE
        ) + Point.VISUAL_PADDING * 2

        self._canvas = TCanvas(width, height)

        self._blah_position = 2
        self._drones = [
            # TDrone(),
            # TDrone(),
            # TDrone(),
            # TDrone(),
            # TDrone(),
            # TDrone(),
        ]

        self._hubs = [
            # THub(),
            # THub(),
            # THub(),
        ]

        for i, d in enumerate(self._drones):
            d.styles.offset = (3, (i + 2) * 4)

        for i, h in enumerate(self._hubs):
            h.styles.offset = (20, (i + 2) * 5)

        self._canvas.draw_line(5, 5, 10, 10)

    # ########################################################################
    # ########################################################## GET SIZE ####
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
    # ######################################################### GET SHIFT ####
    def _get_visual_shift(self) -> None:
        """
        Compute a 'shift' value to move the graph at the top left.
        """
        if self._map.hubs:
            min_row: Hub = min(self._map.hubs, key=lambda h: h.point.row)
            min_col: Hub = min(self._map.hubs, key=lambda h: h.point.col)

            if min_row and min_col:
                row: int = min_row.point.row * Point.VISUAL_SCALE
                col: int = min_col.point.col * Point.VISUAL_SCALE

                shift_row = abs(row) if row < 0 else -row
                shift_col = abs(col) if col < 0 else -col

                # TODO: adapt padding -----------------------------
                self._shift = Point(
                    shift_row + Point.VISUAL_PADDING,
                    shift_col + Point.VISUAL_PADDING,
                )

                self.notify(f"shift set: {Point(shift_row, shift_col)}")
                Point.set_visual_shift(Point(shift_row, shift_col))

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

        # with VerticalGroup():
        yield self._canvas

        for hub in self._hubs:
            yield hub

        for drone in self._drones:
            yield drone

    # ########################################################################
    # ######################################################### DRAW HUBS ####
    async def draw_hubs(self) -> None:

        if self._canvas:
            for hub_from, hub_to in self._map.get_connections():
                self.notify(f"draw that point: {hub_from.point}")
                self.notify(f"draw that adapted: {hub_from.point.visual}")
                self._canvas.draw_adapted_circle(hub_from.point)
                await asyncio.sleep(0.02)
                self._canvas.draw_adapted_circle(hub_to.point)
                await asyncio.sleep(0.02)
                self._canvas.draw_adapted_line(hub_from.point, hub_to.point)
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
