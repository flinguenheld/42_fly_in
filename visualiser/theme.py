from textual.color import Color
from textual.app import App


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█░█░█▀▀░█▄█░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█▀█░█▀▀░█░█░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀░▀░▀▀▀
class Theme:
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

    def __init__(self, app: App):
        self.next(app)

    # ########################################################################
    # ############################################################## NEXT ####
    def next(self, app: App):
        match app.theme[-5:]:
            case "uvbox":
                app.theme = "catppuccin-latte"
            case "latte":
                app.theme = "catppuccin-macchiato"
            case "hiato":
                app.theme = "catppuccin-mocha"
            case "mocha":
                app.theme = "catppuccin-frappe"
            case _:
                app.theme = "gruvbox"

        Theme.up_colours(app)

    # ########################################################################
    # ######################################################## UP COLOURS ####
    @classmethod
    def up_colours(cls, app: App):
        theme = app.get_theme(app.theme)
        if theme:
            cls.primary = Color.parse(theme.primary)
            cls.secondary = Color.parse(theme.secondary)
            cls.accent = Color.parse(theme.accent)
            cls.foreground = Color.parse(theme.foreground)
            cls.background = Color.parse(theme.background)
            cls.success = Color.parse(theme.success)
            cls.warning = Color.parse(theme.warning)
            cls.error = Color.parse(theme.error)
            cls.surface = Color.parse(theme.surface)
            cls.panel = Color.parse(theme.panel)
