#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 30 Aug 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|

#// IMPORT
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView

from uix.widgets.line_number import LineNumber

from kivy.properties import StringProperty, NumericProperty, ColorProperty, OptionProperty
from kivy.properties import ListProperty, VariableListProperty


#// GLOBAL VARIABLES


#// LOGIC
class Debug(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout_main = BoxLayout(orientation="horizontal")
        self.scroll_view = ScrollView(scroll_type=["bars"], bar_width='11dp')

        self.text_input = TextInput(size_hint=(None, None))
        self.line_number = LineNumber(
            self.text_input,
            # width_min="42sp",
            background_color=[0.3,0.3,0.3, 1.0], foreground_color=[1.0,1.0,1.0, 1.0]
        )

    def build(self):
        self.scroll_view.add_widget(self.text_input)

        self.layout_main.add_widget(self.line_number)
        self.layout_main.add_widget(self.scroll_view)

        self.text_input.bind(text=self._update_text_height)
        Window.bind(size=self._update_size)

        return self.layout_main

    def on_start(self):
        sturtup_text: str = ""

        with open(__file__) as file:
            sturtup_text = file.read()

        Clock.schedule_once(lambda _:self._set_startup_text(sturtup_text), 3)

    def _update_text_height(self, parent: TextInput, *_) -> None:
        height = len(parent._lines_rects) * parent.line_height
        height += parent.padding[1] + parent.padding[3]

        parent.height = max(height, self.scroll_view.height)
        parent.width = self.scroll_view.width

    def _set_startup_text(self, text:str) -> None:
        self.text_input.text = text

    def _update_size(self, parent: Window, size: tuple[int, int]) -> None:
        self.text_input.width = self.scroll_view.width = size[0] - self.line_number.width
        self.scroll_view.height = size[1]


#// RUN
if __name__ == "__main__":
    Debug().run()
