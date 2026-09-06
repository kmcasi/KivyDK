#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 21 Jan 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
__all__ = ("MonkeyPatchAll", "MonkeyPatchEvent")

#// IMPORT
from kivydk.tools.monkey.event import MonkeyPatchEvent


#// LOGIC
def MonkeyPatchAll() -> None:
    MonkeyPatchEvent()
