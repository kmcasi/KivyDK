#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 09 Jan 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
"""
Provides a pointer‑based click detection behavior for widgets. ClickBehavior listens to
pointer release events routed through the KiviDK :class:`~kivydk.manager.pointer.PointerManager`
and implements a consistent model for single‑click and double‑click recognition.

§ section : example ¶

Sample demonstrating how ``ClickBehavior`` can be used to detect and handle click events.

§ show image : uix, behavior, TestClick.gif ¶

§ show code : uix, behavior, click.py ¶
"""
__all__ = ("ClickBehavior",)

#// IMPORT
from kivy.clock import Clock
from kivy.input.motionevent import MotionEvent
from kivy.properties import NumericProperty


#// LOGIC
class ClickBehavior:
    """
    A mixin that adds click and double‑click detection to any widget.

    A click is recognized when a pointer is pressed and released inside the widget without leaving its bounds.
    Two valid clicks of the same pointer within :attr:`click_interval` form a double‑click.

    .. note::
        This behavior does not provide ``on_press`` or ``on_release`` callbacks.
        If you require those events, inherit from Kivy’s :class:`~kivy.uix.behaviors.button.ButtonBehavior`
        or KivyDK's :class:`~kivydk.uix.behavior.press.PressBehavior`.
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

        self.register_for_motion_event("kdk_pointer")

        # Private variables
        self.__allow_dispatch: bool = True
        self.__pressed_button: dict[str, str|None] = {"last": None, "prev": None}
        self.__clock: Clock = Clock.create_trigger(self._reset_pressed_button, self.click_interval)

    def on_click(self, button: str|None, modifiers: list[str]) -> None:
        """
        Called when the widget receives a valid pointer click.

        § parameters : button = The name of the pointer button that triggered the event|, or ``None``. ¶
        § param : modifiers = A list of active modifier keys (e.g. ``alt``|, ``ctrl``|, ``shift``|, ``numlock``). ¶
        """
        pass

    def on_double_click(self, button: str|None, modifiers: list[str]) -> None:
        """
        Called when two consecutive valid clicks occur within :attr:`click_interval`.

        § parameters : button = The name of the pointer button that triggered the event|, or ``None``. ¶
        § param : modifiers = A list of active modifier keys (e.g. ``alt``|, ``ctrl``|, ``shift``|, ``numlock``). ¶
        """
        pass

    # noinspection PyUnusedLocal
    def _kdk_pointer_press(self, button: str|None, modifiers: list[str], event: MotionEvent) -> None:
        """
        Called when a mouse button is pressed or when an equivalent device action is triggered.

        :param button:      The button that triggered the press or ``None``.
        :param modifiers:   List of active keyboard modifiers at the moment of press.
        :param event:       The MotionEvent associated with this call.
        """
        self.__pressed_button["last"] = button

    # noinspection PyUnusedLocal, PyUnresolvedReferences
    def _kdk_pointer_release(self, button: str|None, modifiers: list[str], event: MotionEvent) -> None:
        """
        Called when a mouse button is released or when an equivalent device action is triggered.

        :param button:      The button that triggered the release or ``None``.
        :param modifiers:   List of active keyboard modifiers at the moment of release.
        :param event:       The MotionEvent associated with this call.
        """
        if self.__allow_dispatch and button == self.__pressed_button["last"]:
            if self.__clock.is_triggered:
                self.__clock.cancel()

                if button == self.__pressed_button["prev"]:
                    self.dispatch("on_double_click", button, modifiers)

                self._reset_pressed_button()

            else:
                self.__pressed_button["prev"] = button
                self.dispatch("on_click", button, modifiers)
                self.__clock()

        else:
            self.__clock.cancel()
            self._reset_pressed_button()

    # noinspection PyUnusedLocal, PyUnresolvedReferences
    def _kdk_pointer_hold(self, buttons: list[str], modifiers: list[str], event: MotionEvent):
        """
        Called when the pointer moves while at least one button is pressed
        or when an equivalent device action is triggered.

        :param buttons:     List of all currently held buttons or an empty list.
        :param modifiers:   List of active keyboard modifiers during movement.
        :param event:       The MotionEvent associated with this call.
        """
        if self.__allow_dispatch and not self.collide_point(*event.pos):
            self.__allow_dispatch = False

    # noinspection PyUnusedLocal
    def _reset_pressed_button(self, *args) -> None:
        """ Resets the internal button tracking state. """
        self.__allow_dispatch = True
        for key in self.__pressed_button.keys():
            self.__pressed_button[key] = None
