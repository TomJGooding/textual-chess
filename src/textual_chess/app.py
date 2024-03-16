from textual.app import App, ComposeResult
from textual.containers import Grid

from textual_chess.pieces import Bishop, King, Knight, Pawn, Queen, Rook


class ChessApp(App):
    CSS = """
    Screen {
        align: center middle;
    }

    Grid {
        width: 64;
        height: 16;
        grid-size: 8 4;
        background: green;
    }
    """

    def compose(self) -> ComposeResult:
        with Grid():
            yield Rook("black")
            yield Knight("black")
            yield Bishop("black")
            yield Queen("black")
            yield King("black")
            yield Bishop("black")
            yield Knight("black")
            yield Rook("black")
            for _ in range(8):
                yield Pawn("black")

            for _ in range(8):
                yield Pawn("white")
            yield Rook("white")
            yield Knight("white")
            yield Bishop("white")
            yield Queen("white")
            yield King("white")
            yield Bishop("white")
            yield Knight("white")
            yield Rook("white")


if __name__ == "__main__":
    app = ChessApp()
    app.run()
