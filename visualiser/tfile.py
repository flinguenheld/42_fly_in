from typing import List, Iterator
import os
from visualiser.ttitle import TTitleFile
from textual.containers import VerticalGroup, Center, HorizontalGroup
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Static, Label, ListView, ListItem, Button


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀▀░▀█▀░█░░░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█▀▀░░█░░█░░░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░░░▀▀▀░▀▀▀░▀▀▀
class TFile(ModalScreen):
    PATH = "./maps"
    BINDINGS = [
        ("q", "cancel", "Cancel"),
        ("c", "cancel", "Cancel"),
        ("escape", "cancel", "Cancel"),
    ]

    def __init__(self):
        super().__init__()
        self._title = TTitleFile()
        self._help = Label(
            "Files (.txt) stored in the './maps/' folder", classes="tfile_help"
        )
        self._list = ListView(classes="tfile_list")
        self._bt_go = Button("Go", variant="primary", classes="tfile_button")
        self._bt_cancel = Button(
            "Cancel", variant="default", classes="tfile_button"
        )

    # ########################################################################
    # ######################################################### LIST DIRS ####
    def list_dir(self, path: str) -> Iterator[str]:
        for entry in os.scandir(path):
            if entry.is_dir():
                yield from self.list_dir(entry.path)
            elif entry.is_file() and entry.path.endswith("txt"):
                yield entry.path

    def _init_choices(self):
        for path in self.list_dir("./maps/"):
            self._list.append(ListItem(TItemFile(path)))

    # ########################################################################
    # ########################################################### COMPOSE ####
    def compose(self) -> ComposeResult:
        with VerticalGroup(classes="tfile_layout"):
            yield self._title
            yield self._help
            yield self._list
            with HorizontalGroup(classes="tfile_bt_layout"):
                yield self._bt_cancel
                yield self._bt_go

    async def on_mount(self) -> None:
        self._init_choices()
        self._title.launch_animation()

    # ########################################################################
    # ############################################################ CANCEL ####
    def action_cancel(self):
        self.dismiss(None)


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░▀█▀░▀█▀░█▀▀░█▄█░░░█▀▀░▀█▀░█░░░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░░█░░░█░░█▀▀░█░█░░░█▀▀░░█░░█░░░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░░▀░░▀▀▀░▀░▀░░░▀░░░▀▀▀░▀▀▀░▀▀▀
class TItemFile(Label):
    def __init__(self, path: str):
        super().__init__(content=path[7:], classes="tfile_item")
        self.path = path
