"""
:Author:    Oleksii Dovhaniuk
:E-mail:    dovhaniuk.oleksii@chnu.edu.ua
:Date:      24.03.2021

"""
import numpy as np
import matplotlib.pyplot as plt
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

import kivy
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, SlideTransition, Screen
from kivy.uix.scrollview import ScrollView

from ux.lbl import Lbl
from ux.layout import ViewLayout, PropertyLayout, SubtitleLayout, Line1Dark, LightDefault
from ux.btn import DropDownBtn, PropertyDropDown, Btn
from ux.txtinput import PropertyTxtInput
from ux.tbl import TruthTbl
from component.gate import Gate
from component.node import Node

kivy   .require('1.10.1')
Builder.load_file('ui/view.kv')


class View(BoxLayout):
    views = []
    screens = {}

    def __init__(self, views=[]):
        BoxLayout.__init__(self)
        self.screen_manager = self.ids.screen_manager
        self.screen_manager.transition = SlideTransition(
            direction='up',
            duration=.55)
        for view in views:
            self.add_view(view)

    def add_view(self, view):
        self.views.append(view)
        scroll_view = ScrollView(
            do_scroll_x=True,
            effect_cls='ScrollEffect',
            pos_hint={'center_x': .5, 'center_y': .5},
            bar_width=15,
            scroll_type=['bars']
        )
        scroll_view.add_widget(view)
        screen = Screen(name=view.name)
        screen.add_widget(scroll_view)
        self.screen_manager.add_widget(screen)
        self.screens[view.name] = [view]


class ReportView(ViewLayout):
    ROW_HEIGHT = 32
    _results = {'Device': Lbl(text='NaN'),
                'Genotype': BoxLayout(),
                'Scheme': BoxLayout(),
                'Fitness function': Lbl(text='NaN'),
                'Hamming distance': Lbl(text='NaN'),
                'Gate number': Lbl(text='NaN'),
                'Quantum cost': Lbl(text='NaN'),
                'Delay': Lbl(text='NaN'),
                'Ancillary bits': Lbl(text='NaN'),
                'Disparity': Lbl(text='NaN'),
                'Number of stagnations': Lbl(text='NaN'),
                'Process flow': BoxLayout(
                    size_hint_y=None,
                    height=400*6),
                'Total process time': Lbl(text='NaN'),
                'Synthesis time': Lbl(text='NaN'),
                'Optimization time': Lbl(text='NaN'),
                'Pause time': Lbl(text='NaN'),
                'Date/time start': Lbl(text='NaN'),
                'Date/time end': Lbl(text='NaN'),
                }

    def __init__(self):
        ViewLayout.__init__(self, 'Report')
        for field in self._results:
            self.add_widget(PropertyLayout(
                field,
                self._results[field],
                valign='top',
                halign='left',
                lbl_size_hint=(None, 1),
                lbl_size=(300, 24)))

    def raise_results(self, results):
        """ Raise reuslts in Report View.

        :arg: results `results` (nested list).
        """
        for field in results:
            if field == 'Genotype':
                cont = self._results[field]
                height = 0
                for allele in (al for al in results[field] if al[0].tag != 'None'):
                    height = max(len(allele[1])*self.ROW_HEIGHT, height)
                    al_view = BoxLayout(
                        orientation='vertical',
                        size_hint_y=None,
                        height=height)
                    al_view.add_widget(Lbl(text=allele[0].tag))
                    for gate in allele[1]:
                        al_view.add_widget(Lbl(text=str(gate)))
                    cont.add_widget(al_view)
                    cont.bind(minimum_height=cont.setter('height'))
            elif field == 'Process flow':
                data_values, stags, theta_p = results[field]
                generations = np.arange(len(data_values['Delay']))
                plt_no = len(data_values)
                figure, axis = plt.subplots(plt_no)

                for i, key in enumerate(data_values):
                    if key == 'Fitness function':
                        axis[i].plot(
                            generations[:theta_p],
                            np.array(data_values[key][0][:theta_p]),
                            label='Maxs syns.',
                            color='blue')
                        axis[i].plot(
                            generations[theta_p-1:],
                            np.array(data_values[key][0][theta_p-1:]),
                            label='Maxs opt.',
                            color='#00BFF2')
                        axis[i].plot(
                            generations,
                            np.array(data_values[key][1]),
                            label='Avgs',
                            color='#FC8F12')
                        axis[i].plot(
                            generations,
                            np.array(data_values[key][2]),
                            label='Mins',
                            color='#00944E')
                        axis[i].plot(
                            np.array(stags[0]),
                            np.array(stags[1][key]),
                            'o',
                            color='blue',
                            markersize=3,
                            label='Stagnations')
                        axis[i].legend(
                            bbox_to_anchor=(0, 1.02, .8, 0),
                            loc='lower left',
                            ncol=4,
                            mode='expend',
                            borderaxespad=0.)
                        axis[i].grid(True)
                    else:
                        axis[i].plot(
                            generations[:theta_p],
                            np.array(data_values[key][:theta_p]),
                            label=f'Best chromosom {key} syns.',
                            color='blue')
                        axis[i].plot(
                            generations[theta_p-1:],
                            np.array(data_values[key][theta_p-1:]),
                            label=f'Best chromosom {key} opt.',
                            color='#00BFF2')
                        axis[i].plot(
                            np.array(stags[0]),
                            np.array(stags[1][key]),
                            'o',
                            color='blue',
                            markersize=3,
                            label='Stagnations')
                        axis[i].legend(
                            bbox_to_anchor=(0, 1.02, .8, 0),
                            loc='lower left',
                            ncol=1,
                            mode='expend',
                            borderaxespad=0.)
                        axis[i].grid(True)

                for ax, lbl in zip(axis.flat, data_values):
                    ax.set(xlabel='Generation', ylabel=lbl)

                plt.subplots_adjust(
                    left=0.15,
                    bottom=0.1,
                    right=.95,
                    top=.9,
                    wspace=0.,
                    hspace=0.7,)
                self._results[field].add_widget(FigureCanvasKivyAgg(plt.gcf()))
            else:
                self._results[field].text = str(results[field])

    def draw_scheme(self, scheme):
        self._results['sheme'].add_widget(scheme)


class HistoryView(ViewLayout):
    TITLES = ('Date/time', 'Device', 'Configs', 'Status')
    VALUES = (
        ('2021-05-16/15:50:06', 'Add1', 'GA01', 'Done'),
        ('2021-05-18/06:20:03', 'RRG1', 'GA02', 'In proc.'),
        ('2021-05-29/07:01:09', 'RRG2', 'GA03', 'Done'),
        ('2021-05-29/08:07:12', 'Add1', 'GA01', 'In proc.'),
    )

    def __init__(self):
        ViewLayout.__init__(self, 'History')
        layout = self.lt = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_y=None)

        title_row = BoxLayout(size_hint_y=None, height=32)
        for title in self.TITLES:
            title_row.add_widget(Lbl(
                text=title,
                font_size=16,
                halign='center'))
        layout.add_widget(title_row)
        for row in self.VALUES:
            self._add_row(row)

        layout.add_widget(BoxLayout(size_hint_y=None, height=24))
        btn_lt = BoxLayout(spacing=20)
        btn_lt.add_widget(BoxLayout())
        btn_lt.add_widget(Btn(text='Load', disabled=True))
        btn_lt.add_widget(Btn(text='Export', disabled=True))
        layout.add_widget(btn_lt)
        self.add_widget(layout)

        self.lt.bind(minimum_height=layout.setter('height'))

    def _add_row(self, row):
        row_lt = BoxLayout(
            size_hint_y=None,
            height=24,
            spacing=5)
        for value in row:
            row_lt.add_widget(Lbl(
                text=str(value),
                font_size=14,
                halign='center'))
        self.lt.add_widget(Line1Dark())
        self.lt.add_widget(row_lt)


class EntityView(ViewLayout):
    NODES = (
        'Circle Black',
        'Circle Crossed',
        'Circle White',
        'Cross',
        'Cube Black',
        'Cube White',
        'Dot Black Ruby',
        'Dot Black Square',
        'Dot Black Star',
        'Dot Black Triangle Down',
        'Dot Black Triangle Up',
        'Dot Black',
        'Dot White Ruby',
        'Dot White Square',
        'Dot White Triangle Down',
        'Dot White Triangle Up',
        'Dot White',
        'Ruby Black',
        'Ruby Crossed',
        'Ruby Pie',
        'Ruby White',
        'Square Black',
        'Square Crossed',
        'Square Pie',
        'Square White')
    SIGNALS = (('A', 'S'), ('B', 'G1'), ('Cin', 'Cout'),
               ('A1', 'G2'), ('A2', 'G3'), ('A3', 'G4'))
    _entity = {
        'device': '2-bit Reversible Multiplier',
        # 'inputs': np.array([
        #     [0, 0, 0, 0],
        #     [0, 0, 0, 1],
        #     [0, 0, 1, 0],
        #     [0, 0, 1, 1],

        #     [0, 1, 0, 0],
        #     [0, 1, 0, 1],
        #     [0, 1, 1, 0],
        #     [0, 1, 1, 1],

        #     [1, 0, 0, 0],
        #     [1, 0, 0, 1],
        #     [1, 0, 1, 0],
        #     [1, 0, 1, 1],

        #     [1, 1, 0, 0],
        #     [1, 1, 0, 1],
        #     [1, 1, 1, 0],
        #     [1, 1, 1, 1],
        # ], copy=False),
        # 'outputs': np.array([
        #     [0, 0, 0, 0],
        #     [0, 0, 0, 0],
        #     [0, 0, 0, 0],
        #     [0, 0, 0, 0],

        #     [0, 0, 0, 0],
        #     [0, 0, 0, 1],
        #     [0, 0, 1, 0],
        #     [0, 0, 1, 1],

        #     [0, 0, 0, 0],
        #     [0, 0, 1, 0],
        #     [0, 1, 0, 0],
        #     [0, 1, 1, 0],

        #     [0, 0, 0, 0],
        #     [0, 0, 1, 1],
        #     [0, 1, 1, 0],
        #     [1, 0, 0, 1],
        # ], copy=False),
        # 'inputs': np.array([
        #     [0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 1],
        #     [0, 0, 0, 0, 1, 0],
        #     [0, 0, 0, 0, 1, 1],
        #     [0, 0, 0, 1, 0, 0],
        #     [0, 0, 0, 1, 0, 1],
        #     [0, 0, 0, 1, 1, 0],
        #     [0, 0, 0, 1, 1, 1],
        #     [0, 0, 1, 0, 0, 0],
        #     [0, 0, 1, 0, 0, 1],
        #     [0, 0, 1, 0, 1, 0],
        #     [0, 0, 1, 0, 1, 1],
        #     [0, 0, 1, 1, 0, 0],
        #     [0, 0, 1, 1, 0, 1],
        #     [0, 0, 1, 1, 1, 0],
        #     [0, 0, 1, 1, 1, 1],
        #     [0, 1, 0, 0, 0, 0],
        #     [0, 1, 0, 0, 0, 1],
        #     [0, 1, 0, 0, 1, 0],
        #     [0, 1, 0, 0, 1, 1],
        #     [0, 1, 0, 1, 0, 0],
        #     [0, 1, 0, 1, 0, 1],
        #     [0, 1, 0, 1, 1, 0],
        #     [0, 1, 0, 1, 1, 1],
        #     [0, 1, 1, 0, 0, 0],
        #     [0, 1, 1, 0, 0, 1],
        #     [0, 1, 1, 0, 1, 0],
        #     [0, 1, 1, 0, 1, 1],
        #     [0, 1, 1, 1, 0, 0],
        #     [0, 1, 1, 1, 0, 1],
        #     [0, 1, 1, 1, 1, 0],
        #     [0, 1, 1, 1, 1, 1],
        #     [1, 0, 0, 0, 0, 0],
        #     [1, 0, 0, 0, 0, 1],
        #     [1, 0, 0, 0, 1, 0],
        #     [1, 0, 0, 0, 1, 1],
        #     [1, 0, 0, 1, 0, 0],
        #     [1, 0, 0, 1, 0, 1],
        #     [1, 0, 0, 1, 1, 0],
        #     [1, 0, 0, 1, 1, 1],
        #     [1, 0, 1, 0, 0, 0],
        #     [1, 0, 1, 0, 0, 1],
        #     [1, 0, 1, 0, 1, 0],
        #     [1, 0, 1, 0, 1, 1],
        #     [1, 0, 1, 1, 0, 0],
        #     [1, 0, 1, 1, 0, 1],
        #     [1, 0, 1, 1, 1, 0],
        #     [1, 0, 1, 1, 1, 1],
        #     [1, 1, 0, 0, 0, 0],
        #     [1, 1, 0, 0, 0, 1],
        #     [1, 1, 0, 0, 1, 0],
        #     [1, 1, 0, 0, 1, 1],
        #     [1, 1, 0, 1, 0, 0],
        #     [1, 1, 0, 1, 0, 1],
        #     [1, 1, 0, 1, 1, 0],
        #     [1, 1, 0, 1, 1, 1],
        #     [1, 1, 1, 0, 0, 0],
        #     [1, 1, 1, 0, 0, 1],
        #     [1, 1, 1, 0, 1, 0],
        #     [1, 1, 1, 0, 1, 1],
        #     [1, 1, 1, 1, 0, 0],
        #     [1, 1, 1, 1, 0, 1],
        #     [1, 1, 1, 1, 1, 0],
        #     [1, 1, 1, 1, 1, 1],
        # ], copy=False),
        # 'outputs': np.array([
        #     [0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 1, 0],
        #     [0, 0, 0, 0, 0, 1],
        #     [0, 0, 0, 0, 1, 1],
        #     [0, 0, 0, 1, 0, 0],
        #     [0, 0, 0, 1, 1, 0],
        #     [0, 0, 0, 1, 0, 1],
        #     [0, 0, 0, 1, 1, 1],
        #     [0, 0, 1, 0, 0, 0],
        #     [0, 0, 1, 0, 1, 0],
        #     [0, 0, 1, 0, 0, 1],
        #     [0, 0, 1, 0, 1, 1],
        #     [0, 0, 1, 1, 0, 0],
        #     [0, 0, 1, 1, 1, 0],
        #     [0, 0, 1, 1, 0, 1],
        #     [0, 0, 1, 1, 1, 1],
        #     [0, 1, 0, 0, 0, 0],
        #     [0, 1, 0, 0, 0, 1],
        #     [0, 1, 0, 0, 1, 0],
        #     [0, 1, 0, 0, 1, 1],
        #     [0, 1, 0, 1, 0, 0],
        #     [0, 1, 0, 1, 1, 0],
        #     [0, 1, 0, 1, 0, 1],
        #     [0, 1, 0, 1, 1, 1],
        #     [0, 1, 1, 0, 0, 0],
        #     [0, 1, 1, 0, 0, 1],
        #     [0, 1, 1, 0, 1, 0],
        #     [0, 1, 1, 0, 1, 1],
        #     [0, 1, 1, 1, 0, 0],
        #     [0, 1, 1, 1, 1, 0],
        #     [0, 1, 1, 1, 0, 1],
        #     [0, 1, 1, 1, 1, 1],
        #     [1, 0, 0, 0, 0, 0],
        #     [1, 0, 0, 0, 0, 1],
        #     [1, 0, 0, 0, 1, 0],
        #     [1, 0, 0, 0, 1, 1],
        #     [1, 0, 0, 1, 0, 0],
        #     [1, 0, 0, 1, 0, 1],
        #     [1, 0, 0, 1, 1, 0],
        #     [1, 0, 0, 1, 1, 1],
        #     [1, 0, 1, 0, 0, 0],
        #     [1, 0, 1, 0, 1, 0],
        #     [1, 0, 1, 0, 0, 1],
        #     [1, 0, 1, 0, 1, 1],
        #     [1, 0, 1, 1, 0, 0],
        #     [1, 0, 1, 1, 1, 0],
        #     [1, 0, 1, 1, 0, 1],
        #     [1, 0, 1, 1, 1, 1],
        #     [1, 1, 0, 0, 0, 0],
        #     [1, 1, 0, 0, 0, 1],
        #     [1, 1, 0, 0, 1, 0],
        #     [1, 1, 0, 0, 1, 1],
        #     [1, 1, 0, 1, 0, 0],
        #     [1, 1, 0, 1, 0, 1],
        #     [1, 1, 0, 1, 1, 0],
        #     [1, 1, 0, 1, 1, 1],
        #     [1, 1, 1, 0, 0, 0],
        #     [1, 1, 1, 0, 0, 1],
        #     [1, 1, 1, 0, 1, 0],
        #     [1, 1, 1, 0, 1, 1],
        #     [1, 1, 1, 1, 0, 0],
        #     [1, 1, 1, 1, 1, 0],
        #     [1, 1, 1, 1, 0, 1],
        #     [1, 1, 1, 1, 1, 1],
        # ], copy=False),
        'inputs': np.array([
            [0, 0, 0],
            [0, 0, 1],
            [0, 1, 0],
            [0, 1, 1],
            [1, 0, 0],
            [1, 0, 1],
            [1, 1, 0],
            [1, 1, 1]
        ], copy=False),
        'outputs': np.array([
            [0, 0],
            [1, 0],
            [1, 0],
            [0, 1],
            [1, 0],
            [0, 1],
            [0, 1],
            [1, 1]
        ], copy=False),
        # 'inputs': np.array([
        #     [1, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 1, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 1, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 1, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 1, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 1, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 1, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 1]
        # ], copy=False),
        # 'outputs': np.array([
        #     [0, 0, 0],
        #     [0, 0, 1],
        #     [0, 1, 0],
        #     [0, 1, 1],
        #     [1, 0, 0],
        #     [1, 0, 1],
        #     [1, 1, 0],
        #     [1, 1, 1]
        # ], copy=False),
        'signals': SIGNALS
    }

    _nodes = [Btn(
        text=f' {node} ',
        size=(320, 18),
        halign='left',
        font_size=12) for node in NODES]

    def __init__(self, **kwargs):
        ViewLayout.__init__(self, 'Entity', **kwargs)
        self.spacing = 10

        # Device name layout.
        lt = BoxLayout(
            size_hint_y=None,
            spacing=20)
        lt.add_widget(Lbl(
            text='Name',
            size_hint=(None, None),
            size=(50, 32),
            font_size=16))
        self.device_name = PropertyTxtInput(
            hint_text='Enter Device Name',
            size_hint_y=None,
            height=32)
        lt.add_widget(self.device_name)
        self.browse_btn = Btn(
            text='Browse',
            size_hint=(None, None),
            size=(180, 32),
            halign='center',
            disabled=True)
        lt.add_widget(self.browse_btn)
        self.add_widget(lt)
        lt.bind(minimum_height=lt.setter('height'))
        self.add_widget(Line1Dark())

        # Ports layout
        lt_head = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=5,
            height=230)
        lt_head.add_widget(Lbl(text='Ports'))
        lt = BoxLayout(spacing=20)
        lt.add_widget(BoxLayout(size_hint_x=None, width=10))
        self.entity = Btn(
            text='Entity',
            size_hint=(None, 1),
            size=(180, 180))
        lt.add_widget(self.entity)
        lt_right = BoxLayout(
            orientation='vertical',
            spacing=10)
        self.port_name = PropertyTxtInput()
        lt_right.add_widget(PropertyLayout(
            label='Port Name',
            content=self.port_name,
            halign='left',
            lbl_size_hint=(None, None),
            lbl_size=(120, 32)))
        self.array_ind = PropertyTxtInput()
        lt_right.add_widget(PropertyLayout(
            label='Array Indicies',
            content=self.array_ind,
            halign='left',
            lbl_size_hint=(None, None),
            lbl_size=(120, 32)))
        self.gate_view = DropDownBtn(
            self._nodes,
            text=self.NODES[0],
            size_hint=(1, 1))
        lt_right.add_widget(PropertyLayout(
            label='Gate View',
            content=self.gate_view,
            halign='left',
            lbl_size_hint=(None, None),
            lbl_size=(120, 32)))
        self.gate_view = PropertyTxtInput(
            disabled=True,
            size_hint=(1, 1))
        lt_right.add_widget(PropertyLayout(
            label='Gate Mark',
            content=self.gate_view,
            halign='left',
            lbl_size_hint=(None, None),
            lbl_size=(120, 32)))
        lt_btns = BoxLayout(spacing=20)
        lt_btns.add_widget(BoxLayout())
        self.newport_btn = Btn(
            text='New Port',
            size_hint=(None, None),
            size=(180, 24))
        lt_btns.add_widget(self.newport_btn)
        self.delete_btn = Btn(
            text='Delete',
            size_hint=(None, None),
            size=(180, 24))
        lt_btns.add_widget(self.delete_btn)
        lt_right.add_widget(lt_btns)
        lt.add_widget(lt_right)
        lt_head.add_widget(lt)
        self.add_widget(lt_head)
        self.add_widget(Line1Dark())

        # Functioality layout
        lt_head = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=5,
            height=32)
        self.add_widget(lt_head)
        lt_head.add_widget(Lbl(text='Functionality'))

        lt = BoxLayout(size_hint_y=None)
        lt.add_widget(BoxLayout(size_hint_x=None, width=20))
        lt_body = BoxLayout(orientation='vertical',
                            spacing=10,
                            size_hint_y=None)
        self.enter_method = DropDownBtn(
            buttons=[Btn(text='Truth Table')],
            text='Truth Table',
            size_hint=(1, None),
            height=32)
        lt_body.add_widget(PropertyLayout(
            label='Method of Entering',
            content=self.enter_method,
            halign='left',
            lbl_size_hint=(None, 1)))
        self.truth_tbl = TruthTbl()
        for titles in self.SIGNALS:
            self.truth_tbl.add_signal(titles)
        lt_body.add_widget(self.truth_tbl)
        lt.add_widget(lt_body)
        lt_body.bind(minimum_height=lt_body.setter('height'))
        lt.bind(minimum_height=lt.setter('height'))
        self.add_widget(lt)

    def get_data(self):
        return self._entity


class BasisView(ViewLayout):
    TITLES = (
        'Name', 'Base', 'Delay',
        'Quantum Cost', 'Parity', 'Entity')
    VALUES = (
        ('CNOT2B', 2, 2.5, 2, 'No'),
        ('FRG3B', 2, 4.5, 5, 'Yes'),
        ('TFG3B', 2, 2.3, 5, 'No'),
    )
    SWAP_MAP = [
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1]]
    SWAP_NODES = {
        'Target1': Node('__cross'),
        'Target2': Node('__cross')
    }
    FG3B_MAP = [
        [0, 0, 0],
        [1, 0, 0],
        [0, 1, 0],
        [1, 0, 1],
        [0, 0, 1],
        [1, 1, 0],
        [0, 1, 1],
        [1, 1, 1]]
    FG3B_NODES = {
        'Control': Node('__circle_black'),
        'Target1': Node('__cross'),
        'Target2': Node('__cross')
    }
    FG4B_MAP = [
        [0, 0, 0, 0],
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [1, 1, 0, 0],
        [0, 0, 1, 0],
        [1, 0, 1, 0],
        [0, 1, 1, 0],
        [1, 1, 0, 1],
        [0, 0, 0, 1],
        [1, 0, 0, 1],
        [0, 1, 0, 1],
        [1, 1, 1, 0],
        [0, 0, 1, 1],
        [1, 0, 1, 1],
        [0, 1, 1, 1],
        [1, 1, 1, 1],
    ]
    FG4B_NODES = {
        'Control1': Node('__circle_black'),
        'Control2': Node('__circle_black'),
        'Target1': Node('__cross'),
        'Target2': Node('__cross')
    }
    _controls = {}
    _basis = {
        'Elements': [
            Gate(
                tag='SWAP',
                qcost=2,
                delay=2,
                nodes=SWAP_NODES,
                mapping=SWAP_MAP),
            Gate(
                tag='FG3b',
                qcost=5,
                delay=5,
                nodes=FG3B_NODES,
                mapping=FG3B_MAP),
            Gate(
                tag='FG4b',
                qcost=15,
                delay=15,
                nodes=FG4B_NODES,
                mapping=FG4B_MAP),
            Gate(
                tag='None',
                qcost=0,
                delay=0,
                nodes={'None': Node('__dot_white_triangle_down')},
                mapping=[[0], [1]]),
        ],
        'Min Quantum Cost': 2,
        'Min Delay': 2,
    }

    def __init__(self, **kwargs):
        ViewLayout.__init__(self, 'Basis', **kwargs)
        layout = self.lt = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_y=None)

        title_row = BoxLayout(size_hint_y=None, height=32)
        self.checkbox_all = CheckBox(
            active=True,
            size_hint=(None, None),
            size=(32, 32))
        self.checkbox_all.bind(active=self._activate_all)
        title_row.add_widget(self.checkbox_all)
        for title in self.TITLES:
            title_row.add_widget(Lbl(
                text=title,
                font_size=16,
                halign='center'))
        layout.add_widget(title_row)
        for row in self.VALUES:
            self._add_row(row)

        layout.add_widget(BoxLayout(size_hint_y=None, height=24))
        btn_lt = BoxLayout()
        btn_lt.add_widget(BoxLayout())
        self.add_btn = Btn(
            text='Add Component',
            size_hint=(None, None),
            size=(180, 24),
            font_size=14,
            disabled=True)
        btn_lt.add_widget(self.add_btn)
        layout.add_widget(btn_lt)
        self.add_widget(layout)

        self.lt.bind(minimum_height=layout.setter('height'))

    def _activate_all(self, checkbox, value):
        if value:
            for key in self._controls:
                self._controls[key][0].active = True
        else:
            if all([self._controls[key][0].active for key in self._controls]):
                for key in self._controls:
                    self._controls[key][0].active = False

    def _activate(self, checkbox, value):
        if not value:
            self.checkbox_all.active = False
        if all([self._controls[key][0].active for key in self._controls]):
            self.checkbox_all.active = True

    def _add_row(self, row):
        checkbox = CheckBox(
            active=True,
            size_hint=(None, None),
            size=(32, 24))
        checkbox.bind(active=self._activate)
        row_lt = BoxLayout(
            size_hint_y=None,
            height=24,
            spacing=5)
        row_lt.add_widget(checkbox)
        for value in row:
            row_lt.add_widget(Lbl(
                text=str(value),
                font_size=14,
                halign='center'))
        button = Btn(text='...', disabled=True)
        self._controls[row[0]] = (checkbox, button)
        row_lt.add_widget(button)
        self.lt.add_widget(Line1Dark())
        self.lt.add_widget(row_lt)

    def get_data(self):
        return self._basis
