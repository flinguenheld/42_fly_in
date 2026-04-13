from textual.color import Color
from textual.app import App


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█░█░█▀▀░█▄█░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█▀█░█▀▀░█░█░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀░▀░▀▀▀
class FTheme:
    primary = Color.parse("green")
    secondary = Color.parse("green")
    accent = Color.parse("green")
    foreground = Color.parse("green")
    background = Color.parse("white")
    success = Color.parse("green")
    warning = Color.parse("green")
    error = Color.parse("green")
    surface = Color.parse("green")
    panel = Color.parse("green")

    def __init__(self, app: App) -> None:
        self._app = app

    # ########################################################################
    # ############################################################## NEXT ####
    def next(self) -> None:
        match self._app.theme[-5:]:
            case "uvbox":
                self._app.theme = "catppuccin-latte"
            case "latte":
                self._app.theme = "catppuccin-macchiato"
            case "hiato":
                self._app.theme = "catppuccin-mocha"
            case "mocha":
                self._app.theme = "catppuccin-frappe"
            case _:
                self._app.theme = "gruvbox"

        self._up_colours()

    # ########################################################################
    # ######################################################## UP COLOURS ####
    def _up_colours(self) -> None:
        theme = self._app.get_theme(self._app.theme)
        if theme:
            FTheme.primary = Color.parse(theme.primary)
            FTheme.secondary = Color.parse(theme.secondary)
            FTheme.accent = Color.parse(theme.accent)
            FTheme.foreground = Color.parse(theme.foreground)
            FTheme.background = Color.parse(theme.background)
            FTheme.success = Color.parse(theme.success)
            FTheme.warning = Color.parse(theme.warning)
            FTheme.error = Color.parse(theme.error)
            FTheme.surface = Color.parse(theme.surface)
            FTheme.panel = Color.parse(theme.panel)
