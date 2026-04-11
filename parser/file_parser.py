import os
from models.map import Map
from error import ErrorFlyIn
from models.hub import Hub

from typing import List, Iterator


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
            with open(self._path, "r") as file:
                lines: List[str] = [
                    line
                    for line in file.readlines()
                    if line and line.strip() and not line.startswith("#")
                ]

                if not lines:
                    self._raise_errorfile("File is empty.")

                self._parse_nb_drones(lines[0])
                self._parse_hubs(ln for ln in lines if "hub" in ln.split()[0])
                self._parse_connections(
                    ln for ln in lines if ln.startswith("connection: ")
                )

    # ########################################################################
    # ######################################################### NB DRONES ####
    @ErrorFlyIn.spread(title="Number of drones")
    def _parse_nb_drones(self, first_line: str) -> None:
        if not first_line.startswith("nb_drones: "):
            self._raise_errorfile("File does not start with 'nb_drones: '.")

        try:
            self._new_map.nb_drones = int(first_line[10:].strip())
        except ValueError:
            self._raise_errorfile("Invalid drone number.", first_line)

    # ########################################################################
    # ############################################################## HUBS ####
    @ErrorFlyIn.spread(title="Hub parsing")
    def _parse_hubs(self, lines: Iterator[str]) -> None:
        for line in lines:
            try:
                line = line.strip()
                self._new_map += Hub.parse(line)

            except ErrorFlyIn as e:
                raise e + {"file": self._path, "line": line}

        if not self._new_map.hubs:
            self._raise_errorfile("No hub found.")

    # ########################################################################
    # ####################################################### CONNECTIONS ####
    @ErrorFlyIn.spread(title="Connection parsing")
    def _parse_connections(self, lines: Iterator[str]) -> None:
        for line in lines:
            line = line.strip()
            fields = line.split()

            if len(fields) < 2 or fields[0] != "connection:":
                self._raise_errorfile("Invalid connection format.", line)

            if sum(1 for c in fields[1] if c == "-") != 1:
                self._raise_errorfile("Invalid connection format.", line)

            # TODO: MANAGE OPTIONS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            hub_from, hub_to = fields[1].split("-", maxsplit=1)

            if len(hub_from) < 3 or len(hub_to) < 3:
                self._raise_errorfile(
                    f"Connection invalid {hub_from} -> {hub_to}.", line
                )

            self._new_map.connect_hubs(hub_from, hub_to)

    # ########################################################################
    # ############################################################### STR ####
    def __str__(self) -> str:
        # if not self._values:
        #     return "Nothing to display"
        # else:
        return f"Values parsed:\n{self._new_map}"

    # ########################################################################
    # ##################################### RAISE ERROR WITH FILE CONTEXT ####
    def _raise_errorfile(self, text: str, line: str | None = None) -> None:
        if line:
            raise ErrorFlyIn(text, file=self._path, line=line)
        else:
            raise ErrorFlyIn(text, file=self._path)


class LineParser:
    def __init__(self, line: str):
        self._line = line
