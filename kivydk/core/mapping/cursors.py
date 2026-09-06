#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 21 May 2025. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
"""
This module defines the cursor‑mapping layer used by KivyDK to provide a consistent and extensible way of
managing system cursors across different platforms. It abstracts Kivy’s low‑level cursor handling and exposes
a small, stable API for setting or resetting the active cursor within the application.

These mappings allow widgets, behaviors and higher‑level components to request semantic cursor types
(e.g., “resize horizontal”, “busy”, “text selection”) without needing to know the exact string identifiers
used by the underlying system.
"""
__all__ = ("CursorBase", "CursorDefault", "CursorWindows")

#// IMPORT
# TODO: Extend `kivydk.core.window_adapter.WindowAdapter` to implement cursor functionality in `panda3d` system.
from kivy.core.window import Window


#// LOGIC
class CursorBase:
    """
    Lightweight base class for all cursor‑mapping groups in KivyDK.

    This class provides the minimal functionality required to apply or restore a system
    cursor using Kivy’s window provider. Subclasses define semantic cursor names, while
    :class:`CursorBase` handles the actual call to :func:`Window.set_system_cursor`.
    """
    # Private variables
    __default_cursor: str | None = None

    @staticmethod
    def set(cursor: str | None) -> None:
        """
        Applies the given cursor using Kivy’s window provider.

        This method is a thin wrapper around :func:`Window.set_system_cursor` used by all
        cursor mapping classes to activate a specific cursor. It accepts ``None`` as a safe no‑op,
        allowing subclasses to call :meth:`reset` even if their default cursor value has not been initialized yet.

        This function does not validate the cursor name; it assumes that subclasses provide
        valid identifiers based on Kivy’s built‑in cursor strings.
        """
        if cursor is not None:
            Window.set_system_cursor(cursor)

    @staticmethod
    def reset() -> None:
        """
        Restores the default cursor defined by the active cursor mapping class.

        The default cursor is stored internally on :class:`CursorBase` and overridden by
        subclasses. Calling this method ensures that the application returns to a predictable cursor state
        after temporary cursor changes (e.g., during drag operations or hover interactions).
        """
        CursorBase.set(CursorBase.__default_cursor)


class CursorDefault(CursorBase):
    """
    Default cursor mapping used by KivyDK.

    A nested :class:`Size` namespace contains the resize‑related cursor identifiers.

    The default cursor for this mapping is :attr:`Arrow`, which is restored when calling
    :meth:`CursorDefault.reset()`.
    """
    Arrow = "arrow"
    Crosshair = "crosshair"
    Hand = "hand"
    I_Beam = "ibeam"
    No = "no"
    Wait = "wait"
    Wait_Arrow = "wait_arrow"

    class Size:
        NWSE = "size_nwse"
        NESW = "size_nesw"
        WE = "size_we"
        NS = "size_ns"
        All = "size_all"

    # Set the default cursor what will be used on the `reset` function
    CursorBase._CursorBase__default_cursor = Arrow


class CursorWindows(CursorBase):
    """
    Windows‑style cursor mapping for developers who prefer familiar naming conventions.

    This class provides semantic cursor names that resemble those commonly used on
    Microsoft Windows (e.g., ``Busy``, ``Move``, ``Unavailable``). Internally, these
    names still map to Kivy’s built‑in cursor identifiers; the goal is to improve
    readability and autocompletion, not to emulate native Windows cursor behavior.

    Two nested namespaces :class:`Select` and :class:`Resize` group related cursor types
    for text selection and directional resizing.

    The default cursor for this mapping is :attr:`Normal`, restored via
    :meth:`CursorWindows.reset()`.
    """
    Busy = "wait"
    Move = "size_all"
    Normal = "arrow"
    Unavailable = "no"
    Working_In_Background = Busy_In_Background = "wait_arrow"

    class Select:
        Link = "hand"
        Normal = "arrow"
        Precision = "crosshair"
        Text = "ibeam"

    class Resize:
        Diagonal_Left = "size_nwse"
        Diagonal_Right = "size_nesw"
        Horizontal = "size_we"
        Vertical = "size_ns"

    # Set the default cursor what will be used on the `reset` function
    CursorBase._CursorBase__default_cursor = Normal
