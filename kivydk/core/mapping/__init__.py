#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 12 Jan 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
"""
This package contains lightweight semantic mappings used throughout KivyDK to make common
framework constants easier to discover and work with. The goal of these mappings is not to
abstract platform behavior, but to provide clean, IDE‑friendly namespaces that group related
identifiers into readable structures.

They exist purely to make the KivyDK API more expressive, discoverable and pleasant to use.
"""
__all__ = (
    "CursorDefault", "CursorWindows",
    "Icon"
)

#// IMPORT
from .cursors import CursorDefault, CursorWindows
from .icons import Icon
