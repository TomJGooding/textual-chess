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

    ChessBoard .hovered-legal-move-square {
        background: yellow;
    }

    ChessBoard .selected-piece {
        background: green;
    }
    """

    orientation: var[chess.Color] = var(chess.WHITE, init=False)
    selected_piece: var[Piece | None] = var[Piece | None](None)
    selected_piece_legal_moves: list[str] | None = None
    hovered_legal_move_square: var[Piece | EmptySquare | None] = var[
        Piece | EmptySquare | None
    ](None)

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
        self.selected_piece = None
        self.hovered_legal_move_square = None
        self.selected_piece_legal_moves = None
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

    def make_move_from_uci(self, uci: str) -> None:
        move = self.board.parse_uci(uci)
        final_san = self.board.san(move)
        self.board.push(move)
        self.update()
        self.post_message(self.MovePlayed(self, move, final_san))

        outcome = self.board.outcome()
        if outcome is not None:
            self.post_message(self.GameOver(self, outcome))

    def on_click(self, event: events.Click) -> None:
        clicked, _ = self.screen.get_widget_at(
            event.screen_x,
            event.screen_y,
        )
        assert isinstance(clicked, (Piece, EmptySquare))
        if self.selected_piece is not None:
            piece_square_name = self.get_square_name(self.selected_piece)
            clicked_square_name = self.get_square_name(clicked)
            assert self.selected_piece_legal_moves is not None
            if clicked_square_name in self.selected_piece_legal_moves:
                move = f"{piece_square_name}{clicked_square_name}"
                self.make_move_from_uci(move)
                return

        if not isinstance(clicked, Piece):
            self.selected_piece = None
            return
        if (
            clicked.chess_piece.color == self.board.turn
            and clicked != self.selected_piece
        ):
            self.selected_piece = clicked
        else:
            self.selected_piece = None

    def get_square_name(self, square: Piece | EmptySquare) -> str:
        square_name: str = ""
        for class_ in square.classes:
            if class_.startswith("square-"):
                square_name = class_[7:]
                break
        return square_name

    def watch_selected_piece(
        self,
        old_selected: Piece | None,
        new_selected: Piece | None,
    ) -> None:
        if old_selected is not None:
            old_selected.set_class(False, "selected-piece")
        if new_selected is not None:
            new_selected.set_class(True, "selected-piece")
            square_name = self.get_square_name(new_selected)
            self.selected_piece_legal_moves = [
                chess.square_name(move.to_square)
                for move in self.board.legal_moves
                if move.from_square == chess.parse_square(square_name)
            ]
        else:
            self.selected_piece_legal_moves = None

    def on_mouse_move(self, event: events.MouseMove) -> None:
        if self.selected_piece_legal_moves is None:
            return
        hovered, _ = self.screen.get_widget_at(
            event.screen_x,
            event.screen_y,
        )
        assert isinstance(hovered, (Piece, EmptySquare))
        square_name = self.get_square_name(hovered)
        if square_name in self.selected_piece_legal_moves:
            self.hovered_legal_move_square = hovered
        else:
            self.hovered_legal_move_square = None

    def watch_hovered_legal_move_square(
        self,
        old_hovered: Piece | EmptySquare | None,
        new_hovered: Piece | EmptySquare | None,
    ) -> None:
        if old_hovered is not None:
            old_hovered.set_class(False, "hovered-legal-move-square")
        if new_hovered is not None:
            new_hovered.set_class(True, "hovered-legal-move-square")

    def flip(self) -> None:
        self.orientation = not self.orientation

    def watch_orientation(self) -> None:
        self.update()
