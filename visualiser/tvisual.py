import asyncio

from textual import work
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.containers import Vertical, ScrollableContainer

from models.map import Map
from error import ErrorFlyIn
from parser.file_parser import FileParser

from visualiser.tfile import TFile
from visualiser.ftheme import FTheme
from visualiser.map.tmap import TMap
from visualiser.animation import Anim
from visualiser.ttitle import TTitleMain
from visualiser.tmessage import TMessageError, TMessageSuccess


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█░█░▀█▀░█▀▀░█░█░█▀█░█░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░▀▄▀░░█░░▀▀█░█░█░█▀█░█░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░░▀░░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░░
class TVisual(App):
    CSS_PATH = [
        "styles/main.tcss",
        "styles/map.tcss",
        "styles/file.tcss",
        "styles/message.tcss",
    ]
    BINDINGS = [
        ("f", "file_selection", "File selection"),
        ("t", "next_theme", "Next theme"),
        ("d", "draw", "draw"),
        ("m", "move", "move offset"),
    ]

    def __init__(self) -> None:
        super().__init__()

        self._title = TTitleMain()
        self._parser = FileParser()

        self._map: Map | None = None
        self._tmap: TMap | None = None
        self._theme = FTheme(self.app)

        self._layout_map = ScrollableContainer(classes="tmap_layout")

    # ########################################################################
    # ########################################################### COMPOSE ####
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical():
            yield self._title
            yield self._layout_map
        yield Footer()

    # ########################################################################
    # ############################################################# MOUNT ####
    async def on_mount(self) -> None:
        self._theme.next()
        self.call_later(self.action_file_selection)

    # ########################################################################
    # ############################################################# DRAW #####
    async def action_draw(self) -> None:

        if self._map:
            if self._tmap:
                self._tmap.remove()

            self._tmap = TMap(self._map)
            self._layout_map.mount(self._tmap)

            asyncio.create_task(self._tmap.draw_drones())
            asyncio.create_task(self._tmap.draw_hubs())

    # ########################################################################
    # ########################################################### NEW MAP ####
    def new_map(self, map: Map) -> None:

        if self._tmap:
            self._tmap.remove()

        # TODO: Add some test ??
        self._map = map

    # ################################################ TESTS #################
    # ################################################ TESTS #################
    def action_move(self) -> None:
        pass
        # if self._tmap:
        #     self._tmap.move_baby()

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
                map = self._parser.map
                if map:
                    self.new_map(map)

                # self.push_screen(TMessageSuccess(str(self._parser)))
                await self.push_screen_wait(TMessageSuccess(str(self._parser)))

            except ErrorFlyIn as ef:
                await self.push_screen_wait(
                    TMessageError(ef.str_with_context())
                )

            except Exception as e:
                # self.push_screen(TMessageError(str(e)))
                await self.push_screen_wait(TMessageError(str(e)))

    # ########################################################################
    # ########################################################### THEMES #####
    def action_next_theme(self) -> None:
        self._theme.next()
        if self._tmap:
            self._tmap.up_colours()
