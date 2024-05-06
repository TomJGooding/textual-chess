import chess
from textual import events, on
from textual.app import ComposeResult
from textual.geometry import Offset
from textual.screen import ModalScreen
from textual.widgets import ListItem, ListView

from textual_chess.piece import Piece


class PromotionOptions(ListView, inherit_bindings=False):
    DEFAULT_CSS = """
    PromotionOptions {
        width: 8;
        height: 16;
    }

    PromotionOptions ListItem > Widget :hover {
        background: #cf6120;
    }
    """

    def __init__(
        self,
        piece_color: chess.Color,
        board_orientation: chess.Color,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        pieces = [
            Piece(chess.Piece(piece_type, piece_color))
            for piece_type in [
                chess.QUEEN,
                chess.KNIGHT,
                chess.ROOK,
                chess.BISHOP,
            ]
        ]
        if board_orientation is not piece_color:
            pieces.reverse()
        super().__init__(
            *[ListItem(piece) for piece in pieces],
            initial_index=None,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
        )


class PromotionModalScreen(ModalScreen[chess.PieceType | None]):
    CSS = """
    PromotionModalScreen {
        align: left top;
    }
    """

    def __init__(
        self,
        piece_color: chess.Color,
        board_orientation: chess.Color,
        square_offset: Offset,
    ) -> None:
        self.piece_color = piece_color
        self.board_orientation = board_orientation
        self.square_offset = square_offset
        super().__init__()

    def compose(self) -> ComposeResult:
        yield PromotionOptions(
            piece_color=self.piece_color,
            board_orientation=self.board_orientation,
        )

    def on_mount(self) -> None:
        content_offset = self.square_offset
        if self.board_orientation is not self.piece_color:
            content_offset -= Offset(0, 12)
        self.query_one(PromotionOptions).offset = content_offset

    @on(PromotionOptions.Selected)
    def on_promotion_piece_selected(
        self,
        event: PromotionOptions.Selected,
    ) -> None:
        selected_piece = event.item.query_one(Piece)
        piece_type = selected_piece.chess_piece.piece_type
        self.dismiss(piece_type)

    def on_click(self, event: events.Click) -> None:
        clicked, _ = self.get_widget_at(event.screen_x, event.screen_y)
        # Dismiss the screen if the user clicks outside the modal content
        # (i.e. the darkened background)
        if clicked is self:
            self.dismiss(None)
