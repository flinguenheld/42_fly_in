from typing import Dict
from error import ErrorFlyIn


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░▀█▀░█▀▀░█░░░█▀▄░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░░█░░█▀▀░█░░░█░█░▀▀█
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░░▀▀▀░▀▀▀░▀▀▀░▀▀░░▀▀▀
class Fields:
    def __init__(self, line: str) -> None:
        self.line = line
        self._regular = ""
        self._fields = line.split()
        self._dict: Dict[str, str] = {}

    @ErrorFlyIn.spread(title="Extract fields from line")
    def extract(self) -> None:
        self._extract_options()
        self._extract_regular()

    # ########################################################################
    # ####################################################### EXTRACTIONS ####
    def _extract_options(self) -> None:
        if "[" in self.line:
            self._regular, options = self.line.split("[")
            if options[-1] != "]":
                raise ErrorFlyIn(
                    "Options have to be surrounded by brackets []",
                    line=self.line,
                )

            self._dict = {
                key.strip(): value.strip()
                for key, value in (f.split("=") for f in options[:-1].split())
            }

        else:
            self._regular = self.line

    def _extract_regular(self) -> None:
        self._dict.update(
            {
                str(i): value.strip()
                for i, value in enumerate(self._regular.split())
            }
        )

    # ########################################################################
    # ############################################################### HAS ####
    def has(self, key: str) -> bool:
        return key in self._dict

    # ########################################################################
    # ############################################################### GET ####
    def get(self, key: str, help: str = "") -> str:
        if key not in self._dict:
            txt = help if help else key
            raise ErrorFlyIn(f"Field '{txt}' not found.")
        else:
            return self._dict[key]

    # ########################################################################
    # ############################################################ HEADER ####
    @property
    def header(self) -> str:
        return self.get("0", "header")

    # ########################################################################
    # ############################################################### STR ####
    def __str__(self) -> str:
        return str(self._dict)
