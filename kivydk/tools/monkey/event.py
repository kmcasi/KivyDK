#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 21 Jan 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
__all__ = ("MonkeyPatchEvent", "EventDispatcherDK")

#// IMPORT
import kivy.event

from kivy._event import EventDispatcher as _KV_EventDispatcher


#// LOGIC
class EventDispatcherDK(_KV_EventDispatcher):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        # Local variables
        self.__dk_cache_events = {}

    def bind(self, **kwargs) -> None:
        super().bind(**kwargs)

        print(self)
        for key, value in kwargs.items():
            print(f"  {key}: {value}")
            try_uid, try_module = None, None
            try: try_uid = value.uid
            except AttributeError: pass
            try: try_module = value.__module__
            except AttributeError: pass
            print("\t\t", self.__class__, value.__class__)
            print("\t\t", self.__module__, try_module)
            print("\t\t", self.uid, try_uid)


def MonkeyPatchEvent() -> None:
    kivy.event.EventDispatcher = EventDispatcherDK
