from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.checkbox import CheckBox

from design import Design


Builder.load_file('view/radioButton.kv')

class RadioButton(CheckBox):
    C_DISABLED = (.8, .8, .8, 1)
    C_NORMAL = (0, 0, 0, 1)

    theme = Design().default_theme
    label = ObjectProperty(None)
    text_input = ObjectProperty(None)
    mates = []

    def on_press(self):
        self.set_status(True)

    def set_status(self, active):
        """ Args: active [bool]

        """
        if active:
            self.active = True
            self.label.color = self.C_NORMAL
            self.text_input.disabled = False

            for mate in self.mates:
                mate['Radio Button'].active = False
                mate['Label'].color = mate['Radio Button'].C_DISABLED
                mate['Text Input'].disabled = True

class RbtEndCondition(RadioButton):
    pass
