from textual.widgets import Label
from visualiser.ttitle import TTitleDebug
from textual.containers import VerticalGroup
from textual.app import ComposeResult
from textual.screen import ModalScreen


class TDebug(ModalScreen):
    BINDINGS = [
        ("escape", "cancel", "Quit"),
        ("enter", "cancel", "Quit"),
        ("q", "cancel", "Quit"),
    ]

    def __init__(self):
        super().__init__()
        self._tpaths = Label("paths", classes="tdebug_paths")
        self._tturn_table = Label("turn table", classes="tdebug_paths")

    # ########################################################################
    # ########################################################### COMPOSE ####
    def compose(self) -> ComposeResult:
        with VerticalGroup(classes="tdebug_layout"):
            yield TTitleDebug()
            with VerticalGroup(classes="tdebug_layout_group"):
                yield self._tpaths
            with VerticalGroup(classes="tdebug_layout_group"):
                yield self._tturn_table

    # ########################################################################
    # ############################################################ CANCEL ####
    def action_cancel(self) -> None:
        self.dismiss(None)
