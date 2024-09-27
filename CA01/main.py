#Called libraries
import copy
import random
import time
from numpy.polynomial import Polynomial

class CurveFittingSolve:
    possibility_crossover = 1
    possibility_mutation = 0.9
    possibility_carry = 1
    population_len = 1000

    def __init__(self, degree, number, points, maximum_coefficient, minimum_coefficient):
        self.degree = degree
        self.number = number
        self.points = points
        self.maximum_coefficient = maximum_coefficient
        self.minimum_coefficient = minimum_coefficient
        self.population = self.first_population()

    def first_population(self):
        population = []
        for _ in range(CurveFittingSolve.population_len):
            chromosome = []
            for __ in range(self.degree + 1):
                chromosome.append(random.randint(self.minimum_coefficient, self.maximum_coefficient))
            population.append([chromosome, 0])
        return population

    #This function places the points given to the class according to the coefficients in the chromosomes and shows the difference with the original answer.
    def diff(self, coefficient, degree, point):
        sum = 0
        difference = 0
        for z in enumerate(coefficient):
            sum += z[1] * (point[0] ** (degree - z[0]))
        difference = abs(sum - point[1])
        return difference

    def fitness(self, population):
        total = 0
        for chromosome in population:
            for point in self.points:
                total += self.diff(chromosome[0], self.degree, point)
            chromosome[1] = 1/ (total/(self.number) + 1)
            total = 0

    def sort_fitness(self, population):
        population.sort(key=lambda x: x[1], reverse= True)

    def crossover(self, population):
        parents, crossovering = [], []
        for chromosome in population:
            if random.random() > CurveFittingSolve.possibility_carry:
                crossovering.append(chromosome)
            else:
                parents.append(chromosome)

        for chromosome1, chromosome2 in zip(parents, parents[1:]):
            i = random.randint(0, self.degree - 1)
            child1 = chromosome1[0][0:i] + chromosome2[0][i:]
            child2 = chromosome2[0][0:i] + chromosome1[0][i:]
            crossovering.append([child1, 0])
            crossovering.append([child2, 0])
        self.fitness(crossovering)
        self.sort_fitness(crossovering)
        return crossovering

    def mutation(self, population):
        parents, mutationing = [], []
        for chromosome in population:
            if random.random() > self.possibility_mutation:
                mutationing.append(chromosome)
            else:
                parents.append(chromosome)
        for chromosome in parents:
            r = random.randint(0, len(chromosome[0]) - 1)
            chromosome[0][r] = random.randint(self.minimum_coefficient, self.maximum_coefficient)
            child = chromosome
            mutationing.append(child)
        self.fitness(mutationing)
        self.sort_fitness(mutationing)
        return mutationing

    def solving(self):
        #The numberOfGeneration variable shows the number of repetitions of the loop; In fact, if the loop is repeated more than a certain limit, we expect to find the closest answer and not repeat the loop more than that.
        numberOfGeneration = 0
        while True:
            # print(self.population)
            numberOfGeneration += 1
            random.shuffle(self.population)
            self.fitness(self.population)
            for chromosome in self.population:
                # If our problem has an answer, it will be returned in this section.
                if chromosome[1] == 1 and chromosome[0][0] != 0 and numberOfGeneration <= 1000:
                    print("The answer is:", end=' ')
                    return chromosome[0]
                #And if there is no answer or it takes a long time to find the answer, the closest answer will be returned.
                elif chromosome[1] != 1 and chromosome[0][0] != 0 and numberOfGeneration > 1000:
                    print("The closest answer in this algorithm:", end=' ')
                    return max(self.population, key=lambda x: x[:][1])[0]

            #Separate the chromosomes that have high fitness so that no operation is performed on them.
            carried_chromosomes, best_chromosome = [], copy.deepcopy(self.population)
            number_of_carried = int(CurveFittingSolve.population_len * CurveFittingSolve.possibility_carry)
            self.sort_fitness(best_chromosome)
            for i in range(number_of_carried):
                carried_chromosomes.append(best_chromosome[i])

            #crossover chromosomes.
            crossovering = self.crossover(self.population)

            crossovering = crossovering[:CurveFittingSolve.population_len - number_of_carried]

            self.population.clear()

            #Mutated chromosomes.
            self.population = self.mutation(crossovering)
            self.population.extend(carried_chromosomes)

##############################################################Test_Case_1###############################################
# degree = 5
# number = 5
# points = [[0, 1], [1, 43], [3, 1477], [5, 10231], [7, 37969]]

###############################################################Test_Case_2##############################################
#Test_Case_2
# degree = 4
# number = 5
# points = [[0, 3], [1, 12], [-1, 0], [2, 69], [-2, -15]]

################################################################Test_Case_3#############################################
degree = 5
number = 6
points = [(0, 1), (1, 4), (-1, 10), (-2, 139), (2, -161), (-3, 1024)]


maximum_coefficient = 10
minimum_coefficient = -10
t1 = time.time()
curvefit = CurveFittingSolve(degree, number, points, maximum_coefficient, minimum_coefficient)
answerList = curvefit.solving()
t2 = time.time()
answerList.reverse()
print(Polynomial(answerList))
print(f"The time is: {t2 - t1}")