#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 14 Sep 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
"""
This module defines ``Abstract Base Classes`` used by KiviDK to formalize widget capabilities and
interaction patterns. The interfaces in this module provide a consistent foundation
for components that rely on specific widget behaviors, ensuring that custom widgets
can integrate cleanly with the framework. Concrete implementations are expected to
inherit from these interfaces and supply the required functionality.
"""
__all__ = ("TooltipWidgetABC",)

#// IMPORT
from .tooltip import TooltipWidgetABC
