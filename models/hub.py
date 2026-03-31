from point import Point


class Hub:
    def __init__(self, name: str, point: Point):
        self._name = name
        self._point = point

    def __str__(self):
        return f"Hub: {self._name} {self._point.xy}"
