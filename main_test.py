import datetime

from fitness_function import generation_result
import genetic_algorithm as gntc
from file_work import read_configurations, read_truth_table

configurations = read_configurations()
truth_table = read_truth_table()

print('Input the process time in seconds: ')
process_time = input()
generations_number = configurations['iterations limit']
generation_size = configurations['generation size']
chromosome_size = configurations['chromosome size']
crossover_chance = configurations['crossover chance']
mutation_chance = configurations['mutation chance']
inputs = tuple(truth_table['inputs'].values())
outputs = tuple(truth_table['outputs'].values())
garbage_outputs = None
delay = None
quantum_cost = None
coefs = [0.7, 0.1, 0.1, 0.1]
start_time = datetime.datetime.now()

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

""" 
    Zero iteration - creation of the start generation
    """
# genetic algorithm objects (mutable)
generation = gntc.create_generation(generation_size, 
    chromosome_size, len(inputs))
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
            results['time'].append(time_to_find)


""" 
    Make a genetic algorithm loop not included the
    generation creation and the first genectic algorithm objects 
    setting up.
    """
while time <= process_time:
#     # increase iteration
#     iteration += 1
#     # body of genetic algorithm process
#     paired_parents = gntc.roulette_selection(ff_results)
#     generation = gntc.crossover(generation, paired_parents, crossover_chance)
#     generation = gntc.mutation(generation, mutation_chance)
#     ff_results = generation_result(generation, inputs, outputs, coefs)
#     # set process_time
#     time = '0' + str(datetime.datetime.now() - start_time)[:7]
#     # set absolute fitness function values
#     max_ff =  max(ff_results)
#     if max_ff > absolute_max_ff: 
#         absolute_max_ff =  max_ff
#         best_chromosome =  generation[ff_results.index(max_ff)]
#         time_to_find = time
#     average_ff =  sum(ff_results) / len(ff_results)
#     min_ff =  min(ff_results)
#     if min_ff < absolute_min_ff:
#         absolute_min_ff =  min_ff
#     # set average fitness function values
#     max_ffs.append(max(ff_results))
#     average_ffs.append(average_ff)
#     min_ffs.append(min(ff_results))
#     # set test values
#     # if iteration == 10:
#     #     for chromosome_ind, chromosome in enumerate(generation_test):
#     #         generation[chromosome_ind] = chromosome
#     # add new results if exist
#     for index, value in enumerate(ff_results):
#         if (value >= coefs[0] and 
#                 generation[index] not in results['chromosome']):
#             results['chromosome'].append(generation[index])
#             results['fitness_function'].append(value)
#             results['time'].append(time)

# # set result_time
# result_time = '0' + str(datetime.datetime.now() - start_time)[:7]
# print('\tresult time: {}'.formta(result_time))