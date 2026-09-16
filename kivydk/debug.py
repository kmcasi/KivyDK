#// IMPORT
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button

from kivydk.uix.behavior.hover import HoverBehavior
from kivydk.uix.behavior.tooltip import TooltipBehavior
from kivydk.uix.widgets.tooltip import Tooltip


#// LOGIC
class CustomButton(HoverBehavior, TooltipBehavior, Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class TestTooltip(FloatLayout):
    """Each event updates the label text to reflect the current click state."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Local variables
        self.tooltip_w = None
        self.anchors = {
            "top-left":      (0.25, 0.75),
            "top-center":    (0.50, 0.75),
            "top-right":     (0.75, 0.75),
            "center-left":   (0.25, 0.50),
            "center":        (0.50, 0.50),
            "center-right":  (0.75, 0.50),
            "bottom-left":   (0.25, 0.25),
            "bottom-center": (0.50, 0.25),
            "bottom-right":  (0.75, 0.25),
        }

        # Create the buttons
        for name, (ax, ay) in self.anchors.items():
            btn = CustomButton(
                text=name,
                size_hint=(None, None),
                size=(120, 40),
                tooltip_widget=Tooltip,
                tooltip_text=f"Tooltip of the {name!r}.",
                pos_hint={"center_x": ax, "center_y": ay},
            )
            btn.bind(on_hover=lambda i,s:self._handle_tooltip(i,s))
            self.add_widget(btn)

    def _handle_tooltip(self, instance:CustomButton, show):
        if not self.tooltip_w:
            self.tooltip_w:Tooltip = instance.tooltip_widget()
        self.tooltip_w.update_text(instance.tooltip_text)
        self.tooltip_w.update_size()
        self.tooltip_w.update_position(
            instance.x + instance.width // 2 - self.tooltip_w.width // 2,
            instance.y + instance.height + 4
        )

        if show:
            if self.tooltip_w not in Window.children:
                self.tooltip_w.on_show()
                Window.add_widget(self.tooltip_w)
        else:
            if self.tooltip_w in Window.children:
                Window.remove_widget(self.tooltip_w)


#// RUN FILE
if __name__ == "__main__":
    from kivy.app import App
    from kivy.core.window import Window

    class Example(App):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            Window.size = 512, 512-32

        def build(self):
            return TestTooltip()

    Example().run()
