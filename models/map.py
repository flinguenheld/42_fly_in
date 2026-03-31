from typing import List
from models.hub import Hub


class Map:
    def __init__(self, name: str = "No name"):
        self._name = name
        self._nb_drones = 0
        self._hubs: List[Hub] = []

    def add_hub(self, hub: Hub):
        # TODO: Check if there is already a hub with this name
        self._hubs.append(hub)

    @property
    def hubs(self):
        return self._hubs

    @property
    def nb_drones(self):
        return self._nb_drones

    @nb_drones.setter
    def nb_drones(self, nb: int):
        if nb <= 0:
            raise ValueError("Map: nb drones cannot be <= 0")
        self._nb_drones = nb

    def __str__(self):
        return f"Map: {self._name} - {self.nb_drones} - {self._hubs}"
