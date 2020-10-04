from kivy.lang import Builder
from kivy.uix.button import Button

from design import default_theme as atlas


Builder.load_file('view/widgets.kv')

class HistoryWidget(Button):
    def __init__(self, title):
        Button.__init__(self)
        if title == 'Switch':
            self.background_disabled_normal = f'{atlas}SwitchCellBtn_normal'
            self.text = ''
            self.size = (24, 16)
        elif title == 'Add':
            self.background_disabled_normal = f'{atlas}AddCell_normal'
            self.text = '+'
        else:
            self.background_disabled_normal = f'{atlas}Title{title[:-1]}Cell_normal'
            self.text = ''

