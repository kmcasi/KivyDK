#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 09 Jan 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
"""
Provides a pointer‑based click detection behavior for widgets. ClickBehavior listens to
pointer release events routed through :class:`~kivydk.uix.manager.pointer.PointerManager`
and implements a consistent model for single‑click and double‑click recognition.

§ section : example ¶

Sample demonstrating how ``ClickBehavior`` can be used to detect and handle click events.

§ show image : uix, behavior, TestClick.gif ¶

§ show code : uix, behavior, click.py ¶
"""
__all__ = ("ClickBehavior",)

#// IMPORT
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget

from kivydk.uix.manager.pointer import PointerManager


#// LOGIC
class ClickBehavior:
    """
    A mixin that adds lightweight click and double click detection to any widget.

    .. note::
        This behavior does not fire ``on_press`` or ``on_release`` events.
        If you require those callbacks, inherit them from Kivy’s
        :class:`~kivy.uix.behaviors.button.ButtonBehavior`.
    """

    click_interval: NumericProperty = NumericProperty(0.25)
    """
    Maximum time ``(seconds)`` in which a second click is considered part of a double‑click.
    
    The sweet spot is between ``0.2`` and ``0.3``.
    """

    __events__ = ["on_click", "on_double_click"]

    # noinspection PyUnresolvedReferences
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        # Private variables
        self.__last_button: str = ""
        self.__clock: Clock = Clock.create_trigger(self._reset_last_button, self.click_interval)

        self.fbind("parent", self._auto_register)

    def on_click(self, button:str, modifiers:list[str]) -> None:
        """
        Called when the widget receives a valid pointer click.

        § parameters : button = The name of the pointer button that triggered the event. ¶
        § param : modifiers = A list of active modifier keys (e.g. ``alt``|, ``ctrl``|, ``shift``|, ``numlock``). ¶
        """
        pass

    def on_double_click(self, button:str, modifiers:list[str]) -> None:
        """
        Called when two consecutive pointer clicks occur within :attr:`click_interval`.

        § parameters : button = The name of the pointer button that triggered the event. ¶
        § param : modifiers = A list of active modifier keys (e.g. ``alt``|, ``ctrl``|, ``shift``|, ``numlock``). ¶
        """
        pass

    @staticmethod
    def _auto_register(instance:Widget, parent:Widget|None) -> None:
        if parent is None:
            PointerManager.unregister(instance)
        else:
            PointerManager.register(instance)

    # noinspection PyUnresolvedReferences
    def _do_pointer_release(self, button:str, modifiers:list[str]) -> None:
        if button == self.__last_button:
            self.__clock.cancel()
            self.__last_button = ""
            self.dispatch("on_double_click", button, modifiers)
        else:
            self.__clock()
            self.__last_button = button
            self.dispatch("on_click", button, modifiers)

    # noinspection PyUnusedLocal
    def _reset_last_button(self, *args) -> None:
        self.__last_button = ""
