from __future__ import annotations
from functools import singledispatch
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
    ) -> None:
        """2D point, saved with row/col values"""
        self.row: int = row
        self.col: int = col

    # ########################################################################
    # ############################################################# X / Y ####
    @property
    def xy(self) -> Tuple[int, int]:
        return (self.col, self.row)

    @singledispatch
    def from_xy(self, x: int, y: int):
        self.row = y
        self.col = x

    @from_xy.register(str)
    def _(self, x: str, y: str):
        try:
            self.from_xy(x=int(x), y=int(y))

        except ValueError:
            raise ValueError(f"Point: Impossible to convert ({x},{y})")

    @staticmethod
    def new_from_xy(x: str, y: str) -> Point:
        pt = Point(0, 0)
        pt.from_xy(x, y)
        return pt

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
        return f"({self.row})/{self.col})"
