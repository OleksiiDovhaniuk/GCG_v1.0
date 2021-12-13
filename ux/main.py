""" It is the core of the user experiance of the project.

:Author:    Oleksii Dovhaniuk
:E-mail:    dovhaniuk.oleksii@chnu.edu.ua
:Date:      23.03.2021

"""

import kivy
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from file.file import DataSaver

from ux.bar import MenuBar, ToolBar, InfoBar
from ux.view import View, ReportView, HistoryView, EntityView, BasisView
from ux.algorithmView import AlgorithmView
from ux.process import set_views

kivy   .require('1.10.1')
Builder.load_file('ui/main.kv')


class Main(BoxLayout):

    def __init__(self, **kwargs):
        super(Main, self).__init__(**kwargs)

        menu_bar = MenuBar()
        tool_bar = ToolBar()
        views = {
            'Report': ReportView(),
            'History': HistoryView(),
            'Entity': EntityView(),
            'Basis': BasisView(),
            'Algorithm': AlgorithmView(),
        }
        view = View([views[key] for key in views])
        set_views(view.views)
        data_saver = DataSaver(views[key] for key in ('Algorithm', 'Basis', 'Entity', 'Report'))


        view.screen_manager.current = 'Report'
        info_bar = InfoBar()

        tool_bar.bind_screens(view.screen_manager)

        self.add_widget(menu_bar)
        self.add_widget(tool_bar)
        self.add_widget(view)
        self.add_widget(info_bar)
