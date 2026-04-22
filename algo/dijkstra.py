from models.drone import Drone
import math
from collections import deque
from typing import Dict, Set, Deque, List, Tuple

from models.hub import Hub
from models.map import Edge
from dataclasses import dataclass


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▄░▀█▀░▀▀█░█░█░█▀▀░▀█▀░█▀▄░█▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░░█░░░░█░█▀▄░▀▀█░░█░░█▀▄░█▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀░░▀▀▀░▀▀░░▀░▀░▀▀▀░░▀░░▀░▀░▀░▀░░
@dataclass
class Dijkstra:
    graph: Dict[Hub, Set[Edge]]
    end: Hub
    drones: List[Drone]
    # edge_used:

    def run(self, start: Hub) -> List[Edge]:

        adated_graph = self.adapt_graph()
        temp: Dict[Hub, float] = self.init_temp_graph(start)
        done: Set[Hub] = set()

        # TODO: GET A WAY TO MANAGE ADAPTED GRAPH WITHOUT SOLUTION !!!!

        while True:
            current_hub = self.get_lowest(temp, done)
            done.add(current_hub)

            if current_hub == self.end:
                break

            for edge in adated_graph[current_hub]:
                # CHECK IF THE DESTINATION IS AVAILABLE OR NOT !

                # CANNOT BE DONE HERE -----------------------------------
                # HAVE TO ADAPT THE GRAPH -------------------------------
                # Is edge already occupied ??
                # on_edge = sum(1 for d in self.drones if d.where == edge)
                # if on_edge >= edge.restriction:
                #     continue

                # # Are there still room in the hub ??
                # on_hub = sum(1 for d in self.drones if d.where == edge.hub_to)
                # if on_hub >= edge.hub_to.max_drones:
                #     continue

                if edge.hub_to not in done:
                    cost = temp[current_hub] + edge.hub_to.zone.value
                    if cost < temp[edge.hub_to]:
                        temp[edge.hub_to] = cost

        return self.get_path(temp, start)

    def get_lowest(self, temp: Dict[Hub, float], done: Set[Hub]) -> Hub:
        """
        Get the current less expensive Hub in temp
        """

        return min(
            (e for e in temp.items() if e[0] not in done),
            key=lambda pair: pair[1],
        )[0]

    def adapt_graph(self) -> Dict[Hub, Set[Edge]]:

        # Nodes to remove ?
        hubs_full = [
            hub
            for hub in self.graph.keys()
            if sum(1 for d in self.drones if d.where == hub) >= hub.max_drones
        ]

        # Edges to remove ?
        edges_full = [
            d.where for d in self.drones if isinstance(d.where, Edge)
        ]

        # Create the new one !!!
        new_graph = {}
        for hub, edges in self.graph.items():
            # if hub not in hubs_full:
            new_graph[hub] = set(
                [
                    e
                    for e in edges
                    if e not in edges_full and e.hub_to not in hubs_full
                ]
            )

        return new_graph

    def init_temp_graph(self, start: Hub) -> Dict[Hub, float]:
        """
        Create a dict with all hubs and their 'cost' set to infinite
        The cost will be the smallest price requiered to reach the hub
        """

        temp = {hub: math.inf for hub in self.graph.keys()}
        temp[start] = 0.0
        return temp

    def get_path(self, temp: Dict[Hub, float], start: Hub) -> List[Edge]:
        """
        Run in temp to get the final path
        """

        # Start from the end
        # path: Deque[Hub] = deque([self.end])
        edges: Deque[Edge] = deque()

        current = self.end
        while current != start:
            # Get all hub which have the current hub as destination
            sources: List[Hub] = [
                h
                for h, edges in self.graph.items()
                if any(True for e in edges if current == e.hub_to)
            ]

            # Then keep the cheapest
            source = min(sources, key=lambda h: temp[h])

            # Save the used edge
            ed = next(e for e in self.graph[source] if e.hub_to == current)
            edges.appendleft(ed)
            current = source

        return [e for e in edges]
