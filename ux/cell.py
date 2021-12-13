import string
import copy

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.textinput import TextInput
from pandas import DataFrame

from ux.btn import Btn
from ux.hoverBehaviour import HoverBehavior
from ux.textInput import TxtInput
from design import Design


Builder.load_file('ui/cell.kv')


class Cell(Btn):
    cell_type = StringProperty('inputs')
    text = StringProperty('0')
    theme = Design().default_theme
    bent_title = StringProperty('def.')
    bent_index = ObjectProperty(-1)
    bent_title_cell = ObjectProperty(None)

    def none_method(self, *args):
        print('[BeastWood-WARNING]: none_method has been called.')
    save_value = ObjectProperty(none_method)

    def on_release(self):
        cell_type = self.cell_type
        values = ['0', '1', 'X', '@']
        if self.text in values:
            index = 3
            if cell_type == 'inputs':
                index = (values.index(self.text) + 1) % 2
            elif cell_type == 'outputs':
                index = (values.index(self.text) + 1) % 3
            self.text = values[index]

        try:
            self.save_value(self.bent_title_cell.text,
                            self.bent_index, self.text)
        except AttributeError:
            self.save_value(self.bent_title, self.bent_index, self.text)


class EmptyCell(Cell):
    pass


class SwitchCellBtn(Cell):
    bent_title_cell = ObjectProperty(None)

    def on_release(self):
        """ Rewrite function that button will switch 
        column type from inputs to putputs and vice versa.

        """
        self.bent_title_cell.switch()
        Cell.on_release(self)


class TitleCell(TxtInput, HoverBehavior):
    cell_type = StringProperty('Input')
    reserved_title = StringProperty('def.')
    del_column = ObjectProperty(None)
    valid_to_apply = ObjectProperty(None)
    get_titles = ObjectProperty(None)
    rename_title = ObjectProperty(None)
    erase_signal = ObjectProperty(None)
    index = ObjectProperty(None)
    save_switch = ObjectProperty(None)

    def switch(self):
        if self.cell_type == 'Input':
            self.cell_type = 'Output'
            self.canvas.ask_update()
        else:
            self.cell_type = 'Input'
            self.canvas.ask_update()

        self.save_switch(self.text, self.cell_type)

    PROPER_VALUES = {
        'Input': ['0', '1'],
        'Output': ['0', '1']
    }

    def insert_text(self, substring, from_undo=False):
        length = len(self.text) + 1

        abc = string.ascii_letters
        dig = string.digits
        vls = self.PROPER_VALUES[self.cell_type]
        data = [[abc, abc, abc, '=', vls, []],
                [abc, abc, dig, '=', vls, []],
                [abc, abc, '=', vls, [], []],
                [abc, dig, abc, '=', vls, []],
                [abc, dig, dig, '=', vls, []],
                [abc, dig, '=', vls, [], []],
                [abc, '=', vls, [], [], []]]

        text = self.text + substring
        valid = False
        for column in data:
            proper = True
            for index in range(length):
                if text[index] not in column[index]:
                    proper = False
                    break
            if proper:
                valid = True
        s = ''
        if valid:
            if length == 1:
                s = substring.upper()
            else:
                s = substring

        self.cursor = (length, 0)
        return super(TitleCell, self).insert_text(s, from_undo=from_undo)

    def on_focus(self, instance, is_focus):
        text = copy.copy(self.text)
        text_size = len(text)

        if not is_focus:
            if text_size == 0:
                self.del_column(self.index)
                return
            elif '=' in text:
                index = text.index('=')
                if index + 2 == text_size:
                    value = text[index+1]
                    if value == '*':
                        value = 'X'
                    self.write_column(self, value)
                self.text = text[:index]

            if self.is_equal_signal(text):
                if self.reserved_title == 'def.':
                    self.del_column(self.index)
                else:
                    self.text = self.reserved_title
            else:
                self.rename_title(self.reserved_title, text)

            # self.valid_to_apply()
        else:
            if 0 < text_size < 4:
                self.reserved_title = text

    def is_equal_signal(self, text):
        return text in self.get_titles()


class TitleInputCell(TitleCell):
    pass


class TitleOutputCell(TitleCell):
    pass


class IndexCell(Cell):
    title = StringProperty('1')
    del_row = ObjectProperty(None)

    def on_press(self):
        """
        Rewrite the on_press function, that by pushing an
        index cell delete the corresponding row. 

        """
        self.del_row(int(self.title)-1)
        Cell.on_press(self)


class AddCell(Cell):
    pass
