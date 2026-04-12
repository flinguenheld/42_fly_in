from error import ErrorFlyIn


class Fields:
    def __init__(self, line: str):
        self.line = line
        self._regular = ""
        self._fields = line.split()
        self._dict = {}

    def __str__(self):
        return str(self._dict)

    @ErrorFlyIn.spread(title="Extract fields")
    def extract(self):
        self._extract_options()
        self._extract_regular()

    def _extract_options(self):
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

    def _extract_regular(self):
        self._dict.update(
            {
                str(i): value.strip()
                for i, value in enumerate(self._regular.split())
            }
        )

    def get(self, key: str) -> str:
        if key not in self._dict:
            raise ErrorFlyIn(f"Invalid field '{key}'.", line="blototot")
        return self._dict[key]

    def has(self, key: str) -> bool:
        return key in self._dict

    @property
    def header(self) -> str:
        return self._dict["0"]
