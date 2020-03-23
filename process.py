import genetic_algorithm as gntc
import file_work         as fw
from fitness_function    import generation_result
from numpy               import array
from datetime            import datetime

class Process():
    def __init__(self):
        start_time      = self.start_time = datetime.now()
        self.pause_time = start_time - start_time
        str_time        = '00:00:00'

        configurations  = fw.read_configurations()
        truth_table     = fw.read_truth_table()
       
        generation_size       = configurations['generation size'] ['value']
        chromosome_size       = configurations['chromosome size'] ['value']
        memorised_number      = configurations['memorised number']['value']
        alpha                 = configurations['alpha']           ['value']
        betta                 = configurations['betta']           ['value']
        gamma                 = configurations['gamma']           ['value']
        lamda                 = configurations['lambda']          ['value']
        coefs                 = [alpha, betta, gamma, lamda]
        inputs                = array(truth_table['inputs'] .values).T.tolist()
        outputs               = array(truth_table['outputs'].values).T.tolist()

        generation = gntc.create_generation(generation_size, 
                                            chromosome_size, 
                                            len(inputs))
        # ff: fitness function
        ff_results = generation_result(generation, 
                                    inputs, 
                                    outputs, 
                                    coefs) # [alpha, betta, gamma, lambda]
        proper_results = {'chromosome': [],
                          'value'     : [], # fitness function values
                          'time'      : []} # search time

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
            best_results['time']      .append(str_time)   

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


        self.generations_number    = configurations['iterations limit']     ['value']
        self.generation_size       = configurations['generation size']      ['value']
        self.chromosome_size       = configurations['chromosome size']      ['value']
        self.crossover_probability = configurations['crossover probability']['value']
        self.mutation_probability  = configurations['mutation probability'] ['value']
        self.info_delay            = 1
        self.iteration             = 0

        self.configurations        = configurations
        self.truth_table           = truth_table
        self.memorised_number      = memorised_number
        self.inputs                = inputs
        self.outputs               = outputs
        self.coefs                 = coefs
        self.ff_results            = ff_results # ff: fitness function
        self.generation            = generation
        self.proper_results        = proper_results
        self.best_results          = best_results
        
        self.time      = datetime.now() - start_time 
        str_time       = '0' + str(self.time)[:7] 
        self.message   = f'Process time {str_time}, the best result: {max_value_rounded}'
        self.flag_time = datetime.now()
    
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

        self.time         = datetime.now() - (start_time + self.pause_time)
        str_time  = '0' + str(self.time)[:7] 

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
                best_results['time']      .append(str_time) 

                generation.pop(index_max)
                ff_results.pop(index_max)

        # seek for the best current chromosome
        max_value_index = -1
        max_value =       -1
        for index, value in enumerate(best_results['value']):
            if value > max_value:
                max_value_index = index
                max_value       = value


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
        self.iteration     += 1

        self.time         = datetime.now() - (start_time + self.pause_time)
        str_time          = '0' + str(self.time)[:7] 
        max_value_rounded = round(max_value, 6)
        self.message      = f'Process time {str_time}, the best result: {max_value_rounded}'