from __future__ import annotations
from models.edge import Edge
from models.hub import Hub
from dataclasses import dataclass
# from models.map import Edge

# from models.hub import Hub


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▄░█▀▄░█▀█░█▀█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▄░█░█░█░█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀░░▀░▀░▀▀▀░▀░▀░▀▀▀░░
@dataclass
class Drone:
    name: str
    where: Hub | Edge

    def __str__(self) -> str:
        return f"{self.name}-{self.where.name}"
