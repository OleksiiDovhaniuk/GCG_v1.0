""" Contain all ginetic algorithm stages

Each function of the modul represent stage 
if genetic algorithm.

Functions: 
    create_generation(size, genes_number, in_out_number),
    roullete_selection(fitness_function_values),
    crossover(generation, paired_parents, crossover_probability),
    mutation(generation, mutation_probability)

"""
import random

def create_generation(size, genes_number, in_out_number):
    """ Create generation of chromosom for work with genetic algorithm.

    Args:
        size (int): number of chromosomes.
        genes_numbers (int): number of genes in chromosome.
        in_out_number (int): number of inputs/outputs in truth table.
    
    Returns:
        generation (4D list): quazy random generated 4 dimensional list.

    Note: 
        Number of alets is equal to number of inputs/outputs in truth.
        Alet is look like [n (int), m (int)], 
        where n is logic element index (n >= 0),
        m index of input on that element (0 <= m < 3). 

    # >>> create_generation(size, genes_number, in_out_number)

    """
    # set maximal number of logic elements in row
    max_elements_in_row = in_out_number // 3
    # create empty generation (alet: [0,0])
    generation = [[[[0,0] for _ in range(in_out_number)] \
        for _ in range(genes_number)] for _ in range(size)]
        
    # fill generation with properet random elements            
    for chromosome in generation:
        for gene in chromosome:
            # set currnet number of logic elements in row
            elements_in_row = random.randint(0, max_elements_in_row)
            check_list = []
            for element_index in range(elements_in_row):
                for input_index in range(3):
                    index = random.randint(0, in_out_number - 1)
                    while index in check_list:
                        if index + 1 < in_out_number:
                            index += 1
                        else:
                            index = 0
                    gene[index] = [element_index + 1, input_index]
                    check_list.append(index)
    return generation

def roulette_selection(fitness_function_values):
    """ Chooses and pair parents for creating future generation.

    Args: fitness_function_values (list of float).
    
    Returns: paired_parents (2D list): list of parents indexes.

    Note: 
        Sizes of fitness_function_values, parents and 
        generation(if take chromosome as one element) are equal.

    #  >>> roullete_selection(ff_values)

    """
    # define length for fitness_function_values and parents
    length =  len(fitness_function_values)
    # create list for random selection on roullete wheel
    random_shots = [random.uniform(0, 1) for _ in range(length)]  
    # create roullete wheel (list)
    roullete_wheel = [value/sum(fitness_function_values) \
        for value in fitness_function_values]
    for sector_ind in range(1, length):
        roullete_wheel[sector_ind] += roullete_wheel[sector_ind - 1]
    roullete_wheel[length-1] = 1
    # create parents list
    parents = [-1 for _ in range(length)]
    for shot_ind, shot in enumerate(random_shots):
        for sector_ind, sector in enumerate(roullete_wheel):
            if shot <= sector:
                parents[shot_ind] = sector_ind
                break
    # pair parents
    half_len = length // 2
    parents.sort()
    paired_parents = [[parents[index], parents[-(index+1)]] \
        for index in range(half_len)]
    return paired_parents

def crossover(generation, paired_parents, crossover_probability):
    """ Crossover the parents in generation to get new generation.

    Args: 
        generation (4D list).
        paired_parents (2D list): list of parents indexes.
        crossover_probability (float).
    
    Returns: crossovered_generation (4D list): 
        new generation after crossover.

    Note: 
        Current generation should be inmutable 
        on any stages of genetic algorithm.
        Crossover probability in range (0, 1].

    # >>> crossover(create_generation(size, genes_number, in_out_number),\
    #      roullete_selection(ff_values), crossover_probability)
    """
    # define max number of crossovers
    max_crossovers =  len(paired_parents)
    # define max value of crossover point
    max_crossover_point = len(generation[0]) - 1
    # copy chromosomes for integrity of global variables  
    crossovered_generation = [chromosome for chromosome in generation]
    # create list of crossover chances for each pair of parents
    random_shots = [random.uniform(0, 1) for _ in range(max_crossovers)] 
    # create list of crossover points for each pair of parents
    crossover_points = [(index % max_crossover_point) + 1 \
        for index in range(0, max_crossovers)]
    # crossover the generation
    for pair_ind, pair in enumerate(paired_parents):
        if (random_shots[pair_ind] <= crossover_probability
                and pair[0] != pair[1]):
            # split parents into L and R parts
            point = crossover_points[pair_ind]
            child0 = [gene for gene in generation[pair[0]][:point]]
            parent0_r = [gene for gene in generation[pair[0]][point:]]
            child1 = [gene for gene in generation[pair[1]][:point]]
            parent1_r = [gene for gene in generation[pair[1]][point:]]
            # marge parents into new child chromosome
            child0.extend(parent1_r)
            
            child1.extend(parent0_r)
            # if chromosomes are new, set tham to new generation
            if child0 not in crossovered_generation:
                crossovered_generation[pair[0]] = [gene for gene in child0]
            if child1 not in crossovered_generation:
                crossovered_generation[pair[1]] = [gene for gene in child1]

    return crossovered_generation

def mutation(generation, mutation_probability):
    """ Mutate the chromosomes in generation.

    Args: 
        generation (4D list).
        mutation_probability (float).
    
    Returns: mutated_generation (4D list): 
        new generation after mutation.

    Note: 
        Current generation should be inmutable 
        on any stages of genetic algorithm.
        Mutation probability in range (0, 1]. Usually 
        mutation_probability is at least 10-times smaller
        than crossover_probability.

    # >>> mutation(create_generation(size, genes_number, in_out_number),\
    #         mutation_probability)
    """
    # define max value of mutation point
    max_mutation_point = len(generation[0]) - 1 
    # define gene size
    gene_size = len(generation[0][0])
    # set maximal number of logic elements in row
    max_elements_in_row = gene_size // 3
    # copy chromosomes for integrity of global variables 
    mutated_generation = [chromosome for chromosome in generation]
    # create list of mutation chances 
    random_shots = [random.uniform(0, 1) for _ in generation] 
    # create list of mutation points
    mutation_points = [random.randint(0, max_mutation_point) \
        for _ in generation]
    # mumtate generation
    for chromosome_ind, chromosome in enumerate(generation):
        if random_shots[chromosome_ind] <= mutation_probability:
            point = mutation_points[chromosome_ind]
            # create empty chromosome 
            mutated_chromosome = [gene for gene in chromosome]
            mutated_chromosome[point] = [[0,0] for _ in range(gene_size)]
            # fill up mutated chromosom
            elements_in_row = random.randint(0, max_elements_in_row)
            check_list = []
            for element_index in range(elements_in_row):
                for input_index in range(3):
                    index = random.randint(0, gene_size - 1)
                    while index in check_list:
                        if index + 1 < gene_size:
                            index += 1
                        else:
                            index = 0
                    mutated_chromosome[point][index] = \
                        [element_index + 1, input_index]
                    check_list.append(index)
            # if mutated cromosome is new, insert new generation
            if mutated_chromosome not in mutated_generation:
                mutated_generation[chromosome_ind] = \
                    [gene for gene in mutated_chromosome]
    return mutated_generation

if __name__ == '__main__':
    import doctest
    doctest.testmod(extraglobs={'size':             2,
                                'genes_number':     5,
                                'in_out_number':    7,
                                'ff_values':        [.8, .85],
                                'crossover_probability': 1,
                                'mutation_probability':  1
                               })