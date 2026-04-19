import sys
from models.point import Point
from visualiser.ftheme import FTheme

from textual.color import Color
from textual_canvas import Canvas


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀▀░█▀█░█▀█░█░█░█▀█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█░░░█▀█░█░█░▀▄▀░█▀█░▀▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░▀░▀░░▀░░▀░▀░▀▀▀░░
class TCanvas(Canvas):
    def __init__(self, rows: int, cols: int) -> None:

        if cols > 0:
            cols *= Point.VISUAL_SCALE_COL
            cols += Point.VISUAL_PADDING_COL * 3
        else:
            cols = Point.VISUAL_PADDING_COL * 2

        if rows > 0:
            rows *= Point.VISUAL_SCALE_ROW
            rows += Point.VISUAL_PADDING_ROW * 2
        else:
            rows = Point.VISUAL_PADDING_ROW * 2

        super().__init__(cols, rows * 2)

    # ########################################################################
    # ################################################# DRAWING FUNCTIONS ####
    def draw_node(self, center: Point, color: Color) -> None:
        center = center.canvas
        super().draw_circle(center.x, center.y, 3, FTheme.foreground)

    def draw_edge(self, fr: Point, to: Point, restriction: int) -> None:

        fr = fr.canvas
        to = to.canvas

        if restriction == sys.maxsize:
            super().draw_line(fr.x, fr.y, to.x, to.y, FTheme.foreground)
        else:
            super().draw_line(fr.x, fr.y, to.x, to.y, FTheme.warning)

        # Draw a circle to easily see the destination --
        distance_row = to.row - fr.row
        distance_col = to.col - fr.col

        row = to.row - distance_row // 4
        col = to.col - distance_col // 4

        super().draw_circle(col, row, 2, FTheme.accent)
