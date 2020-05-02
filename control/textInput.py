from kivy.properties import StringProperty, ObjectProperty
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

from functools import partial
from design import Design


Builder.load_file('view/textInput.kv')

class TxtInput(TextInput):
    theme = Design().default_theme

class AlgorithmConfigsInput(TxtInput):
    valid_range = ObjectProperty([0, 9999])
    push_value = ObjectProperty(None)
    key = StringProperty('')

    def on_focus(self, *args):
        if not self.focus:
                text_size = len(self.text)
                if text_size > 0:
                    self.push_value(self)

class NameInput(TxtInput):
    def select_textinput(self):
        if self.focus:
            Clock.schedule_once(lambda dt: self.select_all())

class FileInput(TxtInput):
    path = StringProperty('\saves')

    # def __init__ (self, **kwargs):
    #     super(FileInput, self).__init__(**kwargs)
    #     self.path = f'{self.parent.root_path}'

    def show(self, selection, *args):
        path = selection
        name = path.split('\\')[-1]
        
        self.path = path[:-len(name)]
        self.text = name

    def on_focus(self, *args):
        text = self.text.replace('.txt', '')
        text_size = len(text)
        if not self.focus:
            if text_size == 0:
                self.text = 'default.txt'
        else:
            pass