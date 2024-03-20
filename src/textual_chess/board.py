from __future__ import annotations

import chess
from rich.console import RenderableType
from textual.message import Message
from textual.reactive import var
from textual.widget import Widget

from textual_chess import board_themes
from textual_chess.piece import Piece


class EmptySquare(Widget):
    DEFAULT_CSS = """
    Unoccupied {
        width: 8;
        height: 4;
    }
    """

    def render(self) -> RenderableType:
        return ""


class ChessBoard(Widget):

    orientation: var[chess.Color] = var(chess.WHITE, init=False)

    DEFAULT_CSS = """
    ChessBoard {
        width: 64;
        height: 32;
        layout: grid;
        grid-size: 8;
        margin: 1;
    }
    """

    class GameOver(Message):
        def __init__(
            self,
            chess_board: ChessBoard,
            outcome: chess.Outcome,
        ) -> None:
            super().__init__()
            self.outcome: chess.Outcome = outcome
            self.chess_board: ChessBoard = chess_board

        @property
        def control(self) -> ChessBoard:
            return self.chess_board

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
        orientation = self.orientation
        is_check = self.board.is_check()
        for rank_index in range(7, -1, -1) if orientation else range(8):
            for file_index in range(8) if orientation else range(7, -1, -1):
                square = chess.square(file_index, rank_index)
                square_color = (
                    self.theme.light_square_color
                    if (rank_index + file_index) % 2
                    else self.theme.dark_square_color
                )
                chess_piece = self.board.piece_at(square)
                if chess_piece is None:
                    empty_square = EmptySquare()
                    empty_square.styles.background = square_color
                    self.mount(empty_square)
                else:
                    piece = Piece(chess_piece)
                    if (
                        is_check
                        and chess_piece.piece_type == chess.KING
                        and chess_piece.color == self.board.turn
                    ):
                        piece.styles.background = "red"
                    else:
                        piece.styles.background = square_color
                    self.mount(piece)

    def make_move_from_san(self, san: str) -> None:
        self.board.push_san(san)
        self.update()

        outcome = self.board.outcome()
        if outcome is not None:
            self.post_message(self.GameOver(self, outcome))

    def flip(self) -> None:
        self.orientation = not self.orientation

    def watch_orientation(self) -> None:
        self.update()
