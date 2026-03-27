from __future__ import annotations
from math import sqrt
from typing import Tuple


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀█░█▀█░▀█▀░█▀█░▀█▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█░█░░█░░█░█░░█░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░░▀▀▀░▀▀▀░▀░▀░░▀░
class Point:
    def __init__(
        self,
        row: int = 0,
        col: int = 0,
        x: int | None = None,
        y: int | None = None,
    ) -> None:
        """2D point, saved with row/col values"""
        self.row: int = row
        self.col: int = col

        if x and y:
            self.row = y
            self.col = x

    def __str__(self) -> str:
        return f"({self.row})/{self.col})"

    # ########################################################################
    # ############################################################# X / Y ####
    def to_xy(self) -> Tuple[int, int]:
        return (self.col, self.row)

    # ########################################################################
    # ###################################################### CALCULATIONS ####
    def width(self, to: Point) -> int:
        return abs((to.col - self.col))

    def height(self, to: Point) -> int:
        return abs((to.row - self.row))

    def distance(self, to: Point) -> int:
        return int(sqrt(self.width(to) ** 2 + self.height(to) ** 2))
