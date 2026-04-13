from typing import override
from visualiser.animation import Anim
import time
import random
import asyncio
from itertools import pairwise

from point import Point
from visualiser.ftheme import FTheme

from textual_canvas import Canvas


class _Coordinate:
    def __init__(self, left: Point, right: Point, light: str):
        self.left = left
        self.right = right
        self.light = light


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀▄░█▀▄░█▀█░█▀█░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█░█░█▀▄░█░█░█░█░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀░░▀░▀░▀▀▀░▀░▀░▀▀▀
class TDrone(Canvas, Anim):
    animation_status: bool = True
    _points = [
        _Coordinate(Point(2, 0), Point(0, 2), ""),
        _Coordinate(Point(1, 0), Point(1, 2), "babord"),
        _Coordinate(Point(0, 0), Point(2, 2), "babord"),
        _Coordinate(Point(0, 1), Point(2, 1), "babord"),
        _Coordinate(Point(0, 2), Point(2, 0), ""),
        _Coordinate(Point(1, 2), Point(1, 0), "tribord"),
        _Coordinate(Point(2, 2), Point(0, 0), "tribord"),
        _Coordinate(Point(2, 1), Point(0, 1), "tribord"),
        _Coordinate(Point(2, 0), Point(0, 2), ""),
    ]

    def __init__(self) -> None:
        Canvas.__init__(self, 3, 4)
        Anim.__init__(self)
        self.up_colours()

        self._blink_time = time.time()
        self._blink_on = True
        self._speed = 0.1

    # ########################################################################
    # ############################################################## TURN ####
    @override
    async def _anim_run(self) -> None:

        try:
            while True:
                for prev, cur in pairwise(TDrone._points):
                    self.clear_pixel(prev.left.x, prev.left.y)
                    self.clear_pixel(prev.right.x, prev.right.y)

                    if self._blink_on:
                        if cur.light == "babord":
                            self.set_pixel(
                                cur.left.x, cur.left.y, FTheme.error
                            )
                        elif cur.light == "tribord":
                            self.set_pixel(
                                cur.left.x, cur.left.y, FTheme.success
                            )
                        else:
                            self.set_pixel(
                                cur.left.x, cur.left.y, FTheme.primary
                            )
                    else:
                        self.set_pixel(cur.left.x, cur.left.y, FTheme.primary)

                    self.set_pixel(cur.right.x, cur.right.y, FTheme.primary)
                    await asyncio.sleep(self._speed)

                self._up_light_and_speed()
        except asyncio.CancelledError:
            pass

    # ########################################################################
    # ################################################## UP LIGHT & SPEED ####
    def _up_light_and_speed(self) -> None:
        if self._blink_on:
            self._blink_on = False
            self._blink_time = time.time() + random.randint(5, 15)

            self._speed = random.randint(5, 8) / 100

        elif time.time() > self._blink_time:
            self._blink_on = True

    # ########################################################################
    # ######################################################## UP COLOURS ####
    def up_colours(self) -> None:
        self.clear(FTheme.background)
        self.set_pixel(1, 1, FTheme.primary)
