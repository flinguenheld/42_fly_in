from __future__ import annotations
from dataclasses import dataclass, field

from algo.dfs import DFS
from models.hub import Hub
from models.edge import Edge
from error import ErrorFlyIn
from algo.turn_table import TurnTable

from typing import Dict, Set, Any, Callable, Tuple, Iterator, KeysView, List


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▄█░█▀█░█▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░▀░▀░▀░▀░░░░
@dataclass
class Map:
    name: str
    nb_drones: int = 1
    drones: List[str] = field(default_factory=list)
    graph: Dict[Hub, Set[Edge]] = field(default_factory=dict)
    table: TurnTable | None = None

    # current_turn: int = 0

    # ########################################################################
    # ###################################################### CREATE TABLE ####
    def create_table(self) -> None:
        if self.start and self.end:
            # 1 - Get all paths
            dfs = DFS(self.graph, self.start, self.end)
            self.paths = dfs.run()

            # 2 - Create drones
            for i in range(self.nb_drones):
                self.drones.append(f"D{i}")

            # 3 - Create table
            self.table = TurnTable(self.graph, self.paths, self.drones)

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
