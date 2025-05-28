import random
import tkinter as tk
import threading

class NQueensGenetic:
    def __init__(self, N, population_size=100, mutation_rate=0.2, generations=1000):
        self.N = N
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.generations = generations

    def generate_random_board(self):
        return [random.randint(0, self.N - 1) for _ in range(self.N)]

    def fitness(self, board):
        non_attacking_pairs = 0
        for i in range(self.N):
            for j in range(i + 1, self.N):
                if board[i] != board[j] and abs(board[i] - board[j]) != abs(i - j):
                    non_attacking_pairs += 1
        return non_attacking_pairs

    def select_parents(self, population):
        parents = sorted(population, key=lambda x: self.fitness(x), reverse=True)[:2]
        return parents

    def crossover(self, parent1, parent2):
        point = random.randint(0, self.N - 1)
        child = parent1[:point] + parent2[point:]
        return child

    def mutate(self, board):
        if random.random() < self.mutation_rate:
            board[random.randint(0, self.N - 1)] = random.randint(0, self.N - 1)
        return board

    def solve(self):
        population = [self.generate_random_board() for _ in range(self.population_size)]

        for generation in range(self.generations):
            population = sorted(population, key=lambda x: self.fitness(x), reverse=True)
            if self.fitness(population[0]) == (self.N * (self.N - 1)) // 2:
                return population[0]

            new_population = []
            while len(new_population) < self.population_size:
                parent1, parent2 = self.select_parents(population)
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)
                new_population.append(child)

            population = new_population

        return None

class NQueensGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("N-Queens Solver")
        self.geometry("450x500")

        self.input_frame = tk.Frame(self)
        self.input_frame.pack(expand=True)
        
        self.label = tk.Label(self.input_frame, text="Enter the Number of Queens:", font=("Arial", 14))
        self.label.pack(pady=5)
        
        self.entry = tk.Entry(self.input_frame, font=("Arial", 14), width=10)
        self.entry.pack(pady=5)
        self.entry.insert(0, "8")
        
        self.start_button = tk.Button(self.input_frame, text="Go", command=self.init_board, bg="#90EE90", fg="white", font=("Arial", 14, "bold"), padx=10, pady=5)
        self.start_button.pack(pady=10)

        self.canvas = tk.Canvas(self, width=400, height=400)

        self.button_frame = tk.Frame(self)
        self.ga_button = tk.Button(self.button_frame, text="GA", command=self.run_ga, bg="#90EE90", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5)
        self.ga_button.grid(row=0, column=0, padx=5)

        self.btg_button = tk.Button(self.button_frame, text="BTA", command=self.run_btg, bg="#90EE90", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5)
        self.btg_button.grid(row=0, column=1, padx=5)

        self.solution = None
        self.N = 8
    
    def init_board(self):
        try:
            self.N = int(self.entry.get())
            if self.N < 4:
                self.label.config(text="N must be ≥ 4!")
                return
            
            self.input_frame.pack_forget()
            self.canvas.pack()
            self.button_frame.pack(pady=10)

            self.draw_board()

        except ValueError:
            self.label.config(text="Please enter a valid number!")

    def draw_board(self):
        self.canvas.delete("all")
        cell_size = 400 // self.N
        for i in range(self.N):
            for j in range(self.N):
                color = "silver" if (i + j) % 2 == 0 else "white"
                self.canvas.create_rectangle(j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size, fill=color)
        
        if self.solution:
            for col, row in enumerate(self.solution):
                self.canvas.create_oval(col * cell_size + 10, row * cell_size + 10, (col + 1) * cell_size - 10, (row + 1) * cell_size - 10, fill="gold")

    def run_ga(self):
        def solve_and_update():
            genetic_solver = NQueensGenetic(self.N)
            solution = genetic_solver.solve()
            self.after(0, lambda: self.update_board(solution)) 
        
        threading.Thread(target=solve_and_update, daemon=True).start()

    def update_board(self, solution):
        self.solution = solution
        self.draw_board()

    def run_btg(self):
        print("Backtracking algorithm not implemented.")

if __name__ == "__main__":
    app = NQueensGUI()
    app.mainloop()
