import asyncio
from textual.widgets import Header, Footer
from textual.app import App, ComposeResult

from visualiser.ttitle import TTitleMain


class TVisual(App):
    CSS_PATH = ["styles/main.tcss"]
    BINDINGS = [("t", "test", "test baby")]

    def __init__(self):
        super().__init__()
        self._title = TTitleMain()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield self._title
        yield Footer()

    async def on_mount(self) -> None:
        self._title.launch_animation()

    async def action_test(self) -> None:
        pass
