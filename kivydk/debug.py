#// IMPORT
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

from kivydk.uix.behavior import ClickBehavior


#// LOGIC
class TestClick(ClickBehavior, Label):
    """Each event updates the label text to reflect the current click state."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Local variables
        self.count_click = 0
        self.count_double_click = 0
        self.last_button_click = "-"
        self.last_button_double_click = "-"

        # Initialize the label with default information
        self.update_text()

    def on_click(self, button, modifiers):
        self.count_click += 1
        self.last_button_click = button
        self.update_text()

    def on_double_click(self, button, modifiers):
        self.count_double_click += 1
        self.last_button_double_click = button
        self.update_text()

    def update_text(self, *args):
        """
        Update the label text to display the current click information.

        :type args:     tuple[Any, ...]
        :param args:    Unused arguments from event callbacks.
        """
        single_click = f"Click's amount: %.2d" % self.count_click
        double_click = f"Double click's amount: %.2d" % self.count_double_click
        last_single_click = f"Last clicked button: %s" % self.last_button_click
        last_double_click = f"Last double clicked button: %s" % self.last_button_double_click

        self.text = f"{single_click}\n{double_click}\n\n{last_single_click}\n{last_double_click}"

        with self.canvas.before:
            self.canvas.before.clear()
            Color(0.4, 0.3, 0.2, 1.0)
            Rectangle(pos=(self.x, self.height-3), size=(512, 3))


#// RUN FILE
if __name__ == "__main__":
    from kivy.app import App
    from kivy.core.window import Window

    class Example(App):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            Window.size = 512, 512-32

        def build(self):
            return TestClick(size_hint_y=None, height=256)

    Example().run()
