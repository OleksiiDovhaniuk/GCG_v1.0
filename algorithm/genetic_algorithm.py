""" The module is a genetic algorithm calculation unit.

:Author:    Oleksii Dovhaniuk
:E-mail:    dovhaniuk.oleksii@chnu.edu.ua
:Date:      18.01.2021

"""

from itertools import permutations
import numpy as np
from copy import copy, deepcopy

from calc.fitness_function import calc
from component.node import Node


class GeneticAlgorithm():
    """ Contains all ginetic algorithm stages as python methods.

        :attr: `basis` (tuple of Gate objects).

        :attr: `al_size` (int): Number of the lines of the
            synthesing device.

        :attr: `chrm_size` (int): Chromosome size.

        :attr: `gen_size` (int): Generation size.

        :attr: `gms` (int): Generation memory size.
            Number of the best chromosmes, which will pass
            the crossover operation without transformation.

        :attr: `weights` (tuple of float):
            By default None. It represents a gate appearence probability
            in the scheme, including empty None object.

        :attr: `genome` (nested list):
            All possible variation of the alleles according to
            the gained basis and rules.

        :attr: `tops` (dict):
            {Gate object -> <index of the next elment in genome>}.

        :attr: `gen` (nested list): Generation.


        :meth: __init__(basis, al_size, chrm_size, gen_size, gms=0, weights=None).

        :meth: create().

        :meth: crossover(values, p, max_length, fixed=False).

        :meth: mutation(values, p, max_length, fixed=False).

    """

    def __init__(self, basis, al_size, chrm_size, gen_size, gms=0, weights=None):
        """ Initialise Genetic class object.

            :arg: `basis` (tuple of Gate objects).

            :arg: `al_size` (int): Number of the lines of the
                synthesing device.

            :arg: `chrm_size` (int): Chromosome size.

            :arg: `gen_size` (int): Generation size.

            :arg: `gms` (int): Generation memory size.
                Number of the best chromosmes, which will pass
                the crossover operation without transformation.

            :arg: `weights` (tuple of float):
                By default None. It represents a gate appearance probability
                in the scheme, including empty None object. The addition of all
                weights equals 1.

            :creat: `genome` (nested list):
                All possible variation of the alleles according to
                the gained basis and rules.

        """
        self.basis = basis
        self.al_size = max(al_size, 1)
        self.chrm_size = max(chrm_size, 1)
        self.gen_size = max(gen_size, 10)
        self.gms = min(gms, gen_size-1)
        self.tops = {}
        self.genome = {}

        if weights:
            self.weights = list(weights)
        else:
            self.weights = [1/len(basis) for _ in basis]

        for index, unit in enumerate(basis):

            if len(unit.nodes) > al_size:
                self.weights[index] = 0
                continue

            iterable = np.arange(al_size)
            nodes = permutations(iterable, unit.size)
            nodes = self.__clear_duplicats(unit, nodes)

            self.genome[unit] = [list(node) for node in nodes]
            self.tops[unit] = 0

    def create(self, chrms=[]):
        """ Method creates a new generation based on next data:
            self.genome, self.chrm_size, self.gen_size, and self.weights.

            :arg: `chrms` (nested list): If chrms entered, the generation
                will be created with inserted chrms (`len(chrms) <= gen_size`).

            :create: `gen`: Generation.

        """
        size = min(self.gen_size, len(chrms))
        gen = [chrm for chrm in chrms[:size]]

        for _ in range(self.gen_size - size):
            chrm = []
            for _ in range(self.chrm_size):
                chrm.append(self.__create_allele())
            gen.append(chrm)

        self.gen = gen

    def crossover(self, values, p, max_length, fixed=False):
        """ The method does operation crossover on the current generation.

            :arg: `values` (numpy array of float): Evaluetion values for the crossover.
                The values should relate to the current generation; consiquently,
                the number of elements in values array and self.gen array are equal.

            :arg: `p` (float): Crossover probabbility (0<p<=1).

            :arg: `max_length` (int): Maximal length of the crossover.

            :arg: `fixed` (bool): If False the length of the crossover for each
                chromsome can fluctuate in range [0, min(max_length, self.chrm_size-point].
                Otherwise, crossover is fixed to min(max_length, self.chrm_size-point) value.
                Where point is the initial crossover index.

        """
        gen_copy = list(self.gen)
        values_copy = np.array(values)
        gen = self.gen
        # for chrm in gen:
        #     for al in chrm:
        #         print(al[1])
        #     print()
        size = self.gen_size
        new_gen = []

        for _ in range(self.gms):
            try:
                new_gen.append(gen_copy.pop(np.argmax(values_copy)))
                values_copy = np.delete(values_copy, np.argmax(values_copy))
            except IndexError as e:
                print(
                    f'{e}: ff_values size - {len(values_copy)}, generation size - {len(gen_copy)}')

        total = sum(values)
        # Probbabilities of choosing the chromosome.
        probs = values / total
        # print(size, len(probs))

        while len(new_gen) < size:
            i = np.random.choice(size, 1, p=probs)[0]

            new_chrm = gen[i].copy()

            cur_prob = np.random.uniform()

            if (cur_prob <= p):
                # print(cur_prob)
                i = np.random.choice(size, 1, p=probs)[0]
                mate_chrm = gen[i].copy()

                # Crossover range.
                cr = self.operation_range(max_length, fixed)
                # str_new_chrm = ''
                # for al in new_chrm:
                #     str_new_chrm += str(al[1])
                # str_mate_chrm = ''
                # for al in mate_chrm:
                #     str_mate_chrm += str(al[1])
                # print(f'{str_new_chrm}\n {cr[0]} {cr[1]} \n{str_mate_chrm}')
                # print()

                new_chrm[cr[0]: cr[1]], mate_chrm[cr[0]: cr[1]] = (
                    mate_chrm[cr[0]:cr[1]], new_chrm[cr[0]:cr[1]])

                # str_new_chrm = ''
                # for al in new_chrm:
                #     str_new_chrm += str(al[1])
                # str_mate_chrm = ''
                # for al in mate_chrm:
                #     str_mate_chrm += str(al[1])
                # print(f'{str_new_chrm}\n{cr[0]} {cr[1]}\n{str_mate_chrm}')
                # print('--------------------------------------------------')
                # print()

                if mate_chrm in new_gen:
                    continue
                else:
                    new_gen.append(mate_chrm)

            elif new_chrm in new_gen:
                continue
            else:
                new_gen.append(new_chrm)

        # print()
        # print()
        # for chrm in new_gen:
        #     for al in chrm:
        #         print(al[1])
        #     print()

        self.gen = new_gen

    def mutation(self, values, p, max_length, fixed=False):
        """ The method does operation mutation on the current generation.

        :arg: `p` (float): Mutation probabbility (0<=p<=1).

        :arg: `max_length` (int): Maximal length of the mutation.

        :arg: `fixed` (bool): If False the length of the mutation for each
            chromsome can fluctuate in range [0, min(max_length, self.chrm_size-point].
            Otherwise, mutation is fixed to min(max_length, self.chrm_size-point) value.
            Where point is the initial mutation index.

        """
        gen_copy = list(self.gen)
        gen = self.gen
        new_gen = [chrm for chrm in gen[:self.gms]]

        for index, chrm in enumerate(gen):
            new_chrm = list(chrm)

            if np.random.uniform() <= p:
                # Mutation range.
                mut_range = self.operation_range(max_length, fixed)

                for i in range(mut_range[0], mut_range[1]):
                    new_chrm[i] = self.__create_allele()

            while new_chrm in new_gen:
                # Mutation range.
                mut_range = self.operation_range(max_length, fixed)

                for i in range(mut_range[0], mut_range[1]):
                    new_chrm[i] = self.__create_allele()

            new_gen.append(new_chrm)

        """ TODO:
            Think about better way to keep
            generation constantly in gen_size,
            than cutting off appended chromosomes.
        """
        self.gen = new_gen[:self.gen_size]

    def __create_allele(self):
        """ The method creates a new allele.

            :return: A new allele, nested list
                [object of type <Gate>, <indices_of_activating_lines>].

        """
        gate = np.random.choice(self.basis, p=self.weights)
        try:
            self.tops[gate] += 1
            return [gate, self.genome[gate][self.tops[gate]]]
        except IndexError:
            self.tops[gate] = 0
            return [gate, self.genome[gate][0]]

    def operation_range(self, max_length, fixed=False):
        """ Defines an operational range.

            :arg: `max_length` (int): Maximal length of the operation.
            :arg: `fixed` (bool): If False the length of the operation for each
                chromsome can fluctuate in range [0, min(max_length, self.chrm_size-point].
                Otherwise, operation is fixed to min(max_length, self.chrm_size-point) value.
                Where point is the initial operation index.

            :return: tuple of starting and end point of an operation.

        """
        point = np.random.randint(0, self.chrm_size)
        max_end_point = min(point+max_length, self.chrm_size)

        if fixed:
            end_point = max_end_point
        else:
            end_point = np.random.randint(point+1, max_end_point+1)

        return point, end_point

    def __clear_duplicats(self, gate, nodes):
        """ Returns copy of nodes` array without duplicates by
            similar nodes.

            :arg: gate (Gate object).

            :arg: nodes (NumPy ndarray).

            :return: NumPy ndarray object.

        """
        clear_array = []
        check_list = []

        for node_list in nodes:
            node_list = node_list
            check = [None for _ in range(self.al_size)]
            for node, index in zip(gate.nodes, node_list):
                check[index] = node

            if check not in check_list:
                clear_array.append(node_list)
                check_list.append(check)

        return clear_array


def migration(islands, values, p, max_length, fixed=False):
    """ The function realise solutions in solving a stagnation problem.

    :arg: `islands` (list of <obj. GeneticAlgorithm>).

    :arg: `values` (combined list of fitness function values).

    :arg: `p` (float): Crossover probabbility (0<p<=1).

    :arg: `max_length` (int): Maximal length of the crossover.

    :arg: `fixed` (bool): If False the length of the crossover for each
        chromsome can fluctuate in range [0, min(max_length, self.chrm_size-point].
        Otherwise, crossover is fixed to min(max_length, self.chrm_size-point) value.
        Where point is the initial crossover index.

    :return: migrated generations

    """
    combined_gen = []
    for ga in islands:
        combined_gen.extend(ga.gen)

    islands_copy = [copy(ga) for ga in islands]
    top = 0
    for ga, ga_copy in zip(islands, islands_copy):
        ga.gen = []
        values_copy = np.array(copy(values))[top:top+ga.gen_size]
        top += ga.gen_size
        for _ in range(islands[0].gms):
            try:
                ga.gen.append(ga_copy.gen.pop(np.argmax(values_copy)))
                values_copy = np.delete(values_copy, np.argmax(values_copy))
            except IndexError as e:
                print(
                    f'{e}: ff_values size - {len(values_copy)}, generation size - {len(ga_copy.gen)}')

    size = len(combined_gen)
    total = sum(values)
    probs = values / total

    for ga in islands:
        while len(ga.gen) < ga.gen_size:
            i = np.random.choice(size, 1, p=probs)[0]

            new_chrm = combined_gen[i].copy()

            cur_prob = np.random.uniform()

            if (cur_prob <= p):
                i = np.random.choice(size, 1, p=probs)[0]
                mate_chrm = combined_gen[i].copy()

                cr = islands[0].operation_range(max_length, fixed)

                new_chrm[cr[0]: cr[1]], mate_chrm[cr[0]: cr[1]] = (
                    mate_chrm[cr[0]:cr[1]], new_chrm[cr[0]:cr[1]])

                if mate_chrm in ga.gen:
                    continue
                else:
                    ga.gen.append(mate_chrm)

            elif new_chrm in ga.gen:
                continue
            else:
                ga.gen.append(new_chrm)

    print('Hey Ya!!! Migaration!')
    # for ga in islands:
    #     print(len(ga.gen), ga.gen_size)
    return islands
