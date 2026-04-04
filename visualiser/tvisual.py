import asyncio
from textual import work
from textual.containers import Vertical
from textual.widgets import Header, Footer
from textual.app import App, ComposeResult

from models.map import Map
from parser.file_parser import FileParser
from visualiser.tmap import TMap
from visualiser.tfile import TFile
from visualiser.ttitle import TTitleMain
from visualiser.tmessage import TMessageError, TMessageSuccess


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█░█░▀█▀░█▀▀░█░█░█▀█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░▀▄▀░░█░░▀▀█░█░█░█▀█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░░▀░░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀
class TVisual(App):
    CSS_PATH = ["styles/main.tcss", "styles/file.tcss", "styles/message.tcss"]
    BINDINGS = [("t", "test", "test baby"), ("d", "draw", "draw")]

    def __init__(self) -> None:
        super().__init__()
        # self._canvas = TCanvas()
        self._tmap = TMap()
        self._title = TTitleMain()
        self._parser = FileParser()
        self._map: Map | None = None

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
        # self.theme = "gruvbox"
        self.theme = "catppuccin-latte"

        self.action_test()

    # ################################################ TESTS #################
    # ################################################ TESTS #################
    # ################################################ TESTS #################
    # ################################################ TESTS #################
    @work
    async def action_test(self) -> None:
        self._map = None
        file_path: str = await self.push_screen_wait(TFile())
        # file_path = "./maps/hello.txt"

        if file_path:
            try:
                self._parser.up_file(file_path)
                self._parser.parse_file()
                self._map = self._parser.map
                if self._map:
                    self._tmap.new_canvas(self._map)

                self.push_screen(TMessageSuccess(str(self._parser)))

            except Exception as e:
                self.push_screen(TMessageError(str(e)))

    async def action_draw(self) -> None:
        if self._map:
            asyncio.create_task(self._tmap.draw_hubs(self._map))
