""" The module represents a node of the gate.

:Author: Oleksii Dovhaniuk
:E-mail: dovhaniuk.oleksii@chnu.edu.ua
:Date: 22.02.2021

:TODO: Finish Node.save() method.

"""

from PIL import Image, ImageFont, ImageDraw


class Node():
    """ 
        :attr: name (string): Title of the node.

        :attr: tag (string): Up to two characters 
            written inside the node.    

        :attr: icon (PIL Image object): 
            Schematic representation of the node.

        :attr: _default_node (string, immutable): '_cube_white'.

        :attr: _path_node (string, immutable): 
            Path where are stored all png files of the nodes` icons.

        :attr: _default_font (string, immutable): 'Helvetica'.

        :attr: _path_font (string, immutable): 
            Path where are stores all ttf files.

        :attr: _default_width (int, immutable). 

        :attr: _min_width (int, immutable). 

        :meth: __init__(name, tag=None, font_size=_min_font).

        :meth: get_view(font=_default_font).

        :meth: save().

    """
    _default_node = '__cube_white'
    _path_node = 'res/node'
    _default_font = 'Helvetica'
    _path_font = 'res/font'
    _colours = {'K': (0, 0, 0), 'W': (255, 255, 255)}
    _default_width = 256
    _min_width = 8

    def __init__(self, name, tag=None, colour=None):
        path = self._path_node

        if tag:
            self.tag = tag[:2]
        else:
            self.tag = None

        if colour in self._colours.keys():
            self.colour = colour
        else:
            self.colour = None

        try:
            self.icon = Image.open(f'{path}/{name}.png')
            self.name = name
        except FileNotFoundError as e:
            print(f'[Tried open node.icon]: {e}')
            self.icon = Image.open(f'{path}/{self._default_node}.png')
            self.name = self._default_node

    def get_view(self, font=_default_font, a=_default_width):
        """ Method merges icon with tag into single Image object,
            if there is any tag.

            :arg: font (string). Font file name.

            :return: Image object.

        """
        view = self.icon
        tag = self.tag
        a = max(a, self._min_width)

        if tag:
            draw = ImageDraw.Draw(view)
            l = view.size[0] * .5
            font_size = int(l * .9)
            if len(tag) == 1:
                tag_xy = (l - font_size*.37, l - font_size*.42)
            else:
                tag_xy = (l - font_size*.54, l - font_size*.42)

            if self.colour == 'W':
                tag_colour = self._colours['K']
            else:
                tag_colour = self._colours['W']

            try:
                font = ImageFont.truetype(
                    f'{self._path_font}/{font}.ttf', font_size)
            except FileNotFoundError as e:
                print(f'[Tried read a font of the node merge]: {e}')
                font = ImageFont.truetype(
                    f'{self._path_font}/{self._default_font}.ttf', font_size)

            draw.text(tag_xy, tag, tag_colour, font)
        else:
            print('[Component.node]: Cannot merge node.')

        return view.resize((a, a))

    def save(self):
        """ Method saves the node into database and
            stores the node`s view as custom node 
            png file into application file system. 

        """

        ''' TODO: Validate the node before saving.'''
        if self.tag:
            view = self.get_view()
            view.save(f'{self._path_node}/{self.name[2:]}_{self.tag}.png')
        else:
            print('[Component.node]: Saving is failed. Current node already exists.')

        ''' TODO: Save the node to database '''
