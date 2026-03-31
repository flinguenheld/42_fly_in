import os
from point import Point
from models.hub import Hub
from models.map import Map

from typing import Optional, List, Dict, Iterator


class ErrorFile(Exception):
    pass


class FileParser:
    def __init__(self):
        self._path: Optional[str] = None
        self._new_map = Map()

    def up_file(self, path: str) -> None:
        if not os.path.isfile(path):
            raise ErrorFile(f"File '{path}' does not exist.")

        self._path = path
        self._new_map = Map(os.path.basename(path))

    def parse_file(self) -> None:
        if self._path:
            with open(self._path, "r") as file:
                lines: List[str] = [
                    line
                    for line in file.readlines()
                    if line and not line.startswith("#")
                ]

                if not lines:
                    raise ErrorFile(f"File '{self._path}' is empty.")

                self._get_nb_drones(lines[0])
                self._get_hubs(
                    line for line in lines if line.startswith("hub:")
                )

    # ########################################################################
    # ######################################################### NB DRONES ####
    def _get_nb_drones(self, first_line: str):
        if not first_line.startswith("nb_drones: "):
            raise ErrorFile(
                f"File '{self._path}' does not start with 'nb_drones: '."
            )

        # TODO: Any check conversion ?????
        self._new_map.nb_drones = int(first_line[10:].strip())

    # ########################################################################
    # ############################################################## HUBS ####
    def _get_hubs(self, lines: Iterator[str]):
        for line in lines:
            try:
                line = self._is_hub_line_valid(line)

                it = iter(line.split())

                start = next(it)
                if start != "hub:":
                    self._raise_error(
                        f"{line[:10]} does not start with 'hub: '"
                    )

                # Name --
                name = next(it)

                # TODO: Check if there is already a hub with this name
                # if name in self._values:
                # self._raise_error(f"Duplicated hub: '{name}'")

                # Coordinates --
                try:
                    point = Point.new_from_xy(next(it), next(it))
                except Exception:
                    self._raise_error(
                        f"Parsing hub '{name}' fail:\nInvalid coordinates.",
                    )

                new_hub = Hub(name, point)

                if next(it) == "[":
                    while True:
                        option = next(it, None)
                        if option:
                            pass

                        else:
                            break

                self._new_map.add_hub(new_hub)

            except ErrorFile as e:
                self._raise_error(f"Parsing hub fail: {str(e)}")
            except Exception as e:
                self._raise_error(f"Parsing hub fail. '{str(e)}'")

        if not self._new_map.hubs:
            self._raise_error("No hub found.")

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
    # ############################################ RAISE FORMATED MESSAGE ####
    def _raise_error(self, message: str) -> str:
        raise ErrorFile(f"on file: '{self._path}'\n\n{message}")

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
