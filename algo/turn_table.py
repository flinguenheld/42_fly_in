from __future__ import annotations
from itertools import chain
from dataclasses import dataclass, field

from models.hub import Hub
from models.edge import Edge

from typing import Dict, Set, Iterator, List


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█░█░█▀▄░█▀█░░░▀█▀░█▀█░█▀▄░█░░░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█░█░█▀▄░█░█░░░░█░░█▀█░█▀▄░█░░░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀░▀░▀░▀░░░░▀░░▀░▀░▀▀░░▀▀▀░▀▀▀░░
@dataclass
class TurnTable:
    graph: Dict[Hub, Set[Edge]]
    paths: List[List[Edge]]
    drones: List[str]
    table: Dict[str, Dict[int, Edge]] = field(default_factory=dict)

    def __post_init__(self):
        for drone in self.drones:
            self.table[drone] = self._get_shortest_path()

    # ########################################################################
    # ######################################################### ITERATORS ####
    def turn_iterator(self) -> Iterator[Dict[str, Hub | Edge]]:

        for turn in range(1, self.nb_turns + 1):
            to_yield: Dict[str, Hub | Edge] = {}

            for drone, positions in self.table.items():
                if turn in positions:
                    # Is in the middle of a restricted area ?
                    if (
                        turn + 1 in positions
                        and positions[turn] == positions[turn + 1]
                    ):
                        to_yield[drone] = positions[turn]
                    else:
                        to_yield[drone] = positions[turn].hub_to

            yield to_yield

    def drone_iterator(self, drone: str) -> Iterator[Edge | None]:
        for i in range(1, self.nb_turns + 1):
            if i in self.table[drone]:
                yield self.table[drone][i]
            else:
                yield None

    def get_turn(self, turn: int, all: bool = False) -> Dict[str, Hub | Edge]:
        blah: Dict[str, Hub | Edge] = dict()

        for drone, edges in self.table.items():
            if turn in edges:
                # Is in the middle of a restricted area ?
                if turn + 1 in edges and edges[turn] == edges[turn + 1]:
                    blah[drone] = edges[turn]
                else:
                    blah[drone] = edges[turn].hub_to
            # TODO: CAN'T WORK - FIND ANOTHER WAY !!!!!!!!
            # TODO: CAN'T WORK - FIND ANOTHER WAY !!!!!!!!
            # TODO: CAN'T WORK - FIND ANOTHER WAY !!!!!!!!
            # TODO: CAN'T WORK - FIND ANOTHER WAY !!!!!!!!
            elif all and turn > 1:
                # Get the previous turn which is not None
                prev = turn - 1
                while prev not in edges:
                    prev -= 1

                blah[drone] = edges[turn].hub_to

        return blah

    # ########################################################################
    # ######################################################### ACCESSORS ####
    @property
    def nb_turns(self) -> int:
        return max(k for k in chain.from_iterable(self.table.values()))

    # ##################################################################
    # ####################################################################
    # ######################################################################
    # ############################################################## ALGO ####

    # ########################################################################
    # ########################################################## EDGES ON ####
    def _edges_on(self, turn: int) -> Iterator[Edge]:
        for drone, edges in self.table.items():
            if turn in edges:
                yield edges[turn]

    # ########################################################################
    # ################################################# GET SHORTEST PATH ####
    def _get_shortest_path(self):

        # #######################################################
        # ################################ IS EDGE AVAILABLE ####
        def is_edge_available(edge: Edge, turn: int) -> bool:
            amount_on_edge = sum(1 for e in self._edges_on(turn) if e == edge)
            amount_on_hub = sum(
                1 for e in self._edges_on(turn) if e.hub_to == edge.hub_to
            )

            return amount_on_edge < edge.restriction and (
                edge.hub_to.type != Hub.Type.REGULAR
                or amount_on_hub < edge.hub_to.max_drones
            )

        # #######################################################
        # ############################## ARE EDGES AVAILABLE ####
        def are_edges_available(edge: Edge, turn: int) -> bool:

            amount_on_edge = sum(1 for e in self._edges_on(turn) if e == edge)

            return amount_on_edge < edge.restriction and is_edge_available(
                edge, turn + 1
            )

        # #######################################################
        # ################################## CHOOSE EARLIEST ####
        def choose_earliest(current: Dict[int, Edge], temp: Dict[int, Edge]):

            if not temp:
                return current

            temp_max = max(temp.keys())
            current_max = max(current.keys())

            if current_max < temp_max:
                return current

            # If equals, check which one has more priority zones
            if current_max == temp_max:
                current_priorities = sum(
                    1
                    for pr in current.values()
                    if pr.hub_to.zone == Hub.Zone.PRIORITY
                )
                temp_priorities = sum(
                    1
                    for pr in temp.values()
                    if pr.hub_to.zone == Hub.Zone.PRIORITY
                )

                if current_priorities > temp_priorities:
                    return current

            return temp

        # #######################################################
        # ############################################# ALGO ####
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

            temp = choose_earliest(current_line, temp)

        return temp
