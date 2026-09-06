#// IMPORT
from kivy.uix.button import Button

from kivydk.uix.behavior import HoverBehavior


#// LOGIC
class TestHover(HoverBehavior, Button):
    """Each event updates the color and text to reflect the current hover state."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Initialize the button with default information
        self.on_hover()

    def on_hover(self, *args):
        """
        Update the label text and color to display the current hover state.

        :param args: Unused arguments from event callbacks.
        """
        self.background_color = [0.8, 0.4, 0.2, 1] if self.hovered else [1, 1, 1, 1]
        self.text = "Hovered" if self.hovered else "Unhovered"


#// RUN FILE
if __name__ == "__main__":
    from kivy.app import App

    class Example(App):
        def build(self):
            return TestHover(size_hint_y=None, height=256)

    Example().run()
