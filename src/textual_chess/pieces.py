from rich.console import RenderableType
from textual.widget import Widget
from typing_extensions import Literal

from textual_chess import pieces_ascii

PieceColor = Literal["white", "black"]


class Piece(Widget):
    DEFAULT_CSS = """
    Piece {
        width: 8;
        height: 4;
    }
    """

    def __init__(
        self,
        color: PieceColor,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.styles.color = color


class King(Piece):
    def render(self) -> RenderableType:
        return pieces_ascii.KING_ASCII


class Queen(Piece):
    def render(self) -> RenderableType:
        return pieces_ascii.QUEEN_ASCII


class Rook(Piece):
    def render(self) -> RenderableType:
        return pieces_ascii.ROOK_ASCII


class Bishop(Piece):
    def render(self) -> RenderableType:
        return pieces_ascii.BISHOP_ASCII


class Knight(Piece):
    def render(self) -> RenderableType:
        return pieces_ascii.KNIGHT_ASCII


class Pawn(Piece):
    def render(self) -> RenderableType:
        return pieces_ascii.PAWN_ASCII
