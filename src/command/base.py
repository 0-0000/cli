"""
Base class for command classes.
"""



from typing import Tuple, Union



def to_hex_rgb(color:Tuple[int, int, int]) -> str:
    """Convert color tuple to RGB hex code.

    Returns:
        Hex color code, such as `0x3370ff` and `0x4f8`.

    Raises:
        TypeError.
        ValueError: Bad tuple length.
        ValueError: Bad color code.
    """
    if type(color) != tuple:
        raise TypeError()
    if len(color) != 3:
        raise ValueError("bad tuple length")
    # Check color codes.
    if tuple(i for i in color if (type(i) != int or i < 0 or i > 0xff)):
        raise ValueError("bad color code")
    return hex(color[0] * 0x10000 + color[1] * 0x100 + color[2])


def virtual(func):
    """Decorator for pure virtual functions (like C++).

    The derived class must implement this method,
        otherwise an error will be thrown.

    Raises:
        NotImplementedError: Not implemented.
    """
    def inner(*args, **kwargs):
        raise NotImplementedError()
    return inner


# This class is reserved for future use.
class Base(object):
    pass


# Inheriting this class represents that
#     the goal of the inheritor is to generate `Miniworld Lua Script`.
class BaseMiniScript(Base):
    _init:bool = False
    """Whether the instance was initialized successfully."""
    _script:Union[str, None] = None
    """Cached script."""
    @virtual
    def generate_script(self) -> str:
        """Generate `Miniworld Lua Script` by self args.

        Returns:
            Generated script.

        Raises:
            ValueError: If no available port is found.
        """
        return ""
    @property
    def script(self) -> str:
        """Get final script

        Notice:
            This attribute will be cached.
            To force script regeneration, try `generate_script` function.

        Returns:
            Final script.
        """
        if self._script is None:
            self._script = self.generate_script()
        return self._script