from __future__ import annotations
from parser.fields import Fields
from enum import Enum
from typing import Set
from point import Point
from error import ErrorFlyIn


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█░█░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀█░█░█░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░▀░▀▀▀░▀▀░
class Hub:
    class Type(Enum):
        REGULAR = 0
        START = 1
        END = 2

    class Zone(Enum):
        REGULAR = 0
        RESTRICTED = 1
        PRIORITY = 2

        @staticmethod
        def from_txt(text: str) -> Hub.Zone:
            match text.upper():
                case "PRIORITY":
                    return Hub.Zone.PRIORITY
                case "RESTRICTED":
                    return Hub.Zone.RESTRICTED
                case "REGULAR":
                    return Hub.Zone.REGULAR
                case _:
                    raise ErrorFlyIn(f"Invalid zone value '{text}'.")

    def __init__(
        self,
        name: str,
        point: Point,
        type: Hub.Type = Type.REGULAR,
        zone: Zone = Zone.REGULAR,
        color: str = "white",
        max_drones: int = 0,
    ):
        self.name = name
        self._point: Point = point
        self._type: Hub.Type = type
        self._next_nodes: Set[Hub] = set()

    # ########################################################################
    # ############################################################## NEXT ####
    @property
    def next_nodes(self) -> Set[Hub]:
        return self._next_nodes

    def __iadd__(self, other: Hub) -> Hub:
        self._next_nodes.add(other)
        return self

    # ########################################################################
    # ############################################################## NAME ####
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, txt: str) -> None:
        if "-" in txt:
            raise ErrorFlyIn(f"Dashes are forbidden in hub name ({txt}).")
        self._name = txt

    # ########################################################################
    # ###################################################### POINT / TYPE ####
    @property
    def point(self) -> Point:
        return self._point

    @property
    def type(self) -> Hub.Type:
        return self._type

    # ########################################################################
    # ############################################################### STR ####
    def __str__(self) -> str:
        match self.type:
            case Hub.Type.REGULAR:
                title = "Hub :"
            case Hub.Type.START:
                title = "Hub (start):"
            case Hub.Type.END:
                title = "Hub (end):"

        return f"{title} '{self._name}' {self._point} '{self._next_nodes}'"

    # ########################################################################
    # ############################################################# PARSE ####
    @staticmethod
    @ErrorFlyIn.spread("Hub parsing")
    def parse(field: Fields) -> Hub:
        """
        Create a Hub according to the given text.
        Raise ErrorFlyIn

        format: 'hub: roof1 3 4 [zone=restricted color=red]'
        """

        # it = iter(text.split())

        # Starting line --
        match field.header:
            case "start_hub:":
                type = Hub.Type.START
            case "end_hub:":
                type = Hub.Type.END
            case "hub:":
                type = Hub.Type.REGULAR
            case _:
                raise ErrorFlyIn(
                    "Line does not start with 'hub'.", line=field.line
                )

        # Name --
        name = field.get("1")

        # Coordinates --
        point = Point.parse(x=field.get("2"), y=field.get("3"))

        # Options --
        zone = field.get("zone") if field.has("zone") else "regular"
        color = field.get("color") if field.has("color") else "white"
        max_dr = field.get("max_drones") if field.has("max_drones") else "0"

        try:
            max_dr = int(max_dr)
        except ValueError:
            raise ErrorFlyIn("Invalid 'max_drones' value", line=field.line)

        return Hub(name, point, type, Hub.Zone.from_txt(zone), color, max_dr)
