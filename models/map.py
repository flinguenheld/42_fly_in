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

        if hub.type != Hub.Type.REGULAR and any(
            h.type == hub.type for h in self._hubs
        ):
            raise ErrorMap(f"There is already a {hub.type} in the map.")

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
    # ############################################################# VALID ####
    @property
    def valid(self) -> bool:
        """
        Perform tests and raise an ErrorMap on any invalid one
        Return True
        """

        if self._nb_drones < 1:
            raise ErrorMap("Map needs at least one drone")

        if not any(h.point == Hub.Type.START for h in self._hubs):
            raise ErrorMap("Map needs at least one starting hub")

        if not any(h.point == Hub.Type.END for h in self._hubs):
            raise ErrorMap("Map needs at least one ending hub")

        if not any(h.point == Hub.Type.REGULAR for h in self._hubs):
            raise ErrorMap("Map needs at least one REGULAR hub")

        return True

    # ########################################################################
    # ############################################################### STR ####
    def __str__(self) -> str:
        return (
            f"Map: {self._name}\n"
            f"Nb drones: {self.nb_drones}\n"
            f"Hubs ({len(self._hubs)}):\n"
            f"{'\n'.join((str(h) for h in self._hubs))}"
        )


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀▄░█▀▄░█▀█░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀▄░█▀▄░█░█░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░▀░▀░▀░▀▀▀░▀░▀
class ErrorMap(ErrorFlyIn):
    def __init__(self, message: str) -> None:
        super().__init__(f"Map error:\n{message}")
