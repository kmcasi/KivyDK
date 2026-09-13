#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 12 Sep 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
"""
PointerManager provides a centralized, lightweight system for detecting which widget is currently under
the mouse cursor. Instead of relying on per‑widget polling or Kivy’s raw motion events, this module
implements a unified pointer routing layer that tracks hover transitions, dispatches enter/leave events
and maintains a single authoritative hovered widget.

Widgets that participate in pointer detection register themselves with the manager, allowing KiviDK to
evaluate only the relevant widgets and avoid redundant collision checks. This design ensures consistent
hover behavior across the entire UI, enables higher‑level features such as tooltips and forms the
foundation for future pointer‑driven interactions.
"""
__all__ = ("PointerManager", "PointerManagerBase")

#// IMPORT
from kivy.core.window import Window
from kivy.uix.widget import Widget


#// LOGIC
class PointerManagerBase:
    """
    Central component responsible for tracking the widget currently under the mouse cursor.

    It maintains a registry of participating widgets and dispatches pointer enter/leave
    callbacks whenever the hovered target changes. This class provides the low‑level
    infrastructure used by higher‑level hover, tooltip and other pointer‑driven behaviors.
    """
    def __init__(self) -> None:
        # Private variables
        self.__widgets: set[Widget] = set()
        self.__last_widget: Widget|None = None

        if Window is not None:
            Window.fbind("mouse_pos", self._check_pointer)
            # Window.fbind("on_cursor_enter", self._check_pointer)
            Window.fbind("on_cursor_leave", self._invalidate_widget)
            Window.fbind("on_mouse_down", self._do_pointer_press)
            Window.fbind("on_mouse_up", self._do_pointer_release)

    def register(self, widget:Widget) -> None:
        """Register a specific widget for pointer detection system."""
        self.__widgets.add(widget)

    def unregister(self, widget:Widget) -> None:
        """Unregister a specific widget from pointer detection system."""
        self.__widgets.discard(widget)

    # noinspection PyUnusedLocal
    def _check_pointer(self, *args) -> None:
        point_pos: tuple[float, float] = Window.mouse_pos
        this_widget: Widget|None = None

        # Find first widget under pointer
        for widget in self.__widgets:
            # Convert window space to widget space
            wX, wY = widget.to_widget(*point_pos)
            if widget.collide_point(wX, wY):
                this_widget = widget
                break

        # If widget changed, send enter/leave
        if this_widget is not self.__last_widget:
            if self.__last_widget is not None:
                self._do_pointer_leave(self.__last_widget)

            if this_widget is not None:
                self._do_pointer_enter(this_widget)

            self.__last_widget = this_widget

    # noinspection PyUnusedLocal
    def _invalidate_widget(self, *args) -> None:
        if self.__last_widget is not None:
            self._do_pointer_leave(self.__last_widget)
            self.__last_widget = None

    @staticmethod
    def _do_pointer_enter(widget:Widget) -> None:
        if hasattr(widget, "_do_pointer_enter"):
            widget._do_pointer_enter()

        if hasattr(widget, "on_pointer_enter"):
            widget.on_pointer_enter()

    @staticmethod
    def _do_pointer_leave(widget:Widget) -> None:
        if hasattr(widget, "_do_pointer_leave"):
            widget._do_pointer_leave()

        if hasattr(widget, "on_pointer_leave"):
            widget.on_pointer_leave()

    def _do_pointer_press(self, instance:Window, x:float, y:float, button:str, modifiers:list[str]) -> None:
        if self.__last_widget:
            if hasattr(self.__last_widget, "_do_pointer_press"):
                self.__last_widget._do_pointer_press(button, modifiers)

            if hasattr(self.__last_widget, "on_pointer_press"):
                self.__last_widget.on_pointer_press(button, modifiers)

    def _do_pointer_release(self, instance:Window, x:float, y:float, button:str, modifiers:list[str]) -> None:
        if self.__last_widget:
            if hasattr(self.__last_widget, "_do_pointer_release"):
                self.__last_widget._do_pointer_release(button, modifiers)

            if hasattr(self.__last_widget, "on_pointer_release"):
                self.__last_widget.on_pointer_release(button, modifiers)


#: Global manager responsible for efficient pointer detection.
PointerManager: PointerManagerBase = PointerManagerBase()
