import random 


class Genetic():
    """ Contains all ginetic algorithm stages.

    Each function of the modul represent stage of genetic algorithm.

    Args: 
        sgn_no (int): number of inputs/outputs in truth table.
        control_range=(1,1): tuple of two integer digits (n, m), where
            0 < n <= m and n - min number of control gates in the scheme,
            m - max number of control gates in the scheme 
            (Note: when only one number is needed n = m and m for any 
            inputed value less than sgn_no - 1).    

    Methods: 
        create(size, gene_no),
        selection(values),
        paar_crossover(a, b, generation, crossovered_generation, probability),
        crossover(generation, indeces, probability),
        chrm_mutation(chromosom),
        mutation(generation, mutation_probability)

    Examples of execution:
        >>> Genetic(6).EMPTY_COEF
        0.3
        >>> Genetic(6).index
        1
    """
    EMPTY_COEF = .3

    def __init__(self, sgn_no, control_range=(1,1)):
        """ Creating list of all existing genes for the inputed values.

        Args: 
            sgn_no (int): number of inputs/outputs in truth table.
            control_range=(1,1): tuple of two integer digits (n, m), where
                0 < n <= m and n - min number of control gates in the scheme,
                m - max number of control gates in the scheme 
                (Note: when only one number is needed n = m and m for any 
                inputed value less than sgn_no - 1).    

        Examples of execution:
            >>> ganes_6 = [[0, 0], [16, 3], [2, 5], [0, 3],\
                    [16, 17], [63, 63], [32, 1]]
            >>> ganes_5_11 = [[0, 0], [16, 3], [2, 5], [0, 3],\
                    [16, 17], [1, 1], [32, 1], [1, 48]]
            >>> ganes_4_26 = [[0, 0], [1, 6], [9, 6], [0, 3],\
                    [16, 17], [1, 1], [32, 1]]
            >>> sign_no = 0
            >>> Genetic(sign_no).genes
            [[0, 0]]
            >>> sign_no
            0
            >>> sign_no = 1
            >>> Genetic(sign_no).genes
            [[0, 0]]
            >>> sign_no
            1
            >>> sign_no = 6
            >>> len(Genetic(sign_no).genes)
            61
            >>> sign_no
            6
            >>> [x in Genetic(sign_no).genes for x in ganes_6]
            [True, True, True, False, False, False, False]
            >>> sign_no
            6
            >>> sign_no = 5
            >>> len(Genetic(sign_no, (1, 1)).genes)
            31
            >>> sign_no
            5
            >>> [x in Genetic(sign_no, (1, 1)).genes for x in ganes_5_11]
            [True, True, True, False, False, False, False, False]
            >>> sign_no
            5
            >>> sign_no = 4
            >>> len(Genetic(sign_no, (2, 6)).genes)
            7
            >>> sign_no
            4
            >>> [x in Genetic(sign_no, (2, 6)).genes for x in ganes_4_26]
            [True, False, True, False, False, False, False]
            >>> sign_no
            4

        """
        genes = [[0, 0]]
        max_num = int(2 ** sgn_no - 1)

        for control in range(max_num):
            once_no = '{0:b}'.format(control).count('1')

            if (
                control_range[0] <= once_no <= control_range[1]
                and
                once_no < sgn_no - 1
            ):
                for switch in range(max_num):
                    if (
                        '{0:b}'.format(switch).count('1') == 2
                        and
                        control & switch == 0
                    ): 
                        genes.append([control, switch])

        self.genes = genes
        self.index = 1

    def create(self, size, gene_no):
        """ Create generation of chromosom for work with genetic algorithm.
        Filling generation with approperet semi random elements.

        Args:
            size (int): number of chromosomes.
            gene_no (int): number of genes in chromosome.
            
        Returns:
            generation (3D list): semi random generated 3 dimensional list.
        
        Examples of execution:
            >>> gntc = Genetic(4, (2, 6))
            >>> g = gntc.create(3, 10000)
            >>> len(g)
            3
            >>> len(g[2])
            10000
            >>> [gene in g[1] for gene in gntc.genes]
            [True, True, True, True, True, True, True]

        """
        generation = []
        genes = self.genes.copy()
        index = self.index
        empty_coef = self.EMPTY_COEF

        for _ in range(size):
            chromosome = []

            for _ in range(gene_no):
                if random.random() > empty_coef:
                    chromosome.append(genes[index])
                    index = (index % (len(genes) - 1)) + 1
                else:
                    chromosome.append(genes[0])

            while chromosome in generation:
                chromosome = []

                for _ in range(gene_no):
                    if random.random() > empty_coef:
                        chromosome.append(genes[random.randint(1, (len(genes)-1))])
                    else:
                        chromosome.append(genes[0])

            generation.append(chromosome)

        self.index = index
        return generation

    def selection(self, values):
        """ Chooses and pair parents for creating future generation.

        Args: values (list of floats) of fitness function.
        
        Returns: paired_parents (list of floats): list of parents indeсes.

        Examples of execution:
            >>> gntc = Genetic(6)
            >>> indeces = gntc.selection([0, 0, 1, 0, 1, 1, 0])
            >>> len(indeces)
            7
            >>> [index in indeces for index in [0, 1, 2, 3, 4, 5, 6]]
            [False, False, True, False, True, True, False]

        """
        size = len(values)
        indeces = [i for i in range(size)]

        paar = random.choices(indeces, weights=values, k=2)
        while paar[0] == paar[1]:
            paar = random.choices(indeces, weights=values, k=2)

        parent_indeces = [paar.copy()]

        for _ in range(1, size//2):
            while (paar[0] == paar[1] 
                    or 
                    paar in parent_indeces
                    or 
                    paar[::-1] in parent_indeces
                    ):
                paar = random.choices(indeces, weights=values, k=2)
            
            parent_indeces.append(paar.copy())
            
        if size % 2 == 1: 
            parent_indeces.append(random.choices(indeces, weights=values, k=1))

        indeces = []
        for paar in parent_indeces:
            indeces.append(paar[0])
            try:
                indeces.append(paar[1])
            except IndexError:
                pass

        return indeces

    def crossover(self, chunk, parents, probability):
        """ Crossovers the parents in chunk to get new chunk.
        Here 2 point crossover is used.

        Args: 
            chunk (3D list of ints);
            parents (list of ints): list of parents indeces;
            probability (float): crossover probability.

        Returns: new chunk (3D list of ints).

        Examples of execution:
            >>> gntc = Genetic(5)
            >>> gnrtn = [[[1, 6], [0, 0]],\
                         [[32, 3], [16, 3]],\
                         [[4, 24], [16, 6]],\
                         [[8, 3], [8, 33]],\
                         [[16, 36], [1, 36]]]
            >>> indeces = [0, 3, 2, 4, 2]
            >>> new_gnrtn = gntc.crossover(gnrtn, indeces, 1)
            >>> variety = [[1, 6], [0, 0], [32, 3], [16, 3], [4, 24],\
                [16, 6], [8, 3], [8, 33], [16, 36], [1,36]]
            >>> [chrm in gnrtn for chrm in new_gnrtn]
            [False, False, False, False, True]
            >>> [[gene in variety for gene in chrm] for chrm in new_gnrtn]
            [[True, True], [True, True], [True, True], [True, True], [True, True]]

        """
        new_chunk = []

        for first, second in zip(parents[::2], parents[1::2]):
            self.paar_crossover(
                chunk[first], 
                chunk[second], 
                new_chunk, 
                probability
            )
        if len(parents) % 2 == 1:
            new_chrm = chunk[parents[-1]].copy()

            while new_chrm in new_chunk:
                new_chrm = self.chrm_mutation(new_chrm)

            new_chunk.append(new_chrm)

        return new_chunk

    def paar_crossover(self, a, b, new_generation, probability):
        """ Crossover the paar of the parents chromosome.

        Args:
            a (2D list): first chromosome;
            b (2D list): second chromosome;
            new_generation (3D list of ints): mutable;
            probability (float): crossover probaility.
        
        Note: New children chromosomes are unique for crossovered generation.

        Examples of execution:
            >>> gntc = Genetic(6)
            >>> chrm11 = [[1, 6], [32, 3], [8, 3], [4, 33]]
            >>> chrm12 = [[1, 34], [32, 6], [8, 6], [4, 3]]
            >>> gnrtn = []
            >>> gntc.paar_crossover(chrm11, chrm12, gnrtn, 1)
            >>> gnrtn[0].extend(gnrtn[1])
            >>> chrm_list1 = [[1, 6], [32, 3], [8, 3], [4, 33],\
                    [1, 34], [32, 6], [8, 6], [4, 3],\
                    [1, 20], [32, 12], [8, 36], [4, 9]]
            >>> [chrm in gnrtn[0] for chrm in chrm_list1]
            [True, True, True, True, True, True, True, True, False, False, False, False]

        """
        # Initiating child chromosomes
        new_ab = a.copy()
        new_ba = b.copy()
        size = len(new_ab)

        if random.random() < probability:
            crossover_len = random.randint(1, size-1)
            point_a = random.randint(0, size-crossover_len)
            point_b = random.randint(0, size-crossover_len)

            new_ab[point_a : point_a+crossover_len]\
                = b[point_b : point_b+crossover_len].copy()

            new_ba[point_b : point_b+crossover_len]\
                = a[point_a : point_a+crossover_len].copy()
        
        while new_ab in new_generation:
            new_ab = self.chrm_mutation(new_ab)
            
        while new_ba in new_generation:
            new_ba = self.chrm_mutation(new_ba)

        new_generation.append(new_ab.copy())
        new_generation.append(new_ba.copy())

    def chrm_mutation(self, chromosome):
        """ Mutation of the single chromosome.

        Args: chromosome (2D list of ints)

        Returns: mutated chromosome (2d list of ints)

        Examples of execution:
            >>> gntc = Genetic(6)
            >>> chrm1 = [[16, 3], [1, 6], [0, 0]]
            >>> chrm2 = [[16, 3], [1, 6], [0, 0]]
            >>> chrm1 == chrm2
            True
            >>> mutated_chrm = gntc.chrm_mutation(chrm1)
            >>> chrm1 == chrm2
            True
            >>> mutated_chrm == chrm1
            False
            >>> len(mutated_chrm)
            3
            >>> [len(gene) == 2 for gene in mutated_chrm]
            [True, True, True]
        
        """
        chrm = [[c, s] for c, s in chromosome]
        genes = self.genes.copy()
        index = self.index
        top = len(chromosome) - 1
 
        while chrm == chromosome:
            if random.random() > self.EMPTY_COEF:
                chrm[random.randint(0, top)] = genes[index]
                index = (index % (len(genes) - 1)) + 1

            else:
                chrm[random.randint(0, top)] = genes[0]

        self.index = index
        return chrm

    def mutation(self, generation, probability):
        """ Mutate the chromosomes in generation.

        Args: 
            generation (3D list of ints);
            probability (float): mutation probability.

        Note: 
            The pobability in range (0, 1].
            Usually mutation probability is at least 
            10-times smaller than crossover probability.

        Examples of execution:
            >>> gntc = Genetic(6)
            >>> gnrtn = [[[1,6], [32, 3]], [[8, 6], [16, 10]]]
            >>> gnrtn_copy = [[[1,6], [32, 3]], [[8, 6], [16, 10]]]
            >>> gnrtn == gnrtn_copy
            True
            >>> mutated = gntc.mutation(gnrtn, 1)
            >>> gnrtn == gnrtn_copy
            False
            >>> mutated == gnrtn_copy
            False
            >>> mutated == gnrtn
            True
            >>> [chrm in gnrtn_copy[0] for chrm in gnrtn[0]]
            [False, False]
            >>> [chrm in gnrtn_copy[1] for chrm in gnrtn[1]]
            [False, False]
            >>> len(gnrtn) == len(gnrtn_copy)
            True


        """
        for chromosome in generation:
            if random.random() < probability:
                new_chromosome = self.chrm_mutation(chromosome.copy())
                generation.remove(chromosome)

                while new_chromosome in generation:
                    new_chromosome = self.chrm_mutation(new_chromosome)

                generation.append(new_chromosome)

        return generation

if __name__ == '__main__':
    import doctest
    doctest.testmod()