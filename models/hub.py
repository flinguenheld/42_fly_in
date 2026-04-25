from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import math

from error import ErrorFlyIn
from models.point import Point
from parser.fields import Fields
from visualiser.ftheme import FTheme


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█░█░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀█░█░█░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░▀░▀▀▀░▀▀░░░


@dataclass(frozen=True, unsafe_hash=True)
class Hub:
    # ############################################################## TYPE ####
    class Type(Enum):
        REGULAR = 0
        START = 1
        END = 2

        @staticmethod
        @ErrorFlyIn.spread("Hub type parsing")
        def from_txt(text: str) -> Hub.Type:
            match text.upper():
                case "START_HUB:":
                    return Hub.Type.START
                case "END_HUB:":
                    return Hub.Type.END
                case "HUB:":
                    return Hub.Type.REGULAR
                case _:
                    raise ErrorFlyIn(f"Invalid value '{text}'.")

    # ############################################################## ZONE ####
    class Zone(Enum):
        NORMAL = 2
        BLOCKED = math.inf
        PRIORITY = 1.8
        RESTRICTED = 4

        @staticmethod
        @ErrorFlyIn.spread("Hub zone parsing")
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

    name: str
    point: Point
    max_drones: int = 1
    color: str = "white"
    zone: Zone = Zone.NORMAL
    type: Hub.Type = Type.REGULAR

    # ########################################################################
    # ############################################################## INIT ####
    @ErrorFlyIn.spread("Hub creation")
    def __post_init__(self) -> None:
        if "-" in self.name or " " in self.name:
            raise ErrorFlyIn("Name cannot contains space nor dash.")
        # if len(self.name) < 3:
        #     raise ErrorFlyIn("Name cannot have less than three letters.")
        if self.max_drones < 0:
            raise ErrorFlyIn("Max drones value cannot be less than 0.")

    # ########################################################################
    # ############################################################# PARSE ####
    @staticmethod
    @ErrorFlyIn.spread("Hub parsing")
    def parse(fd: Fields) -> Hub:
        """
        Create a Hub according to the given text.
        Raise ErrorFlyIn

        format: 'hub: roof1 3 4 [zone=restricted color=red]'
        """

        # Starting line --
        type = Hub.Type.from_txt(fd.header)

        name = fd.get("1", "Hub name")
        point = Point.parse(x=fd.get("2", "X"), y=fd.get("3", "Y"))

        zone = fd.get("zone") if fd.has("zone") else "normal"
        color = fd.get("color") if fd.has("color") else "white"
        max_drones = fd.get("max_drones") if fd.has("max_drones") else "1"

        # Adapt options --
        color = FTheme._clean_color(color)
        if not FTheme.has_regular(color):
            raise ErrorFlyIn(f"Invalid color.\n{FTheme.colour_list()}")

        try:
            max = int(max_drones)
        except ValueError:
            raise ErrorFlyIn("Invalid 'max_drones' option.")

        return Hub(name, point, max, color, Hub.Zone.from_txt(zone), type)

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

        # return f"{title} '{self.name}' {self.point}"
        return f"Hub '{self.name}'"
