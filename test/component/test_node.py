""" The module is designed to test the Node class.

:Author: Oleksii Dovhaniuk
:E-mail: dovhaniuk.oleksii@chnu.edu.ua
:Date: 08.03.2021

"""

from PIL import Image
from component.node import Node
import unittest
import sys
sys.path.append('D:/Workspace/Python/projects/QubitLab')


class TestGate(unittest.TestCase):

    def setUp(self):
        path_node = 'test/res/node'

        self.n1 = Node('__circle_crossed')
        self.n2 = Node('__circle_white', 'N', 'W')
        self.n3 = Node('__cross')
        self.n4 = Node('__wrong_node_name', '3b', 'W')
        self.n5 = Node('__dot_black')
        self.n6 = Node('__dot_white_triangle_down')
        self.n7 = Node('__square_black', 'V+useless_text', 'K')
        self.n8 = Node('__square_black', colour='K')
        self.n9 = Node('__circle_black', 'T-', colour='K')

    def tearDown(self):
        """ The function is called after each test function is executed.

        If there are connections are needed to enject, 
        then enter appropriate code below.

        """
        self.n1.icon.close()
        self.n2.icon.close()
        self.n3.icon.close()
        self.n4.icon.close()
        self.n5.icon.close()
        self.n6.icon.close()
        self.n7.icon.close()
        self.n8.icon.close()
        self.n9.icon.close()

    def test__init__(self):
        self.assertEquals(self.n1.name, '__circle_crossed')
        self.assertEquals(self.n2.name, '__circle_white')
        self.assertEquals(self.n3.name, '__cross')
        self.assertEquals(self.n4.name, '__cube_white')
        self.assertEquals(self.n5.name, '__dot_black')
        self.assertEquals(self.n6.name, '__dot_white_triangle_down')
        self.assertEquals(self.n7.name, '__square_black')
        self.assertEquals(self.n8.name, '__square_black')
        self.assertEquals(self.n9.name, '__circle_black')

        self.assertEquals(self.n1.tag, None)
        self.assertEquals(self.n2.tag, 'N')
        self.assertEquals(self.n3.tag, None)
        self.assertEquals(self.n4.tag, '3b')
        self.assertEquals(self.n5.tag, None)
        self.assertEquals(self.n6.tag, None)
        self.assertEquals(self.n7.tag, 'V+')
        self.assertEquals(self.n8.tag, None)
        self.assertEquals(self.n9.tag, 'T-')

        self.assertEquals(self.n1.colour, None)
        self.assertEquals(self.n2.colour, 'W')
        self.assertEquals(self.n3.colour, None)
        self.assertEquals(self.n4.colour, 'W')
        self.assertEquals(self.n5.colour, None)
        self.assertEquals(self.n6.colour, None)
        self.assertEquals(self.n7.colour, 'K')
        self.assertEquals(self.n8.colour, 'K')
        self.assertEquals(self.n9.colour, 'K')

    def test_get_view(self):
        a_size = (256, 256)

        view1 = self.n1.get_view()
        view2 = self.n2.get_view('Futura')
        view3 = self.n3.get_view(a=128)
        view4 = self.n4.get_view(a=2)
        view5 = self.n5.get_view()
        view6 = self.n6.get_view('Futura', 64)
        view7 = self.n7.get_view('Futura')
        view8 = self.n8.get_view()
        view9 = self.n9.get_view()

        with Image.open(f'res/node/__circle_crossed.png') as img:
            img_type = type(img.resize(a_size))

            self.assertEquals(type(view1), img_type)
            self.assertEquals(type(view2), img_type)
            self.assertEquals(type(view3), img_type)
            self.assertEquals(type(view4), img_type)
            self.assertEquals(type(view5), img_type)
            self.assertEquals(type(view6), img_type)
            self.assertEquals(type(view7), img_type)
            self.assertEquals(type(view8), img_type)
            self.assertEquals(type(view9), img_type)

        self.assertEquals(view1.size, a_size)
        self.assertEquals(view2.size, a_size)
        self.assertEquals(view3.size, (128, 128))
        self.assertEquals(view4.size, (8, 8))
        self.assertEquals(view5.size, a_size)
        self.assertEquals(view6.size, (64, 64))
        self.assertEquals(view7.size, a_size)
        self.assertEquals(view8.size, a_size)
        self.assertEquals(view9.size, a_size)

    def test_save(self):
        self.n1.save()
        self.n2.save()
        self.n3.save()
        self.n4.save()
        self.n5.save()
        self.n6.save()
        self.n7.save()
        self.n8.save()
        self.n9.save()


if __name__ == '__main__':
    unittest.main()
