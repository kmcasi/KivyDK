#// IMPORT
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.codeinput import CodeInput
from kivy.uix.scrollview import ScrollView

from kivydk.uix import LineNumber


#// LOGIC
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


#// RUN FILE
if __name__ == "__main__":
    from kivy.app import App

    class Example(App):
        def build(self):
            return TestLineNumber()

    Example().run()