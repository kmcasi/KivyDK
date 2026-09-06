#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 09 Jan 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
"""
This behavior encapsulates mouse click detection for widgets. It listens for press and release events,
tracks the click state and triggers callbacks when a valid click occurs. This behavior removes the need for manual
input handling and provides a consistent, reusable pattern for widgets that respond to user clicks.

.. tip::
    Click detection is based on touch events, so finger presses on touch‑enabled monitors are treated as clicks.

§ section : example ¶

Sample demonstrating how ``ClickBehavior`` can be used to detect and handle click events.

§ show image : uix, behavior, TestClick.gif ¶

§ show code : uix, behavior, click.py ¶
"""
__all__ = ("ClickBehavior",)

#// IMPORT
from kivydk.__ref.window import Window

from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.uix.behaviors.button import ButtonBehavior


#// LOGIC
class ClickBehavior(ButtonBehavior):
    """
    A mixin that adds lightweight click and double click detection to any widget.

    This extends :class:`~kivy.uix.behaviors.button.ButtonBehavior`, so the standard ``on_press`` and ``on_release``
    events remain available.
    """

    click_interval: NumericProperty = NumericProperty(0.25)
    """
    Maximum time ``(seconds)`` in which a second click is considered part of a double‑click.
    
    The sweet spot is between ``0.2`` and ``0.3``.
    """

    __events__ = ["on_click", "on_double_click"]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        # Local variables
        self.__count_click: int = 0
        self.__clock: Clock = Clock.create_trigger(self._dispatch_double_click, self.click_interval)

        self.fbind("on_release", self._dispatch_click)

    def on_click(self) -> None:
        """Called when the widget is pressed and released."""
        pass

    def on_double_click(self) -> None:
        """Called when the widget is pressed and released two times."""
        pass

    def _dispatch_click(self, *args) -> None:
        if self.collide_point(*Window.mouse_pos):
            self.__count_click += 1
            self.__clock()

            if self.__count_click < 2:
                self.dispatch("on_click")

    def _dispatch_double_click(self, *args) -> None:
        if self.__count_click > 1:
            self.dispatch("on_double_click")

        self.__count_click = 0
