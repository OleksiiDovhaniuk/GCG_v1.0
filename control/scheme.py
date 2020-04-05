from kivy.app             import App
from kivy.graphics        import Color    ,\
                                 Ellipse  ,\
                                 Line     ,\
                                 Rectangle
from kivy.lang            import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview  import ScrollView

from control.lbl          import Lbl
# from lbl          import Lbl

from random               import choice


class Scheme(FloatLayout):
    SIGNALS_NUMBER = 6
    SIGNALS        = [['A', 'B', 'C',  'A1', 'A2', 'A3'],
                      ['P', 'Q', 'G1', 'G2', 'G3', 'G4']]
    COLOURS_NUMBER = 6
    GENOTYPE       = [[[2,2], [1,0], [2,0], [2,1], [1,2], [1,1]],
                      [[1,0], [1,1], [1,2], [0,0], [0,0], [0,0]],
                      [[1,0], [1,2], [2,0], [2,1], [2,2], [1,1]],
                      [[0,0], [1,0], [1,1], [0,0], [0,0], [1,2]],
                      [[0,0], [1,0], [1,1], [0,0], [0,0], [1,2]],
                      [[0,0], [1,2], [1,1], [1,0], [0,0], [0,0]],
                      [[1,0], [1,1], [1,2], [0,0], [0,0], [0,0]],
                      [[1,0], [1,2], [2,0], [2,1], [2,2], [1,1]],
                      [[0,0], [1,0], [1,1], [0,0], [0,0], [1,2]],
                      [[0,0], [1,0], [1,1], [0,0], [0,0], [1,2]],
                      [[0,0], [1,2], [1,1], [1,0], [0,0], [0,0]],
                      [[1,2], [0,0], [1,1], [0,0], [0,0], [1,0]]]
    GATE_WIDTH     = 30
    HEIGHT         = 600

    def __init__(self, height=HEIGHT, signals=SIGNALS, genotype=GENOTYPE, **kwargs):
        super(Scheme, self).__init__(**kwargs) 
        self.size_hint = (None, 1)
        self.draw(height=height, 
                  genotype=genotype,
                  number=len(signals[0]))
        self.sign(signals)

    def sign(self, signals):
        padding_x  = .5 * self.padding_x
        lbl_height = self.step_y
        font_size  = .8 * self.step_y
        padding_y  = self.padding_y - (lbl_height / 2)

        pos = [[padding_x, padding_y + lbl_height * index] \
            for index in range(len(signals[0]))]
        for index, in_signal in enumerate(reversed(signals[0])):
            self.add_widget(Lbl(text       =in_signal,
                                font_size  =font_size,
                                pos        =pos[index],
                                size_hint_y=None,
                                height     =lbl_height))

        pos = [[self.width - coord[0], coord[1]] \
            for coord in pos]
        for index, out_signal in enumerate(reversed(signals[1])):
            self.add_widget(Lbl(text       =out_signal,
                                font_size  =font_size,
                                pos        =pos[index],
                                size_hint_y=None,
                                height     =lbl_height))
    
    def draw(self, number, genotype, height):
        for gene in genotype:
            NaN_number = gene.count([0, 0])
            if NaN_number == len(gene):
                genotype.remove(gene)

        n_steps_y      = number  
        self.padding_y = padding_y = .1 * height
        self.step_y    = step_y    = \
            (height - 2 * padding_y) / (n_steps_y - 1)
        
        self.padding_x = padding_x = 2.5 * step_y
        n_steps_x      = len(genotype) # n - from number
        self.width     = width     = ((height - 2 * padding_y)
            * (n_steps_x + n_steps_x/number)) + 2 * padding_x
        step_x         = height - 2 * padding_y

        line_width = step_x / 100
        palette    = self.pick_palette(6, .1, .5)
        # coef of an angle of the switching singals  
        coef       = (.8 * step_x) / (height - (2 * padding_y))  
        gate_unit  = step_x / (2 * number) # half of the gate width
        gate_pos   = []

        # calculate coordinates for strate signal-lines in the scheme
        range_y = [height - padding_y - step_y * index 
            for index in range(n_steps_y)]

        # the first points for lines of s scheme
        line_coords = [[padding_x, y] for y in reversed(range_y)]

        for index, gene in enumerate(genotype):
            new_x    = line_coords[0][-2] + step_x 
            n_unused = 1    # n from number
            jndex    = 0

            for alet in reversed(gene):
                x_before = line_coords[jndex][-2] + .1 * step_x
                y_before = line_coords[jndex][-1] 

                if alet == [0, 0]:
                    new_y     = 20
                    new_y     = range_y[-n_unused]
                    n_unused += 1
                else:
                    new_y = range_y[3 * (alet[0] - 1) + alet[1]] 
                    if alet[1] == 0:
                        gate_pos.append([new_x + gate_unit, new_y])

                line_coords[jndex].append(x_before)   
                line_coords[jndex].append(y_before)

                x_between = x_before + coef * abs(new_y - y_before)
                line_coords[jndex].append(x_between)   
                line_coords[jndex].append(new_y)

                line_coords[jndex].append(new_x)   
                line_coords[jndex].append(new_y)  

                line_coords[jndex].append(new_x + 2 * gate_unit)   
                line_coords[jndex].append(new_y)  
                jndex += 1 

        # the last points for lines of s scheme
        for line in line_coords:
            line.append(line[-2] + .1* step_x)
            line.append(line[-2])

        with self.canvas:
            # draw background
            Color(1, 1, 1, 1)
            Rectangle(size=(width, height), pos=(0,0))

            # draw signals-lines
            for index, line in enumerate(line_coords):
                Color(palette[index][0],
                      palette[index][1],
                      palette[index][2],
                      palette[index][3])
                Line (points=(line),
                      width = line_width,
                      cap   ='square',
                      joint ='miter')
            
            # draw circuits of the Fredkin gates 
            Color(0, 0, 0, 1)
            size_unit = .7 * gate_unit
            for pos in gate_pos:
                # the top round
                pos0 = [pos[0] - size_unit, pos[1] - size_unit]
                Ellipse(pos=pos0, size=(2 * size_unit, 2 * size_unit))

                # connection line
                gate_bottom = pos[1] - 2 * step_y
                Line (points=(pos[0], pos[1], pos[0], gate_bottom),
                      width = line_width,
                      cap   ='square')
                
                # the middle cross
                pos1 = [pos[0], pos[1] - step_y]
                Line (points=(pos1[0] - size_unit, 
                              pos1[1] - size_unit, 
                              pos1[0] + size_unit, 
                              pos1[1] + size_unit),
                      width = line_width,
                      cap   ='square')
                Line (points=(pos1[0] + size_unit, 
                              pos1[1] - size_unit, 
                              pos1[0] - size_unit, 
                              pos1[1] + size_unit),
                      width = line_width,
                      cap   ='square')

                # the bottom cross
                pos2 = [pos1[0], pos1[1] - step_y]
                Line (points=(pos2[0] - size_unit, 
                              pos2[1] - size_unit, 
                              pos2[0] + size_unit, 
                              pos2[1] + size_unit),
                      width = line_width,
                      cap   ='square')
                Line (points=(pos2[0] + size_unit, 
                              pos2[1] - size_unit, 
                              pos2[0] - size_unit, 
                              pos2[1] + size_unit),
                      width = line_width,
                      cap   ='square')

        self.width = width

    def pick_palette(self, number=COLOURS_NUMBER, start=.2, stop=1):
        palette = []
        start   = int(start * 100)
        stop    = int(stop  * 100)
        step    = (stop - start) // 7
        points  = [float(value)/100 for value in range(start, stop, step)]

        while len(palette) < number: 
            col_a = choice(points)

            reduced_points = points
            index = points.index(col_a)
            reduced_points.pop(index)
            col_b = choice(reduced_points)
            
            index = reduced_points.index(col_b)
            reduced_points.pop(index)
            col_c = choice(reduced_points)

            palette.append([col_a, col_b, col_c, 1])
            palette.append([col_b, col_a, col_c, 1])
            palette.append([col_c, col_b, col_a, 1])
        
        return palette[:number]

class SchemeDrawApp(App):
    def build(self):
        parent      = ScrollView(do_scroll_x=True, 
                                 effect_cls='ScrollEffect')
        self.parent = Scheme()
        parent.add_widget(self.parent)
        return parent


if __name__ == '__main__':
    SchemeDrawApp().run()