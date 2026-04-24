from __future__ import annotations
from models.edge import Edge
from dataclasses import dataclass

# from algo.bfs import BFS
from models.hub import Hub

from typing import (
    Dict,
    Set,
    List,
)


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▄░█▀▀░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░▀▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀░░▀░░░▀▀▀░░
@dataclass
class DFS:
    graph: Dict[Hub, Set[Edge]]
    start: Hub
    end: Hub

    # ########################################################################
    # ############################################################### RUN ####
    def run(self) -> List[List[Edge]]:

        def dfs(
            next_hub: Hub, current_path: List[Edge], done: Set[Hub]
        ) -> List[List[Edge]]:

            all_paths = []
            if next_hub == self.end:
                return [current_path]

            done.add(next_hub)

            for edge in self.graph[next_hub]:
                if (
                    edge.hub_to not in done
                    and edge.hub_to.zone != Hub.Zone.BLOCKED
                ):
                    new_path = current_path.copy()
                    new_path.append(edge)
                    all_paths.extend(dfs(edge.hub_to, new_path, done.copy()))

            return all_paths

        paths = dfs(self.start, [], set())

        # Sort and take care of restricted zones --
        paths.sort(
            key=lambda path: sum(
                2 if e.hub_to.zone == Hub.Zone.RESTRICTED else 1 for e in path
            )
        )
        return paths
