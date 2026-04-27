import asyncio

from textual import work
from textual.app import App, ComposeResult
from textual.containers import Vertical, ScrollableContainer

from models.map import Map
from error import ErrorFlyIn
from parser.file_parser import FileParser

from visualiser.tfile import TFile
from visualiser.ftheme import FTheme
from visualiser.map.tmap import TMap
from visualiser.tdebug import TDebug
from visualiser.animation import Anim
from visualiser.tactions import TActions
from visualiser.ttitle import TTitleMain
from visualiser.tmessage import TMessageError


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█░█░▀█▀░█▀▀░█░█░█▀█░█░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░▀▄▀░░█░░▀▀█░█░█░█▀█░█░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░░▀░░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░░
class TVisual(App):
    CSS_PATH = [
        "styles/main.tcss",
        "styles/map.tcss",
        "styles/file.tcss",
        "styles/debug.tcss",
        "styles/message.tcss",
        "styles/actions.tcss",
    ]
    BINDINGS = [
        ("t", "next_theme", "Next theme"),
        ("f", "file_selection", "File selection"),
        ("r", "restart", "restart map"),
        ("n", "next_turn", "Next turn"),
        ("p", "previous_turn", "Previous turn"),
        ("d", "debug", "Debug"),
    ]

    def __init__(self) -> None:
        super().__init__()

        self._title = TTitleMain()

        self.map: Map | None = None
        self.tmap: TMap | None = None
        self.ftheme = FTheme(self.app)
        self.file_path: str | None = None

        self._tactions = TActions()
        self._layout_map = ScrollableContainer(classes="tmap_layout")

    # ########################################################################
    # ######################################################### NEXT TURN ####

    # TODO: ADD ANOTHER OPTION TO DO ALL TURNS --
    # TODO: ALSO A WAY TO STOP IN THE MIDDLE ---

    async def action_next_turn(self) -> None:
        if self.map and self.tmap:
            await self.tmap.next_turn()

    async def action_previous_turn(self) -> None:
        if self.map and self.tmap:
            await self.tmap.previous_turn()

    # ########################################################################
    # ########################################################## RESTART #####
    async def action_restart(self) -> None:
        if self.file_path:
            try:
                parser = FileParser(self.file_path)
                parser.parse_file()

                self.map = None
                self.map = Map(parser.map_creation)
                await self._init_map()

            except ErrorFlyIn as ef:
                await self.push_screen_wait(
                    TMessageError(ef.str_with_context())
                )

            except Exception as e:
                await self.push_screen_wait(TMessageError(str(e)))

    # #####################################################
    # ###################################### INIT MAP #####
    async def _init_map(self) -> None:

        if self.tmap:
            self.tmap.remove()
            self.tmap = None

        if self.map:
            self.tmap = TMap(self.map)
            self._layout_map.mount(self.tmap)

            await asyncio.create_task(self.tmap.draw_hubs())

    # ########################################################################
    # ###################################################### SELECT FILE #####
    @work
    @Anim.toggle_anim
    async def action_file_selection(self) -> None:
        new_path = await self.push_screen_wait(TFile())
        # self._file_path = "./maps/hello.txt"

        if new_path:
            self.file_path = new_path
            await self.action_restart()

    # ########################################################################
    # ########################################################### THEMES #####
    def action_next_theme(self) -> None:
        self.ftheme.next()
        if self.tmap:
            self.tmap.up_colours()

    # ########################################################################
    # ########################################################### TDEBUG #####
    @work
    @Anim.toggle_anim
    async def action_debug(self) -> None:
        if self.map:
            await self.push_screen_wait(
                TDebug(self.map.paths, self.map.drones, self.map.table)
            )

    # ########################################################################
    # ########################################################### COMPOSE ####
    def compose(self) -> ComposeResult:
        # yield Header(show_clock=True)
        with Vertical():
            yield self._title
            yield self._tactions
            yield self._layout_map
        # yield Footer()

    # ########################################################################
    # ############################################################# MOUNT ####
    async def on_mount(self) -> None:
        self.ftheme.next()
        self.call_later(self.action_file_selection)
