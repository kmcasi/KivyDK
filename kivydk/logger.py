#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 21 Jan 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
__all__ = ("Logger",)

#// IMPORT
import logging as PYLog
from kivy.logger import Logger as KVLog


#// LOGIC
class Logger:
    __template:str = "KivyDK: {} \u279C {}"

    @staticmethod
    def __compute_args(*args) -> str:
        out:str = ""

        for arg in args:
            out = f"{out}, {str(arg)}"

        return out[2:]

    @staticmethod
    def __format_keys(kwargs:dict[str, any]) -> tuple[str, any]:
        for key, args in kwargs.items():
            yield str(key).capitalize().replace("_", " "), args

    @staticmethod
    def Log(level:int, key:str, *args) -> None:
        KVLog.log(level, Logger.__template.format(key, Logger.__compute_args(*args)))

    @staticmethod
    def LogS(level:int, **kwargs) -> None:
        for formated in Logger.__format_keys(kwargs):
            Logger.Log(level, *formated)

    @staticmethod
    def Debug(key:str, *args) -> None:
        Logger.Log(PYLog.DEBUG, key, *args)

    @staticmethod
    def DebugS(**kwargs) -> None:
        Logger.LogS(PYLog.DEBUG, **kwargs)

    @staticmethod
    def Info(key:str, *args) -> None:
        Logger.Log(PYLog.INFO, key, *args)

    @staticmethod
    def InfoS(**kwargs) -> None:
        Logger.LogS(PYLog.INFO, **kwargs)

    @staticmethod
    def Warn(key:str, *args) -> None:
        Logger.Log(PYLog.WARN, key, *args)

    @staticmethod
    def WarnS(**kwargs) -> None:
        Logger.LogS(PYLog.WARN, **kwargs)

    @staticmethod
    def Error(key:str, *args) -> None:
        Logger.Log(PYLog.ERROR, key, *args)

    @staticmethod
    def ErrorS(**kwargs) -> None:
        Logger.LogS(PYLog.ERROR, **kwargs)

    @staticmethod
    def Fatal(key:str, *args) -> None:
        Logger.Log(PYLog.FATAL, key, *args)

    @staticmethod
    def FatalS(**kwargs) -> None:
        Logger.LogS(PYLog.FATAL, **kwargs)
