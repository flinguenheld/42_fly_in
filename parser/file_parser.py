import functools
from visualiser.tmessage import TMessageSuccess
from typing import Optional, List, Dict, Iterator
import os


class ErrorFile(Exception):
    pass


class FileParser:
    def __init__(self):
        self._path: Optional[str] = None
        self._values: Dict[str, str] = dict()

    def up_file(self, path: str) -> None:
        if not os.path.isfile(path):
            raise ErrorFile(f"File '{path}' does not exist.")

        self._path = path
        self._values.clear()

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

        self._values["nb_drones"] = first_line[10:].strip()

    # ########################################################################
    # ############################################################## HUBS ####
    def _get_hubs(self, lines: Iterator[str]):
        hub = {}

        for line in lines:
            try:
                fields = line.split()
                if fields[0] != "hub:":
                    self._raise_error(f"{line} does not start with 'hub: '")

                hub["name"] = fields[1]
                hub["point"] = (fields[2], fields[3])
                # if len(fields) == 5:
                hub["options"] = self._extract_options(fields[4])

            except ErrorFile as e:
                raise e
            except Exception as e:
                self._raise_error(f"Parsing hub fail. {str(e)}")

        if not hub:
            self._raise_error("No hub found.")

    def _extract_options(self, line: str):
        nb_open = functools.reduce(
            lambda s, c: s + 1 if c == "[" else s, line, 0
        )
        nb_clos = functools.reduce(
            lambda s, c: s + 1 if c == "]" else s, line, 0
        )

        raise ErrorFile(f"open: {nb_open} - {nb_clos}")

        if nb_open != nb_clos or nb_open > 1 or not line.endswith("]\n"):
            self._raise_error(f"{line}\nInvalid option format.")

            if nb_clos == 0:
                return

            options = line.split("[", maxsplit=1)
            options = options.remove("]")

            raise (ErrorFile(str(options)))
            # print(options)

    # ########################################################################
    # ############################################ RAISE FORMATED MESSAGE ####
    def _raise_error(self, message: str) -> str:
        raise ErrorFile(f"on file: '{self._path}'\n\n{message}")

    # ########################################################################
    # ############################################################### STR ####
    def __str__(self) -> str:

        if not self._values:
            return "Nothing to display"
        else:
            return f"Values parsed:\n{self._values}"
