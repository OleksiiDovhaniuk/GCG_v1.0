import numpy as np

class GeneticAlgorithm():
    """
    Class that consists of all stages of genetic algorithm for 
    quantum structure circuit diagrams. 
    This class only compatible for current representation of genotype.
    """
    def createGeneration(self, insNumber, outsNumber, generation_size, genes_number, noneNode_chance):
        """ 
        Returns random generated gene generation. 
     
        Examples of execution:
        >>> g.createGeneration(insNumber_test1, outsNumber_test1, generation_size_test1, genes_number_test1, noneNode_chance_test1)
        """
        alet_list = []
        alet_list2D = []
        gene_list3D = []
        generation_list4D = []
        self.noneNode_chance = noneNode_chance

        x_len = max(insNumber, outsNumber)
        y_len = genes_number
        z_len = generation_size

        # how many elementary elements could be in one gene row. Here 3 is number of in/outputs of Fredkin element 
        element_inOuts = 3
        elementsInLine_number = x_len
        # population list for random numpy choice method
        population_list = []
        populationChance_list = []
        populetion_len = elementsInLine_number * element_inOuts
        node_chance = (1 - noneNode_chance) / populetion_len
        sum = 0
        for i in range(populetion_len):
            population_list.append(i)
            populationChance_list.append(node_chance)
            sum += node_chance
        population_list.append(populetion_len)
        populationChance_list.append(1 - sum)
        # relative list to population_list that is actual population list for gene, that is created
        population_list2D = []
        for i in range(elementsInLine_number):
            for j in range(element_inOuts):
                population_list2D.append([i+1, j])
        population_list2D.append([0, 0])

        for _ in range(z_len):
            for _ in range(y_len):
                alet_list = np.random.choice(population_list, p=populationChance_list, replace=True, size = x_len)
                for k in range(x_len):
                    alet_list2D.append(population_list2D[alet_list[k]])
                gene_list3D.append(alet_list2D)
                alet_list2D = []
            generation_list4D.append(gene_list3D)
            gene_list3D = []

        print('First generation!')
        for x in generation_list4D:
            print(str(x))
        print('-----------------')
        return generation_list4D
        
    def roulleteSelection(self, fitnessFunction_list, genes_number):
        """
        The function returns list of patents inexes for crossover the mating pool.

        Examples of execution:
        >>> g.roulleteSelection(fitnessFunction_list_test1, genes_number_test1)
        """
        parent_list = []
        length = len(fitnessFunction_list)
        roulleteWheele_list = []
        equalsCount_list = []
        for _ in range(length):
            equalsCount_list.append(0)
        max_equals = min(genes_number - 1, len(fitnessFunction_list)//2)
        # creating quasi random list of numbers relative to elements of fitnessFunction_list
        randomShot_list = np.random.random(length)

        sum = 0
        for x in fitnessFunction_list:
            sum += x

        roulletePosition = 0
        for x in fitnessFunction_list:
            roulletePosition += (x / sum)    
            roulleteWheele_list.append(roulletePosition)
        roulleteWheele_list[length-1] = 1

        for i in range(length):
            j = 0
            while randomShot_list[i] >= roulleteWheele_list[j]:
                j += 1
            while equalsCount_list[j] >= max_equals:
                if j+1 == length:
                    j = 0
                else:
                    j += 1
            equalsCount_list[j] += 1
        for i in range(length):
            x = equalsCount_list[i]
            if x != 0:
                for _ in range(x):
                    parent_list.append(i)

        return parent_list

    def pairParents(self, parent_list):
        """
        The function returns two dimensions list with 2 colomns, 
        which consists of generation paired parents. 

        Examples of execution:
        >>> g.pairParents(g.roulleteSelection(fitnessFunction_list_test1, genes_number_test1))
        """
        pairedParents_list2D = [[], []]
        half = len(parent_list)//2
        pairedParents_list2D[0] = parent_list[:half].copy()
        pairedParents_list2D[1] = parent_list[half:].copy()

        print(str(pairedParents_list2D))
        return pairedParents_list2D

    def crossing(self, generation_list4D, pairedParents_list2D, crossing_chance):
        """
        The function returns crossovered three dimensions generation list.

        Examples of execution:
        >>> g.crossing([gene_test1, gene_test2, gene_test3, gene_test8], pairedParents_list2D, crossing_chance)
        """
        crossoveredGeneration_list4D = []
        length = len(pairedParents_list2D[0])
        gene_len = len(generation_list4D[0])
        crossingChance_list = np.random.random(length)
        # create quasi random list with alet indexes, which will be points of crossing
        alet_list = []
        ind = 0
        for _ in range(length):
            if ind + 1 == gene_len:
                ind = 1
            else:
                ind += 1
            alet_list.append(ind)
        
        print(str(alet_list))

        for i in range (length):
            parents_i = pairedParents_list2D[0][i]
            parents_j = pairedParents_list2D[1][i]
            x = generation_list4D[parents_i].copy()
            y = generation_list4D[parents_j].copy()
            if crossingChance_list[i]<=crossing_chance:
                crop_len = gene_len - alet_list[i]
                for j in range (crop_len):
                    z = x[j] 
                    x[j] = y[j]
                    y[j] = z
            j = 0
            while (((x in crossoveredGeneration_list4D) or (y in crossoveredGeneration_list4D)) 
                    and (j < len(generation_list4D))):
                x = generation_list4D[parents_i].copy()
                y = generation_list4D[j].copy()
                j += 1
                crop_len = gene_len - alet_list[i]
                for k in range (crop_len):
                    z = x[k] 
                    x[k] = y[k]
                    y[k] = z

            crossoveredGeneration_list4D.append(x)
            crossoveredGeneration_list4D.append(y)


        # if number of genes in generation is not deisible by 2, 
        # than just live last parent in new generation
        if length != len(pairedParents_list2D[1]):
            crossoveredGeneration_list4D.append(pairedParents_list2D[1][length])

        for x in crossoveredGeneration_list4D:
            print(str(x))
        print('CrossoveredGeneration')
        return crossoveredGeneration_list4D

    def mutation(self, generation_list4D, mutation_chance, noneNode_chance):
        """
        The function returns three dimensions generation list with mutated genotype.
        """
        mutatedGeneration_list4D = []
        length = len(generation_list4D)
        gene_len = len(generation_list4D[0])
        # create quasi random list of numbers,
        # that should be above the given mutation chance to have mutation happening
        mutationChance_list = np.random.random(length)
        # create quasi random list of mutation points for each gene
        alet_list = np.random.randint(gene_len, size=length)

        chromosom_len = len(generation_list4D[0][0])
        element_inOuts = 3
        elementsInLine_number = chromosom_len
        # population list for random numpy choice method
        population_list = []
        populationChance_list = []
        populetion_len = elementsInLine_number * element_inOuts
        node_chance = (1 - noneNode_chance) / populetion_len
        sum = 0
        for i in range(populetion_len):
            population_list.append(i)
            populationChance_list.append(node_chance)
            sum += node_chance
        population_list.append(populetion_len)
        populationChance_list.append(1 - sum)
        # relative list to population_list that is actual population list for gene, that is created
        population_list2D = []
        for i in range(elementsInLine_number):
            for j in range(element_inOuts):
                population_list2D.append([i+1, j])
        population_list2D.append([0, 0])

        print(str(alet_list))
        print(str(mutationChance_list))
        for i in range(length):
            x = generation_list4D[i].copy()
            if mutationChance_list[i] <= mutation_chance:
                alet_part = []
                alet_part = np.random.choice(population_list, p=populationChance_list, replace=True, size = chromosom_len)
                alet_part2D = []
                for y in alet_part:
                    alet_part2D.append(population_list2D[y])
                
                x[alet_list[i]] = alet_part2D
                while x in mutatedGeneration_list4D: 
                    alet_part = []
                    alet_part = np.random.choice(population_list, p=populationChance_list, replace=True, size = chromosom_len)
                    alet_part2D = []
                    for y in alet_part:
                        alet_part2D.append(population_list2D[y])
                    
                    x[alet_list[i]] = alet_part2D

            mutatedGeneration_list4D.append(x)

        for x in mutatedGeneration_list4D:
            print(str(x))
        print('mutatedGeneration_list4D')
        return mutatedGeneration_list4D

if __name__ == '__main__':
    import doctest
    doctest.testmod(extraglobs={'g': GeneticAlgorithm(),
                                'gene_test1':   [[[1,0], [1,1], [1,2]], [[1,1], [1,0], [1,2]]],
                                'gene_test2':   [[[1,2], [2,0], [2,1]], [[1,1], [1,0], [1,2]]],
                                'gene_test3':   [[[1,2], [2,1], [2,2]], [[1,0], [1,0], [1,2]]],
                                'gene_test8':   [[[1,0], [2,1], [2,2]], [[1,0], [1,0], [1,2]]],
                                'gene_test4':   [[[1,2], [2,0], [2,1]], [[1,1], [1,0], [1,2]], [[1,1], [1,0], [1,2]], [[1,1], [1,0], [1,2]]],
                                'gene_test5':   [[[1,2], [2,0], [2,1]], [[1,1], [1,0], [1,2]], [[1,1], [1,0], [1,2]], [[1,1], [1,0], [1,2]]],
                                'gene_test6':   [[[1,2], [2,0], [2,1]], [[1,1], [1,0], [1,2]], [[1,1], [1,0], [1,2]], [[1,1], [1,0], [1,2]]],
                                'gene_test7':   [[[1,2], [2,0], [2,1]], [[1,1], [1,0], [1,2]], [[1,1], [1,0], [1,2]], [[1,1], [1,0], [1,2]]],

                                'insNumber_test1':          2, 
                                'outsNumber_test1':         1, 
                                'generation_size_test1':    4, 
                                'genes_number_test1':       2, 
                                'noneNode_chance_test1':    .3,
                                'crossing_chance':          .9,
                                
                                'pairedParents_list2D': [[0,0],[1,3]],

                                'fitnessFunction_list_test1': [.9, .3, .0, .0, .2, .11]
                                })