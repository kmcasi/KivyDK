#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 18 Sep 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
"""
Provides pointer‑based press and release detection for widgets. PressBehavior listens to
pointer events routed through the KiviDK :class:`~kivydk.manager.pointer.PointerManager`
and dispatches ``on_press`` and ``on_release`` whenever a pointer button is pressed or released.

A press event is fired immediately when a pointer button is pressed. A release
event is fired when the button released, and includes an ``inside`` flag
indicating whether the release occurred within the widget’s bounds.

§ section : example ¶

Sample demonstrating how ``PressBehavior`` can be used to detect press and release actions on a widget.

§ show image : uix, behavior, TestPress.gif ¶

§ show code : uix, behavior, press.py ¶
"""

__all__ = ("PressBehavior",)

#// IMPORT
from kivy.input.motionevent import MotionEvent


#// LOGIC
class PressBehavior:
    """
    A mixin that adds basic press and release detection to any widget.

    .. note::
        This behavior is intentionally lightweight and does not implement click logic.
        For click detection, use :class:`~kivydk.uix.behavior.click.ClickBehavior`.
    """

    __events__ = ["on_press", "on_release"]

    # noinspection PyUnresolvedReferences
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.register_for_motion_event("kdk_pointer")

    def on_press(self, button: str|None, modifiers: list[str]) -> None:
        """
        Fired when a pointer button is pressed.

        § parameters : button = The name of the pointer button that triggered the event|, or ``None``. ¶
        § param : modifiers = A list of active modifier keys (e.g. ``alt``|, ``ctrl``|, ``shift``|, ``numlock``). ¶
        """
        pass

    def on_release(self, button: str|None, modifiers: list[str], inside: bool) -> None:
        """
        Fired when a pointer button is released.

        § parameters : button = The name of the pointer button that triggered the event|, or ``None``. ¶
        § param : modifiers = A list of active modifier keys (e.g. ``alt``|, ``ctrl``|, ``shift``|, ``numlock``). ¶
        § param : inside = ``True`` if the release occurred inside the widget|, ``False`` otherwise. ¶
        """
        pass

    # noinspection PyUnusedLocal, PyUnresolvedReferences
    def _kdk_pointer_press(self, button: str|None, modifiers: list[str], event: MotionEvent) -> None:
        """
        Called when a mouse button is pressed or when an equivalent device action is triggered.

        :param button:      The button that triggered the press or ``None``.
        :param modifiers:   List of active keyboard modifiers at the moment of press.
        :param event:       The MotionEvent associated with this call.
        """
        self.dispatch("on_press", button, modifiers)

    # noinspection PyUnusedLocal, PyUnresolvedReferences
    def _kdk_pointer_release(self, button: str|None, modifiers: list[str], event: MotionEvent) -> None:
        """
        Called when a mouse button is released or when an equivalent device action is triggered.

        :param button:      The button that triggered the release or ``None``.
        :param modifiers:   List of active keyboard modifiers at the moment of release.
        :param event:       The MotionEvent associated with this call.
        """
        self.dispatch("on_release", button, modifiers, self.collide_point(*event.pos))
