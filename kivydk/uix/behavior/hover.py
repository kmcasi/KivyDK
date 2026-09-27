#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 07 Jan 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
"""
This behavior adds hover awareness to widgets, allowing them to react when a pointer enters
or leaves their area. It provides an easy way to create interactive UI elements that respond visually
or functionally to hover interactions, regardless of the input device.

§ section : example ¶

Sample illustrating how ``HoverBehavior`` can be used to create widgets that react to mouse hover.

§ show image : uix, behavior, TestHover.gif ¶

§ show code : uix, behavior, hover.py ¶
"""
__all__ = ("HoverBehavior",)

#// IMPORT
from kivy.input.motionevent import MotionEvent
from kivy.properties import AliasProperty, BooleanProperty


#// LOGIC
class HoverBehavior:
    """ A mixin that adds hover detection to any widget. """

    # [ Advanced Usage ] Property → Allows manual hover state overrides.
    _hover_state: BooleanProperty = BooleanProperty(False)

    def _get_hovered(self) -> bool:
        return self._hover_state

    hovered: AliasProperty = AliasProperty(_get_hovered, None, bind=("_hover_state",), cache=True)
    """
    Whether the widget is currently hovered.
    
    § alias property value : bool, False, _ ¶
    """

    __events__ = ["on_hover", "on_hover_enter", "on_hover_leave"]

    # noinspection PyUnresolvedReferences
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.register_for_motion_event("kdk_pointer")

        self.fbind("_hover_state", self._dispatch_hover_changes)

    def on_hover(self, state: bool) -> None:
        """
        Called when the widget's hover state changes.

        § parameters : state = ``True`` when the widget is hovered and ``False`` otherwise. ¶

        This method is dispatched for both :meth:`on_hover_enter` and :meth:`on_hover_leave` transitions.
        """
        pass

    def on_hover_enter(self) -> None:
        """ Called when the pointer begins hovering over the widget. """
        pass

    def on_hover_leave(self) -> None:
        """ Called when the pointer stops hovering over the widget. """
        pass

    # noinspection PyUnusedLocal, PyTypeChecker
    def _kdk_pointer_enter(self, event: MotionEvent) -> None:
        """
        Called when the pointer enters the widget's area.

        :param event: The MotionEvent associated with this call.
        """
        self._hover_state = True

    # noinspection PyUnusedLocal, PyTypeChecker
    def _kdk_pointer_leave(self, event: MotionEvent) -> None:
        """
        Called when the pointer leaves the widget's area.

        :param event: The MotionEvent associated with this call.
        """
        self._hover_state = False

    # noinspection PyUnusedLocal, PyUnresolvedReferences
    def _dispatch_hover_changes(self, *args) -> None:
        """ Dispatches hover-related events based on the current hover state. """
        self.dispatch("on_hover", self._hover_state)
        self.dispatch(f"on_hover_{'enter' if self._hover_state else 'leave'}")
