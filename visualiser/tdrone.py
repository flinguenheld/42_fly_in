import time
import random
import asyncio
from enum import Enum
from itertools import cycle, pairwise

from point import Point
from visualiser.theme import Theme

from textual.color import Color
from textual_canvas import Canvas


class _Blink(Enum):
    BABORD = 0
    TRIBORD = 1
    DONE = 2
    WAIT = 3


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀▄░█▀▄░█▀█░█▀█░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█░█░█▀▄░█░█░█░█░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀░░▀░▀░▀▀▀░▀░▀░▀▀▀
class TDrone(Canvas):
    _points = [
        (Point(0, 0), Point(2, 2)),
        (Point(0, 1), Point(2, 1)),
        (Point(0, 2), Point(2, 0)),
        (Point(1, 2), Point(1, 0)),
        (Point(2, 2), Point(0, 0)),
        (Point(2, 1), Point(0, 1)),
        (Point(2, 0), Point(0, 2)),
        (Point(1, 0), Point(1, 2)),
    ]

    def __init__(self) -> None:
        super().__init__(3, 4)
        self.up_colours()
        self._blink_time = time.time()

    def on_mount(self) -> None:
        asyncio.create_task(self._turn())

    # ########################################################################
    # ######################################################## UP COLOURS ####
    def up_colours(self) -> None:
        self._colour_drone: Color = Theme.primary
        self.clear(Theme.background)
        self.set_pixel(1, 1, color=self._colour_drone)

    # ########################################################################
    # ############################################################## TURN ####
    async def _turn(self) -> None:

        change_speed = 100
        blink_state = _Blink.TRIBORD

        for (prev_a, prev_b), (a, b) in pairwise(cycle(TDrone._points)):
            change_speed += 1
            if change_speed >= 100:
                speed = random.randint(5, 8) / 100
                change_speed = 0

            self.clear_pixel(prev_a.x, prev_a.y)
            self.clear_pixel(prev_b.x, prev_b.y)

            self.set_pixel(b.x, b.y, color=self._colour_drone)
            blink_state = self._set_blinxel(a, blink_state)
            blink_state = self._up_blink(blink_state)

            await asyncio.sleep(speed)

    # ########################################################################
    # ################################################# SET PIXEL (BLINK) ####
    def _set_blinxel(self, a: Point, blink_state: _Blink) -> _Blink:

        if blink_state == _Blink.TRIBORD and a == Point(2, 2):
            self.set_pixel(a.x, a.y, color=Theme.success)
            return _Blink.BABORD

        if blink_state == _Blink.BABORD and a == Point(0, 0):
            self.set_pixel(a.x, a.y, color=Theme.error)
            return _Blink.DONE

        self.set_pixel(a.x, a.y, color=self._colour_drone)
        return blink_state

    # ########################################################################
    # ########################################################## UP BLINK ####
    def _up_blink(self, blink_state: _Blink) -> _Blink:

        match blink_state:
            case _Blink.DONE:
                self._blink_time = time.time() + random.randint(5, 15)
                return _Blink.WAIT

            case _Blink.WAIT:
                if time.time() > self._blink_time:
                    return _Blink.TRIBORD

        return blink_state
