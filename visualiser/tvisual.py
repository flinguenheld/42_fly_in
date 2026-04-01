from visualiser.tfile import TFile
from visualiser.ttitle import TTitleMain
from visualiser.tmessage import TMessageError, TMessageSuccess

from parser.file_parser import FileParser

from textual import work
from textual.widgets import Header, Footer
from textual.app import App, ComposeResult


class TVisual(App):
    CSS_PATH = ["styles/main.tcss", "styles/file.tcss", "styles/message.tcss"]
    BINDINGS = [("t", "test", "test baby")]

    def __init__(self) -> None:
        super().__init__()
        self._title = TTitleMain()
        self._parser = FileParser()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield self._title
        yield Footer()

    def on_mount(self) -> None:
        self.theme = "gruvbox"

        self.action_test()

    @work
    async def action_test(self) -> None:
        # ############################################### TESTS #################
        file_path = await self.push_screen_wait(TFile())
        # file_path = "./maps/hello.txt"

        if not file_path:
            self.push_screen(TMessageError(f"file:\n{file_path}"))
        else:
            try:
                self._parser.up_file(file_path)
                self._parser.parse_file()

                self.push_screen(TMessageSuccess(str(self._parser)))

            except Exception as e:
                self.push_screen(TMessageError(str(e)))
