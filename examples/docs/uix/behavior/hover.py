#// IMPORT
from kivy.uix.button import Button

from kivydk.uix.behavior import HoverBehavior


#// LOGIC
class TestHover(HoverBehavior, Button):
    """ Updates the Button's color and text to reflect the current hover state. """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Initialize the button style with default information
        self.on_hover(self.hovered)

    def on_hover(self, state):
        """
        Update the label text and background color to reflect the current hover state.

        :param state: ```True`` when the widget is hovered and ``False`` otherwise.
        """
        self.background_color = [0.8, 0.4, 0.2, 1.0] if state else [1.0, 1.0, 1.0, 1.0]
        self.text = "Hovered" if state else "Unhovered"


#// RUN FILE
if __name__ == "__main__":
    from kivydk.app import App

    class Example(App):
        def build(self):
            return TestHover(size_hint_y=None, height=256)

    Example().run()
