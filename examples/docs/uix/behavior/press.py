#// IMPORT
from kivy.uix.label import Label

from kivydk.uix.behavior import PressBehavior


#// LOGIC
class TestPress(PressBehavior, Label):
    """ Each event updates the label text to reflect the current press state. """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Provide the default label context
        self.text = "Press Example"
        self.font_size = "18 dp"

    def on_press(self, button, modifiers):
        self.text = f"The {button!r} button was pressed."

    def on_release(self, button, modifiers, inside):
        self.text = f"The {button!r} button was released {'inside' if inside else 'outside'}."


#// RUN FILE
if __name__ == "__main__":
    from kivydk.app import App

    class Example(App):
        def build(self):
            return TestPress(size_hint_y=None, height=256)

    Example().run()
