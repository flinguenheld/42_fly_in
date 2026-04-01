from error import ErrorFlyIn
import os
from models.map import Map
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

    def parse_file(self) -> None:
        if self._path:
            try:
                with open(self._path, "r") as file:
                    lines: List[str] = [
                        line
                        for line in file.readlines()
                        if line and not line.startswith("#")
                    ]

                    if not lines:
                        raise ErrorFile(self._path, "Empty.")

                    self._get_nb_drones(lines[0])
                    self._get_hubs(ln for ln in lines if ln.startswith("hub:"))

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
                self._new_map.hubs = Hub.parse(line)

            except ErrorHub as e:
                raise ErrorFile(
                    self._path, f"On line: '{line[:10]}...'\n{str(e)}"
                )

        if not self._new_map.hubs:
            raise ErrorFile(self._path, "No hub found.")

    # ########################################################################
    # ########################################################### OPTIONS ####

    def _is_hub_line_valid(self, line: str) -> str:
        line = line.strip()

        nb_open = sum(1 for c in line if c == "[")
        nb_clos = sum(1 for c in line if c == "]")

        # if nb_open != nb_clos or nb_open > 1 or not line.endswith("]\n"):
        #     raise ErrorFile(f"'{line[:10]}...'\nInvalid option format.")

        return line.replace("[", " [ ").replace("]", " ] ")

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
