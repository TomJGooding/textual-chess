import chess
from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer

from textual_chess.board import ChessBoard
from textual_chess.move_input import ChessMoveInput


class ChessApp(App):
    BINDINGS = [
        Binding("ctrl+x", "flip_board", "Flip board"),
    ]

    CSS = """
    Screen {
        align: center middle;
    }
    """

    def compose(self) -> ComposeResult:
        yield ChessBoard()
        yield ChessMoveInput()
        yield Footer()

    @on(ChessMoveInput.Submitted)
    def on_chess_move_submitted(self, event: ChessMoveInput.Submitted) -> None:
        board = self.query_one(ChessBoard)
        try:
            board.make_move_from_san(event.value)
        except chess.IllegalMoveError:
            event.input.set_class(True, "-invalid")
        else:
            event.input.clear()

    @on(ChessBoard.GameOver)
    def on_chess_board_game_over(self) -> None:
        self.query_one(ChessMoveInput).disabled = True

    def action_flip_board(self) -> None:
        self.query_one(ChessBoard).flip()


if __name__ == "__main__":
    app = ChessApp()
    app.run()
