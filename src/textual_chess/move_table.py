from textual.app import ComposeResult
from textual.coordinate import Coordinate
from textual.widget import Widget
from textual.widgets import DataTable

MAX_SAN_LENGTH = 7


class MoveTable(Widget):
    DEFAULT_CSS = """
    MoveTable {
        width: 23;
        min-width: 23;
        background: $panel;
    }
    """

    ply: int = 0
    fullmove_number: int = 0

    def compose(self) -> ComposeResult:
        yield DataTable(show_header=False)

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_column("White", key="white", width=MAX_SAN_LENGTH)
        table.add_column("Black", key="black", width=MAX_SAN_LENGTH)

    def add_move(self, san: str) -> None:
        table = self.query_one(DataTable)
        self.ply += 1
        if self.ply % 2:
            self.fullmove_number += 1
            table.add_row(
                san,
                label=f"{self.fullmove_number : ^3}",
                key=f"move-{self.fullmove_number}",
            )
        else:
            table.update_cell(
                row_key=f"move-{self.fullmove_number}",
                column_key="black",
                value=san,
            )

        self.highlight_last_move()

    def highlight_last_move(self) -> None:
        table = self.query_one(DataTable)
        table.cursor_coordinate = Coordinate(
            self.fullmove_number,
            self.ply % 2 == 0,
        )
