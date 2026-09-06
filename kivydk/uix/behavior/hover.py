#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 07 Jan 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
"""
This behavior adds simple hover awareness to widgets, allowing them to react when the mouse cursor moves over
or away from them. It provides an easy way to create interactive, desktop‑friendly UI elements that respond visually
or functionally to hover interactions.

§ section : example ¶

Sample illustrating how ``HoverBehavior`` can be used to create widgets that react to mouse hover.

§ show image : uix, behavior, TestHover.gif ¶

§ show code : uix, behavior, hover.py ¶
"""
__all__ = ("HoverBehavior",)

#// IMPORT
from kivy.properties import AliasProperty, BooleanProperty

from kivydk.uix.manager.hover import HoverManager


#// LOGIC
class HoverBehavior(object):
    """A mixin that adds lightweight hover detection to any widget."""

    _hover_state: BooleanProperty = BooleanProperty(False)

    def _get_hovered(self) -> bool:
        return self._hover_state

    hovered: AliasProperty = AliasProperty(_get_hovered, None, bind=("_hover_state",), cache=True)
    """
    Whether the mouse cursor is currently hovering over the widget.
    
    § alias property value : bool, False, _ ¶
    """

    __events__ = ["on_hover", "on_hover_start", "on_hover_end"]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.fbind("parent", self._auto_register)
        self.fbind("_hover_state", self._dispatch_hover)

    def on_hover(self, state: bool) -> None:
        """
        Called when the cursor enters and leaves the widget's bounds.

        § parameters : state = ``True`` when the cursor is currently hovering over the widget and ``False`` otherwise. ¶

        This method is dispatched every time the hover state changes, allowing widgets to react
        to both hover‑start and hover‑end transitions.
        """
        pass

    def on_hover_start(self) -> None:
        """Called when the cursor enters the widget's bounds."""
        pass

    def on_hover_end(self) -> None:
        """Called when the cursor leaves the widget's bounds."""
        pass

    def _auto_register(self, instance, parent) -> None:
        if parent is not None:
            HoverManager.register(self)
        else:
            HoverManager.unregister(self)

    def _dispatch_hover(self, *args) -> None:
        self.dispatch("on_hover", self._hover_state)
        self.dispatch("on_hover_start" if self._hover_state else "on_hover_end")
