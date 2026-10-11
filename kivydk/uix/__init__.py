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

These components are intended to be used directly when building interfaces for editors, tools and applications
within the KivyDK ecosystem. They are designed to be flexible, composable and consistent across the entire framework.
"""
__all__ = ("LineNumber",)

#// IMPORT
from .line_number import LineNumber
from .tooltip import Tooltip
