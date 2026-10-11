#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 13 Sep 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
"""
Implements the default tooltip widget used by KiviDK. This widget provides a
ready‑to‑use tooltip suitable for general applications, allowing developers to
benefit from tooltip functionality without creating a custom widget.

The widget conforms to :class:`~kivydk.uix.abc.tooltip.TooltipWidgetABC` and is
fully compatible with TooltipManager. Developers may use it directly or
substitute their own tooltip widget when custom styling or interaction is required.
"""
__all__ = ("Tooltip",)

# // IMPORT
from kivy.core.text import DEFAULT_FONT     # noqa
from kivy.graphics import (
    BorderImage,
    Color,
)
from kivy.properties import (
    ColorProperty,
    NumericProperty,
    ReferenceListProperty,
    StringProperty,
    VariableListProperty,
)
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from kivydk.uix.abc.tooltip import TooltipTemplate


# // LOGIC
class Tooltip(TooltipTemplate):
    """
    Default tooltip widget implementation.

    Designed to serve as a general‑purpose tooltip for most applications, this
    widget integrates with TooltipManager and can be replaced with a custom
    implementation when needed.
    """

    padding: VariableListProperty = VariableListProperty([6, 4])
    """
    Padding between the widget’s bounding box and its content.

    § variable list use ¶
    """

    background_color: ColorProperty = ColorProperty()
    """ Tint color applied to the :attr:`background_texture`. """

    background_texture: StringProperty = StringProperty("atlas://data/images/defaulttheme/textinput")
    """ Background image applied to the entire widget. """

    background_border: VariableListProperty = VariableListProperty(4)
    """
    Border definition used when rendering :attr:`background_texture`.
    This controls how the texture is sliced, allowing custom backgrounds to be applied.
    
    § variable list use ¶
    """

    #: tooltip text
    foreground_color: ColorProperty = ColorProperty([0.0, 0.0, 0.0, 1.0])

    #: tooltip text
    font_context: StringProperty = StringProperty(None, allownone=True)

    #: tooltip text
    font_family: StringProperty = StringProperty(None, allownone=True)

    #: tooltip text
    font_name: StringProperty = StringProperty(DEFAULT_FONT, allownone=True)

    #: tooltip text
    font_size: NumericProperty = NumericProperty("16sp")

    width_max: NumericProperty = NumericProperty(256)
    """ Maximum width of the widget. """

    height_max: NumericProperty = NumericProperty(256)
    """ Maximum height of the widget. """

    size_max: ReferenceListProperty = ReferenceListProperty(width_max, height_max)
    """ Maximum size of the widget. """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # Overwrite default values
        self.size_hint = None, None

        # Local variables
        self.__label_size: tuple[int, int] = (0, 0)

        # Components
        self.__layout: ScrollView = ScrollView(size_hint=self.size_hint)
        self.__label: Label = Label(size_hint=self.size_hint)

        # Initialization
        self._update_label_style()
        self.__bind()

        # Packing
        self.__layout.add_widget(self.__label)
        self.add_widget(self.__layout)

    def __bind(self) -> None:
        self.fbind("foreground_color", self._update_label_style)

        self.fbind("font_context", self._update_label_style)
        self.fbind("font_family", self._update_label_style)
        self.fbind("font_name", self._update_label_style)
        self.fbind("font_size", self._update_label_style)

        self.fbind("padding", self.update_size)
        self.fbind("size_max", self.update_size)

        self.fbind("pos", self._update_background)

    # noinspection PyUnusedParameter
    def _update_label_style(self, *args) -> None:
        self.__label.color = self.foreground_color
        self.__label.font_context = self.font_context
        self.__label.font_family = self.font_family
        self.__label.font_name = self.font_name
        self.__label.font_size = self.font_size

    def update_text(self, text: str, markup: bool = False) -> None:
        """ Update the tooltip's displayed text. """
        self.__label.text = text
        self.__label.markup = markup
        self.__label.text_size = (None, None)

    def update_size(self) -> None:
        self.__label.texture_update()

        padding_horizontal: float = self.padding[0] + self.padding[2]
        padding_vertical: float = self.padding[1] + self.padding[3]
        texture_size: list[float] = self.__label.texture_size
        texture_size_max: tuple[int, int] = (self.width_max - padding_horizontal, self.height_max - padding_vertical)
        this_size: list[float] = [texture_size[0] + padding_horizontal, texture_size[1] + padding_vertical]

        if texture_size[0] > texture_size_max[0]:
            self.__label.text_size = (texture_size_max[0], None)
            self.__label.texture_update()

            this_size[0] = self.width_max
            texture_size = self.__label.texture_size

        if texture_size[1] > texture_size_max[1]:
            this_size[1] = self.height_max

        self.__label.size = self.__label.texture_size
        self.__layout.size = (
                this_size[0] - padding_horizontal,
                this_size[1] - padding_vertical
        )
        self.size = this_size

    # noinspection PyUnusedParameter
    def _update_background(self, *args) -> None:
        """ Called when the tooltip becomes visible. """
        self.__layout.pos = (self.x + self.padding[0], self.y + self.padding[3])
        # self.__layout.pos = self.pos

        # Draw the background
        with self.canvas.before:
            self.canvas.before.clear()

            Color(*self.background_color)
            BorderImage(
                source=self.background_texture,
                pos=self.pos, size=self.size,
                border=self.background_border[::-1]
            )
