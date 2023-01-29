from operator import indexOf
import random

# Making random chromosomes
def random_chromosome(size):
    '''
    Function Info: 
        Creating new random chromosome that given size amount. It returns Chromosome array
    '''
    return [random.randint(0, size - 1) for _ in range(size)]



def fitness(chromosome, maxfitness):
    '''
    Function Info:
        Calculating to fitness about chormosome that we send. Returns float counts between 0 - 1
    '''
    horizontal_collisions = (
        sum([chromosome.count(queen) - 1 for queen in chromosome]) / 2
    )
    diagonal_collisions = 0

    n = len(chromosome)
    left_diagonal = [0] * (2 * n - 1)
    right_diagonal = [0] * (2 * n - 1)
    for i in range(n):
        left_diagonal[i + chromosome[i] - 1] += 1
        right_diagonal[len(chromosome) - i + chromosome[i] - 2] += 1

    diagonal_collisions = 0
    for i in range(2 * n - 1):
        counter = 0
        if left_diagonal[i] > 1:
            counter += left_diagonal[i] - 1
        if right_diagonal[i] > 1:
            counter += right_diagonal[i] - 1
        diagonal_collisions += counter

    evaluation= (horizontal_collisions + diagonal_collisions)/(4*n-2)

            
    return evaluation



# Doing cross_over between two chromosomes
def PMXcrossover(x_offspring, y_offspring):
    '''
    Crossover between chormosomes. Return array that crossovered choromosome
    '''
    first_point = random.randint(0, total_lenght - 1)
    second_point = random.randint(first_point, total_lenght - 1)
    for i in range(0, first_point):
        for j in range(first_point, second_point):
            if x_offspring[i] == x_offspring[j]:
                x_offspring[i] = y_offspring[j]
            else:
                pass
    for k in range(second_point, total_lenght):
        for f in range(first_point, second_point):
            if x_offspring[k] == x_offspring[f]:
                x_offspring[k] = y_offspring[f]
            else:
                pass
    return x_offspring



def mutate(x):
    '''
    Randomly changing the value of a random index of a chromosome 
    '''
    n = len(x)
    c = random.randint(0, n - 1)
    m = random.randint(0, n - 1)
    x[c] = m
    return x



def random_pick(population, probabilities):
    '''
    Roulette-wheel selection
    '''
    populationWithProbabilty = zip(population, probabilities)
    total = sum(w for c, w in populationWithProbabilty)
    r = random.uniform(0, total)
    upto = 0
    for c, w in zip(population, probabilities):
        if upto + w >= r:
            return c
        upto += w
    assert False, "Shouldn't get here"


# Genetic algorithm
def genetic_queen(population, maxFitness):
    '''
    Genetic Algorithm
    '''
    mutation_probability = 0.1
    new_population = []
    sorted_population = []
    probabilities = []

    for n in population:
        f = fitness(n, maxFitness)
        probabilities.append(f)
        sorted_population.append([f, n])

    sorted_population.sort(reverse=True)
    # Elitism
    new_population.append(sorted_population[-1][1])  # the best gen
    new_population.append(sorted_population[0][1])  # the worst gen

    for i in range(len(population) - 2):

        chromosome_1 = random_pick(population, probabilities)
        chromosome_2 = random_pick(population, probabilities)

        # Creating two new chromosomes from 2 chromosomes
        child = PMXcrossover(chromosome_1, chromosome_2)

        # Mutation
        if random.random() < mutation_probability:
            child = mutate(child)

        new_population.append(child)
        if fitness(child, maxFitness) == maxFitness:
            break
    return new_population


# prints given chromosome
def print_chromosome(chrom, maxFitness):
    '''
    prints given chromosome
    '''
    print(
        "Chromosome = {},  Fitness = {}".format(str(chrom), fitness(chrom, maxFitness))
    )



def print_board(chrom):
    '''
    prints given chromosome board
    '''
    board = []

    for x in range(total_lenght):
        board.append(["x"] * total_lenght)

    for i in range(total_lenght):
        board[chrom[i]][i] = "Q"

    def print_board(board):
        for row in board:
            print(" ".join(row))

    print()
    print_board(board)




if __name__ == "__main__":
    POPULATION_SIZE = 500 #population count that we creating in every generation

    while True:
        # say N = 8
        total_lenght = int(input("Please enter your desired number of queens (0 for exit): "))
        
        if total_lenght == 0:
            print("You Have broked the program. ")
            break

        if total_lenght == 2 or total_lenght == 3:
            print("There isn't avaliable solution. Please enter again.")
            break

        if total_lenght<0 :
            print("Queen count can not assign negative count")
            break

        maxFitness = 0.0  # fitness count that best (optimal) solution
        
        population = [random_chromosome(total_lenght) for _ in range(POPULATION_SIZE)] #creating population.

        generation = 1
        while (
            not maxFitness in [fitness(chrom, maxFitness) for chrom in population]
        ):

            population = genetic_queen(population, maxFitness)
            if generation % 10 == 0:
                print("=== Generation {} ===".format(generation))
                print(
                    "Maximum Fitness = {}".format(
                        max([fitness(n, maxFitness) for n in population])
                    )
                )
            generation += 1

        fitnessOfChromosomes = [fitness(chrom, maxFitness) for chrom in population]

        bestChromosomes = population[
            indexOf(fitnessOfChromosomes, min(fitnessOfChromosomes))
        ]

        if maxFitness in fitnessOfChromosomes:
            print("\nSolved in Generation {}!".format(generation - 1))

            print_chromosome(bestChromosomes, maxFitness)

            print_board(bestChromosomes)