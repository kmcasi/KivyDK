from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle

from kivydk.uix.behavior.hover import HoverBehavior
from kivydk.uix.behavior.tooltip import TooltipBehavior
from kivydk.uix.tooltip import Tooltip


class MyButton(TooltipBehavior, HoverBehavior, Label):
    def on_hover(self, state: bool) -> None:
        with self.canvas.before:
            self.canvas.before.clear()
            this_color: list[float] = [0.2, 0.4, 0.4, 1.0] if state else [0.2, 0.2, 0.2, 1.0]
            Color(*this_color)
            Rectangle(pos=self.pos, size=self.size)

    def on_tooltip(self, show: bool):
        # print(f"[ on_tooltip | {show}]", self.tooltip_text)
        pass


class ExampleLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", spacing=16, padding=16, **kwargs)

        # Default tooltip
        self.add_widget(
            MyButton(
                text="Default tooltip",
                tooltip_text="This is a simple tooltip",
            )
        )

        # Tooltip on the left
        self.add_widget(
            MyButton(
                text="Cursor tooltip",
                tooltip_text="Tooltip shown on the left side",
                tooltip_side="cursor",
                pos_hint={"x":0.33, "y":1.0},
                size_hint_x=0.33,
                tooltip_interactive=True,
                tooltip_offset="16sp",
            )
        )

        # Custom tooltip widget
        custom = Tooltip(
            background_color=[0.2, 0.2, 0.2, 1.0],
            foreground_color=[0.9, 0.9, 0.9, 1.0],
            font_size="32sp",
            size_max=(100, 100)
        )

        self.add_widget(
            MyButton(
                text="Custom tooltip",
                tooltip_text="This tooltip uses a custom widget",
                tooltip_template=custom,
                tooltip_interactive=True,
                tooltip_offset="16sp",
            )
        )


if __name__ == "__main__":
    from kivydk.app import App

    class Example(App):
        def build(self):
            return ExampleLayout()

    Example().run()
    