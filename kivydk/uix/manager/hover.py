#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 09 Jan 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
"""
This manager coordinates hover detection by keeping a registry of widgets that support hover interactions
and performing optimized checks to determine which one is currently under the cursor. This centralized approach
eliminates redundant per‑widget computations and ensures that only the relevant widgets are evaluated until a hover
target is identified.
"""
__all__ = ("HoverManager", "HoverManagerBase")

#// IMPORT
from kivydk.__ref.window import Window

from kivy.event import EventDispatcher


#// LOGIC
class HoverBehavior:
    """Lightweight forward declaration used to break a circular import.

    Stub used for type checking. Attributes reflect their runtime value types."""
    _hover_state: bool  # actually a BooleanProperty
    def collide_point(self, x:int|float, y:int|float) -> bool: ...


class HoverManagerBase(EventDispatcher):
    """
    Centralized manager responsible for efficient hover detection across all widgets that inherit from
    :class:`~uix.behavior.hover.HoverBehavior`.

    .. todo::
        - Sort system need to be implemented. Usually the last registered widgets have high chance to be hovered ones.
        - Some system to group widgets in chunks and to check them first.
            - Tree system will be faster if the UIX become more complex.
    """
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        # Local variables
        self.__widgets: list[HoverBehavior] = []
        self.__last_hovered: HoverBehavior|None = None

        if Window is not None:
            Window.fbind("mouse_pos", self._do_mouse_pos)
            Window.fbind("on_cursor_leave", self._hover_end_last)

    def register(self, widget:HoverBehavior) -> None:
        """Register a specific widget for hovering detection system."""
        self.__widgets.append(widget)

    def unregister(self, widget:HoverBehavior) -> None:
        """Unregister a specific widget from hovering detection system."""
        if widget in self.__widgets:
            self.__widgets.remove(widget)

    def _hover_end_last(self, *args) -> None:
        if self.__last_hovered:
            self.__last_hovered._hover_state = False
            self.__last_hovered = None

    def _do_mouse_pos(self, instance:Window, mouse_pos:tuple[float, float]) -> None:
        tmp_hover: HoverBehavior|None = None

        for widget in self.__widgets:
            if widget.collide_point(*mouse_pos):
                tmp_hover = widget
                break

        if tmp_hover is not self.__last_hovered:
            self._hover_end_last()

            if tmp_hover is not None:
                tmp_hover._hover_state = True
                self.__last_hovered = tmp_hover


#: Global manager responsible for efficient hover detection.
HoverManager:HoverManagerBase = HoverManagerBase()
