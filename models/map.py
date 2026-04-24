from __future__ import annotations
from dataclasses import dataclass, field

# from algo.bfs import BFS
from algo.dfs import DFS
from models.hub import Hub
from models.edge import Edge
from error import ErrorFlyIn
from models.drone import Drone

from typing import Dict, Set, Any, Callable, Tuple, Iterator, KeysView, List


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

    def _get_shortest_path(self):

        def edges_on_turn(turn: int) -> Iterator[Edge]:
            for drone, edges in self.table.items():
                if turn in edges:
                    yield edges[turn]

        def is_edge_available(edge: Edge, turn: int) -> bool:
            # return True
            # TODO: TAKE CARE OF RESTRICTED
            amount_on_edge = sum(1 for e in edges_on_turn(turn) if e == edge)
            amount_on_hub = sum(
                1 for e in edges_on_turn(turn) if e.hub_to == edge.hub_to
            )

            return (
                amount_on_edge < edge.restriction
                and amount_on_hub < edge.hub_to.max_drones
            )

        temp: Dict[int, Edge] = dict()

        for path in self.paths:
            new_line: Dict[int, Edge] = dict()

            turn: int = 0
            for edge in path:
                while True:
                    turn += 1

                    if is_edge_available(edge, turn):
                        new_line[turn] = edge
                        break

            if not temp or max(new_line.keys()) <= max(temp.keys()):
                temp = new_line

        return temp


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▄█░█▀█░█▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░▀░▀░▀░▀░░░░
@dataclass
class Map:
    name: str
    nb_drones: int = 1
    drones: List[Drone] = field(default_factory=list)
    graph: Dict[Hub, Set[Edge]] = field(default_factory=dict)

    line: str = ""

    def OK_TEST_PATHS(self) -> List[List[Edge]] | None:
        if self.start and self.end:
            dfs = DFS(self.graph, self.start, self.end)
            return dfs.run()
        return None

    def OK_TEST_TABLE(self):
        if self.start and self.end:
            dfs = DFS(self.graph, self.start, self.end)
            paths = dfs.run()

            table_creation = TurnTable(self.graph, paths, self.drones)
            return table_creation.run()

    # ########################################################################
    # ######################################################## VALIDATION ####
    @ErrorFlyIn.spread(title="Map validation")
    def is_valid(self) -> None:
        if self.nb_drones < 1:
            raise ErrorFlyIn("Nb drones cannot be less than 1")

        if self.start is None:
            raise ErrorFlyIn("Map needs at least one starting hub")

        if self.end is None:
            raise ErrorFlyIn("Map needs at least one ending hub")

        self.drones = [
            Drone(f"D{i + 1}", self.start)
            for i, _ in enumerate(range(self.nb_drones))
        ]

    # ########################################################################
    # ######################################################## GET DRONES ####
    def get_drones(self) -> Iterator[Drone]:
        for d in self.drones:
            yield d

    # ########################################################################
    # ################################################### GET CONNECTIONS ####
    def get_edges(self) -> Iterator[Tuple[Hub, Hub, int]]:
        for hub, edges in self.graph.items():
            for edge in edges:
                yield (hub, edge.hub_to, edge.restriction)

    # ########################################################################
    # ############################################################## HUBS ####
    @property
    def hubs(self) -> KeysView:
        return self.graph.keys()

    @property
    def start(self) -> Hub | None:
        return self._get_hub(lambda h: h.type, Hub.Type.START)

    @property
    def end(self) -> Hub | None:
        return self._get_hub(lambda h: h.type, Hub.Type.END)

    # #################################################### GET HUB ####
    def _get_hub(self, what: Callable, value: Any) -> Hub | None:
        return next((h for h in self.graph.keys() if what(h) == value), None)

    # ######################################################### += ####
    @ErrorFlyIn.spread(title="Add hub in map")
    def __iadd__(self, new_hub: Hub) -> Map:
        """
        Add the hub inside the graph

        Raise ErrorFlyIn if name or point already exist in the map
        """
        if self._get_hub(lambda h: h.name, new_hub.name):
            raise ErrorFlyIn(f"{new_hub.name} already exists in the map.")

        if self._get_hub(lambda h: h.point, new_hub.point):
            raise ErrorFlyIn(f"There is already a hub at {new_hub.point}.")

        if new_hub.type != Hub.Type.REGULAR and any(
            h.type == new_hub.type for h in self.graph.keys()
        ):
            raise ErrorFlyIn(f"There is already a {new_hub.type} in the map.")

        self.graph[new_hub] = set()
        return self

    # #################################################### CONNECT ####
    @ErrorFlyIn.spread(title="Connect two hubs")
    def connect_hubs(
        self, from_name: str, to_name: str, max_link_capacity: int
    ) -> None:

        if from_name == to_name:
            raise ErrorFlyIn(f"Cannot connect hub '{to_name}' with itself.")

        if max_link_capacity < 1:
            raise ErrorFlyIn("Max link capacity has to be at least 1.")

        hub_from = self._get_hub(lambda h: h.name, from_name)
        hub_to = self._get_hub(lambda h: h.name, to_name)

        # raise ErrorFlyIn(f"{from_name}->{self.graph}")

        if hub_from is None:
            raise ErrorFlyIn(f"Hub '{from_name}' doesn't exist in the map.")

        if hub_to is None:
            raise ErrorFlyIn(f"Hub '{to_name}' doesn't exist in the map.")

        self.graph[hub_from].add(Edge.new(hub_from, hub_to, max_link_capacity))

    # ########################################################################
    # ############################################################### STR ####
    def __str__(self) -> str:
        return (
            f"Map: {self.name}\nNb drones: {self.nb_drones}\n"
            # f"Hubs ({len(self._hubs)}):\n"
            # f"{'\n'.join((str(h) for h in self._hubs))}"
        )
