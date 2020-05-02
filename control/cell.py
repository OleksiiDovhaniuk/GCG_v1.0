import string

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.textinput import TextInput
from pandas import DataFrame

from control.btn import Btn
from control.hoverBehaviour import HoverBehavior
from control.textInput import TxtInput
from design import Design


Builder.load_file('view/cell.kv')

class Cell(Btn):
    cell_type = StringProperty('inputs')
    text = StringProperty('0')
    theme = Design().default_theme

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
    cell_type = StringProperty('inputs')
    reserved_title = StringProperty('def.')
    remove_column = ObjectProperty(None)
    valid_to_apply = ObjectProperty(None)
    is_equal_signal = ObjectProperty(None)
    erase_signal = ObjectProperty(None)
    write_column = ObjectProperty(None)
    index = ObjectProperty(None)

    PROPER_VALUES = {
        'inputs': ['0', '1'],
        'outputs': ['0', '1', '*']
    }
    
    def __init__ (self, **kwargs):
        super(TitleCell, self).__init__(**kwargs)
        self.text = self.text.replace(' ', '')

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
        text = self.text
        text_size = len(text)

        if not self.focus:
            if text_size == 0 : 
                self.remove_column(self)
                return
            elif '=' in text: 
                index = text.index('=')
                if index + 2 == text_size:
                    value = text[index+1]
                    if value == '*': value = 'X'
                    self.write_column(self, value)
                self.text = text[:index]

            if self.is_equal_signal(text):
                if self.reserved_title == 'def.':
                    self.remove_column(self)
                else:
                    self.text = self.reserved_title
            else: 
                self.erase_signal(self.reserved_title)

            self.valid_to_apply()
        else:
            if 0 < text_size < 4:
                self.reserved_title = text

    
class IndexCell(Cell):
    index = ObjectProperty(None)
    title = StringProperty(str(index))

    def __init__(self, **kwargs):
        super(IndexCell, self).__init__(**kwargs)
        
        self.title = str(self.index + 1)

class AddCell(Cell):
    pass
