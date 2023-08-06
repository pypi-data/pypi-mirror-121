from __future__ import annotations


# Control Sequence Introducer
CSI = '\u001b['
FIN = 'm'


def csi_seq(sgr: int) -> str:
    """Returns a CSI sequence.

    Parameters
    ----------
    sgr: int
        Select Graphic Rendition parameters
    
    Returns
    -------
    str
        Resulting CSI sequence.
    """
    return f'{CSI}{sgr}{FIN}'


class Colorant:
    """Adds colors and effects to texts in console."""

    # Resets all colors and effects
    RESET = csi_seq(0)

    def __init__(self):
        self._buf = []
        self.reset()

    def __repr__(self) -> str:
        return f'{self.__class__}({self.__dict__})'

    def __str__(self) -> str:
        text = self.reset()._join()
        self._buf.pop()
        return text

    def flush(self, end: str = '\n') -> Colorant:
        """Flush escape sequences and texts from buffer to console.

        Parameters
        ----------
        end: str, default: '\n'
            Ending character.
        
        Returns
        -------
        Colorant
            Current instance.
        """
        print(self.reset()._join(), end=end)
        self._buf.clear()
        return self.reset()

    def err(self, text: str) -> Colorant:
        """Theme for error messages.

        Parameters
        ----------
        text: str
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self.bg_lt_red().lt_white(text)

    def ok(self, text: str) -> Colorant:
        """Theme for okay messages.

        Parameters
        ----------
        text: str
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self.bg_lt_green().black(text)

    def warn(self, text: str) -> Colorant:
        """Theme for warning messages.

        Parameters
        ----------
        text: str
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self.bg_lt_yellow().black(text)

    def info(self, text: str) -> Colorant:
        """Theme for info messages.

        Parameters
        ----------
        text: str
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self.bg_lt_blue().lt_white(text)
    
    def text(self, text: str) -> Colorant:
        """Adds text to buffer.

        Parameters
        ----------
        text: str
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self._add(text)

    def reset(self) -> Colorant:
        """Resets all colors and effects.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self._add(Colorant.RESET)

    def default(self, text: str = None) -> Colorant:
        """Resets the foreground color.

        Parameters
        ----------
        text: str, optional
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self._add(Foreground.DEFAULT, text)

    def black(self, text: str = None) -> Colorant:
        """Sets the foreground color to black.

        Parameters
        ----------
        text: str, optional
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self._add(Foreground.BLACK, text)

    def red(self, text: str = None) -> Colorant:
        """Sets the foreground color to red.

        Parameters
        ----------
        text: str, optional
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self._add(Foreground.RED, text)

    def green(self, text: str = None) -> Colorant:
        """Sets the foreground color to green.

        Parameters
        ----------
        text: str, optional
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self._add(Foreground.GREEN, text)

    def yellow(self, text: str = None) -> Colorant:
        """Sets the foreground color to yellow.

        Parameters
        ----------
        text: str, optional
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self._add(Foreground.YELLOW, text)

    def blue(self, text: str = None) -> Colorant:
        """Sets the foreground color to blue.

        Parameters
        ----------
        text: str, optional
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self._add(Foreground.BLUE, text)

    def magenta(self, text: str = None) -> Colorant:
        """Sets the foreground color to magenta.

        Parameters
        ----------
        text: str, optional
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self._add(Foreground.MAGENTA, text)

    def cyan(self, text: str = None) -> Colorant:
        """Sets the foreground color to cyan.

        Parameters
        ----------
        text: str, optional
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self._add(Foreground.CYAN, text)

    def white(self, text: str = None) -> Colorant:
        """Sets the foreground color to white.

        Parameters
        ----------
        text: str, optional
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self._add(Foreground.WHITE, text)

    def lt_black(self, text: str = None) -> Colorant:
        """Sets the foreground color to light black.

        Parameters
        ----------
        text: str, optional
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self._add(Foreground.LT_BLACK, text)

    def lt_red(self, text: str = None) -> Colorant:
        """Sets the foreground color to light red.

        Parameters
        ----------
        text: str, optional
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self._add(Foreground.LT_RED, text)

    def lt_green(self, text: str = None) -> Colorant:
        """Sets the foreground color to light green.

        Parameters
        ----------
        text: str, optional
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self._add(Foreground.LT_GREEN, text)

    def lt_yellow(self, text: str = None) -> Colorant:
        """Sets the foreground color to light yellow.

        Parameters
        ----------
        text: str, optional
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self._add(Foreground.LT_YELLOW, text)

    def lt_blue(self, text: str = None) -> Colorant:
        """Sets the foreground color to light blue.

        Parameters
        ----------
        text: str, optional
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self._add(Foreground.LT_BLUE, text)

    def lt_magenta(self, text: str = None) -> Colorant:
        """Sets the foreground color to light magenta.

        Parameters
        ----------
        text: str, optional
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self._add(Foreground.LT_MAGENTA, text)

    def lt_cyan(self, text: str = None) -> Colorant:
        """Sets the foreground color to light cyan.

        Parameters
        ----------
        text: str, optional
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self._add(Foreground.LT_CYAN, text)

    def lt_white(self, text: str = None) -> Colorant:
        """Sets the foreground color to light white.

        Parameters
        ----------
        text: str, optional
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self._add(Foreground.LT_WHITE, text)

    def bg_default(self, text: str = None) -> Colorant:
        """Resets the background color.

        Parameters
        ----------
        text: str, optional
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self._add(Background.DEFAULT, text)

    def bg_black(self, text: str = None) -> Colorant:
        """Sets the background color to black.

        Parameters
        ----------
        text: str, optional
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self._add(Background.BLACK, text)

    def bg_red(self, text: str = None) -> Colorant:
        """Sets the background color to red.

        Parameters
        ----------
        text: str, optional
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self._add(Background.RED, text)

    def bg_green(self, text: str = None) -> Colorant:
        """Sets the background color to green.

        Parameters
        ----------
        text: str, optional
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self._add(Background.GREEN, text)

    def bg_yellow(self, text: str = None) -> Colorant:
        """Sets the background color to yellow.

        Parameters
        ----------
        text: str, optional
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self._add(Background.YELLOW, text)

    def bg_blue(self, text: str = None) -> Colorant:
        """Sets the background color to blue.

        Parameters
        ----------
        text: str, optional
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self._add(Background.BLUE, text)

    def bg_magenta(self, text: str = None) -> Colorant:
        """Sets the background color to magenta.

        Parameters
        ----------
        text: str, optional
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self._add(Background.MAGENTA, text)

    def bg_cyan(self, text: str = None) -> Colorant:
        """Sets the background color to cyan.

        Parameters
        ----------
        text: str, optional
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self._add(Background.CYAN, text)

    def bg_white(self, text: str = None) -> Colorant:
        """Sets the background color to white.

        Parameters
        ----------
        text: str, optional
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self._add(Background.WHITE, text)

    def bg_lt_black(self, text: str = None) -> Colorant:
        """Sets the background color to light black.

        Parameters
        ----------
        text: str, optional
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self._add(Background.LT_BLACK, text)

    def bg_lt_red(self, text: str = None) -> Colorant:
        """Sets the background color to light red.

        Parameters
        ----------
        text: str, optional
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self._add(Background.LT_RED, text)

    def bg_lt_green(self, text: str = None) -> Colorant:
        """Sets the background color to light green.

        Parameters
        ----------
        text: str, optional
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self._add(Background.LT_GREEN, text)

    def bg_lt_yellow(self, text: str = None) -> Colorant:
        """Sets the background color to light yellow.

        Parameters
        ----------
        text: str, optional
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self._add(Background.LT_YELLOW, text)

    def bg_lt_blue(self, text: str = None) -> Colorant:
        """Sets the background color to light blue.

        Parameters
        ----------
        text: str, optional
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self._add(Background.LT_BLUE, text)

    def bg_lt_magenta(self, text: str = None) -> Colorant:
        """Sets the background color to light magenta.

        Parameters
        ----------
        text: str, optional
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self._add(Background.LT_MAGENTA, text)

    def bg_lt_cyan(self, text: str = None) -> Colorant:
        """Sets the background color to light cyan.

        Parameters
        ----------
        text: str, optional
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self._add(Background.LT_CYAN, text)

    def bg_lt_white(self, text: str = None) -> Colorant:
        """Sets the background color to light white.

        Parameters
        ----------
        text: str, optional
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self._add(Background.LT_WHITE, text)

    def bold(self, text: str = None) -> Colorant:
        """Increases font intensity.

        Parameters
        ----------
        text: str, optional
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self._add(Decoration.BOLD, text)

    def underline(self, text: str = None) -> Colorant:
        """Adds the underline effect.

        Parameters
        ----------
        text: str, optional
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self._add(Decoration.UNDERLINE, text)

    def reversed(self, text: str = None) -> Colorant:
        """Flips the foreground and background colors.

        Parameters
        ----------
        text: str, optional
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        return self._add(Decoration.REVERSED, text)

    def _add(self, *argv: str) -> Colorant:
        """Adds escape sequences and texts to buffer.

        Parameters
        ----------
        text: str, optional
            Raw text.

        Returns
        -------
        Colorant
            Current instance.
        """
        for arg in argv:
            if arg:
                self._buf.append(arg)
        return self

    def _join(self) -> str:
        """Joins escape sequences with texts.

        Returns
        -------
        Colorant
            Current instance.
        """
        return ''.join(self._buf)


class Foreground:
    """Foreground CSI sequences."""
    BLACK = csi_seq(30)
    RED = csi_seq(31)
    GREEN = csi_seq(32)
    YELLOW = csi_seq(33)
    BLUE = csi_seq(34)
    MAGENTA = csi_seq(35)
    CYAN = csi_seq(36)
    WHITE = csi_seq(37)
    LT_BLACK = csi_seq(90)
    LT_RED = csi_seq(91)
    LT_GREEN = csi_seq(92)
    LT_YELLOW = csi_seq(93)
    LT_BLUE = csi_seq(94)
    LT_MAGENTA = csi_seq(95)
    LT_CYAN = csi_seq(96)
    LT_WHITE = csi_seq(97)
    DEFAULT = csi_seq(39)


class Background:
    """Background CSI sequences."""
    BLACK = csi_seq(40)
    RED = csi_seq(41)
    GREEN = csi_seq(42)
    YELLOW = csi_seq(43)
    BLUE = csi_seq(44)
    MAGENTA = csi_seq(45)
    CYAN = csi_seq(46)
    WHITE = csi_seq(47)
    LT_BLACK = csi_seq(100)
    LT_RED = csi_seq(101)
    LT_GREEN = csi_seq(102)
    LT_YELLOW = csi_seq(103)
    LT_BLUE = csi_seq(104)
    LT_MAGENTA = csi_seq(105)
    LT_CYAN = csi_seq(106)
    LT_WHITE = csi_seq(107)
    DEFAULT = csi_seq(49)


class Decoration:
    """Decoration CSI sequences."""
    BOLD = csi_seq(1)
    UNDERLINE = csi_seq(4)
    REVERSED = csi_seq(7)
