import time
import copy
import matplotlib.pyplot as plt
import numpy as np
#global variables
progression = []  # to store all generations
cell_directory = {}  # to store name and cell pair info

# This class handles Menu operations
class Operations:
    def GetInput(self):
        while True:
            n = int(input("Enter number of inputs (<100) : "))
            if n>100:
                print("Enter Number less than 100")
            else: break

        i = 0
        temp_directory = {}
        while i < n:
            keys = input('Enter Name of cell : ').lower()
            values = tuple(
                map(int, input("Enter values in x,y format : ").split(",")))
            if keys not in cell_directory.keys() and keys not in temp_directory.keys():
                temp_directory[keys] = values
                i += 1
            else:
                print("Already present!")
        cell_directory.update(temp_directory)
        res = set(temp_directory.values())
        if not progression:
            progression.append(res)
        else:
            progression[-1] = progression[-1].union(res)
        return progression[-1]

    
# this method handles search using name and prints whether cell is alive or dead
    def search(self,name):
        if name in cell_directory.keys():
            x = cell_directory[name]
            res = progression[-1]
            if x in res:
                print("Alive")
            else:
                print("Dead")
        else:
            print("Key does not exist!")
        
#This method visualizes all generations on a scatterplot
    def visualize(self):   
        plt.ion()
        fig, ax = plt.subplots()
        x, y = [], []
        sc = ax.scatter(x, y)
        plt.xlim(0, MAX_SIZE)
        plt.ylim(0, MAX_SIZE)
        plt.draw()
        for i in progression:
            x = list(map(lambda x: x[0], i))
            y = list(map(lambda x: x[1], i))
            sc.set_offsets(np.c_[x, y])
            fig.canvas.draw_idle()
            plt.pause(2)
        plt.waitforbuttonpress()
        
#Grid handler class
class Game:
    def __init__(self, initial_state, rules, max_size):
        self.current_state = initial_state
        self.rules = rules
        self.max_size = max_size


    def setState(self, board):
        self.current_state = SetGridState(board)

    #next generation handler definition
    def next_gen(self):
        state = copy.deepcopy(self.current_state)
        state.grid = state.apply_rules(self.rules, self.max_size).grid
        progression.append(state.grid)
        # return progression

#Rules for cells to decide which cells live and which one's die
class SetGridRules():
    def apply_rules(self, grid, max_size, get_neighbours):
        counter = {}
        for cell in grid:
            if cell not in counter:
                counter[cell] = 0
            nb = get_neighbours(cell, max_size)
            for n in nb:
                if n not in counter:
                    counter[n] = 1
                else:
                    counter[n] += 1
        for c in counter:
            if (counter[c] < 2 or counter[c] > 3):
                grid.discard(c)
            if counter[c] == 3:
                grid.add(c)
        return grid

#handle current state of cells in the grid
class SetGridState():
    def __init__(self, grid):
        self.grid = grid

    def get_neighbours(self, cell, max_size):
        # Returns the neighbours of a live cell if they lie within the bounds of the grid specified by max_size
        l = []
        if cell[0]-1 >= 0:
            l.append((cell[0]-1, cell[1]))
        if cell[0]-1 >= 0 and cell[1]-1 >= 0:
            l.append((cell[0]-1, cell[1]-1))
        if cell[0]-1 >= 0 and cell[1]+1 < max_size:
            l.append((cell[0]-1, cell[1]+1))
        if cell[1]-1 >= 0:
            l.append((cell[0], cell[1]-1))
        if cell[1]-1 >= 0 and cell[0]+1 < max_size:
            l.append((cell[0]+1, cell[1]-1))
        if cell[1]+1 < max_size:
            l.append((cell[0], cell[1]+1))
        if cell[0]+1 < max_size:
            l.append((cell[0]+1, cell[1]))
        if cell[1]+1 < max_size and cell[0]+1 < max_size:
            l.append((cell[0]+1, cell[1]+1))
        return l

    def equals(self, other):
        if other is None:
            return False
        return self.grid == other.grid

    def apply_rules(self, rules, max_size):
        # Calls the actual rules and provides them with the grid and the neighbour function
        self.grid = rules.apply_rules(self.grid, max_size, self.get_neighbours)
        return self


# main
#Maximum size of grid (Can be changed as per user requirement)
MAX_SIZE = 500
ops = Operations()
board = {}
rules = SetGridRules()
game = Game(SetGridState(board), rules, MAX_SIZE)
while True:
    ch = int(input('''
    MENU:
        1. New input
        2. Search
        3. visualize generations
        4. Next Generation for current state 
        5. Next Nth generation for current state
        6. Exit!
        Enter your choice : '''))
    if ch == 1:
        board = ops.GetInput()
        game.setState(board)
        game.next_gen()
    elif ch == 2:
        if not progression:
            print("No entries to search! Insert entries first")
        else:
            key = input("Enter string to search : ").lower()
            ops.search(key)
    elif ch == 3:
        if not progression:
            print("No entries to Visualize! Insert entries first")
        else:
            ops.visualize() 
    elif ch == 4:
        if progression:
            game.setState(progression[-1])
            game.next_gen()
            print("Advanced 1 generation/tick")
        else:
            print("Empty current generation, Insert entries First!")

    elif ch == 5:
        if progression: 
            n = int(input("Enter number of generations to Advance : "))
            for _ in range(n):
                game.setState(progression[-1])
                game.next_gen()
    elif ch == 6:
        exit()
    else:
        print("Enter a valid choice! ")