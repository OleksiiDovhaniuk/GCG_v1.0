from kivy.properties import StringProperty, ObjectProperty
from kivy.lang import Builder
from kivy.uix.textinput import TextInput

from control.hoverBehaviour import HoverBehavior, HoverButton


Builder.load_file('view/cell.kv')

class Cell(HoverButton):
    cell_type = StringProperty('inputs')

    def __init__(self, **kwargs):
        super(Cell, self).__init__(**kwargs)
        self.on_release = self.change_value

    def change_value(self):
        cell_type = self.cell_type
        values = ['0', '1', 'X', '@']
        if self.text in values:
            index = 3
            if cell_type == 'inputs':
                index = (values.index(self.text) + 1) % 2
            elif cell_type == 'outputs':
                index = (values.index(self.text) + 1) % 3
            self.text = values[index]
    
class EmptyCell(Cell):  
    pass

class TitleCell(TextInput, HoverBehavior):
    pass

class IndexCell(Cell):
    index = ObjectProperty(None)

class AddCell(Cell):
    pass