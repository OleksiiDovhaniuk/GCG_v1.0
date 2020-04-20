import random 


class Genetic():
    """ Contain all ginetic algorithm stages

    Each function of the modul represent stage of genetic algorithm.

    Args: 
        sgn_no (int): number of inputs/outputs signals coresponding
            the intputed truth table.

    Methods: 
        create(size, gene_no),
        selection(values),
        paar_crossover(a, b, generation, crossovered_generation, probability),
        point2_crossover(generation, indeces, probability),
        chrm_mutation(chromosom),
        mutation(generation, mutation_probability)

    """
    EMPTY_COEF = .3

    def __init__(self, sgn_no, control_range=(1,1)):
        """ Creating list of all existing genes for current number of signals.

        Args: 
            sgn_no (int): number of inputs/outputs in truth table.
            control_range=(1,1): tuple of two integer digits (n, m), where
                0 < n <= m and n - min number of control gates in thescheme,
                m - max number of control gates in the scheme 
                (Note: when only one number is needed n = m and m should be
                less than sgn_no - 1). 

        Examples of execution:
            >>> Genetic(0).genes
            [[0, 0]]
            >>> Genetic(1).genes
            [[0, 0]]
            >>> len(Genetic(6).genes)
            61
            >>> [x in Genetic(6).genes for x in ganes_6]
            [True, True, True, False, False, False, False]
            >>> len(Genetic(5, (1, 1)).genes)
            31
            >>> [x in Genetic(5, (1, 1)).genes for x in ganes_5_11]
            [True, True, True, False, False, False, False, False]
            >>> len(Genetic(4, (2, 6)).genes)
            7
            >>> [x in Genetic(4, (2, 6)).genes for x in ganes_4_26]
            [True, False, True, False, False, False, False]

        """
        genes = [[0, 0]]
        max_num = 2 ** sgn_no - 1

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
        Filling generation with approperet quazy random elements.

        Args:
            size (int): number of chromosomes.
            gene_no (int): number of genes in chromosome.
            
        
        Returns:
            generation (3D list): quazy random generated 3 dimensional list.

        Note.1: Number of alleles in gene equals number of inputs/outputs in truth table.

        Note.2: 
            Allele is int digit: 0, 1 or 2, where: 
                0 - NaN gate input;
                1 - switching gate input;
                2 - control gate input.

        Note.3: There is muximum one elementary element per gene.
        
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

        return parent_indeces

    def point2_crossover(self, generation, indeces, probability):
        """ Crossover the parents in generation to get new generation.

        Args: 
            generation (3D list of ints).
            indeces (list of floats): list of parents indeces.
        
        Returns: crossovered_generation (3D list of ints): 
            new generation after crossover.

        """
        crossovered_generation = []
        chrm_size = len(generation[0])
        genes = self.genes.copy()
        index = self.index
        empty_coef = self.EMPTY_COEF

        for paar in indeces[:-1]:
            self.paar_crossover(paar[0], paar[1],\
                generation, crossovered_generation, probability)

        if len(indeces[-1]) == 1:
            new_chrm = generation[indeces[-1][0]].copy()

            while new_chrm in crossovered_generation:
                new_chrm = self.chrm_mutation(new_chrm)

            crossovered_generation.append(new_chrm)
        else:
            self.paar_crossover(indeces[-1][0], indeces[-1][1],\
                generation, crossovered_generation, probability)

        self.index = index
        return crossovered_generation

    def paar_crossover(self, a, b, generation, crossovered_generation, probability):
        """ Crossover paar of parents chromosome.

        Args:
             generation (3D list of ints)
             crossovered_generation (3D list of ints) - mutable
             a (int) - an index of the first chromosome
             b (int) - an index of the second chromosome
             probability (float) - crossover probaility
        
        Note: New children chromosomes are unique for crossovered generation

        """
        # Initiating child chromosomes
        new_ab = generation[a].copy()
        new_ba = generation[b].copy()
        size = len(new_ab)

        if random.random() < probability:
            crossover_len = random.randint(1, size-1)
            point_a = random.randint(0, size-crossover_len-1)
            point_b = random.randint(0, size-crossover_len-1)

            new_ab[point_a : point_a+crossover_len]\
                = generation[b][point_b : point_b+crossover_len].copy()

            new_ba[point_b : point_b+crossover_len]\
                = generation[a][point_a : point_a+crossover_len].copy()
        
        while new_ab in crossovered_generation:
            new_ab = self.chrm_mutation(new_ab)
            
        while new_ba in crossovered_generation:
            new_ba = self.chrm_mutation(new_ba)

        crossovered_generation.append(new_ab.copy())
        crossovered_generation.append(new_ba.copy())

    def chrm_mutation(self, chromosom):
        """ Mutating a singl chromosom.

        Args: chromosom (2D list of ints)

        Returns: mutated chromosome (2d list of ints)
        
        """
        genes = self.genes.copy()
        index = self.index
        top = len(chromosom) - 1

        if random.random() > self.EMPTY_COEF:
            chromosom[random.randint(0, top)] = genes[index]
            index = (index % (len(genes) - 1)) + 1
        else:
            chromosom[random.randint(0, top)] = genes[0]

        self.index = index
        return chromosom

    def mutation(self, generation, probability):
        """ Mutate the chromosomes in generation.

        Args: 
            generation (3D list of ints).
            probability (float).
        
        Returns: mutated generation (3D list)

        Note: 
            Mutation probability in range (0, 1]. 
            Usually probability is at least 10-times smaller
            than crossover_probability.

        """
        mutated_generation = generation.copy()

        for chromosome in mutated_generation:
            if random.random() < probability:
                new_chromosome = self.chrm_mutation(chromosome.copy())
                mutated_generation.remove(chromosome)

                while new_chromosome in mutated_generation:
                    new_chromosome = self.chrm_mutation(new_chromosome)
                    index +=1

                mutated_generation.append(new_chromosome)

        return mutated_generation

__test_values__ = {
    'ganes_6': [
        [0, 0], [16, 3], [2, 5], [0, 3],
        [16, 17], [63, 63], [32, 1],
    ],
    'ganes_5_11': [
        [0, 0], [16, 3], [2, 5], [0, 3],
        [16, 17], [1, 1], [32, 1], [1, 48],
    ],
    'ganes_4_26': [
        [0, 0], [1, 6], [9, 6], [0, 3],
        [16, 17], [1, 1], [32, 1],
    ],
     
}

if __name__ == '__main__':
    import doctest
    doctest.testmod(extraglobs=__test_values__)