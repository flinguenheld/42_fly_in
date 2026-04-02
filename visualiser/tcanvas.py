from typing import override
import asyncio

from point import Point
from models.hub import Hub
from models.map import Map
from textual_canvas import Canvas


class TCanvas(Canvas):
    _SHIFT: int = 50
    _SCALE: int = 20
    _RADIUS: int = 2

    def __init__(self) -> None:
        super().__init__(width=200, height=200)
        # self._shift: Point = Point(5, 5)

    # def draw_circle(self)

    async def draw_hubs(self, map: Map):
        start = map.start
        if start:
            self.notify(f"here: {start.next_nodes}")
        else:
            self.notify("NO START !!!!!!!")

        for hub_from, hub_to in map.get_connections():
            # self.notify(f"hub: {hub.point}")
            self._draw_circle(hub_from.point)
            await asyncio.sleep(0.1)
            self._draw_circle(hub_to.point)
            await asyncio.sleep(0.1)
            self._draw_line(hub_from.point, hub_to.point)
            await asyncio.sleep(0.3)

    def _adapt_point(self, point: Point) -> Point:
        return point * TCanvas._SCALE + TCanvas._SHIFT

    def _draw_circle(self, center: Point, color=None) -> None:
        point = self._adapt_point(center)

        super().draw_circle(point.x, point.y, TCanvas._RADIUS, color)

    def _draw_line(self, pt_from: Point, pt_to: Point, color=None) -> None:
        fr = self._adapt_point(pt_from)
        to = self._adapt_point(pt_to)

        super().draw_line(fr.x, fr.y, to.x, to.y, color)
