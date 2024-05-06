import chess
from rich.console import RenderableType
from textual.widget import Widget

from textual_chess.ascii_pieces import ASCII_PIECES


class Piece(Widget):
    DEFAULT_CSS = """
    Piece {
        width: 8;
        height: 4;
    }
    """

    def __init__(
        self,
        chess_piece: chess.Piece,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.chess_piece = chess_piece
        self.styles.color = "white" if chess_piece.color else "black"

    def render(self) -> RenderableType:
        return ASCII_PIECES[self.chess_piece.piece_type]
