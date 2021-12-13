""" The module is designed to test the Genetic class.

:Author: Oleksii Dovhaniuk
:E-mail: dovhaniuk.oleksii@chnu.edu.ua
:Date: 18.01.2021

"""
from component.gate import Gate
from component.node import Node
from algorithm.genetic_algorithm import GeneticAlgorithm
import numpy as np
import unittest
import sys
sys.path.append('D:/Workspace/Python/projects/QubitLab')


class TestGenetic(unittest.TestCase):

    def setUp(self):
        n1 = Node('__dot_black')
        n2 = Node('__cross')
        n3 = Node('__circle_crossed')
        n4 = Node('__dot_white')

        self.not2b = Gate('NOT2b', 1, 1, [n3], [[1], [0]])
        self.ncn2b = Gate('NCN2b', 3, 2, [n4, n3],
                          [[0, 1], [0, 0], [1, 0], [1, 1]])
        self.frg2b = Gate('FRG2b', 5, 1.92, [n1, n2, n2],
                          [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1],
                           [1, 0, 0], [1, 1, 0], [1, 0, 1], [1, 1, 1]])
        self.tg2b = Gate('TG2b', 5, 1.5, [n1, n1, n3],
                         [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1],
                          [1, 0, 0], [1, 0, 1], [1, 1, 1], [1, 1, 0]])

        self.g1 = GeneticAlgorithm([self.frg2b, self.not2b, self.ncn2b, None],
                                   7, 10, 1000)
        self.g2 = GeneticAlgorithm([self.frg2b, self.tg2b, None],
                                   6, 7, 550, 5, [.3, .3, .4])

    def tearDown(self):
        """ The function is called after each test function is executed.

        If there are connections are needed to enject,
        then enter appropriate code below.

        """
        for gate in (self.not2b, self.ncn2b, self.frg2b, self.tg2b):
            for node in gate.nodes:
                node.icon.close()

    def test__init__(self):
        gt0 = None
        gt1 = self.frg2b
        gt2 = self.not2b
        gt3 = self.ncn2b
        gt4 = self.tg2b

        g1 = self.g1
        g2 = self.g2

        self.assertListEqual(g1.basis, [gt1, gt2, gt3, gt0])
        self.assertListEqual(g2.basis, [gt1, gt4, gt0])

        self.assertEqual(g1.al_size, 7)
        self.assertEqual(g2.al_size, 6)

        self.assertEqual(g1.chrm_size, 10)
        self.assertEqual(g2.chrm_size, 7)

        self.assertEqual(g1.gen_size, 1000)
        self.assertEqual(g2.gen_size, 550)

        self.assertEqual(g1.gms, 0)
        self.assertEqual(g2.gms, 5)

        self.assertEqual(g1.weights, [.25, .25, .25, .25])
        self.assertEqual(g2.weights, [.3, .3, .4])

        exp1 = {gt1: [[0, 1, 2], [6, 1, 3], [4, 5, 6]],
                gt2: [[1], [3], [6]],
                gt3: [[0, 1], [4, 2], [5, 6]],
                gt0: [()]}
        for key in exp1:
            self.assertTrue(all([pos in g1.genome[key] for pos in exp1[key]]))
        exp2 = {gt1: [[0, 1, 2], [5, 1, 3], [3, 4, 5]],
                gt4: [[0, 1, 2], [2, 5, 4], [3, 4, 5]],
                gt0: [()]}
        for key in exp2:
            self.assertTrue(all([pos in g2.genome[key] for pos in exp2[key]]))

        not_exp1 = {gt1: [[0, 0, 0], [-1, 1, 3], [4, 6, 6], [1, 3, 2]],
                    gt2: [[-1], [7], [99]],
                    gt3: [[0, 1, 2], [7, 2], [6]],
                    gt0: [[0], [1, 2], [1, 2, 6]]}
        for key in not_exp1:
            self.assertFalse(any([pos in g1.genome[key]
                                  for pos in not_exp1[key]]))
        not_exp2 = {gt1: [[0], [6, 1], [4, 5, 6, 1]],
                    gt4: [[0, 1, -2], [15, 2, 4], [4, 7, 6], [7, 6, 2], [5, 2, 4]],
                    gt0: [[0], [1, 2], [1, 2, 6]]}
        for key in not_exp2:
            self.assertFalse(any([pos in g2.genome[key]
                                  for pos in not_exp2[key]]))

        self.assertDictEqual(g1.tops, {
            self.frg2b: 0,
            self.not2b: 0,
            self.ncn2b: 0,
            None: 0})
        self.assertDictEqual(g2.tops, {
            self.frg2b: 0,
            self.tg2b: 0,
            None: 0})

    def test_create(self):
        g1 = self.g1
        g2 = self.g2

        gt0 = None
        gt1 = self.frg2b
        gt2 = self.not2b
        gt3 = self.ncn2b
        gt4 = self.tg2b

        g1.create()
        self.assertEqual(g1.gen_size, len(g1.gen))
        self.assertTrue(all([len(chrm) == g1.chrm_size for chrm in g1.gen]))
        for chrm in g1.gen:
            for key in g1.genome:
                self.assertTrue(
                    all([al[1] in g1.genome[al[0]] for al in chrm]))

        g2.create()
        self.assertEqual(g2.gen_size, len(g2.gen))
        self.assertTrue(all([len(chrm) == g2.chrm_size for chrm in g2.gen]))
        for chrm in g2.gen:
            for key in g2.genome:
                self.assertTrue(
                    all([al[1] in g2.genome[al[0]] for al in chrm]))

        chrms1 = [[[gt0, ()], [gt0, ()], [gt0, ()],
                   [gt1, [1, 2, 3]], [gt1, [1, 3, 5]],
                   [gt2, [1]], [gt2, [3]], [gt2, [5]],
                   [gt3, [1, 2]], [gt3, [3, 6]]]]
        chrms2 = [[[gt0, ()], [gt0, ()], [gt0, ()],
                   [gt1, [1, 2, 3]], [gt1, [1, 3, 5]],
                   [gt4, [1, 4, 5]], [gt4, [1, 2, 5]]]
                  for _ in range(10)]

        g1.create(chrms1)
        self.assertEqual(g1.gen_size, len(g1.gen))
        # print([len(chrm) for chrm in g1.gen])
        # print(g1.chrm_size)
        # print(g1.gen[0])
        # print(len(g1.gen[0]))
        self.assertTrue(all([len(chrm) == g1.chrm_size for chrm in g1.gen]))
        for chrm in g1.gen:
            for key in g1.genome:
                self.assertTrue(
                    all([al[1] in g1.genome[al[0]] for al in chrm]))
        self.assertEqual(chrms1[0], g1.gen[0])

        g2.create(chrms2)
        self.assertEqual(g2.gen_size, len(g2.gen))
        self.assertTrue(all([len(chrm) == g2.chrm_size for chrm in g2.gen]))
        for chrm in g2.gen:
            for key in g2.genome:
                self.assertTrue(
                    all([al[1] in g2.genome[al[0]] for al in chrm]))
        self.assertTrue(all([chrms2[i] == g2.gen[i] for i in range(10)]))

        chrms1 = [[[gt0, ()], [gt0, ()], [gt0, ()],
                   [gt1, [1, 2, 3]], [gt1, [1, 3, 5]],
                   [gt2, [1]], [gt2, [3]], [gt2, [5]],
                   [gt3, [1, 2]], [gt3, [3, 6]]]
                  for _ in range(1000)]
        chrms2 = [[[gt0, ()], [gt0, ()], [gt0, ()],
                   [gt1, [1, 2, 3]], [gt1, [1, 3, 5]],
                   [gt4, [1, 4, 5]], [gt4, [1, 2, 5]]]
                  for _ in range(551)]

        g1.create(chrms1)
        self.assertEqual(g1.gen_size, len(g1.gen))
        self.assertTrue(all([len(chrm) == g1.chrm_size for chrm in g1.gen]))
        for chrm in g1.gen:
            for key in g1.genome:
                self.assertTrue(
                    all([al[1] in g1.genome[al[0]] for al in chrm]))
        self.assertTrue(all([chrms1[i] == g1.gen[i] for i in range(1000)]))

        g2.create(chrms2)
        self.assertEqual(g2.gen_size, len(g2.gen))
        self.assertTrue(all([len(chrm) == g2.chrm_size for chrm in g2.gen]))
        for chrm in g2.gen:
            for key in g2.genome:
                self.assertTrue(
                    all([al[1] in g2.genome[al[0]] for al in chrm]))
        self.assertTrue(all([chrms2[i] == g2.gen[i] for i in range(550)]))

    def test_crossover(self):
        g1 = self.g1
        g1.create()
        v1 = np.random.rand(len(g1.gen))
        g2 = self.g2
        g2.create()
        v2 = np.random.rand(len(g2.gen))
        p = 0.4  # Crossover probabbility.

        g1.crossover(v1, p, 1, True)
        self.assertEqual(g1.gen_size, len(g1.gen))
        self.assertTrue(all([len(chrm) == g1.chrm_size for chrm in g1.gen]))
        for chrm in g1.gen:
            for key in g1.genome:
                self.assertTrue(
                    all([al[1] in g1.genome[al[0]] for al in chrm]))

        g1.crossover(v1, p, 10)
        self.assertEqual(g1.gen_size, len(g1.gen))
        self.assertTrue(all([len(chrm) == g1.chrm_size for chrm in g1.gen]))
        for chrm in g1.gen:
            for key in g1.genome:
                self.assertTrue(
                    all([al[1] in g1.genome[al[0]] for al in chrm]))

        g2.crossover(v2, p, 2, True)
        self.assertEqual(g2.gen_size, len(g2.gen))
        self.assertTrue(all([len(chrm) == g2.chrm_size for chrm in g2.gen]))
        for chrm in g2.gen:
            for key in g2.genome:
                self.assertTrue(
                    all([al[1] in g2.genome[al[0]] for al in chrm]))

        g2.crossover(v2, p, 4)
        self.assertEqual(g2.gen_size, len(g2.gen))
        self.assertTrue(all([len(chrm) == g2.chrm_size for chrm in g2.gen]))
        for chrm in g2.gen:
            for key in g2.genome:
                self.assertTrue(
                    all([al[1] in g2.genome[al[0]] for al in chrm]))

    def test_mutation(self):
        g1 = self.g1
        g1.create()
        v1 = np.random.rand(len(g1.gen))
        g2 = self.g2
        g2.create()
        v2 = np.random.rand(len(g2.gen))
        p = 0.08  # Mutation probabbility.

        g1.mutation(v1, p, 1, True)
        self.assertEqual(g1.gen_size, len(g1.gen))
        self.assertTrue(all([len(chrm) == g1.chrm_size for chrm in g1.gen]))
        for chrm in g1.gen:
            for key in g1.genome:
                self.assertTrue(
                    all([al[1] in g1.genome[al[0]] for al in chrm]))

        g1.mutation(v1, p, 10)
        self.assertEqual(g1.gen_size, len(g1.gen))
        self.assertTrue(all([len(chrm) == g1.chrm_size for chrm in g1.gen]))
        for chrm in g1.gen:
            for key in g1.genome:
                self.assertTrue(
                    all([al[1] in g1.genome[al[0]] for al in chrm]))

        g2.mutation(v2, p, 2, True)
        self.assertEqual(g2.gen_size, len(g2.gen))
        self.assertTrue(all([len(chrm) == g2.chrm_size for chrm in g2.gen]))
        for chrm in g2.gen:
            for key in g2.genome:
                self.assertTrue(
                    all([al[1] in g2.genome[al[0]] for al in chrm]))

        g2.mutation(v2, p, 4)
        self.assertEqual(g2.gen_size, len(g2.gen))
        self.assertTrue(all([len(chrm) == g2.chrm_size for chrm in g2.gen]))
        for chrm in g2.gen:
            for key in g2.genome:
                self.assertTrue(
                    all([al[1] in g2.genome[al[0]] for al in chrm]))


if __name__ == '__main__':
    unittest.main()
