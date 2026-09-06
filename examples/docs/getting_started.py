#// IMPORT
from kivy.app import App
from kivydk.examples.ButtonIcon import ButtonIcon


#// LOGIC
class TestApp(App):
    def build(self):
        self.count = 0
        self.button = ButtonIcon(text="Button", size_hint_y=None, height=50)
        self.button.bind(on_click=self._do_clicking)

        return self.button

    def _do_clicking(self, *args):
        self.count += 1
        print("Button clicked %.2d times" % self.count)


#// RUN FILE
if __name__ == "__main__":
    TestApp().run()
