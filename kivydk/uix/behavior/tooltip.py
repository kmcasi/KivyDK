#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 13 Sep 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
"""
TooltipBehavior does not create or manage tooltip widgets directly. Instead, it
exposes a small set of properties that describe how a tooltip should be rendered
and positioned. TooltipManager reads these properties and applies the appropriate
defaults or overrides when showing a tooltip for the widget.
"""
__all__ = ("TooltipBehavior",)

#// IMPORT
from kivy.properties import (
    BooleanProperty,
    NumericProperty,
    ObjectProperty,
    OptionProperty,
    StringProperty,
)

from kivydk.manager.tooltip import TooltipManager


#// LOGIC
class TooltipBehavior:
    """
    Declarative behavior that adds tooltip configuration to widgets.

    When a property is ``None``, TooltipManager falls back to its own default value.
    This allows widgets to customize only the aspects they need while preserving a
    consistent global tooltip style and behavior across the application.
    """

    tooltip_text: StringProperty = StringProperty()
    """ Text content displayed inside the tooltip. """

    tooltip_markup: BooleanProperty = BooleanProperty(False)
    """ Whether :attr:`tooltip_text` should be interpreted as markup. """

    tooltip_side: OptionProperty = OptionProperty(
        allownone = True,
        defaultvalue = None,
        options = TooltipManager.tooltip_side.options
    )
    """
    Preferred placement side for the tooltip relative to the widget.
    
    TooltipManager resolves this preference and selects the final side based on available screen space.
    """

    tooltip_offset: NumericProperty = NumericProperty(None, allownone=True)
    """ Additional offset ``(in pixels)`` applied between the tooltip and its anchor position (widget or cursor). """

    tooltip_template: ObjectProperty = ObjectProperty(None, allownone=True)
    """ Custom widget class or instance used to render the tooltip. """

    tooltip_interactive: BooleanProperty = BooleanProperty(None, allownone=True)
    """ Enable interactive tooltips instead of auto‑hiding hover hints. """

    __events__ = ["on_tooltip", "on_pre_tooltip"]

    # noinspection PyUnresolvedReferences
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.register_for_motion_event("kdk_tooltip")

    def on_tooltip(self, show: bool) -> None:
        """
        Called after the tooltip's visibility state changes.

        § parameters : state = ``True`` when the tooltip becomes visible/, and ``False`` otherwise. ¶
        """
        pass

    def on_pre_tooltip(self, show: bool) -> None:
        """
        Called before the tooltip's visibility state changes.

        § parameters : state = ``True`` when the tooltip is about to be shown/, and ``False`` otherwise. ¶
        """
        pass
