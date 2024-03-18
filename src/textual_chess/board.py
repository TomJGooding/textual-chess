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

        board_str = self.board.__str__()
        ranks_strs = board_str.split("\n")
        for rank_idx, rank_str in enumerate(ranks_strs):
            for file_idx, square_symbol in enumerate(rank_str.split(" ")):
                if (file_idx + (rank_idx % 2)) % 2:
                    square_color = self.theme.dark_square_color
                else:
                    square_color = self.theme.light_square_color

                if square_symbol == ".":
                    square = UnoccupiedSquare()
                    square.styles.background = square_color
                    self.mount(square)
                else:
                    piece = Piece.from_symbol(square_symbol)
                    piece.styles.background = square_color
                    self.mount(piece)

    def make_move_from_san(self, san: str) -> None:
        self.board.push_san(san)
        self.update()
