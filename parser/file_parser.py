import os
from models.map import Map
from error import ErrorFlyIn
from models.hub import Hub, ErrorHub

from typing import Optional, List, Iterator


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░▀█▀░█░░░█▀▀░░░█▀█░█▀█░█▀▄░█▀▀░█▀▀░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░░█░░█░░░█▀▀░░░█▀▀░█▀█░█▀▄░▀▀█░█▀▀░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░░▀▀▀░▀▀▀░▀▀▀░░░▀░░░▀░▀░▀░▀░▀▀▀░▀▀▀░▀░▀
class FileParser:
    def __init__(self) -> None:
        self._path: Optional[str] = None
        self._new_map = Map()

    def up_file(self, path: str) -> None:
        if not os.path.isfile(path):
            raise ErrorFile(path, "Does not exist.")

        self._path = path
        self._new_map = Map(os.path.basename(path))

    # ########################################################################
    # ########################################################### GET MAP ####
    @property
    def map(self) -> Map | None:
        if self._new_map:
            # TODO: ADD SOME CHECKS ????
            return self._new_map
        return None

    def parse_file(self) -> None:
        if self._path:
            try:
                with open(self._path, "r") as file:
                    lines: List[str] = [
                        line
                        for line in file.readlines()
                        if line and line.strip() and not line.startswith("#")
                    ]

                    if not lines:
                        raise ErrorFile(self._path, "Empty.")

                    self._get_nb_drones(lines[0])
                    self._get_hubs(
                        ln for ln in lines if "hub" in ln.split()[0]
                    )
                    self._get_connections(
                        ln for ln in lines if ln.startswith("connection: ")
                    )

            except ErrorFlyIn as e:
                raise ErrorFile(self._path, f"\n'{e}")

    # ########################################################################
    # ######################################################### NB DRONES ####
    def _get_nb_drones(self, first_line: str) -> None:
        if not first_line.startswith("nb_drones: "):
            raise ErrorFile(self._path, "Does not start with 'nb_drones: '.")

        try:
            self._new_map.nb_drones = int(first_line[10:].strip())
        except ValueError:
            raise ErrorFile(
                self._path,
                f"Invalid drone number ({first_line[10:].strip()}).",
            )

    # ########################################################################
    # ############################################################## HUBS ####
    def _get_hubs(self, lines: Iterator[str]) -> None:
        for line in lines:
            try:
                self._new_map += Hub.parse(line)

            except ErrorHub as e:
                raise ErrorFile(
                    self._path, f"On line: '{line[:10]}...'\n{str(e)}"
                )

        if not self._new_map.hubs:
            raise ErrorFile(self._path, "No hub found.")

    # ########################################################################
    # ####################################################### CONNECTIONS ####
    def _get_connections(self, lines: Iterator[str]) -> None:
        for line in lines:
            header, connection = line.split(maxsplit=1)

            if header != "connection:":
                raise ErrorFile(
                    self._path, f"Line '{line[:10]}' is not a connection."
                )

            if sum(1 for c in connection if c == "-") != 1:
                raise ErrorFile(
                    self._path, f"Line '{line[:10]}' is an invalid connection."
                )

            hub_from, hub_to = connection.split("-", maxsplit=1)

            if len(hub_from) < 3 or len(hub_to) < 3:
                raise ErrorFile(
                    self._path, f"Connection invalid {hub_from} -> {hub_to}"
                )

            self._new_map.connect_hubs(hub_from, hub_to)

    # ########################################################################
    # ############################################################### STR ####
    def __str__(self) -> str:
        # if not self._values:
        #     return "Nothing to display"
        # else:
        return f"Values parsed:\n{self._new_map}"


class LineParser:
    def __init__(self, line: str):
        self._line = line


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀▄░█▀▄░█▀█░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀▄░█▀▄░█░█░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░▀░▀░▀░▀▀▀░▀░▀
class ErrorFile(Exception):
    def __init__(self, file: str | None, message: str) -> None:
        if file:
            super().__init__(f"On file '{file}':\n{message}")
        else:
            super().__init__(f"Error file:\n{message}")
