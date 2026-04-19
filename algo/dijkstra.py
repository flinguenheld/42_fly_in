import math

from models.hub import Hub
from models.map import Edge
from typing import Dict, Set
from dataclasses import dataclass


@dataclass
class Dijkstra:
    graph: Dict[Hub, Set[Edge]]
    start: Hub

    def run(self, start: Hub):

        # new_graph = self.create_graph_with_costs()

        costs = {h: math.inf for h in self.graph.keys()}
        parents = {start: start}

    def create_graph_with_costs(self) -> Dict[Hub, Dict[Hub, int]]:

        new_graph: Dict[Hub, Dict[Hub, int]] = dict()

        for hub, edges in self.graph.items():
            destinations = {}
            for edge in edges:
                match edge.hub_to.zone:
                    case Hub.Zone.BLOCKED:
                        destinations[edge.hub_to] = math.inf
                    case Hub.Zone.RESTRICTED:
                        destinations[edge.hub_to] = 2
                    case _:
                        destinations[edge.hub_to] = 1

            new_graph[hub] = destinations

        return new_graph
