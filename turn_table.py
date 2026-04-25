from __future__ import annotations
from dataclasses import dataclass

from models.hub import Hub
from models.edge import Edge
from models.drone import Drone

from typing import Dict, Set, Iterator, List


@dataclass
class TurnTable:
    graph: Dict[Hub, Set[Edge]]
    paths: List[List[Edge]]
    drones: List[Drone]

    def __post_init__(self):
        self.table: Dict[str, Dict[int, Edge]] = dict()

    def run(self) -> Dict[str, Dict[int, Edge]]:

        for drone in self.drones:
            self.table[drone.name] = self._get_shortest_path()

        return self.table

    def edges_on(self, turn: int) -> Iterator[Edge]:
        for drone, edges in self.table.items():
            if turn in edges:
                yield edges[turn]

    def _get_shortest_path(self):

        def is_edge_available(edge: Edge, turn: int) -> bool:
            amount_on_edge = sum(1 for e in self.edges_on(turn) if e == edge)
            amount_on_hub = sum(
                1 for e in self.edges_on(turn) if e.hub_to == edge.hub_to
            )

            return amount_on_edge < edge.restriction and (
                edge.hub_to.type != Hub.Type.REGULAR
                or amount_on_hub < edge.hub_to.max_drones
            )

        def are_edges_available(edge: Edge, turn: int) -> bool:

            amount_on_edge = sum(1 for e in self.edges_on(turn) if e == edge)

            return amount_on_edge < edge.restriction and is_edge_available(
                edge, turn + 1
            )

        def choose_earliest(current: Dict[int, Edge], temp: Dict[int, Edge]):

            if not temp:
                return current

            temp_max = max(temp.keys())
            current_max = max(current.keys())

            if current_max < temp_max:
                return current

            if current_max == temp_max:
                current_priority = sum(
                    1
                    for pr in current.values()
                    if pr.hub_to.zone == Hub.Zone.PRIORITY
                )
                temp_priority = sum(
                    1
                    for pr in temp.values()
                    if pr.hub_to.zone == Hub.Zone.PRIORITY
                )

                if current_priority > temp_priority:
                    return current

            return temp

        temp: Dict[int, Edge] = dict()

        for path in self.paths:
            turn: int = 0
            current_line: Dict[int, Edge] = dict()

            for edge in path:
                while True:
                    turn += 1

                    if edge.hub_to.zone == Hub.Zone.RESTRICTED:
                        if are_edges_available(edge, turn):
                            current_line[turn + 1] = edge
                            current_line[turn] = edge
                            turn += 1
                            break

                    else:
                        if is_edge_available(edge, turn):
                            current_line[turn] = edge
                            break

            if not temp or max(current_line.keys()) <= max(temp.keys()):
                temp = current_line

        return temp
