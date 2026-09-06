#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 07 Jan 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|

#// IMPORT
from kivy.uix.label import Label

from kivy.utils import escape_markup, get_hex_from_color
from kivy.properties import NumericProperty, StringProperty, ColorProperty, OptionProperty

from kivydk.core.mapping.icons import Icon
from kivydk.uix.behavior.hover import HoverBehavior
from kivydk.uix.behavior.click import ClickBehavior


#// LOGIC
class ButtonIcon(ClickBehavior, HoverBehavior, Label):
    icon = StringProperty(Icon.CursorDefaultClickOutline)
    """Icon of the button.

    :attr:`icon` is a :class:`~kivy.properties.StringProperty` and defaults to
    :data:`Icon.CursorDefaultClickOutline <kivydk.mapping.icons.Icon.CursorDefaultClickOutline>`."""

    icon_hover = StringProperty(Icon.CursorDefaultClick, allownone=True)
    """Icon of the button when hovered.
    
    If None is provided the icon will not be changed when the cursor hover the button.

    :attr:`icon_hover` is a :class:`~kivy.properties.StringProperty` and defaults to
    :data:`Icon.CursorDefaultClick <kivydk.mapping.icons.Icon.CursorDefaultClick>`."""

    icon_color = ColorProperty([.5, .5, .5, 1])
    """Text color of the icon, in the RGBA format.

    :attr:`icon_color` is a :class:`~kivy.properties.ColorProperty` and defaults to `[0.5, 0.5, 0.5, 1.0]`."""

    icon_color_hover = ColorProperty([1, .5, .1, 1])
    """Text color of the icon when hovered, in the RGBA format.

    :attr:`icon_color` is a :class:`~kivy.properties.ColorProperty` and defaults to `[1.0, 0.5, 0.1, 1.0]`."""

    icon_size = NumericProperty("24sp")
    """Font size of the icon, in pixels.

    :attr:`font_size` is a :class:`~kivy.properties.NumericProperty` and defaults to `24sp`."""

    icon_position = OptionProperty("left", options=["left", "right"])
    """Position of the icon relative to the text.
    
    :attr:`icon_position` is an :class:`~kivy.properties.OptionProperty` and defaults to "left"."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        # Some default values what are need it no mather what
        self.markup = True

        # Local variables
        self.__text_changed_internally:bool = False
        self.__icon_format:str = "[color={color}][size={size}][font=Icons]{icon}[/font][/size][/color]"
        self.__cached_text:str = escape_markup(self.text)

        self._update_text()

        self.fbind("text", self._cache_text)

        self.fbind("icon", self._update_text)
        self.fbind("icon_hover", self._update_text)

        self.fbind("icon_color", self._update_text)
        self.fbind("icon_color_hover", self._update_text)

        self.fbind("icon_size", self._update_text)
        self.fbind("icon_position", self._update_text)

        self.fbind("on_click", self._update_click)
        self.fbind("on_hover", self._update_text)

    def _update_text(self, *args) -> None:
        formated_icon:str = self.__icon_format.format(
            icon=self.icon_hover if (self.hovered and self.icon_hover is not None) else self.icon,
            color=get_hex_from_color(self.icon_color_hover) if self.hovered else get_hex_from_color(self.icon_color),
            size=int(self.icon_size)
        )

        if self.icon_position == "left":
            self.__change_text(formated_icon, self.__cached_text)
        else:
            self.__change_text(self.__cached_text, formated_icon)

    def _update_click(self, *args) -> None:
        msg:str = "{cat} OR {dog} = {smile}&{heart}".format(
            cat = self.__icon_format.format(icon=Icon.Cat, color="#FF9999", size=int(self.icon_size)),
            dog = self.__icon_format.format(icon=Icon.Dog, color="#80380C", size=int(self.icon_size)),
            heart = self.__icon_format.format(icon=Icon.Heart, color="#FF4C4C", size=int(self.icon_size)),
            smile = self.__icon_format.format(icon=Icon.EmoticonExcited, color="#FFC77F", size=int(self.icon_size))
        )

        self.__change_text(msg)

    def _cache_text(self, instance:object, new_text:str) -> None:
        if self.__text_changed_internally:
            self.__text_changed_internally = False

        else:
            self.__cached_text = escape_markup(new_text)
            self._update_text()

    def __change_text(self, *values) -> None:
        """Internal function to change the text.

        The main purpose is to not forget to flagg the change, otherwise the text will not render as expected."""
        self.__text_changed_internally = True
        self.text = "".join(values)
