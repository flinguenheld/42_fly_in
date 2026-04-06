from visualiser.theme import Theme
import time
import random
import asyncio

from textual.color import Color
from textual.widgets import Label
from textual_canvas import Canvas

from point import Point
from itertools import cycle, pairwise


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀▄░█▀▄░█▀█░█▀█░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█░█░█▀▄░█░█░█░█░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀░░▀░▀░▀▀▀░▀░▀░▀▀▀
class TDrone(Canvas):
    def __init__(self):
        super().__init__(3, 4)
        self.up_colours()

        # --
        self._blink_time = time.time()
        self._blink_state = 0

    def on_mount(self) -> None:
        asyncio.create_task(self._turn())

    # ########################################################################
    # ######################################################## UP COLOURS ####
    def up_colours(self):
        self._colour_drone: Color = Theme.primary
        self._colour_light: Color = Theme.success

        self.clear(Theme.background)
        self.set_pixel(1, 1, color=self._colour_drone)

    # ########################################################################
    # ############################################################## TURN ####
    async def _turn(self):

        points = [
            (Point(0, 0), Point(2, 2)),
            (Point(0, 1), Point(2, 1)),
            (Point(0, 2), Point(2, 0)),
            (Point(1, 2), Point(1, 0)),
            (Point(2, 2), Point(0, 0)),
            (Point(2, 1), Point(0, 1)),
            (Point(2, 0), Point(0, 2)),
            (Point(1, 0), Point(1, 2)),
        ]

        change_speed = 100

        for (a, b), (a2, b2) in pairwise(cycle(points)):
            change_speed += 1
            if change_speed >= 100:
                speed = random.randint(4, 8) / 100
                change_speed = 0

            self.clear_pixel(a.x, a.y)
            self.clear_pixel(b.x, b.y)

            self.set_pixel(a2.x, a2.y, color=self._colour_drone)
            self.set_pixel(b2.x, b2.y, color=self._colour_drone)

            self._blink()

            await asyncio.sleep(speed)

    # ########################################################################
    # ############################################################# BLINK ####
    def _blink(self) -> None:
        if time.time() >= self._blink_time:
            match self._blink_state:
                case 0 | 2 | 4:
                    self.set_pixel(1, 1, color=self._colour_light)
                    self._blink_time = time.time() + 0.3
                case 1 | 3:
                    self.set_pixel(1, 1, color=self._colour_drone)
                    self._blink_time = time.time() + 0.2
                case 5:
                    self.set_pixel(1, 1, color=self._colour_drone)
                    self._blink_time = time.time() + random.randint(8, 20)
                    self._blink_state = -1

            self._blink_state += 1


# TODO: DELETE ###############################################################
# TODO: DELETE ###############################################################
# TODO: DELETE ###############################################################
class TDrone2(Label):
    def __init__(self):
        super().__init__("dro", classes="drones")

    def on_mount(self) -> None:
        asyncio.create_task(self._turns())

    async def _turns(self):

        txt = [
            "▄▄▄\n  \0",
            "▀▄ \n  ▀",
            " █ \n ▀\0",
            " ▄▀\n▀ \0",
        ]

        for current in cycle(txt):
            self.update(current)
            await asyncio.sleep(0.05)
