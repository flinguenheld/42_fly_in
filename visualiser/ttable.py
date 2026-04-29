from typing import List, Iterator

from models.hub import Hub
from models.edge import Edge
from algo.turn_table import TurnTable
from visualiser.ttitle import TTitleTable

from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Label, DataTable
from textual.containers import VerticalGroup, ScrollableContainer


class TTable(ModalScreen):
    BINDINGS = [
        ("escape", "cancel", "Quit"),
        ("enter", "cancel", "Quit"),
        ("d", "cancel", "Quit"),
        ("q", "cancel", "Quit"),
    ]

    def __init__(
        self,
        paths: List[List[Edge]] | None,
        drones: List[str],
        table: TurnTable,
        current_turn: int,
    ) -> None:
        super().__init__()
        self._tpaths_lay = ScrollableContainer(classes="ttable_layout_paths")
        self._tpaths = Label("paths", classes="ttable_field", markup=False)

        self._ttable_lay = ScrollableContainer(classes="ttable_layout_table")
        self._ttable: DataTable[str] = DataTable(classes="ttable_field")

        self._fill_paths(paths)
        self._fill_table(drones, table)

        # Table styles --
        self._ttable.zebra_stripes = True
        self._ttable.cursor_type = "column"
        self._ttable.move_cursor(column=current_turn + 1)

    # ########################################################################
    # ####################################################### SHAPE TABLE ####
    def _fill_table(self, drones: List[str], table: TurnTable) -> None:

        # ###################################### CREATE ROW ####
        def create_row(drone: str, table: TurnTable) -> Iterator[str]:
            yield drone
            yield table.paths[0][0].hub_from.name

            for where in table.drone_iterator(drone):
                if where:
                    if where.first_on_restricted_zone:
                        yield f"{where.hub_to.name} (on edge)"
                    else:
                        yield where.hub_to.name
                else:
                    yield " "

        # ######################################################
        self._ttable_lay.border_title = f"Done in {table.nb_turns} turns"

        self._ttable.add_column("Drones\\Turns")

        for i in range(2, table.nb_turns + 3):
            self._ttable.add_column(str(i - 2))

        for drone in drones:
            self._ttable.add_row(*[c for c in create_row(drone, table)])

    # ########################################################################
    # ####################################################### SHAPE PATHS ####
    def _fill_paths(self, paths: List[List[Edge]] | None) -> None:

        if paths:
            txt = ""

            for path in paths:
                line = "Start"
                if path:
                    for edge in path:
                        if edge.hub_to.zone == Hub.Zone.RESTRICTED:
                            line += f" -> (R) {edge.hub_to.name}"
                        else:
                            line += f" -> {edge.hub_to.name}"

                txt += f"{line}\n"

            self._tpaths.update(txt)
            self._tpaths_lay.border_title = f"{len(paths)} paths found"
        else:
            self._tpaths.update("Nothing")

    # ########################################################################
    # ########################################################### COMPOSE ####
    def compose(self) -> ComposeResult:
        with VerticalGroup(classes="ttable_layout"):
            yield TTitleTable()
            with self._tpaths_lay:
                yield self._tpaths
            with self._ttable_lay:
                yield self._ttable

    # ########################################################################
    # ############################################################ CANCEL ####
    def action_cancel(self) -> None:
        self.dismiss(None)
