#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 14 Jan 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
"""
The ``kivydk`` module provides the core infrastructure, global configuration and shared resources used throughout
the KivyDK framework. While most functionality is implemented in submodules, the top-level package exposes a small
set of global paths that define the runtime environment for all KivyDK components.
"""
__all__ = ("DIR_ROOT", "DIR_DATA", "DIR_FONTS")

#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| KivyDK monkey-patch's
#//|>-----------------------------------------------------------------------------------------------------------------<|
# from kivydk.tools.monkey.patch import MonkeyPatchAll

# MonkeyPatchAll()

#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| KivyDK directories
#//|>-----------------------------------------------------------------------------------------------------------------<|
from importlib.resources import files  # noqa: E402
from importlib.resources.abc import Traversable  # noqa: E402

#: The root directory of the KivyDK package.
DIR_ROOT: Traversable = files(__name__)

#: The base directory containing framework data files such as fonts, themes and other assets.
DIR_DATA: Traversable = DIR_ROOT / "data"

#: Directory containing all font resources automatically registered at startup.
DIR_FONTS: Traversable = DIR_DATA / "fonts"


#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| KivyDK initialization helpers
#//|>-----------------------------------------------------------------------------------------------------------------<|
from kivydk.core.resources.fonts import _auto_register_fonts  # noqa: E402

_auto_register_fonts(DIR_FONTS)


#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| KivyDK initialization log
#//|>-----------------------------------------------------------------------------------------------------------------<|
from kivydk._version import VERSION_STRING  # noqa: E402
from kivydk.logger import Logger  # noqa: E402

Logger.InfoS(version=VERSION_STRING, root_directory=DIR_ROOT)
