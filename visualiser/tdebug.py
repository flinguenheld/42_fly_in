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

    def __init__(self, paths: List[List[Edge]] | None, table):
        super().__init__()
        self._tpaths = Label("paths", classes="tdebug_paths", markup=False)
        # self._tturn_table = Label(
        #     "turn table", classes="tdebug_paths", markup=False
        # )
        self._tturn_table = DataTable()

        self._shape_paths(paths)
        self._shape_table(table)

    def _shape_table(self, table: Dict[str, Dict[int, Edge]]) -> None:

        # self._tturn_table.fixed_rows = 2
        # self._tturn_table.fixed_columns = 20

        # if table:

        # self._tturn_table.update(str(table))

        # TODO: GET THE AMOUNT OF TURNS !
        nb_turns = 20

        def create_row(drone: str, path: Dict[int, Edge]):

            yield drone
            for i in range(1, nb_turns):
                if i in path:
                    yield path[i].name
                else:
                    yield " "

        for i in range(1, nb_turns + 1):
            self._tturn_table.add_column(str(i - 1))

        for drone, path in table.items():
            self._tturn_table.add_row(*[c for c in create_row(drone, path)])

    # ########################################################################
    # ####################################################### SHAPE PATHS ####
    def _shape_paths(self, paths: List[List[Edge]] | None) -> None:

        if paths:
            txt = f"--== {len(paths)} paths found ==--\n\n"

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
        else:
            self._tpaths.update("Nothing")

    # ########################################################################
    # ########################################################### COMPOSE ####
    def compose(self) -> ComposeResult:
        with VerticalGroup(classes="tdebug_layout"):
            yield TTitleDebug()
            with ScrollableContainer(classes="tdebug_layout_group"):
                yield self._tpaths
            with ScrollableContainer(classes="tdebug_layout_group"):
                yield self._tturn_table

    # ########################################################################
    # ############################################################ CANCEL ####
    def action_cancel(self) -> None:
        self.dismiss(None)
