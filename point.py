from __future__ import annotations
from math import sqrt
from typing import Tuple, Any

from error import ErrorFlyIn


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
    # ############################################################# PARSE ####
    @staticmethod
    def parse(x: str, y: str) -> Point:
        try:
            return Point(int(y), int(x))
        except ValueError:
            raise ErrorPoint(f"Impossible to convert '({x},{y})'")

    # ########################################################################
    # ############################################################# X / Y ####
    @property
    def xy(self) -> Tuple[int, int]:
        return (self.col, self.row)

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
    # ############################################################# EQUAL ####
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Point):
            return self.row == other.row and self.col == other.col
        return False


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀▄░█▀▄░█▀█░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀▄░█▀▄░█░█░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░▀░▀░▀░▀▀▀░▀░▀
class ErrorPoint(ErrorFlyIn):
    def __init__(self, message: str) -> None:
        super().__init__(f"Point error:\n{message}")
