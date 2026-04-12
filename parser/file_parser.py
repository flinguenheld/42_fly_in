from __future__ import annotations

import os
from typing import List, Iterator

from models.map import Map
from models.hub import Hub
from error import ErrorFlyIn
from parser.fields import Fields


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░▀█▀░█░░░█▀▀░░░█▀█░█▀█░█▀▄░█▀▀░█▀▀░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░░█░░█░░░█▀▀░░░█▀▀░█▀█░█▀▄░▀▀█░█▀▀░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░░▀▀▀░▀▀▀░▀▀▀░░░▀░░░▀░▀░▀░▀░▀▀▀░▀▀▀░▀░▀
class FileParser:
    def __init__(self) -> None:
        self._path: str = ""
        self._new_map = Map()

    # ########################################################################
    # ########################################################## NEW FILE ####
    @ErrorFlyIn.spread(title="Parsing file")
    def new_file(self, path: str) -> None:
        if not os.path.isfile(path):
            self._raise_errorfile("File does not exist.")

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

    # ########################################################################
    # ######################################################## PARSE FILE ####
    @ErrorFlyIn.spread(title="Parsing file")
    def parse_file(self) -> None:
        if self._path:
            lines: List[Fields] = []
            with open(self._path, "r") as file:
                for line in file.readlines():
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue

                    fields = Fields(line)
                    fields.extract()

                    lines.append(fields)

                if not lines:
                    self._raise_errorfile("File is empty.")

                self._parse_nb_drones(lines[0])
                self._parse_hubs(fd for fd in lines if "hub" in fd.header)
                self._parse_connections(
                    fd for fd in lines if "connection" in fd.header
                )

    # ########################################################################
    # ######################################################### NB DRONES ####
    @ErrorFlyIn.spread(title="Number of drones")
    def _parse_nb_drones(self, first_line: Fields) -> None:

        if first_line.header != "nb_drones:":
            self._raise_errorfile("File does not start with 'nb_drones: '.")

        nb = first_line.get("1")

        try:
            self._new_map.nb_drones = int(nb)
        except ValueError:
            self._raise_errorfile("Invalid drone number.", first_line.line)

    # ########################################################################
    # ############################################################## HUBS ####
    @ErrorFlyIn.spread(title="Hub parsing")
    def _parse_hubs(self, lines: Iterator[Fields]) -> None:
        for field in lines:
            try:
                self._new_map += Hub.parse(field)

            except ErrorFlyIn as e:
                raise e + {"file": self._path, "line": field.line}

        if not self._new_map.hubs:
            self._raise_errorfile("No hub found.")

    # ########################################################################
    # ####################################################### CONNECTIONS ####
    @ErrorFlyIn.spread(title="Connection parsing")
    def _parse_connections(self, lines: Iterator[Fields]) -> None:
        for field in lines:
            if field.header != "connection:":
                self._raise_errorfile("Invalid connection format.", field.line)

            hub_from, hub_to = field.get("1", "hubs").split("-", maxsplit=1)
            try:
                self._new_map.connect_hubs(hub_from, hub_to)
            except ErrorFlyIn as e:
                raise e + {"file": self._path, "line": field.line}

            # Option --
            # TODO: ADD THE OPTION IN THE MAP ---
            if field.has("max_link_capacity"):
                pass

    # ########################################################################
    # ############################################################### STR ####
    def __str__(self) -> str:
        return f"Values parsed:\n{self._new_map}"

    # ########################################################################
    # ##################################### RAISE ERROR WITH FILE CONTEXT ####
    def _raise_errorfile(self, text: str, line: str | None = None) -> None:
        if line:
            raise ErrorFlyIn(text, file=self._path, line=line)
        else:
            raise ErrorFlyIn(text, file=self._path)
