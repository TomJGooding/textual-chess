import chess
from rich.console import RenderableType
from textual.widget import Widget

from textual_chess import board_themes
from textual_chess.pieces import (
    Bishop,
    King,
    Knight,
    Pawn,
    Piece,
    PieceColor,
    Queen,
    Rook,
)


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
        *,
        board: chess.Board | None = None,
        theme: board_themes.BoardTheme = board_themes.BROWN_THEME,
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

        board_str = self.board.__str__()
        ranks_strs = board_str.split("\n")
        for rank_idx, rank_str in enumerate(ranks_strs):
            for file_idx, square_str in enumerate(rank_str.split(" ")):
                if (file_idx + (rank_idx % 2)) % 2:
                    square_color = self.theme.dark_square_color
                else:
                    square_color = self.theme.light_square_color

                if square_str == ".":
                    square = UnoccupiedSquare()
                    square.styles.background = square_color
                    self.mount(square)
                    continue

                piece_color: PieceColor
                if square_str.isupper():
                    piece_color = "white"
                else:
                    piece_color = "black"

                piece_str = square_str.lower()
                piece: Piece
                if piece_str == "r":
                    piece = Rook(piece_color)
                elif piece_str == "n":
                    piece = Knight(piece_color)
                elif piece_str == "b":
                    piece = Bishop(piece_color)
                elif piece_str == "k":
                    piece = King(piece_color)
                elif piece_str == "q":
                    piece = Queen(piece_color)
                else:
                    piece = Pawn(piece_color)

                piece.styles.background = square_color
                self.mount(piece)
