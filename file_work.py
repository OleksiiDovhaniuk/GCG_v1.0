import os

class FileWork:

    def __init__(self, **kwargs):
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        rel_path_configurations = "Saves/configurations.txt"
        self.abs_file_path_configurations = os.path.join(script_dir, rel_path_configurations)
        rel_path_truthTable = "Saves/truthTable.txt"
        self.abs_file_path_truthTable = os.path.join(script_dir, rel_path_truthTable)

        self.default_inputNames = ['A_default', 'B_default']
        self.default_outputNames = ['C_default']
        self.default_inputValues = [[0, 0, 1], [0, 1, 1], [1, 0, 1], [1, 1, 1]]
        self.default_outputValues = [[0], [1], [1], [1]]
        
        self.default_generationNumber = 100
        self.default_generationSize = 1000
        self.default_genesNumber = 7
        self.default_crossingChance = 0.4
        self.default_mutationChance = 0.02
        self.default_fitnessFunctionCoefficients = [0.9 , 0.033, 0.033, 0.34]

# ------------------------------- SAVES ------------------------------------- #  
    # ------------------------- TRUTH TABLE ------------------------- #
    def save_truthTable(self, inputNames, outputNames, inputValues, outputValues):

        f = open(self.abs_file_path_truthTable, 'w')
        f.write(inputNames + '$\n')
        f.write(outputNames + '$\n')
        f.write(inputValues + '$\n')
        f.write(outputValues + '$')
        f.close()

    # ------------------------- CONFIGURATIONS ------------------------- #
    def save_configurations(self, generation_number, generation_size, 
    genes_number, crossing_chance, mutation_chance, fitnessFunction_coefficients):
        f = open(self.abs_file_path_configurations, 'w')
        f.write(generation_number + '$\n')
        f.write(generation_size + '$\n')
        f.write(genes_number + '$\n')
        f.write(crossing_chance + '$\n')
        f.write(mutation_chance + '$\n')
        f.write(fitnessFunction_coefficients + '$')
        f.close()

# ------------------------ READING FROM FILES ------------------------------------- #  
    # -------------------------TRUTH TABLE------------------------- #
    def read_truthTable(self):
        try:
            f = open (self.abs_file_path_truthTable, 'r')
            if f.mode == 'r':
                content = f.read()
            content_list = content.split('$')  
            return content_list
        except IOError:
            print('An error occured trying to read the file (truthTable.txt).')
            return None

    # ------------------------- CONFIGURATIONS ------------------------- #
    def read_configurations(self):
        try:
            f = open (self.abs_file_path_configurations, 'r')
            if f.mode == 'r':
                content = f.read()
            content_list = content.split('$')  
            return content_list
        except IOError:
            print('An error occured trying to read the file (configurations.txt).')
            return None

 # ----------------------------- GETTERS ------------------------------------- #   
    # ------------------------- TRUTH TABLE ------------------------- #
    def get_insNames(self):
        content_list = self.read_truthTable()
        try:
            return content_list[0].split(' ')
        except:  
            print('Could not return inputs names (fileWork.get_insNames()).')
            return self.default_inputNames
        
    def get_outsNames(self):
        content_list = self.read_truthTable()
        try:
            return content_list[1].split(' ')    
        except:
            print('Could not return outputs names (fileWork.get_outsNames()).')
            return self.default_outputNames
        
    def get_insValues(self):
        content_list = self.read_truthTable()
        try:
            lines_list = content_list[2][1:].split('\n')
            ins_list = []
            for x in lines_list:
                ins_list.append([int(s) for s in x.split(' ')])
            return ins_list
        except:
            print('Could not return inputs values (fileWork.get_insValues()).')
            return self.default_inputValues

    def get_outsValues(self):
        content_list = self.read_truthTable()
        try:
            lines_list = content_list[3][1:].split('\n')
            outs_list = []
            for x in lines_list:
                outs_list.append([int(s) for s in x.split(' ')])
            return outs_list
        except:
            print('Could not return output values (fileWork.get_outsValues()).')
            return self.default_outputValues

    # ------------------------- CONFIGURATIONS ------------------------- #
    def get_generationNumber(self):
        content_list = self.read_configurations()
        try:
            return int(content_list[0], 10)
        except :
            print('Could not return generation number (fileWork.get_generationNumber()).')
            return self.default_generationNumber

    def get_generationSize(self):
        content_list = self.read_configurations()
        try:
            return int(content_list[1], 10)
        except:
            print('Could not return generation size (fileWork.get_generationSize()).')
            return self.default_generationSize

    def get_genesNumber(self):
        content_list = self.read_configurations()
        try:
            return int(content_list[2], 10)
        except:
            print('Could not return genes number (fileWork.get_genesNumber()).')
            return self.default_genesNumber

    def get_crossingChance(self):
        content_list = self.read_configurations()
        try:
            return float(content_list[3])
        except:
            print('Could not return crossing chance (fileWork.get_crossingChance()).')
            return self.default_crossingChance

    def get_mutationChance(self):
        content_list = self.read_configurations()
        try:
            return float(content_list[4])
        except:
            print('Could not return mutation chance (fileWork.get_mutationChance()).')
            return self.default_mutationChance

    def get_coefficients(self):
        content_list = self.read_configurations()
        try:
            return [float(s) for s in content_list[5].split(' ')]
        except:
            print('Could not return fitness function coefficients (fileWork.get_coefficients()).')
            return self.default_fitnessFunctionCoefficients
        
# ----------------------------STRING GETTERS--------------------------------- #
    # -------------------------TRUTH TABLE------------------------- #
    def str_insNames(self):
        content_list = self.read_truthTable()
        try:
            return content_list[0]
        except:
            print('Could not return input names string type (fileWork.str_insNames()).')
            str_result = ''
            for x in self.default_inputNames:
                str_result += x
            return str_result
        
    def str_outsNames(self):
        content_list = self.read_truthTable()
        try:
            return content_list[1][1:]
        except:
            print('Could not return output names string type (fileWork.str_outsNames()).')
            str_result = ''
            for x in self.default_outputNames:
                str_result += x
            return str_result
        
    def str_insValues(self):
        content_list = self.read_truthTable()
        try:
            return content_list[2][1:]
        except:
            print('Could not return input values string type (fileWork.str_insValues()).')
            str_result = ''
            for x in self.default_inputValues:
                str_result += str(x)
            return str_result

    def str_outsValues(self):
        content_list = self.read_truthTable()
        try:
            return content_list[3][1:]
        except:
            print('Could not return output values string type (fileWork.str_outsValues()).')
            str_result = ''
            for x in self.default_outputValues:
                str_result += str(x)
            return str_result

    # -------------------------CONFIGURATIONS------------------------- #
    def str_generationNumber(self):
        content_list = self.read_configurations()
        try:
            return content_list[0]
        except:
            print('Could not return generations number string type (fileWork.str_generationNumber()).')
            return str(self.default_generationNumber)

    def str_generationSize(self):
        content_list = self.read_configurations()
        try:
            return content_list[1][1:]
        except:
            print('Could not return generations size string type (fileWork.str_generationSize()).')
            return str(self.default_generationSize)

    def str_genesNumber(self):
        content_list = self.read_configurations()
        try:
            return content_list[2][1:]     
        except:
            print('Could not return genes number string type (fileWork.str_genesNumber()).')
            return str(self.default_genesNumber)

    def str_crossingChance(self):
        content_list = self.read_configurations()
        try:
            return content_list[3][1:]
        except:
            print('Could not return crossing chance string type (fileWork.str_crossingChance()).')
            return str(self.default_crossingChance)

    def str_mutationChance(self):
        content_list = self.read_configurations()
        try:
            return content_list[4][1:]
        except:
            print('Could not return mutation chance string type (fileWork.str_mutationChance()).')
            return str(self.default_mutationChance)

    def str_coefficients(self):
        content_list = self.read_configurations()
        try:
            return content_list[5][1:]
        except:
            print('Could not return fitness function coefficiens string type (fileWork.str_coefficients()).')
            str_retult = ''
            for x in self.default_fitnessFunctionCoefficients:
                str_retult += str(x)
            return str_retult