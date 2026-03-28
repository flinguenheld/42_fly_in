from visualiser.tfile import TFile
from visualiser.ttitle import TTitleMain

from textual import work
from textual.widgets import Header, Footer
from textual.app import App, ComposeResult


class TVisual(App):
    CSS_PATH = ["styles/main.tcss", "styles/file.tcss"]
    BINDINGS = [("t", "test", "test baby")]

    def __init__(self) -> None:
        super().__init__()
        self._title = TTitleMain()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield self._title
        yield Footer()

    async def on_mount(self) -> None:
        self._title.launch_animation()

    @work
    async def action_test(self) -> None:
        await self.push_screen_wait(TFile())
        # self.push_screen(TFile())
