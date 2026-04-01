from __future__ import annotations
from enum import Enum
from error import ErrorFlyIn
from point import Point


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█░█░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀█░█░█░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░▀░▀▀▀░▀▀░
class Hub:
    class Type(Enum):
        REGULAR = 0
        START = 1
        END = 2

    def __init__(self, name: str, point: Point, type: Hub.Type = Type.REGULAR):
        self.name = name
        self._point = point
        self._type = type

    # ########################################################################
    # ######################################################### ACCESSORS ####
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, txt: str) -> None:
        if "-" in txt:
            raise ErrorHub(f"Dashes are forbidden in hub name ({txt}).")
        self._name = txt

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

        return f"{title} {self._name} {self._point}"

    # ########################################################################
    # ############################################################# PARSE ####
    @staticmethod
    def parse(text: str) -> Hub:
        """
        Create a Hub according to the given text.
        Raise ErrorHub


        format: 'hub: roof1 3 4 [zone=restricted color=red]'
        """

        try:
            it = iter(text.split())

            # Starting line --
            match next(it):
                case "start_hub:":
                    type = Hub.Type.START
                case "end_hub:":
                    type = Hub.Type.END
                case "hub:":
                    type = Hub.Type.REGULAR
                case _:
                    raise ErrorHub(f"{text[:10]} does not start with 'hub: '")

            # Name --
            name = next(it)

            # Coordinates --
            point = Point.parse(x=next(it), y=next(it))

            # Options ?

            return Hub(name, point, type)

        except Exception as e:
            raise ErrorHub(str(e))


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀▄░█▀▄░█▀█░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀▄░█▀▄░█░█░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░▀░▀░▀░▀▀▀░▀░▀
class ErrorHub(ErrorFlyIn):
    def __init__(self, message: str) -> None:
        super().__init__(f"Hub error:\n{message}")
