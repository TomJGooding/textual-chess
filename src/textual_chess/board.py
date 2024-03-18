import chess
from rich.console import RenderableType
from textual.widget import Widget

from textual_chess import board_themes
from textual_chess.piece import Piece


class UnoccupiedSquare(Widget):
    DEFAULT_CSS = """
    Unoccupied {
        width: 8;
        height: 4;
    }
    """

    def render(self) -> RenderableType:
        return ""


class ChessBoard(Widget):
    DEFAULT_CSS = """
    ChessBoard {
        width: 64;
        height: 32;
        layout: grid;
        grid-size: 8;
        margin: 1;
    }
    """

    def __init__(
        self,
        board: chess.Board | None = None,
        theme: board_themes.BoardTheme = board_themes.BROWN_THEME,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        self.board = board if board is not None else chess.Board()
        self.theme = theme
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)

    def on_mount(self) -> None:
        self.update()

    def update(self) -> None:
        self.remove_children()
        for square in chess.SQUARES_180:
            square_color = (
                self.theme.light_square_color
                if (chess.square_rank(square) + chess.square_file(square)) % 2
                else self.theme.dark_square_color
            )
            chess_piece = self.board.piece_at(square)
            if chess_piece is None:
                unoccupied_square = UnoccupiedSquare()
                unoccupied_square.styles.background = square_color
                self.mount(unoccupied_square)
            else:
                piece = Piece(chess_piece)
                piece.styles.background = square_color
                self.mount(piece)

    def make_move_from_san(self, san: str) -> None:
        self.board.push_san(san)
        self.update()
