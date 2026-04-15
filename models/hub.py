from __future__ import annotations

from enum import Enum
from typing import Set

from point import Point
from error import ErrorFlyIn
from parser.fields import Fields
from visualiser.ftheme import FTheme


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█░█░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀█░█░█░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░▀░▀▀▀░▀▀░░░
class Hub:
    # ############################################################## TYPE ####
    class Type(Enum):
        REGULAR = 0
        START = 1
        END = 2

    # ############################################################## ZONE ####
    class Zone(Enum):
        NORMAL = 0
        BLOCKED = 1
        PRIORITY = 2
        RESTRICTED = 3

        @staticmethod
        @ErrorFlyIn.spread("Hub zone type parsing")
        def from_txt(text: str) -> Hub.Zone:
            match text.upper():
                case "NORMAL":
                    return Hub.Zone.NORMAL
                case "BLOCKED":
                    return Hub.Zone.BLOCKED
                case "PRIORITY":
                    return Hub.Zone.PRIORITY
                case "RESTRICTED":
                    return Hub.Zone.RESTRICTED
                case _:
                    raise ErrorFlyIn(f"Invalid value '{text}'.")

    # ########################################################################
    def __init__(
        self,
        name: str,
        point: Point,
        type: Hub.Type = Type.REGULAR,
        zone: Zone = Zone.NORMAL,
        color: str = "white",
        max_drones: int = 0,
    ):
        self._name = name
        self.point: Point = point
        self.type: Hub.Type = type
        self.zone = zone
        self.color = color
        self.max_drones = max_drones
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
    @ErrorFlyIn.spread("Hub name")
    def name(self, txt: str) -> None:
        if "-" in txt:
            raise ErrorFlyIn(f"Dashes are forbidden in hub name ({txt}).")
        self._name = txt

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

        return f"{title} '{self._name}' {self.point} '{self._next_nodes}'"

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

        name = field.get("1", "Hub name")
        point = Point.parse(x=field.get("2", "X"), y=field.get("3", "Y"))

        zone = field.get("zone") if field.has("zone") else "normal"
        color = field.get("color") if field.has("color") else "white"
        max_dr = field.get("max_drones") if field.has("max_drones") else "0"

        # Adapt options --
        color = FTheme._clean_color(color)
        if not FTheme.has_regular(color):
            raise ErrorFlyIn(
                f"Invalid color option. Allowed:\n{FTheme.colour_list()}",
                line=field.line,
            )

        try:
            max_d = int(max_dr)
        except ValueError:
            raise ErrorFlyIn("Invalid 'max_drones' option", line=field.line)

        return Hub(name, point, type, Hub.Zone.from_txt(zone), color, max_d)
