from __future__ import annotations

import chess
from rich.console import RenderableType
from textual.widget import Widget

from textual_chess import ascii_pieces

ASCII_PIECES = {
    chess.KING: ascii_pieces.KING,
    chess.QUEEN: ascii_pieces.QUEEN,
    chess.ROOK: ascii_pieces.ROOK,
    chess.BISHOP: ascii_pieces.BISHOP,
    chess.KNIGHT: ascii_pieces.KNIGHT,
    chess.PAWN: ascii_pieces.PAWN,
}


class Piece(Widget):
    def __init__(
        self,
        piece_type: chess.PieceType,
        color: chess.Color,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.piece_type = piece_type
        self.color = color
        self.styles.color = "white" if color else "black"

    def render(self) -> RenderableType:
        return ASCII_PIECES[self.piece_type]

    @classmethod
    def from_symbol(cls, symbol: str) -> Piece:
        return cls(chess.PIECE_SYMBOLS.index(symbol.lower()), symbol.isupper())
