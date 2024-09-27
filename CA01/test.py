from random import *
from time import time


class Genetic:
    def __init__(self, n, lowLim, highLim, numPopulation, crossoverRate, mutationRate, numIteration, *points) -> None:
        self.order = n
        self.domain = [lowLim, highLim]
        self.N_population = numPopulation
        self.P_cross = crossoverRate
        self.P_mut = mutationRate
        self.N_iteration = numIteration
        self.points = list(points)
        self.initial_population()

    def initial_population(self):
        self.population = []
        for i in range(self.N_population):
            Chromosome = list(randint(*self.domain)
                              for j in range(self.order + 1))
            while Chromosome[0] == 0:
                Chromosome[0] = randint(*self.domain)

            self.population.append([Chromosome, 0])

    def crossover(self):
        self.crossed = []
        for i in range(1, self.N_population, 2):
            parents = [self.population[i-1], self.population[i]]
            if random() <= self.P_cross:
                slicePoint = randint(0, self.order - 1)
                child1 = parents[0][0][:slicePoint] + \
                    parents[1][0][slicePoint:]
                child2 = parents[1][0][:slicePoint] + \
                    parents[0][0][slicePoint:]
                self.crossed.extend([[child1, 0], [child2, 0]])

            else:
                self.crossed.extend(parents)

        if self.N_population % 2:
            self.crossed.append(self.population[-1])

        self.population.clear()
        self.population = self.crossed.copy()
        self.fitness()
        self.sorter()

    def mutation(self):
        for i in range(self.N_population):
            if random() <= self.P_mut:
                slicePoint = randint(0, self.order)
                substitution = randint(*self.domain)
                while slicePoint == 0 and substitution == 0:
                    substitution = randint(*self.domain)
                self.population[i][0][slicePoint] = substitution

        self.fitness()
        self.sorter()

    def fitness(self):
        for i in range(self.N_population):
            mean_err = 0
            for pt in self.points:
                x = pt[0]
                y_estimation = 0
                for j in range(self.order + 1):
                    power = self.order - j
                    coeff = self.population[i][0][j]
                    y_estimation += coeff * x ** power
                error = abs(y_estimation - pt[1])
                mean_err += error
            mean_err /= len(self.points)
            mean_err = mean_err**(1/3)
            fit = 1/(1+mean_err)
            self.population[i][1] = fit

    def sorter(self):
        self.population = sorted(
            self.population, key=lambda x: x[1], reverse=True)

    def answer(self):
        ans, power = '   y = ', self.order
        for gene in self.population[0][0]:
            if power:
                ans += f'{gene}*x^{power} + '
            else:
                ans += f'{gene}   '
            power -= 1
        return ans

    def main(self):
        for i in range(self.N_iteration):
            self.crossover()
            self.mutation()

            if self.population[0][1] == 1:
                print(
                    f'We\'ve reached the exact answer as: {self.answer()} in #{i}th iteration.')
                return 1
        print(
            f'We couldn\'t find the perfect answer; but here\'s the best answer we could get: {self.answer()}')
        return 0


# Running the code:
start = time()

# test case 1 ----------------------------------------------------------------------------------------
# (n=1, lowLim=0, highLim=9, numPopulation=100, crossoverRate=0.1, mutationRate=0.1, numIteration=100)
Points = [(1, 2), (2, 4)]
sample = Genetic(1, 0, 9, 100, 0.1, 0.1, 100, *Points)
sample.main()

# test case 2 -------------------------------------------------------------------------------------------
# (n=2, lowLim=-10, highLim=35, numPopulation=1000, crossoverRate=0.5, mutationRate=0.5, numIteration=1000)
# Points = [(0, 10), (-1, 0), (-0.5, 0)]
# sample = Genetic(2, -10, 35, 1000, 0.5, 0.5, 1000, *Points)
# sample.main()

# test case 3 -------------------------------------------------------------------------------------------
# (n=3, lowLim=-9, highLim=9, numPopulation=1000, crossoverRate=0.5, mutationRate=0.5, numIteration=1000)
# Points = [(0, 1), (1, 0), (2, -5), (-1, -8)]
# sample = Genetic(3, -9, 9, 1000, 0.5, 0.5, 1000, *Points)
# sample.main()

# test case 4 ----------------------------------------------------------------------------
# (n=4, lowLim=0, highLim=20, numPopulation=1000, crossoverRate=0.9, mutationRate=0.8, numIteration=1000)
# Points = [(0, 1), (1, 43), (3, 1477), (5, 10231), (7, 37969)]
# sample = Genetic(4, 0, 20, 1000, 0.9, 0.8, 1000, *Points)
# sample.main()
# true answer: y = 15x^{4} +3x^{3} +18x^{2} +6x +1

# test case 5 ----------------------------------------------------------------------------
# (n=5, lowLim=-10, highLim=10, numPopulation=1000, crossoverRate=1, mutationRate=0.9, numIteration=10000)
# Points = [(0, 1), (1, 2), (-1, 12), (-2, 149), (2, -171), (-3, 1054)]
# sample = Genetic(5, -9, 9, 1000, 1, 0.9, 1000, *Points)
# sample.main()
# true answer: y = -5x^{5} -3x^{4} +9x^{2} +1

# test case 6 ----------------------------------------------------------------------------
# (n=5, lowLim=-10, highLim=10, numPopulation=1000, crossoverRate=1, mutationRate=0.9, numIteration=10000)
# Points = [(0, 1), (1, 4), (-1, 10), (-2, 139), (2, -161), (-3, 1024)]
# sample = Genetic(5, -10, 10, 1000, 1, 0.9, 10000, *Points)
# sample.main()
# true answer: y = -5x^{5} -3x^{4} +x^{3} +9x^{2} +x +1

# test case 7 ----------------------------------------------------------------------------
# (n=6, lowLim=0, highLim=5, numPopulation=1000, crossoverRate=1, mutationRate=0.9, numIteration=1000)
# Points = [(0, 0), (-1, -1), (1, 3), (-2, 48), (2, 80), (-3, 675), (3, 783)]
# sample = Genetic(6, 0, 5, 1000, 1, 0.9, 1000, *Points)
# sample.main()
# true answer: y = x^{6} +2x^{3}

# test case 8 ----------------------------------------------------------------------------
# (n=8, lowLim=-25, highLim=-10, numPopulation=1000, crossoverRate=1, mutationRate=0.9, numIteration=1000)
# Points = [(0, 0), (-1, -22), (1, -22), (-2, -5632), (2, -5632), (-3, -144342), (3, -144342), (-4, -1441792), (4, -1441792)]
# sample = Genetic(8, -23, 2, 1000, 1, 1, 1000, *Points)
# sample.main()
# true answer: y = -22x^{8}

stop = time()
print(f'runtime = {stop - start}')
