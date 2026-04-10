from textual.color import Color
from textual_canvas import Canvas

from point import Point


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀▀░█▀█░█▀█░█░█░█▀█░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█░░░█▀█░█░█░▀▄▀░█▀█░▀▀█
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░▀░▀░░▀░░▀░▀░▀▀▀
class TCanvas(Canvas):
    _RADIUS: int = 2

    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)

    # ########################################################################
    # ################################################# DRAWING FUNCTIONS ####
    def draw_adapted_circle(
        self, center: Point, color: Color | None = None
    ) -> None:
        # TODO: Still usefull ???
        point = center.visual
        super().draw_circle(point.x, point.y, TCanvas._RADIUS, color)

    def draw_adapted_line(
        self, pt_from: Point, pt_to: Point, color: Color | None = None
    ) -> None:
        fr = pt_from.visual
        to = pt_to.visual

        super().draw_line(fr.x, fr.y, to.x, to.y, color)
