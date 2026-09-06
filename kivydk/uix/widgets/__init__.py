#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 12 Feb 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
"""
This module contains the reusable UI components provided by KivyDK. Each widget is self‑contained and focuses on
a single responsibility providing, offering small, interactive elements used throughout the framework.

All public widgets are implemented entirely in Python (no KV language) to provide a clean, consistent and fully
code‑driven development experience. This approach keeps the API intuitive for developers who prefer Python‑only
workflows and avoids the structural complexity often introduced by KV‑based widget bundles.
Developers who wish to style these widgets using KV language are still free to do so.

.. important::
    All public widgets are also re‑exported through :mod:`kivydk.uix` to offer a flexible import style for developers:

    .. code-block:: python
        :class: no-copybutton

        from kivydk.uix import LineNumber                               # style: kivy
        from kivydk.uix.widgets import LineNumber                       # style: general
        from kivydk.uix.widgets.line_number import LineNumber           # style: explicit

    This structure keeps the internal organization clean while allowing users to choose the import pattern
    that best fits their workflow.
"""
__all__ = ("LineNumber",)

#// IMPORT
from .line_number import LineNumber
