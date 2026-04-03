from visualiser.tmap import TMap
import asyncio
from models.map import Map
from textual.containers import (
    Center,
    ScrollableContainer,
    VerticalGroup,
    Vertical,
)
from textual.canvas import Canvas
from visualiser.tcanvas import TCanvas
from visualiser.tfile import TFile
from visualiser.ttitle import TTitleMain
from visualiser.tmessage import TMessageError, TMessageSuccess

from parser.file_parser import FileParser

from textual import work
from textual.widgets import Header, Footer, Label
from textual.app import App, ComposeResult


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
        self._layout = ScrollableContainer(classes="tmap_layout")

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical():
            yield self._title
            with self._layout:
                yield self._tmap
        yield Footer()

    def on_mount(self) -> None:
        self.theme = "gruvbox"

        self.action_test()

    @work
    async def action_test(self) -> None:
        # ############################################### TESTS #################
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
            # self._tmap.new_canvas(self._map)
            # self._canvas.up_my_ass(self._map)
            asyncio.create_task(self._tmap.draw_hubs(self._map))

    # async def blah(self) -> None:
    #     if self._map:
    #         start = self._map.start
    #         if start:
    #             self.notify(f"here: {start.next_nodes}")
    #         else:
    #             self.notify("NO START !!!!!!!")

    #         for hub in self._map.loop():
    #             self.notify(f"hub: {hub.point}")
    #             self._canvas.draw_circle(
    #                 hub.point.col * 20 + 5, hub.point.row * 20 + 5, 2
    #             )
    #             await asyncio.sleep(0.3)
