from __future__ import annotations
from error import ErrorFlyIn
from point import Point


class ErrorHub(ErrorFlyIn):
    def __init__(self, message: str) -> None:
        super().__init__(f"Hub error:\n{message}")


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█░█░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀█░█░█░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░▀░▀▀▀░▀▀░
class Hub:
    def __init__(self, name: str, point: Point):
        self._name = name
        self._point = point

    # ########################################################################
    # ############################################################### STR ####
    def __str__(self):
        return f"Hub: {self._name} {self._point}"

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

            start = next(it)
            if start != "hub:":
                raise ErrorHub(f"{text[:10]} does not start with 'hub: '")

            # Name --
            name = next(it)

            # Coordinates --
            point = Point.parse(x=next(it), y=next(it))

            # Options ?

            return Hub(name, point)

        except Exception as e:
            raise ErrorHub(str(e))
