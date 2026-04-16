import os
from typing import Iterator
from visualiser.ttitle import TTitleFile

from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Label, ListView, ListItem, Button
from textual.containers import VerticalGroup, HorizontalGroup


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀▀░▀█▀░█░░░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█▀▀░░█░░█░░░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░░░▀▀▀░▀▀▀░▀▀▀░░
class TFile(ModalScreen):
    PATH = "./maps"
    BINDINGS = [
        ("q", "cancel", "Cancel"),
        ("c", "cancel", "Cancel"),
        ("escape", "cancel", "Cancel"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self._ttitle = TTitleFile()
        self._thelp = Label(
            "Files (.txt) stored in the './maps/' folder", classes="tfile_help"
        )

        self._tlist = ListView(classes="tfile_list")
        self._terror = Label("Error", classes="tfile_error tfile_hidden")

        self._bt_go = Button("Go", variant="primary", classes="tfile_button")
        self._bt_cancel = Button(
            "Cancel", variant="default", classes="tfile_button"
        )

    # ########################################################################
    # ######################################################### LIST DIRS ####
    def list_dir(self, path: str) -> Iterator[str]:
        for entry in os.scandir(path):
            if entry.is_file() and entry.path.endswith("txt"):
                yield entry.path
            elif entry.is_dir():
                yield from self.list_dir(entry.path)

    def _init_choices(self) -> None:
        if os.path.isdir(self.PATH):
            for path in self.list_dir(self.PATH):
                self._tlist.append(TItemFile(path))

            if len(self._tlist) == 0:
                self._error("The folder 'maps' is empty !")
            else:
                self._tlist.action_cursor_down()
        else:
            self._error("The folder 'maps' does not exist !")

    # ########################################################################
    # ############################################################# ERROR ####
    def _error(self, txt: str) -> None:
        self._tlist.add_class("tfile_hidden")
        self._terror.remove_class("tfile_hidden")
        self._terror.update(txt)

    # ########################################################################
    # ########################################################### COMPOSE ####
    def compose(self) -> ComposeResult:
        with VerticalGroup(classes="tfile_layout"):
            yield self._ttitle
            yield self._thelp
            yield self._terror
            yield self._tlist
            with HorizontalGroup(classes="tfile_bt_layout"):
                yield self._bt_cancel
                yield self._bt_go

    async def on_mount(self) -> None:
        self._init_choices()

    # ########################################################################
    # ############################################################ CANCEL ####
    def action_cancel(self) -> None:
        self.dismiss(None)

    # ########################################################################
    # ########################################################### EVENTS #####
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button == self._bt_cancel:
            self.dismiss(None)
        if event.button == self._bt_go:
            self._dismiss_selection()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        self._dismiss_selection()

    def _dismiss_selection(self) -> None:
        item = self._tlist.highlighted_child
        if item and isinstance(item, TItemFile):
            self.dismiss(item.path)


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░▀█▀░▀█▀░█▀▀░█▄█░░░█▀▀░▀█▀░█░░░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░░█░░░█░░█▀▀░█░█░░░█▀▀░░█░░█░░░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░░▀░░▀▀▀░▀░▀░░░▀░░░▀▀▀░▀▀▀░▀▀▀
class TItemFile(ListItem):
    def __init__(self, path: str):
        super().__init__(
            Label(
                content=path[7:].replace("/", " / "),
                classes="tfile_item",
            )
        )
        self.path = path
