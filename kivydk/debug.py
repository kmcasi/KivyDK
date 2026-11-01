#// IMPORT
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

from kivydk.uix.behavior.tooltip import TooltipBehavior
from kivydk.uix.tooltip import Tooltip


#// LOGIC
class MyButton(TooltipBehavior, Button):
    pass


class TestTooltip(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(spacing=16, size_hint_y=None, height=128, **kwargs)

        # Default tooltip
        self.add_widget(
            MyButton(
                text="Default tooltip",
                tooltip_text="This is a simple tooltip.",
            )
        )

        # Tooltip on the cursor position
        self.add_widget(
            MyButton(
                text="Cursor tooltip",
                tooltip_text="Tooltip shown on the cursor side.",
                tooltip_side="cursor",
            )
        )

        # Custom tooltip widget
        custom_tooltip = Tooltip(
            background_color=[0.2, 0.2, 0.2, 1.0],
            foreground_color=[0.9, 0.9, 0.9, 1.0],
            font_size="24sp",
            size_max=(256, 64)
        )

        self.add_widget(
            MyButton(
                text="Custom tooltip",
                tooltip_text="This tooltip is interactive and uses a custom widget.",
                tooltip_template=custom_tooltip,
                tooltip_side="left",
                tooltip_interactive=True,
                tooltip_offset="24sp",
            )
        )


#// RUN FILE
if __name__ == "__main__":
    from kivydk.app import App

    class Example(App):
        def build(self):
            return TestTooltip()

    Example().run()