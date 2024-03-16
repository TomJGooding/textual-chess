from dataclasses import dataclass

from textual.color import Color


@dataclass
class BoardTheme:
    dark_square_color: Color
    light_square_color: Color


BROWN_THEME = BoardTheme(
    dark_square_color=Color(181, 136, 99),
    light_square_color=Color(240, 217, 181),
)

BLUE_THEME = BoardTheme(
    dark_square_color=Color(140, 162, 173),
    light_square_color=Color(222, 227, 230),
)
