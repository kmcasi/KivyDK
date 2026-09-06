#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 12 Feb 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
"""
This module provides the :class:`LineNumber` widget, a companion component for
:class:`~kivy.uix.textinput.TextInput` that renders synchronized line numbers
alongside editable text.

Is intended for use in text editors, code editors and any UI
component where visible line numbering is required. The widget integrates
cleanly with both standalone TextInput instances and TextInputs embedded inside
a :class:`~kivy.uix.scrollview.ScrollView`.

The LineNumber widget handles automatic sizing, vertical alignment and
scroll synchronization, ensuring that the displayed line numbers always match
the visible portion of the associated TextInput.
"""
__all__ = ("LineNumber",)

#// IMPORT
from os import cpu_count
from concurrent.futures import ThreadPoolExecutor as Threads

from kivy.core.text import DEFAULT_FONT, Label
from kivy.graphics import Color, Rectangle, BorderImage
from kivy.graphics.texture import Texture
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from kivy.properties import StringProperty, NumericProperty, ColorProperty
from kivy.properties import OptionProperty, VariableListProperty


#// LOGIC
class LineNumber(Widget):
    """Widget that displays line numbers for a linked :class:`~kivy.uix.textinput.TextInput`.

    A :class:`~kivy.uix.textinput.TextInput` instance must be provided as the ``text_input`` argument.
    It is used to extract line information, wrapping state, scroll position
    and all metrics required to compute the widget’s size and vertical placement.

    When used together with a :class:`~kivy.uix.scrollview.ScrollView`, the
    :class:`LineNumber` widget must be placed outside the ScrollView. Its height and
    vertical offset are calculated automatically so that the visible line numbers
    remain synchronized with the associated TextInput, regardless of whether the
    TextInput is scrollable or not.

    The widget updates dynamically based on the state of the linked TextInput,
    including text changes, wrapping, scrolling and font metrics.
    """

    align: OptionProperty = OptionProperty("right", options=["left", "center", "right"])
    """Horizontal alignment of the line numbers."""

    background_color: ColorProperty = ColorProperty()
    """Tint color applied to the :attr:`background_texture`."""

    background_texture: StringProperty = StringProperty('atlas://data/images/defaulttheme/textinput')
    """Background image applied to the entire widget."""

    background_border: VariableListProperty = VariableListProperty([4])
    """Border used for :attr:`background_texture` graphics instruction.
    Can be used to define a custom background.
    
    The border may be specified as one, two or four values.
    These are expanded into a list of four values: ``[left, top, right, bottom]``."""

    #:
    font_context: StringProperty = StringProperty(None, allownone=True)

    #:
    font_family: StringProperty = StringProperty(None, allownone=True)

    #:
    font_name: StringProperty = StringProperty(DEFAULT_FONT, allownone=True)

    font_size: NumericProperty = NumericProperty("15sp")
    """Font size of the line numbers."""

    foreground_color: ColorProperty = ColorProperty([0.0, 0.0, 0.0, 1.0])
    """Color used to render the line numbers, in RGBA format."""

    padding: VariableListProperty = VariableListProperty([4], length=2)
    """Horizontal padding applied to the line numbers.

    The padding may be specified as one or two values.
    These are expanded into a list of two values: ``[left, right]``."""

    width_min: NumericProperty = NumericProperty("18sp")
    """Minimum desired width of the widget.

    The actual width is computed automatically based on :attr:`padding`,
    :attr:`font_size`, the active font and the current line‑number context.
    This property ensures that the computed width is never smaller than the specified minimum."""

    def __init__(self, text_input: TextInput, **kwargs) -> None:
        super().__init__(**kwargs)
        self.size_hint_x = None

        # Private variables
        self.__text_input: TextInput = text_input
        self.__desired_number_width: int = 0

        self.__bind()
        self._update_font()

    def __bind(self) -> None:
        self.bind(align=self._update_line_numbers,
                  background_color=self._update_line_numbers,
                  background_texture=self._update_line_numbers,
                  background_border=self._update_line_numbers,
                  font_context=self._update_font,
                  font_family=self._update_font,
                  font_name=self._update_font,
                  font_size=self._update_font,
                  foreground_color=self._update_line_numbers,
                  padding=self._update_line_numbers)

        self.__text_input.bind(parent=self._sync_scroll,
                               size=self._update_line_numbers,
                               text=self._update_line_numbers)

    def _sync_scroll(self, instance: TextInput, parent) -> None:
        """Used to bind the scroll event for updating the line numbers."""
        # Kivy’s unbind method is designed to quietly fail if the event handler doesn't exist
        instance.unbind(scroll_y=self._update_line_numbers)
        try:
            instance.parent.unbind(scroll_y=self._update_line_numbers)
        except KeyError:
            pass

        # Bind :attr:`scroll_y` base on the parent
        if isinstance(parent, ScrollView):
            instance.parent.bind(scroll_y=self._update_line_numbers)
        else:
            instance.bind(scroll_y=self._update_line_numbers)

    def _update_font(self, *_) -> None:
        """Used to calculate the maximum width need it to draw one number."""
        sizes: list[int] = []

        for number in range(10):
            label = Label(text=str(number), font_size=self.font_size, font_name=self.font_name,
                          font_family=self.font_family, font_context=self.font_context)
            label.refresh()
            sizes.append(label.texture.size[0])

        self.__desired_number_width = max(*sizes)
        self._update_line_numbers()

    def __draw_line_number(self, number: int, y: float, y_min_render: float, y_max_render: float) -> None:
        """Used to draw one line number."""
        # Make texture
        label: Label = Label(text=str(number), color=self.foreground_color, font_size=self.font_size,
                             font_name=self.font_name, font_family=self.font_family, font_context=self.font_context)
        label.refresh()

        # Get necessary values for drawing
        texture: Texture = label.texture
        size: list[int] = [*texture.size]
        uv: list[float] = [
            0.0, 1.0,  # bottom-left
            1.0, 1.0,  # bottom-right
            1.0, 0.0,  # top-right
            0.0, 0.0  # top-left
        ]

        # Update the values for partial visible ones
        if y > y_max_render:
            h: int = int(size[1] - (y - y_max_render))
            uv[5] = uv[7] = 1.0 - h / size[1]
            size[1] = h

        if y < y_min_render:
            h: int = int(y + size[1] - y_min_render)
            uv[1] = uv[3] = h / size[1]
            size[1] = h
            y = y_min_render

        # Calculate the horizontal position
        if self.align == "left":
            x = self.x + self.padding[0]
        elif self.align == "right":
            x = self.width - size[0] - self.padding[1]
        else:
            x = (self.width - size[0]) // 2

        # Draw the line number
        Rectangle(texture=texture, pos=(x, y), size=size, tex_coords=uv)

    def __count_wrapped_lines(self, arg: list[int, int]) -> int:
        """Used to count the amount of wrapped lines with multithreading."""
        wrapped: int = 0

        try:
            for index in range(arg[0], sum(arg)):
                if self.__text_input._lines_flags[index] != 1:
                    wrapped += 1

        except IndexError:
            pass

        return wrapped

    def _update_line_numbers(self, *_) -> None:
        """Update the visible line numbers"""

        # Draw the background
        with self.canvas.before:
            self.canvas.before.clear()
            Color(*self.background_color)
            BorderImage(
                source=self.background_texture,
                pos=self.pos, size=self.size,
                border=self.background_border[::-1]
            )

        # Draw the line number's
        with self.canvas.after:
            self.canvas.after.clear()
            Color(1.0, 1.0, 1.0, 1.0)

            # Get necessary values
            total_lines: int = len(self.__text_input._lines_flags)
            padding_top: float = self.__text_input.padding[1]
            padding_bottom: float = self.__text_input.padding[3]
            line_height: int = self.__text_input.line_height

            # Calculate the constraints
            y: float = self.top - padding_top - line_height
            y_min: float = self.y - line_height + 1
            # y_max:float = self.top - 1
            y_min_render: float = self.y
            y_max_render: float = self.top - line_height

            # Update the constraints base on the parent instance
            if not isinstance(self.__text_input.parent, ScrollView):
                y_min += padding_bottom
                # y_max -= padding_top
                y_min_render += padding_bottom
                y_max_render -= padding_top

            # Auto update the width
            desired_width: int = sum(self.padding) + self.__desired_number_width * len(str(total_lines))
            self.width = max(self.width_min, desired_width)

            # Calculate the scroll position, first visible lines and vertical position of the first line
            if isinstance(self.__text_input.parent, ScrollView):
                hidden_area: float = self.__text_input.height - self.height
                scroll: float = (1.0 - self.__text_input.parent.scroll_y) * hidden_area
                first_visible_line: int = max(0, int((scroll - padding_top) / line_height))

                try:
                    y = self.__text_input._lines_rects[first_visible_line].pos[1] - hidden_area + scroll + self.y
                except IndexError:
                    pass

            else:
                scroll: float = self.__text_input.scroll_y
                first_visible_line: int = max(0, int(scroll / line_height))
                y += scroll % line_height

            # If the text is wrapped, calculate the first logical line number
            if self.__text_input.do_wrap:
                line_number: int = first_visible_line
                cpus: int = max(2, cpu_count() - 7)

                # Use multithreading if is worth it. Otherwise, will be much slower than main thread
                if line_number > 100:
                    chunk_size: int = line_number // cpus
                    chunk_offset: int = line_number - chunk_size * cpus

                    with Threads() as threads:
                        chunks = [[cpu * chunk_size, chunk_size] for cpu in range(cpus)]
                        # Offset the first chunk by one, because the first line is not counted as a new line
                        chunks[0][0] += 1
                        chunks[0][1] -= 1

                        # If we have an unequal chunk size, use it also
                        if chunk_offset > 0:
                            chunks.append([cpus * chunk_size, chunk_offset])

                        # Use the multithreading for counting wrapped lines and update the line number
                        line_number -= sum(threads.map(self.__count_wrapped_lines, chunks))

                # Otherwise, use the main thread for counting the real line numbers
                else:
                    try:
                        for hidden_line in range(1, first_visible_line):
                            if self.__text_input._lines_flags[hidden_line] != 1:
                                line_number -= 1

                    except IndexError:
                        pass

            # Check for all visible lines
            for line in range(first_visible_line, total_lines):
                try:
                    # If the text is wrapped, draw the logical line number only for non-wrapped lines
                    if self.__text_input.do_wrap:
                        if self.__text_input._lines_flags[line] == 1 or line == 0:
                            line_number += 1
                            self.__draw_line_number(line_number, y, y_min_render, y_max_render)

                    # Otherwise draw the line number for every line
                    else:
                        self.__draw_line_number(line + 1, y, y_min_render, y_max_render)

                except IndexError:
                    pass

                # Move to the next line's y position
                y -= line_height

                # Break if we've rendered all the visible lines
                if y < y_min: break
