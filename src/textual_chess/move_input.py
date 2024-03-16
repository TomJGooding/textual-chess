from __future__ import annotations

import chess
from textual import on
from textual.validation import ValidationResult, Validator
from textual.widgets import Input

MAX_SAN_LENGTH = 7


class ChessSAN(Validator):
    def validate(self, value: str) -> ValidationResult:
        if self.is_valid_san(value):
            return self.success()
        else:
            return self.failure()

    @staticmethod
    def is_valid_san(value: str) -> bool:
        match = chess.SAN_REGEX.match(value)
        if not match:
            return False
        return True


class ChessMoveInput(Input):
    DEFAULT_CSS = """
    ChessMoveInput {
        width: 14;
    }
    """

    def __init__(
        self,
        value: str | None = None,
        placeholder: str = "",
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(
            value,
            placeholder,
            highlighter=None,
            password=False,
            restrict=None,
            type="text",
            max_length=MAX_SAN_LENGTH,
            suggester=None,
            validators=[ChessSAN()],
            validate_on=["submitted"],
            valid_empty=False,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
        )

    @on(Input.Submitted)
    def on_chess_move_submitted(self, event: ChessMoveInput.Submitted) -> None:
        assert event.validation_result is not None
        if not event.validation_result.is_valid:
            event.stop()
