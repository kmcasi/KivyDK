#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 12 Jan 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
"""
This module implements behaviors that can be `mixed in <https://en.wikipedia.org/wiki/Mixin>`_
with existing base widgets. The idea behind these classes is to encapsulate properties and events associated with
certain types of widgets.

Isolating these properties and events in a mixin class allows you to define your own implementation for standard kivy
widgets or kivydk widgets that can act as drop-in replacements. This means you can re-style and re-define widgets
as desired without breaking compatibility: as long as they implement the behavior correctly, they can simply replace
the standard widgets.

.. important::
    The behavior class must always be **before** the widget class. If you don't specify the inheritance in this order,
    the behavior may not work because the behavior methods are overwritten by the class method listed first.

    .. code-block:: python

        class Correct(ClickBehavior, Image):
            '''The correct way to implement a behavior.'''
            pass

        class Wrong(Image, ClickBehavior):
            '''The wrong way to implement a behavior.'''
            pass

.. caution::
    Similarly, if you combine a behavior class with a class which requires the use of the methods also defined by the
    behavior class, the resulting class may not function properly. For example, when combining the
    :class:`~kivydk.ui.behavior.click.ClickBehavior` with a :class:`kivy Button <kivy.uix.button.Button>`,
    both of which use the :class:`kivy ButtonBehavior <kivy.uix.behaviors.button.ButtonBehavior>` method,
    the resulting class may not work properly.
"""
__all__ = ("ClickBehavior", "HoverBehavior")


#// IMPORT
from kivydk.uix.behavior.click import ClickBehavior
from kivydk.uix.behavior.hover import HoverBehavior
