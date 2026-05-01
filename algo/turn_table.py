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

    def __post_init__(self) -> None:
        for drone in self.drones:
            self.table[drone] = self._get_shortest_path()

    # ########################################################################
    # #################################################### DRONE ITERATOR ####
    def drone_iterator(self, drone: str) -> Iterator[Edge | None]:
        for i in range(1, self.nb_turns + 1):
            if i in self.table[drone]:
                yield self.table[drone][i]
            else:
                yield None

    # ########################################################################
    # ########################################################## GET TURN ####
    def get_turn(
        self,
        turn: int,
        with_duplicates: bool = True,
    ) -> Dict[str, Edge]:
        """
        Get drones and their position at the given turn

           |  1  |  2  |  3  |  4  |  5  |
        ---|-----|-----|-----|-----|-----|
        D1 | A/B |     | B/C |     |     |
        D2 |     | A/B |     | B/C |     |
        D3 |     |     | A/B |     | B/C |
        D4 |     |     |     | A/B |     |

        If with duplicates is True:

           |  1  |  2  |  3  |  4  |  5  |
        ---|-----|-----|-----|-----|-----|
        D1 | A/B | A/B | B/C |     |     |
        D2 |     | A/B | A/B | B/C |     |
        D3 |     |     | A/B | A/B | B/C |
        D4 |     |     |     | A/B | A/B |

        """

        positions: Dict[str, Edge] = dict()

        if turn <= 0:
            return {}

        for drone, edges in self.table.items():
            if turn in edges:
                if with_duplicates or not (
                    turn - 1 in self.table[drone]
                    and self.table[drone][turn - 1] == edges[turn]
                ):
                    positions[drone] = edges[turn]

        return positions

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
    # ################################################# GET SHORTEST PATH ####
    def _get_shortest_path(self) -> Dict[int, Edge]:

        # #######################################################
        # #################################### EDGES ON TURN ####
        def edges_on_turn(turn: int) -> Iterator[Edge]:

            for drone, edges in self.table.items():
                if turn in edges:
                    yield edges[turn]

        # #######################################################
        # ################################ IS EDGE AVAILABLE ####
        def is_edge_available(edge: Edge, turn: int) -> bool:
            amount_on_edge = sum(1 for e in edges_on_turn(turn) if e == edge)
            amount_on_hub = sum(
                1 for e in edges_on_turn(turn) if e.hub_to == edge.hub_to
            )

            return amount_on_edge < edge.restriction and (
                edge.hub_to.type != Hub.Type.REGULAR
                or amount_on_hub < edge.hub_to.max_drones
            )

        # #######################################################
        # ############################## ARE EDGES AVAILABLE ####
        def are_edges_available(edge: Edge, turn: int) -> bool:

            amount_on_edge = sum(1 for e in edges_on_turn(turn) if e == edge)

            return amount_on_edge < edge.restriction and is_edge_available(
                edge, turn + 1
            )

        # #######################################################
        # ################################## CHOOSE EARLIEST ####
        def choose_earliest(
            current: Dict[int, Edge],
            temp: Dict[int, Edge],
        ) -> Dict[int, Edge]:

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

            keep_last_edge: Edge | None = None

            for edge in path:
                while True:
                    turn += 1

                    if edge.hub_to.zone == Hub.Zone.RESTRICTED:
                        if are_edges_available(edge, turn):
                            current_line[turn] = edge.copy_first_true()
                            current_line[turn + 1] = edge
                            keep_last_edge = edge
                            turn += 1
                            break

                    else:
                        if is_edge_available(edge, turn):
                            current_line[turn] = edge
                            keep_last_edge = edge
                            break

                    if keep_last_edge:
                        current_line[turn] = keep_last_edge

            temp = choose_earliest(current_line, temp)

        return temp
