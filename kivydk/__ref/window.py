#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 12 Jan 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
__all__ = ("Window",)

#// IMPORT
from kivy.core.window import Window as WindowKivy

#// GLOBAL VARIABLES
# TODO: Need a better implementation to support also the `panda3d` library.
Window = WindowKivy
# Window = WindowPanda3D


#// LOGIC
