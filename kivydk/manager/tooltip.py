#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 18 Sep 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
""" < Module documentation here > """
__all__ = ("TooltipManager", "TooltipManagerBase")

#// IMPORT
from kivy.properties import ObjectProperty, OptionProperty, StringProperty

from kivydk.uix.widgets.tooltip import Tooltip


#// LOGIC
class TooltipManagerBase:

    tooltip_widget: ObjectProperty = ObjectProperty(Tooltip)
    """ Custom widget class or instance used to render the tooltip. """

    tooltip_position: OptionProperty = OptionProperty(["cursor"], options=[
        ["cursor"], ["left"], ["top"], ["right"], ["bottom"],

        ["cursor", "left"],     ["left", "cursor"],
        ["cursor", "top"],      ["top",     "cursor"],
        ["cursor", "right"],    ["right",   "cursor"],
        ["cursor", "bottom"],   ["bottom",  "cursor"],

        ["top", "left"],        ["left",    "top"],
        ["top", "right"],       ["right",   "top"],

        ["bottom", "left"],     ["left",    "bottom"],
        ["bottom", "right"],    ["right",   "bottom"],
    ])
    """ Preferred placement rules for the tooltip relative to the widget. """


#: Global manager responsible for efficient tooltip system.
TooltipManager: TooltipManagerBase = TooltipManagerBase()
