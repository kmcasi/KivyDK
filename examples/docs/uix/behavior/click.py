#// IMPORT
from kivy.uix.label import Label

from kivydk.uix.behavior import ClickBehavior


#// LOGIC
class TestClick(ClickBehavior, Label):
    """Each event updates the label text to reflect the current click state."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Local variables to count the clicks
        self.count_click = 0
        self.count_double_click = 0

        # Initialize the label with default information
        self.update_text()

        # Register event to update the text for press/release
        # `state` is classic kivy property
        self.bind(state=self.update_text)

    def on_click(self):
        self.count_click += 1
        self.update_text()

    def on_double_click(self):
        self.count_double_click += 1
        self.update_text()

    def update_text(self, *args):
        """
        Update the label text to display the current click state.

        :type args:     tuple[Any, ...]
        :param args:    Unused arguments from event callbacks.
        """
        state = "Click state: %s" % ("press" if self.state == "down" else "release")
        single_click = f"Click's amount: %.2d" % self.count_click
        double_click = f"Double click's amount: %.2d" % self.count_double_click

        self.text = f"{single_click}\n{double_click}\n\n{state}"


#// RUN FILE
if __name__ == "__main__":
    from kivy.app import App

    class Example(App):
        def build(self):
            return TestClick(size_hint_y=None, height=256)

    Example().run()
