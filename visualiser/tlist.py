from typing import List

from algo.turn_table import TurnTable
from visualiser.ttitle import TTitleList

from textual.widgets import Label
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.containers import VerticalGroup, ScrollableContainer


class TList(ModalScreen):
    BINDINGS = [
        ("escape", "cancel", "Quit"),
        ("enter", "cancel", "Quit"),
        ("d", "cancel", "Quit"),
        ("q", "cancel", "Quit"),
    ]

    def __init__(
        self,
        file_path: str,
        drones: List[str],
        table: TurnTable,
        current_turn: int,
    ) -> None:
        super().__init__()

        self._tinfo = self._fill_info(file_path, drones, table, current_turn)
        self._toutput = self._fill_output(drones, table, current_turn)

    # ########################################################################
    # ####################################################### FILL OUTPUT ####
    def _fill_info(
        self,
        file_path: str,
        drones: List[str],
        table: TurnTable,
        current_turn: int,
    ) -> Label:
        text = f"{file_path}"
        text += f"\n{len(drones)} drones"
        text += f"\n turn {current_turn} on {table.nb_turns}"

        return Label(text, markup=False, classes="tlist_info")

    # ########################################################################
    # ####################################################### FILL OUTPUT ####
    def _fill_output(
        self,
        drones: List[str],
        table: TurnTable,
        current_turn: int,
    ) -> Label:
        text = ""

        for turn in range(1, current_turn + 1):
            turn_moves = table.get_turn(turn, with_duplicates=False)
            line = ""
            for drone in drones:
                if drone in turn_moves:
                    to = turn_moves[drone]

                    if to:
                        if to.first_on_restricted_zone:
                            line += (
                                f"{drone}-{to.hub_from.name}/{to.hub_to.name} "
                            )

                        else:
                            line += f"{drone}-{to.hub_to.name} "

            if line:
                text += f"{line}\n"

        if not text:
            text = "This widget will display each movements as follow:\n"
            text += "D<ID>-<zone>, or D<ID>-<connection>\n"
            text += "One line per turn"

        return Label(text, markup=False, classes="tlist_turns")

    # ########################################################################
    # ########################################################### COMPOSE ####
    def compose(self) -> ComposeResult:
        with VerticalGroup(classes="tlist_layout"):
            yield TTitleList()
            with ScrollableContainer():
                yield self._tinfo
                yield self._toutput

    # ########################################################################
    # ############################################################ CANCEL ####
    def action_cancel(self) -> None:
        self.dismiss(None)
