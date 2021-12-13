from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout

from ux.lbl import Lbl

from design import Design


Builder.load_file('ui/popup.kv')


class WhitePopup(Popup):
    theme = Design().default_theme


class ProgressPopup(WhitePopup):
    values = {}  # Dictionary for ProgressValue objects.

    def __init__(self, title='Initializing...', progress=0, values=None):
        """ ProgressPopup object inherited from WhitePopup object and has next arguments 
            and methods:

            :arg: `title` (str): Title of the pop-up window. By default is set to 'Initializing...'.

            :arg: `progress` (int): Value in range [0, 100]. Be default equals 0.

            :arg: `values` (dict): Python dictionary, where the keys are names of the
                progress properties and values are obviously thair values. If values
                are not defined, no vhanges of values occure.

            :meth: `update(title=None, values=None)`: Updates the progress bar.

        """
        WhitePopup.__init__(self, title=self.title)

        self.ids.progress_bar.value = int(progress)
        self.ids.progress.text = f'{str(int(progress))}%'

        for key in values:
            if key == 'Fitness function':
                value = ProgressValue(key, values[key], precision=4)
            else:
                value = ProgressValue(key, values[key])

            self.values[key] = value
            self.ids.container.add_widget(value)

    def update(self, title=None, progress=None, values=None, ):
        """ Updates the progress bar.

            :arg: `title` (str): The title of the pop-up window of the progress.
                If title is not set, no change occures.

            :arg: `progress` (int): Th eprogress value. If the progress is not 
                inputed, no changes to the progress bar occures.

            :arg: `value` (dict): Python dictionary, where the keys are names of the
                progress properties and values are obviously thair values. If values
                are not defined, no vhanges of values occure.

        """
        if title:
            self.title = title

        if progress:
            self.ids.progress_bar.value = int(progress)
            self.ids.progress.text = f'{str(int(progress))}%'

        if values:
            for key in values:
                self.values[key].update(values[key])


class ProgressValue(BoxLayout):
    def __init__(self, title, value, precision=0, units=''):
        """ Progress value object which contains of two horizontally placed
            labels inherited from BoxLayout kivy class.

            :arg: `title` (str): text of the first label.

            :arg: `value` (int or float): first part of the text of the second label.

            :arg: `precision` (int): if value is a float digit, 
                precision defines a number of digits after a comma.
                By default precision=0.

            :arg: `units` (str): second part of the text of the second label, 
                units of the inputed value. By default units=''

        """
        self.title = Lbl(text=f'{title}:')
        self.precision = precision
        self.units = units

        if precision == 0:
            rounded_value = int(value)
        else:
            rounded_value = round(value, precision)
        self.value = Lbl(text=f'{rounded_value}{units}', size_hint_x=.5)

        BoxLayout.__init__(self)

        self.add_widget(self.title)
        self.add_widget(self.value)

    def update(self, value):
        """ Updates a value in the value label.

            :arg: `value` (int, float): new value.

        """
        if self.precision == 0:
            rounded_value = int(value)
        else:
            rounded_value = round(value, self.precision)
        self.value.text = f'{rounded_value}{self.units}'
