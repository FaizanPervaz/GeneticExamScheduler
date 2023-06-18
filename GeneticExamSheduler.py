# 20I0565_Faizan_Pervaz_E
import random

# Define problem parameters
N = 5  # total no of courses
K = 3  # total no of exam halls
T = 3  # total no of time slots
HOURS_PER_DAY = 6

# random conflicting pairs
conflict_pairs = [(1, 2, 2), (1, 3, 1), (3, 2, 3), (5, 1, 2), (4, 2, 1)]


# Define solution as list of tuples
# Each tuple represents an exam and contains information about its course, time slot, and exam hall
def generate_random_solution():
    solution = []
    for i in range(N):
        course = i + 1
        time_slot = random.randint(1, T)
        exam_hall = random.randint(1, K)
        solution.append((course, time_slot, exam_hall))
    # print(solution)
    return solution


# Define fitness function
def evaluate_fitness(solution):
    fitness = 0
    hall_hours = [0] * K
    conflicts = set()
    for i in range(N):
        course_i, time_slot_i, hall_i = solution[i]
        hall_hours[hall_i - 1] += 3
        for j in range(i + 1, N):
            course_j, time_slot_j, hall_j = solution[j]
            if course_i == course_j:
                continue
            if time_slot_i == time_slot_j and (course_i, course_j) not in conflicts and (
            course_j, course_i) not in conflicts:
                conflicts.add((course_i, course_j))
                fitness += 10
            for pair in conflict_pairs:
                if course_i == pair[0] and course_j == pair[1] and time_slot_i == time_slot_j:
                    fitness += 10
    for hall_hour in hall_hours:
        if hall_hour > HOURS_PER_DAY:
            # print("Hour limit full")
            fitness += (hall_hour - HOURS_PER_DAY) * 10     #increase fitness value so that it does not get pick for solution
    print(fitness)
    return fitness


# Define genetic algorithm
def genetic_algorithm(population_size=50, tournament_size=5, crossover_prob=0.8, mutation_prob=0.1,
                      num_generations=100):
    # Initialize population
    population = [generate_random_solution() for _ in range(population_size)]
    # Main loop
    for generation in range(num_generations):
        # Selecting parents for crossover
        parents = []
        for _ in range(population_size):
            tournament = random.sample(population, tournament_size)
            parent = min(tournament, key=lambda x: evaluate_fitness(x))
            parents.append(parent)

        # crossover
        offspring = []
        for i in range(population_size // 2):
            parent1 = parents[2 * i]
            parent2 = parents[2 * i + 1]
            if random.random() < crossover_prob:
                crossover_point = random.randint(1, N - 1)
                child1 = parent1[:crossover_point] + parent2[crossover_point:]
                child2 = parent2[:crossover_point] + parent1[crossover_point:]
            else:
                child1 = parent1
                child2 = parent2
            offspring.append(child1)
            offspring.append(child2)

        # mutation
        for i in range(population_size):
            if random.random() < mutation_prob:
                mutated_gene = random.randint(0, N - 1)
                course = mutated_gene + 1
                time_slot = random.randint(1, T)
                exam_hall = random.randint(1, K)
                offspring[i][mutated_gene] = (course, time_slot, exam_hall)
                # Evaluate fitness of offspring and select next generation
                population = parents + offspring
                population = sorted(population, key=lambda x: evaluate_fitness(x))[:population_size]
                print(population)

                # print(population)

    # Return best solution found
    temp_solution = min(population, key=lambda x: evaluate_fitness(x))
    print(evaluate_fitness(temp_solution))
    return temp_solution

def local_search(solution):
    best_score = evaluate_fitness(solution)
    while True:
        # Generate all neighboring solutions
        neighbors = []  
        for i in range(len(solution)):
            for j in range(i + 1, len(solution)):
                new_solution = solution[:]
                new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
                neighbors.append(new_solution)

        # Evaluate the neighboring solutions and select the best one
        best_neighbor = solution
        for neighbor in neighbors:
            neighbor_score = evaluate_fitness(neighbor)
            if neighbor_score < best_score:
                best_neighbor = neighbor
                best_score = neighbor_score

        # If no better neighbor is found, return the current solution
        if best_neighbor == solution:
            return solution

        # Otherwise, continue with the best neighbor
        solution = best_neighbor


best_solution = genetic_algorithm()
best_solution = genetic_algorithm()
print('course, time slot, and exam hall')
print(best_solution)
print('\n')
local_solution = local_search(best_solution)
print(local_solution)

