from fitness_function import generation_result
import genetic_algorithm as gntc
from file_work import FileWork

file_work = FileWork()

# genetic algorithm configurations (immutable)
generations_number = file_work.get_generationNumber()
generation_size = file_work.get_generationSize()
chromosome_size = file_work.get_genesNumber()
crossover_chance = file_work.get_crossingChance()
mutation_chance = file_work.get_mutationChance()
inputs = file_work.get_insValues()
outputs = file_work.get_outsValues()
for row in outputs:
    for _ in range(len(inputs) - len(outputs)):
        row.append(None)
coefs = file_work.get_coefficients()
progress_step = 1 / generations_number

# genetic algorithm objects (mutable)
generation = gntc.create_generation(generation_size, 
    chromosome_size, len(inputs[0]))

# chromosome_sum1 =  [((0,0), (1,0), (0,0), (0,0), (1,2), (1,1)),
#                     ((0,0), (0,0), (0,0), (0,0), (0,0), (0,0)),
#                     ((1,0), (1,2), (0,0), (0,0), (0,0), (1,1)),
#                     ((2,2), (1,0), (1,1), (2,1), (2,0), (1,2)),
#                     ((0,0), (0,0), (0,0), (0,0), (0,0), (0,0)),
#                     ((0,0), (0,0), (0,0), (0,0), (0,0), (0,0)),
#                     ((1,2), (1,2), (1,1), (0,0), (0,0), (1,0))]
# generation[0] = chromosome_sum1

# ff: fitness function
ff_results = generation_result(generation, inputs, outputs, coefs)
max_ff =  max(ff_results)
average_ff =  sum(ff_results) / len(ff_results)
min_ff =  min(ff_results)
# ffs: list of fitness function values
max_ffs =  [max_ff]
average_ffs =  [average_ff]
min_ffs =  [min_ff]
# absolute values
absolute_max_ff = max_ff
absolute_min_ff = min_ff
# best but not necessarily satisfactory
best_chromosome =  generation[ff_results.index(max_ff)] 
# list of satisfactory chromosomes
result_chromosomes = []
for index, value in enumerate(ff_results):
    if value >= coefs[0]:
        result_chromosomes.append(generation[index])

def go():
    """ Make full iteration of genetic algorithm not included 
    generation creation and first genectic algorithm objects 
    setting up

    Works with global variables of process module:
        configurations (immutable):
            generations_number (int).
            generation_size (int).
            chromosome_size (int).
            crossover_chance (float): in range [0, 1].
            mutation_chance (float): in range [0,1].
            inputs (2D list): truth table input signals.
            outputs (2D list): truth table output signals.
            coefs (list): fitness function coeficients [α, ß, y, δ].
            progress_step (float): portion of one iteration for 
                overal progress (0, 1].
        objects (mutable):
            generation (4D list).
            ff_results (list): fitness function results.
            max_ff (float): absolute maximum of fitness 
                function values in range [0, 1].
            average_ff (float):  current average of fitness 
                function values in range [0, 1].
            min_ff (float): absolute minimum of fitness 
                function values in range [0, 1].
            max_ffs (list): maximum values of fitness function
                for all iterations.
            average_ffs (list): average values of fitness function
                for all iterations.
            min_ffs (list): minimum values of fitness function
                for all iterations.
            best_chromosome (3D list).
            result_chromosomes (4d list): list of all suitable 
                chromosom.
    """
    global ff_results, generation, max_ff, average_ff, min_ff, \
        absolute_max_ff, absolute_min_ff, max_ffs, average_ffs, min_ffs, \
        best_chromosome, result_chromosomes

     # body of genetic algorithm process
    paired_parents = gntc.roullete_selection(ff_results)
    generation = gntc.crossover(generation, paired_parents, crossover_chance)
    generation = gntc.mutation(generation, mutation_chance)
    ff_results = generation_result(generation, inputs, outputs, coefs)
    # set absolute fitness function values
    max_ff =  max(ff_results)
    if max_ff > absolute_max_ff: 
        absolute_max_ff =  max_ff
        best_chromosome =  generation[ff_results.index(max_ff)]
    average_ff =  sum(ff_results) / len(ff_results)
    min_ff =  min(ff_results)
    if min_ff < absolute_min_ff:
        absolute_min_ff =  min_ff
    # set average fitness function values
    max_ffs.append(max(ff_results))
    average_ffs.append(average_ff)
    min_ffs.append(min(ff_results))
     
    # list of satisfactory chromosomes
    for index, value in enumerate(ff_results):
        if value >= coefs[0]:
            result_chromosomes.append(generation[index])


print(generations_number)
print(generation_size)
print(chromosome_size)
print(crossover_chance)
print(mutation_chance)
for row in inputs:
    print(row)
for row in outputs:
    print(row)
print(coefs)
print(progress_step)


print(max_ff)
print(average_ff)
print(min_ff)
print(max_ffs)
print(average_ffs)
print(min_ffs)
for gene in best_chromosome:
    print(gene)
print() 