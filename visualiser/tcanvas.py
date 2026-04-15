from point import Point

from textual.color import Color
from textual_canvas import Canvas


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀▀░█▀█░█▀█░█░█░█▀█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█░░░█▀█░█░█░▀▄▀░█▀█░▀▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░▀░▀░░▀░░▀░▀░▀▀▀░░
class TCanvas(Canvas):
    _RADIUS: int = 2

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
    def draw_adapted_circle(self, center: Point, color: Color) -> None:
        # TODO: Still usefull ???
        point = center.canvas
        super().draw_circle(point.x, point.y, TCanvas._RADIUS, color)

    def draw_adapted_line(
        self, pt_from: Point, pt_to: Point, color: Color
    ) -> None:
        fr = pt_from.canvas
        to = pt_to.canvas

        super().draw_line(fr.x, fr.y, to.x, to.y, color)
