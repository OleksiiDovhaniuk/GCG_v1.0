from kivy.lang import Builder
from kivy.uix.filechooser import FileChooserListLayout,\
    FileChooserIconLayout


Builder.load_file('ui/flChsr.kv')


class FlChsrListLayout(FileChooserListLayout):
    pass


class FlChsrIconLayout(FileChooserIconLayout):
    pass
