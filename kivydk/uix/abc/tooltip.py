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
__all__ = ("TooltipTemplate",)

#// IMPORT
from abc import abstractmethod

from kivy.properties import BooleanProperty
from kivy.uix.widget import Widget


#// LOGIC
class TooltipTemplate(Widget):
    """
    Abstract interface for tooltip widgets.

    TooltipManager relies on this interface to interact with any tooltip widget in
    a consistent way. Custom tooltip widgets must provide the required methods, so
    they can be positioned, updated and shown correctly within the tooltip system.
    """

    def __init__(self, **kwargs):
        if self.__class__ is TooltipTemplate:
            raise NotImplementedError("'TooltipTemplate' is abstract and cannot be instantiated.")

        super().__init__(**kwargs)

    @abstractmethod
    def update_text(self, text: str, markup: bool = False) -> None:
        """
        Update the tooltip's displayed text.

        Implementations should apply the text and prepare any internal layout changes required before sizing.

        Called whenever TooltipManager resolves a tooltip message for the hovered widget.
        """
        pass

    @abstractmethod
    def update_size(self) -> None:
        """
        Recalculate the widget’s size based on its current content.

        Implementations must update ``width`` and ``height`` to reflect the actual rendered size.

        TooltipManager calls this after updating the text, so it can compute
        the correct placement for the tooltip before making it visible.
        """
        pass
