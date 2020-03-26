from kivy.properties        import StringProperty, ObjectProperty
from kivy.lang              import Builder
from kivy.clock             import Clock
from kivy.uix.textinput     import TextInput

from control.hoverBehaviour import HoverBehavior, HoverButton
from control.textInput      import TxtInput

from pandas                 import DataFrame
from design                 import Design
import string 

Builder.load_file('view/cell.kv')

class Cell(HoverButton):
    cell_type = StringProperty('inputs')
    text      = StringProperty('0')
    theme     = Design().default_theme

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

class TitleCell(TxtInput, HoverBehavior):
    cell_type     = StringProperty('inputs')
    remove_column = ObjectProperty(None)
    index         = ObjectProperty(None)
    PROPER_VALUES = {'inputs': ['0', '1'],
                    'outputs': ['0', '1', '*']}
    
    def insert_text(self, substring, from_undo=False):
        length = len(self.text) + 1
        
        abc = string.ascii_letters
        dig = string.digits
        vls = self.PROPER_VALUES[self.cell_type]
        data = [[abc, abc, abc, '=', vls, [ ]],
                [abc, abc, dig, '=', vls, [ ]],
                [abc, abc, '=', vls, [ ], [ ]],
                [abc, dig, abc, '=', vls, [ ]],
                [abc, dig, dig, '=', vls, [ ]],
                [abc, dig, '=', vls, [ ], [ ]],
                [abc, '=', vls, [ ], [ ], [ ]]]
        
        text = self.text + substring
        valid = False
        for column in data:
            proper = True
            for index in range(length):
                if text[index] not in column[index]:
                    proper = False
                    break
            if proper: valid = True
        s = ''
        if valid: 
            if length == 1:
                s = substring.upper()
            else:
                s = substring

        self.cursor = (length, 0)
        return super(TitleCell, self).insert_text(s, from_undo=from_undo)

    def on_focus(self, *args):
        if not self.focus:
            text_size = len(self.text)
            if text_size == 0:
                self.remove_column(self)
            elif text_size > 2:
                self.text = self.text[:3]
    
class IndexCell(Cell):
    index = ObjectProperty(None)
    title = StringProperty(str(index))

    def __init__(self, **kwargs):
        super(IndexCell, self).__init__(**kwargs)
        
        self.title = str(self.index + 1)

class AddCell(Cell):
    pass