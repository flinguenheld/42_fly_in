import math
from collections import deque
from typing import Dict, Set, Deque, List

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

    def run(self, start: Hub) -> List[Hub]:

        temp: Dict[Hub, float] = self.init_temp_graph(start)
        done: Set[Hub] = set()

        while True:
            current = self.get_lowest(temp, done)
            done.add(current)

            if current == self.end:
                break

            for edge in self.graph[current]:
                if edge.hub_to not in done:
                    cost = temp[current] + edge.hub_to.zone.value
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

    def init_temp_graph(self, start: Hub) -> Dict[Hub, float]:
        """
        Create a dict with all hubs and their 'cost' set to infinite
        The cost is the smallerst price requiered to reach the hub
        """

        temp = {hub: math.inf for hub in self.graph.keys()}
        temp[start] = 0.0
        return temp

    def get_path(self, temp: Dict[Hub, float], start: Hub) -> List[Hub]:
        """
        Run in temp to get the final path
        """

        # Start form the end
        path: Deque[Hub] = deque([self.end])

        while path[0] != start:
            # Get all hub which have the current hub as destination
            sources: List[Hub] = [
                h
                for h, edges in self.graph.items()
                if any(True for e in edges if path[0] == e.hub_to)
            ]

            # Then keep the cheapest
            path.appendleft(min(sources, key=lambda h: temp[h]))

        return [h for h in path]
