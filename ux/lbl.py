from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy import utils

Builder.load_file('ui/lbl.kv')


class Lbl(Label):
    pass


class InfoLbl(Lbl, Button):
    PADDING_Y = 20
    TIMER = 3
    _is_poped = False

    def __init__(self, root):
        Lbl.__init__(self)
        Button.__init__(self)
        self.pos_hint['center_x'] = .5
        self.root = root
        self.TEXT_WIDTH = (self.width * .9) // ((self.font_size * 2) // 3)

    def pop_up(self, info):
        if self._is_poped:
            Clock.unschedule(self.clock)
            self.dismiss_popup()

        self._is_poped = True
        self.root.add_widget(self)
        self.text = self.fit_text(info)
        self.clock = Clock.schedule_once(self.dismiss_popup, self.TIMER)

    def fit_text(self, text):
        split_text = text.split(' ')
        fit_text, line = '', ''
        lines_no = 1

        for word in split_text:
            if len(line + word) < self.TEXT_WIDTH:
                line += word + ' '
            else:
                fit_text += line + '\n'
                lines_no += 1
                line = word + ' '
        fit_text += line + '\n'

        self.height = (lines_no * self.font_size * 1.25) + self.PADDING_Y
        self.pos_hint['center_y'] = .5
        return fit_text

    def dismiss_popup(self, *args):
        self.root.remove_widget(self)
        self._is_poped = False


class InfoCoefLbl(Lbl):
    STATUS = {
        'Default': utils.get_color_from_hex('#A1A1A1'),
        'Help': utils.get_color_from_hex('#32A4CE'),
        'Error': utils.get_color_from_hex('#EC512F'),
    }
    status = StringProperty('Default')

    def change_status_to(self, status):
        """ Change status of the Label and all properties related to it.

        Args: status ("Default", "Help", "Error")

        """
        if status in self.STATUS:
            self.status = status
            self.color = self.STATUS[status]


class ResultsLbl(Lbl):
    pass


class TitleLbl(Lbl):
    title = StringProperty('Default')


class PropertyLbl(Lbl):
    title = StringProperty('default')


class SubtitleLbl(Lbl):
    subtitle = StringProperty('default')

    def __init__(self, subtitle, halign='left', **kwargs):
        self.subtitle = subtitle
        width = self.font_size*.6 * len(subtitle)
        Lbl.__init__(self, width=width, halign=halign, ** kwargs)
