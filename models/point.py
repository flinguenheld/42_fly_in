from __future__ import annotations
from dataclasses import dataclass

from math import sqrt
from error import ErrorFlyIn
from typing import Any, ClassVar, Iterator


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀█░█▀█░▀█▀░█▀█░▀█▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█░█░░█░░█░█░░█░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░░▀▀▀░▀▀▀░▀░▀░░▀░░░
@dataclass(frozen=True, unsafe_hash=True)
class Point:
    """2D point, saved with row/col values"""

    row: int
    col: int

    VISUAL_SCALE_ROW: ClassVar[int] = 10
    VISUAL_SCALE_COL: ClassVar[int] = 30
    VISUAL_PADDING_ROW: ClassVar[int] = 6
    VISUAL_PADDING_COL: ClassVar[int] = 10
    visual_shift: ClassVar[int | Point] = 0

    # ########################################################################
    # ############################################################# X / Y ####
    @property
    def x(self) -> int:
        return self.col

    @property
    def y(self) -> int:
        return self.row

    # ########################################################################
    # ################################################### VISUAL / CANVAS ####
    @property
    def visual(self) -> Point:

        pt = self + Point.visual_shift

        row = pt.row * Point.VISUAL_SCALE_ROW + Point.VISUAL_PADDING_ROW
        col = pt.col * Point.VISUAL_SCALE_COL + Point.VISUAL_PADDING_COL

        # Stay on even (regular widgets cannot fit on canvas odd values)
        if row % 2 != 0:
            row += 1

        return Point(row, col)

    @property
    def canvas(self) -> Point:
        """The canvas pixel system works by dividing a char by 2 on y !"""

        pt = self + Point.visual_shift

        return Point(
            pt.row * 2 * Point.VISUAL_SCALE_ROW + Point.VISUAL_PADDING_ROW,
            pt.col * Point.VISUAL_SCALE_COL + Point.VISUAL_PADDING_COL,
        )

    # ########################################################################
    # ###################################################### CALCULATIONS ####
    def width(self, to: Point) -> int:
        return abs((to.col - self.col))

    def height(self, to: Point) -> int:
        return abs((to.row - self.row))

    def distance(self, to: Point) -> int:
        return int(sqrt(self.width(to) ** 2 + self.height(to) ** 2))

    # ########################################################################
    # ############################################################### STR ####
    def __str__(self) -> str:
        return f"({self.row},{self.col})"

    # ########################################################################
    # ######################################################### OPERATORS ####
    def __add__(self, other: Any) -> Point:
        if isinstance(other, Point):
            return Point(self.row + other.row, self.col + other.col)
        if isinstance(other, int):
            return Point(self.row + other, self.col + other)

        raise ErrorFlyIn("Operator 'add' only allows Point or int")

    def __sub__(self, other: Any) -> Point:
        if isinstance(other, Point):
            return self + Point(-other.row, -other.col)
        if isinstance(other, int):
            return self + -other

        raise ErrorFlyIn("Operator 'sub' only allows Point or int")

    def __mul__(self, other: Any) -> Point:
        if isinstance(other, Point):
            return Point(self.row * other.row, self.col * other.col)
        if isinstance(other, int):
            return Point(self.row * other, self.col * other)

        raise ErrorFlyIn("Operator 'mul' only allows Point or int")

    # ########################################################################
    # ############################################################# PARSE ####
    @staticmethod
    @ErrorFlyIn.spread(title="Point parser")
    def parse(x: str, y: str) -> Point:
        try:
            return Point(int(y), int(x))
        except ValueError:
            raise ErrorFlyIn(f"Impossible to convert '({x},{y})'")

    # ########################################################################
    # ######################################## ALL POINTS FROM SELF TO TO ####
    def line_points(self, to: Point) -> Iterator[Point]:

        x0 = self.col
        y0 = self.row

        x1 = to.col
        y1 = to.row

        # Taken from Textual canvas - draw line
        dx = abs(x1 - x0)
        sx = 1 if x0 < x1 else -1
        dy = -abs(y1 - y0)
        sy = 1 if y0 < y1 else -1
        err = dx + dy

        while True:
            yield Point(y0, x0)

            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                if x0 == x1:
                    break
                err += dy
                x0 += sx
            if e2 <= dx:
                if y0 == y1:
                    break
                err += dx
                y0 += sy
