from textual.app import ComposeResult
from textual.widgets import Static, Button
from textual.containers import (
    HorizontalGroup,
    HorizontalScroll,
)


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀█░█▀▀░▀█▀░▀█▀░█▀█░█▀█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█▀█░█░░░░█░░░█░░█░█░█░█░▀▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░░▀░░▀▀▀░▀▀▀░▀░▀░▀▀▀░░
class TActions(Static):
    def __init__(self) -> None:

        super().__init__()
        self._previous = Button(
            "(P)revious",
            flat=True,
            variant="success",
            classes="bt_actions",
        )
        self._run = Button(
            "R(u)n",
            flat=True,
            variant="primary",
            classes="bt_actions",
        )
        self._next = Button(
            "(N)ext",
            flat=True,
            variant="success",
            classes="bt_actions",
        )

        self._file_selection = Button(
            "(F)ile selector",
            flat=True,
            variant="primary",
            classes="bt_actions",
        )
        self._restart = Button(
            "(R)estart",
            flat=True,
            variant="primary",
            classes="bt_actions",
        )

        self._list = Button(
            "(L)ist",
            flat=True,
            variant="default",
            classes="bt_actions",
        )
        self._table = Button(
            "T(A)ble",
            flat=True,
            variant="warning",
            classes="bt_actions",
        )

        self._theme = Button(
            "(T)heme",
            flat=True,
            variant="primary",
            classes="bt_actions",
        )
        self._quit = Button(
            "(Q)uit",
            flat=True,
            variant="default",
            classes="bt_actions",
        )

    # ########################################################################
    # ############################################## UP RUN BUTTON LABEL #####
    def up_run_button(self, is_running_all: bool) -> None:
        if is_running_all:
            self._run.variant = "error"
            self._run.label = "Stop r(u)nning"
        else:
            self._run.variant = "primary"
            self._run.label = "R(u)n"

    # ########################################################################
    # ########################################################## COMPOSE #####
    def compose(self) -> ComposeResult:
        with HorizontalScroll(id="amain_layout"):
            with HorizontalGroup(classes="alayout_group alayout_success"):
                yield self._previous
                yield self._run
                yield self._next
            with HorizontalGroup(classes="alayout_group alayout_primary"):
                yield self._file_selection
                yield self._restart
            with HorizontalGroup(classes="alayout_group alayout_warning"):
                yield self._list
                yield self._table
            with HorizontalGroup(classes="alayout_group alayout_primary"):
                yield self._theme
                yield self._quit

    # ########################################################################
    # ########################################################## ACTIONS #####
    async def on_button_pressed(self, event: Button.Pressed) -> None:

        if event.button == self._previous:
            await self.app.run_action("previous_turn")

        # TODO: ADD that
        if event.button == self._run:
            await self.app.run_action("run")

        if event.button == self._next:
            await self.app.run_action("next_turn")

        if event.button == self._file_selection:
            await self.app.run_action("file_selection")

        if event.button == self._restart:
            await self.app.run_action("restart")

        if event.button == self._list:
            await self.app.run_action("list")

        if event.button == self._table:
            await self.app.run_action("table")

        if event.button == self._theme:
            await self.app.run_action("next_theme")

        if event.button == self._quit:
            await self.app.run_action("quit")
