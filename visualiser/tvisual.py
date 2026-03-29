from visualiser.tfile import TFile
from visualiser.ttitle import TTitleMain
from visualiser.tmessage import TMessageError

from textual import work
from textual.widgets import Header, Footer
from textual.app import App, ComposeResult


class TVisual(App):
    CSS_PATH = ["styles/main.tcss", "styles/file.tcss", "styles/message.tcss"]
    BINDINGS = [("t", "test", "test baby")]

    def __init__(self) -> None:
        super().__init__()
        self._title = TTitleMain()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield self._title
        yield Footer()

    def on_mount(self) -> None:
        self.theme = "gruvbox"

    @work
    async def action_test(self) -> None:
        file_path = await self.push_screen_wait(TFile())

        if file_path:
            # self.push_screen(TMessageSuccess(f"file:\n{file_path}"))
            self.push_screen(TMessageError(f"file:\n{file_path}"))

        # self.push_screen(TFile())
