import genetic_algorithm as gntc
import file_work         as fw
from fitness_function    import generation_result
from numpy               import array
from datetime            import datetime

class Process():
    configurations = fw.read_configurations()
    truth_table    = fw.read_truth_table()

    generations_number    = configurations['iterations limit']     ['value']
    generation_size       = configurations['generation size']      ['value']
    chromosome_size       = configurations['chromosome size']      ['value']
    crossover_probability = configurations['crossover probability']['value']
    mutation_probability  = configurations['mutation probability'] ['value']
    memorised_number      = configurations['memorised number']     ['value']
    process_time          = configurations['process time']         ['value']
    alpha                 = configurations['alpha']                ['value']
    betta                 = configurations['betta']                ['value']
    gamma                 = configurations['gamma']                ['value']
    lamda                 = configurations['lambda']               ['value']
    inputs                = array(truth_table['inputs'] .values).T.tolist()
    outputs               = array(truth_table['outputs'].values).T.tolist()
    coefs                 = [alpha, betta, gamma, lamda]
    info_delay            = 1

    start_time = datetime.now()
    time_flag  = datetime.now()
    generation = gntc.create_generation(generation_size, 
                                        chromosome_size, 
                                        len(inputs))
    # ff: fitness function
    ff_results = generation_result(generation, 
                                   inputs, 
                                   outputs, 
                                   coefs) # [alpha, betta, gamma, lambda]
    iteration  = 0
    time       = '00:00:00'
    proper_results = {'chromosome': [],
                      'value'     : [], # fitness function values
                      'time'      : []} # search time

    def __init__(self):
        memorised_number =  self.memorised_number
        coefs =             self.coefs
        generation =        self.generation
        ff_results =        self.ff_results
        time =              self.time
        best_results = {'chromosome': [],
                        'value'     : [], # fitness function values
                        'time'      : []} # search time

        # add best N (N = memorised_number) chromosome to the dictionary of the best results 
        for _ in range(memorised_number):
            max_ff    = -1
            index_max = -1
            for index, value in enumerate(ff_results):
                if value > max_ff:
                    index_max = index 
                    max_ff    = value
            best_results['chromosome'].append(generation[index_max])
            best_results['value']     .append(max_ff)
            best_results['time']      .append(time)   

            generation.pop(index_max)
            ff_results.pop(index_max)

        # generate first info message of the process
        max_value       = -1
        max_value_index = -1
        for index, value in enumerate(best_results['value']):
            if value > max_value:
                max_value       = value
                max_value_index = index
        max_value_rounded = round(max_value, 6)
        message = f'Process time {time}, the best result: {max_value_rounded}'

        self.best_results = best_results
        self.message      = message
        
    def do_loop(self):
        best_results            = self.best_results
        ff_results              = self.ff_results
        generation              = self.generation
        generation_size         = self.generation_size
        crossover_probability   = self.crossover_probability
        mutation_probability    = self.mutation_probability
        inputs                  = self.inputs
        outputs                 = self.outputs
        coefs                   = self.coefs
        start_time              = self.start_time
        memorised_number        = self.memorised_number
        proper_results          = self.proper_results
        configurations          = self.configurations
        truth_table             = self.truth_table

        # restore "stolen" chromosome back to generation
        ff_results.extend(best_results['value'])
        generation.extend(best_results['chromosome'])
        while len(generation) > generation_size:
            min_ff      = 99
            index_min   = -1
            for index, value in enumerate(ff_results):
                if value < min_ff: index_min = index 
            generation.pop(index_min)
            ff_results.pop(index_min)
        
        # body of genetic algorithm process
        paired_parents = gntc.roulette_selection(ff_results)
        generation     = gntc.crossover(generation, 
                                        paired_parents, 
                                        crossover_probability)
        generation     = gntc.mutation(generation, 
                                       mutation_probability)
        ff_results     = generation_result(generation, 
                                           inputs, 
                                           outputs, 
                                           coefs)
        # set process_time
        time = '0' + str(datetime.now() - start_time)[:7] 

        # updating dictionary of the best chromosomes
        for _ in range(memorised_number):
            index_min_best  = -1
            min_best_result = 999
            for index, value in enumerate(best_results['value']):
                if value < min_best_result:
                    index_min_best  = index 
                    min_best_result = value

            max_ff    = -1
            index_max = -1
            for index, value in enumerate(ff_results):
                if value > max_ff:
                    index_max = index 
                    max_ff    = value

            if max_ff > min_best_result:
                best_results['chromosome'].pop(index_min_best)
                best_results['value']     .pop(index_min_best)
                best_results['time']      .pop(index_min_best)   
                
                best_results['chromosome'].append(generation[index_max])
                best_results['value']     .append(max_ff)
                best_results['time']      .append(time) 

                generation.pop(index_max)
                ff_results.pop(index_max)

        # seek for the best current chromosome
        max_value_index = -1
        max_value =       -1
        for index, value in enumerate(best_results['value']):
            if value > max_value:
                max_value_index = index
                max_value       = value

        max_value_rounded = round(max_value, 6)
        message = f'Process time {time}, the best result: {max_value_rounded}'

        # save results to a folder in new txt-file
        if proper_results['chromosome']:
            fw.autosave('Complete Proper',
                        proper_results, 
                        configurations, 
                        truth_table, 
                        start_time)
        else:
            fw.autosave('Complete Best',
                        best_results, 
                        configurations, 
                        truth_table, 

                        start_time)

        self.best_results   = best_results
        self.ff_results     = ff_results
        self.generation     = generation
        self.proper_results = proper_results
        self.message        = message
        self.iteration     += 1