from textual.app import App, ComposeResult

from textual_chess.board import ChessBoard


class ChessApp(App):
    CSS = """
    Screen {
        align: center middle;
    }
    """

    def compose(self) -> ComposeResult:
        yield ChessBoard()


if __name__ == "__main__":
    app = ChessApp()
    app.run()
