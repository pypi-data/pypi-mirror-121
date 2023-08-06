from typing import Callable
from color import foreground, background, style


class Option:
    def __init__(
        self,
        title: str,
        function: Callable,
        exit: bool = False,
        cursor: str = ">",
        foreground_color: str = foreground.RESET,
        background_color: str = background.RESET,
        style: str = style.NORMAL,
        highlight_fg_color: str = foreground.BLUE,
        highlight_bg_color: str = background.RESET,
        highlight_style: str = style.NORMAL,
    ) -> None:

        self.active = True

        self.title = title
        self.function = function
        self.exit = exit

        self.foreground_color = foreground_color
        self.background_color = background_color
        self.style = style

        self.highlight_fg_color = highlight_fg_color
        self.highlight_bg_color = highlight_bg_color
        self.highlight_style = highlight_style

        self.cursor = cursor

    def __str__(self) -> str:
        if self.active:
            pre_set = (
                self.highlight_fg_color
                + self.highlight_bg_color
                + self.highlight_style
                + self.cursor
                + " "
            )
        else:
            pre_set = self.foreground_color + self.background_color + self.style + "  "

        return f"{pre_set}{self.title}{style.RESET_ALL}"
