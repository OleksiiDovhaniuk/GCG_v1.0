import genetic_algorithm as gntc
import file_work         as fw

from fitness_function    import generation_result
from numpy               import array
from datetime            import datetime
from pandas              import DataFrame

class Process():
    def __init__(self):
        start_time      = self.start_time = datetime.now()
        self.pause_time = start_time - start_time

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
        have_result           = False

        generation = gntc.create_generation(generation_size, 
                                            chromosome_size, 
                                            len(inputs))
        # ff: fitness function
        ff_results = generation_result(generation, 
                                    inputs, 
                                    outputs, 
                                    coefs) # [alpha, betta, gamma, lambda]

        columns = ['chromosome', # DataFrame columns
                   'value',      # fitness function value
                   'time',]      # search time

        data    = []             # DataFrame data 

        self.time = datetime.now() - (start_time + self.pause_time)
        # add best N (N = memorised_number) chromosome to the DataFrame data of the best results 
        for _ in range(memorised_number):
            max_ff    = -1
            index_max = -1
            for index, value in enumerate(ff_results):
                if value > max_ff:
                    index_max = index 
                    max_ff    = value
            data.append([generation[index_max], max_ff, self.time])

            generation.pop(index_max)
            ff_results.pop(index_max)

        # serach for the appropiate chromosomes
        index = 0
        value = data[index][1]
        data_proper = [] # DataFrame data of proper chromosomes
        while value > alpha:
            data_proper.append(data[index])
            have_result = True
            index += 1


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
        self.best_results          = DataFrame(columns=columns, data=data)
        self.proper_results        = DataFrame(columns=columns, data=data_proper)
        self.have_result           = have_result
        self.columns               = columns
        
        self.time      = datetime.now() - start_time 
        str_time       = '0' + str(self.time)[:7] 
        max_value      = round(data[0][1], 6)
        self.message   = f'Process time {str_time}, the best result: {max_value}'
        self.flag_time = datetime.now()
        self.int_time  = int(round(self.time.total_seconds(), 0))
    
    def do_loop(self):
        best_results          = self.best_results
        proper_results         = self.proper_results
        ff_results            = self.ff_results
        generation            = self.generation
        generation_size       = self.generation_size
        crossover_probability = self.crossover_probability
        mutation_probability  = self.mutation_probability
        inputs                = self.inputs
        outputs               = self.outputs
        coefs                 = self.coefs
        alpha                 = self.coefs[0]
        start_time            = self.start_time
        memorised_number      = self.memorised_number
        configurations        = self.configurations
        truth_table           = self.truth_table
        have_result           = self.have_result
        columns               = self.columns


        # restore "stolen" chromosome back to generation
        ff_results.extend(best_results['value'].tolist())
        generation.extend(best_results['chromosome'].tolist())
        while len(generation) > generation_size:
            min_ff    = 99
            index_min = -1
            for index, value in enumerate(ff_results):
                if value < min_ff: index_min = index 

            generation.pop(index_min)
            ff_results.pop(index_min)
        
        # body of genetic algorithm process
        paired_parents = gntc.roulette_selection(ff_results)
        generation     = gntc.crossover(generation, 
                                        paired_parents, 
                                        crossover_probability)
        ff_results     = generation_result(generation, 
                                           inputs, 
                                           outputs, 
                                           coefs)

        # updating dictionary of the best chromosomes
        self.time = datetime.now() - (start_time + self.pause_time)
        top       = len(best_results.index) - 1
        count     = 0
        for index, value in enumerate(ff_results):
            if (value >= alpha and 
                generation[index] not in proper_results['chromosome'].tolist()):

                have_result    = True
                proper_results = proper_results.append([value, 
                                                      generation[index], 
                                                      self.time])

            if (value > best_results['value'].tolist()[top] and 
                count < memorised_number):
                
                best_results = best_results.drop([top])
                data         = best_results.values.tolist()
                data.append([generation[index], value, self.time])
                best_results = DataFrame(columns=columns,
                                         data=data)
                best_results = best_results.sort_values(by='value', 
                                                        ascending=False)

                generation.pop(index)
                ff_results.pop(index)

                count += 1

        # save results to a folder in new txt-file
        if have_result:
            proper_results = proper_results.sort_values(by='value',
                                                        ascending=False)
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
        max_value_rounded = round(best_results['value'].tolist()[0], 6)
        self.message      = f'Process time {str_time}, the best result: {max_value_rounded}'
        self.int_time = int(round(self.time.total_seconds(), 0))
        