import random
import tkinter as tk

N = 8  

class NQueensGenetic:
    def __init__(self, population_size=100, mutation_rate=0.2, generations=1000):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.generations = generations

    def generate_random_board(self):
        return [random.randint(0, N - 1) for _ in range(N)]

    def fitness(self, board):

        non_attacking_pairs = 0
        for i in range(N):
            for j in range(i + 1, N):
                if board[i] != board[j] and abs(board[i] - board[j]) != abs(i - j):
                    non_attacking_pairs += 1
        return non_attacking_pairs

    def select_parents(self, population):
       
        parents = sorted(population, key=lambda x: self.fitness(x), reverse=True)[:2]
        return parents

    def crossover(self, parent1, parent2):
        
        point = random.randint(0, N - 1)
        child = parent1[:point] + parent2[point:]
        return child

    def mutate(self, board):
        
        if random.random() < self.mutation_rate:
            board[random.randint(0, N - 1)] = random.randint(0, N - 1)
        return board

    def solve(self):
        population = [self.generate_random_board() for _ in range(self.population_size)]

        for generation in range(self.generations):
            population = sorted(population, key=lambda x: self.fitness(x), reverse=True)
            if self.fitness(population[0]) == (N * (N - 1)) // 2:
                return population[0]

            new_population = []
            while len(new_population) < self.population_size:
                parent1, parent2 = self.select_parents(population)
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)
                new_population.append(child)

            population = new_population

        return None 
