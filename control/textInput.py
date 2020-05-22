from kivy.properties import StringProperty, ObjectProperty
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

from functools import partial
from design import Design

from os import path
from file_work import STORAGE_PATH

Builder.load_file('view/textInput.kv')

class TxtInput(TextInput):
    theme = Design().default_theme

class AlgorithmConfigsInput(TxtInput):
    """
    Args:
        valid_range <tuple of 2 elements [int, float]>;
        info_label [kivy ObjectProperty];
        key [kivy StringProperty];
        dtype [str] in ('int', 'float');

    """
    valid_range = ObjectProperty([0, 9999])
    push_value = ObjectProperty(None)
    info_label = ObjectProperty(None)
    related_max = ObjectProperty(None)
    related_min = ObjectProperty(None)
    key = StringProperty('')

    MAX_CHARACTERS = 8
    
    def insert_text(self, substring, from_undo=False):

        if not len(self.text) < self.MAX_CHARACTERS:
            substring = ''
        else:
            substring = self.is_proper_input(substring)

        return super().insert_text(substring, from_undo=from_undo)

    def is_proper_input(self, substring):
        """ Check if an inputed character together with a text in a
        text-input field forms an appropriate input value.

        Args: 
            substring [str], len(substring)<=1;

        Returns: 
            if the inputed character with a text in text-input field
            forms an appropriate input value returns `the character`,
            otherwise returns `empty string`.

        Examples of execution:
            >>> test_input_int = AlgorithmConfigsInput(\
                    input_filter='int',\
                    valid_range=(0, 25),\
                )
            # >>> test_input_int.cursor = (0, 0)
            >>> test_sequins = ['-', '.', '0', '-', '.', ',', '2', '5', '9', '2', '5', '0']
            >>> [test_input_int.is_proper_input(value) for value in test_sequins]
            >>> ['', '', '0', '', '', '', '2', '5', '', '', '', '']

            >>> test_input_float = AlgorithmConfigsInput(\
                    input_filter='float',\
                    valid_range=(0, 10),\
                )
            # >>> test_input_float.cursor = (0, 0)
            >>> test_sequins = ['-', '.', '0', '-', '.', ',', '2', '5', '9', '2', '5', '0']
            >>> [test_input_float.is_proper_input(value) for value in test_sequins]
            >>> ['', '.', '0', '', '', '', '2', '5', '9', '2', '5', '0']

        """
        pos = self.cursor[0]
        new_text = f'{self.text[:pos]}{substring}{self.text[pos:]}'
        
        if self.input_filter == 'int':
            try:
                digit = int(new_text)
            except ValueError:
                self.show_warning(dtype='int')
                return ''

        elif self.input_filter == 'float':
            try:
                digit = float(new_text)
            except ValueError:
                self.show_warning(dtype='float')
                return ''

        else:
            return ''

        if digit < self.get_extreme('min'):
            self.text = str(self.get_extreme('min'))
            self.show_warning(dmin=self.valid_range[0])
            return ''
            
        elif digit > self.get_extreme('max'):
            self.text = str(self.get_extreme('max'))
            self.show_warning(dmax=self.valid_range[1])
            return ''

        else:
            return substring

    def get_extreme(self, extreme):
        """ Connects self AlgorithmConfigsInput object to enother 
        with title of the value if value is str argument and return
        digit value of the bent AlgorithmConfigsInput, otherwise
        just return value as digit.

        Args: extreme [str] in ('min', 'max').

        Returns: [float, int].

        """

        if extreme == 'min':
            try:
                if self.input_filter == 'float':
                    return float(self.valid_range[0])
                elif self.input_filter == 'int':
                    return int(self.valid_range[0])
            except ValueError:
                pass

            return self.related_min.get_value()

        elif extreme == 'max':
            try:
                if self.input_filter == 'float':
                    return float(self.valid_range[1])
                elif self.input_filter == 'int':
                    return int(self.valid_range[1])
            except ValueError:
                pass

            return self.related_max.get_value()
    
    def get_value(self):
        """ Returns digit value of inputed text of None.

        Returns: [int, float, None].

        """
        if self.text:
            text = self.text
        else:
            text = self.hint_text

        if self.input_filter == 'int':
            return int(text)
        elif self.input_filter == 'float':
            return float(text)
        else:
            return None

    def show_warning(self, dmin=None, dmax=None, dtype=None):
        warning = f'[WARNING]: {self.key} should be '

        if dtype: warning += f'non-negative {dtype}-type.'
        elif dmin: warning += f'not less than {dmin}.'
        elif dmax: warning += f'not bigger than {dmax}.'
        else: warning = '[ERROR]: Unknown issue in the code!'

        self.info_label.pop_up(warning)

    def on_focus(self, *args):
        if not self.focus and self.text:
            self.is_proper_input('')

    
class AlgorithmCoefInput(AlgorithmConfigsInput):
    mates = []
    info_coef = ObjectProperty(None)

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        pos = self.cursor[0]
        try:
            if keycode[1] == "backspace":
                try:
                    dvalue = float(self.text[:pos-1] + self.text[pos:])
                except ValueError:
                    dvalue = float(self.hint_text)
                self.change_persents(dvalue)

            elif keycode[1] == "delete":
                try:
                    dvalue = float(self.text[:pos] + self.text[pos+1:])
                except ValueError:
                    dvalue = float(self.hint_text)
                self.change_persents(dvalue)

        except IndexError:
            pass

        TextInput.keyboard_on_key_down(self, window, keycode, text, modifiers)
    
    def insert_text(self, substring, from_undo=False):
        self.info_coef.change_status_to('Help')
        pos = self.cursor[0]

        if (
            (not substring.isdigit() and substring != '.') 
            or 
            not len(self.text) < self.MAX_CHARACTERS
        ):
            return super(AlgorithmCoefInput, self).insert_text('', from_undo=from_undo)
        
        else:
            sco0 = (not self.text) and (not substring) 
            sco1 = (not self.text) and (substring=='.') 
            sco2 = ('.' in self.text) and (not substring) 
            sco3 = ('.' in self.text) and (substring=='.') 
            
            if sco0 or sco1 or sco2 or sco3:
                if len(self.text) > 1:
                    dvalue = float(self.text)
                else:
                    dvalue = float(self.hint_text)
            else:
                dvalue = float(self.text[:pos] + substring + self.text[pos:])

            self.change_persents(dvalue)
            return super().insert_text(substring, from_undo=from_undo)

    def change_persents(self, value):
        values = []

        for txt_in in self.mates:
            if txt_in.text:
                values.append(float(txt_in.text))
            else:
                values.append(float(txt_in.hint_text))

        dsum = sum(values) + value
        if dsum:
            in_persent = value / dsum * 100
        else:
            in_persent = 0
        in_persent = round((in_persent - (in_persent % .05)), 1) 
        self.info_coef.text = f'{in_persent}%'

        for txt_in in self.mates:
            if txt_in.text:
                dvalue = (float(txt_in.text))
            else:
                dvalue = (float(txt_in.hint_text))

            if dsum:
                in_persent = dvalue / dsum * 100
            else:
                in_persent = 0
            in_persent = round((in_persent - (in_persent % .05)), 1) 
            txt_in.info_coef.text = f'{in_persent}%'

    def refresh_coef_info(self):
        self.change_persents(float(self.hint_text))

    def get_value(self):
        return float(self.info_coef.text[:-1]) / 100

class NameInput(TxtInput):
    def select_textinput(self):
        if self.focus:
            Clock.schedule_once(lambda dt: self.select_all())

class FileInput(TxtInput):
    def __init__ (self, **kwargs):
        super(FileInput, self).__init__(**kwargs)

        index = 0
        default_text = start_default_text = 'untitled'
        while path.isfile(f'{STORAGE_PATH}\{default_text}.json'):
            index += 1
            default_text = f'{start_default_text}{index}'
        self.text = f'{default_text}.json'

    def show(self, selection, *args):
        path = selection
        name = path.split('\\')[-1]
        self.path = path[:-len(name)]
        self.text = name

if __name__ == '__main__':
    import doctest
    doctest.testmod()