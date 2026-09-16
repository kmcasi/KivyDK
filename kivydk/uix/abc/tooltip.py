#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 13 Sep 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
"""
Defines the abstract interface required for tooltip rendering widgets. Any widget used
as a tooltip must implement this interface so that TooltipManager can update its content,
size, position and visibility in a consistent and predictable way.

The interface does not impose any visual style or layout. Applications may provide their
own tooltip widget implementations as long as the required methods are implemented.
"""
__all__ = ("TooltipWidgetABC",)

#// IMPORT
from abc import abstractmethod
from kivy.uix.widget import Widget


#// LOGIC
class TooltipWidgetABC(Widget):
    """
    Abstract interface for tooltip widgets.

    TooltipManager relies on this interface to interact with any tooltip widget in
    a consistent way. Custom tooltip widgets must provide the required methods, so
    they can be positioned, updated and shown correctly within the tooltip system.
    """

    @abstractmethod
    def update_text(self, text: str) -> None:
        """Update the tooltip's displayed text."""
        pass

    @abstractmethod
    def update_position(self, x: float, y: float) -> None:
        """
        Move the tooltip to the given window coordinates.
        TooltipManager ensures the coordinates are already resolved according to the chosen anchor and widget's size.
        """
        pass

    @abstractmethod
    def update_size(self) -> None:
        """
        Recalculate the widget’s size based on its current content.
        Called whenever TooltipManager requires the widget’s actual size to be updated.
        """
        pass

    @abstractmethod
    def on_show(self, *args) -> None:
        """
        Called when the tooltip becomes visible.
        Implementations may perform layout adjustments or prepare internal state before rendering.
        """
        pass

    @abstractmethod
    def on_close(self, *args) -> None:
        """
        Called when the tooltip is hidden.
        Implementations may release resources or reset internal state before removal.
        """
        pass
