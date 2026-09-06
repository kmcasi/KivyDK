#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 07 Jan 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
__all__ = ("WindowAdapter", "Window")

#// IMPORT
from kivy.uix.widget import WidgetBase

from kivy.properties import NumericProperty
from kivy.properties import ReferenceListProperty, AliasProperty


#// LOGIC
# TODO: Extend this class to support all `~kivy.core.window.Window` functionality.
class WindowAdapter(WidgetBase):
    """
    Basically is a replacement for :class:`~kivy.core.window.Window` needs some manual assistant.

    .. note::
        Usefully only if a second rendering library is used, like `panda3d`.

    :Events:
        `on_cursor_enter`
            Fired when the cursor enters the window.
        `on_cursor_leave`
            Fired when the cursor leaves the window.
        `on_mouse_move`
            Fired when the cursor move inside the window.
    """

    mouse_x = NumericProperty(-1)
    """X position of the mouse cursor within the window.

    Position is relative to the left/bottom point of the window.

    :attr:`mouse_x` is a :class:`~kivy.properties.NumericProperty` and defaults to `-1`."""

    mouse_y = NumericProperty(-1)
    """Y position of the mouse cursor within the window.

    Position is relative to the left/bottom point of the window.

    :attr:`mouse_y` is a :class:`~kivy.properties.NumericProperty` and defaults to `-1`."""

    mouse_pos = ReferenceListProperty(mouse_x, mouse_y)
    """2d position of the mouse cursor within the window.

    Position is relative to the left/bottom point of the window.

    :attr:`mouse_pos` is an :class:`~kivy.properties.ReferenceListProperty` of
    (:attr:`mouse_x`, :attr:`mouse_y`) properties."""

    __events__ = [
        "on_cursor_enter", "on_cursor_leave", "on_mouse_move"
    ]

    def __init__(self, **kwargs) -> None:
        super(WindowAdapter, self).__init__(**kwargs)

        self._focus:bool = False
        self.fbind("mouse_pos", self._do_mouse_move)

    def _get_focus(self) -> bool:
        return self._focus

    def _set_focus(self, value:bool) -> bool:
        if self._focus != value:
            self.dispatch(f"on_cursor_{"enter" if value else "leave"}")

            self._focus = value

        return True

    focus = AliasProperty(_get_focus, _set_focus)
    """Check whether or not the window currently has focus.

    :attr:`focus` is a :class:`~kivy.properties.AliasProperty` and defaults to False."""

    def _do_mouse_move(self, instance:object, mouse_pos:tuple[float, float]) -> None:
        # TODO: Modifiers not properly implemented, for now is an empty list
        self.dispatch("on_mouse_move", mouse_pos)
        # self.dispatch("on_mouse_move", self.mouse_x, self.mouse_y, [])

    def on_cursor_enter(self, *args) -> None:
        """Event called when the cursor enters the window."""
        pass

    def on_cursor_leave(self, *args) -> None:
        """Event called when the cursor leaves the window."""
        pass

    def on_mouse_move(self, mouse_pos:tuple[float, float]) -> None:
        """Event called when the mouse is moved across the window."""
        pass


#// GLOBAL VARIABLES
Window = WindowAdapter()
