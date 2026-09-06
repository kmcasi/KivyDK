#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 12 Feb 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
"""
This module contains the reusable user-interface components that form the visual layer of the KivyDK framework.
These widgets and layouts extend Kivy’s own UI system with additional behavior, interaction models and
higher-level abstractions designed specifically for editor-style applications.

These components are intended to be used directly when building interfaces for editors, tools and applications
within the KivyDK ecosystem. They are designed to be flexible, composable and consistent across the entire framework.

.. attention::
    The :mod:`kivydk.uix.manager` module is an internal component and is not intended for direct use.
    Developers typically should not need to import this module. Its functionality is reserved for the framework’s
    internal management of UI behavior.
"""

#// IMPORT
# Expose public widgets to not force the users to adapt to a totally new workflow
# Example valid imports for the same module:
#   from kivydk.uix import LineNumber                       # kivy style
#   from kivydk.uix.widgets import LineNumber               # module path
#   from kivydk.uix.widgets.line_number import LineNumber   # full path
from .widgets import *
