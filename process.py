from copy import deepcopy
from datetime import (
    datetime,
    timedelta,
)

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
    
    Examples of execution:
        >>> r1 = Result([[4, 33], [0, 0]])
        >>> r1.chromosome
        [[4, 33], [0, 0]]
        >>> r1.value
        >>> r1.time
        >>> r1.is_proper
        False
        >>> r2 = Result([[4, 33], [0, 0]], .5433322391, 43, True)
        >>> r2.chromosome
        [[4, 33], [0, 0]]
        >>> r2.value
        0.5433322391
        >>> r2.time
        43
        >>> r2.is_proper
        True

    """
    def __init__(self, chromosome, value=None, time=None, is_proper=False):
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
        
        if self.value:
            str_res += f'\nValue: {round(self.value, 5)};'
        else:
            str_res += f'\nValue: None;'

        str_res += f'\nSearch time: {self.time}.'

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

    Examples of execution:
        >>> p = Process()
        >>> p.DELTA
        (0.016, 0.04)
        >>> p._creation_step
        100
        >>> p._loop_step
        100
    
    """
    DELTA = (.016, .04)
    _creation_step = 100
    _loop_step = 100
    _creating = False
    _ending = False
    _doing = False
    _calculating = False

    def __init__(self):
        """ First of all, pulls configurations and the truth table
        from the responsible files. Afterwords, creats 
        genetic material for the work with genetic algorithm. 

        Examples of execution:
            >>> p = Process()
            >>> p.pause_time
            datetime.timedelta(0)
            >>> p.have_result 
            False
            >>> p.generation
            []
            >>> p.results
            []
            >>> p.bests
            []
            >>> p.maxs
            []
            >>> p.mins
            []
            >>> p.avgs
            []
            >>> p.indeces
            []

        """
        self.start_time = datetime.now()
        self.pause_time = timedelta()
        self.have_result = False
        self.iter = 0

        self.configs = configs = fw.read()['Algorithm']['configurations']
        self.coefs = configs['fitness function coeficients']['value']

        t_tbl =   fw.read()['Truth Table']
        self.inputs = prep_ins(
            t_tbl['inputs'],
            configs['gene size']['value']
        )
        self.outputs = prep_outs(t_tbl['outputs'])
        self.gene_no = configs['chromosome size']['value']
        self.gene_size = configs['gene size']['value']
        self.gntc = Genetic(configs['gene size']['value'])
        self.generation = []
        self.results = []
        self.bests = []

        # Y axes of the plot:
        self.maxs = [] 
        self.mins = []
        self.avgs = []
        self.indeces = []  # X axes of the plot

        self._creating = True
        self.percent = 0
    
    def create_chunk(self, step_size=_creation_step):
        """The method generats chunks of the generation and 
        appends it to the existing part of the generation. 
        Size of this chunk equals step_size.

        Args: 
            step_size (int): by default step_size = _creation_step.
                It is better to do not change the argument manualy.

        Examples of execution:
            >>> p = Process()

            >>> p.create_chunk()
            >>> p._creating
            True
            >>> len(p.results)
            100
            >>> chrms = [res.chromosome for res in p.results]
            >>> [gene in p.gntc.genes for gene in chrms[0][:5]]
            [True, True, True, True, True]
            >>> [gene in p.gntc.genes for gene in chrms[49][:5]]
            [True, True, True, True, True]
            >>> [gene in p.gntc.genes for gene in chrms[99][:5]]
            [True, True, True, True, True]

            >>> p.create_chunk(5)
            >>> p._creating
            True
            >>> len(p.results)
            105
            >>> chrms = [res.chromosome for res in p.results]
            >>> [gene in p.gntc.genes for gene in chrms[100][:5]]
            [True, True, True, True, True]
            >>> [gene in p.gntc.genes for gene in chrms[102][:5]]
            [True, True, True, True, True]
            >>> [gene in p.gntc.genes for gene in chrms[104][:5]]
            [True, True, True, True, True]

        """
        start = datetime.now()

        step_size = self._creation_step
        current_size = len(self.results)
        size = self.configs['generation size']['value']

        if current_size + step_size > size:
            chunk = self.gntc.create(size-current_size, self.gene_no)
            self._creating = False
            self._ending = True
        else:
            chunk = self.gntc.create(step_size, self.gene_no)
        
        values = calculate(
            chunk,
            self.gene_size, 
            self.inputs, 
            self.outputs, 
            self.coefs
        )
        time = datetime.now() - self.start_time - self.pause_time

        for chromosome, value in zip(chunk, values):
            if value > self.coefs[0]:
                self.results.append(Result(chromosome, value, time, True))
            else:
                self.results.append(Result(chromosome, value, time))

        self._creation_step = self.regulate(self._creation_step, (datetime.now()-start).total_seconds())

    def end_loop(self):
        """The method finishs the iteration of the Genetic Algorithm.
        Prepare data for use in upper classes of the program
        
        Examples of execution:
            >>> p = Process()
            >>> p.configs['memorised number']['value'] = 5
            >>> p.configs['generation size']['value'] = 100
            >>> p.create_chunk(999)
            >>> p._creating
            False
            >>> p.end_loop()
            >>> len(p.bests)
            5
            >>> p.results[0].value <= p.results[1].value 
            True
            >>> p.results[1].value <= p.results[49].value 
            True
            >>> p.results[49].value <= p.results[50].value
            True
            >>> p.results[50].value <= p.results[98].value
            True
            >>> p.results[98].value <= p.results[99].value
            True
            >>> p.bests[0].value <= p.bests[2].value <= p.bests[4].value
            True
            >>> p.maxs[-1] > p.avgs[-1] > p.mins[-1] 
            True
            >>> p.indeces[-1]
            0

        """
        bests_no = self.configs['memorised number']['value']
        size = self.configs['generation size']['value']
        results = self.results = sorted(self.results, key=lambda result: result.value)[-size:]

        if self.bests:
            self.bests.extend(results[-bests_no:].copy())
            self.bests = sorted(self.bests, key=lambda best: best.value)[-bests_no:]
        else: 
            self.bests= results[-bests_no:].copy()

        self.maxs.append(results[-1].value)
        self.mins.append(results[0].value)
        self.avgs.append(sum([result.value for result in results]) / len(results))
        if self.indeces:
            self.indeces.append(self.indeces[-1]+1)
        else: 
            self.indeces.append(0)
        
        self._ending = False
        self._doing = True
        self.iter += self.iter
        

    def do_loop(self):
        """This method begins the iteration of the Genetic Algorithm.
        Steps: selection, crossver and mutation are implemented here.

        Examples of execution:
            >>> p = Process()
            >>> p.configs['memorised number']['value'] = 5
            >>> p.configs['generation size']['value'] = 100
            >>> p.create_chunk(999)
            >>> p._creating
            False
            >>> p.end_loop()
            >>> len(p.results)
            100
            >>> p.do_loop()
            >>> p.results
            []
            >>> len(p.generation)
            105

        """
        gntc = self.gntc
        generation = [result.chromosome for result in self.results]
        generation.extend([best.chromosome for best in self.bests])
        values = [result.value for result in self.results]  # fitness function values
        values.extend([best.value for best in self.bests])
        crossover_prob = self.configs['crossover probability']['value']
        mutation_prob = self.configs['mutation probability']['value']


        parents = gntc.selection(values)
        self.generation = gntc.crossover(generation, parents, crossover_prob)
        gntc.mutation(self.generation, mutation_prob)
        
        self.results = []
        self._doing = False
        self._calculating = True

    def do_chunk(self, step_size=_loop_step):
        """The method creates chunk of new results list from existing
        generation.

        Args:
            step_size (int): by default step_size = _loop_step.
                It is better to do not change the argument manualy.

        Examples of execution:
            >>> p = Process()
            >>> p.configs['memorised number']['value'] = 5
            >>> p.configs['generation size']['value'] = 100
            >>> p.create_chunk(999)
            >>> p._creating
            False
            >>> p.end_loop()
            >>> p.do_loop()
            >>> len(p.results)
            0
            >>> p.do_chunk(10)
            >>> p._calculating
            True
            >>> len(p.results)
            10
            >>> p.do_chunk(50)
            >>> p._calculating
            True
            >>> len(p.results)
            60
            >>> p.do_chunk(99)
            >>> p._calculating
            False
            >>> len(p.results)
            105

        """
        start = datetime.now()

        step_size = self._loop_step
        size = len(self.generation)
        top = len(self.results)
        is_last = False

        if top + step_size > size:
            chunk = self.generation[top:]
            self._calculating = False
            self._ending = True
        else:
            chunk = self.gntc.create(step_size, self.gene_no)
        
        values = calculate(
            chunk, 
            self.gene_size,
            self.inputs, 
            self.outputs, 
            self.coefs
        )
        time = datetime.now() - self.start_time - self.pause_time

        for chromosome, value in zip(chunk, values):
            if value > self.coefs[0]:
                self.results.append(Result(chromosome, value, time, True))
            else:
                self.results.append(Result(chromosome, value, time))
        
        self._loop_step = self.regulate(self._loop_step, (datetime.now()- start).total_seconds())
        
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

    def process(self):
        """ Process the algorithm. The method regulates witch stage should
        proceed next and also when to stop process.

        """
        time_info = self.configs['process time']
        iter_info = self.configs['iterations limit']
        total_seconds = (datetime.now() - self.start_time - self.pause_time).total_seconds()
        
        if time_info['is active']:
            self.percent = int(total_seconds / time_info['value']  * 100)
            if self.percent > 100: 
                self.percent = 100
        elif iter_info['is active']:
            self.percent = int(self.iter / iter_info['value'] * 100)

        if (
            (time_info['is active'] and total_seconds< time_info['value'])
            or
            (iter_info['is active'] and self.iter < iter_info['value'])
        ):
            if self._creating: 
                self.create_chunk()
            elif self._ending:
                self.end_loop()
            elif self._doing:
                self.do_loop()
            elif self._calculating:
                self.do_chunk()
            return True
            
        else:
            return False

def prep_ins( inputs, sgn_no):
    """ Interprets input signals of the truth table
    into view that can be used by fitness_function module.

    Args: 
        inputs (dictionary);
        sgn_no int.

    Returns: list of ints.

    Examples of execution:
        >>> ins = {\
            'X':  '00001111',\
            'Y':  '00110011',\
            'C1': '01010101',\
        }
        >>> prep_ins(ins, 1)
        [0, 0, 0, 0, 1, 1, 1, 1]
        >>> prep_ins(ins, 2)
        [0, 0, 1, 1, 2, 2, 3, 3]
        >>> prep_ins(ins, 3)
        [0, 1, 2, 3, 4, 5, 6, 7]
        >>> prep_ins(ins, 4)
        [1, 3, 5, 7, 9, 11, 13, 15]
        >>> prep_ins(ins, 5)
        [2, 6, 10, 14, 18, 22, 26, 30]
        >>> prep_ins(ins, 6)
        [5, 13, 21, 29, 37, 45, 53, 61]

    """
    ins = [inputs[signal] for signal in inputs]
    size = len(ins[0])
    bynery_list = [''] * size

    for i in range(size):
        for j in range(sgn_no):
            try:
                bynery_list[i] += ins[j][i]

            except IndexError:
                bynery_list[i] += str(j % 2)

    return [int(binary, 2) for binary in bynery_list]

def prep_outs(outputs):
    """Interprets output signals of the truth table
    into view that can be used by fitness_function module.

    Args: 
        outputs (dictionary);

    Returns: nested list of ints` lists [0 or 1].

    Examples of execution:
        >>> outs = {\
            'X':  '01101001',\
            'Y':  '00010111',\
            'C1': '00111100',\
        }
        >>> prep_outs(outs)
        [[0, 0, 0],\
 [1, 0, 0],\
 [1, 0, 1],\
 [0, 1, 1],\
 [1, 0, 1],\
 [0, 1, 1],\
 [0, 1, 0],\
 [1, 1, 0]]

    """
    outs = [outputs[signal] for signal in outputs]

    return [[int(signal[i]) for signal in outs]\
        for i in range(len(outs[0]))]
        

__test_values__ = {'prcs': Process()}

if __name__ == '__main__':
    import doctest
    doctest.testmod(extraglobs=__test_values__)
