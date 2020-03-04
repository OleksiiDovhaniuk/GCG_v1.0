import datetime

from fitness_function import generation_result
import genetic_algorithm as gntc
from file_work import read_configurations, read_truth_table

configurations = read_configurations()
truth_table = read_truth_table()

generations_number = configurations['iterations limit']
generation_size = configurations['generation size']
chromosome_size = configurations['chromosome size']
crossover_chance = configurations['crossover chance']
mutation_chance = configurations['mutation chance']
memorised_number = configurations['memorised number']
process_time = configurations['process time']
info_delay = configurations['info delay']
inputs = tuple(truth_table['inputs'].values())
outputs = tuple(truth_table['outputs'].values())
coefs = [0.7, 0.1, 0.1, 0.1]

inputs_str = ''
for value in inputs:
    inputs_str += '\n\t'
    inputs_str += str(value)
outputs_str = ''
for value in outputs:
    outputs_str += '\n\t'
    outputs_str += str(value)

log_config= f'''--- N E W   R U N ---
Truth Table:
    Inputs: {inputs_str}
    Outputs: {outputs_str}

Genetic Algorithm Configurations:
    Power of the Population: {generation_size}
    Chromosome Size: {chromosome_size}
    Crossover Probability: {crossover_chance}
    Mutation Probability: {mutation_chance}
    Coef-s of the Fitness Function: {coefs}
    Number of Chromosomes, which will be memorised: {memorised_number}
    Process Time: {process_time}
    Info Delay: {info_delay}
'''
print(log_config)
memorised_number = 5
start_time = datetime.datetime.now()
time_flag = datetime.datetime.now()

# genetic algorithm objects (mutable)
generation = None
ff_results = None
best_results = None
best_chromosome =  None
iteration = None
time = None
results = None

""" 
    Zero iteration - creation of the start generation
    """
# genetic algorithm objects (mutable)
generation = gntc.create_generation(generation_size, 
    chromosome_size, len(inputs))
# ff: fitness function
ff_results = generation_result(generation, inputs, outputs, coefs)
# interation
iteration = 0
# time atributes
time = '00:00:00'

# dictionary of the best results(chromosome, ff_value, time)
best_results = {
    'chromosome': [],
    'value': [],
    'time': []
    }

for _ in range(memorised_number):
    max_ff = -1
    index_max = -1
    for index, value in enumerate(ff_results):
        if value > max_ff:
            index_max = index 
            max_ff = value
    best_results['chromosome'].append(generation[index_max])
    best_results['value'].append(max_ff)
    best_results['time'].append(time)   
    generation.pop(index_max)
    ff_results.pop(index_max)

def time_delta_in_s(curent_time, start_time):
    time_delta = int(str(datetime.datetime.now() - start_time)[5:7])
    time_delta = time_delta + int(str(datetime.datetime.now() - start_time)[2:4])*60
    return time_delta        


max_value_index = -1
max_value = -1
for index, value in enumerate(best_results['value']):
    if value > max_value:
        max_value_index = index
        max_value = value
print('Process time {}, current value: {}'.format(time, round(max_value, 5)), end='\r')
if max_value > coefs[0]:
    print('An appropriate chromosome:')
    for gene in best_results['chromosome'][max_value_index]:
        print(gene) 
    print('The search time is: {}'.format(best_results['time'][max_value_index  ]))

""" 
    Make a genetic algorithm loop not included the
    generation creation and the first genectic algorithm objects 
    setting up.
    """
while time_delta_in_s(datetime.datetime.now(), start_time) <= process_time:
    # increase iteration
    iteration += 1

    ff_results.extend(best_results['value'])
    generation.extend(best_results['chromosome'])
    while len(generation) > generation_size:
        min_ff = 999
        index_min = -1
        for index, value in enumerate(ff_results):
            if value < min_ff: index_max = index 
        generation.pop(index_min)
        ff_results.pop(index_min)
    # body of genetic algorithm process
    paired_parents = gntc.roulette_selection(ff_results)
    generation = gntc.crossover(generation, paired_parents, crossover_chance)
    generation = gntc.mutation(generation, mutation_chance)
    ff_results = generation_result(generation, inputs, outputs, coefs)
    # set process_time
    time = '0' + str(datetime.datetime.now() - start_time)[:7]
    
    
    for _ in range(memorised_number):
        index_min_best = -1
        min_best_result = 999
        for index, value in enumerate(best_results['value']):
            if value < min_best_result:
                index_min_best = index 
                min_best_result = value
        max_ff = -1
        index_max = -1
        for index, value in enumerate(ff_results):
            if value > max_ff:
                index_max = index 
                max_ff = value
        if max_ff > min_best_result:
            best_results['chromosome'].pop(index_min_best)
            best_results['value'].pop(index_min_best)
            best_results['time'].pop(index_min_best)   
            best_results['chromosome'].append(generation[index_max])
            best_results['value'].append(max_ff)
            best_results['time'].append(time)   
            generation.pop(index_max)
            ff_results.pop(index_max)

    max_value_index = -1
    max_value = -1
    for index, value in enumerate(best_results['value']):
        if value > max_value:
            max_value_index = index
            max_value = value
            
    if time_delta_in_s(datetime.datetime.now(), time_flag) >= info_delay:
        print('Process time {}, current value: {}'.format(time, round(max_value, 5)), end='\r')
        if max_value > coefs[0]:
            print('An appropriate chromosome:')
            for gene in best_results['chromosome'][max_value_index]:
                print(gene)
            print('The search time is: {}'.format(best_results['time'][max_value_index]))
        time_flag = datetime.datetime.now()


max_value_index = -1
max_value = -1
for index, value in enumerate(best_results['value']):
    if value > max_value:
        max_value_index = index
        max_value = value
print('Process time {}, current value: {}'.format(time, round(max_value, 5)))
if max_value > coefs[0]:
    print('An appropriate chromosome:')
    for gene in best_results['chromosome'][max_value_index]:
        print(gene) 
    print('The search time is: {}'.format(best_results['time'][max_value_index  ]))