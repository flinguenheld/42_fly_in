from __future__ import annotations
from dataclasses import dataclass

from math import sqrt
from error import ErrorFlyIn
from typing import Any, ClassVar


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀█░█▀█░▀█▀░█▀█░▀█▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█░█░░█░░█░█░░█░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░░▀▀▀░▀▀▀░▀░▀░░▀░░░
@dataclass(frozen=True)
class Point:
    """2D point, saved with row/col values"""

    row: int
    col: int

    VISUAL_SCALE_ROW: ClassVar[int] = 20
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

        raise ErrorFlyIn("Operator 'add' only allows Points or int")

    def __mul__(self, other: Any) -> Point:
        if isinstance(other, Point):
            return Point(self.row * other.row, self.col * other.col)
        if isinstance(other, int):
            return Point(self.row * other, self.col * other)

        raise ErrorFlyIn("Operator 'mul' only allows Points or int")

    # ########################################################################
    # ############################################################# PARSE ####
    @staticmethod
    @ErrorFlyIn.spread(title="Point parser")
    def parse(x: str, y: str) -> Point:
        try:
            return Point(int(y), int(x))
        except ValueError:
            raise ErrorFlyIn(f"Impossible to convert '({x},{y})'")
