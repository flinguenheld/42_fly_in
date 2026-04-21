from models.edge import Edge
from models.hub import Hub
import time
import random
import asyncio
from typing import override
from itertools import pairwise
from dataclasses import dataclass

from models.map import Drone
from models.point import Point
from visualiser.ftheme import FTheme
from visualiser.animation import Anim

from textual_canvas import Canvas


@dataclass
class _Coordinate:
    """Local class only used to draw with animation"""

    left: Point
    right: Point
    light: str = ""


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀▄░█▀▄░█▀█░█▀█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█░█░█▀▄░█░█░█░█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀░░▀░▀░▀▀▀░▀░▀░▀▀▀░░
class TDrone(Canvas, Anim):
    WIDTH = 3
    HEIGHT = 4

    _points = [
        _Coordinate(Point(3, 0), Point(1, 2)),
        _Coordinate(Point(2, 0), Point(2, 2), "babord"),
        _Coordinate(Point(1, 0), Point(3, 2), "babord"),
        _Coordinate(Point(1, 1), Point(3, 1), "babord"),
        _Coordinate(Point(1, 2), Point(3, 0)),
        _Coordinate(Point(2, 2), Point(2, 0), "tribord"),
        _Coordinate(Point(3, 2), Point(1, 0), "tribord"),
        _Coordinate(Point(3, 1), Point(1, 1), "tribord"),
        _Coordinate(Point(3, 0), Point(1, 2)),
    ]

    def __init__(self, drone: Drone) -> None:
        Canvas.__init__(self, 3, 4)
        Anim.__init__(self)
        self.up_colours()

        self._blink_time = time.time()
        self._blink_on = True
        self._speed = 0.1

        # Associate a model with the visual and init a random position --
        self._drone = drone
        self.styles.offset = (random.randint(-5, 40), random.randint(-5, 40))

        # Not init for the first fly
        self._where: Hub | Edge

    # ########################################################################
    # ############################################################### FLY ####
    async def fly_to_new_position(self) -> None:
        """If the drone has moved, fly !"""

        self.styles.display = "block"

        if not hasattr(self, "_where") or self._drone.where != self._where:
            destination = self._drone.where.point.visual

            # Get all points in the line --
            for position in self._current_offset().line_points(destination):
                self.styles.offset = (
                    position.x - (TDrone.WIDTH // 2),
                    position.y - (TDrone.HEIGHT),
                )
                await asyncio.sleep(0.04)

            self._where = self._drone.where

    # ########################################################################
    # #################################################### CURRENT OFFSET ####
    def _current_offset(self) -> Point:
        return Point(
            self.offset.y + (TDrone.HEIGHT),
            self.offset.x + (TDrone.WIDTH // 2),
        )

    # ########################################################################
    # ######################################################## UP COLOURS ####
    def up_colours(self) -> None:
        self.clear(FTheme.background)
        self.set_pixel(1, 2, FTheme.primary)

    # ###########################################################
    # ###############################################################
    # ####################################################################
    # ######################################################### ANIMATION ####

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
