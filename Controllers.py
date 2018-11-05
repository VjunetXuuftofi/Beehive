from Forager import Forager
import random
from copy import copy
import math


def moves(forager):
    legal_moves = []
    for x_increment in range(-1, 2):
        for y_increment in range(-1, 2):
            new_pos = (forager.pos[0] + x_increment,
                       forager.pos[1] + y_increment)
            if 0 < new_pos[0] < forager.environment.X_SIZE \
                    and 0 < new_pos[1] < forager.environment.Y_SIZE \
                    and new_pos not in forager.environment.foragers:
                legal_moves.append(new_pos)
    return legal_moves


def distance_from_center(pos, environment):
    return math.sqrt((pos[0]-environment.X_SIZE/2)**2 + (pos[1]-environment.Y_SIZE/2)**2)


def forager_controller(foragers):
    locations = list(foragers.keys())
    for pos in locations:
        forager = foragers[pos]
        if forager.pos in forager.environment.cells \
                and forager.environment.cells[pos]["nectar"] > 0:
            forager.submit_action((Forager.REDUCE_INTO_HONEY,))
        elif forager.hunger > Forager.HONEY_HUNGER_DECREASE \
                and forager.pos in forager.environment.cells and \
                forager.environment.cells[forager.pos]["honey"] > 1:
            forager.submit_action((Forager.EAT,))
        elif forager.nectar < Forager.MAX_NECTAR_CAPACITY \
                and forager.pos in forager.environment.flowers:
            forager.submit_action((Forager.FORAGE,))
        elif forager.nectar > 0 and forager.pos in forager.environment.cells \
                and forager.environment.cells[forager.pos]["nectar"] +\
                    forager.environment.cells[forager.pos]["honey"] < \
                    forager.environment.MAX_CELL_CAPACITY:
            forager.submit_action((Forager.DEPOSIT_NECTAR,))
        else:
            legal_moves = moves(forager)
            if forager.nectar < Forager.MAX_NECTAR_CAPACITY:
                move_choice = random.choice(legal_moves)
            elif forager.environment.pos_in_hive(forager.pos):
                staying_in_hive = []
                for move in legal_moves:
                    if forager.environment.pos_in_hive(move):
                        staying_in_hive.append(move)
                move_choice = random.choice(staying_in_hive)
            else:
                move_choice = min(legal_moves,
                                  key=lambda x:
                                  distance_from_center(x, forager.environment))
            forager.submit_action((Forager.MOVE, move_choice))



