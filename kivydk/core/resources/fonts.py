#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 06 Jan 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
"""
This module provides the font‑registration layer used internally by KivyDK. Its primary responsibility is to
prepare and register all bundled font families, so they can be used consistently across the framework.

During initialization, the module automatically registers several font sets including JetBrainsMono, MaterialIcons
and other internal fonts ensuring that text rendering behaves the same on every supported platform.

Only a minimal public API is exposed for introspection.
"""
__all__ = ("get_registered_fonts", "get_supported_font_styles")

#// IMPORT
from os.path import join
from importlib.resources.abc import Traversable

from kivy.core.text import LabelBase


#// LOGIC
def _auto_register_fonts(fonts_dir:Traversable) -> None:
    """
    Internal helper used during KivyDK initialization to register the framework's bundled fonts.
    """
    # OTF files will need pango for the features of JetBrainsMono_OTF
    # https://github.com/JetBrains/JetBrainsMono/wiki/OpenType-features
    # https://fonts.google.com/icons?icon.set=Material+Icons
    fonts_directory: str = str(fonts_dir)

    fonts: list[dict[str, str]] = [
        {
            "name":             "JetBrainsMono",
            "fn_regular":       join(fonts_directory, "JetBrainsMono", "JetBrainsMono-Regular.ttf"),
            "fn_italic":        join(fonts_directory, "JetBrainsMono", "JetBrainsMono-Italic.ttf"),
            "fn_bold":          join(fonts_directory, "JetBrainsMono", "JetBrainsMono-Bold.ttf"),
            "fn_bolditalic":    join(fonts_directory, "JetBrainsMono", "JetBrainsMono-BoldItalic.ttf")
        },
        {
            "name":             "JetBrainsMono_OTF",
            "fn_regular":       join(fonts_directory, "JetBrainsMono", "JetBrainsMono-Regular.otf"),
            "fn_italic":        join(fonts_directory, "JetBrainsMono", "JetBrainsMono-Italic.otf"),
            "fn_bold":          join(fonts_directory, "JetBrainsMono", "JetBrainsMono-Bold.otf"),
            "fn_bolditalic":    join(fonts_directory, "JetBrainsMono", "JetBrainsMono-BoldItalic.otf")
        },
        {
            "name":             "MaterialIcons",
            "fn_regular":       join(fonts_directory, "MaterialIcons", "MaterialIcons-Filled.ttf"),
            "fn_italic":        join(fonts_directory, "MaterialIcons", "MaterialIcons-Outlined.otf"),
            "fn_bold":          join(fonts_directory, "MaterialIcons", "MaterialIcons-Round.otf"),
            "fn_bolditalic":    join(fonts_directory, "MaterialIcons", "MaterialIcons-TwoTone.otf")
        },
        {
            # This is only temporarily. `MaterialIcons` need to be sorted before to use it.
            "name": "Icons",
            "fn_regular":       join(fonts_directory, "materialdesignicons-webfont.ttf")
        },
    ]

    for font in fonts:
        LabelBase.register(**font)


def get_registered_fonts() -> list[str]:
    """
    Returns the names of all fonts that have been successfully registered with Kivy's text provider.
    Useful for introspection, debugging or presenting available font options to the user.
    """
    return [*LabelBase._fonts.keys()]


def get_supported_font_styles(font_name: str) -> dict[str, bool]:
    """
    Inspects the registered font entry and reports which style variants are actually backed by distinct font files.
    This allows callers to determine whether italic, bold or bold‑italic styles are available or whether the
    regular style will be used as a fallback.

    .. tip::
        If the font is not registered, all values are returned as False. In this case the ``regular`` style
        can be used as a simple validity check without raising errors or warnings.

    :type font_name:    str
    :param font_name:   The name of a font that has already been registered.

    :return: A dictionary with boolean flags for **regular**, **italic**, **bold** and **bolditalic**,
            indicating which styles the font supports.
    """
    if font_name in LabelBase._fonts.keys():
        files: tuple[str] = LabelBase._fonts[font_name]

        return {
            "regular": True,
            "italic": files[0] != files[1],
            "bold": files[0] != files[2],
            "bolditalic": files[0] != files[3]
        }

    return {"regular": False, "italic": False, "bold": False, "bolditalic": False}
