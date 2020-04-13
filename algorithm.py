import random 
from timeit import timeit


class Genetic():
    """ Contain all ginetic algorithm stages

    Each function of the modul represent stage of genetic algorithm.

    Functions: 
        __init__(sgn_no)
        create_generation(size, gene_no),
        selection(values),
        point2_crossover(generation, indeces, probability),
        mutation(generation, mutation_probability)

    """
    EMPTY_COEF = .3

    def __init__(self, sgn_no):
        """ Creating list of all existing genes for current number of signals.

        Args: 
            sgn_no (int): number of inputs/outputs in truth table.

        """
        element = [0 for _ in range(sgn_no)]
        genes = [element]

        for i in range(sgn_no):
            element[i] = 2

            for j in range(sgn_no):
                if not element[j]: 
                    element[j] = 1

                    for k in range(j, sgn_no):
                        if not element[k]:
                            element[k] = 1
                            genes.append(element.copy())
                            element[k] = 0

                    element[j] = 0

            element[i] = 0
        
        self.genes = genes
        self.index = 1

    def create_generation(self, size, gene_no):
        """ Create generation of chromosom for work with genetic algorithm.

        Args:
            size (int): number of chromosomes.
            gene_no (int): number of genes in chromosome.
            
        
        Returns:
            generation (3D list): quazy random generated 3 dimensional list.

        Note: 
            Number of alleles in gene equals number of inputs/outputs in truth table.
            Allele is int digit: 0, 1 or 2, 
            where: 
                0 - no gate input;
                1 - switching gate input;
                2 - control gate input. 

        """
        generation = []
        genes = self.genes.copy()
        index = self.index
        empty_coef = self.EMPTY_COEF

        # Filling generation with quazy approperet random elements.
        # Note: There is muximum one elementary element per gene.  
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
            self.cossover_paar(paar[0], paar[1],\
                generation, crossovered_generation, probability)

        if len(indeces[-1]) == 1:
            new_chrm = generation[indeces[-1][0]].copy()

            while new_chrm in crossovered_generation:
                new_chrm = self.chrm_mutation(new_chrm)

            crossovered_generation.append(new_chrm)
        else:
            self.cossover_paar(indeces[-1][0], indeces[-1][1],\
                generation, crossovered_generation, probability)

        self.index = index
        return crossovered_generation

    def cossover_paar(self, a, b, generation, crossovered_generation, probability):
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

# if __name__ == '__main__':
#     import doctest
#     doctest.testmod(extraglobs={'size': 12,
#                                 'gene_no': 5,
#                                 'sgn_no': 6,
#                                 'values': [.8, .85, .25, .8, .85, .25, .8, .85, .25],
#                                 'crossover_probability': .5,
#                                 'mutation_probability':  1
#                             })


# def test(): create_generation(40000, 20, 12) 

# print(timeit(test, number=1))

# size = 9000
# gene_no = 5
# sgn_no = 6
# values = [.8, .85, .5, .8, .85, .5, .8, .85, .5, .8, .85, .5, .8, .85, .5,
#         .8, .85, .5, .8, .85, .5, .8, .85, .5, .8, .85, .5, .8, .85, .5,
#         .8, .85, .5, .8, .85, .5, .8, .85, .5, .8, .85, .5, .8, .85, .5]
# crossover_probability = .5
# mutation_probability =  1

# gntc = Genetic(sgn_no)
# generation = gntc.create_generation(size, gene_no)
# indeces = gntc.selection(values)
# generation = gntc.point2_crossover(generation, indeces, crossover_probability)
# generation = gntc.mutation(generation, mutation_probability)
