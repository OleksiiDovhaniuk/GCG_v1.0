import datetime

from fitness_function import generation_result
import genetic_algorithm as gntc
from file_work import FileWork

file_work = FileWork()

generations_number = None
generation_size = None
chromosome_size = None
crossover_chance = None
mutation_chance = None
inputs = None
outputs = None
coefs = None
progress_step = None
start_time = None


# genetic algorithm objects (mutable)
is_process = None
is_paused = None
is_finished = None
generation = None
ff_results = None
max_ff =  None
average_ff =  None
min_ff =  None
max_ffs =  None
average_ffs =  None
min_ffs =  None
absolute_max_ff = None
absolute_min_ff = None
best_chromosome =  None
iteration = None
time = None
time_to_find = None
results = None

        
def new_start():
    """ Sets up all parameters of genetic algorithm process.

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
    global generations_number, generation_size, chromosome_size, crossover_chance, \
        mutation_chance, inputs, outputs, coefs, progress_step, start_time
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
    start_time = datetime.datetime.now()

    global is_process, is_paused, is_finished, ff_results, generation, \
        max_ff, average_ff, min_ff, absolute_max_ff, absolute_min_ff, max_ffs, \
        average_ffs, min_ffs, best_chromosome, results, time, time_to_find, iteration
    # bool value shows wether algorithm is in process or not
    in_process = True
    # bool value shows wether algorithm is in paused or not
    is_paused = False
    # bool value shows wether algorithm is finished or not
    is_finished = False
    # genetic algorithm objects (mutable)
    generation = gntc.create_generation(generation_size, 
        chromosome_size, len(inputs[0]))
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
    # interation
    iteration = 0
    # time atributes
    time = 0
    time_to_find = '00:00:00'
    # dictionary of results(chromosome, ff_value, time)
    results = {
        'chromosome': [],
        'fitness_function': [],
        'time': []
        }
    for index, value in enumerate(ff_results):
        if (value >= coefs[0] and 
                generation[index] not in results['chromosome']):
            results['chromosome'].append(generation[index])
            results['fitness_function'].append(value)
            results['time'].append('00:00:00')


def go():
    """ Make full iteration of genetic algorithm not included 
    generation creation and first genectic algorithm objects 
    setting up.

    """
    global ff_results, generation, max_ff, average_ff, min_ff, \
        absolute_max_ff, absolute_min_ff, max_ffs, average_ffs, min_ffs, \
        best_chromosome, results, time, time_to_find, iteration

    # increase iteration
    iteration += 1
    # body of genetic algorithm process
    paired_parents = gntc.roulette_selection(ff_results)
    generation = gntc.crossover(generation, paired_parents, crossover_chance)
    generation = gntc.mutation(generation, mutation_chance)
    ff_results = generation_result(generation, inputs, outputs, coefs)
    # set process_time
    time = '0' + str(datetime.datetime.now() - start_time)[:7]
    # set absolute fitness function values
    max_ff =  max(ff_results)
    if max_ff > absolute_max_ff: 
        absolute_max_ff =  max_ff
        best_chromosome =  generation[ff_results.index(max_ff)]
        time_to_find = time
    average_ff =  sum(ff_results) / len(ff_results)
    min_ff =  min(ff_results)
    if min_ff < absolute_min_ff:
        absolute_min_ff =  min_ff
    # set average fitness function values
    max_ffs.append(max(ff_results))
    average_ffs.append(average_ff)
    min_ffs.append(min(ff_results))
    # set test values
    # if iteration == 10:
    #     for chromosome_ind, chromosome in enumerate(generation_test):
    #         generation[chromosome_ind] = chromosome
    # add new results if exist
    for index, value in enumerate(ff_results):
        if (value >= coefs[0] and 
                generation[index] not in results['chromosome']):
            results['chromosome'].append(generation[index])
            results['fitness_function'].append(value)
            results['time'].append(time)

def resume_time():
    global start_time
    start_time = datetime.datetime.now()