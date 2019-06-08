import numpy as np
import random

from fitness_function import generation_result

class GeneticAlgorithm():
    """
    Class that consists of all stages of genetic algorithm for 
    quantum structure circuit diagrams. 
    This class only compatible for current representation of genotype.
    """
    def createGeneration(self, insNumber, outsNumber, generation_size, genes_number):
        """ 
        Returns random generated gene generation. 
     
        """
        z_len = max(insNumber, outsNumber)
        y_len = genes_number
        x_len = generation_size

        # how many elementary elements could be in one gene row. Here 3 is number of in/outputs of Fredkin element 
        element_inOuts = 3
        elementsInRow_number = x_len
        max_el_in_row = z_len // 3

        # create and fill with [0,0] elements empty generation
        generation_list4D = []
        for _ in range(x_len):
            gene_list3D = []
            for _ in range(y_len):
                alet_list2D = []
                for _ in range(z_len):
                    alet_list2D.append([0, 0])
                gene_list3D.append(alet_list2D)
            generation_list4D.append(gene_list3D)

        # fill generation with properet random elements            
        for x in generation_list4D:
            for y in x:
                el_in_row = random.randint(0, max_el_in_row)
                check_list = []
                for i in range(el_in_row):
                    for j in range(3):
                        index = random.randint(0, z_len - 1)
                        while index in check_list:
                            if index + 1 < z_len:
                                index += 1
                            else:
                                index = 0
                        y[index] = [i + 1, j]
                        check_list.append(index)

        return generation_list4D
        
    def roulleteSelection(self, fitnessFunction_list, genes_number):
        """
        The function returns list of patents inexes for crossover the mating pool.

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

        """
        pairedParents_list2D = [[], []]
        half = len(parent_list)//2
        pairedParents_list2D[0] = parent_list[:half].copy()
        pairedParents_list2D[1] = parent_list[half:].copy()

        # print(str(pairedParents_list2D))
        return pairedParents_list2D

    def crossing(self, generation_list4D, pairedParents_list2D, crossing_chance):
        """
        The function returns crossovered three dimensions generation list.

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
        
        # print(str(alet_list))

        for i in range (length):
            parents_i = pairedParents_list2D[0][i]
            parents_j = pairedParents_list2D[1][i]
            x = generation_list4D[parents_i].copy()
            y = generation_list4D[parents_j].copy()
            if crossingChance_list[i] <= crossing_chance:
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
            parents_i = pairedParents_list2D[1][length]
            x = generation_list4D[parents_i].copy()
            crossoveredGeneration_list4D.append(x)

        return crossoveredGeneration_list4D

    def mutation(self, generation_list4D, mutation_chance):
        """
        The function returns three dimensions generation list with mutated genotype.
        """
        mutatedGeneration_list4D = generation_list4D.copy()
        x_len = len(generation_list4D)
        y_len = len(generation_list4D[0])
        z_len = len(generation_list4D[0][0])
        max_el_in_row = z_len // 3
        # create quasi random list of numbers, ...
        # ... that should be above the given mutation chance to have mutation happening
        mutationChance_list = np.random.random(x_len)
        # create quasi random list of mutation points for each gene
        alet_list = np.random.randint(y_len, size=x_len)

        for i in range(x_len):
            x = generation_list4D[i]
            if mutationChance_list[i] <= mutation_chance:
                y = x[alet_list[i]]
                for j in range(z_len):
                    y[j] = [0,0]
                el_in_row = random.randint(0, max_el_in_row)
                check_list = []
                for p in range(el_in_row):
                    for q in range(3):
                        index = random.randint(0, z_len - 1)
                        while index in check_list:
                            if index + 1 < z_len:
                                index += 1
                            else:
                                index = 0
                        y[index] = [p + 1, q]
                        check_list.append(index)
        
        return mutatedGeneration_list4D