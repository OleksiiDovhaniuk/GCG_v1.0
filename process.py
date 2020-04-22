from datetime import datetime

from pandas import DataFrame

import file_work as fw
from algorithm import Genetic
from fitness_function import calculate


class Result():
    """A class represents the result of the algorithm process.

    Instances:
        chromosome (2d list of ints): shape = gene_no * 2
        value (float): fitness function value accordinly;
        time (float): time spended for element search;
        is_proper (bool).
    
    """
    def __init__(self, chromosome, value=None, time=None, is_proper=True):
        self.chromosome = chromosome
        self.value = value
        self.time = time
        self.is_proper = bool(is_proper)

    def __str__(self):
        if self.is_proper: 
            str_res = f'Proper genotype:'
        else: 
            str_res = 'Genotype:'

        for gene in self.chromosome:
            str_res += f'{gene}, '
        
        str_res += f'\nValue {round(self.value)};\n'
        str_res += f'Search time {self.time}.'

        return str_res

class Process():
    """The class initialies and handles the Genetic Algorithm
    calculation process; also prepares data for GUI 
    representation. The data for the class are pulled from
    the files. 

    Methods:
        create_chunk(step_size),
        end_loop(),
        do_loop(),
        do_chunk(step_size),
        regulate(x, p).
    
    """
    DELTA = (.016, .04)
    _creation_step = 100
    _loop_step = 100

    def __init__(self):
        """ First of all, pulls configurations and the truth table
        from the responsible files. Afterwords, creats 
        genetic material for the work with genetic algorithm. 

        """
        self.start_time = datetime.now()
        self.pause_time = 0
        self.have_result = False

        self.configs = configs = fw.read_configs()
        self.coefs = [
            configs.loc['alpha', 'value'],
            configs.loc['betta', 'value'],
            configs.loc['gamma', 'value'],
            configs.loc['lambda', 'value']
            ]

        truth_table = fw.read_ttbl()
        self.inputs = truth_table['inputs'].copy()
        self.outputs = truth_table['outputs'].copy()
        self.gntc = Genetic(configs.loc['gene size', 'value'])
        self.results = []
        self.bests = []

        # Y axes of the plot:
        self.maxs = [] 
        self.mins = []
        self.avgs = []
        self.iterations = []  # X axes of the plot
    
    def create_chunk(self, step_size=_creation_step):
        """The method generats chunks of the generation and 
        appends it to the existing part of the generation. 
        Size of this chunk equals step_size.

        Args: 
            step_size (int): by default step_size = _creation_step.
                It is better to do not change the argument manualy.

        Returns: 
            True if it is the last chunk of the generation,
            False - otherwise.
        """
        start = datetime.now()

        current_size = len(self.generation)
        size = self.configs['generation size']['value']
        is_last = False

        inputs = self.inputs
        outputs = self.outputs
        coefs = self.coefs
        
        if current_size + step_size > size:
            chunk = self.gntc.create(chunk, size-current_size, self.gene_no)
            is_last = True
        else:
            chunk = self.gntc.create(step_size, self.gene_no)
        
        values = calculate(chunk, inputs, outputs, coefs)
        time = datetime.now() - self.start_time - self.pause_time

        for chromosome, value in zip(chunk, values):
            if value > self.configs['alpha']['value']:
                self.results.append(Result(chromosome, value, time, True))
            else:
                self.results.append(Result(chromosome, value, time))

        _creation_step = self.regulate(_creation_step, start-datetime.now())
        return is_last

    def end_loop(self):
        """The method finishs the iteration of the Genetic Algorithm.
        Prepare data for use in upper classes of the program
        
        """
        bests_no = self.configs['memorised number']['value']
        size = self.configs['generation size']['value']
        results = self.results = sorted(self.results, key=self.results.value)[-size:]

        if self.bests:
            self.bests.extand(results[-bests_no:].copy())
            self.bests = sorted(self.bests,  key=self.best.value)[-bests_no:]
        else: 
            self.bests= results[-bests_no:].copy()

        self.maxs.append(results[-1].value)
        self.mins.append(results[0].value)
        self.avgs.append(sum([result.values for result in results]) / len(results))
        for _ in range(size):
            self.index.append(self.index[-1]+1)

    def do_loop(self):
        """This method begins the iteration of the Genetic Algorithm.
        Steps: selection, crossver and mutation are implemented here.

        """
        gntc = self.gntc
        generation = [result.chromosome for result in self.results]
        generation.extend([best.chromosome for best in self.bests])
        values = [result.value for result in self.results]  # fitness function values
        values.extend([best.value for best in self.bests])
        crossover_prob = self.configs['crossover probability']['values']
        mutation_prob = self.configs['mutation probability']['values']

        parents = gntc.selection(values)
        generation = gntc.point2_crossover(generation, values, crossover_prob)
        self.generation = gntc.mutation(generation, mutation_prob)
        
        self.results = []

    def do_chunk(self, step_size=_loop_step):
        """The method creates chunk of new results list from existing
        generation.

        Args:
            step_size (int): by default step_size = _loop_step.
                It is better to do not change the argument manualy.
        """
        start = datetime.now()

        size = len(self.generation)
        top = len(self.results)
        is_last = False

        inputs = self.inputs
        outputs = self.outputs
        coefs = self.coefs

        if top + step_size > size:
            chunk = self.generation[top:]
            is_last = True
        else:
            chunk = self.gntc.create(step_size, self.gene_no)
        
        values = calculate(chunk, inputs, outputs, coefs)
        time = datetime.now() - self.start_time - self.pause_time

        for chromosome, value in zip(chunk, values):
            if value > self.configs['alpha']['value']:
                self.results.append(Result(chromosome, value, time, True))
            else:
                self.results.append(Result(chromosome, value, time))
        
        _loop_step = self.regulate(_loop_step, start-datetime.now())
        return is_last

    def regulate(self, x, p):
        """ Change inputed x in order to fit it into 
        range - DELTA with function: x = x * (1 - A),
        where A = (2 * p - DELTA[0] - DELTA[1]) / (2 * p)

        Args:
            x (float): in result cannot be less than 1;
            p (float): it is time point in the 
                same unit (seconds) with DELTA, 
                when x can be initialised in other units.   
        
        Examples of execution:
        >>> prcs.regulate(1, .1)
        1
        >>> prcs.regulate(100, .1)
        28
        >>> prcs.regulate(28, .001)
        784
        >>> prcs.regulate(76, .04)
        76
        >>> prcs.regulate(16, .016)
        16
        """
        
        if (
            p < self.DELTA[0]
            or
            p > self.DELTA[1]
        ):
            if p == 0: p = 0.00001
            A = (2 * p - self.DELTA[0] - self.DELTA[1]) / (2 * p)

            x = int(x * (1 - A))
        
        if x == 0: 
            return 1
        else: 
            return x

__test_values__ = {'prcs': Process()}

if __name__ == '__main__':
    import doctest
    doctest.testmod(extraglobs=__test_values__)