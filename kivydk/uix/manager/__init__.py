#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 12 Jan 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
"""
This module contains internal management systems used by KivyDK to coordinate and orchestrate widget‑level behavior.
These managers operate behind the scenes to provide higher‑level functionality such as hover tracking and other
UI interaction services that may be added in the future. They form part of the UIX infrastructure, ensuring that
complex interactions work consistently across the framework without requiring manual setup from the user.

.. attention::
    These modules are not intended for direct use. All managers are created and controlled internally by KivyDK
    and developers typically never need to interact with them directly.
"""
__all__ = ("HoverManager",)

#// IMPORT
from kivydk.uix.manager.hover import HoverManager
