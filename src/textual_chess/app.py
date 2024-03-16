import chess
from textual import on
from textual.app import App, ComposeResult

from textual_chess.board import ChessBoard
from textual_chess.move_input import ChessMoveInput


class ChessApp(App):
    CSS = """
    Screen {
        align: center middle;
    }
    """

    def compose(self) -> ComposeResult:
        yield ChessBoard()
        yield ChessMoveInput()

    @on(ChessMoveInput.Submitted)
    def on_chess_move_submitted(self, event: ChessMoveInput.Submitted) -> None:
        board = self.query_one(ChessBoard)
        try:
            board.make_move_from_san(event.value)
        except chess.IllegalMoveError:
            event.input.set_class(True, "-invalid")
        else:
            event.input.clear()


if __name__ == "__main__":
    app = ChessApp()
    app.run()
