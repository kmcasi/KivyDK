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
from kivy.properties import ObjectProperty, OptionProperty, StringProperty


#// LOGIC
class TooltipBehavior:
    """
    Declarative behavior that adds tooltip configuration to widgets.

    Each property may override the corresponding default stored in TooltipManager.
    When a property is ``None``, TooltipManager falls back to its own default value.
    This allows widgets to customize only the aspects they need while preserving a
    consistent global tooltip style and behavior across the application.
    """

    tooltip_widget: ObjectProperty = ObjectProperty(None, allownone=True)
    """Custom widget class or instance used to render the tooltip."""

    tooltip_position: OptionProperty = OptionProperty(None, allownone=True, options=[
        ["cursor"], ["left"], ["top"], ["right"], ["bottom"],

        ["cursor", "left"], ["left", "cursor"],
        ["cursor", "top"],      ["top",     "cursor"],
        ["cursor", "right"],    ["right",   "cursor"],
        ["cursor", "bottom"],   ["bottom",  "cursor"],

        ["top", "left"],        ["left",    "top"],
        ["top", "right"],       ["right",   "top"],

        ["bottom", "left"],     ["left",    "bottom"],
        ["bottom", "right"],    ["right",   "bottom"],
    ])
    """
    Preferred placement rules for the tooltip relative to the widget.
    TooltipManager resolves these rules and selects the final position based on available screen space.
    """

    tooltip_text: StringProperty = StringProperty()
    """Text displayed inside the tooltip."""
