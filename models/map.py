from __future__ import annotations
from error import ErrorFlyIn
from typing import List, Iterator, Tuple
from models.hub import Hub


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▄█░█▀█░█▀█
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀█░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░▀░▀░▀░▀░░
class Map:
    def __init__(self, name: str = "No name") -> None:
        self._name: str = name
        self._nb_drones: int = 0
        self._hubs: List[Hub] = []

    # ########################################################################
    # ################################################### GET CONNECTIONS ####

    def get_connections(self) -> Iterator[Tuple[Hub, Hub]]:
        for hub in self._hubs:
            for nxt in hub.next_nodes:
                yield (hub, nxt)

    # ################################################ TEST ##################
    # ################################################ TEST ##################
    # ################################################ TEST ##################
    def loop(self, current: Hub | None = None) -> Iterator[Hub]:
        if not current:
            current = self.start

        if current:
            yield current
            for node in current.next_nodes:
                yield node
                yield from self.loop(node)

    # ############################################### START / STOP ####
    # TODO: CHANGE TO ATTRIBUTES ?
    @property
    def start(self) -> Hub | None:
        return next(h for h in self._hubs if h.type == Hub.Type.START)

    @property
    def end(self) -> Hub | None:
        return next(h for h in self._hubs if h.type == Hub.Type.END)

    # ########################################################################
    # ############################################################## HUBS ####
    @property
    def hubs(self) -> List[Hub]:
        return self._hubs

    # ######################################################### += ####
    @ErrorFlyIn.spread(title="Add hub in map")
    def __iadd__(self, hub: Hub) -> Map:
        """
        Add the hub inside the map

        Raise ErrorFlyIn if name or point already exist in the map
        """
        if any(h.name == hub.name for h in self._hubs):
            raise ErrorFlyIn(f"{hub.name} already exists in the map.")

        if any(h.point == hub.point for h in self._hubs):
            raise ErrorFlyIn(f"There is already a hub at {hub.point}.")

        if hub.type != Hub.Type.REGULAR and any(
            h.type == hub.type for h in self._hubs
        ):
            raise ErrorFlyIn(f"There is already a {hub.type} in the map.")

        self._hubs.append(hub)
        return self

    # #################################################### CONNECT ####
    @ErrorFlyIn.spread(title="Connect two hubs")
    def connect_hubs(self, from_name: str, to_name: str) -> None:
        """
        Add 'to' to 'from'

        Raise ErrorFlyIn to or from hubs are not found in the hub list
        """
        hub_from = next((h for h in self._hubs if h.name == from_name), None)
        hub_to = next((h for h in self._hubs if h.name == to_name), None)

        if not hub_from:
            raise ErrorFlyIn(
                f"The hub '{from_name}' doesn't exist in the map.",
                # title="Hub connection",
            )
        if not hub_to:
            raise ErrorFlyIn(
                f"The hub: '{to_name}' doesn't exist in the map.",
                # title="Hub connection",
            )

        hub_from += hub_to

    # ########################################################################
    # ######################################################### NB DRONES ####
    @property
    def nb_drones(self) -> int:
        return self._nb_drones

    # TODO: WHAT IS THAT - CHECK IS ALREADY DONE BELOW ????
    @nb_drones.setter
    @ErrorFlyIn.spread(title="Number of drones")
    def nb_drones(self, nb: int) -> None:
        if nb < 1:
            raise ErrorFlyIn("Nb drones cannot be less than 1")

        self._nb_drones = nb

    # ########################################################################
    # ############################################################# VALID ####
    @property
    @ErrorFlyIn.spread(title="Map validation")
    def is_valid(self) -> bool:
        """
        Perform tests and raise an ErrorMap on any invalid one
        Return True
        """

        if self._nb_drones < 2:
            raise ErrorFlyIn("Map needs at least two drones")

        if not any(h.point == Hub.Type.START for h in self._hubs):
            raise ErrorFlyIn("Map needs at least one starting hub")

        if not any(h.point == Hub.Type.END for h in self._hubs):
            raise ErrorFlyIn("Map needs at least one ending hub")

        if not any(h.point == Hub.Type.REGULAR for h in self._hubs):
            raise ErrorFlyIn("Map needs at least one REGULAR hub")

        return True

    # TODO: TEST THE GRAPH LOGIC - ARE ALL HUBS CONNECTED ??
    def test_hubs(self) -> bool:
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
