""" 
:Author:    Oleksii Dovhaniuk
:E-mail:    dovhaniuk.oleksii@chnu.edu.ua
:Date:      24.03.2021

"""
from threading import Thread

import kivy
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


from ux.btn import DropDownBtn, ToolBtn, Btn
from ux.process import run
<<<<<<< HEAD
from design import default_theme as theme
from file.filedialog import show_save_filedialog
from file.file import DataSaver
=======
>>>>>>> parent of 395bcd5 (Restart workflow)

kivy   .require('1.10.1')
Builder.load_file('ui/bar.kv')


class MenuBar(BoxLayout):
<<<<<<< HEAD
    FILE_MENU = (
        MenuListItem(label='Open...', shortcut='Ctrl+O'), 
        MenuSeparator(),
        MenuListItem(label='Save', shortcut='Ctrl+S',
                    #  on_release=data_saver.save,
                     ),
        MenuListItem(label='Save As...', shortcut='Ctrl+Shift+S',
                     on_release=show_save_filedialog),
        MenuSeparator(),
        MenuListItem(label='Export PDF'),
        MenuListItem(label='Export XLS'),
        MenuSeparator(),
        MenuListItem(label='Auto Save'),
        MenuListItem(label='Settings'),
        MenuSeparator(),
        MenuListItem(label='Exit', on_release=quit),
    )
    EDIT_MENU = (
        MenuListItem(label='Undo', shortcut='Ctrl+Z'),
        MenuListItem(label='Redo', shortcut='Ctrl+Shift+Z'),
        MenuSeparator(),
        MenuListItem(label='Cut', shortcut='Ctrl+X'),
        MenuListItem(label='Copy', shortcut='Ctrl+C'),
        MenuListItem(label='Paste', shortcut='Ctrl+V'),
    )
    HELP_MENU = (
        MenuListItem(label='Release Notes'),
        MenuSeparator(),
        MenuListItem(label='About'),
    )

    active_menu = None


class MenuBtn(Btn):
    content = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Clock.schedule_once(self.setup, -1)

    def setup(self, *args):
        self.menu = DropDownMenu(
            menu_btn=self,
            bar=self.parent,
            content=self.content,
        )

    def on_enter(self):
        active_menu = self.parent.active_menu
        menu = self.menu

        if active_menu != None and active_menu != menu:
            active_menu.dismiss()
            self.parent.active_menu = menu
            menu.open(self)

        return super().on_enter()

    def on_release(self):
        active_menu = self.parent.active_menu
        menu = self.menu
        menu.open(self)
        self.parent.active_menu = menu
        self.disabled = True

        return super().on_release()


class DropDownMenu(DropDown):
    menu_btn = ObjectProperty()
    bar = ObjectProperty()
    content = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Clock.schedule_once(self.setup, -1)

    def setup(self, *args):
        box = self.ids.box
        box.bind(minimum_height=box.setter('height'))

        if self.content:
            for item in self.content:
                box.add_widget(item)


class MinimizeBtn(Btn):
    pass


class MaximizeBtn(Btn):
    state = 'normal'

    # def toggle_fullscreen(self, *args):
    #     Window.toggle_fullscreen()
    # if Window.fullscreen:
    #     Window.fullscreen = False
    # else:
    #     Window.fullscreen = True

    # def on_release(self):
    #     Clock.schedule_once(self.toggle_fullscreen, -1)
    # if Window.fullscreen:
    #     Window.fullscreen = False
    # else:
    #     Window.fullscreen = True
    # sleep(1)

    # for _ in range(2):
    #     user32.keybd_event(0x12, 0, 0, 0)  # Alt
    #     sleep(1)
    #     user32.keybd_event(0x09, 0, 0, 0)  # Tab
    #     sleep(1)
    #     user32.keybd_event(0x09, 0, 2, 0)  # ~Tab
    #     sleep(.1)
    #     user32.keybd_event(0x12, 0, 2, 0)  # ~Alt

    # Window.window_state = 'maximized'

    # hWnd = user32.GetForegroundWindow()
    # user32.ShowWindow(hWnd, SW_MAXIMISE)
    # Window.window_state = 'maximized'
    # Window.fullscreen = True
    # Window.maximize()
    # Window.toggle_fullscreen()
    # if self.state == 'normal':
    #     with self.canvas:
    #         Rectangle(
    #             source=theme + 'MaximizeBtn',
    #             pos=self.pos,
    #             size=self.size
    #         )


class CloseBtn(Btn):
    pass


class ToolTBtn(ToggleButton, HoverBehavior):
    title = StringProperty('Tool')
    view = StringProperty(f'{theme}ToolBtn_')
=======
    def __init__(self, **kwargs):
        BoxLayout.__init__(self, **kwargs)

        file_menu = {
            'Open': Btn(text='Open'),
            'Save': Btn(text='Save'),
            'Export': Btn(text='Export'),
            'Exit': Btn(text='Exit'),
        }
        file_btn = DropDownBtn(
            buttons=[file_menu[key] for key in file_menu],
            text='File',
            disabled=True)
        self.add_widget(file_btn)

        edit_menu = {
            'Undo': Btn(text='Undo'),
            'Redo': Btn(text='Redo'),
            'Cut': Btn(text='Cut'),
            'Copy': Btn(text='Copy'),
            'Past': Btn(text='Past'),
            'Delete': Btn(text='Delete'),
            'Select All': Btn(text='Select All'),
            'Properties': Btn(text='Properties'),
        }
        edit_btn = DropDownBtn(
            buttons=[edit_menu[key] for key in edit_menu],
            text='Edit',
            disabled=True)
        self.add_widget(edit_btn)

        help_menu = {
            'User Guide': Btn(text='User Guide'),
            'Product Help': Btn(text='Product Help'),
            'Keyboard Map': Btn(text='Keyboard Map'),
            'About QubitLab': Btn(text='About QubitLab'),
        }
        help_btn = DropDownBtn(
            buttons=[help_menu[key] for key in help_menu],
            text='Help',
            disabled=True)
        self.add_widget(help_btn)
>>>>>>> parent of 395bcd5 (Restart workflow)


class ToolBar(BoxLayout):
    def __init__(self):
        BoxLayout.__init__(self)

        container = self.container = self.ids.container
        self.btns = [
            ToolBtn(text='Report', disabled=True),
            ToolBtn(text='History'),
            ToolBtn(text='Entity'),
            ToolBtn(text='Basis'),
            ToolBtn(text='Algorithm'),
        ]
        self.run_btn = ToolBtn(text='Run')
        self.run_btn.bind(on_press=self.button_press)

        for btn in self.btns:
            btn.bind(on_release=lambda button: self.change_tab(button))
            container.add_widget(btn)
        container.add_widget(BoxLayout())
        container.add_widget(self.run_btn)

    def button_press(self, button):
        # create the thread to invoke other_func with arguments (2, 5)
        t = Thread(target=run, args=[button])
        # set daemon to true so the thread dies when app is closed
        t.daemon = True
        # start the thread
        t.start()

    def change_tab(self, tool_btn):
        for btn in self.btns:
            btn.disabled = False
            self.screen_manager.current = tool_btn.text

        tool_btn.disabled = True

    def bind_screens(self, screen_manager):
        self.screen_manager = screen_manager


class InfoBar(BoxLayout):
    pass
