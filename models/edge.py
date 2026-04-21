from __future__ import annotations

from dataclasses import dataclass, field
from models.point import Point
from models.hub import Hub


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀▄░█▀▀░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█░█░█░█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀▀░░▀▀▀░▀▀▀░░
@dataclass(frozen=True, unsafe_hash=True)
class Edge:
    hub_to: Hub = field(hash=True)
    restriction: int = field(hash=True)
    point: Point = field(hash=True)
    name: str

    @staticmethod
    def new(hub_from: Hub, hub_to: Hub, restriction: int) -> Edge:
        pts = [p for p in hub_from.point.line_points(hub_to.point)]

        return Edge(
            hub_to=hub_to,
            restriction=restriction,
            point=pts[len(pts) // 2],
            name=f"{hub_from.name}-{hub_to.name}",
        )
