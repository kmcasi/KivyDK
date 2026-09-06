#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 19 Jan 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
"""
This module implements the resource-management layer used internally by KivyDK. It handles tasks such as registering
bundled fonts and preparing UI resources for use by higher-level components. Although the module’s primary purpose
is internal, it exposes a minimal public API that allows developers to inspect or query registered resources
when needed. Only these stable entry points are documented here.
"""
__all__ = ("get_registered_fonts","get_supported_font_styles")

#// IMPORT
from .fonts import get_registered_fonts
from .fonts import get_supported_font_styles
