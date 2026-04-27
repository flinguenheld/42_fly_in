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
class Map:
    def __init__(self, creator: MapCreator):
        """Raise ErrorFly if map_creator is invalid"""

        creator.is_valid()

        self.name: str = creator.name
        self.graph: dict[Hub, set[Edge]] = creator.graph
        self.drones: List[str] = [f"D{i}" for i in range(creator.nb_drones)]

        self.table: TurnTable = self._create_table()

    # ########################################################################
    # ###################################################### CREATE TABLE ####
    def _create_table(self) -> TurnTable:
        # 1 - Get all paths
        dfs = DFS(self.graph, self.start, self.end)
        self.paths = dfs.run()

        # 2 - Create table
        return TurnTable(self.graph, self.paths, self.drones)

    # ########################################################################
    # ############################################################## HUBS ####
    @property
    def hubs(self) -> KeysView:
        return self.graph.keys()

    @property
    def start(self) -> Hub:
        return self._get_hub(lambda h: h.type, Hub.Type.START)

    @property
    def end(self) -> Hub:
        return self._get_hub(lambda h: h.type, Hub.Type.END)

    # #################################################### GET HUB ####
    def _get_hub(self, what: Callable, value: Any) -> Hub:
        return next((h for h in self.graph.keys() if what(h) == value))

    # ########################################################################
    # ################################################### GET CONNECTIONS ####
    def get_edges(self) -> Iterator[Tuple[Hub, Hub, int]]:
        for hub, edges in self.graph.items():
            for edge in edges:
                yield (hub, edge.hub_to, edge.restriction)


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▄█░█▀█░█▀█░░░█▀▀░█▀▄░█▀▀░█▀█░▀█▀░█▀█░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀█░█▀▀░░░█░░░█▀▄░█▀▀░█▀█░░█░░█░█░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░▀░▀░▀░▀░░░░░▀▀▀░▀░▀░▀▀▀░▀░▀░░▀░░▀▀▀░▀░▀░░
@dataclass
class MapCreator:
    name: str
    nb_drones: int = 1
    graph: Dict[Hub, Set[Edge]] = field(default_factory=dict)

    # ########################################################################
    # ######################################################## VALIDATION ####
    @ErrorFlyIn.spread(title="Map validation")
    def is_valid(self) -> None:
        if self.nb_drones < 1:
            raise ErrorFlyIn("Nb drones cannot be less than 1")

        if self._get_hub(lambda h: h.type, Hub.Type.START) is None:
            raise ErrorFlyIn("Map needs at least one starting hub")

        if self._get_hub(lambda h: h.type, Hub.Type.END) is None:
            raise ErrorFlyIn("Map needs at least one ending hub")

    # ########################################################################
    # ############################################################## HUBS ####
    def _get_hub(self, what: Callable, value: Any) -> Hub | None:
        return next((h for h in self.graph.keys() if what(h) == value), None)

    # ######################################################### += ####
    @ErrorFlyIn.spread(title="Add hub in map")
    def __iadd__(self, new_hub: Hub) -> MapCreator:
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
