#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 12 Sep 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
# noinspection PyUnresolvedReferences
"""
This manager provides a unified pointer routing layer primarily designed for mouse devices
and adapted to support other MotionEvent‑based devices such as touch and stylus.

Widgets register their interest in pointer events, allowing the manager to evaluate
only relevant subtrees and perform deep hit‑testing using a consistent coordinate model.
This system provides reliable cross‑device pointer behavior, supports multi‑button input
for mouse devices and forms the foundation for higher‑level interactions such as tooltips,
drag operations and future custom pointer‑driven UI components.

§ section : usage ¶

Widgets participate in pointer routing only if they explicitly register for the ``kdk_pointer`` MotionEvent type.

§ code ¶
    self.register_for_motion_event("kdk_pointer")

Once registered, the PointerManager will call pointer‑related callbacks on the widget whenever
the pointer hovers over its area or interacts with it through a press. A widget may define any subset
of these callbacks; only the methods that exist on the widget are invoked, allowing developers to keep
their code minimal and implement only the behaviors they need.

§ dropdown : hover, style = az ¶
    Hover callbacks are fired during pointer or mouse movement and are not called on widgets
    that are currently interacting with the touch pointer callbacks. This means that once the user
    presses a widget, it will no longer receive hover callbacks until the pointer is released.


    § code : begin, style = az ¶
        def _kdk_pointer_enter(self, event):
            \"""
            Called when the pointer enters the widget's area.

            :param event: The MotionEvent associated with this call.
            \"""
            print("[ ENTER ]", event)

    § code : end, style = az ¶
        def _kdk_pointer_leave(self, event):
            \"""
            Called when the pointer leaves the widget's area.

            :param event: The MotionEvent associated with this call.
            \"""
            print("[ LEAVE ]", event)

    § code : update, style = az ¶
        def _kdk_pointer_move(self, event):
            \"""
            Called when the pointer moves while hovering over the widget.

            :param event: The MotionEvent associated with this call.
            \"""
            print("[ MOVE ]", event)

§ dropdown : touch, style = az ¶
    Touch callbacks are fired when the pointer or mouse is pressed, held or released and are always
    routed to a single widget at a time. Once a widget is pressed, these callbacks will not be dispatched
    to other widgets until the pointer is released. Even though the manager supports multi‑button
    mouse input, interaction remains locked to one widget until all buttons released.

    .. attention::
        For mouse devices, the forwarded MotionEvent can be used **only** to retrieve pointer coordinates.

        Because Kivy is primarily touch‑oriented, mouse‑based touch callbacks may receive different
        MotionEvent instances. Do not rely on these MotionEvent objects for anything other than pointer position.

    § code : begin, style = az ¶
        def _kdk_pointer_press(self, button, modifiers, event):
            \"""
            Called when a mouse button is pressed or when an equivalent device action is triggered.

            :param button:      The button that triggered the press, or ``None``.
            :param modifiers:   List of active keyboard modifiers at the moment of press.
            :param event:       The MotionEvent associated with this call.
            \"""
            print("[ PRESS ]", button, modifiers, event)

    § code : end, style = az ¶
        def _kdk_pointer_release(self, button, modifiers, event):
            \"""
            Called when a mouse button is released or when an equivalent device action is triggered.

            :param button:      The button that triggered the release, or ``None``.
            :param modifiers:   List of active keyboard modifiers at the moment of release.
            :param event:       The MotionEvent associated with this call.
            \"""
            print("[ RELEASE ]", button, modifiers, event)

    § code : update, style = az ¶
        def _kdk_pointer_hold(self, buttons, modifiers, event):
            \"""
            Called when the pointer moves while at least one button is pressed
            or when an equivalent device action is triggered.

            :param buttons:     List of all currently held buttons or an empty list.
            :param modifiers:   List of active keyboard modifiers during movement.
            :param event:       The MotionEvent associated with this call.
            \"""
            print("[ HOLD ]", buttons, modifiers, event)

"""
__all__ = ("PointerManager",)

#// IMPORT
from typing import Callable, Any

from kivy.core.window import Window
from kivy.eventmanager import EventManagerBase
from kivy.input.motionevent import MotionEvent
from kivy.uix.widget import Widget


#// LOGIC
class PointerManager(EventManagerBase):
    """
    Manages the active pointer state for KiviDK by tracking the currently hovered
    widget and locking pointer interaction to that widget once a press occurs.

    It dispatches pointer-related callbacks with forwarded MotionEvent objects,
    ensuring consistent pointer behavior across mouse and other supported devices.
    """

    type_ids: tuple[str] = ("touch", "hover")
    """
    The MotionEvent types this manager processes.
    Only events with these type IDs are routed through the pointer system for handling.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        # Private variables
        self.__interest_widget: Widget|None = None
        self.__last_hover_widget: Widget|None = None
        self.__last_touch_widget: Widget|None = None
        self.__last_mEvent: MotionEvent|None = None
        self.__hold_buttons: set[str] = set()
        self.__touch_method: dict[str, str] = {
            "begin": "press",
            "end": "release",
            "update": "hold"
        }
        self.__binds: dict[str, Callable] = {
            "on_mouse_down": self._do_pointer_begin,
            "on_mouse_up": self._do_pointer_end,
            "on_mouse_move": self._do_pointer_update,
        }

    def start(self) -> None:
        """ Activate the manager and bind the necessary Window callbacks. """
        for key, method in self.__binds.items():
            self.window.fbind(key, method)

    def stop(self) -> None:
        """ Deactivate the manager, clear pointer state and unbind Window callbacks. """
        self.__invalidate_last_hover_widget()
        self.__invalidate_last_touch_widget()
        self.__last_mEvent = None

        for key, method in self.__binds.items():
            self.window.funbind(key, method)

    def dispatch(self, eType: str, mEvent: MotionEvent) -> bool:
        """
        Dispatch the MotionEvent to the appropriate widget in the window.

        § parameters : eType = One of ``"begin"``/, ``"update"`` or ``"end"`` ¶
        § param : mEvent = The MotionEvent currently being dispatched ¶
        § param : RETURN = Always ``False`` to allow other managers and widgets to process their own event logic ¶
        """
        # MotionEvent.begin often reports (0.0, 0.0) → use Window provider coordinates all the time
        self.__last_mEvent = mEvent
        mEvent.pos = self.window.mouse_pos
        mEvent.x, mEvent.y = mEvent.pos

        if mEvent.type_id == "hover":
            # Pointer left the window boundaries
            if eType == "end":
                self.__invalidate_last_hover_widget()
                return False

            # Resolve the widget currently under the pointer
            self.__solve_interest_widget("kdk_pointer", mEvent)

            # Hover target changed → dispatch leave/enter
            if self.__interest_widget is not self.__last_hover_widget:
                if self.__last_hover_widget:
                    self.__call_pointer_method("leave", self.__last_hover_widget, mEvent)

                if self.__interest_widget:
                    self.__call_pointer_method("enter", self.__interest_widget, mEvent)

                # Update the local reference for the hovered widget
                self.__last_hover_widget = self.__interest_widget

            # Hover target unchanged → dispatch update
            elif self.__interest_widget:
                self.__call_pointer_method("move", self.__interest_widget, mEvent)

        else:
            # MouseMotionEvent simulates touch and cannot represent multiple buttons.
            # Skip MotionEvent‑based touch logic for mouse devices and rely on Window
            # provider events to handle multi‑button input correctly.
            if mEvent.device == "mouse":
                return False

            # Update the active touch target using the last hovered widget
            if eType == "begin":
                self.__last_touch_widget = self.__last_hover_widget

            # Non-mouse devices → dispatch pointer-related callbacks
            if self.__last_touch_widget:
                btn: list|str|None = mEvent.button if (eType != "update") else [mEvent.button] if mEvent.button else []
                self.__call_pointer_method(self.__touch_method[eType], self.__last_touch_widget,
                                           btn, self.window.modifiers, mEvent
                                           )

            # Clear the active touch target reference
            if eType == "end":
                self.__last_touch_widget = None

        return False

    # noinspection PyUnusedLocal
    def _do_pointer_begin(self, instance: Window, x: float, y: float, button: str, modifiers: list[str]) -> None:
        """
        Handle the beginning of a pointer press triggered by the Window provider.

        The last hovered widget becomes the active touch target.
        If a widget is currently hovered, its pointer‑press callback is invoked.

        :param instance:    Window instance emitting the event.
        :param x:           Pointer X coordinate in window space.
        :param y:           Pointer Y coordinate in window space.
        :param button:      Mouse button identifier (e.g. ``"left"``, ``"right"``).
        :param modifiers:   List of active keyboard modifiers at the moment of press.
        """
        # Register the pressed button so pointer-hold callback can report active buttons
        self.__hold_buttons.add(button)

        # Update the active touch target using the last hovered widget
        if not self.__last_touch_widget:
            self.__last_touch_widget = self.__last_hover_widget

        # The last known pointer position is used to avoid SDL2’s top‑left origin mismatch
        if self.__last_touch_widget:
            self.__call_pointer_method(self.__touch_method["begin"], self.__last_touch_widget,
                                       button, modifiers, self.__last_mEvent
                                       )

    # noinspection PyUnusedLocal
    def _do_pointer_end(self, instance: Window, x: float, y: float, button: str, modifiers: list[str]) -> None:
        """
        Handle the ending of a pointer press triggered by the Window provider.

        If a widget was previously marked as the active touch target, its
        pointer‑release callback is invoked.

        :param instance:    Window instance emitting the event.
        :param x:           Pointer X coordinate in window space.
        :param y:           Pointer Y coordinate in window space.
        :param button:      Mouse button identifier (e.g. ``"left"``, ``"right"``).
        :param modifiers:   List of active keyboard modifiers at the moment of release.
        """
        # Remove the released button so pointer-hold callback can report only the active buttons
        self.__hold_buttons.discard(button)

        # The last known pointer position is used to avoid SDL2’s top‑left origin mismatch
        if self.__last_touch_widget:
            self.__call_pointer_method(self.__touch_method["end"], self.__last_touch_widget,
                                       button, modifiers, self.__last_mEvent
                                       )

            # Clear the active touch target reference
            if len(self.__hold_buttons) == 0:
                self.__last_touch_widget = None

    # noinspection PyUnusedLocal
    def _do_pointer_update(self, instance: Window, x: float, y: float, modifiers: list[str]) -> None:
        """
        Handle the movement of a pointer press triggered by the Window provider.

        If a widget was previously marked as the active touch target, its
        pointer‑hold callback is invoked.

        :param instance:    Window instance emitting the event.
        :param x:           Pointer X coordinate in window space.
        :param y:           Pointer Y coordinate in window space.
        :param modifiers:   List of active keyboard modifiers at the moment of press.
        """
        # The last known pointer position is used to avoid SDL2’s top‑left origin mismatch
        if self.__last_touch_widget:
            self.__call_pointer_method(self.__touch_method["update"], self.__last_touch_widget,
                                       list(self.__hold_buttons), modifiers, self.__last_mEvent
                                       )

    def __deep_search_widget(self, widget: Widget, type_id: str, point: tuple[float, float]) -> Widget|None:
        """
        Recursively locate the deepest widget interested in a specific MotionEvent type.

        The search is pruned using the widget's ``motion_filter`` so only subtrees
        containing widgets registered for ``type_id`` are evaluated.
        Collision checks are performed in window‑space coordinates.

        :param widget:  Root widget of the subtree being evaluated.
        :param type_id: MotionEvent type identifier (e.g. ``"hover"``, ``"touch"``).
        :param point:   Pointer position in window coordinates (x, y).
        """
        # TODO: Extra filtering optimization could be done here for shore...

        # Skip entire subtree if no child cares about this `type_id` event type
        filters: dict[str, list[Widget]] = widget.motion_filter
        if type_id not in filters:
            return None

        # Skip entire subtree if the provided point (x, y) is outside interested `widget`
        if not widget.collide_point(*point):
            return None

        # Search children first
        for child in widget.children:
            found_widget: Widget|None = self.__deep_search_widget(child, type_id, point)
            if found_widget:
                return found_widget

        # If this widget itself registered for the type, return it
        if widget in filters.get(type_id, []):
            return widget

        return None

    def __solve_interest_widget(self, type_id: str, mEvent: MotionEvent) -> None:
        """
        Resolve the widget that should receive the current pointer call.

        If the MotionEvent is grabbed, the grabbed widget takes priority regardless
        of pointer position. Otherwise, the search begins from each top‑level window
        child and uses :meth:`__deep_search_widget` to locate the deepest widget
        interested in ``type_id``.

        :param type_id: MotionEvent type identifier (e.g. ``"hover"``, ``"touch"``).
        :param mEvent:  The MotionEvent instance currently processed.
        """
        if self.__last_touch_widget and self.__last_touch_widget.collide_point(*mEvent.pos):
            self.__interest_widget = None
            return None

        for window_child in self.window.children:
            self.__interest_widget = self.__deep_search_widget(window_child, type_id, mEvent.pos)

            if self.__interest_widget:
                break

    def __invalidate_last_hover_widget(self) -> None:
        """ Clear the previously hovered widget reference and dispatch its pointer-leave callback. """
        if self.__last_hover_widget:
            self.__call_pointer_method("leave", self.__last_hover_widget, self.__last_mEvent)

        self.__last_hover_widget = None

    def __invalidate_last_touch_widget(self) -> None:
        """ Clear the previously touched widget reference and dispatch its pointer-release callback. """
        if self.__last_touch_widget:
            self.__call_pointer_method(self.__touch_method["end"], self.__last_touch_widget,
                                       "None", self.window.modifiers, self.__last_mEvent
                                       )

        self.__last_touch_widget = None

    @staticmethod
    def __call_pointer_method(name: str, widget: Widget, *args, **kwargs) -> None:
        """
        Dynamically invoke a pointer‑related callback on ``widget`` if it exists.

        The resolved method name follows the KivyDK convention: ``_kdk_pointer_<name>``

        :param name:    Pointer action name (``"enter"``, ``"press"``, etc.).
        :param widget:  Target widget receiving the callback.
        :param args:    Positional arguments forwarded to the callback.
        :param kwargs:  Keyword arguments forwarded to the callback.
        """
        pointer_method: Callable[..., Any]|None = getattr(widget, f"_kdk_pointer_{name}", None)

        if callable(pointer_method):
            pointer_method(*args, **kwargs)
