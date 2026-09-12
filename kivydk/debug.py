#// IMPORT
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.codeinput import CodeInput
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView

from kivy.properties import NumericProperty

from kivydk.uix import LineNumber

from kivy.uix.button import Button
from kivydk.uix.behavior.HoverBehavior import HoverBehavior


#// LOGIC
class HoverButton(HoverBehavior, Button):
    def on_hovered(self, instance, value):
        if value:
            self.background_color = (1, 0, 0, 1)
        else:
            self.background_color = (1, 1, 1, 1)


class TestLineNumber(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Components
        self.scroll_view = ScrollView(scroll_type=["bars"], bar_width="11dp")
        self.text_input = CodeInput(size_hint=(None, None))
        self.line_number = LineNumber(
            self.text_input,
            background_color=[0.3,0.3,0.3, 1.0], foreground_color=[1.0,1.0,1.0, 1.0]
        )

        # Packing
        self.scroll_view.add_widget(self.text_input)

        self.add_widget(self.line_number)
        self.add_widget(self.scroll_view)

        # Binds
        self.text_input.bind(text=self._update_text_height)
        self.scroll_view.bind(size=self._update_text_height)

    def _update_text_height(self, *args):
        height = len(self.text_input._lines_rects) * self.text_input.line_height
        height += self.text_input.padding[1] + self.text_input.padding[3]

        self.text_input.height = max(height, self.scroll_view.height)
        self.text_input.width = self.scroll_view.width
        self.line_number.refresh()


class Debug(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation="vertical", size_hint_x=None, width=128)
        self.txt_ln = TestLineNumber()

        self.debug_font_size = TextInput(text=str(self.txt_ln.text_input.font_size), size_hint_y=None, height="32sp")

        self.layout.add_widget(self.debug_font_size)
        self.add_widget(self.txt_ln)
        self.add_widget(self.layout)

        self.debug_font_size.bind(text=self._debug_font_size_change)

        for i in range(1000):
            self.txt_ln.text_input.text += "Line number %.4d\n" % (i + 1)

    def _debug_font_size_change(self, *_):
        try:
            font_size = int(self.debug_font_size.text.strip())
            if font_size > 0:
                self.txt_ln.text_input.font_size = font_size
        except ValueError: pass


#// RUN FILE
if __name__ == "__main__":
    from kivy.app import App

    class Example(App):
        def build(self):
            # return TestLineNumber()
            # return Debug()
            return HoverButton(text="HoverButton", size_hint_y=None, height=128)

    Example().run()