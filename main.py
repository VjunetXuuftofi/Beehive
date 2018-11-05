import random
import copy
from Forager import Forager
from Controllers import forager_controller
from graphics import *
import time
import math



class Environment:
    X_SIZE = 100
    Y_SIZE = 100
    GRAPHICS_MULTIPLIER = 5
    TIMESTEPS_IN_SEASON = 100
    SEASON_TO_GENERATION_RATE = [0.001, 0.0002, 0.00001, 0.0005]
    FLOWER_LIFESPAN = 30
    MAX_CELL_CAPACITY = 20
    HIVE_X_MIN = 45
    HIVE_X_MAX = 55
    HIVE_Y_MIN = 45
    HIVE_Y_MAX = 55

    def __init__(self, subset=False):
        if not subset:
            self.flowers = {}
            self.cells = {}
            self.foragers = {}
            self.win = GraphWin(width=Environment.X_SIZE *
                                      Environment.GRAPHICS_MULTIPLIER,
                                height=Environment.Y_SIZE *
                                       Environment.GRAPHICS_MULTIPLIER,
                                autoflush=False)

    def within_distance(self, pos1, pos2, distance):
        return math.sqrt((pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2) < distance


    def produce_subset(self):
        subset = Environment(subset=True)
        


    def free_for_flowers(self):
        no_flowers = []
        for x in range(Environment.X_SIZE):
            for y in range(Environment.Y_SIZE):
                coords = (x, y)
                if coords not in self.flowers and coords not in self.cells:
                    no_flowers.append(coords)
        return no_flowers

    def generate_flowers(self, season, t):
        rate = self.SEASON_TO_GENERATION_RATE[season]
        for pos in self.free_for_flowers():
            if random.random() < rate:
                self.flowers[pos] = {
                    "birth": t
                }

    def kill_flowers(self, t):
        new_flowers = {}
        for pos, info in self.flowers.items():
            if t - info["birth"] < Environment.FLOWER_LIFESPAN:
                new_flowers[pos] = info
        self.flowers = new_flowers

    def deposit_nectar(self, pos, amount):
        if pos in self.cells:
            cell_info = self.cells[pos]
            total = cell_info["honey"] + cell_info["nectar"]
            allowed_to_deposit = min(Environment.MAX_CELL_CAPACITY - total,
                                     amount)
            cell_info["nectar"] += allowed_to_deposit
            return allowed_to_deposit
        else:
            return 0

    def manage_foragers(self):
        for pos, forager in self.foragers.items():
            forager.action_taken = False
            if forager.hunger < Forager.MAX_HUNGER:
                forager.hunger += 1
        forager_controller(self.foragers)

    def populate_cells(self):
        for x in range(Environment.HIVE_X_MIN, Environment.HIVE_X_MAX):
            for y in range(Environment.HIVE_Y_MIN, Environment.HIVE_Y_MAX):
                self.cells[(x, y)] = {"honey": 0, "nectar": 0}

    def populate_foragers(self):
        for x in range(45, 55):
            for y in range(45, 55):
                if random.random() < 0.2:
                    self.foragers[(x, y)] = Forager(self, (x, y))

    def create_point(self, pos, offset=0.):
        return Point((pos[0]+offset)*Environment.GRAPHICS_MULTIPLIER,
                     (pos[1]+offset)*Environment.GRAPHICS_MULTIPLIER)

    def pos_in_hive(self, pos):
        return Environment.HIVE_X_MIN < pos[0] < Environment.HIVE_X_MAX and \
               Environment.HIVE_Y_MIN < pos[1] < Environment.HIVE_Y_MAX

    def draw(self):
        self.win.delete("all")
        for pos, flower in self.flowers.items():
            flower_drawing = Rectangle(self.create_point(pos),
                                       self.create_point(pos, offset=1))
            flower_drawing.setOutline("white")
            flower_drawing.setFill("red")
            flower_drawing.draw(self.win)
        for pos, cell in self.cells.items():
            cell_drawing = Rectangle(self.create_point(pos),
                                     self.create_point(pos, offset=1))
            cell_drawing.setOutline("black")
            if cell["honey"] + cell["nectar"] > 0:
                cell_drawing.setFill(color_rgb(int(255-255/2/Environment.MAX_CELL_CAPACITY*cell["honey"]), int(255-255/2/Environment.MAX_CELL_CAPACITY*cell["nectar"]), 0))
            cell_drawing.draw(self.win)
        for pos, forager in self.foragers.items():
            forager_drawing = Circle(self.create_point(pos, offset=0.5),
                                     0.5*Environment.GRAPHICS_MULTIPLIER)
            forager_drawing.setOutline("black")
            forager_drawing.setFill("yellow")
            forager_drawing.draw(self.win)

    def loop(self):
        self.populate_cells()
        self.populate_foragers()
        for t in range(100000):
            season = int(t / Environment.TIMESTEPS_IN_SEASON) % 4
            self.generate_flowers(season, t)
            self.kill_flowers(t)
            self.manage_foragers()
            self.draw()
            update()
            #time.sleep(.5)

if __name__ == "__main__":
    sim = Environment()
    sim.loop()