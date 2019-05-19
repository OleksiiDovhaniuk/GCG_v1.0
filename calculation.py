import math

class Calculation:
    """ Class that consists all functions for culculation processes.
    """
    def __init__(self, alpha, betta, delta, gamma):
        """ Constructor of class Calculation. 
        
        Setting up constans.

        Examples of execution:
        >>> c.__init__(.9, .034, .033, .033)
        """
        self.alpha = alpha
        self.betta = betta
        self.delta = delta
        self.gamma = gamma

        self.fredkin_delay = 1
        self.fredkin_quantum_cost = 5

    def k_from_error(self, error):
        """ Factor k based on number of errors in system. Return k = 1 / (errors + 1).

        Examples of execution:
        >>> c.k_from_error(0)
        1.0
        >>> c.k_from_error(24)
        0.04
        >>> c.k_from_error(49)
        0.02
        >>> c.k_from_error(99)
        0.01
        """
        k = 1 / (error + 1)
        return k

    def g_from_c(self, c):
        """ Factor g based on quantum value. Return g = exp(-((1 - (5 / c))^2)).

        Examples of execution:
        >>> c.g_from_c(5)
        1.0
        >>> c.g_from_c(10)
        0.7788007830714049
        >>> c.g_from_c(125)
        0.3978819204512047
        """
        if c == 0:
            return 0
        else:
            x = -((1 - (5 / c))**2)
            g = math.exp(x)
            return g

    def h_from_g(self, g):
        """ Factor h based on number of garbage outputs. Return h = 1 / (1 + g).

        Examples of execution:
        >>> c.h_from_g(0)
        1.0
        >>> c.h_from_g(24)
        0.04
        >>> c.h_from_g(49)
        0.02
        >>> c.h_from_g(99)
        0.01
        """
        h = 1 / (1 + g)
        return h
    
    def i_from_s(self, s):
        """ Factor i based on value of general system delay. Return i = exp(-((1 - 1 / s)^2)).

        Examples of execution:
        >>> c.i_from_s(1)
        1.0
        >>> c.i_from_s(2)
        0.7788007830714049
        >>> c.i_from_s(25)
        0.3978819204512047
        """
        if s == 0:
            return 0
        else:
            x = -((1 - 1 / s)**2)
            i = math.exp(x)
            return i

    def fitnessFunctionValue(self, alpha, errors, betta, c, gamma, g, delta, s):
        """ Return F = αK(errors) + ßG(c) + yH(g) + δI(s).

        Examples of execution:
        >>> round(c.fitnessFunctionValue(0.7, 0, 0.1, 5, 0.1, 0, 0.1, 1), 5)
        1.0
        >>> round(c.fitnessFunctionValue(0.5, 0, 0.1, 5, 0.15, 0, 0.25, 1), 5)
        1.0
        >>> round(c.fitnessFunctionValue(0.7, 24, 0.1, 125, 0.1, 99, 0.1, 25), 5)
        0.10858
        """
        f = (alpha * self.k_from_error(errors) + 
        betta * self.g_from_c(c) + 
        gamma * self.h_from_g(g) + 
        delta * self.i_from_s(s))
        return f

    def getFredkinElResolt(self, signals_list):
        """Return list from (A, B, C) => (P, Q, R) = (A, A`B - AC, A`C - AB).

        Examples of execution:
        >>> c.getFredkinElResolt([0, 0, 0])
        [0, 0, 0]
        >>> c.getFredkinElResolt([0, 0, 1])
        [0, 0, 1]
        >>> c.getFredkinElResolt([0, 1, 0])
        [0, 1, 0]
        >>> c.getFredkinElResolt([1, 0, 0])
        [1, 0, 0]
        >>> c.getFredkinElResolt([0, 1, 1])
        [0, 1, 1]
        >>> c.getFredkinElResolt([1, 0, 1])
        [1, 1, 0]
        >>> c.getFredkinElResolt([1, 1, 0])
        [1, 0, 1]
        >>> c.getFredkinElResolt([1, 1, 1])
        [1, 1, 1]
        """
        A = signals_list[0]
        B = signals_list[1]
        C = signals_list[2]

        PQR = [A]
        if A == 1:
            PQR.append(C)
            PQR.append(B)
            return PQR
        else:
            return signals_list

    def getErrors(self, gene_list3D, ins_list2D, outs_list2D, emptyInputs_value):
        """ Return errors number of schemotechnical system.
   
        Examples of execution:
        >>> c.getErrors(gene_test1, ins2_1_test1, outs_OR, 0)
        1
        >>> c.getErrors(gene_test2, ins2_1_test2, outs_OR, 0)
        1
        >>> c.getErrors(gene_test1, ins2_1_test1, outs_AND, 0)
        0
        >>> c.getErrors(gene_test2, ins2_1_test2, outs_AND, 0)
        1
        >>> c.getErrors(gene_test1, ins2_1_test1, outs_NOR, 0)
        2
        >>> c.getErrors(gene_test2, ins2_1_test2, outs_NOR, 0)
        2
        >>> c.getErrors(gene_test1, ins2_1_test1, outs_NAND, 0)
        2
        >>> c.getErrors(gene_test2, ins2_1_test2, outs_NAND, 0)
        2
        >>> c.getErrors(gene_test5, insInv_test5, outsInv_test5, 1)
        1
        >>> c.getErrors(gene_test6, insInv_test6, outsInv_test6, 1)
        1
        >>> c.getErrors(gene_test7, insInv_test7, outsInv_test6, 1)
        0
        """

        genes_list3D = gene_list3D.copy()
        ins_len = len(ins_list2D[0])
        length = len(ins_list2D)
        errorsNumber_list = []
        allRez_list = []
        outputs_list2D = outs_list2D.copy()
        print('-----------------------------------------')
        print(str(gene_list3D))
        # print(str(ins_list2D))
        # print(str(outs_list2D))
        # print('ins_list2d: ' + str(ins_list2D))
        for i in range(len(ins_list2D)):
            allRez_list = []
            
            for j in range(ins_len):
                is_using = False
                for ind in range(len(genes_list3D)):
                    if genes_list3D[ind][j] != [0, 0]:
                            is_using = True
                if not is_using:
                    allRez_list.append(ins_list2D[i][j])
                    errorsNumber_list.append(0)

            activeSignals_list = ins_list2D[i].copy()
            for ind in range(len(genes_list3D)):
                x = genes_list3D[ind].copy() 
                check_list = [0]
                for j in range(len(x)):
                    indChanges_list = []
                    if x[j][0] not in check_list:
                        elementSignals_list = [emptyInputs_value] * 3
                        currentCheck = x[j][0]
                        check_list.append(currentCheck)
                        elementSignals_list[x[j][1]] = activeSignals_list[j]
                        indChanges_list.append(j)
                        for k in range(len(x)-j-1):
                            p = k + j + 1
                            if x[p][0] == currentCheck:
                                elementSignals_list[ x[p][1]] = activeSignals_list[p]
                                indChanges_list.append(p)
                        elementSignals_list = self.getFredkinElResolt(elementSignals_list)
                        # print('before: ' + str(elementSignals_list))
                        delta = 0
                        for k in range(len(indChanges_list)):
                            ind_k = indChanges_list[k]
                            ind_x = x[ind_k][1] 
                            # print(str(ind_x))
                            elementSignal = elementSignals_list[ind_x]
                            # activeSignals_list[ind_k] = elementSignals_list[x[ind_k][1]]
                            activeSignals_list[ind_k] = elementSignal
                            is_using = False
                            for r in range(len(genes_list3D) - ind - 1):
                                q = ind + r + 1
                                if genes_list3D[q][ind_k] != [0, 0]:
                                    is_using = True
                                    # print()
                            if not is_using:
                                allRez_list.append(elementSignal)
                                errorsNumber_list.append(0)

                            # print('after' +str(elementSignals_list))
                        # for y in elementSignals_list:
                        #     allRez_list.append(y)
                        #     errorsNumber_list.append(0)
                        # # print(str(activeSignals_list))

            # print(str(allRez_list))
            for x in outputs_list2D[i]:
                for k in range(len(allRez_list)):
                    if x != allRez_list[k]:
                        errorsNumber_list[k] += 1

        errorsNumber_list = errorsNumber_list[:len(allRez_list)]
        # print(str(errorsNumber_list))
        errorsNumber_min = errorsNumber_list[0]
        for x in errorsNumber_list:
            if x < errorsNumber_min:
                errorsNumber_min = x

        return errorsNumber_min

    def getDelay(self, gene_list3D, element_delay):
        """ Return delay value of system in ns.

        Examples of execution:
        >>> c.getDelay(gene_test1, 1)
        1
        >>> c.getDelay(gene_test2, 1)
        3
        >>> c.getDelay(gene_test1, 2)
        2
        >>> c.getDelay(gene_test2, 2)
        6
        """
        elemetsNumber = self.find_elementsNumber(gene_list3D)

        return elemetsNumber * element_delay
            
    def getQuantumCost(self, gene_list3D, el_quantom_cost):
        """ Return quantum value of schemotechnical system. 

        Examples of execution:
        >>> c.getQuantumCost(gene_test1, 5)
        5
        >>> c.getQuantumCost(gene_test2, 5)
        15
        >>> c.getQuantumCost(gene_test1, 2)
        2
        >>> c.getQuantumCost(gene_test2, 2)
        6
        """
        elemetsNumber = self.find_elementsNumber(gene_list3D)

        return elemetsNumber * el_quantom_cost
    
    def find_elementsNumber(self, gene_list3D):
        """ Return number of elements of schemotechnical system. 

        Examples of execution:
        >>> c.find_elementsNumber(gene_test1)
        1
        >>> c.find_elementsNumber(gene_test2)
        3
        >>> c.find_elementsNumber(gene_test3)
        0
        >>> c.find_elementsNumber(gene_test4)
        18
        """
        elementsNumber = 0

        for x in gene_list3D:
            check_list = [0] 
            for i in range(len(x)):
                if x[i][0] not in check_list:
                    check_list.append(x[i][0])
                    elementsNumber += 1

        return elementsNumber

    def getGarbageOutput(self, insNumber, outsNumber):
        """ Return number of garbage outputs/ extra inputs

        Examples of execution:
        >>> c.getGarbageOutput(3, 5)
        2
        >>> c.getGarbageOutput(2, 2)
        0
        """
        return abs(insNumber - outsNumber)

    def getGenerationResuls(self, generation_list4D, input_signals_list2D, output_signals_list2D, emptyInputs_value):
        """ Returns list of fitness function values for current generation.
        >>> round(c.getGenerationResuls([gene_test2, gene_test3], ins2_1_test1, outs_OR, 0)[0], 3)
        0.504
        >>> round(c.getGenerationResuls([gene_test2, gene_test3], ins2_1_test1, outs_OR, 0)[1], 3)
        0.461
        """
        list4D = generation_list4D
        x_len = len(list4D)
        fitnessFunction_results = []
        for i in range(x_len):
            errors = self.getErrors(list4D[i], input_signals_list2D, output_signals_list2D, emptyInputs_value)
            c = self.getQuantumCost(list4D[i], self.fredkin_quantum_cost)
            g = self.getGarbageOutput(len(input_signals_list2D[0]), len(output_signals_list2D[0]))
            s = self.getDelay(list4D[i], self.fredkin_delay)
            fitnessFunction_value = self.fitnessFunctionValue(self.alpha, errors, self.betta, c, self.gamma, g, self.delta, s) 
            fitnessFunction_results.append(fitnessFunction_value)

        return fitnessFunction_results

if __name__ == '__main__':
    import doctest
    doctest.testmod(extraglobs={'c': Calculation(.9, .034, .033, .033),
                                'gene_test1':   [[[1,0], [1,1], [1,2]]],
                                'gene_test2':   [[[1,2], [2,0], [2,1]], [[1,1], [1,0], [1,2]]],
                                'gene_test3':   [[[0,0], [0,0], [0,0]], [[0,0], [0,0], [0,0]]],
                                'gene_test4':   [[[1,0], [2,0], [3,0]], [[1,0], [3,0], [2,0]], \
                                                 [[2,0], [1,0], [3,0]], [[2,0], [3,0], [1,0]], \
                                                 [[3,0], [1,0], [2,0]], [[3,0], [2,0], [1,0]]],
                                'gene_test5':   [[[1,1], [0,0]], [[1,0], [0,0]]],
                                'gene_test6':   [[[1,1]], [[0,0]]],
                                'gene_test7':   [[[1,0], [0,0]], [[1,2], [0,0]]],
                                'ins2_1_test1': [[0,0,0], [0,1,0], [1,0,0], [1,1,0]],
                                'ins2_1_test2': [[0,0,1], [0,1,1], [1,0,1], [1,1,1]],
                                'insInv_test5': [[0, 1], [1, 1]],
                                'insInv_test6': [[0], [1]],
                                'insInv_test7': [[0, 1], [0, 0]],
                                'outsInv_test5':[[1, 1], [0, 1]],
                                'outsInv_test6':[[1], [0]],
                                'outs_OR':      [[0], [1], [1], [1]],
                                'outs_AND':     [[0], [0], [0], [1]],
                                'outs_NOR':     [[1], [0], [0], [0]],
                                'outs_NAND':    [[1], [1], [1], [0]]
                                })
