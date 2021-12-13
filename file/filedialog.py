from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.lang import Builder


def show_save_filedialog(*args):
    content = SaveFileDialog()
    popup = Popup(
        title="Save a file",
        content=content,
        size_hint=(1, 1),
    )
    popup.open()


class SaveFileDialog(BoxLayout):
    Builder.load_file('file/filedialog.kv')
    save = ObjectProperty()
    cancel = ObjectProperty()

    def save(self, path, filename):
        pass

    def cancel(self):
        self._popup.dismiss()
