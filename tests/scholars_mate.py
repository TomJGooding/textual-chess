from textual.app import App, ComposeResult

from textual_chess.board import ChessBoard

SCHOLARS_MATE = iter(["e4", "e5", "Qh5", "Nc6", "Bc4", "Nf6", "Qxf7#"])


class ScholarsMateApp(App):
    BINDINGS = [("space", "next_move")]

    CSS = """
    Screen {
        align: center middle;
    }
    """

    def compose(self) -> ComposeResult:
        yield ChessBoard()

    def action_next_move(self) -> None:
        board = self.query_one(ChessBoard)
        next_move = next(SCHOLARS_MATE, None)
        if next_move is not None:
            board.make_move_from_san(next_move)


if __name__ == "__main__":
    app = ScholarsMateApp()
    app.run()
