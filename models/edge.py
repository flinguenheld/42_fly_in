from __future__ import annotations

from dataclasses import dataclass
from models.hub import Hub


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀▄░█▀▀░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█░█░█░█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀▀░░▀▀▀░▀▀▀░░
@dataclass(frozen=True, unsafe_hash=True)
class Edge:
    hub_from: Hub
    hub_to: Hub
    restriction: int
    name: str
    first_on_restricted_zone: bool

    @staticmethod
    def new(hub_from: Hub, hub_to: Hub, restriction: int) -> Edge:

        return Edge(
            hub_from=hub_from,
            hub_to=hub_to,
            restriction=restriction,
            name=f"{hub_from.name}-{hub_to.name}",
            first_on_restricted_zone=False,
        )

    def copy_first_true(original: Edge) -> Edge:
        return Edge(
            hub_from=original.hub_from,
            hub_to=original.hub_to,
            restriction=original.restriction,
            name=original.name,
            first_on_restricted_zone=True,
        )
