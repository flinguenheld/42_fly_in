from models.map import Edge
from models.hub import Hub
from typing import Dict, Set
from dataclasses import dataclass


@dataclass
class Dijkstra:
    graph: Dict[Hub, Set[Edge]]
    start: Hub
