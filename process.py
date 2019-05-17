from geneticAlgorithm import GeneticAlgorithm
from calculation import Calculation

class Process:
    def __init__(self, generations_number, insNumber, outsNumber, emptyInputs_value, generation_size, genes_number, noneNode_chance,
        crossing_chance, mutation_chance, ins_list, outs_list, fitness_coefs):
        self.generations_number = generations_number
        self.insNumber = insNumber
        self.outsNumber = outsNumber
        self.emptyInputs_value = emptyInputs_value
        self.generation_size = generation_size
        self.genes_number = genes_number
        self.fitness_coefs = fitness_coefs
        self.generation = None
        self.fitnessFunction = 0
        self.current_averageResult = 0
        self.winnerGenes_list = []
        self.winnerResults_list = []
        self.ins_list = ins_list
        self.outs_list = outs_list
        self.noneNode_chance = noneNode_chance
        self.crossing_chance = crossing_chance
        self.mutation_chance = mutation_chance
        self.winnerGene = None
        self.winnerResult = None

        if generations_number <= 100:
            self.step = 1
        else:
            self.step = generations_number // 100

    def go(self):
        fitness_coefs = self.fitness_coefs
        cal = Calculation(fitness_coefs[0], fitness_coefs[1], fitness_coefs[2], fitness_coefs[3])
        GenAlg = GeneticAlgorithm()
        generation = self.generation

        # If it is the first iteration of algorithm, than randeom create generation
        if generation is None: 
            generation = GenAlg.createGeneration(self.insNumber, self.outsNumber, self.generation_size, self.genes_number, self.noneNode_chance)

        results = cal.getGenerationResuls(generation, self.ins_list, self.outs_list, self.emptyInputs_value)
        for i in range(len(results)):
            # save results that is sutable for current experiment
            if results[i] > fitness_coefs[0]:
                self.winnerGenes_list.append(generation[i]) 
                self.winnerResults_list.append(results[i])
        else:
            # body of genetic algorithm process
            selection = GenAlg.roulleteSelection(results, self.genes_number)
            # pair_list = GenAlg.pairParents_byDifference(selection, generation)
            pair_list = GenAlg.pairParents(selection)
            generation = GenAlg.crossing(generation, pair_list, self.crossing_chance)
            # print(str(generation))
            generation = GenAlg.mutation(generation, self.mutation_chance, self.noneNode_chance)
            

        # find average fitness function value of current generation
        sum = 0
        for i in range(len(results)):
            sum += results[i]
        average_result = sum / len(results)
        self.current_averageResult = average_result
        
        # global generation changes to next step generation
        self.generation = generation
        # print(str(pair_list))

    def set_winnerResult(self):
        # find the best result from suitable results list, if such exists
        if self.winnerResults_list:
            self.winnerResult = self.winnerResults_list[0]
            for x in self.winnerResults_list:
                if x > self.winnerResult:
                    self.winnerResult = x 
                    x_ind = self.winnerResults_list.index(x)
                    self.winnerGene =  self.winnerGenes_list[x_ind]