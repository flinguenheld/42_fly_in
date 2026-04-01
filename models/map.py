from error import ErrorFlyIn
from typing import List
from models.hub import Hub


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▄█░█▀█░█▀█
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀█░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░▀░▀░▀░▀░░
class Map:
    def __init__(self, name: str = "No name") -> None:
        self._name = name
        self._nb_drones = 0
        self._hubs: List[Hub] = []

    # ########################################################################
    # ############################################################## HUBS ####
    @property
    def hubs(self) -> List[Hub]:
        return self._hubs

    @hubs.setter
    def hubs(self, hub: Hub) -> None:
        """
        Add the hub inside the map

        Raise ErrorMap if name or point already exist in the map
        """
        if any(h.name == hub.name for h in self._hubs):
            raise ErrorMap(f"{hub.name} already exists in the map.")

        if any(h.point == hub.point for h in self._hubs):
            raise ErrorMap(f"There is already a hub at {hub.point}.")

        self._hubs.append(hub)

    # ########################################################################
    # ######################################################### NB DRONES ####
    @property
    def nb_drones(self) -> int:
        return self._nb_drones

    @nb_drones.setter
    def nb_drones(self, nb: int) -> None:
        if nb < 1:
            raise ErrorMap("Nb drones cannot be less than 1")

        self._nb_drones = nb

    # ########################################################################
    # ############################################################### STR ####
    def __str__(self) -> str:
        return (
            f"Map: {self._name} - {self.nb_drones} "
            f"{'\n'.join((str(h) for h in self._hubs))}"
        )


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀▄░█▀▄░█▀█░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀▄░█▀▄░█░█░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░▀░▀░▀░▀▀▀░▀░▀
class ErrorMap(ErrorFlyIn):
    def __init__(self, message: str) -> None:
        super().__init__(f"Map error:\n{message}")
