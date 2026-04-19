from collections import deque
from dataclasses import dataclass
from typing import Dict, Set, Deque, List

from models.map import Edge
from models.hub import Hub


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▄░█▀▀░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▄░█▀▀░▀▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀░░▀░░░▀▀▀░░
@dataclass
class BFS:
    graph: Dict[Hub, Set[Edge]]
    end: Hub

    # ########################################################################
    # ############################################################### RUN ####
    def run(self, start: Hub) -> List[Hub]:

        search_queue: Deque[Hub] = deque([start])
        add_queue = search_queue.append

        # Start to start will be skipped by _reverse_path
        parents: Dict[Hub, Hub] = {start: start}

        while search_queue:
            hub = search_queue.popleft()

            if hub == self.end:
                return self._reverse_path(start, parents)

            else:
                for edge in self.graph[hub]:
                    if edge.hub_to not in parents:
                        parents[edge.hub_to] = hub
                        add_queue(edge.hub_to)

        return []

    # ########################################################################
    # ###################################################### REVERSE PATH ####
    def _reverse_path(self, start: Hub, path: Dict[Hub, Hub]) -> List[Hub]:
        reversed = deque([self.end])
        while reversed[0] != start:
            reversed.appendleft(path[reversed[0]])

        return [h for h in reversed]
