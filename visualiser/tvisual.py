from visualiser.animation import Anim
import asyncio
from textual import work
from textual.containers import Vertical
from textual.widgets import Header, Footer
from textual.app import App, ComposeResult

from models.map import Map
from parser.file_parser import FileParser
from visualiser.tmap import TMap
from visualiser.theme import Theme
from visualiser.tfile import TFile
from visualiser.ttitle import TTitleMain
from visualiser.tmessage import TMessageError, TMessageSuccess


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█░█░▀█▀░█▀▀░█░█░█▀█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░▀▄▀░░█░░▀▀█░█░█░█▀█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░░▀░░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀
class TVisual(App):
    CSS_PATH = ["styles/main.tcss", "styles/file.tcss", "styles/message.tcss"]
    BINDINGS = [
        ("f", "file_selection", "File selection"),
        ("t", "next_theme", "Next theme"),
        ("d", "draw", "draw"),
        ("m", "move", "move offset"),
    ]

    def __init__(self) -> None:
        super().__init__()
        # self._canvas = TCanvas()
        self._tmap = TMap()
        self._title = TTitleMain()
        self._parser = FileParser()
        self._map: Map | None = None
        self._theme = Theme(self.app)

    # ########################################################################
    # ########################################################### COMPOSE ####
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical():
            yield self._title
            yield self._tmap
        yield Footer()

    # ########################################################################
    # ############################################################# MOUNT ####
    def on_mount(self) -> None:
        self._theme.next(self.app)
        # self.action_file_selection()

    # ################################################ TESTS #################
    # ################################################ TESTS #################
    def action_move(self) -> None:
        self._tmap.move_baby()

    # ################################################ TESTS #################
    # ################################################ TESTS #################
    @work
    @Anim.toggle_anim
    async def action_file_selection(self) -> None:
        self._map = None
        file_path: str = await self.push_screen_wait(TFile())
        # file_path = "./maps/hello.txt"

        if file_path:
            try:
                self._parser.new_file(file_path)
                self._parser.parse_file()
                self._map = self._parser.map
                if self._map:
                    self._tmap.new_canvas(self._map)

                # self.push_screen(TMessageSuccess(str(self._parser)))
                await self.push_screen_wait(TMessageSuccess(str(self._parser)))

            except Exception as e:
                # self.push_screen(TMessageError(str(e)))
                await self.push_screen_wait(TMessageError(str(e)))

    async def action_draw(self) -> None:
        if self._map:
            asyncio.create_task(self._tmap.draw_hubs(self._map))

    # ########################################################################
    # ########################################################### THEMES #####
    def action_next_theme(self) -> None:
        self._theme.next(self.app)
        self._tmap.up_colours()
