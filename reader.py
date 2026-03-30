from typing import Optional, List, Dict
import os


class ErrorFile(Exception):
    pass


class FileParser:
    def __init__(self):
        self._path: Optional[str] = None
        self._values: Dict[str, str]

    def up_file(self, path: str) -> None:
        if not os.path.isfile(path):
            raise ErrorFile(f"File '{path}' does not exist.")

        self._path = path

    def parse_file(self) -> None:
        if self._path:
            with open(self._path, "r") as file:
                lines = file.readlines()

                if not lines:
                    raise ErrorFile(f"File '{self._path}' is empty.")

                self._get_nb_drones(lines[0])
                self._get_hubs(lines[0])

    # ########################################################################
    # ######################################################### NB DRONES ####
    def _get_nb_drones(self, first_line: str):
        if not first_line.startswith("nb_drones: "):
            raise ErrorFile(
                f"File '{self._path}' does not start with 'nb_drones: '."
            )

        self._values["nb_drones"] = first_line[10:].strip()

    # ########################################################################
    # #########################################################  ####
    def _get_hubs(self):
        pass

    # ########################################################################
    # ############################################################### STR ####
    def __str__(self) -> str:

        if not self._values:
            return "Nothing to display"
        else:
            return f"Values parsed:\n{self._values}"
