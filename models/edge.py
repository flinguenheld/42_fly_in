from __future__ import annotations

from dataclasses import dataclass
from models.hub import Hub


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀▄░█▀▀░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█░█░█░█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀▀░░▀▀▀░▀▀▀░░
@dataclass(frozen=True, unsafe_hash=True)
class Edge:
    hub_to: Hub
    restriction: int
    name: str

    @staticmethod
    def new(hub_from: Hub, hub_to: Hub, restriction: int) -> Edge:

        return Edge(
            hub_to=hub_to,
            restriction=restriction,
            name=f"{hub_from.name}-{hub_to.name}",
        )
