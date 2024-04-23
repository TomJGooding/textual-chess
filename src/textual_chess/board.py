from __future__ import annotations

import chess
from rich.console import RenderableType
from textual import events
from textual.message import Message
from textual.reactive import var
from textual.widget import Widget

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
    DEFAULT_CSS = """
    ChessBoard {
        width: 64;
        height: 32;
        layout: grid;
        grid-size: 8;
        margin: 1;
    }

    ChessBoard .dark-square {
        background: #b58863;
    }

    ChessBoard .light-square {
        background: #f0d9b5;
    }
    """

    orientation: var[chess.Color] = var(chess.WHITE, init=False)

    class MovePlayed(Message):
        def __init__(
            self,
            chess_board: ChessBoard,
            move: chess.Move,
            san: str,
        ) -> None:
            super().__init__()
            self.move: chess.Move = move
            self.san: str = san
            self.chess_board: ChessBoard = chess_board

        @property
        def control(self) -> ChessBoard:
            return self.chess_board

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
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        self.board = board if board is not None else chess.Board()
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)

    def on_mount(self) -> None:
        self.update()

    def update(self) -> None:
        self.remove_children()
        orientation = self.orientation
        is_check = self.board.is_check()
        for rank_idx in range(7, -1, -1) if orientation else range(8):
            for file_idx in range(8) if orientation else range(7, -1, -1):
                square = chess.square(file_idx, rank_idx)
                square_name = chess.square_name(square)
                square_color = "light" if (rank_idx + file_idx) % 2 else "dark"
                chess_piece = self.board.piece_at(square)
                if chess_piece is None:
                    empty_square = EmptySquare()
                    empty_square.add_class(f"square-{square_name}")
                    empty_square.add_class(f"{square_color}-square")
                    self.mount(empty_square)
                else:
                    piece = Piece(chess_piece)
                    piece.add_class(f"square-{square_name}")
                    piece.add_class(f"{square_color}-square")
                    if (
                        is_check
                        and chess_piece.piece_type == chess.KING
                        and chess_piece.color == self.board.turn
                    ):
                        piece.styles.background = "red"
                    self.mount(piece)

    def make_move_from_san(self, san: str) -> None:
        move = self.board.parse_san(san)
        # We want the 'complete' final san, for example Qxf7# where the user
        # may have only entered Qf7.
        final_san = self.board.san(move)
        self.board.push(move)
        self.update()
        self.post_message(self.MovePlayed(self, move, final_san))

        outcome = self.board.outcome()
        if outcome is not None:
            self.post_message(self.GameOver(self, outcome))

    def flip(self) -> None:
        self.orientation = not self.orientation

    def watch_orientation(self) -> None:
        self.update()
