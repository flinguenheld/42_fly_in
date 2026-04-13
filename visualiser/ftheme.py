from textual.app import App
from textual.color import Color


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█░█░█▀▀░█▄█░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█▀█░█▀▀░█░█░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀░▀░▀▀▀
class FTheme:
    error = Color.parse("green")
    panel = Color.parse("green")
    accent = Color.parse("green")
    primary = Color.parse("green")
    success = Color.parse("green")
    warning = Color.parse("green")
    surface = Color.parse("green")
    secondary = Color.parse("green")
    foreground = Color.parse("green")
    background = Color.parse("white")

    _regular = {
        "red": Color.parse("red"),
        "blue": Color.parse("blue"),
        "pink": Color.parse("pink"),
        "grey": Color.parse("grey"),
        "green": Color.parse("green"),
        "brown": Color.parse("brown"),
        "black": Color.parse("black"),
        "white": Color.parse("white"),
        "purple": Color.parse("purple"),
        "orange": Color.parse("orange"),
        "yellow": Color.parse("yellow"),
    }

    _EXTRA = {
        "cyan": "blue",
        "lime": "green",
        "gold": "yellow",
        "crimson": "red",
        "rainbow": "pink",
        "maroon": "brown",
        "violet": "purple",
        "magenta": "purple",
    }

    def __init__(self, app: App) -> None:
        self._app = app

    # ########################################################################
    # ############################################# COLOURS OUTSIDE THEME ####
    @classmethod
    def get_regular(cls, which: str) -> Color:
        if which in cls._regular:
            return cls._regular[which]
        if which in cls._EXTRA:
            return cls._regular[cls._EXTRA[which]]

        return cls._regular[("black")]

    @classmethod
    def has_regular(cls, which: str) -> bool:
        return which in cls._regular or which in cls._EXTRA

    @classmethod
    def _clean_color(cls, name: str) -> str:
        return (
            name.removeprefix("dark")
            .removeprefix("bright")
            .removeprefix("light")
        )

    @classmethod
    def colour_list(cls) -> str:
        text = "Regular colours:\n"
        for c in cls._regular.keys():
            text += f"- {c}\n"
        text += "Crazy fucking ones:\n"
        for c in cls._EXTRA.keys():
            text += f"- {c}\n"
        return text

    # ########################################################################
    # ############################################################## NEXT ####
    def next(self) -> None:
        match self._app.theme[-5:]:
            case "uvbox":
                self._app.theme = "catppuccin-latte"
            case "hiato":
                self._app.theme = "catppuccin-mocha"
            case "mocha":
                self._app.theme = "catppuccin-frappe"
            case "latte":
                self._app.theme = "catppuccin-macchiato"
            case _:
                self._app.theme = "gruvbox"

        self._up_colours()

    # ########################################################################
    # ######################################################## UP COLOURS ####
    def _up_colours(self) -> None:
        theme = self._app.get_theme(self._app.theme)
        if theme:
            FTheme.error = Color.parse(theme.error)
            FTheme.panel = Color.parse(theme.panel)
            FTheme.accent = Color.parse(theme.accent)
            FTheme.primary = Color.parse(theme.primary)
            FTheme.success = Color.parse(theme.success)
            FTheme.warning = Color.parse(theme.warning)
            FTheme.surface = Color.parse(theme.surface)
            FTheme.secondary = Color.parse(theme.secondary)
            FTheme.foreground = Color.parse(theme.foreground)
            FTheme.background = Color.parse(theme.background)

            match self._app.theme:
                case "gruvbox":
                    FTheme._regular["red"] = Color(204, 36, 29)
                    FTheme._regular["blue"] = Color(69, 133, 136)
                    FTheme._regular["pink"] = Color(211, 134, 155)
                    FTheme._regular["grey"] = Color(102, 92, 84)
                    FTheme._regular["green"] = Color(152, 151, 26)
                    FTheme._regular["brown"] = Color(215, 153, 33)
                    FTheme._regular["black"] = Color(102, 92, 84)
                    FTheme._regular["white"] = Color(251, 241, 199)
                    FTheme._regular["purple"] = Color(177, 98, 134)
                    FTheme._regular["orange"] = Color(254, 128, 25)
                    FTheme._regular["yellow"] = Color(250, 189, 47)

                case "catppuccin-latte":
                    FTheme._regular["red"] = Color(210, 15, 57)
                    FTheme._regular["blue"] = Color(30, 102, 245)
                    FTheme._regular["pink"] = Color(234, 118, 203)
                    FTheme._regular["grey"] = Color(140, 143, 161)
                    FTheme._regular["green"] = Color(64, 160, 43)
                    FTheme._regular["brown"] = Color(230, 69, 83)
                    FTheme._regular["black"] = Color(156, 160, 176)
                    FTheme._regular["white"] = Color(76, 79, 105)
                    FTheme._regular["purple"] = Color(136, 57, 239)
                    FTheme._regular["orange"] = Color(254, 100, 11)
                    FTheme._regular["yellow"] = Color(223, 142, 29)

                case "catppuccin-frappe":
                    FTheme._regular["red"] = Color(231, 130, 132)
                    FTheme._regular["blue"] = Color(140, 170, 238)
                    FTheme._regular["pink"] = Color(244, 184, 228)
                    FTheme._regular["grey"] = Color(115, 121, 148)
                    FTheme._regular["green"] = Color(166, 209, 137)
                    FTheme._regular["brown"] = Color(234, 153, 156)
                    FTheme._regular["black"] = Color(81, 87, 109)
                    FTheme._regular["white"] = Color(198, 208, 245)
                    FTheme._regular["purple"] = Color(202, 158, 230)
                    FTheme._regular["orange"] = Color(239, 159, 118)
                    FTheme._regular["yellow"] = Color(229, 200, 144)

                case "catppuccin-macchiato":
                    FTheme._regular["red"] = Color(237, 135, 150)
                    FTheme._regular["blue"] = Color(138, 173, 244)
                    FTheme._regular["pink"] = Color(245, 189, 230)
                    FTheme._regular["grey"] = Color(110, 115, 141)
                    FTheme._regular["green"] = Color(166, 218, 149)
                    FTheme._regular["brown"] = Color(238, 153, 160)
                    FTheme._regular["black"] = Color(91, 96, 120)
                    FTheme._regular["white"] = Color(202, 211, 245)
                    FTheme._regular["purple"] = Color(198, 160, 246)
                    FTheme._regular["orange"] = Color(245, 169, 127)
                    FTheme._regular["yellow"] = Color(238, 212, 159)

                case _:
                    FTheme._regular["red"] = Color(243, 139, 168)
                    FTheme._regular["blue"] = Color(137, 180, 250)
                    FTheme._regular["pink"] = Color(245, 194, 231)
                    FTheme._regular["grey"] = Color(127, 132, 156)
                    FTheme._regular["green"] = Color(166, 227, 161)
                    FTheme._regular["brown"] = Color(235, 160, 172)
                    FTheme._regular["black"] = Color(88, 91, 112)
                    FTheme._regular["white"] = Color(205, 214, 244)
                    FTheme._regular["purple"] = Color(203, 166, 247)
                    FTheme._regular["orange"] = Color(250, 179, 135)
                    FTheme._regular["yellow"] = Color(249, 226, 175)
