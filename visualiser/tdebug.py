from algo.turn_table import TurnTable
from models.hub import Hub
from typing import List, Dict
from models.edge import Edge
from textual.widgets import Label, DataTable
from visualiser.ttitle import TTitleDebug
from textual.containers import VerticalGroup, ScrollableContainer
from textual.app import ComposeResult
from textual.screen import ModalScreen


class TDebug(ModalScreen):
    BINDINGS = [
        ("escape", "cancel", "Quit"),
        ("enter", "cancel", "Quit"),
        ("q", "cancel", "Quit"),
    ]

    def __init__(self, paths: List[List[Edge]] | None, drones, table):
        super().__init__()
        self._tpaths_lay = ScrollableContainer(classes="tdebug_layout_paths")
        self._tpaths = Label("paths", classes="tdebug_field", markup=False)

        self._ttable_lay = ScrollableContainer(classes="tdebug_layout_table")
        self._ttable = DataTable(classes="tdebug_field")

        self._shape_paths(paths)
        self._shape_table(drones, table)

    # ########################################################################
    # ####################################################### SHAPE TABLE ####
    def _shape_table(self, drones, table: TurnTable) -> None:

        # ###################################### CREATE ROW ####
        def create_row(drone: str, table):
            yield drone
            for where in table.drone_iterator(drone):
                if where:
                    yield where.name
                else:
                    yield " "

        # ######################################################
        self._ttable_lay.border_title = f"Done in {table.nb_turns} turns"

        self._ttable.add_column("Drones\\Turns")
        self._ttable.zebra_stripes = True

        for i in range(2, table.nb_turns + 2):
            self._ttable.add_column(str(i - 1))

        for drone in drones:
            self._ttable.add_row(*[c for c in create_row(drone, table)])

    # ########################################################################
    # ####################################################### SHAPE PATHS ####
    def _shape_paths(self, paths: List[List[Edge]] | None) -> None:

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
        with VerticalGroup(classes="tdebug_layout"):
            yield TTitleDebug()
            with self._tpaths_lay:
                yield self._tpaths
            with self._ttable_lay:
                yield self._ttable

    # ########################################################################
    # ############################################################ CANCEL ####
    def action_cancel(self) -> None:
        self.dismiss(None)
