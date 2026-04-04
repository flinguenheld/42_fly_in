from typing import Tuple
from textual.color import Color
from textual_canvas import Canvas

from point import Point
from models.hub import Hub
from models.map import Map


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀▀░█▀█░█▀█░█░█░█▀█░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█░░░█▀█░█░█░▀▄▀░█▀█░▀▀█
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░▀░▀░░▀░░▀░▀░▀▀▀
class TCanvas(Canvas):
    _SCALE: int = 30
    _RADIUS: int = 2
    _PADDING: int = 20

    def __init__(self, map: Map) -> None:

        self._set_shift(map)
        rows, cols = self._set_size(map)

        super().__init__(
            cols * TCanvas._SCALE + TCanvas._PADDING,
            rows * TCanvas._SCALE + TCanvas._PADDING,
        )

    # ########################################################################
    # ########################################################## GET SIZE ####
    def _set_size(self, map: Map) -> Tuple[int, int]:
        """
        Save the map and return the required size of the canvas
        """

        max_row: Hub = max(map.hubs, key=lambda h: h.point.row)
        min_row: Hub = min(map.hubs, key=lambda h: h.point.row)

        max_col: Hub = max(map.hubs, key=lambda h: h.point.col)
        min_col: Hub = min(map.hubs, key=lambda h: h.point.col)

        if max_row and min_row and max_col and min_col:
            rows = max_row.point.row - min_row.point.row
            cols = max_col.point.col - min_col.point.col
            return (rows, cols)

        return (0, 0)

    # ########################################################################
    # ######################################################### SET SHIFT ####
    def _set_shift(self, map: Map) -> None:
        if map.hubs:
            min_row: Hub = min(map.hubs, key=lambda h: h.point.row)
            min_col: Hub = min(map.hubs, key=lambda h: h.point.col)

            if min_row and min_col:
                row: int = min_row.point.row * self._SCALE
                col: int = min_col.point.col * self._SCALE

                shift_row = abs(row) if row < 0 else -row
                shift_col = abs(col) if col < 0 else -col

                self._shift = Point(
                    shift_row + TCanvas._PADDING // 2,
                    shift_col + TCanvas._PADDING // 2,
                )

    # ########################################################################
    # ####################################################### ADAPT POINT ####
    def _adapt_point(self, point: Point) -> Point:
        return point * TCanvas._SCALE + self._shift

    # ########################################################################
    # ################################################# DRAWING FUNCTIONS ####
    def draw_adapted_circle(
        self, center: Point, color: Color | None = None
    ) -> None:
        point = self._adapt_point(center)
        super().draw_circle(point.x, point.y, TCanvas._RADIUS, color)

    def draw_adapted_line(
        self, pt_from: Point, pt_to: Point, color: Color | None = None
    ) -> None:
        fr = self._adapt_point(pt_from)
        to = self._adapt_point(pt_to)

        super().draw_line(fr.x, fr.y, to.x, to.y, color)
