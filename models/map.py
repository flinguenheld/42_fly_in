from __future__ import annotations
from models.edge import Edge
from dataclasses import dataclass, field

# from algo.bfs import BFS
from algo.dijkstra import Dijkstra
from models.hub import Hub
from error import ErrorFlyIn
from models.drone import Drone

from typing import Dict, Set, Any, Callable, Tuple, Iterator, KeysView, List


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

    def next_turn(self) -> Any:

        if self.start and self.end:
            turn_txt = ""

            while not all(d.where == self.end for d in self.drones):
                for drone in (d for d in self.drones if d.where != self.end):
                    # ACTION FOR EACH DRONES !
                    algo = Dijkstra(self.graph, self.end)
                    best_path = algo.run(drone.where)
                    drone.where = best_path[1]
                    turn_txt += f" {drone}"

                yield turn_txt.lstrip()

        # if self.start and self.end:
        #     algo = BFS(self.graph, self.end)
        #     aaaa = algo.run(self.start)
        #     return aaaa

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
