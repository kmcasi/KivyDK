#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 17 Apr 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
"""
This ``core`` package contains the low-level building blocks that power the entire KivyDK framework.
The module provide fundamental logic and system utilities that higher-level UI components rely on.

The purpose of ``core`` is to centralize functionality that must remain lightweight, reusable and independent of any
specific editor or widget. Most editors and UI components in KivyDK depend on these modules to provide
consistent behavior across the entire ecosystem.

.. caution::
    Unlike the widgets found in :mod:`kivydk.uix`, the classes and functions in ``core`` are **not** intended to be
    used directly as visual elements. They represent internal mechanisms that support the framework’s behavior.

.. important::
    If a feature appears to be missing at the widget level, consider checking :mod:`kivydk.uix` first before
    relying on ``core``.
"""
